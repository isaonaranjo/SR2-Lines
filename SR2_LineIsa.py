# Maria Isabel Ortiz Naranjo
# Graficas por computadora
# 18176

# Basado en codigo proporcionado en clase por Dennis

# Ejercicio no. 2 - agregar funcion glLine

import struct

def char(c):
    return struct.pack('=c', c.encode('ascii'))

def word(c):
    return struct.pack('=h', c)

def dword(c):
    return struct.pack('=l', c)

def color(r, g, b):
    return bytes([b, g, r])

class Render(object):
    def __init__(self):
        self.framebuffer = []

    def point(self, x, y):
        self.framebuffer[y][x] = self.color

    # función glInit() 
    def glInit(self):
        pass

    # función glCreateWindow(width, height) 
    def glCreateWindow(self, width, height):
        self.width = width
        self.height = height

    # función glViewPort(x, y, width, height)
    def glViewport(self, x, y, width, height):
        self.xViewPort = x
        self.yViewPort = y
        self.viewPortWidth = width
        self.viewPortHeight = height

    # función glClear() 
    def glClear(self):
        self.framebuffer = [
            [color(1, 1, 1) for x in range(self.width)]
            for y in range(self.height)
        ]

    # funcion glLine
    def glLine(self, x0, y0, x1, y1):
        x0 = int(round((x0+1) * self.width / 2))
        y0 = int(round((y0+1) * self.height / 2))
        x1 = int(round((x1+1) * self.width / 2))
        y1 = int(round((y1+1) * self.height / 2))

        dy = abs(y1 - y0)
        dx = abs(x1 - x0)
        steep = dy > dx
        if steep:
            x0, y0 = y0, x0
            x1, y1 = y1, x1

        if x0 > x1:
            x0, x1 = x1, x0
            y0, y1 = y1, y0
        dy = abs(y1 - y0)
        dx = abs(x1 - x0)
        offset = 0 
        threshold =  dx
        y = y0
        inc = 1 if y1 > y0 else -1
        for x in range(x0, x1):
            if steep:
                self.point(y, x)
            else:
                self.point(x, y)

            offset += 2 * dy
            if offset >= threshold:
                y += inc
                threshold += 2 * dx
    
    def glClearColor(self, r=1, g=1, b=1):
        r = round(r*255)
        g = round(g*255)
        b = round(b*255)

        self.framebuffer = [
            [color(r, g, b) for x in range(self.width)]
            for y in range(self.height)
        ]

    def glColor(self, r=0.5, g=0.5, b=0.5):
        r = round(r*255)
        g = round(g*255)
        b = round(b*255)
        self.color = color(r, g, b)

    def glVertex(self, x, y):
        X = round((x+1)*(self.viewPortWidth/2)+self.xViewPort)
        Y = round((y+1)*(self.viewPortHeight/2)+self.yViewPort)
        self.point(X, Y)

    def glFinish(self, filename):
        f = open(filename, 'bw')
        f.write(char('B'))
        f.write(char('M'))
        f.write(dword(14 + 40 + self.width * self.height * 3))
        f.write(dword(0))
        f.write(dword(14 + 40))

        f.write(dword(40))
        f.write(dword(self.width))
        f.write(dword(self.height))
        f.write(word(1))
        f.write(word(24))
        f.write(dword(0))
        f.write(dword(self.width * self.height * 3))
        f.write(dword(0))
        f.write(dword(0))
        f.write(dword(0))
        f.write(dword(0))

        for x in range(self.width):
            for y in range(self.height):
                f.write(self.framebuffer[y][x])

        f.close()

bitmap = Render()

# Lineas 
bitmap.glCreateWindow(100, 100)
bitmap.glClearColor(0.33, 0.33, 0.33)
bitmap.glViewport(10, 10, 50, 50)
bitmap.glColor(0.35, 0, 0)
bitmap.glVertex(-1, -1)
bitmap.glLine(0,0,1,1)
bitmap.glFinish("lineaIsa.bmp")
