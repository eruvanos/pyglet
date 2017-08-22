import os
import pyglet
from pyglet.gl import *


# pyglet.options['debug_gl_shaders'] = True

window = pyglet.window.Window(width=540, height=540, resizable=True)
print("OpenGL Context: {}".format(window.context.get_info().version))

##########################################################
#   TESTS !
##########################################################
# TODO: update text module to fix this:
# label = pyglet.text.Label("test label")


# vertex_list = pyglet.graphics.vertex_list(3, ('v3f', (-0.6, -0.5, 0,  0.6, -0.5, 0,  0, 0.5, 0)),
#                                              ('c3f', (1, 0, 1, 0, 1, 1, 0, 1, 0)))

batch = pyglet.graphics.Batch()


def create_quad_vertex_list(x, y, z, width, height):
    return x, y, z, x + width, y, z, x + width, y + height, z, x, y + height, z


batch.add_indexed(4, GL_TRIANGLES, None, [0, 1, 2, 0, 2, 3],
                  ('v3f', create_quad_vertex_list(200, 200, 0, 55, 55)),
                  ('c3f', (1, 0.5, 0.2, 1, 0.5, 0.2, 1, 0.5, 0.2, 1, 0.5, 0.2)))

batch.add_indexed(4, GL_TRIANGLES, None, [0, 1, 2, 0, 2, 3],
                  ('v2f', (400, 400, 400+50, 400, 400+50, 400+50, 400, 400+50)),
                  ('c3f', (1, 0.5, 0.2, 1, 0.5, 0.2, 1, 0.5, 0.2, 1, 0.5, 0.2)))


os.chdir('..')
img = pyglet.image.load("examples/pyglet.png")
# img = pyglet.image.load_animation("test.gif")
img.anchor_x = img.width // 2
img.anchor_y = img.height // 2
red = pyglet.image.SolidColorImagePattern((255, 0, 0, 255)).create_image(50, 50)
green = pyglet.image.SolidColorImagePattern((0, 255, 0, 255)).create_image(50, 50)
blue = pyglet.image.SolidColorImagePattern((0, 0, 255, 255)).create_image(50, 50)
white = pyglet.image.SolidColorImagePattern((255, 255, 255, 255)).create_image(50, 50)

sprites = [
    pyglet.sprite.Sprite(img=img, x=60, y=80, batch=batch),
    pyglet.sprite.Sprite(img=img, x=110, y=90, batch=batch),
    pyglet.sprite.Sprite(img=img, x=160, y=100, batch=batch),
    pyglet.sprite.Sprite(img=img, x=210, y=110, batch=batch),
]

sprite2 = pyglet.sprite.Sprite(img=red, x=200, y=100, batch=batch)
sprite3 = pyglet.sprite.Sprite(img=green, x=300, y=200, batch=batch)
sprite4 = pyglet.sprite.Sprite(img=blue, x=400, y=300, batch=batch)
sprite5 = pyglet.sprite.Sprite(img=white, x=500, y=400, batch=batch)


###########################################################
# Set the "zoom" uniform value.
###########################################################
program = pyglet.graphics.default_group.shader_program
program.use_program()
program['window_size'] = window.width, window.height

# print("zoom", program['zoom'])
# print("size", program['window_size'])
# print("texture loc", program['our_texture'])


##########################################################
# Modify the "zoom" Uniform value scrolling the mouse
##########################################################
@window.event
def on_mouse_scroll(x, y, mouse, direction):
    if not program.active:
        program.use_program()
    program['zoom'] += direction / 32
    if program['zoom'] < 0.1:
        program['zoom'] = 0.1
    program.stop_program()


###########################################################
#
###########################################################
@window.event
def on_draw():
    window.clear()
    # pyglet.graphics.draw(3, GL_TRIANGLES, ('v3f', (-0.6, -0.5, 0,  0.6, -0.5, 0,  0, 0.5, 0)),
    #                                       ('c3f', (1, 0.5, 0.2,  1, 0.5, 0.2,  1, 0.5, 0.2)))
    # TODO: fix drawing vertex_lists
    # vertex_list.draw(GL_TRIANGLES)

    # pyglet.graphics.draw_indexed(4, GL_TRIANGLES, [0, 1, 2, 0, 2, 3],
    #                              ('v2i', (-1, -1,   1, -1,   1, 1,   -1, 1)),
    #                              ('c3f', (1, 0.5, 0.2,  1, 0.5, 0.2,  1, 0.5, 0.2, 1, 0.5, 0.2)))

    # glActiveTexture(GL_TEXTURE0)
    # glBindTexture(img.texture.target, img.texture.id)

    batch.draw()

    # for c in batch._draw_list:
    #     print(c)
    #
    # print(len(batch._draw_list))


def update(dt):
    for sprite in sprites:
        sprite.rotation += 100 * dt % 360


if __name__ == "__main__":
    pyglet.gl.glClearColor(0.2, 0.3, 0.3, 1)
    pyglet.clock.schedule_interval(update, 1/60)
    pyglet.app.run()
