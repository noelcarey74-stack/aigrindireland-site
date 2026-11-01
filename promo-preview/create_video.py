from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import math
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'promo-preview'
OUT.mkdir(exist_ok=True)
NAVY=(8,38,91); BLUE=(16,74,154); GOLD=(255,203,44); CREAM=(243,249,255); SOFT=(194,218,247)
FONT='/System/Library/Fonts/Supplemental/Arial.ttf'
BOLD='/System/Library/Fonts/Supplemental/Arial Bold.ttf'
def f(n,b=False):return ImageFont.truetype(BOLD if b else FONT,n)
def rr(base,image,rect,r=21):
    x,y,w,h=rect
    img=image.resize((w,h),Image.Resampling.LANCZOS).convert('RGBA')
    m=Image.new('L',(w,h));ImageDraw.Draw(m).rounded_rectangle((0,0,w-1,h-1),radius=r,fill=255)
    sh=Image.new('RGBA',(w+44,h+44));sd=ImageDraw.Draw(sh);sd.rounded_rectangle((22,22,22+w,22+h),radius=r,fill=(0,5,25,170));sh=sh.filter(ImageFilter.GaussianBlur(13))
    base.paste(sh,(x-22,y-17),sh)
    base.paste(img,(x,y),m)
def wordwrap(d,text,font,limit):
    words=text.split();ls=[];line=''
    for w in words:
        s=(line+' '+w).strip()
        if d.textbbox((0,0),s,font=font)[2] <= limit:line=s
        else:ls.append(line);line=w
    if line:ls.append(line)
    return ls
def background():
    im=Image.new('RGB',(1280,720))
    px=im.load()
    for y in range(720):
        for x in range(1280):
            a=y/720;b=x/1280;t=.42*a+.26*b
            px[x,y]=tuple(int(NAVY[i]*(1-t)+BLUE[i]*t) for i in range(3))
    return im
def screen(im,name):
    a=Image.open(ROOT/'assets'/name).convert('RGB')
    if name=='home.webp':
        # Public marketing: remove the real account holder's name from the app screenshot.
        d=ImageDraw.Draw(a);d.rectangle((170,272,408,334),fill=(13,64,139))
        d.text((179,280),'Hi Student',font=f(36,True),fill='white')
    if name=='grind.webp':
        # Replace personalised first name with anonymous illustrative learner text.
        d=ImageDraw.Draw(a)
        d.rounded_rectangle((137,73,466,125),radius=7,fill=(245,247,252))
        d.text((147,81),'Reading Skills Grind',font=f(25,True),fill=(16,35,64))
        d.rounded_rectangle((26,166,574,320),radius=24,fill=(228,243,253),outline=(211,229,245),width=2)
        d.text((60,199),'Practise reading and making',font=f(20),fill=(99,111,131))
        d.text((60,229),'inferences using evidence',font=f(20),fill=(99,111,131))
        d.text((60,259),'from the text.',font=f(20),fill=(99,111,131))
    h=545;w=int(a.width/a.height*h);x=1002-w//2;y=84
    d=ImageDraw.Draw(im)
    d.rounded_rectangle((x-13,y-13,x+w+13,y+h+13),radius=34,fill=(6,20,44),outline=(102,156,219),width=3)
    rr(im,a,(x,y,w,h),22)
    d.rounded_rectangle((x+w//2-34,y+6,x+w//2+34,y+15),radius=6,fill=(2,15,38))
def make_frame(n,title,subtitle,pic):
    im=background();d=ImageDraw.Draw(im)
    d.ellipse((835,-245,1505,430),outline=(24,96,189),width=37)
    d.ellipse((-190,510,235,935),outline=(26,104,205),width=32)
    d.rounded_rectangle((50,30,1230,692),radius=32,outline=(63,135,222),width=2)
    ic=Image.open(ROOT/'assets/app-icon.webp').convert('RGB')
    rr(im,ic,(73,59,69,69),16)
    d.text((166,83),'AI GRIND IRELAND',font=f(25,True),fill=GOLD)
    d.text((82,198),'STUDY SMARTER',font=f(21,True),fill=GOLD)
    y=255
    for ln in wordwrap(d,title,f(57,True),645):
        d.text((78,y),ln,font=f(57,True),fill=CREAM);y+=69
    y+=12
    for ln in wordwrap(d,subtitle,f(27),615):
        d.text((82,y),ln,font=f(27),fill=SOFT);y+=37
    if pic: screen(im,pic)
    else:
        rr(im,ic,(885,230,210,210),41)
        d.rounded_rectangle((828,500,1160,563),radius=23,fill=GOLD)
        d.text((850,516),'Download on the App Store',font=f(22,True),fill=NAVY)
    d.line((79,641,1200,641),fill=(64,131,205),width=2)
    d.text((82,655),'Junior Cycle  •  Leaving Cert',font=f(19,True),fill=GOLD)
    d.text((1070,655),f'AGI  {n:02d}',font=f(19,True),fill=SOFT)
    im.save(OUT/f'frame_{n:02}.png',optimize=True)
scenes=[
 ('Your personal AI tutor','Junior Cycle and Leaving Cert, at your level.','welcome.webp'),
 ('Your year. Your subjects.','Personalised study help built around you.','home.webp'),
 ('Start a Grind','Learn with clear, step-by-step support.','grind.webp'),
 ('Ask AGI','Get unstuck with explanations that make sense.','home.webp'),
 ('Exam-style practice','Original questions and useful feedback.','home.webp'),
 ('See your progress','Know what to revise next.','progress.webp'),
 ('Official sources','Curriculum-aware learning and trusted links.','sources.webp'),
 ('Small steps. Big progress.','AI Grind Ireland. Learn at your own pace.',None)
]
for i,(a,b,c) in enumerate(scenes,1):make_frame(i,a,b,c)
print('Created 8 scene frames in',OUT)
