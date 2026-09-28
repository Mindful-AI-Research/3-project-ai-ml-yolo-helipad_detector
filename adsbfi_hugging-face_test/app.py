import gradio as gr
import requests
import spaces
from datetime import datetime

# São Paulo city center, 50 nm radius (~92 km) — comfortably covers Greater São
# Paulo. adsb.fi's own hard cap on this endpoint is 250 nm.
LAT, LON, DIST_NM = -23.55, -46.63, 50
URL = f"https://opendata.adsb.fi/api/v2/lat/{LAT}/lon/{LON}/dist/{DIST_NM}"


@spaces.GPU
def test_connection():
    ts = datetime.now().strftime("%H:%M:%S")
    try:
        resp = requests.get(URL, timeout=(5, 12))
        resp.raise_for_status()
        data = resp.json()
        aircraft = data.get("ac") or []
        return (
            f"[{ts}] ✅ Conectou! HTTP {resp.status_code} — "
            f"{len(aircraft)} aeronave(s) num raio de {DIST_NM} nm de São Paulo.\n\n"
            f"Resposta crua (pra ver os campos reais, ex: 't' = tipo da aeronave):\n\n{data}"
        )
    except requests.exceptions.RequestException as exc:
        return f"[{ts}] ❌ Não conectou: {exc}"


with gr.Blocks(title="Teste de Conexão — adsb.fi") as demo:
    gr.Markdown("## 🛩️ Teste de Conexão com o adsb.fi")
    gr.Markdown(
        "App mínimo, só pra confirmar (1) se esta hospedagem consegue alcançar o "
        "adsb.fi, e (2) se a resposta traz o campo `t` (tipo da aeronave, ex: "
        "'R44', 'EC35') — é isso que permitiria identificar helicóptero de verdade, "
        "em vez de heurística por callsign."
    )
    btn = gr.Button("🔄 Testar conexão agora")
    output = gr.Textbox(label="Resultado", lines=18)
    btn.click(fn=test_connection, outputs=output)

demo.launch()
