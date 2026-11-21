"""Converte a wiki (MkDocs Material) para o formato do GitBook.

Saída: gitbook/ (páginas .md, SUMMARY.md, README.md e as imagens) + .gitbook.yaml na raiz.
O GitBook não entende admonitions, abas do Material nem o HTML dos cartões; aqui tudo vira
blocos do GitBook ({% hint %}, {% tabs %}, <details>) ou markdown simples.
Uso: python3 gen_gitbook.py  (rodar na pasta da wiki)
"""
import os
import re
import shutil

import yaml
from bs4 import BeautifulSoup

RAIZ = os.path.dirname(os.path.abspath(__file__))
DOCS = os.path.join(RAIZ, "docs")
OUT = os.path.join(RAIZ, "gitbook")

ESTILO = {"info": "info", "note": "info", "tip": "success", "success": "success", "question": "info",
          "warning": "warning", "danger": "danger", "failure": "danger", "example": "info", "abstract": "info"}


def bloco_indentado(linhas, i):
    """Junta as linhas indentadas (4 espaços) depois de i. Devolve (texto, próximo índice)."""
    corpo = []
    while i < len(linhas) and (linhas[i].startswith("    ") or linhas[i].strip() == ""):
        if linhas[i].strip() == "" and (i + 1 >= len(linhas) or not linhas[i + 1].startswith("    ")):
            break
        corpo.append(linhas[i][4:])
        i += 1
    return "\n".join(corpo).strip(), i


CONT = {"n": 0}


def svg_para_png(svg, pagina):
    """Diagramas em SVG inline viram PNG (o GitBook não mostra SVG inline)."""
    CONT["n"] += 1
    nome = f"{os.path.splitext(pagina)[0]}_{CONT['n']}"
    pasta = os.path.join(OUT, "img", "diagramas")
    os.makedirs(pasta, exist_ok=True)
    tmp = os.path.join(DOCS, f"_tmp_{nome}.svg")
    if 'xmlns:xlink' not in svg:
        svg = svg.replace("<svg ", '<svg xmlns:xlink="http://www.w3.org/1999/xlink" ', 1)
    open(tmp, "w", encoding="utf-8").write(svg)
    png = os.path.join(pasta, nome + ".png")
    os.system(f'rsvg-convert -z 2 -o "{png}" "{tmp}"')
    os.remove(tmp)
    return f"img/diagramas/{nome}.png"


def inline(el):
    """Texto de um elemento com negrito, código e links em markdown."""
    partes = []
    for c in el.children:
        if isinstance(c, str):
            partes.append(re.sub(r"\s+", " ", c))
        elif c.name in ("b", "strong"):
            partes.append(f"**{c.get_text(strip=True)}**")
        elif c.name in ("i", "em"):
            partes.append(f"*{c.get_text(strip=True)}*" if c.get_text(strip=True) else "")
        elif c.name == "code":
            partes.append(f"`{c.get_text()}`")
        elif c.name == "a":
            partes.append(f"[{inline(c).strip()}]({c.get('href', '').replace('.html', '.md')})")
        elif c.name == "br":
            partes.append(" · ")
        elif c.name == "img":
            partes.append(f'<img src="{c["src"]}" alt="" width="64">')
        elif c.name == "span" and "tag" in (c.get("class") or []):
            partes.append(f"`{c.get_text(strip=True)}`")
        else:
            partes.append(inline(c))
    return "".join(partes)


def bloco(el, saida, pagina):
    classes = el.get("class") or []
    if el.name in ("h1", "h2", "h3", "h4"):
        saida += ["#" * int(el.name[1]) + " " + el.get_text(" ", strip=True), ""]
    elif el.name == "p":
        if "legenda" in classes:
            saida += ["*" + el.get_text(" ", strip=True) + "*", ""]
        else:
            saida += [inline(el).strip(), ""]
    elif el.name == "svg":
        saida += [f"![]({svg_para_png(str(el), pagina)})", ""]
    elif el.name == "figure":
        svg = el.find("svg")
        img = el.find("img")
        cap = el.find("figcaption")
        src = svg_para_png(str(svg), pagina) if svg else (img["src"] if img else None)
        if src:
            saida.append(f'<figure><img src="{src}" alt=""><figcaption><p>'
                         f'{cap.get_text(" ", strip=True) if cap else ""}</p></figcaption></figure>')
            saida.append("")
    elif el.name == "img":
        saida += [f"![{el.get('alt', '')}]({el['src']})", ""]
    elif "cards" in classes:
        for card in el.find_all(class_="card"):
            for svg in card.find_all("svg"):
                svg.decompose()
            h = card.find(["h3", "h2"])
            titulo = h.get_text(" ", strip=True) if h else ""
            textos = []
            for p in card.find_all("p"):
                t = p.get_text(" ", strip=True)
                pc = p.get("class") or []
                if "mais" in pc:
                    t = "🟢 " + t.lstrip("+ ").strip()
                elif "menos" in pc:
                    t = "🔴 " + t.lstrip("−- ").strip()
                textos.append(t)
            if card.name == "a" and card.get("href"):
                titulo = f"[{titulo}]({card['href'].replace('.html', '.md')})"
            saida.append(f"* **{titulo}** — " + " · ".join(textos))
        saida.append("")
    elif "passos" in classes:
        for n, p in enumerate(el.find_all(class_="passo"), 1):
            h = p.find("h3")
            corpo = " ".join(inline(x).strip() for x in p.find_all("p"))
            saida.append(f"{n}. **{h.get_text(strip=True) if h else ''}** — {corpo}")
        saida.append("")
    elif "barras" in classes:
        saida += ["| Qualidade | Bônus |", "|---|---|"]
        for b in el.find_all(class_="barra"):
            spans = b.find_all("span", recursive=False)
            saida.append(f"| {spans[0].get_text(strip=True)} | {spans[-1].get_text(strip=True)} |")
        saida.append("")
    elif "hero" in classes:
        for x in el.find_all(["h1", "p"]):
            if x.find_parent(class_="botoes"):
                continue
            bloco(x, saida, pagina)
        bot = el.find(class_="botoes")
        if bot:
            saida += [" · ".join(f"**[{a.get_text(strip=True)} →]({a['href'].replace('.html', '.md')})**"
                                 for a in bot.find_all("a")), ""]
        linha = el.find(class_="linha")
        if linha:
            saida += [" ".join(f'<img src="{i["src"]}" alt="" width="80">' for i in linha.find_all("img")), ""]
    elif "ordem" in classes:
        topo = el.find("div", class_="topo")
        nome = topo.find("h2").get_text(strip=True)
        selos = [s.get_text(strip=True) for s in topo.find_all("span", class_="selo")]
        saida += [f"## {nome}", "", " · ".join(f"`{s}`" for s in selos), ""]
        for p in el.find_all("p", recursive=False):
            saida += [inline(p).strip(), ""]
        t5 = el.find("div", class_="tiers5")
        if t5:
            figs = t5.find_all("figure")
            cab, imgs, mats = [], [], []
            for f in figs:
                cap = f.find("figcaption")
                b = cap.find("b")
                cab.append(b.get_text(strip=True))
                b.extract()
                mats.append(cap.get_text(" ", strip=True))
                imgs.append(f'<img src="{f.find("img")["src"]}" alt="" width="96">')
            saida += ["| " + " | ".join(cab) + " |", "|" + "---|" * len(cab),
                      "| " + " | ".join(imgs) + " |", "| " + " | ".join(mats) + " |", ""]
        cam = el.find("div", class_="caminhos")
        if cam:
            itens = []
            for d in cam.find_all("div", recursive=False):
                arma = d.find("b").get_text(strip=True)
                deus = d.find("span").get_text(strip=True) if d.find("span") else ""
                itens.append(f"**{arma}** ({deus})")
            saida += ["**Caminhos de arma:** " + " · ".join(itens), ""]
    elif "foto" in classes:
        img = el.find("img")
        if img:
            saida += [f"![{img.get('alt', '')}]({img['src']})", ""]
    elif el.name in ("div", "section", "a"):
        for c in el.find_all(recursive=False):
            bloco(c, saida, pagina)
    else:
        saida += [el.get_text(" ", strip=True), ""]


def html_para_md(trecho, pagina):
    sopa = BeautifulSoup(trecho, "html.parser")
    saida = []
    for el in sopa.find_all(recursive=False):
        bloco(el, saida, pagina)
    return "\n".join(saida)


def converter(texto, pagina=""):
    # imagens markdown dentro de <div class="foto" markdown> e <figure markdown>
    texto = re.sub(r'<div class="foto" markdown>(.*?)</div>', r"\1", texto)
    texto = re.sub(r"<figure([^>]*) markdown>\s*(!\[[^\]]*\]\(([^)]+)\))\s*<figcaption>(.*?)</figcaption>\s*</figure>",
                   lambda m: f'<figure><img src="{m.group(3)}" alt=""><figcaption><p>{m.group(4).strip()}</p></figcaption></figure>',
                   texto, flags=re.S)
    texto = re.sub(r"\{ ?[.#:][^}\n]*\}", "", texto)           # attr_list
    linhas = texto.split("\n")
    out = []
    i = 0
    while i < len(linhas):
        ln = linhas[i]
        m = re.match(r'^(!!!|\?\?\?\+?) (\w+)(?: "(.*)")?\s*$', ln)
        if m:
            corpo, i = bloco_indentado(linhas, i + 1)
            corpo = converter(corpo, pagina)
            if m.group(1) == "!!!":
                estilo = ESTILO.get(m.group(2), "info")
                titulo = f"**{m.group(3)}**\n\n" if m.group(3) else ""
                out += [f'{{% hint style="{estilo}" %}}', titulo + corpo, "{% endhint %}", ""]
            else:
                out += ["<details>", "", f"<summary>{m.group(3) or 'Detalhes'}</summary>", "", corpo, "", "</details>", ""]
            continue
        if re.match(r'^=== "(.*)"\s*$', ln):
            out.append("{% tabs %}")
            while i < len(linhas) and re.match(r'^=== "(.*)"\s*$', linhas[i]):
                titulo = re.match(r'^=== "(.*)"\s*$', linhas[i]).group(1)
                corpo, i = bloco_indentado(linhas, i + 1)
                out += [f'{{% tab title="{titulo}" %}}', converter(corpo, pagina), "{% endtab %}"]
                while i < len(linhas) and linhas[i].strip() == "":
                    i += 1
            out += ["{% endtabs %}", ""]
            continue
        if re.match(r"\s*<(div|figure|a class|p class)", ln):
            # junta o bloco HTML até fechar os divs
            bloco = [ln]
            prof = ln.count("<div") + ln.count("<figure") + ln.count("<a ") - ln.count("</div>") - ln.count("</figure>") - ln.count("</a>")
            i += 1
            while prof > 0 and i < len(linhas):
                bloco.append(linhas[i])
                prof += linhas[i].count("<div") + linhas[i].count("<figure") + linhas[i].count("<a ") - linhas[i].count("</div>") - linhas[i].count("</figure>") - linhas[i].count("</a>")
                i += 1
            out.append(html_para_md("\n".join(bloco).replace(" markdown>", ">"), pagina))
            continue
        out.append(ln)
        i += 1
    return "\n".join(out)


def main():
    cfg = yaml.load(open(os.path.join(RAIZ, "mkdocs.yml")), Loader=yaml.BaseLoader)
    if os.path.isdir(OUT):
        shutil.rmtree(OUT)
    os.makedirs(OUT)
    shutil.copytree(os.path.join(DOCS, "img"), os.path.join(OUT, "img"))
    resumo = ["# Table of contents", ""]
    for entrada in cfg["nav"]:
        (nome, alvo), = entrada.items()
        if isinstance(alvo, str):
            destino = "README.md" if alvo == "index.md" else alvo
            resumo.append(f"* [{nome}]({destino})")
            continue
        resumo += ["", f"## {nome}", ""]
        for sub in alvo:
            (n2, a2), = sub.items()
            resumo.append(f"* [{n2}]({a2})")
    for fn in os.listdir(DOCS):
        if not fn.endswith(".md"):
            continue
        bruto = open(os.path.join(DOCS, fn), encoding="utf-8").read()
        bruto = re.sub(r"\A---\n.*?\n---\n", "", bruto, flags=re.S)     # front matter do MkDocs
        texto = converter(bruto, fn)
        texto = re.sub(r"\]\(([a-z_]+)\.html(#[^)]*)?\)", r"](\1.md\2)", texto)
        texto = re.sub(r'<span class="tag t(\d)">([^<]*)</span>', r"T\2", texto)
        texto = re.sub(r"\n{3,}", "\n\n", texto)
        texto = texto.replace("(index.md)", "(README.md)").replace("(index.md#", "(README.md#")
        destino = "README.md" if fn == "index.md" else fn
        open(os.path.join(OUT, destino), "w", encoding="utf-8").write(texto.rstrip() + "\n")
    open(os.path.join(OUT, "SUMMARY.md"), "w", encoding="utf-8").write("\n".join(resumo) + "\n")
    open(os.path.join(RAIZ, ".gitbook.yaml"), "w").write(
        "root: ./gitbook/\n\nstructure:\n  readme: README.md\n  summary: SUMMARY.md\n")
    print("ok:", sorted(os.listdir(OUT)))


if __name__ == "__main__":
    main()
