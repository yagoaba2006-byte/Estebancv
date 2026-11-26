# -*- coding: utf-8 -*-
"""QR code du sondage, et sa diapo de projection.
Relancer apres tout changement d'adresse :  python3 qr.py
Les fichiers sont ecrits dans ../qr/"""
import os
import segno
from PIL import Image, ImageDraw, ImageFont

ICI = os.path.dirname(os.path.abspath(__file__))
SORTIE = os.path.join(os.path.dirname(ICI), 'qr', '')
os.makedirs(SORTIE, exist_ok=True)

URL = "https://yagoaba2006-byte.github.io/sondage-mondelez/"

# charte de la page : blanc, un accent violet, neutres tires vers le violet
VIOLET   = (123, 79, 160)
ENCRE    = (22, 22, 29)
DOUX     = (107, 107, 123)
FILET    = (236, 234, 242)
PALE     = (243, 237, 250)

SERIF = None
SANS  = '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'
SANSB = '/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'

# ------------------------------------------------------------------
# 1. le QR seul : noir sur blanc, la version la plus sure a scanner
# ------------------------------------------------------------------
code = segno.make(URL, error='q')
code.save(SORTIE + 'qr-sondage.png', scale=24, border=4, dark='#000000', light='#ffffff')
code.save(SORTIE + 'qr-sondage.svg', scale=12, border=4, dark='#000000', light='#ffffff')
# version violette, a reserver aux supports imprimes de qualite
code.save(SORTIE + 'qr-sondage-violet.png', scale=24, border=4, dark='#7b4fa0', light='#ffffff')

# ------------------------------------------------------------------
# 2. la diapo 1920 x 1080, a projeter telle quelle
# ------------------------------------------------------------------
L, H = 1920, 1080
dia = Image.new('RGB', (L, H), (255, 255, 255))
d = ImageDraw.Draw(dia)

def tenir(texte, chemin, taille, largeur):
    """Reduit la police jusqu'a ce que le texte tienne dans la largeur."""
    t = taille
    while t > 10:
        f = ImageFont.truetype(chemin, t)
        if d.textlength(texte, font=f) <= largeur:
            return f
        t -= 2
    return ImageFont.truetype(chemin, 10)

# --- QR, rendu a l'echelle exacte : un module = un nombre entier de pixels
code.save(SORTIE + 'qr-diapo.png', scale=15, border=4, dark='#000000', light='#ffffff')
qr = Image.open(SORTIE + 'qr-diapo.png').convert('RGB')
T = qr.size[0]
cx, cy = L - T - 190, (H - T) // 2
d.rounded_rectangle([cx - 34, cy - 34, cx + T + 34, cy + T + 34], radius=26, fill=(246, 245, 249))
dia.paste(qr, (cx, cy))

# --- biscuit, compose comme sur la page : anneau cacao et creme pleine
V = 150
bis = Image.open(os.path.join(ICI, 'biscuit.png')).convert('RGBA').resize((V, V))
S = V * 384 / 396
R = 0.655 * S / 2
vign = Image.new('RGBA', (V, V), (0, 0, 0, 0))
couche = Image.open(os.path.join(ICI, 'creme.png')).convert('RGB').resize((V, V)).convert('RGBA')
masque = Image.new('L', (V, V), 0)
ImageDraw.Draw(masque).ellipse([S/2 - R, S/2 - R, S/2 + R, S/2 + R], fill=255)
couche.putalpha(masque)
vign.paste(couche, (0, 0), couche)
omb = Image.open(os.path.join(ICI, 'ombre-puits.png')).convert('RGBA').resize((int(2*R), int(2*R)))
vign.paste(omb, (int(S/2 - R), int(S/2 - R)), omb)
vign.paste(bis, (0, 0), bis)
dia.paste(vign, (150, 196), vign)

MARGE = cx - 100 - 150          # largeur utile a gauche du QR

d.text((150, 384), "ICN BUSINESS SCHOOL  ·  PPDE3017", font=ImageFont.truetype(SANSB, 28), fill=VIOLET)
f1 = tenir("Sondage en direct", SANSB, 92, MARGE)
f2 = tenir("Mondelēz International", SANSB, 92, MARGE)
d.text((150, 436), "Sondage en direct", font=f1, fill=ENCRE)
d.text((150, 540), "Mondelēz International", font=f2, fill=ENCRE)

d.rounded_rectangle([150, 684, 150 + MARGE, 824], radius=18, fill=(246, 245, 249))
d.text((186, 706), "Scannez le QR code", font=ImageFont.truetype(SANSB, 46), fill=ENCRE)
d.text((186, 766), "et répondez sur votre téléphone", font=ImageFont.truetype(SANS, 36), fill=DOUX)

d.text((150, 880), "Groupe 1 — Tamara, Juliane, Ilian, Yago", font=ImageFont.truetype(SANS, 32), fill=DOUX)
d.rectangle([150, 944, L - 150, 946], fill=FILET)
d.text((150, 968), URL, font=ImageFont.truetype(SANS, 28), fill=VIOLET)

dia.save(SORTIE + 'diapo-qr.png', optimize=True)
os.remove(SORTIE + 'qr-diapo.png')

print("adresse encodée :", URL)
print("version du QR   :", code.version, "· correction", code.error, "·", len(code.matrix), "modules")
for f in ('qr-sondage.png', 'qr-sondage.svg', 'qr-sondage-violet.png', 'diapo-qr.png'):
    print(f"  {f:24s} {os.path.getsize(SORTIE + f) // 1024:4d} ko")
