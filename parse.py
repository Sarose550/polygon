from display import *
from matrix import *
from draw import *

"""
Goes through the file named filename and performs all of the actions listed in that file.
The file follows the following format:
     Every command is a single character that takes up a line
     Any command that requires arguments must have those arguments in the second line.
     The commands are as follows:
   circle: add a circle to the edge matrix - 
           takes 4 arguments (cx, cy, cz, r)
   hermite: add a hermite curve to the edge matrix -
            takes 8 arguments (x0, y0, x1, y1, rx0, ry0, rx1, ry1)
   bezier: add a bezier curve to the edge matrix -
           takes 8 arguments (x0, y0, x1, y1, x2, y2, x3, y3)
         line: add a line to the edge matrix -
               takes 6 arguemnts (x0, y0, z0, x1, y1, z1)
         ident: set the transform matrix to the identity matrix -
         scale: create a scale matrix,
                then multiply the transform matrix by the scale matrix -
                takes 3 arguments (sx, sy, sz)
         move: create a translation matrix,
               then multiply the transform matrix by the translation matrix -
               takes 3 arguments (tx, ty, tz)
         rotate: create a rotation matrix,
                 then multiply the transform matrix by the rotation matrix -
                 takes 2 arguments (axis, theta) axis should be x y or z
         apply: apply the current transformation matrix to the edge matrix
         display: clear the screen, then
                  draw the lines of the edge matrix to the screen
                  display the screen
         save: clear the screen, then
               draw the lines of the edge matrix to the screen
               save the screen to a file -
               takes 1 argument (file name)
         quit: end parsing
See the file script for an example of the file format
"""
ARG_COMMANDS = [ 'line', 'scale', 'move', 'rotate', 'save' ]

def parse_file( fname, edges, transform, screen, color ):
    finput = open(fname, 'r')
    instructions = finput.read().split("\n")
    i = 0
    default_step = 20
    while(i < len(instructions)):
      upshift = 1
      if(instructions[i] == 'ident'):
        ident(transform)
      if(instructions[i] == 'apply'):
        matrix_mult(transform, edges)
      if(instructions[i] == 'display'):
        clear_screen(screen)
        draw_lines(edges, screen, color)
        display(screen)
      if(instructions[i] == "save"):
        clear_screen(screen)
        draw_lines(edges, screen, color)
        display(screen)
        save_extension(screen, instructions[i+1])
        upshift = 2
      if(instructions[i] == "line"):
        newpoints = instructions[i+1].split()
        add_edge(edges, int(newpoints[0]), int(newpoints[1]), int(newpoints[2]), int(newpoints[3]), int(newpoints[4]), int(newpoints[5]))
        upshift = 2
      if(instructions[i] == "scale"):
        newpoints = instructions[i+1].split()
        matrix_mult(make_scale(int(newpoints[0]), int(newpoints[1]), int(newpoints[2])), transform)
        upshift = 2
      if(instructions[i] == "rotate"):
        nextstuff = instructions[i+1].split()
        if(nextstuff[0] == "x"):
          matrix_mult(make_rotX(int(nextstuff[1])), transform)
        if(nextstuff[0] == "y"):
          matrix_mult(make_rotY(int(nextstuff[1])), transform)
        if(nextstuff[0] == "z"):
          matrix_mult(make_rotZ(int(nextstuff[1])), transform)
        upshift = 2
      if(instructions[i] == "move"):
        newpoints = instructions[i+1].split()
        matrix_mult(make_translate(int(newpoints[0]), int(newpoints[1]), int(newpoints[2])), transform)
        upshift = 2
      if instructions[i] == "circle":
        p = [int(y) for y in instructions[i + 1].split(" ")]
        add_circle(edges, p[0], p[1], p[2], p[3])
        upshift = 2
      if instructions[i] == "hermite":
        p = [int(y) for y in instructions[i + 1].split(" ")]
        add_hermite(edges, p[0], p[1], p[2], p[3], p[4], p[5], p[6], p[7])
        upshift = 2
      if instructions[i] == "bezier":
        p = [int(y) for y in instructions[i + 1].split(" ")]
        add_bezier(edges, p[0], p[1], p[2], p[3], p[4], p[5], p[6], p[7])
        upshift = 2
      if instructions[i] == "sector":
        p = [int(y) for y in instructions[i + 1].split(" ")]
        add_sector(edges, p[0], p[1], p[2], p[3], p[4], p[5])
        upshift = 2
      if instructions[i] == "quit":
        break
      if instructions[i] == 'box':
        p = [int(y) for y in instructions[i + 1].split(" ")]
        add_box(edges, p[0], p[1], p[2], p[3], p[4], p[5])
        upshift = 2
      elif instructions[i] == 'sphere':
        p = [int(y) for y in instructions[i + 1].split(" ")]
        add_sphere(edges, p[0], p[1], p[2], p[3], default_step)
        upshift = 2
      elif instructions[i] == 'torus':
        p = [int(y) for y in instructions[i + 1].split(" ")]
        add_torus(edges, p[0], p[1], p[2], p[3], p[4], default_step)
        upshift = 2
      i += upshift