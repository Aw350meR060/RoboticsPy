import math
from PIL import Image, ImageDraw
import numpy as np
import numpy.random as rand
from scipy.spatial import Delaunay

def distance(ax, ay, bx, by):
    return math.sqrt((by - ay)**2 + (bx - ax)**2)

def rotation(ax, ay, bx, by, angle):
    radius = distance(ax, ay, bx, by)
    angle += math.atan2(ay-by,ax - bx)
    return(
        round(bx + radius * math.cos(angle)),
        round(by + radius * math.sin(angle)),
    )

image = Image.new('RGB',(800, 400), "white")
draw = ImageDraw.Draw(image)

robot_vertices = ((60, 40), (83, 40), (83, 111), (60, 111))
robot_center =  [72, 76]
robot_vertices = [rotation(x, y, robot_center[0], robot_center[1], math.radians(-45)) for x, y in robot_vertices]
draw.polygon(robot_vertices, fill = "red")

wall1_vertices = ((390, 400), (410, 400), (410, 275), (390, 275))
draw.polygon(wall1_vertices, fill = (0, 128, 255))
wall2_vertices = ((390, 0), (410, 0), (410, 125), (390, 125))
draw.polygon(wall2_vertices, fill = (0, 128, 255))

draw.rectangle((105, 155, 255, 305), fill = (0, 128, 255), outline = (0, 128, 255))
draw.rectangle((545, 135, 695, 285), fill = (0, 128, 255), outline = (0, 128, 255))

width, height = image.size
white = (255, 255, 255)
lightblue = (128, 194, 255)
pixel = image.load()
borders = []
red = []


for row in range (width):
    for col in range (height):
        if row == 0 or col == 0 or row == 799 or col == 399:
            borders.append([row, col])
        elif pixel[row - 1, col - 1] == white \
                or pixel[row + 1, col + 1] == white \
                or pixel[row - 1, col + 1] == white \
                or pixel[row + 1, col - 1] == white:
            if pixel[row, col] == (0, 128, 255):
                borders.append([row, col])
            elif pixel[row, col] == (255, 0, 0):
                red.append([row - robot_center[0],col - robot_center[1]])
for pixl in borders:
    for r in red:
        x = pixl[0] + r[0]
        y = pixl[1] + r[1]
        if 0 <= x < 800 and 0 <= y < 400 and pixel[x, y] == white:
            pixel[x, y] = lightblue

delta = 30
whites = []

for x1 in range (width):
    for y1 in range (height):
        if pixel[x1, y1] == white:
            whites.append([x1, y1])

dps = []
dps.append(robot_center)
f_p = [650, 75]
dps.append(f_p)

while len(dps) < 100:
    x1 = np.asscalar(np.random.randint(0,width,1))
    y1 = np.asscalar(np.random.randint(0,height,1))
    t = True
    for j in dps:
        if distance(j[0], j[1], x1, y1) < delta:
            t = False
    if t:
        if [x1, y1] in whites:
            dps.append([x1, y1])

for i in dps:
    for j in range(i[0] - 2, i[0] + 2):
        for k in range(i[1] - 2, i[1] + 2):
            pixel[j, k] = (0, 0, 0)

s_p = dps[0]


points = np.array(dps)
tri = Delaunay(points)

def draw_line(x1, y1, x2, y2):
       min_y, max_y = (y1 if y1 < y2 else y2, y2 if y1 < y2 else y1)
       min_x, max_x = (x1 if x1 < x2 else x2, x2 if x1 < x2 else x1)
       print("X = {}, {}\t Y= {}, {}".format(x1,x2,y1,y2))
       if (min_x, min_y) == (x1, y1) or (min_x, min_y) == (x2, y2):
           k = 1000 if x2 == x1 else -(math.fabs(y2 - y1) / math.fabs(x2 - x1))
           b = 0
       else:
           k = 1000 if x2 == x1 else math.fabs(y2 - y1) / math.fabs(x2 - x1)
           b = -(max_y-min_y)
       f = True
       if not k == 1000:
           if not x1 == x2:
               r_x = np.arange(min_x*1.0+1, max_x*1.0-1, (max_x - min_x - 2) / 4)
               for x in r_x:
                   count_x = int(-(k * (x - min_x) + b) + min_y)
                   if 0 <= count_x < 400 and \
                           (pixel[int(x), count_x+1] == (0,128,255) or pixel[int(x), count_x+1] == lightblue or
                            pixel[int(x), count_x-1] == (0,128,255) or pixel[int(x), count_x-1] == lightblue or
                            pixel[int(x)-1, count_x] == (0,128,255) or pixel[int(x)-1, count_x] == lightblue or
                            pixel[int(x)+1, count_x] == (0,128,255) or pixel[int(x)+1, count_x] == lightblue):
                       f = False
       if f:
           draw.line(((x1, y1), (x2, y2)), fill='black')

for triangle in points[tri.simplices]:
    draw_line(triangle[0][0], triangle[0][1], triangle[1][0], triangle[1][1])
    draw_line(triangle[1][0], triangle[1][1], triangle[2][0], triangle[2][1])
    draw_line(triangle[2][0], triangle[2][1], triangle[0][0], triangle[0][1])

for j in range(s_p[0] - 3, s_p[0] + 3):
    for k in range(s_p[1] - 3, s_p[1] + 3):
        pixel[j, k] = (255, 255, 0)

for j in range(f_p[0] - 3, f_p[0] + 3):
    for k in range(f_p[1] - 3, f_p[1] + 3):
        pixel[j, k] = (0, 255, 0)

image.save("output5.png")


