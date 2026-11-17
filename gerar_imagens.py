"""Gera favicon/apple-touch/logo 512 e a imagem de compartilhamento (OG) a partir do simbolo.svg."""
from pathlib import Path
from playwright.sync_api import sync_playwright
IMG = Path(__file__).parent / "src/static/assets/img"
svg = (IMG / "simbolo.svg").read_text()
import base64
# Fonte embutida: set_content roda em about:blank, que não carrega file:// (caía em serifa)
font = "data:font/woff2;base64," + base64.b64encode((Path(__file__).parent / "src/static/assets/fonts/manrope-latin-wght-normal.woff2").read_bytes()).decode()
css = f"@font-face{{font-family:M;src:url({font}) format('woff2');font-weight:200 800}}body{{margin:0;font-family:M}}"
quad = lambda s, pad: f"<style>{css}</style><div style='width:{s}px;height:{s}px;background:#152B1C;display:grid;place-items:center;border-radius:{s//5}px'><div style='width:{s-2*pad}px'>{svg}</div></div>"
og = f"""<style>{css}</style><div style="width:1200px;height:630px;background:#152B1C;color:#F4F1E6;display:flex;align-items:center;gap:64px;padding:0 90px;box-sizing:border-box;position:relative;overflow:hidden">
<div style="position:absolute;right:-120px;bottom:-200px;width:700px;height:700px;background:radial-gradient(closest-side,rgba(140,203,94,.18),transparent)"></div>
<div style="width:300px;flex:none">{svg}</div>
<div><div style="font-weight:800;letter-spacing:.18em;font-size:30px">CAMPO <span style="color:#8CCB5E">DIGITAL</span></div>
<div style="font-weight:800;font-size:58px;line-height:1.08;letter-spacing:-.02em;margin-top:22px">Agentes que trabalham pela sua operação.</div>
<div style="font-size:30px;color:#8CCB5E;font-weight:700;margin-top:18px">Pelo WhatsApp, sem app novo.</div></div></div>"""
og_granja = f"""<style>{css}</style><div style="width:1200px;height:630px;background:linear-gradient(135deg,#152B1C 0%,#1A2E20 55%,#22402A 100%);color:#F4F1E6;display:flex;align-items:center;gap:64px;padding:0 90px;box-sizing:border-box;position:relative;overflow:hidden">
<div style="position:absolute;right:-120px;bottom:-200px;width:700px;height:700px;background:radial-gradient(closest-side,rgba(140,203,94,.14),transparent)"></div>
<div style="width:270px;flex:none">{svg}</div>
<div><div style="font-weight:800;letter-spacing:.18em;font-size:28px">GRANJA <span style="color:#8CCB5E">DIGITAL</span></div>
<div style="font-weight:700;letter-spacing:.12em;font-size:15px;color:#B9CDB9;margin-top:10px">BY CAMPO DIGITAL · SUINOCULTURA</div>
<div style="font-weight:800;font-size:50px;line-height:1.12;letter-spacing:-.01em;margin-top:22px">Você diz a idade do lote.<br><span style="color:#8CCB5E">O agente diz o peso estimado.</span></div>
<div style="font-size:24px;color:#8CCB5E;font-weight:700;margin-top:22px">Pelo WhatsApp. Teste grátis de 14 dias.</div></div></div>"""
jobs = [("favicon-32.png", quad(32, 3), 32, 32, False), ("apple-touch-icon.png", quad(180, 22), 180, 180, False),
        ("campo-digital-512.png", quad(512, 60), 512, 512, False), ("og-campo-digital.png", og, 1200, 630, False),
        ("og-granja-digital.png", og_granja, 1200, 630, False)]
import sys
so = [a for a in sys.argv[1:]]  # opcional: só os arquivos citados, ex.: python gerar_imagens.py og-granja-digital.png
with sync_playwright() as p:
    b = p.chromium.launch()
    for nome, html, w, h, _ in jobs:
        if so and nome not in so:
            continue
        pg = b.new_page(viewport={"width": w, "height": h})
        pg.set_content(html); pg.wait_for_timeout(300)
        pg.screenshot(path=str(IMG / nome), omit_background=nome.startswith("favicon"))
        print("ok", nome)
    b.close()
