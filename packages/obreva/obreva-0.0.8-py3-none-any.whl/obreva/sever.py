import turtle as tr
import os
from cmath import *
from PIL import Image
import numpy as np
import scipy.special as spa
def ip(x):
    a=aiff(x)*mandh(x)*iff(x)
    b=sqrt(-x)*tx(x)
    try:c=a**b
    except:c=(a*a)*(b*b)
    return ((a*b)+c)*(x/2)
def aip(x):
    return (ip(x)**2+ip(x))/2
def iph(x):
    return (ip(x)**2)/2
def aiph(x):
    return aip(x)/iph(x)*ip(x)
def aiff(z):
    r, theta = abs(z), phase(z)
    wave = spa.jv(2, r * 4) * exp(1j * (sin(theta * 3) + cos(r * theta * 2)))
    fractal = sum(exp(1j * (z * (0.5 ** n)).real) / (2 ** n) for n in range(1, 10))
    modulation = exp(1j * (sin(z.real * 5) + cos(z.imag * 4))) * fractal
    a=wave * modulation + z * exp(1.5j * sin(z.real * z.imag) * cos(z.real - z.imag))
    b=complex(abs(a),(a**2-a)/a)
    theta=phase(b)
    r=theta
    b=wave * modulation + b * exp(b * sin(z.real * z.imag) * cos(z.real - z.imag))
    return b
def iff(z):
    return 1/aiff(z)
def mand(z):
    c0=z
    c=0
    for i in range(200):
        if abs(c)>1:return complex(0,0)
        c=c**2+c0
    return c*complex(10,10)
def amand(z):
    return 1/mand(z)
def mandh(z):
    return (mand(z)**2+amand(z))/aiff(z)
def amandh(z):
    return sqrt(-(1/mandh(z)*ifi(z)**2))
def aif(z):
    return iff(z)**2
def ifi(z):
    return aif(z)/iff(z)*aiff(z)-phase(z)*abs(z)
def search(l,name):
    ind=0
    for i in l:
        if name==i:return ind
        ind+=1
def draw(name,func,ind=0):
    size = 1000
    scale = 500
    img = Image.new("RGB", (size, size))
    pixels = img.load()
    
    for x in range(size):
        print(x/size*100+ind*100)
        for y in range(size):
            real = (x - scale) / scale
            imag = (y - scale) / scale
            try:
                value = func(complex(real, imag))
                r = max(0, min(255, int((value.real + 1) * 127.5)))
                g = max(0, min(255, int((value.imag + 1) * 127.5)))
                b = max(0, min(255, int((abs(value) + 1) * 127.5)))
                pixels[x, y] = (r, g, b)
            except:
                pixels[x, y] = (0, 0, 0)
    img.save(f'res\\{name}.png')
def normer(x):
    if isinstance(x,complex):return detect(x)*abs(x)
    if isinstance(x,float):return detect(x)*x
    return x
def tx(x):
    """ограничивающая функция для волновых взаимодействий. Максимальное значение x=143, а минимум. Любое положительное число tx(x)->1,а tx(-x)->0"""
    """функция психодела для draw"""
    if x==0:return 1
    return (x**x)**(1/x/x)
def t2x(x):
    """функция искаженного психодела"""
    if x==0:return 1
    return (x**x)**(1/x/x/x)
def qd(x):
    return x**(-x**(1/2))
def aqd(x):return 1/qd(x)
def qdh(x):return qd(x)/aqd(x)
def aqdh(x):
    a=1/qdh(x)
    b=qd(x)
    return a*b
def ion(x):return aiff(x)/key(x)*10
def aion(x):return iff(x)/akey(x)*10
def ionh(x):return aiff(x)*key(x)/10
def aionh(x):return iff(x)*akey(x)/10
def sp(x):return x.real**x.imag
def asp(x):return 1/sp(x)
def sph(x):return sp(x)/asp(x)
def asph(x):
    a=1/sph(x)
    b=sp(x)
    return a*b
def key(x):return qd(x)*sp(x)
def akey(x):return qdh(x)/(1/key(x)*sph(x))
def keyh(x):return (1/aqdh(x)*akey(x))/(key(x)+akey(x))
def akeyh(x):return (1/(akey(x)/keyh(x)))*sp(x)-qd(x)
def sug(x):
    c0=x
    c=0
    for i in range(6):
        if abs(c)>1:return complex(255,255)
        c=c0**2+c
    return c
def asug(x):
    return 1/sug(x)
def sugh(x):
    c0=x
    c=0
    for i in range(6):
        if abs(c)>1:return complex(255,255)
        if abs(c)<-1:return complex(0,0)
        c=sug(c0)**2+c
    return c
def gort(x):
    return x*sugh(x)+asugh(x*2)/akey(x)
def asugh(x):
    c0=x
    c=0
    for i in range(6):
        if abs(c)>1:return complex(255,255)
        if abs(c)<-1:return complex(0,0)
        c=sugh(c0)**3+c
        c0=sug(c)*sp(c)
    return c
def check(x):
    if int(x)==x:return True
    return False
def detect(x):
    if type(x)==complex:return detect(abs(x))
    if type(x)==int:return x
    else:
        i=10
        while not check(x*i):
            i*=10
        return i
def square(x,y):
    a=tr.xcor();b=tr.ycor()
    tr.goto(a+x,b)
    tr.goto(a+x,b+y)
    tr.goto(a,b+y)
    tr.goto(a,b)
def romb(x,y):
    a=tr.xcor();b=tr.ycor()
    tr.goto(a+x,b+y)
    tr.goto(a,b+y*2)
    tr.goto(a-x,b+y)
    tr.goto(a,b)
def sider(size,sides):
    a=tr.xcor();b=tr.ycor()
    for i in range(sides+1):
        tr.right(360/sides)
        tr.forward(size/sides)
def x1d(size,sides,phase=cos):
    """симулирует простые завихрения, используй цикл для полного погружения"""
    a=tr.xcor();b=tr.ycor()
    for i in range(sides+1):
        tr.right(360/sides)
        tr.forward(size/sides*phase(i))
def x2d(size,sides,phase=cos):
    """симулирует кривую дракона, только при условии цикличного использования"""
    a=tr.xcor();b=tr.ycor()
    for i in range(sides+1):        
        tr.right(360/sides*phase(i))
        tr.forward(size/sides*phase(i))
def julia(z):
    """
    Генерирует фрактал Жулиа для комплексного числа z.

    Args:
        z: Комплексное число, представляющее точку на комплексной плоскости.

    Returns:
        Комплексное число, которое при подаче в draw отрисовывает фрактал Жулиа.
        Возвращаемое значение используется для определения цвета пикселя в draw.
    """
    c = complex(-0.4, 0.6)  # Константа для множества Жулиа.  Можно менять для разных форм.
    n = 0
    while abs(z) < 2 and n < 256:  # Максимальное количество итераций
        z = z**2 + c
        n += 1
    return z
def ajulia(z):
    return 1/julia(z)
def juliah(z):
    return julia(z)*ajulia(z)**2
def ajuliah(z):
    return 1/(ajulia(z)*juliah(z))
def geo(x):
    mask=gort(x)
    col=tx(x)
    sask=acosh(x)
    return sask-((abs(mask)+1)*col)
def ageo(x):
    return 1/geo(x)
def geoh(x):
    return ageo(x)**2-gort(x)
def ageoh(x):
    a=ageo(x)*geoh(x)
    b=geoh(x)/ageo(x)
    c=geo(x)/(a+b)
    return c-b+a
def nut(x):
    a=tx(x)
    b=t2x(x)
    c=(a-b)*x
    d=qd(c)-qd(a-b)
    return (a*b)-(b*c)+(c*d)-(d*a)+(b*d)-(a*c)
def anut(x):
    a=t2x(x)
    b=tx(x)
    c=(a+b)/x
    d=aqd(c)+aqd(a+b)
    return (a/b)+(b/c)-(c/d)+(d/a)-(b/d)+(a/c)
def nuth(x):
    a=t2x(x)
    b=tx(x)
    c=(a+b)/x
    d=aqd(c)+aqd(a+b)
    return (a*b)+(b/c)-(c*d)+(d/a)-(b*d)+(a/c)
def anuth(x):
    return 1/nuth(x)*anut(x)
def x3d(size,sides,phase=cos):
    """симулирует куст"""
    iter=-1
    a=tr.xcor();b=tr.ycor()
    for i in range(sides):
        A=tr.xcor();B=tr.ycor()
        for ix in range(sides):
            for Iix in range(iter):
                tr.right(360/sides*phase(ix)*phase(i))
                tr.forward(size/sides*phase(ix)*phase(i)/phase(Iix))
            tr.right(360/sides*phase(ix)*phase(i))
            tr.forward(size/sides*phase(ix)*phase(i))
            tr.penup()
            tr.goto(A,B)
            tr.pendown()
        tr.right(360/sides*phase(i))
        tr.forward(360/sides*phase(i))
matin={
    "tx":tx,"t2x":t2x,"qd":qd,
    "aqd":aqd,"qdh":qdh,"aqdh":aqdh,
    "sp":sp,"asp":asp,"sph":sph,
    "asph":asph,"sug":sug,"asug":asug,
    "sugh":sugh,"asugh":asugh,"key":key,
    "akey":akey,"keyh":keyh,"akeyh":akeyh,
    "sin":sin,"cos":cos,"tan":tan,
    "asin":asin,"acos":acos,"atan":atan,
    "sinh":sinh,"cosh":cosh,"tanh":tanh,
    "asinh":asinh,"acosh":acosh,"atanh":atanh,
    "exp":exp,"sqrt":sqrt,"gort":gort,
    "geo":geo,"ageo":ageo,"geoh":geoh,"ageoh":ageoh,
    "nut":nut,"anut":anut,"nuth":nuth,"anuth":anuth,
    "aiff":aiff,'iff':iff,'aif':aif,"ifi":ifi,
    "ion":ion,'ionh':ionh,'aion':aion,"aionh":aionh,
    'mand':mand,"amand":amand,"mandh":mandh,"amandh":amandh,
    "ip":ip,"aip":aip,"iph":iph,"aiph":aiph,"julia":julia,
    "ajulia":ajulia,"juliah":juliah,"ajuliah":ajuliah}

ind=0
for i in range(len(list(matin.keys()))):
    if not f"{list(matin.keys())[i]}.png" in os.listdir("res"):draw(f"{list(matin.keys())[i]}",list(matin.values())[i],ind);ind+=1
