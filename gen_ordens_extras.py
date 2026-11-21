"""Ordens: bloco 'Todas as armaduras que a Ordem pode vestir' (conjuntos da Ordem + mods de classe + conjuntos temáticos).
Idempotente: substitui o bloco entre os marcadores em docs/ordens.md."""
import os, re, shutil
D = "/home/claude/wiki/docs"; M = "/home/claude/tools/mods_molde"
os.makedirs(f"{D}/img/icones/mods", exist_ok=True)
def ic(chave):
    for suf in ("_chest.png", "_chestplate.png"):
        f = f"{M}/{chave}{suf}"
        if os.path.exists(f):
            shutil.copy(f, f"{D}/img/icones/mods/{chave}.png"); return f'<img src="img/icones/mods/{chave}.png" width="28" alt=""> '
    return ""
# (nome, mod, ícone) — armaduras de mods de classe exclusivas de cada Ordem
CLASSE = {
 "guerreiro": [("Guerreiro", "Rogues & Warriors", "rogues__warrior_armor"), ("Investida (Onslaught)", "Armory RPGs", "")],
 "paladino": [("Paladino e Cruzado", "Paladins & Priests", "paladins__paladin_armor"), ("Portador da Luz", "Armory RPGs", "armory__lightbringer_armor")],
 "sacerdote": [("Sacerdote e Prior", "Paladins & Priests", "paladins__priest_robe"), ("Absolvição", "Armory RPGs", "armory__absolution_robe")],
 "mago": [("Robes de escola (Piromante, Criomante, Eletromante, Cultista...)", "Iron's Spells 'n Spellbooks", "")],
 "ladino": [("Ladino e Assassino", "Rogues & Warriors", "rogues__rogue_armor"), ("Matador (Slayer)", "Armory RPGs", "")],
 "arqueiro": [("Arqueiro e Patrulheiro", "Archers", "rogues__assassin_armor"), ("Riftstalker", "Armory RPGs", "armory__riftstalker_armor")],
 "berserker": [("Nortenho, Selvagem e Senhor da Guerra", "Berserker RPG", "berserker__warlord"), ("Senhor da Guerra", "Armory RPGs", "")],
 "bruxo": [("Escolas do Lobo, do Gato e outras", "Witcher RPG", "witcher__wolven")],
 "druida": [("Mantos de druida", "Druids", "")],
 "monge": [("Aken e Phasleb", "Forcemaster RPG", "forcemaster__aken")],
 "lamina_arcana": [],
}
TEMA = [("Samurai", "Samurai Dynasty", ["guerreiro", "lamina_arcana", "monge"], "samurai__master"),
 ("Shinobi", "Samurai Dynasty", ["ladino", "monge"], "samurai__ninja"),
 ("Druzhina", "Epic Knights: Slavic Armory", ["berserker", "bruxo"], ""),
 ("Nórdico", "Immersive Armors (Warrior), Epic Knights: Dark Ages", ["berserker", "guerreiro"], ""),
 ("Legião Antiga", "Epic Knights: Antique Legacy", ["guerreiro", "paladino"], ""),
 ("Sagrado", "Immersive Armors (Divine), Fantasy Armor", ["sacerdote", "paladino"], ""),
 ("Mantos Arcanos", "Immersive Armors (Robe), Fantasy Armor", ["mago", "sacerdote", "druida"], "immersive__robe"),
 ("Sombras", "Fantasy Armor e outros", ["ladino", "bruxo", "arqueiro"], ""),
 ("Selvagem", "Immersive Armors (Bone, Wooden) e outros", ["druida", "arqueiro", "berserker"], ""),
 ("Cavaleiro", "Epic Knights (+ Addon), Immersive Armors (Heavy), Fantasy Armor", ["paladino", "guerreiro"], "epic__knight")]
ICT = {"epic__knight": "epic__knight_chestplate", "immersive__robe": "immersive__robe_chestplate"}
NOMES = {"Legião de Ferro": "guerreiro", "Ordem da Aurora": "paladino", "Clã da Fúria": "berserker", "Irmandade do Véu": "ladino",
 "Patrulheiros do Vento": "arqueiro", "Escola do Lobo": "bruxo", "Mosteiro do Punho": "monge", "Lâminas do Crepúsculo": "lamina_arcana",
 "Chama Branca": "sacerdote", "Círculo Arcano": "mago"}
def bloco(o):
    L = ['<!-- extras:ini -->', '<details class="todas-armaduras" markdown><summary>Todas as armaduras que esta Ordem pode vestir</summary>', '',
         '- **Da própria Ordem:** linha de Defesa (Guardiã) e linha de Ataque, tiers 1 a 5 (veja acima e na [Lista de armaduras](armaduras.md)).']
    for n, mod, k in CLASSE.get(o, []):
        L.append(f'- {ic(k) if k else ""}**{n}** · {mod} · exclusiva da Ordem')
    for n, mod, ords, k in TEMA:
        if o in ords:
            outras = ", ".join(x for x in ords if x != o)
            L.append(f'- {ic(ICT.get(k, k)) if k else ""}**{n}** · {mod} · conjunto temático (também: {outras}); 4 peças dão bônus de conjunto')
    L += ['- **Vanilla** (couro, cota de malha, ferro, ouro, diamante, netherita): livre para todos, respeitando a trava de tier.', '',
          'Peças de outros mods têm os atributos reduzidos e seguem a trava de tier (diamante = tier 2, netherita = tier 3, aço de dragão = tier 4): o endgame é o da Ordem.',
          '</details>', '<!-- extras:fim -->']
    return "\n".join(L)
s = open(f"{D}/ordens.md", encoding="utf-8").read()
s = re.sub(r"\n?<!-- extras:ini -->.*?<!-- extras:fim -->", "", s, flags=re.S)
out = []; atual = None
for linha in s.split("\n"):
    m = re.search(r"<h2>(.*?)</h2>", linha)
    if m: atual = NOMES.get(m.group(1)) or ("druida" if "Druida" in linha else None)
    if linha.startswith('<div class="caminhos">') and atual:
        out.append(linha); out.append(bloco(atual)); atual = None; continue
    out.append(linha)
open(f"{D}/ordens.md", "w", encoding="utf-8").write("\n".join(out))
print(s.count('<div class="caminhos">'), "\n".join(out).count("extras:ini"))
