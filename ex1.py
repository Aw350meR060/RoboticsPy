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

image = Image.new('RGB',(400, 400), "white")
draw = ImageDraw.Draw(image)

draw.ellipse((149.5,149.5,350.5,350.5), fill = (0, 128, 255), outline = (0, 128, 255))
robot_vertices = ((60, 60), (81, 60), (81, 101), (60, 101))
robot_center =  [71, 81]
robot_vertices = [rotation(x, y, robot_center[0], robot_center[1], math.radians(-20)) for x, y in robot_vertices]
draw.polygon(robot_vertices, fill = "red")
image.save("output1.png")


img = Image.open("output1.png")
width, height = img.size
white = (255, 255, 255)
lightblue = (128, 194, 255)
pixel = img.load()
borders = []
red = []

for row in range (1,height-1):
    for col in range (1, width-1):
        if (pixel[row, col] == (0, 128, 255)) and \
                (pixel[row - 1, col - 1] == white or
                        pixel[row + 1, col + 1] == white or
                        pixel[row - 1, col + 1] == white or
                        pixel[row + 1, col - 1] == white):
                        # pixel[row + 1, col - 1] == white) or row == 0 or col == 0 or row == 399 or col == 399:
                borders.append([row, col])
        if (pixel[row, col] == (255, 0, 0)) and \
                (pixel[row - 1, col - 1] == white or
                        pixel[row + 1, col + 1] == white or
                        pixel[row - 1, col + 1] == white or
                        pixel[row + 1, col - 1] == white):
            red.append([row - robot_center[0],col - robot_center[1]])
for pixl in borders:
    for p in red:
        x = pixl[0] + p[0]
        y = pixl[1] + p[1]
        if 0 <= x < 400 and 0 <= y < 400 and pixel[x, y] == white:
            pixel[x, y] = lightblue

img.save("output1.png")


