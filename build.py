#!/usr/bin/env python3
"""Gera o site estático da Campo Digital em ./dist a partir de ./src.

Uso:  python build.py
Tudo que muda com frequência (WhatsApp, preços, domínio) está em CONFIG abaixo.
Cada página em src/pages/*.html começa com um bloco de metadados entre linhas '---'.
Marcadores aceitos no conteúdo:
  {{wa:Mensagem pronta}}  -> link wa.me com a mensagem já preenchida
  {{icone:nome}}          -> ícone SVG em linha
  {{cfg:chave}}           -> valor de CONFIG
"""
import html, json, re, shutil, urllib.parse
from datetime import date
from pathlib import Path

RAIZ = Path(__file__).parent
SRC, DIST = RAIZ / "src", RAIZ / "dist"

CONFIG = {
    "dominio": "https://campodigital.com.br",
    "whatsapp": "5548996373942",            # número comercial (só dígitos, com DDI)
    "whatsapp_legivel": "(48) 99637-3942",
    "preco_fazenda_a_partir": "R$ 149",      # "a partir de" (decisão 01/10/2026)
    "gratis_lancamentos": "40",
    "ano": str(date.today().year),
    "cidade": "Florianópolis, SC",
}

ICONES = {
    "mic": '<path d="M12 3a3 3 0 0 0-3 3v6a3 3 0 0 0 6 0V6a3 3 0 0 0-3-3z"/><path d="M19 11a7 7 0 0 1-14 0"/><path d="M12 18v3"/>',
    "camera": '<path d="M4 8h3l2-3h6l2 3h3v11H4z"/><circle cx="12" cy="13" r="3.5"/>',
    "pergunta": '<path d="M4 5h16v11H9l-5 4z"/><path d="M10 9.5a2 2 0 1 1 2.6 1.9c-.4.2-.6.5-.6.9v.2"/><path d="M12 14.5h.01"/>',
    "sino": '<path d="M6 16v-5a6 6 0 0 1 12 0v5l2 2H4z"/><path d="M10 20a2 2 0 0 0 4 0"/>',
    "sol": '<circle cx="12" cy="12" r="4"/><path d="M12 2v2M12 20v2M4.9 4.9l1.4 1.4M17.7 17.7l1.4 1.4M2 12h2M20 12h2M4.9 19.1l1.4-1.4M17.7 6.3l1.4-1.4"/>',
    "confere": '<path d="M6 3h9l4 4v14H6z"/><path d="M9 13l2 2 4-4"/>',
    "registra": '<path d="M4 20h4L19 9l-4-4L4 16z"/><path d="M13 7l4 4"/>',
    "grafico": '<path d="M4 20V4M4 20h16"/><path d="M8 16v-4M12 16V8M16 16v-6"/>',
    "cadeado": '<rect x="5" y="11" width="14" height="9" rx="2"/><path d="M8 11V8a4 4 0 0 1 8 0v3"/>',
    "pessoa": '<circle cx="12" cy="8" r="4"/><path d="M4 21a8 8 0 0 1 16 0"/>',
    "termometro": '<path d="M14 14.8V5a2 2 0 0 0-4 0v9.8a4 4 0 1 0 4 0z"/><path d="M12 9v7"/>',
    "silo": '<path d="M6 9a6 4 0 0 1 12 0v12H6z"/><path d="M6 13h12M6 17h12"/>',
    "relogio": '<circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 2"/>',
    "cotacao": '<path d="M3 17l6-6 4 4 8-8"/><path d="M15 7h6v6"/>',
    "vento": '<path d="M3 8h11a3 3 0 1 0-3-3"/><path d="M3 12h16a3 3 0 1 1-3 3"/><path d="M3 16h7"/>',
    "engrenagem": '<circle cx="12" cy="12" r="3"/><path d="M12 2v3M12 19v3M2 12h3M19 12h3M5 5l2 2M17 17l2 2M5 19l2-2M17 7l2-2"/>',
    "caixa": '<path d="M3 13h5l2 3h4l2-3h5"/><path d="M5 5h14l2 8v6H3v-6z"/>',
    "link": '<path d="M10 14a4 4 0 0 0 5.7 0l3-3a4 4 0 0 0-5.7-5.7l-1 1"/><path d="M14 10a4 4 0 0 0-5.7 0l-3 3a4 4 0 0 0 5.7 5.7l1-1"/>',
    "escudo": '<path d="M12 3l8 3v6c0 5-3.5 8-8 9-4.5-1-8-4-8-9V6z"/><path d="M9 12l2 2 4-4"/>',
    "x": '<path d="M6 6l12 12M18 6L6 18"/>',
    "ok": '<path d="M5 12l5 5 9-10"/>',
    "seta": '<path d="M5 12h14M13 6l6 6-6 6"/>',
    "documentos": '<path d="M8 3h8l4 4v12H8z"/><path d="M4 7v14h12"/>',
    "dinheiro": '<rect x="3" y="6" width="18" height="12" rx="2"/><circle cx="12" cy="12" r="2.5"/><path d="M7 12h.01M17 12h.01"/>',
    "lista": '<path d="M9 6h11M9 12h11M9 18h11"/><path d="M4 6h.01M4 12h.01M4 18h.01"/>',
    "folha": '<path d="M5 19c0-8 5-14 15-14 0 10-6 15-14 15"/><path d="M5 19l7-7"/>',
    "ovo": '<path d="M12 3c-4 0-7 6-7 10a7 7 0 0 0 14 0c0-4-3-10-7-10z"/>',
    "gota": '<path d="M12 3s-6 7-6 11a6 6 0 0 0 12 0c0-4-6-11-6-11z"/>',
}
WA_SVG = ('<svg viewBox="0 0 24 24" aria-hidden="true" fill="currentColor"><path d="M17.472 14.382c-.297-.149-1.758-.867-2.03-.967-.273-.099-.471-.148-.67.15-.197.297-.767.966-.94 1.164-.173.199-.347.223-.644.075-.297-.15-1.255-.463-2.39-1.475-.883-.788-1.48-1.761-1.653-2.059-.173-.297-.018-.458.13-.606.134-.133.298-.347.446-.52.149-.174.198-.298.298-.497.099-.198.05-.371-.025-.52-.075-.149-.669-1.612-.916-2.207-.242-.579-.487-.5-.669-.51-.173-.008-.371-.01-.57-.01-.198 0-.52.074-.792.372-.272.297-1.04 1.016-1.04 2.479 0 1.462 1.065 2.875 1.213 3.074.149.198 2.096 3.2 5.077 4.487.709.306 1.262.489 1.694.625.712.227 1.36.195 1.871.118.571-.085 1.758-.719 2.006-1.413.248-.694.248-1.289.173-1.413-.074-.124-.272-.198-.57-.347m-5.421 7.403h-.004a9.87 9.87 0 01-5.031-1.378l-.361-.214-3.741.982.998-3.648-.235-.374a9.86 9.86 0 01-1.51-5.26c.001-5.45 4.436-9.884 9.888-9.884 2.64 0 5.122 1.03 6.988 2.898a9.825 9.825 0 012.893 6.994c-.003 5.45-4.437 9.884-9.885 9.884m8.413-18.297A11.815 11.815 0 0012.05 0C5.495 0 .16 5.335.157 11.892c0 2.096.547 4.142 1.588 5.945L.057 24l6.305-1.654a11.882 11.882 0 005.683 1.448h.005c6.554 0 11.89-5.335 11.893-11.893a11.821 11.821 0 00-3.48-8.413Z"/></svg>')

NAV = [
    ("/", "Início", "inicio"),
    ("/fazenda-digital/", "Fazenda Digital", "fazenda"),
    ("/armazem-digital/", "Armazém Digital", "armazem"),
    ("/projetos/", "Projetos sob medida", "projetos"),
    ("/#quem-somos", "Quem somos", "quem"),
]


def icone(nome):
    return f'<svg viewBox="0 0 24 24" aria-hidden="true">{ICONES[nome]}</svg>'


def wa(msg):
    return f"https://wa.me/{CONFIG['whatsapp']}?text=" + urllib.parse.quote(msg)


def expandir(txt):
    txt = re.sub(r"\{\{wa:(.+?)\}\}", lambda m: html.escape(wa(m.group(1)), quote=True), txt)
    txt = re.sub(r"\{\{icone:(\w+)\}\}", lambda m: icone(m.group(1)), txt)
    txt = txt.replace("{{wa_svg}}", WA_SVG)
    txt = re.sub(r"\{\{cfg:(\w+)\}\}", lambda m: CONFIG[m.group(1)], txt)
    return txt


def ler_pagina(p):
    bruto = p.read_text(encoding="utf-8")
    _, meta, corpo = bruto.split("---", 2)
    dados = {}
    for linha in meta.strip().splitlines():
        k, v = linha.split(":", 1)
        dados[k.strip()] = v.strip()
    return dados, corpo


def layout(meta, corpo):
    caminho = meta["caminho"]
    url = CONFIG["dominio"] + caminho
    titulo = meta["titulo"]
    desc = meta["descricao"]
    ativo = meta.get("nav", "")
    itens = []
    for href, rotulo, chave in NAV:
        cur = ' aria-current="page"' if chave == ativo else ""
        itens.append(f'<a href="{href}"{cur}>{rotulo}</a>')
    msg_topo = meta.get("wa_topo", "Olá! Vim pelo site da Campo Digital e quero conhecer os agentes.")
    noindex = '<meta name="robots" content="noindex">' if meta.get("noindex") else ""
    jsonld = ""
    if caminho == "/":
        jsonld = '<script type="application/ld+json">' + json.dumps({
            "@context": "https://schema.org", "@type": "Organization",
            "name": "Campo Digital", "url": CONFIG["dominio"],
            "logo": CONFIG["dominio"] + "/assets/img/campo-digital-512.png",
            "description": desc,
            "address": {"@type": "PostalAddress", "addressLocality": "Florianópolis", "addressRegion": "SC", "addressCountry": "BR"},
            "contactPoint": {"@type": "ContactPoint", "contactType": "sales", "telephone": "+" + CONFIG["whatsapp"], "availableLanguage": "Portuguese"},
        }, ensure_ascii=False) + "</script>"
    classe_body = f' class="{meta["classe_body"]}"' if meta.get("classe_body") else ""
    js_extra = "".join(f'\n<script src="{j.strip()}" defer></script>' for j in meta.get("js", "").split(",") if j.strip())
    flutuante = "" if meta.get("sem_flutuante") else (
        f'<a class="wa-flutuante" href="{html.escape(wa(msg_topo), quote=True)}" target="_blank" rel="noopener" '
        f'aria-label="Falar no WhatsApp" style="color:#152B1C">{WA_SVG}</a>')
    return f"""<!doctype html>
<html lang="pt-BR" class="sem-js">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{titulo}</title>
<meta name="description" content="{desc}">
<link rel="canonical" href="{url}">
{noindex}
<meta name="theme-color" content="#152B1C">
<meta property="og:type" content="website">
<meta property="og:locale" content="pt_BR">
<meta property="og:site_name" content="Campo Digital">
<meta property="og:title" content="{titulo}">
<meta property="og:description" content="{desc}">
<meta property="og:url" content="{url}">
<meta property="og:image" content="{CONFIG['dominio']}/assets/img/og-campo-digital.png">
<meta property="og:image:width" content="1200"><meta property="og:image:height" content="630">
<meta name="twitter:card" content="summary_large_image">
<link rel="icon" href="/assets/img/simbolo.svg" type="image/svg+xml">
<link rel="icon" href="/assets/img/favicon-32.png" sizes="32x32" type="image/png">
<link rel="apple-touch-icon" href="/assets/img/apple-touch-icon.png">
<link rel="preload" href="/assets/fonts/manrope-latin-wght-normal.woff2" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="/assets/css/site.css">
{jsonld}
</head>
<body{classe_body}>
<a class="pular" href="#conteudo">Pular para o conteúdo</a>
<header class="topo">
  <div class="wrap">
    <a class="marca" href="/" aria-label="Campo Digital, página inicial"><img src="/assets/img/simbolo.svg" alt="" width="40" height="35"><span>Campo<b>Digital</b></span></a>
    <button class="menu-botao" aria-expanded="false" aria-controls="menu">Menu</button>
    <nav class="menu" id="menu" aria-label="Principal">
      {''.join(itens)}
      <a class="btn btn-wa btn-sm" href="{html.escape(wa(msg_topo), quote=True)}" target="_blank" rel="noopener">{WA_SVG}Falar no WhatsApp</a>
    </nav>
  </div>
</header>
<main id="conteudo">
{expandir(corpo)}
</main>
<footer class="rodape">
  <div class="wrap">
    <div class="colunas">
      <div>
        <a class="marca" href="/"><img src="/assets/img/simbolo.svg" alt="" width="40" height="35"><span>Campo<b>Digital</b></span></a>
        <p class="tag">Agentes autônomos que sustentam a operação do agro. Pelo WhatsApp, sem app novo e sem planilha.</p>
        <p class="tag">Uma spinoff da PecSmart.</p>
      </div>
      <div>
        <h4>Soluções</h4>
        <ul>
          <li><a href="/fazenda-digital/">Fazenda Digital (leite)</a></li>
          <li><a href="/armazem-digital/">Armazém Digital (grãos)</a></li>
          <li><a href="/granja-digital/">Granja Digital (em breve)</a></li>
          <li><a href="/projetos/">Projetos sob medida</a></li>
        </ul>
        <h4 style="margin-top:22px">Diagnóstico rápido</h4>
        <ul>
          <li><a href="/fazenda-digital/indicadores/">Indicadores do leite</a></li>
          <li><a href="/armazem-digital/indicadores/">Indicadores do armazém</a></li>
        </ul>
      </div>
      <div>
        <h4>Empresa</h4>
        <ul>
          <li><a href="/#quem-somos">Quem somos</a></li>
          <li><a href="/#perguntas">Perguntas frequentes</a></li>
          <li><a href="{html.escape(wa('Olá! Vim pelo site da Campo Digital.'), quote=True)}" target="_blank" rel="noopener">WhatsApp {CONFIG['whatsapp_legivel']}</a></li>
        </ul>
      </div>
      <div>
        <h4>Legal</h4>
        <ul>
          <li><a href="/privacidade/">Privacidade e LGPD</a></li>
          <li><a href="/termos/">Termos de uso</a></li>
        </ul>
      </div>
    </div>
    <div class="base">
      <span>© {CONFIG['ano']} Campo Digital. Todos os direitos reservados.</span>
      <span>{CONFIG['cidade']} · Este site não usa cookies de rastreamento.</span>
    </div>
  </div>
</footer>
{flutuante}
<script src="/assets/js/site.js" defer></script>{js_extra}
</body>
</html>
"""


def relativizar(txt, caminho):
    """Versão de prévia: links relativos que abrem com duplo clique, sem servidor."""
    prof = 0 if caminho in ("/", "/404") else caminho.strip("/").count("/") + 1
    pre = "../" * prof
    def troca(m):
        attr, alvo = m.group(1), m.group(2)
        frag = ""
        if "#" in alvo:
            alvo, frag = alvo.split("#", 1); frag = "#" + frag
        alvo = alvo.lstrip("/")
        if alvo == "" or alvo.endswith("/"):
            alvo += "index.html"
        return f'{attr}="{pre}{alvo}{frag}"'
    return re.sub(r'(href|src)="/(?!/)([^"]*)"', troca, txt)


def main():
    import sys
    global DIST
    previa = "--previa" in sys.argv
    if previa:
        DIST = RAIZ / "previa"
    if DIST.exists():
        shutil.rmtree(DIST)
    shutil.copytree(SRC / "static", DIST)
    urls = []
    for p in sorted((SRC / "pages").glob("*.html")):
        meta, corpo = ler_pagina(p)
        destino = DIST / meta["caminho"].strip("/") / "index.html" if meta["caminho"] != "/404" else DIST / "404.html"
        destino.parent.mkdir(parents=True, exist_ok=True)
        pagina = layout(meta, corpo)
        if previa:
            pagina = relativizar(pagina, meta["caminho"])
        destino.write_text(pagina, encoding="utf-8")
        if not meta.get("noindex"):
            urls.append((meta["caminho"], meta.get("prioridade", "0.7")))
        print("ok", meta["caminho"])
    hoje = date.today().isoformat()
    sm = ['<?xml version="1.0" encoding="UTF-8"?>', '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    for c, pr in urls:
        sm.append(f"  <url><loc>{CONFIG['dominio']}{c}</loc><lastmod>{hoje}</lastmod><priority>{pr}</priority></url>")
    sm.append("</urlset>")
    (DIST / "sitemap.xml").write_text("\n".join(sm) + "\n", encoding="utf-8")
    (DIST / "robots.txt").write_text(f"User-agent: *\nAllow: /\n\nSitemap: {CONFIG['dominio']}/sitemap.xml\n", encoding="utf-8")


if __name__ == "__main__":
    main()
