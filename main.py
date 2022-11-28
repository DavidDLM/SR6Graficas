from gl import Renderer, _color_, V2, V3
from textures import Texture
from obj import Obj

from shaders import gourad, toon, glow, greyScale

#################################

width = 1300
height = 866
depth = -10
black = _color_(0, 0, 0)
white = _color_(1, 1, 1)

rend = Renderer(width, height)

#################################

# Posiciones
SCALE = V3(0.07, 0.07, 0.07)
TRANSLATE = V3(0, -4, -10)
TRANSLATE2 = V3(0, -12, -10)
TRANSLATE3 = V3(1, -14, -10)
ROTATE = V3(0, 0, 0)  # La rotacion se va a hacer con las camaras
ROTATE2 = V3(0, 0, -20)

# Capta al cello desde la mitad, dejando que se vea el fondo
MEDIUM_SHOT = V3(2, 1, -1)
# Capta al cello desde un leve angulo por debajo
LOW_SHOT = V3(2, -1, 0.8)
# Capta al cello desde un leve angulo por arriba
HIGH_SHOT = V3(1, 8, 1)
# Capta al cello desde un angulo inclinado
DUTCH_SHOT = V3(1, 8, -2)

#################################

# Para ver los angulos solo hay que descomentarlos
# Para ver HIGH_SHOT, modificar TRANSLATE en glLoadModel a TRANSLATE2
# Para ver DUTCH_SHOT, modificar TRANSLATE a TRANSLATE3 y ROTATE a ROTATE2

rend.glLookAt(V3(1, 0.5, -5), MEDIUM_SHOT)  # Medium Shot (eye, camPosition)
# rend.glLookAt(V3(1, 0.5, -5), LOW_SHOT)  # Low Shot (eye, camPosition)
# rend.glLookAt(V3(1, 0.5, -5), HIGH_SHOT)  # High Shot (eye, camPosition)
# rend.glLookAt(V3(1, 0.5, -5), DUTCH_SHOT)  # Dutch Shot (eye, camPosition)
#################################

rend.active_shader = toon
rend.active_texture = Texture("models/CelloTX.bmp")
rend.glLoadModel("models/Cello.obj",
                 translate=TRANSLATE,  # USAR TRANSLATE2 PARA HIGH_SHOT Y TRANSLATE 3 PARA DUTCH_SHOT
                 scale=SCALE,
                 rotate=ROTATE)    # USAR ROTATE2 PARA DUTCH_SHOT

#################################


rend.write("dutchShot.bmp")
