"""Páginas novas da wiki: receitas desenhadas no estilo do Minecraft, forja de cada Ordem, magia e teclas.

Gera imagens em docs/img/receitas/ e docs/img/icones/ e as páginas crafts.md, forja_ordens.md,
magia.md e teclas.md. Também refaz a tabela de minérios de minerios.md.
Uso: python3 -I gen_receitas.py
"""
import json
import os
import re
import sys

sys.path.insert(0, "/home/claude/tools")
import receitas_img as R  # noqa: E402
import spec5  # noqa: E402

D = "/home/claude/wiki/docs"
IMG = f"{D}/img/receitas"
ICO = f"{D}/img/icones"
os.makedirs(IMG, exist_ok=True)
os.makedirs(ICO, exist_ok=True)
DADOS = json.load(open("/home/claude/tools/v5_dados.json", encoding="utf-8"))
s = open("/home/claude/kit5/kubejs/server_scripts/mmo_receitas.js", encoding="utf-8").read()
i = s.index("const VELARIA_RECEITAS = ") + len("const VELARIA_RECEITAS = ")
REC, _ = json.JSONDecoder().raw_decode(s[i:])

NOME_ORDEM = {"guerreiro": "Guerreiro", "paladino": "Paladino", "sacerdote": "Sacerdote", "mago": "Mago",
              "ladino": "Ladino", "arqueiro": "Arqueiro", "berserker": "Berserker", "bruxo": "Bruxo",
              "druida": "Druida", "monge": "Monge", "lamina_arcana": "Lâmina Arcana"}
ORDEM_ORDEM = list(NOME_ORDEM)
TIER_BIGORNA = {"stone": "Bigorna de Pedra", "iron": "Bigorna do Ferreiro", "steel": "Bigorna do Ferreiro",
                "tier_a": "Bigorna da Fornalha", "tier_b": "Bigorna Dracônica", "a": "Bigorna da Fornalha",
                "b": "Bigorna Dracônica"}
NOME_ITEM = {}
for lang in ["/home/claude/kit5/kubejs/assets/kubejs/lang/pt_br.json"]:
    if os.path.exists(lang):
        for k, v in json.load(open(lang, encoding="utf-8")).items():
            m = re.match(r"(?:item|block)\.kubejs\.(.+)", k)
            if m:
                NOME_ITEM["kubejs:" + m.group(1)] = v
VANILLA = {"minecraft:copper_ingot": "Lingote de Cobre", "minecraft:gold_ingot": "Lingote de Ouro",
           "minecraft:iron_ingot": "Lingote de Ferro", "minecraft:lapis_lazuli": "Lápis-lazúli",
           "minecraft:redstone": "Redstone", "minecraft:amethyst_shard": "Fragmento de Ametista",
           "minecraft:coal": "Carvão", "minecraft:calcite": "Calcita", "minecraft:bone_meal": "Farinha de Osso",
           "minecraft:stick": "Graveto"}
TROCA = {"iceandfire:silver_ingot": "minecraft:iron_ingot", "#c:ingots/silver": "minecraft:iron_ingot"}


def nome(it):
    return NOME_ITEM.get(it) or VANILLA.get(it) or it.split(":")[1].replace("_", " ").title()


TAGS_FIXAS = {"minecraft:wool": "minecraft:white_wool", "c:ingots/silver": "minecraft:iron_ingot",
              "runes:fancy_stone_materials": "minecraft:polished_andesite",
              "minecraft:stone_tool_materials": "minecraft:cobblestone", "minecraft:wooden_slabs": "minecraft:oak_planks",
              "minecraft:wooden_fences": "minecraft:stick", "minecraft:planks": "minecraft:oak_planks",
              "minecraft:logs": "minecraft:oak_log", "c:bookshelves": "minecraft:bookshelf", "c:glass_blocks": "minecraft:glass",
              "c:leathers": "minecraft:leather", "c:obsidians": "minecraft:obsidian", "c:nuggets/iron": "minecraft:iron_nugget",
              "c:raw_materials/iron": "minecraft:raw_iron", "c:gems/amethyst": "minecraft:amethyst_shard"}
DATA_TAGS = ["/home/claude/irons/x/data", "/tmp/wz/rj/data"]


def tag_item(t, prof=0):
    """Resolve uma tag para um item com textura: tabela fixa, padrões c:, depois o json da tag nos mods."""
    if t in TAGS_FIXAS:
        return TAGS_FIXAS[t]
    if t.startswith("c:ingots/") or t.startswith("c:gems/"):
        base = t.split("/")[1]
        return f"minecraft:{base}_ingot" if t.startswith("c:ingots/") and base in ("iron", "gold", "copper", "netherite") \
            else f"minecraft:{base}" if base in ("diamond", "emerald") else TROCA.get(f"irons_spellbooks:{base}_ingot", f"irons_spellbooks:{base}")
    ns, p = t.split(":", 1)
    for d in DATA_TAGS:
        for pasta in ("item", "items"):
            f = f"{d}/{ns}/tags/{pasta}/{p}.json"
            if os.path.exists(f) and prof < 3:
                for v in json.load(open(f)).get("values", []):
                    v = v["id"] if isinstance(v, dict) else v
                    return tag_item(v[1:], prof + 1) if v.startswith("#") else v
    return "minecraft:barrier"


def ing(k):
    """Ingrediente de receita (item ou tag) → item com textura."""
    if isinstance(k, list):
        k = k[0]
    it = k.get("item") or k.get("tag")
    if "tag" in k:
        it = tag_item(k["tag"])
    return TROCA.get(it, it)


def grade(pattern, key):
    linhas = []
    largura = max(len(p) for p in pattern)
    for p in pattern:
        p = p.ljust(largura)
        linhas.append([ing(key[c]) if c != " " else None for c in p])
    # centraliza receitas estreitas na grade 3x3 como o Minecraft mostra
    while len(linhas) < 3:
        linhas.append([None] * largura)
    return linhas


def desenhar_forma(r, destino):
    if r.get("type") in ("minecraft:crafting_shaped", "overgeared:forging"):
        return R.bancada(grade(r["pattern"], r["key"]), r["result"]["id"], r["result"].get("count", 1), destino)
    if r.get("type") == "minecraft:crafting_shapeless":
        ent = [ing(x) for x in r["ingredients"]]
        g = [ent[0:3], ent[3:6], ent[6:9]]
        return R.bancada(g, r["result"]["id"], r["result"].get("count", 1), destino)
    if r.get("type") == "minecraft:smithing_transform":
        return R.linha([(ing(r["template"]), 1), (ing(r["base"]), 1), (ing(r["addition"]), 1)],
                       r["result"]["id"], r["result"].get("count", 1), destino)
    raise ValueError(r.get("type"))


def icone(it, tam=48):
    base = it.replace(":", "_").replace("/", "_")
    try:
        return "img/icones/" + R.icone(it, f"{ICO}/{base}", tam)
    except FileNotFoundError:
        return None


def img(caminho, alt="", largura=None):
    w = f' width="{largura}"' if largura else ""
    return f'<img src="{caminho}" alt="{alt}"{w}>'


# ================================================================ crafts.md
def pagina_crafts():
    out = ["# Crafts e receitas", "",
           "Todas as receitas de Velária desenhadas do jeito que aparecem no jogo. No servidor, passe o mouse "
           "num item e aperte **R** no EMI para ver a receita ao vivo.", ""]
    # ligas
    out += ["## Ligas", "",
            "Uma **liga** mistura minérios **na bigorna** (Overgeared): coloque os ingredientes no formato da "
            "receita e martele. Cada receita rende **2 lingotes**. A bigorna precisa ser do tier da liga.", ""]
    ligas = [r for r in REC["forja"] if r["result"]["id"].endswith("_ingot")]
    por_tier = {}
    for r in ligas:
        mid = r["result"]["id"].split(":")[1][:-6]
        mat = next((m for m in DADOS["materiais"] if m["id"] == mid), None)
        t = mat["tier"] if mat else 1
        por_tier.setdefault(t, []).append((r, mat))
    for t in sorted(por_tier):
        out += [f"### Tier {t}", "", "| Receita na bigorna | Liga | Ordem |", "| --- | --- | --- |"]
        for r, mat in por_tier[t]:
            f = desenhar_forma(r, f"{IMG}/liga_{r['result']['id'].split(':')[1]}")
            dono = NOME_ORDEM.get(mat.get("ordem"), "—") if mat else "—"
            bigorna = TIER_BIGORNA.get(r.get("tier", ""), r.get("tier", ""))
            out.append(f"| {img('img/receitas/' + f, mat['nome'] if mat else '', 240)} | **{mat['nome'] if mat else ''}**"
                       f"<br>{bigorna} | {dono} |")
        out.append("")
    # picaretas e machados
    out += ["## Picaretas e machados", "",
            "As ferramentas continuam na **bancada**, com o mesmo molde das de ferro. Cada picareta quebra o "
            "minério seguinte da cadeia.", ""]
    exemplos = [f for f in REC["ferramentas"]]
    out += ["| Material | Picareta | Machado |", "| --- | --- | --- |"]
    for f in exemplos:
        mat = f["material"]
        try:
            p = R.bancada([[mat, mat, mat], [None, "minecraft:stick", None], [None, "minecraft:stick", None]],
                          f"kubejs:{f['id']}_pickaxe", 1, f"{IMG}/pic_{f['id']}")
            a = R.bancada([[mat, mat, None], [mat, "minecraft:stick", None], [None, "minecraft:stick", None]],
                          f"kubejs:{f['id']}_axe", 1, f"{IMG}/mac_{f['id']}")
        except FileNotFoundError:
            continue
        out.append(f"| **{nome(mat)}** | {img('img/receitas/' + p, '', 200)} | {img('img/receitas/' + a, '', 200)} |")
    out.append("")
    # bigornas
    out += ["## Bigornas", "",
            "As duas primeiras bigornas saem como no Overgeared (agachar e clicar com o martelo numa pedra ou bloco "
            "de ferro). As do tier 3 em diante são feitas na bancada:", ""]
    big = [
        ("Bigorna da Fornalha (tier 3)", {"pattern": ["RRR", " A ", "PPP"], "key": {
            "R": {"item": "kubejs:ouro_rosa_block"}, "A": {"item": "overgeared:smithing_anvil"},
            "P": {"item": "minecraft:polished_blackstone_bricks"}},
            "result": {"id": "overgeared:tier_a_smithing_anvil"}, "type": "minecraft:crafting_shaped"}),
        ("Bigorna Dracônica (tier 4)", {"pattern": ["UUU", " A ", "CDC"], "key": {
            "U": {"item": "kubejs:umbrita_block"}, "A": {"item": "overgeared:tier_a_smithing_anvil"},
            "C": {"item": "minecraft:crying_obsidian"}, "D": {"item": "kubejs:draconita_ingot"}},
            "result": {"id": "overgeared:tier_b_smithing_anvil"}, "type": "minecraft:crafting_shaped"}),
        ("Base Estelar (tier 5, vai embaixo da Bigorna Dracônica)", {"pattern": ["EVE", "VNV", "EVE"], "key": {
            "E": {"item": "kubejs:estelita_ingot"}, "V": {"item": "kubejs:vacuita_ingot"},
            "N": {"item": "minecraft:nether_star"}},
            "result": {"id": "kubejs:base_estelar"}, "type": "minecraft:crafting_shaped"}),
        ("Lingote de Adamantita (4 chapas + 4 Ouro Rosa)", {"type": "minecraft:crafting_shapeless", "ingredients": [
            {"item": "kubejs:chapa_adamantita"}] * 4 + [{"item": "kubejs:ouro_rosa_ingot"}] * 4,
            "result": {"id": "kubejs:adamantita_ingot"}}),
    ]
    for titulo, r in big:
        try:
            f = desenhar_forma(r, f"{IMG}/{r['result']['id'].split(':')[1]}")
            out += [f"**{titulo}**", "", img("img/receitas/" + f, titulo, 300), ""]
        except FileNotFoundError as e:
            out += [f"**{titulo}** — veja no EMI ({e}).", ""]
    open(f"{D}/crafts.md", "w", encoding="utf-8").write("\n".join(out) + "\n")


# ================================================================ forja_ordens.md
def pagina_forja():
    out = ["# Forja de cada Ordem", "",
           "Armaduras e armas das Ordens saem da **bigorna** (Overgeared): o formato é o mesmo da bancada, mas "
           "você martela no minigame e a peça ganha **qualidade** (Ruim até Obra-prima). Escolha sua Ordem:", ""]
    por = {}
    for r in REC["forja"]:
        rid = r["result"]["id"].split(":")[1]
        if rid.endswith("_ingot"):
            continue
        arm = next((a for a in DADOS["armaduras"] if rid.startswith(a["id"] + "_")), None)
        arma = next((a for a in DADOS["armas"] if a["id"] == rid), None)
        if arm:
            por.setdefault(arm["ordem"], {}).setdefault(arm["tier"], []).append((r, arm["pecas"].get(rid[len(arm["id"]) + 1:], rid)))
        elif arma:
            por.setdefault(arma["ordem"], {}).setdefault(arma["t"], []).append((r, arma["nome"]))
    for o in ORDEM_ORDEM:
        out.append(f'=== "{NOME_ORDEM[o]}"')
        for t in sorted(por.get(o, {})):
            mat = next((m for m in DADOS["materiais"] if m.get("ordem") == o and m["tier"] == t), None)
            out.append(f'    ??? note "Tier {t}: {mat["nome"] if mat else ""}"')
            linha = []
            for r, n in por[o][t]:
                f = desenhar_forma(r, f"{IMG}/forja_{r['result']['id'].split(':')[1]}")
                linha.append(f'<figure>{img("img/receitas/" + f, n, 186)}<figcaption>{n}</figcaption></figure>')
            out.append("        " + "".join(linha))
            out.append("")
    open(f"{D}/forja_ordens.md", "w", encoding="utf-8").write("\n".join(out) + "\n")


# ================================================================ magia.md (1.1.19: Mago do Iron's Spells)
def pagina_magia():
    import spec6
    IR = "/home/claude/irons/x/data/irons_spellbooks/recipe"

    def fig(f, t, w=240):
        return f'<figure>{img("img/receitas/" + f, t, w)}<figcaption>{t}</figcaption></figure>'

    def rec_iron(n, t, w=220):
        try:
            r = json.load(open(f"{IR}/{n}.json"))
            return fig(desenhar_forma(r, f"{IMG}/iron_{n}"), t, w)
        except Exception as e:  # noqa: BLE001
            return f"<!-- {n}: {e} -->"

    out = ["# Magia", "",
           "O **Mago** de Velária usa o **Iron's Spells 'n Spellbooks**: mana, livros de magia, pergaminhos e "
           "7 Caminhos Elementais com progressão longa (5 Círculos). As outras classes mágicas (Sacerdote, Paladino, "
           "Druida, Lâmina Arcana) continuam no **Spell Engine** com runas, no fim desta página.", "",
           '!!! info "Sem armas físicas"',
           "    O Mago não usa espada, adaga nem foice. Ele luta com o **cajado** (mão principal) e o **orbe** "
           "(mão secundária): os dois dão poder mágico, mana e recarga menor. Ao jurar, você recebe o Cajado e o "
           "Orbe de Cobre e o **Diário Frágil** (o primeiro livro de magia).", "",
           "## Como lançar", "",
           "1. Coloque o **livro de magia** no slot **Livro** dos acessórios (tecla **G**).",
           "2. Segure **Alt esquerdo** para abrir a **roda de magias** e escolha a magia.",
           "3. Aperte **H** para lançar a magia escolhida. Pergaminhos também lançam uma vez com o botão direito.",
           "4. Toda magia gasta **mana** (a barra azul). Ela volta sozinha; o orbe e as peças de Mago aumentam a mana.", "",
           "## Os 7 Caminhos Elementais", "",
           "No primeiro ponto da aba **Caminhos** (tecla **K**) você escolhe **uma** escola. A escolha fecha as outras: "
           "só as magias da sua escola funcionam e só elas entram no livro. Ao escolher, o Círculo te dá "
           "**2 pergaminhos** da escola.", "",
           "| Caminho | Escolas do Iron's | O que faz | Pergaminhos iniciais |", "| --- | --- | --- | --- |"]
    INIC = {"arcano": "Míssil Mágico, Teleporte", "fogo": "Raio de Fogo, Investida Ardente",
            "gelo": "Estalactite, Passo Gélido", "tempestade": "Eletrocutar, Carga",
            "luz": "Cura, Fogo-fátuo", "trevas": "Corte de Sangue, Agulhas de Sangue",
            "natureza": "Flecha Venenosa, Raízes"}
    for k, e in spec6.ESCOLAS_MAGO.items():
        ic = icone(e["icone"], 32)
        out.append(f"| {img(ic, e['nome'], 32) if ic else ''} **{e['nome']}** | {', '.join(e['escolas'])} | "
                   f"{e['desc']} | {INIC[k]} |")
    out += ["", '!!! tip "Arcano: o espadachim-mago"',
            "    O Caminho Arcano tem **Lâminas Conjuradas**, **Golpes Ecoantes**, **Corte das Sombras** e o "
            "**Martelo Espectral**: luta corpo a corpo com magia, sem arma física. Quem quer espada de verdade "
            "com magia joga de **Lâmina Arcana** (Spellblades).", "",
            "## Os 5 Círculos", "",
            "Cada tier que você sobe dá **+1 ponto** na aba Caminhos. Os pontos sobem o **Círculo** embaixo da sua "
            "escola. O Círculo limita o **nível máximo** que as suas magias alcançam (uma fração do nível máximo de "
            "cada feitiço) e soma **+5% de poder da escola** por Círculo.", "",
            "| Círculo | Nível das magias | Poder da escola | Quando |", "| --- | --- | --- | --- |"]
    for n, (nome_c, frac) in enumerate(spec6.CIRCULOS, start=1):
        out.append(f"| **{nome_c}** | até {int(frac * 100)}% do máximo | +{5 * n}% | "
                   + ("ao escolher o Caminho" if n == 1 else f"tier {n}") + (" · também dobra a sua Graça" if n == 5 else "")
                   + " |")
    out += ["", "Veja o seu Caminho e Círculo no jogo com **/caminho_mago**.", "",
            "## Livros de magia por tier", "",
            "Cada livro usa o material do Mago daquele tier e o livro anterior. Livros maiores têm mais espaços de magia.", ""]
    LIV = [("copper_spell_book", "kubejs:ambar_runico_ingot", "minecraft:book", "Diário Frágil (T1)"),
           ("iron_spell_book", "kubejs:cobalto_runico_ingot", "irons_spellbooks:copper_spell_book", "Tomo de Ferro (T2)"),
           ("gold_spell_book", "kubejs:adamantita_ingot", "irons_spellbooks:iron_spell_book", "Livro do Aprendiz (T3)"),
           ("diamond_spell_book", "kubejs:umbra_arcana_ingot", "irons_spellbooks:gold_spell_book", "Livro Encantado (T4)"),
           ("netherite_spell_book", "kubejs:vacuita_ingot", "irons_spellbooks:diamond_spell_book", "Códice Ancestral (T5)")]
    for i2, (lid, m, b, t) in enumerate(LIV):
        r = {"type": "minecraft:crafting_shaped", "pattern": ["MPM", "PBP", "MPM"],
             "key": {"M": {"item": m}, "P": {"item": "minecraft:paper" if i2 < 3 else "irons_spellbooks:magic_cloth"},
                     "B": {"item": b}}, "result": {"id": f"irons_spellbooks:{lid}", "count": 1}}
        try:
            out.append(fig(desenhar_forma(r, f"{IMG}/mago_{lid}"), t, 220))
        except Exception as e:  # noqa: BLE001
            out.append(f"<!-- {lid}: {e} -->")
    out += ["", "## Cajados e orbes", "",
            "Forjados na **bigorna** com **Essência Arcana** (sai de monstros mágicos e do Caldeirão Alquímico). "
            "Os números aparecem na dica do item.", "",
            "| Tier | Cajado (mão principal) | Orbe (mão secundária) |", "| --- | --- | --- |"]
    for t in range(1, 6):
        c = ", ".join(f"{k.split(':')[1].replace('_', ' ')} +{v[t - 1] if 'mana' in k and 'regen' not in k else str(int(v[t - 1] * 100)) + '%'}"
                      for k, v in spec6.MAGO_CAJADO.items() if v[t - 1])
        o = ", ".join(f"{k.split(':')[1].replace('_', ' ')} +{v[t - 1] if k.endswith('max_mana') else str(int(v[t - 1] * 100)) + '%'}"
                      for k, v in spec6.MAGO_ORBE.items() if v[t - 1])
        out.append(f"| {t} | {c} | {o} |")
    out += ["", "Receitas de cada tier na página **Forja de cada Ordem** (aba Mago).", "",
            "## Mesa de Inscrição, Caldeirão e Bigorna Arcana", ""]
    out.append(rec_iron("inscription_table", "Mesa de Inscrição: grava pergaminhos no livro"))
    out.append(rec_iron("alchemist_cauldron", "Caldeirão Alquímico: tintas e poções"))
    out.append(rec_iron("arcane_anvil", "Bigorna Arcana: orbes de melhoria"))
    out += ["", "- **Pergaminhos repetidos** viram tinta no caldeirão; tinta + papel na mesa faz o pergaminho de uma magia "
            "que você já tem, num nível maior.",
            "- **Orbes de melhoria** na Bigorna Arcana aumentam o poder de uma escola, a mana ou a recarga de uma peça.",
            "- O **Mitril** do Iron's é o **Mitril de Velária**: o minério do Iron's não nasce mais.", "",
            "## Armaduras do Mago", "",
            "As duas linhas de armadura leve do Mago (Guardiã e **Elementalista**) dão **mana máxima, poder mágico, "
            "recarga menor e resistência a magia** em cada peça. As armaduras de escola do Iron's (Piromante, "
            "Criomante...) continuam no jogo, mas com os atributos reduzidos: o endgame é o das Ordens.", "",
            "## As outras classes mágicas (Spell Engine)", "",
            "Sacerdote, Paladino, Druida e Lâmina Arcana usam o **Spell Engine**: segure a arma mágica, escolha a magia "
            "com **1 a 9** e lance com o **botão direito**. Cada magia gasta **1 runa** da escola dela.", ""]
    rj = "/tmp/wz/rj/data/runes/recipe"
    for n, t in [("healing_rune_small_hand", "Runa de Cura"), ("arcane_rune_small_hand", "Runa Arcana"),
                 ("rune_crafting_altar", "Altar de Runas (16 por vez)"), ("pouch/small_rune_pouch", "Bolsa de Runas")]:
        try:
            r = json.load(open(f"{rj}/{n}.json"))
            out.append(fig(desenhar_forma(r, f"{IMG}/{os.path.basename(n)}"), t, 200))
        except Exception as e:  # noqa: BLE001
            out.append(f"<!-- {n}: {e} -->")
    open(f"{D}/magia.md", "w", encoding="utf-8").write("\n".join(out) + "\n")


# ================================================================ teclas.md
def pagina_teclas():
    t = [("K", "Árvore de habilidades (Caminhos, Class Skills, Weapon Skills)"), ("J", "Livro de quests"),
         ("G", "Acessórios (Curios): livro de magia, bolsa de runas, joias"), ("O", "Ver sua Linhagem, Ofício e Ordem"),
         ("R", "Rolar (esquiva)"), ("Z", "Zoom (role o mouse para aproximar)"),
         ("Botões laterais do mouse", "Habilidade das espadas únicas (Simply Swords)"),
         ("Y", "Habilidade da armadura Cataclysm · Ctrl+Y capacete · Shift+Y peitoral · Alt+Y botas"),
         ("Alt esquerdo", "Mago: segurar abre a roda de magias (Iron's) · outras classes: volta à hotbar normal"),
         ("H", "Mago: lançar a magia escolhida na roda"),
         ("M", "Mapa (Diorama) · Shift+M configurações · Alt+M liga/desliga o minimapa"),
         ("Ctrl+M", "Mapa do FTB Chunks: proteger terreno"), ("Ctrl+B / Shift+N", "Marcar ponto / lista de pontos"),
         ("V", "Carteira de moedas"), ("=", "Caixa eletrônico portátil"), ("\\", "Terminal de comércio"),
         ("U", "Ligar/desligar PvP"), (",", "Painel de guerra"), (".", "Time / guilda"),
         ("C", "Emotes"), ("I", "Sentar"), ("B", "Best in Pack"), ("Alt+R / Alt+G / Alt+X / F7",
                                                                  "Dragão: fogo, golpe, descer e câmera"),
         ("F9 / F10", "Escolher shader / ligar e desligar shader"), ("Ctrl+N", "Visão noturna da Linhagem"),
         ("` (crase)", "Ultimine: quebrar o veio todo")]
    out = ["# Teclas", "",
           "O modpack já vem com as teclas organizadas, sem conflitos. Se você trocou alguma, as suas continuam. "
           "Para mudar: **Opções → Controles → Atalhos**.", "",
           "| Tecla | O que faz |", "| --- | --- |"] + [f"| <kbd>{a}</kbd> | {b} |" for a, b in t]
    open(f"{D}/teclas.md", "w", encoding="utf-8").write("\n".join(out) + "\n")


# ================================================================ minerios.md (tabela com fotos maiores)
def tabela_minerios():
    p = f"{D}/minerios.md"
    txt = open(p, encoding="utf-8").read()
    ini = txt.index("## Onde achar cada um")
    fim = txt.index("\n", txt.index("| --- |", ini))
    resto = txt[fim + 1:]
    # pula as linhas da tabela antiga
    resto_linhas = resto.split("\n")
    while resto_linhas and resto_linhas[0].startswith("|"):
        resto_linhas.pop(0)
    nova = ["## Onde achar cada um", "",
            "| Minério | Vira | Nome | Onde | Picareta mínima | Comprador do Rei | Para quem |",
            "| --- | --- | --- | --- | --- | --- | --- |"]
    for m in sorted(spec5.MATERIAIS, key=lambda m: (m["tier"], DADOS["req"].get(f"kubejs:{m['id']}_ore", 99))):
        ore = next((f"img/minerios/{m['id']}_ore.{e}" for e in ("gif", "png")
                    if os.path.exists(f"{D}/img/minerios/{m['id']}_ore.{e}")), None)
        mat = next((x for x in DADOS["materiais"] if x["id"] == m["id"]), None)
        it = mat["item"] if mat else f"kubejs:{m['id']}_ingot"
        ico = icone(it, 48) if not it.startswith("#") else None
        req = DADOS["req"].get(f"kubejs:{m['id']}_ore")
        pic = spec5.CADEIA[req][2] if req is not None else "—"
        dono = spec5.MINERIO_ORDEM.get(m["id"])
        nova.append(f"| {img(ore, '', 64) if ore else ''} | {img(ico, '', 40) if ico else ''} | "
                    f"**{m['nome']}** · T{m['tier']} | {m.get('onde', '')} | {pic} | {m.get('loja', '')} | "
                    f"{NOME_ORDEM.get(dono, 'liga') if dono else 'ingrediente de liga'} |")
    txt = txt[:ini] + "\n".join(nova) + "\n" + "\n".join(resto_linhas)
    open(p, "w", encoding="utf-8").write(txt)


if __name__ == "__main__":
    pagina_crafts()
    pagina_forja()
    pagina_magia()
    pagina_teclas()
    tabela_minerios()
    print("ok:", len(os.listdir(IMG)), "receitas,", len(os.listdir(ICO)), "ícones")
