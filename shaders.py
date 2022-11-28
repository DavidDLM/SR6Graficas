# Mario de Leon 19019
# Graficos por computadora basado en lo escrito por Ing. Dennis Aldana / Ing. Carlos Alonso

import matMath as mt
from textures import Texture


def gourad(render, **kwargs):
    # Normal calculada por vertice
    u, v, w = kwargs["baryCoords"]
    b, g, r = kwargs["vColor"]
    tA, tB, tC = kwargs["texCoords"]
    nA, nB, nC = kwargs["normals"]

    b /= 255
    g /= 255
    r /= 255

    if render.active_texture:
        # P = Au + Bv + Cw
        tU = tA[0] * u + tB[0] * v + tC[0] * w
        tV = tA[1] * u + tB[1] * v + tC[1] * w

        texColor = render.active_texture.getColor(tU, tV)

        b *= texColor[2]
        g *= texColor[1]
        r *= texColor[0]

    triangleNormal = [nA[0] * u + nB[0] * v + nC[0] * w,
                      nA[1] * u + nB[1] * v + nC[1] * w,
                      nA[2] * u + nB[2] * v + nC[2] * w]

    dirLight = render.dirLight
    intensity = mt.dotMatrix(
        triangleNormal, [-dirLight.x, -dirLight.y, -dirLight.z])

    b *= intensity
    g *= intensity
    r *= intensity

    if intensity > 0:
        return r, g, b
    else:
        return 0, 0, 0


def toon(render, **kwargs):

    u, v, w = kwargs["baryCoords"]
    b, g, r = kwargs["vColor"]
    tA, tB, tC = kwargs["texCoords"]
    nA, nB, nC = kwargs["normals"]

    b /= 255
    g /= 255
    r /= 255

    if render.active_texture:
        # P = Au + Bv + Cw
        tU = tA[0] * u + tB[0] * v + tC[0] * w
        tV = tA[1] * u + tB[1] * v + tC[1] * w

        texColor = render.active_texture.getColor(tU, tV)

        b *= texColor[2]
        g *= texColor[1]
        r *= texColor[0]

    triangleNormal = [nA[0] * u + nB[0] * v + nC[0] * w,
                      nA[1] * u + nB[1] * v + nC[1] * w,
                      nA[2] * u + nB[2] * v + nC[2] * w]

    dirLight = render.dirLight
    intensity = mt.dotMatrix(
        triangleNormal, [-dirLight.x, -dirLight.y, -dirLight.z])

    if intensity < 0.2:
        intensity = 0.1
    elif intensity < 0.5:
        intensity = 0.4
    elif intensity < 0.8:
        intensity = 0.7
    elif intensity <= 1:
        intensity = 1

    b *= intensity
    g *= intensity
    r *= intensity

    if intensity > 0:
        return r, g, b
    else:
        return 0, 0, 0


def glow(render, **kwargs):

    u, v, w = kwargs["baryCoords"]
    b, g, r = kwargs["vColor"]
    tA, tB, tC = kwargs["texCoords"]
    nA, nB, nC = kwargs["normals"]

    b /= 255
    g /= 255
    r /= 255

    if render.active_texture:
        # P = Au + Bv + Cw
        tU = tA[0] * u + tB[0] * v + tC[0] * w
        tV = tA[1] * u + tB[1] * v + tC[1] * w

        texColor = render.active_texture.getColor(tU, tV)

        b *= texColor[2]
        g *= texColor[1]
        r *= texColor[0]

    triangleNormal = [nA[0] * u + nB[0] * v + nC[0] * w,
                      nA[1] * u + nB[1] * v + nC[1] * w,
                      nA[2] * u + nB[2] * v + nC[2] * w]

    dirLight = render.dirLight
    intensity = mt.dotMatrix(
        triangleNormal, [-dirLight.x, -dirLight.y, -dirLight.z])

    b *= intensity
    g *= intensity
    r *= intensity

    camForward = (render.camMatrix[0][2],
                  render.camMatrix[1][2],
                  render.camMatrix[2][2])

    glowAmount = 1 - mt.dotMatrix(triangleNormal, camForward)

    if glowAmount <= 0:
        glowAmount = 0

    yellow = (1, 1, 0)

    b += yellow[2] * glowAmount
    g += yellow[1] * glowAmount
    r += yellow[0] * glowAmount

    if b > 1:
        b = 1
    if g > 1:
        g = 1
    if r > 1:
        r = 1

    if intensity > 0:
        return r, g, b
    else:
        return 0, 0, 0


def greyScale(render, **kwargs):

    u, v, w = kwargs["baryCoords"]
    b, g, r = kwargs["vColor"]
    tA, tB, tC = kwargs["texCoords"]
    nA, nB, nC = kwargs["normals"]

    b /= 255
    g /= 255
    r /= 255

    if render.active_texture:
        # P = Au + Bv + Cw
        tU = tA[0] * u + tB[0] * v + tC[0] * w
        tV = tA[1] * u + tB[1] * v + tC[1] * w

        texColor = render.active_texture.getColor(tU, tV)

        b *= texColor[2]
        g *= texColor[1]
        r *= texColor[0]

    triangleNormal = [nA[0] * u + nB[0] * v + nC[0] * w,
                      nA[1] * u + nB[1] * v + nC[1] * w,
                      nA[2] * u + nB[2] * v + nC[2] * w]

    dirLight = render.dirLight
    intensity = mt.dotMatrix(
        triangleNormal, [-dirLight.x, -dirLight.y, -dirLight.z])

    r *= intensity
    b *= intensity
    g *= intensity

    if intensity > 0:
        return r, g, b
    else:
        return 0, 0, 0
