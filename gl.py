# Proyecto 1
# Mario de Leon 19019
# Graficos por computadora basado en lo escrito por Ing. Dennis Aldana / Ing. Carlos Alonso
import conversions as conv
import random
import struct
from collections import namedtuple
import matMath as mt
from obj import Obj
from math import cos, sin, tan, pi

V2 = namedtuple('Point2', ['x', 'y'])
V3 = namedtuple('Point3', ['x', 'y', 'z'])
V4 = namedtuple('Point4', ['x', 'y', 'z', 'w'])


def char(c):
    # 1 byte
    return struct.pack('=c', c.encode('ascii'))


def word(w):
    # 2 bytes
    return struct.pack('=h', w)


def dword(d):
    # 4 bytes
    return struct.pack('=l', d)


def _color_(r, g, b):
    return bytes([int(b*255),
                  int(g*255),
                  int(r*255)])


# Colores default
white = _color_(1, 1, 1)
black = _color_(0, 0, 0)


def baryCoords(A, B, C, P):

    areaPBC = (B.y - C.y) * (P.x - C.x) + (C.x - B.x) * (P.y - C.y)
    areaPAC = (C.y - A.y) * (P.x - C.x) + (A.x - C.x) * (P.y - C.y)
    areaABC = (B.y - C.y) * (A.x - C.x) + (C.x - B.x) * (A.y - C.y)

    try:
        # PBC / ABC
        u = areaPBC / areaABC
        # PAC / ABC
        v = areaPAC / areaABC
        # 1 - u - v
        w = 1 - u - v
    except:
        return -1, -1, -1
    else:
        return u, v, w


class Renderer(object):
    def __init__(this, width, height):
        this.width = width
        this.height = height
        this.clearColor = black
        this.currColor = white
        this.active_shader = None
        this.active_texture = None
        this.active_texture2 = None
        this.normal_map = None
        this.background = None
        this.dirLight = V3(0, 0, -1)
        this.glViewMatrix()
        this.glViewPort(0, 0, this.width, this.height)
        this.glClear()

    # El area donde se v1 a dibujar
    def glCreateWindow(this, width, height):
        this.width = width
        this.height = height
        this.glClear()

    # Utiliza las coordenadas
    def glViewPort(this, x, y, width, height):
        this.viewportX = x
        this.viewportY = y
        this.viewportWidth = width
        this.viewportHeight = height
        this.viewportMatrix = [[width/2, 0, 0, x+width/2],
                               [0, height/2, 0, y+height/2],
                               [0, 0, 0.5, 0.5],
                               [0, 0, 0, 1]]

        this.glProjectionMatrix()

    # View Matrix
    def glViewMatrix(this, translate=V3(0, 0, 0), rotate=V3(0, 0, 0)):
        this.camMatrix = this.glCreateObjectMatrix(translate, rotate)
        this.viewMatrix = mt.inverseMatrix(this.camMatrix)

    # LookAt
    def glLookAt(this, eye, camPosition=V3(0, 0, 0)):
        forward = mt.subtractVectors(
            [camPosition.x, camPosition.y, camPosition.z], [eye.x, eye.y, eye.z])
        forward[:] = [f / mt.normMatrix(forward) for f in forward]

        right = mt.crossProductMatrix(V3(0, 1, 0), forward)
        right[:] = [r / mt.normMatrix(right) for r in right]

        up = mt.crossProductMatrix(forward, right)
        up[:] = [u / mt.normMatrix(up) for u in up]

        this.camMatrix = [[right[0], up[0], forward[0], camPosition[0]],
                          [right[1], up[1], forward[1], camPosition[1]],
                          [right[2], up[2], forward[2], camPosition[2]],
                          [0, 0, 0, 1]]

        this.viewMatrix = mt.inverseMatrix(this.camMatrix)

    # Projection Matrix
    def glProjectionMatrix(this, n=0.1, f=1000, fov=60):
        aspectRatio = this.viewportWidth / this.viewportHeight
        t = tan((fov * pi / 180) / 2) * n
        r = t * aspectRatio

        this.projectionMatrix = ([[n/r, 0, 0, 0],
                                  [0, n/t, 0, 0],
                                  [0, 0, -(f+n)/(f-n), -(2*f*n)/(f-n)],
                                  [0, 0, -1, 0]])

    # Limpia los pixeles de la pantalla poniendolos en blanco o negro
    def glClear(this):
        this.framebuffer = [[this.clearColor for y in range(this.height)]
                            for x in range(this.width)]
        this.buffer = [[float('inf') for y in range(this.height)]
                       for x in range(this.width)]

    # Limpia el fondo
    def glClearBackground(this):
        if this.background:
            for x in range(this.viewportX, this.viewportX + this.viewportWidth + 1):
                for y in range(this.viewportY, this.viewportY + this.viewportHeight + 1):

                    tU = (x - this.viewportX) / this.viewportWidth
                    tV = (y - this.viewportY) / this.viewportHeight

                    texColor = this.background.getColor(tU, tV)

                    if texColor:
                        this.glPoint(x, y, _color_(
                            texColor[0], texColor[1], texColor[2]))

    # Coloca color de fondo
    def glClearColor(this, r, g, b):
        this.clearColor = _color_(r, g, b)

    # Dibuja un punto
    def glVertex(this, vertexX, vertexY, color=None):
        x = int((vertexX+1)*(this.viewportWidth/2)+this.viewportX)
        y = int((vertexY+1)*(this.viewportHeight/2)+this.viewportY)
        this.glPoint(x, y, color)

    def glPoint(this, x, y, color=None):
        # Coordenadas de la ventana
        if (0 <= x < this.width) and (0 <= y < this.height):
            this.framebuffer[x][y] = color or this.currColor

    # Se establece el color de dibujo, si no tiene nada se dibuja blanco
    def glColor(this, r, g, b):
        this.currColor = _color_(r, g, b)

    def glClearViewPort(this, color=None):
        for x in range(this.viewportX, this.viewportX + this.viewportWidth):
            for y in range(this.viewportY, this.viewportY + this.viewportHeight):
                this.glVertex(x, y, color)

    # Algoritmo de Bresenham para creación de lineas
    def glLine(this, v1, v2, color=None):
        # Bresenham line algorithm
        # y = m * x + b
        x1 = int(v1.x)
        x2 = int(v2.x)
        y1 = int(v1.y)
        y2 = int(v2.y)

        # Si el punto0 es igual al punto 1, dibujar solamente un punto
        if x1 == x2 and y1 == y2:
            this.glPoint(x1, y1, color)
            return

        dy = abs(y2 - y1)
        dx = abs(x2 - x1)

        steep = dy > dx

        # Si la linea tiene pendiente mayor a 1 o menor a -1
        # intercambio las x por las y, y se dibuja la linea
        # de manera vertical
        if steep:
            x1, y1 = y1, x1
            x2, y2 = y2, x2

        # Si el punto inicial X es mayor que el punto final X,
        # intercambio los puntos para siempre dibujar de
        # izquierda a derecha
        if x1 > x2:
            x1, x2 = x2, x1
            y1, y2 = y2, y1

        dy = abs(y2 - y1)
        dx = abs(x2 - x1)

        offset = 0
        limit = 0.5
        m = dy / dx
        y = y1

        for x in range(x1, x2 + 1):
            if steep:
                # Dibujar de manera vertical
                this.glPoint(y, x, color)
            else:
                # Dibujar de manera horizontal
                this.glPoint(x, y, color)

            offset += m

            if offset >= limit:
                if y1 < y2:
                    y += 1
                else:
                    y -= 1

                limit += 1

    def glCreateRotationMatrix(this, pitch=0, yaw=0, roll=0):

        # https://howthingsfly.si.edu/flight-dynamics/roll-pitch-and-yaw
        # Rotation around the front-to-back axis is called roll.
        # Rotation around the side-to-side axis is called pitch.
        # Rotation around the vertical axis is called yaw.
        pitch *= pi/180
        yaw *= pi/180
        roll *= pi/180

        # Matrices de rotacion proporcionadas por Ing. Dennis Aldana
        rotationX = [[1, 0, 0, 0],
                     [0, cos(pitch), -sin(pitch), 0],
                     [0, sin(pitch), cos(pitch), 0],
                     [0, 0, 0, 1]]

        rotationY = [[cos(yaw), 0, sin(yaw), 0],
                     [0, 1, 0, 0],
                     [-sin(yaw), 0, cos(yaw), 0],
                     [0, 0, 0, 1]]

        rotationZ = [[cos(roll), -sin(roll), 0, 0],
                     [sin(roll), cos(roll), 0, 0],
                     [0, 0, 1, 0],
                     [0, 0, 0, 1]]

        return mt.multMatrix(mt.multMatrix(rotationX, rotationY), rotationZ)

    def glCreateObjectMatrix(this, translate=V3(0, 0, 0), rotate=V3(0, 0, 0), scale=V3(1, 1, 1)):

        translateMatrix = [[1, 0, 0, translate.x],
                           [0, 1, 0, translate.y],
                           [0, 0, 1, translate.z],
                           [0, 0, 0, 1]]

        rotationMatrix = this.glCreateRotationMatrix(
            rotate.x, rotate.y, rotate.z)

        scaleMatrix = [[scale.x, 0, 0, 0],
                       [0, scale.y, 0, 0],
                       [0, 0, scale.z, 0],
                       [0, 0, 0, 1]]

        return mt.multMatrix(mt.multMatrix(translateMatrix, rotationMatrix), scaleMatrix)

    def glTransform(this, vertex, matrix):

        aV = V4(vertex[0], vertex[1], vertex[2], 1)
        transV = mt.vectMultMatrix(matrix, aV)

        transV = V3(transV[0] / transV[3],
                    transV[1] / transV[3],
                    transV[2] / transV[3])

        return transV

    def glDirTransform(this, dirVector, rotMatrix):
        v = V4(dirVector[0], dirVector[1], dirVector[2], 0)
        vt = mt.vectMultMatrix(rotMatrix, v)
        vf = V3(vt[0],
                vt[1],
                vt[2])

        return vf

    def glCamTransform(this, vertex):
        v = V4(vertex[0], vertex[1], vertex[2], 1)

        vt = mt.vectMultMatrix(this.viewportMatrix, mt.vectMultMatrix(
            this.projectionMatrix, mt.vectMultMatrix(this.viewMatrix, v)))
        vf = V3(vt[0] / vt[3],
                vt[1] / vt[3],
                vt[2] / vt[3])

        return vf

    def glLoadModel(this, filename, translate=V3(0, 0, 0), rotate=V3(0, 0, 0), scale=V3(1, 1, 1)):
        model = Obj(filename)
        modelMatrix = this.glCreateObjectMatrix(translate, rotate, scale)
        rotationMatrix = this.glCreateRotationMatrix(
            rotate[0], rotate[1], rotate[2])

        for face in model.faces:
            vertCount = len(face)
            # Relleno con triangulos de colores
            v0 = model.vertices[face[0][0] - 1]
            v1 = model.vertices[face[1][0] - 1]
            v2 = model.vertices[face[2][0] - 1]

            v0 = this.glTransform(v0, modelMatrix)
            v1 = this.glTransform(v1, modelMatrix)
            v2 = this.glTransform(v2, modelMatrix)

            A = this.glCamTransform(v0)
            B = this.glCamTransform(v1)
            C = this.glCamTransform(v2)

            vt0 = model.texcoords[face[0][1] - 1]
            vt1 = model.texcoords[face[1][1] - 1]
            vt2 = model.texcoords[face[2][1] - 1]

            vn0 = model.normals[face[0][2] - 1]
            vn1 = model.normals[face[1][2] - 1]
            vn2 = model.normals[face[2][2] - 1]
            vn0 = this.glDirTransform(vn0, rotationMatrix)
            vn1 = this.glDirTransform(vn1, rotationMatrix)
            vn2 = this.glDirTransform(vn2, rotationMatrix)

            this.glTriangle_bc(A, B, C,
                               verts=(v0, v1, v2),
                               texCoords=(vt0, vt1, vt2),
                               normals=(vn0, vn1, vn2))
            if vertCount == 4:
                v3 = model.vertices[face[3][0] - 1]
                v3 = this.glTransform(v3, modelMatrix)
                D = this.glCamTransform(v3)
                vt3 = model.texcoords[face[3][1] - 1]
                vn3 = model.normals[face[3][2] - 1]
                vn3 = this.glDirTransform(vn3, rotationMatrix)

                this.glTriangle_bc(A, C, D,
                                   verts=(v0, v2, v3),
                                   texCoords=(vt0, vt2, vt3),
                                   normals=(vn0, vn2, vn3))

    def glTriangle_standard(this, A, B, C, color=None):
        # Para asegurarnos que estamos trabajando con el orden correcto de los vertices
        if A.y < B.y:
            A, B = B, A
        if A.y < C.y:
            A, C = C, A
        if B.y < C.y:
            B, C = C, B

        def flatBottomTriangle(v1, v2, v3):
            try:
                m21 = (v2.x - v1.x) / (v2.y - v1.y)
                m31 = (v3.x - v1.x) / (v3.y - v1.y)
            except:
                pass
            else:
                x1 = v2.x
                x2 = v3.x
                for y in range(int(v2.y), int(v1.y)):
                    this.glLine(V2(int(x1), y), V2(int(x2), y), color)
                    x1 += m21
                    x2 += m31

        def flatTopTriangle(v1, v2, v3):
            try:
                m31 = (v3.x - v1.x) / (v3.y - v1.y)
                m32 = (v3.x - v2.x) / (v3.y - v2.y)
            except:
                pass
            else:
                x1 = v1.x
                x2 = v2.x

                for y in range(int(v1.y), int(v3.y), -1):
                    this.glLine(V2(int(x1), y), V2(int(x2), y), color)
                    x1 -= m31
                    x2 -= m32

        if B.y == C.y:
            # Parte plana abajo
            flatBottomTriangle(A, B, C)
        elif A.y == B.y:
            # Parte plana arriba
            flatTopTriangle(A, B, C)
        else:
            # Dibujo ambos tipos de triangulos
            # Teorema de intercepto
            D = V2(A.x + ((B.y - A.y) / (C.y - A.y)) * (C.x - A.x), B.y)
            flatBottomTriangle(A, B, D)
            flatTopTriangle(B, D, C)

    def glTriangle_bc(this, A, B, C, verts=(), texCoords=(), normals=(), color=None):
        # bounding box
        minX = round(min(A.x, B.x, C.x))
        minY = round(min(A.y, B.y, C.y))
        maxX = round(max(A.x, B.x, C.x))
        maxY = round(max(A.y, B.y, C.y))

        triangleNormal = mt.crossProductMatrix(mt.subtractVectors([verts[1].x, verts[1].y, verts[1].z], [
                                               verts[0].x, verts[0].y, verts[0].z]), mt.subtractVectors([verts[2].x, verts[2].y, verts[2].z], [verts[0].x, verts[0].y, verts[0].z]))
        # normalizar
        # triangleNormal[:] = [x / ml.norm(triangleNormal) for x in triangleNormal]

        for x in range(minX, maxX + 1):
            for y in range(minY, maxY + 1):
                u, v, w = baryCoords(A, B, C, V2(x, y))

                if 0 <= u and 0 <= v and 0 <= w:

                    z = A.z * u + B.z * v + C.z * w

                    if 0 <= x < this.width and 0 <= y < this.height:
                        if z < this.buffer[x][y] and -1 <= z <= 1:
                            this.buffer[x][y] = z

                            if this.active_shader:
                                r, g, b = this.active_shader(this,
                                                             baryCoords=(
                                                                 u, v, w),
                                                             vColor=color or this.currColor,
                                                             texCoords=texCoords,
                                                             normals=normals,
                                                             triangleNormal=triangleNormal)

                                this.glPoint(x, y, _color_(r, g, b))
                            else:
                                this.glPoint(x, y, color)

    # Crea un archivo BMP

    def write(this, filename):
        with open(filename, "bw") as file:
            # pixel header
            file.write(bytes('B'.encode('ascii')))
            file.write(bytes('M'.encode('ascii')))
            file.write(dword(14 + 40 + this.width * this.height * 3))
            file.write(word(0))
            file.write(word(0))
            file.write(dword(14 + 40))

            # informacion del header
            file.write(dword(40))
            file.write(dword(this.width))
            file.write(dword(this.height))
            file.write(word(1))
            file.write(word(24))
            file.write(dword(0))
            file.write(dword(this.width * this.height * 3))
            file.write(dword(0))
            file.write(dword(0))
            file.write(dword(0))
            file.write(dword(0))

            # pixel data
            for y in range(this.height):
                for x in range(this.width):
                    file.write(this.framebuffer[x][y])
