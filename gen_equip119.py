"""Imagens da wiki para a 1.1.19: linha de Ataque em 3D, brilho animado das armaduras e equipamento de cada Ordem.

Saída (docs/img):
  galeria/linha_ataque_3d_a.png, _b.png   linha de Ataque vestida (frente e 3/4), Ordem x tier
  galeria/brilho_animado.gif              camada brilhante animada de 8 conjuntos de tier 5
  equip/<ordem>.gif                       por tier: Guardiã (4 peças) | Ataque (4 peças) | armas/focos (animado)
Uso: python3 -I gen_equip119.py
"""
import json
import os
import subprocess
import sys

from PIL import Image, ImageDraw, ImageFont

sys.path.insert(0, "/home/claude/tools")
K = "/home/claude/kit5/kubejs/assets/kubejs"
D = "/home/claude/wiki/docs/img"
T = "/tmp/eq119"
os.makedirs(T, exist_ok=True)
DADOS = json.load(open("/home/claude/tools/v5_dados.json", encoding="utf-8"))
ORDENS = ["guerreiro", "paladino", "berserker", "ladino", "arqueiro", "bruxo", "monge", "lamina_arcana",
          "sacerdote", "mago", "druida"]
NOME = {"guerreiro": "Guerreiro", "paladino": "Paladino", "berserker": "Berserker", "ladino": "Ladino",
        "arqueiro": "Arqueiro", "bruxo": "Bruxo", "monge": "Monge", "lamina_arcana": "Lâmina Arcana",
        "sacerdote": "Sacerdote", "mago": "Mago", "druida": "Druida"}
FONTE = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
FUNDO = (22, 22, 30, 255)
CELULA = (30, 31, 42, 255)


def fonte(t):
    try:
        return ImageFont.truetype(FONTE, t)
    except OSError:
        return ImageFont.load_default()


def render(geo, tex, destino, escala=6):
    subprocess.run(["python3", "-I", "/home/claude/tools/render_geo.py", geo, tex, destino, str(escala)], check=True,
                   stdout=subprocess.DEVNULL)
    return Image.open(destino).convert("RGBA")


def somar(base, emi):
    b = base.copy()
    pb, pe = b.load(), emi.load()
    for y in range(b.height):
        for x in range(b.width):
            if pe[x, y][3]:
                c, e = pb[x, y], pe[x, y]
                pb[x, y] = (min(255, c[0] + e[0]), min(255, c[1] + e[1]), min(255, c[2] + e[2]), c[3])
    return b


def grade_3d(ordens, destino):
    """Linha de Ataque vestida: uma linha por Ordem, uma coluna por tier (frente e 3/4)."""
    cw, ch, rot = 360, 200, 178
    W = rot + cw * 5 + 6 * 4
    H = len(ordens) * (ch + 8)
    img = Image.new("RGBA", (W, H), FUNDO)
    dr = ImageDraw.Draw(img)
    for r, o in enumerate(ordens):
        y = r * (ch + 8)
        b = [a for a in DADOS["armaduras"] if a["ordem"] == o and a["estilo"] == "b"]
        dr.text((14, y + ch // 2 - 22), NOME[o], font=fonte(20), fill=(240, 240, 245))
        if b:
            dr.text((14, y + ch // 2 + 6), b[0]["linha"], font=fonte(13), fill=(230, 120, 110))
        for a in sorted(b, key=lambda a: a["tier"]):
            x = rot + (a["tier"] - 1) * (cw + 6)
            dr.rectangle([x, y, x + cw, y + ch], fill=CELULA)
            im = render(f"{K}/geo/{a['id']}.geo.json", f"{K}/textures/armor/{a['id']}.png", f"{T}/{a['id']}.png", 4)
            q = im.width // 4
            for k in range(2):
                v = im.crop((k * q, 0, (k + 1) * q, im.height))
                v.thumbnail((cw // 2, ch - 26))
                img.alpha_composite(v, (x + k * cw // 2 + (cw // 2 - v.width) // 2, y + 4))
            txt = f"T{a['tier']} · {a['nome']}"
            tw = dr.textlength(txt, font=fonte(14))
            dr.text((x + (cw - tw) / 2, y + ch - 22), txt, font=fonte(14), fill=(215, 215, 225))
    img.convert("RGB").save(destino)


def brilho_gif(destino):
    ids = []
    for o in ORDENS[:8]:
        a = next(a for a in DADOS["armaduras"] if a["ordem"] == o and a["tier"] == 5 and a["estilo"] == "b")
        ids.append(a)
    quadros = []
    for f in range(8):
        linha = []
        for a in ids:
            base = Image.open(f"{K}/textures/armor/{a['id']}.png").convert("RGBA")
            emi = Image.open(f"{K}/textures/armor/brilho/{a['id']}_{f}.png").convert("RGBA")
            somar(base, emi).save(f"{T}/t.png")
            im = render(f"{K}/geo/{a['id']}.geo.json", f"{T}/t.png", f"{T}/g.png", 5)
            linha.append(im.crop((0, 0, im.width // 4, im.height)))
        W = sum(x.width for x in linha)
        fr = Image.new("RGBA", (W, linha[0].height + 30), FUNDO)
        dr = ImageDraw.Draw(fr)
        x = 0
        for im, a in zip(linha, ids):
            fr.alpha_composite(im, (x, 0))
            tw = dr.textlength(NOME[a["ordem"]], font=fonte(13))
            dr.text((x + (im.width - tw) / 2, im.height + 6), NOME[a["ordem"]], font=fonte(13), fill=(220, 220, 230))
            x += im.width
        quadros.append(fr.convert("P", palette=Image.ADAPTIVE))
    quadros[0].save(destino, save_all=True, append_images=quadros[1:], duration=100, loop=0)


def icone_frames(it):
    p = f"{K}/textures/item/{it}.png"
    im = Image.open(p).convert("RGBA")
    w = im.width
    return [im.crop((0, i * w, w, (i + 1) * w)).resize((32, 32), Image.NEAREST) for i in range(im.height // w)]


def equip_gif(o, destino):
    """Por tier: Guardiã (4) | Ataque (4) | armas e focos, animado como no jogo."""
    S = 32
    linhas = []
    for t in range(1, 6):
        arms = sorted([a for a in DADOS["armaduras"] if a["ordem"] == o and a["tier"] == t], key=lambda a: a["estilo"])
        armas = [a for a in DADOS["armas"] if a.get("ordem") == o and a.get("t") == t]
        itens = [[f"{a['id']}_{p}" for p in ("helmet", "chestplate", "leggings", "boots")] for a in arms]
        itens.append([a["id"] for a in armas])
        linhas.append(itens)
    largura = 60 + (4 * (S + 4) + 18) * 2 + 3 * (S + 4)
    altura = 30 + 5 * (S + 12)
    n = 12
    frames_cache = {}
    quadros = []
    for f in range(n):
        img = Image.new("RGBA", (largura, altura), FUNDO)
        dr = ImageDraw.Draw(img)
        dr.text((60, 6), "Guardiã", font=fonte(12), fill=(140, 220, 140))
        dr.text((60 + 4 * (S + 4) + 18, 6), "Ataque", font=fonte(12), fill=(230, 120, 110))
        dr.text((60 + 2 * (4 * (S + 4) + 18), 6), "Armas", font=fonte(12), fill=(220, 220, 230))
        for t, itens in enumerate(linhas, start=1):
            y = 26 + (t - 1) * (S + 12)
            dr.text((10, y + 8), f"T{t}", font=fonte(14), fill=(220, 220, 230))
            x = 60
            for g, grupo in enumerate(itens):
                for it in grupo:
                    if it not in frames_cache:
                        try:
                            frames_cache[it] = icone_frames(it)
                        except FileNotFoundError:
                            frames_cache[it] = [Image.new("RGBA", (S, S))]
                    fr = frames_cache[it]
                    img.alpha_composite(fr[f % len(fr)], (x, y))
                    x += S + 4
                x += 18 if g < len(itens) - 1 else 0
        quadros.append(img.convert("P", palette=Image.ADAPTIVE))
    quadros[0].save(destino, save_all=True, append_images=quadros[1:], duration=100, loop=0)


if __name__ == "__main__":
    grade_3d(ORDENS[:6], f"{D}/galeria/linha_ataque_3d_a.png")
    grade_3d(ORDENS[6:], f"{D}/galeria/linha_ataque_3d_b.png")
    brilho_gif(f"{D}/galeria/brilho_animado.gif")
    for o in ORDENS:
        equip_gif(o, f"{D}/equip/{o}.gif")
    print("ok")
