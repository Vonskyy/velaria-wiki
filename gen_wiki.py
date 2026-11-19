"""Gera as páginas da wiki de Velária (MkDocs Material) a partir dos dados do kit."""
import json
import sys

sys.path.insert(0, "/home/claude/tools")
from spec5 import MATERIAIS, MATERIAIS_ORDEM, ORDENS  # noqa: E402

D = "/home/claude/wiki/docs"
VO = json.load(open("/tmp/vo.json"))
MAT = {m["id"]: m for m in MATERIAIS}
POR_ORDEM = {}
for m in MATERIAIS_ORDEM:
    POR_ORDEM.setdefault(m["ordem"], {})[m["tier"]] = m
NOME_ORDEM = {o: VO["ordens"][o]["nome"] for o in VO["ordens"]}
CLASSE = {"guerreiro": "Guerreiro", "paladino": "Paladino", "berserker": "Berserker", "ladino": "Ladino",
          "arqueiro": "Arqueiro", "bruxo": "Bruxo (Witcher)", "monge": "Monge", "lamina_arcana": "Lâmina Arcana",
          "sacerdote": "Sacerdote", "mago": "Mago", "druida": "Druida"}
PESO = {"guerreiro": "pesada", "paladino": "pesada", "berserker": "pesada", "ladino": "media", "arqueiro": "media",
        "bruxo": "media", "monge": "media", "lamina_arcana": "media", "sacerdote": "leve", "mago": "leve", "druida": "leve"}
PESO_TXT = {"pesada": "Armadura pesada", "media": "Armadura média", "leve": "Armadura leve"}
JEITO = {
    "guerreiro": "O tanque de linha de frente. Aguenta pancada e segura os inimigos para o grupo.",
    "paladino": "Guerreiro sagrado: bate forte, protege e cura um pouco os aliados.",
    "berserker": "Quanto mais apanha, mais forte fica. Fúria e machado.",
    "ladino": "Rápido e escondido. Dano enorme pelas costas, pouca vida.",
    "arqueiro": "Mata de longe com arco e besta. Fraco se o inimigo chega perto.",
    "bruxo": "Caçador de monstros: espada, sinais mágicos e poções.",
    "monge": "Luta de mãos (manoplas) e é o mais veloz de todos.",
    "lamina_arcana": "Mistura espada e magia: golpes que soltam feitiços.",
    "sacerdote": "O curandeiro. Mantém o grupo vivo e queima mortos-vivos.",
    "mago": "Dano mágico em área. Muito frágil, muito poderoso.",
    "druida": "Magia da natureza: cura, raízes e invocações.",
}


import os as _os, re as _re, material as _mat
_BASE = _os.path.join(_os.path.dirname(_mat.__file__), "templates", ".icons", "material")


def _icone(m):
    p = _os.path.join(_BASE, m.group(1) + ".svg")
    if not _os.path.exists(p):
        return ""
    return open(p).read().replace("<svg ", '<svg class="mi" width="22" height="22" fill="currentColor" ')


def w(nome, txt):
    txt = _re.sub(r":material-([a-z0-9-]+):", _icone, txt)
    open(f"{D}/{nome}", "w").write(txt.strip() + "\n")


def ic(item, tam=32):
    return f'<img class="px" src="img/itens/{item}.png" width="{tam}" height="{tam}" alt="">'


def icone_mat(m, tam=32):
    if m["tipo"] == "externo":
        return ""
    nome = m["item"].split(":")[1]
    return ic(nome, tam)


TIERCOR = {1: "#9aa3ad", 2: "#6fbf73", 3: "#e0603a", 4: "#7b86e8", 5: "#c07be8"}

# ------------------------------------------------------------------ desenhos (SVG)
def svg_mapa():
    """Mapa de círculos: limite de distância por tier a partir de Porto Alvorada."""
    cx, cy = 300, 300
    aneis = [(8000, 5, "Tier 5: sem limite"), (5000, 4, "Tier 4: até 8.000"), (3000, 3, "Tier 3: até 5.000"),
             (1500, 2, "Tier 2: até 3.000"), (0, 1, "Tier 1: até 1.500")]
    raios = {1: 52, 2: 104, 3: 168, 4: 236, 5: 290}
    s = [f'<svg viewBox="0 0 980 600" xmlns="http://www.w3.org/2000/svg" font-family="Inter, sans-serif">',
         '<defs><radialGradient id="ch" cx="50%" cy="50%" r="50%"><stop offset="0" stop-color="#2d2a45"/><stop offset="1" stop-color="#15131f"/></radialGradient></defs>',
         '<rect width="980" height="600" fill="url(#ch)" rx="14"/>']
    for t in (5, 4, 3, 2, 1):
        s.append(f'<circle cx="{cx}" cy="{cy}" r="{raios[t]}" fill="{TIERCOR[t]}" fill-opacity="{0.10 + 0.05 * (5 - t)}" stroke="{TIERCOR[t]}" stroke-width="2" stroke-dasharray="{"0" if t == 1 else "6 5"}"/>')
    rotulo = {1: ("1.500", 52), 2: ("3.000", 104), 3: ("5.000", 168), 4: ("8.000", 236)}
    for t, (txt, r) in rotulo.items():
        s.append(f'<text x="{cx + r * 0.71 + 6}" y="{cy - r * 0.71 - 4}" fill="{TIERCOR[t + 1] if t < 5 else "#fff"}" font-size="14" font-weight="700">{txt} blocos</text>')
    s.append(f'<circle cx="{cx}" cy="{cy}" r="9" fill="#ffd27a" stroke="#2a1b10" stroke-width="3"/>')
    s.append(f'<text x="{cx}" y="{cy + 30}" fill="#fff" font-size="14" font-weight="700" text-anchor="middle">Porto Alvorada</text>')
    s.append(f'<text x="{cx}" y="{cy + 47}" fill="#c9c4dc" font-size="12" text-anchor="middle">centro (0, 0)</text>')
    # portais
    s.append('<g transform="translate(640 120)"><rect width="300" height="150" rx="14" fill="#3a1714" stroke="#e0603a"/>'
             '<rect x="18" y="22" width="34" height="56" rx="4" fill="#2a0d3d" stroke="#9a5cff" stroke-width="5"/>'
             '<text x="70" y="42" fill="#ffb39c" font-size="17" font-weight="700">A Fornalha (Nether)</text>'
             '<text x="70" y="64" fill="#f3eefe" font-size="13">abre no tier 3</text>'
             '<text x="18" y="108" fill="#c9c4dc" font-size="12.5">Adamantita, Ouro Rosa, Vulcanita,</text>'
             '<text x="18" y="126" fill="#c9c4dc" font-size="12.5">Animita e Sangrita</text></g>')
    s.append('<g transform="translate(640 300)"><rect width="300" height="150" rx="14" fill="#241a33" stroke="#c07be8"/>'
             '<circle cx="35" cy="50" r="24" fill="#0b0814" stroke="#d6c6ff" stroke-width="3"/><circle cx="35" cy="50" r="4" fill="#fff"/>'
             '<text x="70" y="42" fill="#e4c8ff" font-size="17" font-weight="700">A Estrela Partida (End)</text>'
             '<text x="70" y="64" fill="#f3eefe" font-size="13">abre no tier 5</text>'
             '<text x="18" y="108" fill="#c9c4dc" font-size="12.5">Estelita, Vacuíta e Eclipsita</text>'
             '<text x="18" y="126" fill="#c9c4dc" font-size="12.5">nas ilhas de fora</text></g>')
    s.append('<text x="640" y="500" fill="#ffd27a" font-size="13" font-weight="700">Passou do seu limite?</text>'
             '<text x="640" y="520" fill="#c9c4dc" font-size="13">Aparece um aviso 64 blocos antes e</text>'
             '<text x="640" y="538" fill="#c9c4dc" font-size="13">você é empurrado de volta.</text>')
    s.append('</svg>')
    return "\n".join(s)


def svg_escada():
    """Escada dos 5 tiers com os minérios de cada degrau."""
    passos = [(1, "Tier 1", "Pedra", ["estanho", "ambar", "malaquita"], "Elites do tier 1"),
              (2, "Tier 2", "Pedra e ardósia", ["mitril", "oricalco", "cobalto", "glaciarita", "ferro_sombrio", "onix"], "Wroughtnaut, Frostmaw ou Guardião Ancestral"),
              (3, "Tier 3", "Nether + oceano e picos", ["adamantita", "ouro_rosa", "vulcanita", "animita", "sangrita", "abissita", "tempestita"], "Lich, Void Blossom, Umvuthi ou Sculptor"),
              (4, "Tier 4", "Ardósia profunda", ["umbrita", "draconita", "viridita"], "Gauntlet, Wither, Ignis, Warden..."),
              (5, "Tier 5", "End", ["estelita", "vacuita", "eclipsita"], "Você chegou ao topo")]
    W, H = 980, 540
    s = [f'<svg viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" font-family="Inter, sans-serif">',
         f'<rect width="{W}" height="{H}" rx="14" fill="#15131f"/>']
    for i, (t, nome, onde, ores, chefe) in enumerate(passos):
        x, w_ = 20 + i * 190, 180
        y = 340 - i * 62
        s.append(f'<rect x="{x}" y="{y}" width="{w_}" height="{H - y - 20}" rx="10" fill="{TIERCOR[t]}" fill-opacity=".16" stroke="{TIERCOR[t]}"/>')
        s.append(f'<rect x="{x}" y="{y}" width="{w_}" height="8" rx="4" fill="{TIERCOR[t]}"/>')
        s.append(f'<text x="{x + 12}" y="{y + 34}" fill="#fff" font-size="20" font-weight="700" font-family="Cinzel, serif">{nome}</text>')
        s.append(f'<text x="{x + 12}" y="{y + 54}" fill="{TIERCOR[t]}" font-size="12.5" font-weight="700">{onde}</text>')
        for j, o in enumerate(ores):
            s.append(f'<image href="img/blocos/{o}_ore.png" x="{x + 12 + (j % 4) * 40}" y="{y + 64 + (j // 4) * 40}" width="34" height="38"/>')
        yy = y + 64 + ((len(ores) + 3) // 4) * 40 + 16
        if t < 5:
            s.append(f'<text x="{x + 12}" y="{yy}" fill="#c9c4dc" font-size="11.5">Para subir:</text>')
        palavras, linha, linhas = chefe.split(" "), "", []
        for p in palavras:
            if len(linha + " " + p) > 24:
                linhas.append(linha)
                linha = p
            else:
                linha = (linha + " " + p).strip()
        linhas.append(linha)
        for k, l in enumerate(linhas):
            s.append(f'<text x="{x + 12}" y="{yy + 16 + k * 15}" fill="#f3eefe" font-size="11.5" font-weight="600">{l}</text>')
        if t < 5:
            s.append(f'<path d="M{x + w_ - 20} {y - 14} q 30 -40 60 -60" stroke="#ffd27a" stroke-width="3" fill="none" marker-end="url(#seta)"/>')
    s.insert(1, '<defs><marker id="seta" markerWidth="10" markerHeight="10" refX="6" refY="5" orient="auto"><path d="M0,0 L10,5 L0,10 z" fill="#ffd27a"/></marker></defs>')
    s.append('</svg>')
    return "\n".join(s)


def svg_cadeia_adamantita():
    s = ['<svg viewBox="0 0 980 230" xmlns="http://www.w3.org/2000/svg" font-family="Inter, sans-serif">',
         '<defs><marker id="sa" markerWidth="10" markerHeight="10" refX="6" refY="5" orient="auto"><path d="M0,0 L10,5 L0,10 z" fill="#ffd27a"/></marker></defs>',
         '<rect width="980" height="230" rx="14" fill="#15131f"/>']
    caixas = [(20, "img/blocos/adamantita_ore.png", "Detrito Adamântico", "mine no Nether, Y 8 a 40"),
              (250, "img/itens/chapa_adamantita.png", "Chapa de Adamantita", "asse no forno"),
              (560, "img/itens/ouro_rosa_ingot.png", "Lingote de Ouro Rosa", "minério do Nether, Y 10 a 117"),
              (790, "img/itens/adamantita_ingot.png", "Lingote de Adamantita", "a netherite de Velária")]
    for x, img, t, sub in caixas:
        s.append(f'<rect x="{x}" y="30" width="170" height="170" rx="14" fill="#1f1b2e" stroke="#3a3358"/>')
        s.append(f'<image href="{img}" x="{x + 53}" y="46" width="64" height="64" style="image-rendering:pixelated"/>')
        s.append(f'<text x="{x + 85}" y="140" fill="#fff" font-size="13.5" font-weight="700" text-anchor="middle">{t}</text>')
        s.append(f'<text x="{x + 85}" y="160" fill="#c9c4dc" font-size="11.5" text-anchor="middle">{sub}</text>')
    s.append('<path d="M192 115 H 244" stroke="#ffd27a" stroke-width="3" marker-end="url(#sa)"/><text x="218" y="104" fill="#ffd27a" font-size="12" text-anchor="middle">forno</text>')
    s.append('<text x="470" y="100" fill="#ffd27a" font-size="26" font-weight="700" text-anchor="middle">4×  +  4×</text>')
    s.append('<text x="470" y="128" fill="#c9c4dc" font-size="12" text-anchor="middle">na bancada (sem forma)</text>')
    s.append('<path d="M424 145 H 516" stroke="#3a3358" stroke-width="2"/>')
    s.append('<path d="M732 115 H 784" stroke="#ffd27a" stroke-width="3" marker-end="url(#sa)"/><text x="758" y="104" fill="#ffd27a" font-size="12" text-anchor="middle">= 1</text>')
    s.append('</svg>')
    return "\n".join(s)


def svg_moedas():
    moedas = [("Cobre", "#c8794a"), ("Prata", "#d8dde3"), ("Ouro", "#ffd34d"), ("Esmeralda", "#3fd17a"), ("Diamante", "#6fe3e8"),
              ("Netherite", "#5b4a52"), ("Adamantita", "#a86bff"), ("Draconita", "#ff6a3d"), ("Estelar", "#cbd6ff")]
    s = ['<svg viewBox="0 0 980 200" xmlns="http://www.w3.org/2000/svg" font-family="Inter, sans-serif">', '<rect width="980" height="200" rx="14" fill="#15131f"/>']
    for i, (n, c) in enumerate(moedas):
        x = 50 + i * 110
        s.append(f'<ellipse cx="{x}" cy="88" rx="30" ry="30" fill="{c}" stroke="#00000066" stroke-width="4"/>')
        s.append(f'<ellipse cx="{x - 8}" cy="78" rx="10" ry="6" fill="#ffffff55"/>')
        s.append(f'<text x="{x}" y="140" fill="#fff" font-size="13" font-weight="700" text-anchor="middle">{n}</text>')
        if i < len(moedas) - 1:
            s.append(f'<text x="{x + 55}" y="93" fill="#ffd27a" font-size="13" font-weight="700" text-anchor="middle">×10</text>')
    s.append('<text x="490" y="178" fill="#c9c4dc" font-size="12.5" text-anchor="middle">Cada moeda vale 10 da anterior. O caixa (ATM) troca para você.</text>')
    s.append('</svg>')
    return "\n".join(s)


def svg_bigornas():
    big = [(1, "Bigorna de Pedra", "Shift + clique direito numa pedra", None),
           (2, "Bigorna do Ferreiro", "Shift + clique direito numa bigorna", None),
           (3, "Bigorna da Fornalha", "Ouro Rosa + Bigorna do Ferreiro", "ouro_rosa_block"),
           (4, "Bigorna Dracônica", "Umbrita + Draconita + Bigorna da Fornalha", "draconita_block"),
           (5, "Bigorna Estelar", "Dracônica em cima da Base Estelar", "base_estelar")]
    s = ['<svg viewBox="0 0 980 260" xmlns="http://www.w3.org/2000/svg" font-family="Inter, sans-serif">', '<rect width="980" height="260" rx="14" fill="#15131f"/>']
    for i, (t, n, como, img) in enumerate(big):
        x = 18 + i * 192
        s.append(f'<rect x="{x}" y="20" width="180" height="220" rx="14" fill="#1f1b2e" stroke="{TIERCOR[t]}"/>')
        s.append(f'<text x="{x + 14}" y="48" fill="{TIERCOR[t]}" font-size="13" font-weight="700">TIER {t}</text>')
        # bigorna desenhada
        cor = {1: "#8a8f96", 2: "#4a4f57", 3: "#b05a3a", 4: "#3b3f8f", 5: "#3b3f8f"}[t]
        s.append(f'<g transform="translate({x + 45} 70)"><path d="M0 0 H90 Q 92 14 70 18 H58 V40 H74 V52 H16 V40 H32 V18 H20 Q -6 14 0 0z" fill="{cor}" stroke="#00000088" stroke-width="2"/>'
                 f'<path d="M4 3 H86" stroke="#ffffff44" stroke-width="3"/></g>')
        if t == 5:
            s.append(f'<image href="img/blocos/base_estelar.png" x="{x + 70}" y="124" width="40" height="44"/>')
        elif img:
            s.append(f'<image href="img/blocos/{img}.png" x="{x + 132}" y="56" width="30" height="34"/>')
        s.append(f'<text x="{x + 90}" y="188" fill="#fff" font-size="13.5" font-weight="700" text-anchor="middle">{n}</text>')
        palavras, linha, linhas = como.split(" "), "", []
        for p in palavras:
            if len(linha + " " + p) > 26:
                linhas.append(linha); linha = p
            else:
                linha = (linha + " " + p).strip()
        linhas.append(linha)
        for k, l in enumerate(linhas):
            s.append(f'<text x="{x + 90}" y="{207 + k * 14}" fill="#c9c4dc" font-size="11" text-anchor="middle">{l}</text>')
    s.append('</svg>')
    return "\n".join(s)


def svg_juramento():
    s = ['<svg viewBox="0 0 980 220" xmlns="http://www.w3.org/2000/svg" font-family="Inter, sans-serif">',
         '<defs><marker id="sj" markerWidth="10" markerHeight="10" refX="6" refY="5" orient="auto"><path d="M0,0 L10,5 L0,10 z" fill="#ff9a8a"/></marker></defs>',
         '<rect width="980" height="220" rx="14" fill="#15131f"/>',
         '<image href="img/arm/guerreiro_t2.png" x="60" y="20" width="110" height="180"/>',
         '<text x="115" y="212" fill="#fff" font-size="13" font-weight="700" text-anchor="middle">Você: Legião de Ferro</text>',
         '<rect x="240" y="40" width="300" height="60" rx="10" fill="#1d3324" stroke="#4f8a60"/>',
         f'<image href="img/itens/oricalco_ingot.png" x="252" y="52" width="36" height="36" style="image-rendering:pixelated"/>',
         '<text x="300" y="66" fill="#8fe39a" font-size="14" font-weight="700">Oricalco (da sua Ordem)</text>',
         '<text x="300" y="86" fill="#c9c4dc" font-size="12">fica no inventário e pode vestir</text>',
         '<rect x="240" y="120" width="300" height="60" rx="10" fill="#3a1d1a" stroke="#a85a3f"/>',
         f'<image href="img/itens/mitril_ingot.png" x="252" y="132" width="36" height="36" style="image-rendering:pixelated"/>',
         '<text x="300" y="146" fill="#ff9a8a" font-size="14" font-weight="700">Mitril (dos Patrulheiros)</text>',
         '<text x="300" y="166" fill="#c9c4dc" font-size="12">cai do inventário em 2 segundos</text>',
         '<path d="M545 150 C 620 150 640 190 720 190" stroke="#ff9a8a" stroke-width="3" fill="none" stroke-dasharray="6 5" marker-end="url(#sj)"/>',
         f'<image href="img/itens/mitril_ingot.png" x="735" y="168" width="36" height="36" style="image-rendering:pixelated;opacity:.7"/>',
         '<text x="620" y="62" fill="#ffd27a" font-size="13" font-weight="700">Dica</text>',
         '<text x="620" y="82" fill="#c9c4dc" font-size="12.5">Baú, mochila e shulker podem guardar</text>',
         '<text x="620" y="100" fill="#c9c4dc" font-size="12.5">itens de outra Ordem para vender ou trocar.</text>',
         '<text x="620" y="118" fill="#c9c4dc" font-size="12.5">Equipamento vanilla é livre para todos.</text>',
         '</svg>']
    return "\n".join(s)


def fig(svg, legenda):
    return f'<figure class="figura" markdown>\n{svg}\n<figcaption>{legenda}</figcaption>\n</figure>'


# ------------------------------------------------------------------ páginas
herois = "".join(f'<img src="img/arm/{o}_t5.png" alt="">' for o in ["guerreiro", "mago", "berserker", "monge", "sacerdote", "ladino", "druida"])
w("index.md", f"""
---
hide:
  - toc
  - navigation
---
<div class="hero">
<div>
<h1>Velária</h1>
<p>Mil anos depois da queda da Estrela Partida, você acorda no cais de Porto Alvorada sem lembrar do próprio nome.
Escolha sua Linhagem, jure a uma Ordem, forje suas armas e suba os 5 tiers de um MMORPG feito em Minecraft.</p>
<div class="botoes"><a href="comecando.html">Começar aqui</a><a class="sec" href="tiers.html">Como subir de tier</a></div>
</div>
<div class="linha">{herois}</div>
</div>

## Por onde começar

<div class="cards">
<a class="card" href="comecando.html"><h3>:material-flag-checkered: Seu primeiro dia</h3><p>Passo a passo do que fazer ao entrar, sem pular nada.</p></a>
<a class="card" href="linhagens.html"><h3>:material-account-group: Linhagens</h3><p>13 povos. Cada um tem um talento e uma fraqueza de verdade.</p></a>
<a class="card" href="ordens.html"><h3>:material-shield-sword: Ordens</h3><p>11 classes, cada uma com armadura própria em todos os tiers.</p></a>
<a class="card" href="tiers.html"><h3>:material-stairs-up: Os 5 tiers</h3><p>Até onde você pode andar e o que precisa para subir.</p></a>
<a class="card" href="minerios.html"><h3>:material-pickaxe: Minérios</h3><p>Onde nasce cada minério, com fotos de como ele aparece no mundo.</p></a>
<a class="card" href="forja.html"><h3>:material-anvil: A forja</h3><p>Bigornas, ligas e como fazer uma peça Obra-prima.</p></a>
<a class="card" href="economia.html"><h3>:material-cash-multiple: Economia</h3><p>Moedas, contratos, leilão e caça a procurados.</p></a>
<a class="card" href="receitas.html"><h3>:material-book-search: Receitas no jogo</h3><p>Como achar qualquer receita apertando uma tecla.</p></a>
</div>

## Velária em 30 segundos

<div class="cards">
<div class="card"><h3>Você sobe sozinho</h3><p>Tier só sobe se você estava lá quando o chefe morreu. Ninguém sobe de carona.</p></div>
<div class="card"><h3>Sua Ordem, suas armas</h3><p>Cada Ordem tem materiais exclusivos. Item de outra Ordem cai do seu inventário.</p></div>
<div class="card"><h3>Tudo é forjado</h3><p>Armas e armaduras saem da bigorna, com qualidade de Ruim a Obra-prima.</p></div>
<div class="card"><h3>Moeda não se fabrica</h3><p>Dinheiro vem de contratos, vendas, chefes e recompensas.</p></div>
</div>

<div class="foto" markdown>![Mina em primeira pessoa](img/cenas/foto_1_mina.jpg)</div>
""")

w("comecando.md", f"""
# Seu primeiro dia

Faça estes passos na ordem. Em 20 minutos você já está minerando e forjando.

<div class="passos">
<div class="passo"><div><h3>Entre e leia a introdução</h3><p>Aparece <b>VELÁRIA</b> na tela e a história no chat. Você ganha o <b>Diário do Desperto</b>: clique direito nele quando tiver dúvida.</p></div></div>
<div class="passo"><div><h3>Escolha sua Linhagem</h3><p>É o seu povo: Humano, Anão, Elfo, Orc... Cada um tem um ponto forte e uma fraqueza. Leia a <a href="linhagens.html">tabela de Linhagens</a> antes.</p></div></div>
<div class="passo"><div><h3>Jure a uma Ordem</h3><p>É a sua classe. Ela decide sua armadura, suas armas e seus materiais. <b>Não dá para usar o equipamento de outra Ordem.</b> Veja as <a href="ordens.html">11 Ordens</a>.</p></div></div>
<div class="passo"><div><h3>Um deus escolhe você</h3><p>Você ganha uma <b>Graça</b>: lutando com a arma do seu deus, bate mais forte. Digite <code>/graca</code> para ver qual é.</p></div></div>
<div class="passo"><div><h3>Pegue um contrato</h3><p>Na praça de Porto Alvorada, fale com o <b>Mercante de Contratos</b>. Contrato é a forma mais fácil de ganhar as primeiras moedas.</p></div></div>
<div class="passo"><div><h3>Minere o tier 1</h3><p>Faça a picareta de cobre e procure <b>Estanho</b>, <b>Âmbar</b> e <b>Malaquita</b> na pedra. Cada minério só cai com a picareta do anterior.</p></div></div>
<div class="passo"><div><h3>Monte sua primeira bigorna</h3><p>Agache (Shift) e clique direito numa pedra com um martelo de ferreiro: ela vira a <b>Bigorna de Pedra</b>. Veja <a href="forja.html">como forjar</a>.</p></div></div>
<div class="passo"><div><h3>Mate Elites para subir ao tier 2</h3><p>Elites são monstros mais fortes, com nome. Estar perto quando 3 a 6 deles morrem sobe você de tier.</p></div></div>
</div>

!!! tip "Perdeu algo? Aperte `/menu`"
    O menu mostra seu tier, sua Ordem, sua Graça e os comandos principais.

## O Juramento: por que meu item caiu?

{fig(svg_juramento(), "Itens de outra Ordem caem do inventário a cada 2 segundos, até armadura vestida.")}
""")

LIN = [("Humano de Alvorada", "Bom de negócio, sem fraqueza", "Sem grande talento", "humano"),
       ("Anão das Profundezas", "Mais armadura e minera melhor", "Lento e afunda na água", "anao"),
       ("Elfo do Bosque Prateado", "Rápido e silencioso", "Frágil; não come carne", "elfo"),
       ("Elfo da Noite", "Enxerga no escuro", "Fraco no sol sem capuz", "drow"),
       ("Sangue de Wyrm", "Escamas resistem ao fogo", "Sofre mais no frio", "draconato"),
       ("Feérico", "Leve, rápido, sem dano de queda", "Morre fácil; não come carne", "feerico"),
       ("Forjado", "Não precisa respirar; come metal e carvão", "Afunda na água", "forjado"),
       ("Gigante das Montanhas", "Enorme e resistente", "Lento, alvo maior, sempre com fome", "gigante"),
       ("Orc das Cinzas", "Grande e bruto", "Aldeões cobram caro; só come carne e peixe", "orc"),
       ("Pequenino das Colinas", "Pequeno, rápido e sortudo", "Aguenta pouco dano", "pequenino"),
       ("Salamandrino", "Imune ao fogo", "Água e chuva queimam", "salamandrino"),
       ("Filho da Maré", "Rei debaixo d'água", "Sufoca no calor do Nether", "tritao"),
       ("Filho da Noite", "Amaldiçoado pela Estrela: forte à noite", "Queima no sol sem elmo; só bebe sangue", "vampiro")]
cards = "\n".join(f'<div class="card"><h3>{n}</h3><p class="mais">+ {a}</p><p class="menos">− {b}</p></div>' for n, a, b, _ in LIN)
w("linhagens.md", f"""
# Linhagens

A Linhagem é o seu povo. Ela vem antes da Ordem e não muda depois. Toda Linhagem tem um **ponto forte (+)** e uma **fraqueza (−)** de verdade: escolha a que combina com o seu jeito de jogar.

<div class="cards">
{cards}
</div>

!!! question "Qual escolher se eu não sei?"
    **Humano de Alvorada.** Não tem fraqueza nenhuma, então você aprende o jogo sem se preocupar com sol, água ou comida.

!!! warning "Combina com a Ordem"
    Um **Anão** paladino aguenta muito mais pancada. Um **Feérico** guerreiro morre rápido demais. Pense nos dois juntos.
""")

partes = []
for o in ["guerreiro", "paladino", "berserker", "ladino", "arqueiro", "bruxo", "monge", "lamina_arcana", "sacerdote", "mago", "druida"]:
    fig5 = "".join(f'<figure><img src="img/arm/{o}_t{t}.png" alt=""><figcaption><b>Tier {t}</b>{POR_ORDEM[o][t]["nome"]}{" (liga)" if POR_ORDEM[o][t]["tipo"] == "liga" else ""}</figcaption></figure>' for t in range(1, 6))
    cams = "".join(f'<div><b>{VO["caminhos"][c]["nome"]}</b><br><span>deus: {VO["caminhos"][c]["deus"]}</span></div>' for c in VO["ordens"][o]["caminhos"])
    partes.append(f"""<div class="ordem" markdown>
<div class="topo"><h2>{NOME_ORDEM[o]}</h2><span class="selo">{CLASSE[o]}</span><span class="selo peso-{PESO[o]}">{PESO_TXT[PESO[o]]}</span></div>
<p>{JEITO[o]}</p>
<div class="tiers5">{fig5}</div>
<div class="caminhos">{cams}</div>
</div>""")
w("ordens.md", f"""
# Ordens

A Ordem é a sua classe. Cada uma tem **uma armadura própria em cada tier**, feita só com os materiais dela, e **3 caminhos de arma**, cada um ligado a um deus.

!!! info "Como funciona o caminho de arma"
    Você ganha 1 ponto ao entrar na Ordem e mais 1 a cada tier. Gaste na aba **Caminhos** da árvore de habilidades.
    Lutando com a arma do **seu deus**, você ganha **+8% de dano** (ou **+1,5** em arco e magia). O nó **Devoção** dobra esse bônus.

{chr(10).join(partes)}
""")

w("tiers.md", f"""
# Os 5 tiers

Seu tier vai de **1 a 5** e decide até onde você pode andar, quais dimensões abrem e o que você consegue forjar.

{fig(svg_escada(), "Cada degrau: onde minerar, os minérios do tier e o que você precisa derrotar para subir.")}

## Como eu subo de tier?

Só existem dois jeitos, e os dois exigem que **você esteja lá** (até 48 blocos do monstro quando ele morre):

<div class="cards">
<div class="card"><h3>:material-sword: Matar Elites</h3><p>Monstros mais fortes, com nome. 3 a 6 Elites do seu tier mortos perto de você = próximo tier.</p></div>
<div class="card"><h3>:material-skull: Derrotar um chefe</h3><p>Estar perto quando um chefe do seu tier morre sobe você na hora.</p></div>
<div class="card"><h3>:material-close-octagon: O que NÃO conta</h3><p>Quest de time, item dado por amigo, comando. Ninguém sobe de carona.</p></div>
</div>

## Até onde eu posso ir?

{fig(svg_mapa(), "O mapa é medido a partir de Porto Alvorada (0, 0). Cada tier libera um círculo maior.")}

| Tier | Distância máxima | Dimensões | Estruturas |
| --- | --- | --- | --- |
| <span class="tag t1">1</span> | 1.500 blocos | Mundo normal | Só as comuns |
| <span class="tag t2">2</span> | 3.000 blocos | Mundo normal | Masmorras do tier 2 |
| <span class="tag t3">3</span> | 5.000 blocos | + Nether | Masmorras do tier 3 |
| <span class="tag t4">4</span> | 8.000 blocos | + Nether | Masmorras do tier 4 |
| <span class="tag t5">5</span> | Sem limite | + End | Todas |

!!! tip "Monstros ficam mais fortes longe do centro"
    Quanto mais longe de Porto Alvorada, maior o nível dos monstros e das vilas.
""")

linhas = []
for m in sorted(MATERIAIS, key=lambda m: (m["tier"], m["id"])):
    nome = "Detrito Adamântico" if m["id"] == "adamantita" else f"Minério de {m['nome']}"
    dono = [NOME_ORDEM[o] for o, d in POR_ORDEM.items() for t, x in d.items() if x["id"] == m["id"]]
    linhas.append(f'| <img src="img/blocos/{m["id"]}_ore.png" width="34"> | **{nome}** | <span class="tag t{m["tier"]}">{m["tier"]}</span> | {m["onde"]} | {", ".join(dono) or "ingrediente de liga"} |')
w("minerios.md", f"""
# Minérios

Velária tem **22 minérios novos**. O fundo de cada bloco é a própria pedra onde ele nasce (pedra, ardósia, netherrack, basalto ou pedra do End). Procure o **veio colorido**.

=== "Mina (tiers 1, 2 e 4)"
    <div class="foto" markdown>![Mina](img/cenas/foto_1_mina.jpg)</div>
=== "Nether (tier 3)"
    <div class="foto" markdown>![Nether](img/cenas/foto_2_nether.jpg)</div>
=== "End (tier 5)"
    <div class="foto" markdown>![End](img/cenas/foto_3_end.jpg)</div>

## Onde achar cada um

| | Minério | Tier | Onde | Ordem que usa |
| --- | --- | --- | --- | --- |
{chr(10).join(linhas)}

!!! warning "Picareta em cadeia"
    Cada minério só cai com a **picareta do minério anterior**. Se o bloco quebrar e não soltar nada, sua picareta é fraca demais.

!!! info "Ultimine (quebrar o veio inteiro)"
    Segure a tecla do Ultimine para quebrar o veio todo de uma vez. Nos tiers 1 e 2 funciona só em minério; a partir do tier 3 também em terra e pedra. Madeira nunca.

## Todos os itens e blocos

<div class="foto" markdown>![Itens e blocos](img/cenas/foto_4_itens_blocos.jpg)</div>
""")

w("forja.md", f"""
# A forja

Armas, armaduras e ligas **não são feitas na bancada**: elas são forjadas na **bigorna**, com marteladas. Quanto melhor você martela, melhor a peça.

## As 5 bigornas

Cada tier pede uma bigorna melhor. Para montar a próxima, você precisa do minério do tier atual.

{fig(svg_bigornas(), "A bigorna certa aparece na receita do EMI. Material do tier 5 só é forjado com a Base Estelar embaixo.")}

## Como forjar, passo a passo

<div class="passos">
<div class="passo"><div><h3>Coloque os materiais na bigorna</h3><p>Clique direito na bigorna com o material na mão, no formato da receita (veja no EMI).</p></div></div>
<div class="passo"><div><h3>Pegue o martelo e agache</h3><p>Segure Shift e clique na bigorna com o martelo de ferreiro para começar o minigame.</p></div></div>
<div class="passo"><div><h3>Acerte o ritmo</h3><p>Martele quando o marcador estiver na zona certa. Cada acerto melhora a qualidade.</p></div></div>
<div class="passo"><div><h3>Pegue a peça</h3><p>A qualidade aparece no nome do item. Armaduras levam várias marteladas: tenha paciência.</p></div></div>
</div>

## Qualidade da peça

<div class="barras">
<div class="barra"><span>Ruim</span><div class="trilho"><i style="left:0;width:25%;background:#ff9a8a"></i></div><span class="v">−0,5</span></div>
<div class="barra"><span>Boa</span><div class="trilho"><i style="left:0;width:2%;background:#c9c4dc"></i></div><span class="v">0</span></div>
<div class="barra"><span>Especialista</span><div class="trilho"><i style="left:0;width:50%;background:#6fbf73"></i></div><span class="v">+0,5</span></div>
<div class="barra"><span>Perfeita</span><div class="trilho"><i style="left:0;width:75%;background:#7b86e8"></i></div><span class="v">+0,75</span></div>
<div class="barra"><span>Obra-prima</span><div class="trilho"><i style="left:0;width:100%;background:#ffd27a"></i></div><span class="v">+1</span></div>
</div>
<p class="legenda">Bônus de armadura por peça. No dano das armas vai de −0,5 (Ruim) a +1,5 (Obra-prima).</p>

## Ligas: misturando minérios

33 dos 55 materiais são **ligas**: você mistura minérios na bigorna e ganha 2 lingotes de um metal novo, exclusivo da sua Ordem. A receita de cada liga está no EMI.

## Adamantita: a netherite de Velária

{fig(svg_cadeia_adamantita(), "O Detrito Adamântico vira chapa no forno. 4 chapas + 4 lingotes de Ouro Rosa = 1 lingote de Adamantita.")}

!!! info "Armas e armaduras dos outros mods também vão para a bigorna"
    Epic Knights, Immersive Armors, Fantasy Armor, Samurai Dynasty, Simply Swords, os mods de classe e o aço de dragão do Ice and Fire.
    Cobre e ouro: Bigorna de Pedra. Ferro e diamante: Bigorna do Ferreiro. Netherite: Bigorna da Fornalha. Aço de dragão: Bigorna Dracônica.
    Roupas de pano, couro, cajados e arcos continuam na bancada.
""")

w("economia.md", f"""
# Economia

**Moeda não se fabrica.** Todo dinheiro do servidor vem de trabalho: contratos, vendas, Elites, chefes e recompensas.

{fig(svg_moedas(), "As moedas de Velária, da menor para a maior.")}

## Onde ganhar e gastar em Porto Alvorada

<div class="cards">
<div class="card"><h3>:material-file-sign: Mercante de Contratos</h3><p>Contratos de coleta, de caça e do Chefe Lendário. Você paga pelo contrato e recebe mais ao cumprir.</p></div>
<div class="card"><h3>:material-shield-crown: Bancas das Ordens</h3><p>Uma por Ordem. Troca as Insígnias da sua Ordem por equipamento e consumíveis.</p></div>
<div class="card"><h3>:material-crown: Comprador do Rei</h3><p>O servidor compra seus lingotes e gemas até o tier 4.</p></div>
<div class="card"><h3>:material-gavel: Casa de Leilões</h3><p>Venda entre jogadores. Material do tier 5 só se negocia aqui.</p></div>
</div>

## Honra e caça a procurados

Matar jogadores sem motivo baixa sua **Honra**. Com honra baixa, você vira **Procurado** e quem te matar ganha a recompensa. A **Carta de Perdão** limpa sua ficha.

## Viagem rápida

As **Waystones** são caras de propósito: só compradas de aldeão nível 100+ ou feitas com minério de tier alto. Antes disso, use os **pergaminhos de retorno e de teleporte**.
""")

w("receitas.md", """
# Receitas no jogo (EMI)

Toda receita do servidor aparece no **EMI**, a lista de itens que fica à direita do inventário. Você não precisa decorar nada.

<div class="cards">
<div class="card"><h3><kbd>R</kbd> Receita</h3><p>Passe o mouse em cima de um item e aperte <b>R</b>: mostra como fazer.</p></div>
<div class="card"><h3><kbd>U</kbd> Uso</h3><p>Aperte <b>U</b>: mostra onde esse item é usado (ligas, armas, bigornas...).</p></div>
<div class="card"><h3>:material-magnify: Busca</h3><p>Digite na barra de baixo. <code>@kubejs</code> mostra só os itens de Velária.</p></div>
</div>

## O que aparece no EMI

| Sistema | Aparece? | Onde ver |
| --- | --- | --- |
| Forja do Overgeared (bigorna, ligas, tier da bigorna) | Sim | Aba da bigorna |
| Cozinha do Farmer's Delight e Hands-On Delight | Sim | Abas de panela, tábua e forno |
| Brewin' and Chewin', Cultural Delights | Sim | Abas próprias |
| Joias, runas e livros de magia | Sim | Abas próprias |
| Itens e blocos de Velária | Sim | Lista à direita |
| Apotheosis (gemas e encaixes), Farmer's Respite, My Nether's Delight | Sim | Abas próprias |
| Cinematic Interaction, Waystones, altares do Cataclysm | Sim | Abas próprias |
| Explicação dos minérios, ligas, bigornas e Base Estelar | Sim | Aba "Informação" (aperte R) |
| Onde cada minério nasce | Sim | Aba "Informação" do minério |
""")

w("faq.md", """
# Perguntas frequentes

??? question "Meu item sumiu do inventário!"
    Ele é de outra Ordem: o Juramento derruba. Ele está no chão perto de você. Guarde num baú para vender ou trocar.

??? question "Quebrei o minério e não caiu nada."
    Sua picareta é fraca demais. Cada minério precisa da picareta do minério anterior.

??? question "Fui empurrado de volta andando pelo mapa."
    Você chegou no limite do seu tier. Veja [até onde você pode ir](tiers.html).

??? question "Não consigo entrar no Nether."
    O Nether abre no tier 3. O End, no tier 5.

??? question "Como faço moedas?"
    Não faz. Moeda vem de contratos, vendas ao Comprador do Rei, Elites, chefes e recompensas.

??? question "Minha bigorna não aceita o material."
    O material é de um tier acima da bigorna. Monte a bigorna do tier certo: veja [A forja](forja.html).
""")
print("ok")
