from  math import sqrt,trunc
import pyglet
import numpy as np
from pyglet.gl import *
import triomino

class State(object):
    def __init__(self, ):
        self.focus = ((0,0),(0,1),(1,0))
        self.offset = (0,0)
        self.direction = (0,0)

state = State()
game = triomino.Game([triomino.Player()])

def move_up(point):
    return (point[0]+1,point[1])
def move_down(point):
    return (point[0]-1,point[1])
def move_left(point):
    return (point[0],point[1])

def point_to_triangle(point):
    x = trunc(point[0])
    if point[0] < 0:
      x -= 1
    y = trunc(point[1])
    if point[1] < 0:
        y -= 1
    converted_point = np.array(point_to_position(point),dtype = "f")
    points = [(x,y),(x+1,y),(x,y+1),(x+1,y+1)]
    converted_points = [np.array(point_to_position(p),dtype = "f") for p in points]
    distance1 = np.sum(-(converted_points[0]) + converted_point) ** 2
    distance2 = np.sum(-converted_point + converted_points[-1]) ** 2
    if distance1 > distance2:
        return tuple(points[1:])
    else:
        return tuple([points[0],points[2],points[1]])
    
def flatten(iterable):
  it = iter(iterable)
  for e in it:
    if isinstance(e, (list, tuple)):
      for f in flatten(e):
        yield f
    else:
      yield e

def position_to_point(p):
    #p[0]/sqrt(0.75)
    x = p[0]/sqrt(0.75)
    y = p[1]-x*0.5
    return (x,y)

def point_to_pos(point):
    con_point = (point[0]*sqrt(0.75),point[0]*0.5+point[1])
    return con_point

def point_to_position(point):
    con_point = (point[0]*sqrt(0.75),point[0]*0.5+point[1])
    return (window.width/2+con_point[0]*100,window.height/2+con_point[1]*100)

# class Triangle:
#     def __init__(self,points):
#         self.points = points
#     def contains(point):

if __name__ == "__main__":
    values = {(0,0):1,(0,1):2,(1,0):3,(1,-1):4}
    positions = {((0,0),(1,0),(0,1)):True,
                 ((0,0),(1,-1),(1,0)):True
                 }
    
    #,((0,0),(0,1),(-1,0)):Truel
    window = pyglet.window.Window()
    def value_label(v,p): 
        return pyglet.text.Label(str(v),
                                 font_name='Times New Roman',
                                 font_size=14,
                                 x=p[0], y=p[1],
                                 #color=(0,0,0,0),
                                 color=(1, 255, 1, 255),
                                 anchor_x='center', anchor_y='center')
    
    @window.event
    def on_key_press(symbol,modifiers):
        if symbol == pyglet.window.key.TAB:
            game.player().next()
        elif symbol == pyglet.window.key.SPACE:
            game.player().rotate()

    #onclick try to set stone if not settable rotate focus by one
    @window.event
    def on_mouse_press(x, y, button, modifiers):
        prev_focus = state.focus
        middle = (window.width/2,window.height/2)
        position = ((-middle[0]+x-state.offset[0])/100.0,(-middle[1]+y-state.offset[1])/100.0) #TODO offset beruecksichtigen
        point = position_to_point(position)
        triangle = point_to_triangle(point)
        game.move(triangle)
        state.focus = list(triangle)
        if state.focus == prev_focus:
            game.player().rotate()
        #focus[0].sort()

    @window.event
    def on_mouse_motion(x,y,dx,dy):
        dir = (0,0)
        if (x > window.width-20):
            dir = (dir[0]+1,dir[1])
        if x < 20:
            dir = (dir[0]-1,dir[1])
        if y > window.height-20: 
            dir = (dir[0],dir[1]+1)
        if y < 20:
            dir = (dir[0],dir[1]-1)
        state.direction = dir
    
    @window.event
    def on_draw():
        state.offset = (state.offset[0] + state.direction[0],state.offset[1] + state.direction[1])
        window.clear()
        pyglet.gl.glPushMatrix()
        pyglet.gl.glTranslatef(state.offset[0],state.offset[1],0)
        for triangle in game.positionfield:
            pos = [ point_to_position(point) for point in triangle]
            pyglet.graphics.draw(3, pyglet.gl.GL_TRIANGLES,
                                 ('v2f', tuple(flatten(pos))))
            for point in triangle:
                con_point = (point[0]*sqrt(0.75),point[0]*0.5+point[1])
                position = (window.width/2+con_point[0]*100,window.height/2+con_point[1]*100)
                value_label(game.valuefield[point],position).draw()
        pyglet.graphics.draw(3, pyglet.gl.GL_TRIANGLES,
                             ('v2f',tuple(flatten([point_to_position(p) for p in state.focus]))),
                             ('c3B',(0,0,255,0,0,255,255,0,0)))
        for i,point in enumerate(state.focus):
            con_point = (point[0]*sqrt(0.75),point[0]*0.5+point[1])
            position = (window.width/2+con_point[0]*100,window.height/2+con_point[1]*100)
            value_label(game.player().stone()[i],position).draw()
        pyglet.text.Label(str(game.player().stone()),
                          font_name='Times New Roman',
                          font_size=14,
                          x=40, y=40,
                          color=(1, 255, 1, 255),
                          anchor_x='center', anchor_y='center').draw()
        pyglet.text.Label(str(state.offset),
                          font_name='Times New Roman',
                          font_size=14,
                          x=200, y=40,
                          color=(1, 255, 1, 255),
                          anchor_x='center', anchor_y='center').draw()
        pyglet.gl.glPopMatrix()

    pyglet.app.run()



    run()
