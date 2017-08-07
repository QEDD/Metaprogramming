import tkinter as tk
from time import time as tm
import threading as th
from functools import wraps as wr
from functools import partial
import os
import logging as lg
# ==============================================================================
# Metapg


def decorator(funct):
    """ Param funct: function to be weapped."""

    # print(os.environ)
    '''
    if "DEBUG" not in os.environ:
        print("HEY")
        return funct
    '''

    log = lg.getLogger(funct.__module__)
    msg = funct.__qualname__

    @wr(funct)
    def wapper(*args, **kwargs):
        print("----", funct.__name__, msg)
        log.debug(msg)
        return funct(*args, **kwargs)
    return wapper


def debug(ms=""):
    def decor(funct):
        msg = ms + funct.__qualname__

        def wapper(*args, **kwargs):
            print("----", funct.__name__, msg)
            return funct(*args, **kwargs)
        return wapper
    return decor


def debug2(funct=None, *, prefix=""):
    if funct is None:
        return partial(debug2, prefix=prefix)

    msg = prefix + funct.__qualname__

    @wr(funct)
    def wrapper(*args, **kwargs):
        print("----", funct.__name__, msg)
        return funct(*args, **kwargs)
    return wrapper
# ==============================================================================


def classDecorator(cls):
    for key, val in vars(cls).items():
        if callable(val):                       # if val is callable
            setattr(cls, key, decorator(val))   # set attrs of the class
    return cls


class MetaClass(type):
    """docstring for MetaClass."""

    def __new__(cls, clsName, bases, clsDict):
        if len(bases) > 1:
            raise TypeError("NO inheritance from more than one class")
        clsObj = super(MetaClass, cls).__new__(cls, clsName, bases, clsDict)
        clsObj = classDecorator(clsObj)
        return clsObj


class Spam(metaclass=MetaClass):
    """docstring for Spam."""

    def __init__(self, arg):
        super(Spam, self).__init__()
        self.arg = arg

    def HI(self, arg):
        print("<function method Spam.HI>")


# @classDecorator it fails because it has an inner class :)
# The staticmethods won't be wrapped
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

    # @debug2("2+2+2+2")
    @debug("+++")
    @decorator
    def numericalIntegral(self, dwLimit, upLimit, funct):
        width = (upLimit - dwLimit) / 100000
        return round(sum(list(map(lambda x: width * funct(dwLimit + x * width), range(100000)))), ndigits=5)


# ==============================================================================


class PhysicalObject(object):
    """docstring for PhysicalObject."""
    _args = ["master", "floor", "scale"]

    def __init__(self, master, floor=None, scale=5):
        super(PhysicalObject, self).__init__()
        for name, val in zip(self.__class__._args):
            setattr(self, name, val)
        self.shape = None
        if floor is None:
            self.floor = int(self.master["height"])
        self.math = Math()
        self.mouse = False

    def analizer(self, arg):
        pass
        # return self.mouse, vector

    def gravity(self):                          # threading while true if not()
        def sumInHeight(coords, sumation):
            nwCoords = []
            for i in range(0, len(coords)):
                co = coords[i]
                if i % 2 == 1:
                    co += sumation
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
            tiempo = (tm() - temp) ** (self.scale)
            dist = self.math.cm2pix(gravit * tiempo * self.scale)
            self.master.coords(self.shape, *sumInHeight(coords, dist))
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
        self.shape = self.master.create_rectangle(x, y, x + width, y + height, fill=color)
        self.master.create_line(x, y, x + width, y, fill="green")


# ==============================================================================
# MAIN
# ==============================================================================
if __name__ == '__main__':
    '''
    window = tk.Tk()
    canvas = tk.Canvas(window, width=1000, height=500, bg="gray20")
    canvas.pack()
    for i in range(5):
        sq = Square(canvas, x=100 * i)
        # hilo = th.Thread(target=sq.gravity, daemon=True)
        # hilo.start()
        print(sq.gravity())
    tk.mainloop()
    # hilo.stop()
    '''
    m = Math()
    vector1 = m.vector(1, 2, 3)
    vector2 = m.vector(2, 2, 2)
    vector3 = m.vector(1, 1, 1)
    print(vector1 + vector2 + vector3)

    def f(x): return x**2
    print("derivative", m.numericalDerivative(f, 1))
    print("integral", m.numericalIntegral(dwLimit=0, upLimit=1, funct=f))
