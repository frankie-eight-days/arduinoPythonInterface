#import all functions from pygame, OpenGL libraries
import pygame
from pygame.locals import *

from OpenGL.GL import *
from OpenGL.GLU import *

import serial

#Opens serial connection on port. Ensure that the baudrate is equal what's set in your arduino
ser = serial.Serial('COM5', baudrate = 9600, timeout = None)
bytesToRead = 0 #Holds the number of bytes to read in the serial port

#Dimensions of the rendered object
depth = 4
height = 0.5
length = 1

#Arrays used to handle angle data
rotationData = [0.0, 0.0, 0.0]
oldAngle = [0.0, 0.0, 0.0]
deltaAngle = [0.0, 0.0, 0.0]

#Tuples used to describe the geometry of the cube
verticies = (
    (length, -height, -depth),
    (length, height, -depth),
    (-length, height, -depth),
    (-length, -height, -depth),
    (length, -height, 0),
    (length, height, 0),
    (-length, -height, 0),
    (-length, height, 0)
)

edges = (
    (0,1),
    (0,3),
    (0,4),
    (2,1),
    (2,3),
    (2,7),
    (6,3),
    (6,4),
    (6,7),
    (5,1),
    (5,4),
    (5,7)
)

surfaces = (
    (0,1,2,3),
    (3,2,7,6),
    (6,7,5,4),
    (4,5,1,0),
    (1,5,7,2),
    (4,0,3,6)
)

colors = (
    (1,0,0),
    (0,1,0),
    (0,0,1),
    (0,0,0),
    (1,1,1),
    (0,1,1),
    (1,0,0),
    (0,1,0),
    (0,0,1),
    (0,0,0),
    (1,1,1),
    (0,1,1)
)

#This function draws the cube on the screen.
def Cube():
    #Loops through the geometry of the cube and draws the colors.
    glBegin(GL_QUADS)
    for surface in surfaces:
        x = 0
        for vertex in surface:
            x += 1
            glColor3fv(colors[x])
            glVertex3fv(verticies[vertex])
    glEnd()

    #Draws the framework of the cube. Not necessary but looks nicer.
    glBegin(GL_LINES)
    for edge in edges:
        for vertex in edge:
            glVertex3fv(verticies[vertex])
    glEnd()

def getSerialData():
    global arduinoData
    arduinoData = []
    bytesToRead = ser.in_waiting
    #Reads the data from the serial port and converts it to an array of ascii characters.
    arduinoData += [chr(c) for c in ser.read(bytesToRead)]
    arduinoData = ''.join(arduinoData)  #Converts the array to a string
    if len(arduinoData) > 1:            #Checks to see if the serial is sending data
        for i in range(3):              #Loops through the three angles
            rotationData[i] = arduinoData.split(" ")[i]     #Splits the string at spaces into it's angles.
        rotationData[2] = rotationData[2][:-2]              #Gets rid of the new line at the end of the string.
    #print(rotationData)

#Calculates how much the cube should rotate
def getDeltaAngle():
    for i in range(3):
        deltaAngle[i] = float(rotationData[i]) - oldAngle[i]
        oldAngle[i] = float(rotationData[i])    #Sets the 'old' angle to the new angle after calculations

#Rotates the cube on the longitudinal axis.
def rotateRoll():
    glTranslatef(0, 0, -depth / 2)          #The object must be brought to the origin to be rotated.
    glRotatef(-deltaAngle[1], 0, 0, depth/2)
    glTranslatef(0, 0, depth / 2)           #Object gets put back in it's original position.

#Rotates the cube on the lateral axis
def rotatePitch():
    glTranslatef(0, 0, -depth / 2)              #The object must be brought to the origin to be rotated.
    glRotatef(deltaAngle[0], depth / 2, 0, 0)
    glTranslatef(0, 0, depth / 2)               #Object gets put back in it's original position.

def main():
    pygame.init()
    display = (800,600) #Size of the window
    pygame.display.set_mode(display, DOUBLEBUF|OPENGL)
    gluPerspective(45, (display[0]/display[1]), 0.1, 50.0)
    glTranslatef(0.0, 0.0, -5)      #Sets original position of the cube.

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        getSerialData()
        getDeltaAngle()
        rotateRoll()
        rotatePitch()
        glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
        Cube()
        pygame.display.flip()

main()