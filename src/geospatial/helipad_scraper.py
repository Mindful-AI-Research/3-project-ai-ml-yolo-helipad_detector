import argparse
import csv
import os
import re
import sys
import time
from datetime import datetime
from typing import Optional, List, Dict

try:
    from selenium import webdriver
    from selenium.webdriver.common.by import By
    from selenium.webdriver.firefox.options import Options as FirefoxOptions
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    from selenium.common.exceptions import TimeoutException, WebDriverException
except ImportError:
    sys.exit("[ERRO] Selenium não encontrado. Rode:  pip install selenium")

BASE = "https://www.flightmarket.com.br"

ICAO_RE = re.compile(r"/pt/aeroportos/([A-Z]{4})\b")

_SEP  = r"[^0-9NSEWnsew]{0,3}"
_SEP2 = r"[^0-9NSEWnsew]{1,8}"
COORD_RE = re.compile(
    rf"(\d{{1,3}}){_SEP}(\d{{1,2}}){_SEP}(\d{{1,2}}(?:[.,]\d+)?){_SEP}([NSns])"
    rf"{_SEP2}(\d{{1,3}}){_SEP}(\d{{1,2}}){_SEP}(\d{{1,2}}(?:[.,]\d+)?){_SEP}([EWew])"
)

LOC_RE = re.compile(r"Localiza[cç][aã]o\s*[:\-]?\s*([^\n]+)")

DEFAULT_ESTADOS = [
    "RJ", "MG", "RS", "PR", "BA",
    "CE", "GO", "SC", "PE", "DF",
    "AM", "PA", "ES", "MT", "MS",
]

CSV_HEADER = ["Carimbo de data/hora", "Coordenadas da Bounding Box", "Nome do Bairro"]


def _dms_para_decimal(d: str, m: str, s: str, h: str) -> float:
    v = float(d) + float(m) / 60 + float(str(s).replace(",", ".")) / 3600
    return -v if h.upper() in ("S", "W") else v


def _formatar_dms(d1, m1, s1, h1, d2, m2, s2, h2) -> str:
    def _norm(d, m, s):
        s = round(float(str(s).replace(",", ".")))
        if s >= 60:
            s -= 60
            m += 1
        if m >= 60:
            m -= 60
            d += 1
        return int(d), int(m), int(s)

    d1n, m1n, s1n = _norm(int(d1), int(m1), s1)
    d2n, m2n, s2n = _norm(int(d2), int(m2), s2)

    lat_str = f"{d1n}°{m1n}'{s1n}\"{h1.upper()}"
    lon_str = f"{d2n}°{m2n}'{s2n}\"{h2.upper()}"
    return f"{lat_str} {lon_str}"


def parse_coords(texto: str):
    m = COORD_RE.search(texto)
    if not m:
        return None, None, ""
    d1, m1, s1, h1, d2, m2, s2, h2 = m.groups()
    lat = _dms_para_decimal(d1, m1, s1, h1)
    lon = _dms_para_decimal(d2, m2, s2, h2)
    dms = _formatar_dms(d1, m1, s1, h1, d2, m2, s2, h2)
    return lat, lon, dms

def extrair_cidade(texto: str) -> str:
    m = LOC_RE.search(texto)  # Procura por "Localização: ..."
    if m:
        loc = m.group(1).strip(" ·-")
        return loc.split(" - ")[0].strip()
    return ""


def extrair_nome(titulo: str, icao: str) -> str:
    partes = [p.strip() for p in titulo.split(" - ") if p.strip()]
    if len(partes) >= 2:
        nome = re.sub(r"(?i)^helip\w+\s+", "", partes[1]).strip()
        if nome:
            return nome
    return icao


def eh_heliponto(titulo: str, texto: str) -> bool:
    palavras = ("heliport", "heliponto", "heliporto")
    titulo_lower = titulo.lower()
    texto_lower  = texto.lower()
    return any(p in titulo_lower or p in texto_lower for p in palavras)


def geocode_bairro(lat, lon) -> str:
    # Faz busca reversa nas coordenadas
    # Retorna: suburb, neighbourhood, quarter, city_district, city, town
    if lat is None or lon is None:
        return ""
    try:
        import requests
        resp = requests.get(
            "https://nominatim.openstreetmap.org/reverse",
            params={
                "lat": lat, "lon": lon,
                "format": "jsonv2",
                "zoom": 16,
                "addressdetails": 1,
            },
            headers={"User-Agent": "helipontos-cidades-csv/2.0 (estudo pessoal)"},
            timeout=10,
        )
        addr = resp.json().get("address", {})
        return (
            addr.get("suburb")
            or addr.get("neighbourhood")
            or addr.get("quarter")
            or addr.get("city_district")
            or addr.get("city")
            or addr.get("town")
            or ""
        )
    except Exception:
        return ""
    finally:
        time.sleep(1.0)


def make_driver(headless: bool = True) -> webdriver.Firefox:
    opts = FirefoxOptions()
    if headless:
        opts.add_argument("-headless")
    driver = webdriver.Firefox(options=opts)
    driver.set_page_load_timeout(30)
    return driver


def coletar_icaos_do_estado(
    driver: webdriver.Firefox,
    estado: str,
    alvo: int,
    max_iter: int = 30,
    espera: float = 1.3,
) -> List[str]:
    seed_url = f"{BASE}/pt/aeroportos/{estado}"
    print(f"    Carregando: {seed_url}")
    try:
        driver.get(seed_url)
    except WebDriverException as exc:
        print(f"    ⚠  Falha ao carregar página do estado {estado}: {exc}")
        return []

    encontrados: set = set()
    sem_novos = 0

    for iteracao in range(max_iter):
        antes = len(encontrados)

        for el in driver.find_elements(By.CSS_SELECTOR, "a[href*='/pt/aeroportos/']"):
            href = el.get_attribute("href") or ""
            m = ICAO_RE.search(href)
            if m:
                encontrados.add(m.group(1))

        if len(encontrados) == antes:
            sem_novos += 1
        else:
            sem_novos = 0

        if sem_novos >= 3 or len(encontrados) >= max(alvo * 5, 50):
            break

        botao_clicado = False
        for rotulo in ("Próxima", "Proxima", "próxima", "Carregar mais", "›", ">", "next"):
            try:
                btn = driver.find_element(
                    By.XPATH,
                    f"//*[contains(normalize-space(.), '{rotulo}')]"
                )
                driver.execute_script("arguments[0].scrollIntoView(true);", btn)
                btn.click()
                time.sleep(espera)
                botao_clicado = True
                break
            except Exception:
                pass

        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(espera)

    return list(encontrados)


def extrair_entry(
    driver: webdriver.Firefox,
    icao: str,
    geocode: bool = False,
    wait_secs: float = 12,
) -> Optional[Dict]:
    url = f"{BASE}/pt/aeroportos/{icao}"
    try:
        driver.get(url)
        WebDriverWait(driver, wait_secs).until(
            EC.presence_of_element_located(
                (By.XPATH, "//*[contains(text(),'Coordenadas')]")
            )
        )
    except (TimeoutException, WebDriverException):
        return None

    titulo = driver.title or ""
    texto  = driver.find_element(By.TAG_NAME, "body").text

    if not eh_heliponto(titulo, texto):
        return None

    lat, lon, dms = parse_coords(texto)
    if not dms:
        return None

    cidade = extrair_cidade(texto)
    
    # Tenta geocoding primeiro para obter o nome real
    if lat is not None and lon is not None:
        bairro = geocode_bairro(lat, lon)
    else:
        bairro = ""
    
    # Se geocoding falhou, tenta usar a cidade extraída do site
    if not bairro:
        bairro = cidade
    
    # Se tudo falhou, usa o código ICAO como último recurso
    if not bairro:
        bairro = icao

    return {
        "ts":      datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
        "coords":  dms,
        "bairro":  bairro,
        "icao":    icao,
        "nome":    extrair_nome(titulo, icao),
        "url":     url,
        "estado":  "",
    }


def append_csv(entry: Dict, path: str) -> None:
    novo = not (os.path.isfile(path) and os.path.getsize(path) > 0)
    with open(path, "a", newline="", encoding="utf-8-sig") as f:
        w = csv.writer(f, quoting=csv.QUOTE_MINIMAL)
        if novo:
            w.writerow(CSV_HEADER)
        w.writerow([entry["ts"], entry["coords"], entry["bairro"]])


def mostrar_menu():
    print("\n" + "=" * 60)
    print("  COLETA DE HELIPONTOS - FlightMarket")
    print("=" * 60 + "\n")
    
    while True:
        print("Quantos helipontos deseja coletar?")
        print("(Digite um número entre 1 e 500)")
        try:
            quantidade = int(input("\nQuantidade: "))
            if 1 <= quantidade <= 500:
                return quantidade
            else:
                print("[ERRO] Digite um número entre 1 e 500.\n")
        except (ValueError, EOFError):
            print("[ERRO] Digite um número válido.\n")

def main() -> None:
    quantidade = mostrar_menu()
    
    ap = argparse.ArgumentParser(
        description="Coleta helipontos do FlightMarket (sem SP) → CSV formatado",
    )
    ap.add_argument(
        "--estados", nargs="+", default=DEFAULT_ESTADOS,
        metavar="UF",
        help="Siglas dos estados a varrer (ex: RJ MG RS). SP é sempre ignorado.",
    )
    ap.add_argument(
        "--output", default="helipontos_resultado.csv",
        help="Caminho do arquivo CSV de saída (padrão: helipontos_resultado.csv).",
    )
    ap.add_argument(
        "--no-headless", action="store_true",
        help="Exibe o Firefox na tela (útil para depuração).",
    )
    ap.add_argument(
        "--geocode", action="store_true", default=True,
        help="Busca o bairro real via Nominatim/OSM — mais preciso, mas lento (1 req/seg).",
    )
    ap.add_argument(
        "--delay", type=float, default=1.5,
        help="Pausa em segundos entre requisições de páginas (padrão: 1.5).",
    )
    args = ap.parse_args()

    estados = [e.upper() for e in args.estados if e.upper() != "SP"]
    if not estados:
        sys.exit("[ERRO] Nenhum estado válido informado (SP não é permitido).")

    if quantidade <= 0:
        sys.exit("[ERRO] A quantidade precisa ser maior que zero.")
    print()
    print("=" * 60)
    print("  COLETA DE HELIPONTOS - FlightMarket")
    print("=" * 60)
    print(f"  Estados : {', '.join(estados)}")
    print(f"  Meta    : {quantidade} heliponto(s)")
    print(f"  Saída   : {args.output}")
    print(f"  Geocode : {'sim (OSM/Nominatim)' if args.geocode else 'não (cidade do site)'}")
    print(f"  Firefox : {'visível' if args.no_headless else 'headless'}")
    print("=" * 60)
    print()

    try:
        driver = make_driver(headless=not args.no_headless)
    except WebDriverException as exc:
        sys.exit(
            f"[ERRO] Não foi possível iniciar o Firefox.\n"
            f"   Verifique se firefox + geckodriver estão instalados.\n"
            f"   Detalhe: {exc}"
        )

    coletados: List[Dict] = []
    visitados: set        = set()
    por_estado: Dict[str, int] = {}

    try:
        for estado in estados:
            if len(coletados) >= quantidade:
                break

            faltam = quantidade - len(coletados)
            print(f"\n{'─'*60}")
            print(f"  Estado: {estado}  │  Restam: {faltam}  │  "
                  f"Total: {len(coletados)}/{quantidade}")
            print(f"{'─'*60}")

            icaos = coletar_icaos_do_estado(driver, estado, faltam, espera=args.delay)
            novos = [i for i in icaos if i not in visitados]
            print(f"    {len(icaos)} candidato(s) encontrado(s) ({len(novos)} novo(s))\n")

            por_estado[estado] = 0

            for icao in novos:
                if len(coletados) >= quantidade:
                    break

                visitados.add(icao)
                print(f"    [{len(coletados)+1:3d}/{quantidade}] {icao}  ...", end="  ", flush=True)

                try:
                    entry = extrair_entry(
                        driver, icao,
                        geocode=args.geocode,
                        wait_secs=12,
                    )
                except Exception as exc:
                    print(f"ERRO: {exc}")
                    continue

                if entry is None:
                    print("não é heliponto / sem coordenadas — pulando")
                    continue

                entry["estado"] = estado
                print(f"✓  {entry['coords']}  ←  {entry['bairro']}")

                coletados.append(entry)
                por_estado[estado] = por_estado.get(estado, 0) + 1
                append_csv(entry, args.output)
                time.sleep(args.delay)

    except KeyboardInterrupt:
        print("\n\n⚠  Interrompido pelo usuário.")

    finally:
        driver.quit()

    print()
    print("=" * 60)
    print(f"  [SUCESSO] Concluído! {len(coletados)} heliponto(s) coletado(s)")
    print(f"  [ARQUIVO] Arquivo: {os.path.abspath(args.output)}")
    print()
    if por_estado:
        print("  Por estado:")
        for uf, qtd in por_estado.items():
            if qtd > 0:
                print(f"    {uf}: {qtd}")
    print("=" * 60)


if __name__ == "__main__":
    main()
