import math
from PIL import Image, ImageDraw
import numpy as np


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
image.save("output2.png")


img = Image.open("output2.png")
width, height = img.size
white = (255, 255, 255)
lightblue = (128, 194, 255)
pixel = img.load()
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

img.save("output2.png")


