from display import *
from matrix import *


def add_circle(matrix, cx, cy, cz, r):
  t = 0
  while t <= 1:
    x = r * math.cos(2*math.pi * t) + cx
    y = r * math.sin(2*math.pi * t) + cy
    z = cz
    add_point(matrix, x, y, z)
    if t != 0: add_point(matrix, x, y, z)
    t += TSTEP
  add_point(matrix, r + cx, cy, cz)

def add_polygon( points, x0, y0, z0, x1, y1, z1, x2, y2, z2 ):
    add_point(points, x0, y0, z0)
    add_point(points, x1, y1, z1)
    add_point(points, x2, y2, z2)

def draw_polygons( matrix, screen, color ):
    if len(matrix) < 3:
        print("Need at least 3 points")
    point = 0
    while point < len(matrix)-1:
        p0 = matrix[point]
        p1 = matrix[point+1]
        p2 = matrix[point+2]

        A = [(p1[0] - p0[0]), (p1[1] - p0[1]), (p1[2] - p0[2])]
        B = [(p2[0] - p0[0]), (p2[1] - p0[1]), (p2[2] - p0[2])]

        N = cross_product(A, B)

        if N[2] > 0:
            draw_line( int(p0[0]),
                       int(p0[1]),
                       int(p1[0]),
                       int(p1[1]),
                       screen, color)
            draw_line( int(p1[0]),
                       int(p1[1]),
                       int(p2[0]),
                       int(p2[1]),
                       screen, color)
            draw_line( int(p2[0]),
                       int(p2[1]),
                       int(p0[0]),
                       int(p0[1]),
                       screen, color)
        point+= 3


def add_box( polygons, x, y, z, width, height, depth ):
    x1 = x + width
    y1 = y - height
    z1 = z - depth

    #front
    add_edge(polygons, x, y, z, x1, y, z)
    add_edge(polygons, x, y1, z, x1, y1, z)
    add_edge(polygons, x1, y, z, x1, y1, z)
    add_edge(polygons, x, y, z, x, y1, z)

    #back
    add_edge(polygons, x, y, z1, x1, y, z1)
    add_edge(polygons, x, y1, z1, x1, y1, z1)
    add_edge(polygons, x1, y, z1, x1, y1, z1)
    add_edge(polygons, x, y, z1, x, y1, z1)

    #sides
    add_edge(polygons, x, y, z, x, y, z1)
    add_edge(polygons, x1, y, z, x1, y, z1)
    add_edge(polygons, x, y1, z, x, y1, z1)
    add_edge(polygons, x1, y1, z, x1, y1, z1)

def add_sphere(polygons, cx, cy, cz, r, steps ):
    points = generate_sphere(cx, cy, cz, r, steps)

    lat_start = 0
    lat_stop = steps
    longt_start = 0
    longt_stop = steps

    steps += 1
    i = 0
    while i < len(points) - 1:
        add_polygon(polygons,
        int(points[i][0]), int(points[i][1]), int(points[i][2]),
        int(points[i + 1][0]), int(points[i + 1][1]), int(points[i + 1][2]),
        int(points[(i + 1+steps) % len(points)][0]), int(points[(i + 1+steps) % len(points)][1]), int(points[(i + 1+steps)  % len(points)][2])
        )

        if i % steps != 0 and i % steps != steps - 1:
            add_polygon(polygons,
            int(points[i][0]), int(points[i][1]), int(points[i][2]),
            int(points[(i + 1 + steps) % len(points)][0]), int(points[(i + 1 + steps)  % len(points)][1]), int(points[(i + 1 + steps)  % len(points)][2]),
            int(points[(i + steps) % len(points)][0]), int(points[(i + steps) % len(points)][1]), int(points[(i + steps) % len(points)][2])
            )
        i += 1

def generate_sphere( cx, cy, cz, r, steps ):
    points = []

    rot_start = 0
    rot_stop = steps
    circ_start = 0
    circ_stop = steps

    for rotation in range(rot_start, rot_stop):
        rot = rotation/float(steps)
        for circle in range(circ_start, circ_stop+1):
            circ = circle/float(steps)

            x = r * math.cos(math.pi * circ) + cx
            y = r * math.sin(math.pi * circ) * math.cos(2*math.pi * rot) + cy
            z = r * math.sin(math.pi * circ) * math.sin(2*math.pi * rot) + cz

            points.append([x, y, z])
            #print 'rotation: %d\tcircle%d'%(rotation, circle)
    return points


def add_torus( edges, cx, cy, cz, r0, r1, step ):
    points = generate_torus(cx, cy, cz, r0, r1, step)

    lat_start = 0
    lat_stop = step
    longt_start = 0
    longt_stop = step

    for lat in range(lat_start, lat_stop):
        for longt in range(longt_start, longt_stop):
            curr = (lat*step) + longt
            if lat == lat_stop - 1:
                next = longt
            else:
                next = curr + step
            if not longt == longt_stop - 1:
                add_polygon(edges, points[curr][0], points[curr][1], points[curr][2], points[next][0], points[next][1], points[next][2], points[next+1][0], points[next+1][1], points[next+1][2])
                add_polygon(edges, points[next+1][0], points[next+1][1], points[next+1][2], points[curr + 1][0], points[curr + 1][1], points[curr + 1][2], points[curr][0], points[curr][1], points[curr][2])
            else:
                if lat == lat_stop - 1:
                    extreme = 0
                else:
                    extreme = curr + step - longt
                add_polygon(edges, points[curr][0], points[curr][1], points[curr][2], points[next][0], points[next][1], points[next][2], points[extreme][0], points[extreme][1], points[extreme][2])
                add_polygon(edges, points[extreme][0], points[extreme][1], points[extreme][2], points[curr - longt][0], points[curr - longt][1], points[curr - longt][2], points[curr][0], points[curr][1], points[curr][2])

def generate_torus( cx, cy, cz, r0, r1, step ):
    points = []
    rot_start = 0
    rot_stop = step
    circ_start = 0
    circ_stop = step

    for rotation in range(rot_start, rot_stop):
        rot = rotation/float(step)
        for circle in range(circ_start, circ_stop):
            circ = circle/float(step)

            x = math.cos(2*math.pi * rot) * (r0 * math.cos(2*math.pi * circ) + r1) + cx;
            y = r0 * math.sin(2*math.pi * circ) + cy;
            z = -1*math.sin(2*math.pi * rot) * (r0 * math.cos(2*math.pi * circ) + r1) + cz;

            points.append([x, y, z])
    return points

def add_sector(matrix, cx, cy, cz, r, theta_i, theta_f):
    theta_i *= math.pi / 180
    theta_f *= math.pi / 180
    t = theta_i / (2*math.pi)
    while t <= theta_f / (2*math.pi):
        x = r * math.cos(2*math.pi * t) + cx
        y = r * math.sin(2*math.pi * t) + cy
        z = cz
        add_point(matrix, x, y, z)
        if t != 0: add_point(matrix, x, y, z)
        t += TSTEP
    add_edge(matrix, cx, cy, cz, cx + r*math.cos(theta_i), cy + r*math.sin(theta_i), cz)
    add_edge(matrix, cx, cy, cz, cx + r*math.cos(theta_f), cy + r*math.sin(theta_f), cz)

def add_bezier(matrix, x0, y0, x1, y1, x2, y2, x3, y3):
  ax = (3 * x1 + x3 - x0 - 3 * x2)
  bx = (3 * x0 + 3 * x2 - 6 * x1)
  cx = (3 * x1 - 3 * x0)
  dx = x0
  ay = (3 * y1 + y3 - y0 - 3 * y2)
  by = (3 * y0 + 3 * y2 - 6 * y1)
  cy = (3 * y1 - 3 * y0)
  dy = y0
  t = 0
  while t <= 1:
    x = dx + t * (cx + t * (bx + t * ax))
    y = dy + t * (cy + t * (by + t * ay))
    add_point(matrix, x, y)
    if t != 0 and t < 1: add_point(matrix, x, y)
    t += TSTEP
  del matrix[-1]

def add_hermite(matrix, x0, y0, x1, y1, rx0, ry0, rx1, ry1):
  ax = (2 * x0 + rx0 + rx1 - 2 * x1)
  bx = (3 * x1 - 3 * x0 - 2 * rx0 - rx1)
  cx = rx0
  dx = x0
  ay = (2 * y0 + ry0 + ry1 - 2 * y1)
  by = (3 * y1 - 3 * y0 - 2 * ry0 - ry1)
  cy = ry0
  dy = y0
  t = 0
  while t <= 1:
    x = dx + t * (cx + t * (bx + t * ax))
    y = dy + t * (cy + t * (by + t * ay))
    add_point(matrix, x, y)
    if t != 0 and t < 1: add_point(matrix, x, y)
    t += TSTEP
  del matrix[-1]


def draw_lines( matrix, screen, color ):
    if len(matrix) < 2:
        print('Need at least 2 points to draw')
        return

    point = 0
    while point < len(matrix) - 1:
        draw_line( int(matrix[point][0]),
                   int(matrix[point][1]),
                   int(matrix[point+1][0]),
                   int(matrix[point+1][1]),
                   screen, color)    
        point+= 2
        
def add_edge( matrix, x0, y0, z0, x1, y1, z1 ):
    add_point(matrix, x0, y0, z0)
    add_point(matrix, x1, y1, z1)
    
def add_point( matrix, x, y, z=0 ):
    matrix.append( [x, y, z, 1] )


def draw_line( x0, y0, x1, y1, screen, color ):
    #swap points if going right -> left
    if x0 > x1:
        xt = x0
        yt = y0
        x0 = x1
        y0 = y1
        x1 = xt
        y1 = yt

    x = x0
    y = y0
    A = 2 * (y1 - y0)
    B = -2 * (x1 - x0)

    #octants 1 and 8
    if ( abs(x1-x0) >= abs(y1 - y0) ):

        #octant 1
        if A > 0:            
            d = A + B/2

            while x < x1:
                plot(screen, color, x, y)
                if d > 0:
                    y+= 1
                    d+= B
                x+= 1
                d+= A
            #end octant 1 while
            plot(screen, color, x1, y1)
        #end octant 1

        #octant 8
        else:
            d = A - B/2

            while x < x1:
                plot(screen, color, x, y)
                if d < 0:
                    y-= 1
                    d-= B
                x+= 1
                d+= A
            #end octant 8 while
            plot(screen, color, x1, y1)
        #end octant 8
    #end octants 1 and 8

    #octants 2 and 7
    else:
        #octant 2
        if A > 0:
            d = A/2 + B

            while y < y1:
                plot(screen, color, x, y)
                if d < 0:
                    x+= 1
                    d+= A
                y+= 1
                d+= B
            #end octant 2 while
            plot(screen, color, x1, y1)
        #end octant 2

        #octant 7
        else:
            d = A/2 - B;

            while y > y1:
                plot(screen, color, x, y)
                if d > 0:
                    x+= 1
                    d+= A
                y-= 1
                d-= B
            #end octant 7 while
            plot(screen, color, x1, y1)
        #end octant 7
    #end octants 2 and 7
#end draw_line