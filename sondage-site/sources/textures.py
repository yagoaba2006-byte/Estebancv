import numpy as np, os
from PIL import Image, ImageFilter

import os
D = os.path.join(os.path.dirname(os.path.abspath(__file__)), '')

RNG = np.random.default_rng(20251125)

def bruit(n, exp=1.9, fmin=2):
    fx=np.fft.fftfreq(n)[:,None]; fy=np.fft.fftfreq(n)[None,:]
    f=np.sqrt(fx**2+fy**2); f[0,0]=1.0
    s=np.where(f*n<fmin,0.0,f**(-exp))
    c=np.fft.ifft2(s*np.exp(1j*RNG.uniform(0,2*np.pi,(n,n)))).real
    c-=c.mean(); m=np.abs(c).max()
    return c/m if m else c

def norm(a):
    a=a-a.min(); return a/a.max() if a.max() else a

def eclairer(h, force=2.4, lx=-0.55, ly=-0.62):
    gy,gx=np.gradient(h*force); nz=np.ones_like(gx)
    n=np.sqrt(gx**2+gy**2+nz**2); lz=np.sqrt(max(1e-6,1-lx*lx-ly*ly))
    return np.clip((-gx*lx-gy*ly+nz*lz)/n,0,None)

def teinter(rgb,l,var=None):
    img=np.array(rgb,float)/255.0*l[...,None]
    if var is not None: img=img+var[...,None]
    return (np.clip(img,0,1)*255).astype(np.uint8)

def lisser(t):
    t=np.clip(t,0,1); return t*t*(3-2*t)

def ecrire_palette(arr, nom, couleurs):
    im=Image.fromarray(arr).convert('P',palette=Image.ADAPTIVE,colors=couleurs)
    im.save(D+nom,optimize=True); return im

# 1 papier ---------------------------------------------------------
N=192
h=0.75*bruit(N,1.35,3)+0.5*bruit(N,2.6,2)
lum=1.0+0.055*h+0.035*bruit(N,0.9,6)
ecrire_palette(teinter((251,243,228),np.clip(lum,0.80,1.06)),'papier.png',32)

# 2 creme ----------------------------------------------------------
N=160
h=0.6*bruit(N,1.1,4)+0.45*bruit(N,2.2,2)+1.1*np.clip(bruit(N,3.0,5),0.25,None)
lum=0.87+0.24*norm(eclairer(h*0.5,force=1.5))
ecrire_palette(teinter((250,240,218),np.clip(lum,0.78,1.05)),'creme.png',48)

# 3 fond du puits --------------------------------------------------
N=128
h=0.7*bruit(N,1.3,4)+0.4*bruit(N,2.5,2)
lum=0.70+0.45*norm(eclairer(h*0.6,force=1.8))
ecrire_palette(teinter((46,26,17),np.clip(lum,0.5,1.15)),'puits.png',24)

# 4 biscuit --------------------------------------------------------
S=384
y,x=np.mgrid[0:S,0:S].astype(float); c=(S-1)/2.0
dx,dy=x-c,y-c; r=np.sqrt(dx*dx+dy*dy)/(S/2.0); th=np.arctan2(dy,dx)
R_EXT,R_INT,DENTS=0.955,0.655,38
bord=R_EXT-0.030*(0.5+0.5*np.cos(DENTS*th))
gb,po=bruit(S,1.25,4),bruit(S,2.4,2)
hauteur=np.clip(lisser((r-(R_INT-0.055))/0.075),0,1)*np.clip(lisser((bord-r)/0.055),0,1)
hauteur=hauteur*(1.0+0.10*gb+0.06*po)+0.055*gb+0.03*po
lum=0.42+0.78*norm(eclairer(hauteur,force=3.1))
lum=lum*(1.0-0.42*np.exp(-((r-R_INT)/0.075)**2))*(1.0-0.14*lisser((r-0.62)/0.34))
biscuit=teinter((82,49,33),np.clip(lum,0.12,1.25),0.030*gb+0.018*po)
AA=3.2/S
alpha=(np.clip((bord-r)/AA,0,1)*np.clip((r-(R_INT-0.012))/AA,0,1)*255).astype(np.uint8)
im=Image.fromarray(np.dstack([biscuit,alpha]),'RGBA')
ombre=Image.new('RGBA',(S,S),(0,0,0,0))
ombre.paste((42,24,16,150),(0,0),Image.fromarray(alpha).filter(ImageFilter.GaussianBlur(0.6)))
plan=Image.new('RGBA',(S+12,S+12),(0,0,0,0))
plan.paste(ombre,(10,10),ombre); plan.paste(im,(0,0),im)
plan.save(D+'biscuit.png',optimize=True)

# 5 ombre d'encastrement : anneau sombre au bord interieur du puits
T=256
y,x=np.mgrid[0:T,0:T].astype(float); c=(T-1)/2.0
dx,dy=x-c,y-c; rr=np.sqrt(dx*dx+dy*dy)/(T/2.0)
a=lisser((rr-0.55)/0.45)**1.35                       # monte vers le bord
a=a*(1.0+0.85*np.clip(-dy/(T/2.0),0,1))              # plus marque en haut
a=np.clip(a,0,1)*(rr<=1.0)
alpha=(a*165).astype(np.uint8)
rgbd=np.zeros((T,T,3),np.uint8); rgbd[...,0]=38; rgbd[...,1]=21; rgbd[...,2]=13
Image.fromarray(np.dstack([rgbd,alpha]),'RGBA').save(D+'ombre-puits.png',optimize=True)

for f in ('papier.png','creme.png','puits.png','biscuit.png','ombre-puits.png'):
    print(f, os.path.getsize(D+f), 'octets', Image.open(D+f).size, Image.open(D+f).mode)
print('total', sum(os.path.getsize(D+f) for f in ('papier.png','creme.png','puits.png','biscuit.png','ombre-puits.png')))
