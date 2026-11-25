import base64, os

import os
D = os.path.join(os.path.dirname(os.path.abspath(__file__)), '')

src=open(D+'modele.html',encoding='utf-8').read()
for marque,fichier in (('@@PAPIER@@','papier.png'),('@@CREME@@','creme.png'),
                       ('@@PUITS@@','puits.png'),('@@OMBRE@@','ombre-puits.png'),
                       ('@@BISCUIT@@','biscuit.png')):
    b=base64.b64encode(open(D+fichier,'rb').read()).decode('ascii')
    src=src.replace(marque,'data:image/png;base64,'+b)
assert '@@' not in src, 'marqueur non remplace'
cible='/home/user/Estebancv/sondage-site/index.html'
open(cible,'w',encoding='utf-8').write(src)
print('index.html', os.path.getsize(cible), 'octets')
