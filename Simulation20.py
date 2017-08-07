import tkinter as tk
from time import time as tm
import threading as th
# ==============================================================================
"""
DERIVATIVE RULES

    u+v	du/dx+dv/dx
    u-v	du/dx-dv/dx
    u/v	(v*du/dx-u*dv/dx)/v^2
    u*v	u*dv/dx+v*du/dx
    c*u	c*du/dx	c is constant
    u^v	v*u^(v-1)*du/dx+u^v*ln(u)*dv/dx
    u^n	n*u^(n-1)*du/dx	n is real
    c^u	c^u*ln(c)*du/dx	c is constant
    e^u	e^u*du/dx	e = 2.7182818284590452353602874713527
1	sin(u)	cos(u)*du/dx
2	cos(u)	-sin(u)*du/dx
3	tan(u)	sec(u)^2*du/dx
4	sec(u)	sec(u)*tan(u)*du/dx
5	cosec(u)	-cosec(u)*cot(u)*du/dx
6	cot(u)	-cosec(u)^2*du/dx
7	sinh(u)	cosh(u)*du/dx
8	cosh(u)	sinh(u)*du/dx
9	tanh(u)	sech(u)^2*du/dx
10	sech(u)	sech(u)*tanh(u)*du/dx
11	cosech(u)	cosech(u)*coth(u)*du/dx
12	coth(u)	-cosech(u)^2*du/dx
13	asin(u)	1/sqrt(1-u^2)*du/dx
14	acos(u)	-1/sqrt(1-u^2)*du/dx
15	atan(u)	1/(1+u^2)*du/dx
16	asec(u)	1/(|u|*sqrt(u^2-1))*du/dx	|u| is abs(u)
17	acosec(u)	-1/(|u|*sqrt(u^2-1))*du/dx	|u| is abs(u)
18	acot(u)	-1/(1+u^2)*du/dx
19	asinh(u)	1/sqrt(u^2+1)*du/dx
20	acosh(u)	1/sqrt(u^2-1)*du/dx
21	atanh(u)	1/(1-u^2)*du/dx
22	asech(u)	-1/(u*sqrt(1-u^2))*du/dx
23	acosech(u)	-1/(u*sqrt(1+u^2))*du/dx
24	acoth(u)	1/(1-u^2)*du/dx
25	sqrt(u)	1/(2*sqrt(u))*du/dx
26	log10(u)	1/(u*ln(10))*du/dx
27	log(u)	1/u*du/dx
28	ln(u)	1/u*du/dx
29	sign(u)	0
30	abs(u)	u/|u|*du/dx	|u| is abs(u)
"""


class Math(object):
    """docstring for Math."""

    def __init__(self):
        super(Math, self).__init__()
        self.h = 10**-10

    class vector(object):
        """docstring for vector."""

        def __init__(self, x, y, z=0):
            super(Math.vector, self).__init__()
            self.x = x
            self.y = y
            self.z = z
            self.vec = (self.x, self.y, self.z)

        def __repr__(self):
            return "<{0}, {1}, {2}>".format(*self.vec)

        def __add__(self, other):
            return Math.vector(*(x + y for x, y in zip(self.vec, other.vec)))

    def pix2cm(self, pix):                  # Conversion from pixels to centimeters
        return pix * 0.026458333

    def cm2pix(self, cm):                   # Conversion from centimeters to pixels
        return cm * 37.795275591

    def numericalDerivative(self, funct, num):
        return round((funct(num + self.h) - funct(num)) / self.h, ndigits=5)

    def numericalIntegral(self, dwLimit, upLimit, funct):
        width = (upLimit - dwLimit) / 100000
        return round(sum(list(map(lambda x: width * funct(dwLimit + x * width), range(100000)))), ndigits=5)


# ==============================================================================


class PhysicalObject(object):
    """docstring for PhysicalObject."""

    def __init__(self, master, floor=None, scale=5):
        super(PhysicalObject, self).__init__()
        self.master = master
        self.shape = None
        self.floor = floor
        self.scale = scale                      # each 1m ==> 5cm
        if floor is None:
            self.floor = int(self.master["height"])
        self.math = Math()
        self.mouse = False

    def analizer(self, arg):
        pass
        # return self.mouse,

    def gravity(self):                          # threading while true if not()
        parab = 10
        up = 10

        def sumInHeight(coords, sumation, parab, up):
            nwCoords = []
            for i in range(0, len(coords)):
                co = coords[i]
                if i % 2 == 1:
                    co += sumation - up
                else:
                    co += parab
                nwCoords.append(co)
            return list(nwCoords)

        def heightCoords(coords):
            height = []
            for i in range(1, len(coords), 2):
                height.append(coords[i])
            return tuple(height)
        temp = tm()
        coords = self.master.coords(self.shape)
        nwCoords = coords
        height = heightCoords(coords)
        initHeight = self.math.pix2cm((max(height) + min(height)) / 2)
        gravit = 9.8

        while nwCoords[1] < self.floor and nwCoords[3] < self.floor:
            parab += 5
            up += 6
            tiempo = (tm() - temp) ** (self.scale)
            dist = self.math.cm2pix(gravit * tiempo * self.scale)
            self.master.coords(self.shape, *sumInHeight(coords, dist, parab, up))
            self.master.update()
            self.master.after(5)
            nwCoords = self.master.coords(self.shape)

        height = heightCoords(nwCoords)
        finalHeight = self.math.pix2cm((max(height) + min(height)) / 2)

        return {"time": round(tiempo, ndigits=2),
                "height": finalHeight - initHeight}


# ==============================================================================


class Square(PhysicalObject):
    """docstring for Square."""

    def __init__(self, master=None, x=100, y=100, width=50, height=50, color="white", **kwargs):
        super(Square, self).__init__(master=master, **kwargs)
        self.master = master
        self.shape = self.master.create_oval(x, y, x + width, y + height, fill=color)
        self.master.create_line(x, y, x + width, y, fill="green")


# ==============================================================================
# MAIN
# ==============================================================================
if __name__ == '__main__':
    window = tk.Tk()
    canvas = tk.Canvas(window, width=1000, height=500, bg="gray20")
    canvas.pack()
    # for i in range(5):
    sq = Square(canvas, x=100, y=430)
    """
    hilo1 = th.Thread(target=sq.gravity)
    hilo1.start()
    sq2 = Square(canvas, x=100)
    hilo2 = th.Thread(target=sq2.gravity)
    hilo2.start()
    sq3 = Square(canvas, x=200)
    hilo3 = th.Thread(target=sq3.gravity)
    hilo3.start()
    window.bind("<Escape>", quit)
    """
    print(sq.gravity())
    tk.mainloop()
    """
    hilo1.stop()
    hilo2.stop()
    hilo3.stop()
    """
    '''
    m = Math()
    vector1 = m.vector(1, 2, 3)
    vector2 = m.vector(2, 2, 2)
    vector3 = m.vector(1, 1, 1)
    print(vector1 + vector2 + vector3)

    def f(x): return x**2
    print("derivative", m.numericalDerivative(f, 1))
    print("integral", m.numericalIntegral(dwLimit=0, upLimit=1, funct=f))
    '''
