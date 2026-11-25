import segno, os
from PIL import Image, ImageDraw, ImageFont

import os
_ici = os.path.dirname(os.path.abspath(__file__))
D = os.path.join(_ici, '')                       # textures sources
SORTIE = os.path.join(os.path.dirname(_ici), 'qr', '')   # QR et diapo
os.makedirs(SORTIE, exist_ok=True)

URL = "https://yagoaba2006-byte.github.io/sondage-mondelez/"
CHOCOLAT=(74,44,29); CREME=(251,243,228); CARAMEL=(217,154,62); ROSE=(228,99,127)
SERIF='/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf'
SANS ='/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'
SANSB='/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'

q = segno.make(URL, error='q')
q.save(SORTIE+'qr-sondage.png', scale=22, border=4, dark='#000000', light='#ffffff')
q.save(SORTIE+'qr-sondage.svg', scale=12, border=4, dark='#000000', light='#ffffff')

W,H = 1920,1080
dia = Image.new('RGB',(W,H),CREME)
pap = Image.open(D+'papier.png').convert('RGB')
for i in range(0,W,192):
    for j in range(0,H,192): dia.paste(pap,(i,j))
d = ImageDraw.Draw(dia)

def tenir(texte, chemin, taille_max, largeur_max):
    """Reduit la police jusqu'a ce que le texte tienne."""
    t = taille_max
    while t > 10:
        f = ImageFont.truetype(chemin, t)
        if d.textlength(texte, font=f) <= largeur_max:
            return f
        t -= 2
    return ImageFont.truetype(chemin, 10)

# --- QR sur carton blanc, ombre decalee nette ---
# rendu a l'echelle exacte : chaque module fait un nombre entier de
# pixels, aucun redimensionnement ne vient deformer la trame
q.save(SORTIE+'qr-diapo.png', scale=12, border=4, dark='#000000', light='#ffffff')
qr = Image.open(SORTIE+'qr-diapo.png').convert('RGB')
T = qr.size[0]
cx, cy = 1255, 245
BORD = 22
d.rectangle([cx-BORD+20, cy-BORD+20, cx+T+BORD+20, cy+T+BORD+20], fill=CHOCOLAT)
d.rectangle([cx-BORD, cy-BORD, cx+T+BORD, cy+T+BORD], fill=(255,255,255))
dia.paste(qr,(cx,cy))
print('QR :', T, 'px de cote, module entier')

# --- biscuit : anneau cacao + creme pleine, comme sur la page ---
V = 170
bis = Image.open(D+'biscuit.png').convert('RGBA').resize((V,V))
S = V*384/396
R = 0.655*S/2
vign = Image.new('RGBA',(V,V),(0,0,0,0))
couche = Image.open(D+'creme.png').convert('RGB').resize((V,V)).convert('RGBA')
m = Image.new('L',(V,V),0)
ImageDraw.Draw(m).ellipse([S/2-R, S/2-R, S/2+R, S/2+R], fill=255)
couche.putalpha(m); vign.paste(couche,(0,0),couche)
omb = Image.open(D+'ombre-puits.png').convert('RGBA').resize((int(2*R),int(2*R)))
vign.paste(omb,(int(S/2-R),int(S/2-R)),omb)
vign.paste(bis,(0,0),bis)
dia.paste(vign,(150,130),vign)

MARGE = 1150 - 150          # largeur utile a gauche du QR
d.text((150, 338), "ICN BUSINESS SCHOOL  ·  PPDE3017", font=ImageFont.truetype(SANSB,30), fill=CHOCOLAT)
f1 = tenir("Sondage en direct", SERIF, 84, MARGE)
f2 = tenir("Mondelēz International", SERIF, 84, MARGE)
d.text((150, 398), "Sondage en direct", font=f1, fill=CHOCOLAT)
d.text((150, 498), "Mondelēz International", font=f2, fill=CHOCOLAT)

d.rectangle([150, 648, 162, 768], fill=ROSE)
d.text((195, 646), "Scannez le QR code", font=tenir("Scannez le QR code", SANSB, 52, MARGE-60), fill=CHOCOLAT)
d.text((195, 714), "et votez sur votre téléphone", font=tenir("et votez sur votre téléphone", SANS, 44, MARGE-60), fill=CHOCOLAT)

d.text((150, 848), "Groupe 1 — Tamara, Juliane, Ilian, Yago", font=ImageFont.truetype(SANS,34), fill=CHOCOLAT)
d.rectangle([150, 912, 1770, 918], fill=CHOCOLAT)
d.text((150, 942), URL, font=ImageFont.truetype(SANS,30), fill=CARAMEL)
dia.save(SORTIE+'diapo-qr.png', optimize=True)
print('titre 1 :', f1.size, 'px   titre 2 :', f2.size, 'px')
for f in ('qr-sondage.png','qr-sondage.svg','diapo-qr.png'):
    print(f, os.path.getsize(D+f), 'octets')
