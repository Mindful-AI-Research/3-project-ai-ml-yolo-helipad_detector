import csv
import re
import sys
from pathlib import Path

_NUM = r"[-+]?\d+(?:\.\d+)?"
_COORD_RE = re.compile(
    rf"""
    (?P<g>{_NUM})\s*[°ºo]?\s*
    (?:(?P<m>{_NUM})\s*['’′]?\s*)?
    (?:(?P<s>{_NUM})\s*["”″]?\s*)?
    (?P<dir>[NSEWnsew])?
    """,
    re.VERBOSE,
)

# Margem ao redor do ponto, em graus decimais.
# 0.0005 graus equivale a aproximadamente 55 metros.
MARGEM = 0.0005

COLUNA_COORD = "Coordenadas da Bounding Box"


def dms_to_dd(graus, minutos, segundos, direcao=""):
    dd = abs(graus) + minutos / 60 + segundos / 3600
    if direcao.upper() in ("S", "W") or graus < 0:
        dd = -dd
    return dd


def parse_dms_pair(texto):
    coords = []
    for m in _COORD_RE.finditer(texto):
        if m.group("g") is None or m.group(0).strip() == "":
            continue
        graus = float(m.group("g"))
        minutos = float(m.group("m")) if m.group("m") else 0.0
        segundos = float(m.group("s")) if m.group("s") else 0.0
        direcao = m.group("dir") or ""
        coords.append(dms_to_dd(graus, minutos, segundos, direcao))
    if len(coords) < 2:
        raise ValueError(f"coordenada inválida: {texto!r}")
    return coords[0], coords[1]  # lat, lon


def bbox_para_ponto(texto_coord):
    lat, lon = parse_dms_pair(texto_coord)
    lon_min = lon - MARGEM
    lon_max = lon + MARGEM
    lat_min = lat - MARGEM
    lat_max = lat + MARGEM
    return f"{lon_min:.6f}\t{lat_min:.6f}\t{lon_max:.6f}\t{lat_max:.6f}"


def processar(entrada: Path, saida: Path):
    if not entrada.exists():
        print(f"Erro: arquivo não encontrado -> {entrada}")
        sys.exit(1)

    with open(entrada, newline="", encoding="utf-8-sig") as f_in:
        reader = csv.DictReader(f_in)
        fieldnames = reader.fieldnames

        if not fieldnames or COLUNA_COORD not in fieldnames:
            print(f"Erro: coluna '{COLUNA_COORD}' não encontrada no CSV.")
            print(f"Colunas encontradas: {fieldnames}")
            sys.exit(1)

        linhas = list(reader)

    convertidas = 0
    falhas = 0

    with open(saida, "w", newline="", encoding="utf-8") as f_out:
        writer = csv.DictWriter(f_out, fieldnames=fieldnames)
        writer.writeheader()
        for i, linha in enumerate(linhas, start=2):  # linha 1 = cabeçalho
            coord_original = linha.get(COLUNA_COORD, "")
            try:
                linha[COLUNA_COORD] = bbox_para_ponto(coord_original)
                convertidas += 1
            except ValueError as e:
                print(f"Aviso (linha {i}): {e} -> mantida sem alteração")
                falhas += 1
            writer.writerow(linha)

    print(f"\nConcluído: {convertidas} linha(s) convertida(s), {falhas} falha(s).")
    print(f"Arquivo gerado: {saida}")


def main():
    if len(sys.argv) >= 3:
        entrada = Path(sys.argv[1])
        saida = Path(sys.argv[2])
    elif len(sys.argv) == 2:
        entrada = Path(sys.argv[1])
        saida = entrada.with_name(entrada.stem + "_bbox.csv")
    else:
        # Procura os arquivos na mesma pasta do script
        script_dir = Path(__file__).parent
        entrada = script_dir / "helipontos_resultado.csv"
        saida = script_dir / "cordenadasheli.csv"

    processar(entrada, saida)


if __name__ == "__main__":
    main()