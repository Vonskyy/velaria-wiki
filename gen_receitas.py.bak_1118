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


def ing(k):
    """Ingrediente de receita (item ou tag) → item com textura."""
    if isinstance(k, list):
        k = k[0]
    it = k.get("item") or k.get("tag")
    if "tag" in k:
        it = {"minecraft:wool": "minecraft:white_wool", "c:ingots/silver": "minecraft:iron_ingot",
              "runes:fancy_stone_materials": "minecraft:polished_andesite",
              "minecraft:stone_tool_materials": "minecraft:cobblestone"}.get(k["tag"], "minecraft:barrier")
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


# ================================================================ magia.md
def pagina_magia():
    wz = "/tmp/wz/wj/data/wizards/recipe"
    rj = "/tmp/wz/rj/data/runes/recipe"

    def rec(caminho):
        r = json.load(open(caminho))
        return desenhar_forma(r, f"{IMG}/{os.path.basename(caminho)[:-5]}")

    def fig(f, t, w=240):
        return f'<figure>{img("img/receitas/" + f, t, w)}<figcaption>{t}</figcaption></figure>'

    out = ["# Magia", "",
           "As magias usam o **Spell Engine**: Mago (Wizards), Sacerdote e Paladino (Paladins), Lâmina Arcana "
           "(Spellblades) e as habilidades das outras classes. Este guia é do **Mago**, mas as regras de runas e "
           "árvore valem para todos.", "",
           "!!! warning \"Sem runa, sem magia\"",
           "    Toda magia gasta **1 runa da escola dela** a cada lançamento. Se o cajado não solta nada, faltam "
           "runas. Quem jura pelo Círculo Arcano ganha 32 runas de cada escola e uma **Bolsa de Runas**.", "",
           "## Como lançar", "",
           "1. Segure uma **varinha** ou **cajado**. A barra de magias aparece no lugar da hotbar.",
           "2. Use as teclas **1 a 9** para escolher a magia e o **botão direito** para lançar.",
           "3. Segure **Alt** para voltar à hotbar normal sem largar o cajado.",
           "4. Aperte **K → Class Skills** e escolha a raiz **Arcano, Fogo ou Gelo**. Cada ponto destranca uma "
           "magia nova. Os pontos vêm de matar monstros.", "",
           "## Runas", ""]
    for n, t in [("arcane_rune_small_hand", "Runa Arcana (bancada)"), ("fire_rune_small_hand", "Runa de Fogo"),
                 ("frost_rune_small_hand", "Runa de Gelo"), ("healing_rune_small_hand", "Runa de Cura"),
                 ("rune_crafting_altar", "Altar de Runas (16 por vez)"), ("pouch/small_rune_pouch", "Bolsa de Runas")]:
        try:
            out.append(fig(rec(f"{rj}/{n}.json"), t, 200))
        except Exception as e:  # noqa: BLE001
            out.append(f"<!-- {n}: {e} -->")
    out += ["", "## Varinhas e cajados por tier", "",
            "| Tier | Arma | Receita |", "| --- | --- | --- |"]
    linhas = [(1, "wand_novice", "Varinha do Novato (vem no kit)"), (1, "wand_arcane", "Varinha Arcana"),
              (1, "wand_fire", "Varinha de Fogo"), (1, "wand_frost", "Varinha de Gelo"),
              (2, "staff_wizard", "Cajado do Mago"), (3, "staff_arcane", "Cajado Arcano"),
              (3, "staff_fire", "Cajado de Fogo"), (3, "staff_frost", "Cajado de Gelo"),
              (4, "staff_netherite_arcane_smithing", "Cajado Arcano de Netherite"),
              (4, "staff_netherite_fire_smithing", "Cajado de Fogo de Netherite"),
              (4, "staff_netherite_frost_smithing", "Cajado de Gelo de Netherite")]
    for t, n, titulo in linhas:
        try:
            f = rec(f"{wz}/{n}.json")
            out.append(f"| {t} | **{titulo}** | {img('img/receitas/' + f, titulo, 220)} |")
        except Exception as e:  # noqa: BLE001
            out.append(f"| {t} | **{titulo}** | veja no EMI |")
    out += ["", "## Mantos", "",
            "Mantos dão pouca armadura e muito **poder mágico**. Só o Círculo Arcano veste.", ""]
    for n, t in [("wizard_robe_chest", "Manto do Mago (tiers 1–2)"), ("arcane_robe_chest", "Manto Arcano (tier 3)"),
                 ("fire_robe_chest", "Manto de Fogo (tier 3)"), ("frost_robe_chest", "Manto de Gelo (tier 3)"),
                 ("netherite_arcane_robe_chest_smithing", "Manto Arcano de Netherite (tier 4)")]:
        try:
            out.append(fig(rec(f"{wz}/{n}.json"), t, 220))
        except Exception as e:  # noqa: BLE001
            out.append(f"<!-- {n}: {e} -->")
    out += ["", "No tier 5 vêm os mantos do **Armory**: Tempestade, Fumegante e Tecelã do Gelo, melhorados com o "
            "Cristal do Conquistador (Arcano e Fogo) ou do Vencedor (Gelo) na mesa de ferraria.", "",
            "## Tomos de magia", "",
            "A **Mesa de Vinculação** transforma um livro no **Tomo** da sua escola. Vincule as magias do tomo "
            "pagando níveis de XP e lápis, e equipe o tomo no slot de Livro de Magia (tecla **G**).", ""]
    try:
        r = json.load(open("/tmp/wz/se_binding.json"))
        out.append(fig(desenhar_forma(r, f"{IMG}/spell_binding"), "Mesa de Vinculação", 220))
    except Exception:  # noqa: BLE001
        pass
    open(f"{D}/magia.md", "w", encoding="utf-8").write("\n".join(out) + "\n")


# ================================================================ teclas.md
def pagina_teclas():
    t = [("K", "Árvore de habilidades (Caminhos, Class Skills, Weapon Skills)"), ("J", "Livro de quests"),
         ("G", "Acessórios (Curios): bolsa de runas, tomo, joias"), ("O", "Ver sua Linhagem, Ofício e Ordem"),
         ("R", "Rolar (esquiva)"), ("Z", "Zoom (role o mouse para aproximar)"),
         ("Botões laterais do mouse", "Habilidade das espadas únicas (Simply Swords)"),
         ("Y", "Habilidade da armadura Cataclysm · Ctrl+Y capacete · Shift+Y peitoral · Alt+Y botas"),
         ("Alt", "Segurar: volta à hotbar normal com cajado na mão"),
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
