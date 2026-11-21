"""Imagens da wiki feitas com as texturas ATUAIS do pack (rodar de novo quando uma textura mudar).

Gera em docs/img:
  cenas/vitrine_mina.gif, vitrine_nether.gif, vitrine_end.gif  → blocos de minério em 3D, animados
  cenas/itens_blocos.png                                         → folha com minérios, lingotes, gemas, ligas e blocos
  anim/gemas.gif, anim/lingotes.gif                              → faixas animadas com os nomes
"""
import json
import math
import os
import sys

from PIL import Image, ImageDraw, ImageFont

sys.path.insert(0, "/home/claude/tools")
import spec5  # noqa: E402

KJS = "/home/claude/kit5/kubejs/assets/kubejs/textures"
MC = "/home/claude/tex/mc/assets/minecraft/textures/block"
D = "/home/claude/wiki/docs/img"
DADOS = json.load(open("/home/claude/tools/v5_dados.json"))
FONTE = "/usr/share/fonts/opentype/inter/Inter-SemiBold.otf"
FONTE_B = "/usr/share/fonts/opentype/inter/Inter-Bold.otf"
FUNDO = (30, 30, 42)
CORES_T = {1: (255, 85, 85), 2: (85, 255, 85), 3: (255, 170, 0), 4: (85, 85, 255), 5: (255, 85, 255)}
BASE = {"stone": "stone", "both": "stone", "deepslate": "deepslate", "netherrack": "netherrack",
        "basalt": "basalt_side", "end_stone": "end_stone"}


def frames_png(caminho):
    im = Image.open(caminho).convert("RGBA")
    w, h = im.size
    ft = 1
    if h > w and os.path.exists(caminho + ".mcmeta"):
        ft = json.load(open(caminho + ".mcmeta")).get("animation", {}).get("frametime", 1)
    return [im.crop((0, i * w, w, (i + 1) * w)) for i in range(max(1, h // w))], ft


def textura_minerio(mid, ardosia=False):
    """Quadros 16x16 do minério: pedra vanilla + veio (animado quando tem .mcmeta)."""
    m = spec5.MAT[mid]
    base_nome = "deepslate" if ardosia else BASE.get(m.get("base", "stone"), "stone")
    base = Image.open(f"{MC}/{base_nome}.png").convert("RGBA").resize((16, 16), Image.NEAREST)
    veio = f"{KJS}/block/{'deepslate_' if ardosia else ''}{mid}_ore_veio.png"
    if os.path.exists(veio):
        fr, ft = frames_png(veio)
        out = []
        for f in fr:
            q = base.copy()
            q.alpha_composite(f.resize((16, 16), Image.NEAREST))
            out.append(q)
        return out, ft
    fr, ft = frames_png(f"{KJS}/block/{'deepslate_' if ardosia else ''}{mid}_ore.png")
    return [f.resize((16, 16), Image.NEAREST) for f in fr], ft


def cubo(tex, k=4):
    """Cubo isométrico com a mesma textura nas 3 faces (topo claro, esquerda média, direita escura)."""
    n = tex.width
    w = 2 * n * k
    h = 2 * n * k
    im = Image.new("RGBA", (w + 2, h + 2), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    px = tex.load()
    cx, topo = w / 2, 0
    ax, ay = k, k / 2  # passo de um texel na diagonal

    def face(origem, du, dv, fator):
        for v in range(n):
            for u in range(n):
                r, g, b, a = px[u, v]
                if a == 0:
                    continue
                c = (int(r * fator), int(g * fator), int(b * fator), 255)
                p0 = (origem[0] + du[0] * u + dv[0] * v, origem[1] + du[1] * u + dv[1] * v)
                pts = [p0, (p0[0] + du[0], p0[1] + du[1]), (p0[0] + du[0] + dv[0], p0[1] + du[1] + dv[1]),
                       (p0[0] + dv[0], p0[1] + dv[1])]
                d.polygon(pts, fill=c)
    # topo: losango
    face((cx, topo), (ax, ay), (-ax, ay), 1.0)
    # esquerda
    face((0, topo + n * ay), (ax, ay), (0, k), 0.78)
    # direita
    face((cx, topo + n * ay * 2), (ax, -ay), (0, k), 0.6)
    return im


def nome_mat(mid):
    m = spec5.MAT.get(mid)
    return m["nome"] if m else mid


def texto(d, xy, s, tam=18, cor=(235, 235, 245), fonte=FONTE, ancora="mm"):
    d.text(xy, s, font=ImageFont.truetype(fonte, tam), fill=cor, anchor=ancora)


def salvar_gif(quadros, destino, dur):
    pal = [q.convert("RGB").convert("P", palette=Image.ADAPTIVE, colors=255) for q in quadros]
    pal[0].save(destino, save_all=True, append_images=pal[1:], duration=dur, loop=0, optimize=False, disposal=2)


def vitrine(itens, titulo, sub, destino, por_linha=8, k=4):
    """itens: lista de (rótulo, tier, quadros, frametime). Gera GIF de 20 quadros."""
    cel_w, cel_h = 2 * 16 * k + 40, 2 * 16 * k + 70
    linhas = math.ceil(len(itens) / por_linha)
    cols = min(por_linha, len(itens))
    W, H = cols * cel_w + 40, linhas * cel_h + 110
    quadros = []
    for f in range(20):
        im = Image.new("RGBA", (W, H), FUNDO + (255,))
        d = ImageDraw.Draw(im)
        texto(d, (24, 30), titulo, 30, (255, 255, 255), FONTE_B, "lm")
        texto(d, (24, 66), sub, 17, (180, 180, 200), FONTE, "lm")
        for i, (rot, t, fr, ft) in enumerate(itens):
            col, lin = i % por_linha, i // por_linha
            x0, y0 = 20 + col * cel_w, 100 + lin * cel_h
            q = fr[(f * 2 // ft) % len(fr)]
            c = cubo(q, k)
            im.alpha_composite(c, (x0 + 20, y0))
            d.rounded_rectangle([x0 + 22, y0 + c.height + 8, x0 + 22 + 30, y0 + c.height + 30], 5, fill=CORES_T[t])
            texto(d, (x0 + 37, y0 + c.height + 19), f"T{t}", 14, (20, 20, 20), FONTE_B)
            texto(d, (x0 + 60, y0 + c.height + 19), rot, 17, (235, 235, 245), FONTE, "lm")
        quadros.append(im)
    salvar_gif(quadros, destino, 100)


def faixa(itens, destino, k=4):
    """Faixa horizontal de itens 2D grandes com o nome embaixo (GIF)."""
    cel = 16 * k + 70
    W, H = len(itens) * cel + 20, 16 * k + 60
    quadros = []
    for f in range(20):
        im = Image.new("RGBA", (W, H), (44, 42, 62, 255))
        d = ImageDraw.Draw(im)
        for i, (rot, fr, ft) in enumerate(itens):
            q = fr[(f * 2 // ft) % len(fr)].resize((16 * k, 16 * k), Image.NEAREST)
            x = 10 + i * cel + (cel - 16 * k) // 2
            im.alpha_composite(q, (x, 8))
            texto(d, (10 + i * cel + cel // 2, 16 * k + 32), rot, 16)
        quadros.append(im)
    salvar_gif(quadros, destino, 100)


def item_frames(item):
    mod, nome = item.split(":")
    p = f"{KJS}/item/{nome}.png"
    return frames_png(p)


def main():
    os.makedirs(f"{D}/cenas", exist_ok=True)
    os.makedirs(f"{D}/anim", exist_ok=True)
    mats = sorted(spec5.MATERIAIS, key=lambda m: (m["tier"], m["id"]))
    over, nether, end = [], [], []
    for m in mats:
        fr, ft = textura_minerio(m["id"])
        alvo = end if m.get("base") == "end_stone" else nether if m.get("base") in ("netherrack", "basalt") else over
        alvo.append((m["nome"], m["tier"], fr, ft))
        if m.get("base") == "both":
            fr2, ft2 = textura_minerio(m["id"], ardosia=True)
            over.append((m["nome"] + " (ardósia)", m["tier"], fr2, ft2))
    vitrine(over, "Mina — Overworld", "Tiers 1 e 2 na pedra; os mais fundos na ardósia. Os raros brilham e se mexem.",
            f"{D}/cenas/vitrine_mina.gif", por_linha=6)
    vitrine(nether, "Nether — tier 3", "Netherrack, basalto e as florestas do Nether.",
            f"{D}/cenas/vitrine_nether.gif", por_linha=5)
    vitrine(end, "End — tier 5", "Só nas ilhas externas, depois do dragão.", f"{D}/cenas/vitrine_end.gif", por_linha=3)

    # gemas e lingotes
    gemas, lingotes = [], []
    for m in DADOS["materiais"]:
        if m.get("tipo") == "liga":
            continue
        it = m.get("item", "")
        if not it.startswith("kubejs:"):
            continue
        fr, ft = item_frames(it)
        (lingotes if it.endswith("_ingot") else gemas).append((m["nome"], fr, ft))
    faixa(gemas, f"{D}/anim/gemas.gif")
    faixa(lingotes, f"{D}/anim/lingotes.gif")

    # folha geral (primeiro quadro de tudo)
    secoes = [("Minérios", [(n, t, fr[0]) for n, t, fr, _ in over + nether + end], True),
              ("Lingotes e gemas", [(m["nome"], m["tier"], item_frames(m["item"])[0][0]) for m in DADOS["materiais"]
                                    if m.get("tipo") != "liga" and str(m.get("item", "")).startswith("kubejs:")], False),
              ("Ligas forjadas na bigorna", [(m["nome"], m["tier"], item_frames(m["item"])[0][0])
                                             for m in DADOS["materiais"] if m.get("tipo") == "liga"], False)]
    cel, por = 120, 11
    H = 90
    for _, it, cubo_ in secoes:
        H += 60 + math.ceil(len(it) / por) * (150 if cubo_ else 120)
    W = por * cel + 40
    im = Image.new("RGBA", (W, H), (245, 245, 248, 255))
    d = ImageDraw.Draw(im)
    d.rectangle([0, 0, W, 64], fill=(52, 52, 70))
    texto(d, (24, 32), "Velária — itens e blocos (texturas atuais)", 28, (255, 255, 255), FONTE_B, "lm")
    y = 84
    for nome_sec, it, eh_cubo in secoes:
        texto(d, (24, y + 18), nome_sec, 24, (50, 50, 66), FONTE_B, "lm")
        y += 50
        alt = 150 if eh_cubo else 120
        for i, (rot, t, tex) in enumerate(it):
            x = 20 + (i % por) * cel
            yy = y + (i // por) * alt
            if eh_cubo:
                c = cubo(tex.resize((16, 16), Image.NEAREST), 3)
                im.alpha_composite(c, (x + (cel - c.width) // 2, yy))
                ty = yy + c.height + 14
            else:
                q = tex.resize((64, 64), Image.NEAREST)
                im.alpha_composite(q, (x + (cel - 64) // 2, yy + 6))
                ty = yy + 84
            d.rounded_rectangle([x + 6, yy, x + 26, yy + 16], 4, fill=CORES_T[t])
            texto(d, (x + 16, yy + 8), str(t), 12, (20, 20, 20), FONTE_B)
            for j, parte in enumerate(rot.split(" (")):
                texto(d, (x + cel // 2, ty + j * 16), parte if j == 0 else "(" + parte, 13, (60, 60, 76))
        y += math.ceil(len(it) / por) * alt + 10
    im.convert("RGB").save(f"{D}/cenas/itens_blocos.png")
    print("ok")


if __name__ == "__main__":
    main()
