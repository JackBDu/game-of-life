########################################################
###       Project 3 - Conway's Game of Life          ###
########################################################

__author__ = "Jack B. Du (Jiadong Du)"
__copyright__ = "Copyright 2014, DS @NYUSH"
__email__ = "JackDu@nyu.edu"

import pygame
from pygame.locals import *
import random

# absolute varibles
BLACK_COLOR = (0, 0, 0)
WHITE_COLOR = (255, 255, 255)
GRAY_COLOR = (200, 200, 200)
LEVELS = 9
ELEMENT = 255//(LEVELS+1)
COLOR = [(ELEMENT*(LEVELS-i), ELEMENT*(LEVELS-i), ELEMENT*(LEVELS-i)) for i in range(1, LEVELS+1)]
RED_COLOR = (255, 0, 0)
GREEN_COLOR = (0, 255, 0)
BLUE_COLOR = (0, 0, 255)

# manual initialization
pygame.init()
INIT_SCREEN_W = 800
INIT_SCREEN_H = 600
MARGIN = 50
cellSize = 50
fps = 50
bg_color = GRAY_COLOR
fullscreen = False
FONT = "arial"
caption = "Jack's Game of Life"
showNum = False
zoomMode = False
zoomWidth = 2
minSize = 10
moveX = 0
moveY = 0

# get device info
infoObject = pygame.display.Info()
FULLSCREEN_W = infoObject.current_w
FULLSCREEN_H = infoObject.current_h

# automatic initialization
if fullscreen:
    current_screen_w = FULLSCREEN_W
    current_screen_h = FULLSCREEN_H
else:
    current_screen_w = INIT_SCREEN_W
    current_screen_h = INIT_SCREEN_H
    
paused = False
screen = pygame.display.set_mode((current_screen_w, current_screen_h), RESIZABLE, 32)
background = pygame.Surface(screen.get_size())
background = background.convert()
background.fill(bg_color)
lastMouseClick = None
setFalse = False

pygame.display.set_caption(caption)

def setup():
    global cellMatrix, w_num, h_num, background, counts, font, current_margin_w, current_margin_h, screen

    background = pygame.Surface(screen.get_size())
    background = background.convert()
    background.fill(bg_color)

    if not zoomMode:
        current_margin_w = MARGIN + (current_screen_w - MARGIN * 2) % cellSize / 2
        current_margin_h = MARGIN + (current_screen_h - MARGIN * 2) % cellSize / 2
        w_num = int((current_screen_w - current_margin_w * 2) / cellSize)
        h_num = int((current_screen_h - current_margin_h * 2) / cellSize)
        
        cellMatrix = [[None for y in range(h_num)] for x in range(w_num)]
        counts = [[None for y in range(h_num)] for x in range(w_num)]

    fontSize = cellSize
    font = pygame.font.SysFont("arial", fontSize)
        
    for x in range(w_num):
        for y in range(h_num):
            if zoomMode:
                cellMatrix[x][y].zoom((current_margin_w+x*cellSize+moveX, current_margin_h+y*cellSize+moveY, cellSize-1, cellSize-1))
            else:
                c = random.randint(0,1)
                if c == 0:
                    isOn = False
                else:
                    isOn = True
                if setFalse:
                    isOn = False
                cellMatrix[x][y] = cell(screen, isOn, (current_margin_w+x*cellSize, current_margin_h+y*cellSize, cellSize-1, cellSize-1))

def checkEdge():
    global moveX, moveY
    
    xMax = w_num * cellSize - (current_screen_w - 2 * current_margin_w)
    if moveX < -xMax:
        moveX = -xMax
    elif moveX > 0:
        moveX = 0
    
    yMax = h_num * cellSize - (current_screen_h - 2 * current_margin_h)
    if moveY < -yMax:
        moveY = -yMax
    elif moveY > 0:
        moveY = 0

def events():
    global mainloop, screen, fullscreen, background, lastMouseClick, current_screen_w, current_screen_h, paused, cellSize, showNum, setFalse, fps, zoomMode, minSize, moveX, moveY
    
    for event in pygame.event.get():
        
        if event.type == QUIT:
            mainloop = False
            
        if event.type == KEYDOWN:

            # handling fullscreen
            if event.key == K_f:
                fullscreen = not fullscreen
                if fullscreen:
                    current_screen_w = FULLSCREEN_W
                    current_screen_h = FULLSCREEN_H
                    screen = pygame.display.set_mode((current_screen_w, current_screen_h), FULLSCREEN, 32)
                else:
                    current_screen_w = INIT_SCREEN_W
                    current_screen_h = INIT_SCREEN_H
                    screen = pygame.display.set_mode((current_screen_w, current_screen_h), RESIZABLE, 32)
                setup()
            elif event.key == K_r:
                if zoomMode:
                    zoomMode = False
                    cellSize = minSize
                    minSize = 10
                    moveX = 0
                    moveY = 0
                setup()
            elif event.key == K_SPACE:
                paused = not(paused)
            elif event.key == K_EQUALS:
                if cellSize < 100:
                    cellSize += 10
                    if zoomMode:
                        checkEdge()
                    setup()
            elif event.key == K_MINUS:
                if cellSize > minSize:
                    cellSize -= 10
                    if zoomMode:
                        checkEdge()
                    setup()
            elif event.key == K_n:
                showNum = not showNum
            elif event.key == K_ESCAPE:
                setFalse = True
                setup()
                setFalse = False
            elif event.key == K_1:
                if fps > 5:
                    fps -= 5
                elif fps > 1:
                    fps -= 1
            elif event.key == K_2:
                if fps < 100:
                    fps += 5
            elif event.key == K_DOWN:
                if zoomMode:
                    moveY -= cellSize
                    checkEdge()
                    setup()
            elif event.key == K_UP:
                if zoomMode:
                    moveY += cellSize
                    checkEdge()
                    setup()
            elif event.key == K_RIGHT:
                if zoomMode:
                    moveX -= cellSize
                    checkEdge()
                    setup()
            elif event.key == K_LEFT:
                if zoomMode:
                    moveX += cellSize
                    checkEdge()
                    setup()
            elif event.key == K_z:
                zoomMode = not zoomMode
                if zoomMode:
                    minSize = cellSize
                else:
                    cellSize = minSize
                    minSize = 10
                    zoomMode = not zoomMode
                    moveX = 0
                    moveY = 0
                    setup()
                    zoomMode = not zoomMode
                    

        elif event.type == pygame.MOUSEBUTTONDOWN:
            lastMouseClick = pygame.mouse.get_pos()
            for x in range(w_num):
                for y in range(h_num):
                    cellMatrix[x][y].isClicked(lastMouseClick)

        elif event.type == VIDEORESIZE:
            current_screen_w = event.size[0]
            current_screen_h = event.size[1]
            screen = pygame.display.set_mode(event.size, RESIZABLE, 32)
            zoomMode = False
            setup()

def main():
    global mainloop, screen, fullscreen, background

    setup()
    
    mainloop = True
    
    while mainloop:

        pygame.time.Clock().tick(fps)

        # update
        update()

        # draw
        draw()

    pygame.quit()

def update():
    global counts
    
    events()

    if not paused:
        for x in range(w_num):
            for y in range(h_num):
                count = countArounded(x, y)
                if count == 3:
                    cellMatrix[x][y].setStatus(True)
                elif count == 2 and cellMatrix[x][y].getStatus():
                    cellMatrix[x][y].setStatus(True)
                else:
                    cellMatrix[x][y].setStatus(False)


def countArounded(x, y):
    count = 0
    try:
        if cellMatrix[x-1][y].getStatus() and x > 0:
            count += 1
    except:
        count += 0
    try:
        if cellMatrix[x+1][y].getStatus():
            count += 1
    except:
        count += 0
    try:
        if cellMatrix[x][y+1].getStatus():
            count += 1
    except:
        count += 0
    try:
        if cellMatrix[x][y-1].getStatus() and y > 0:
            count += 1
    except:
        count += 0
    try:
        if cellMatrix[x-1][y-1].getStatus() and x > 0 and y > 0:
            count += 1
    except:
        count += 0
    try:
        if cellMatrix[x-1][y+1].getStatus() and x > 0:
            count += 1
    except:
        count += 0
    try:
        if cellMatrix[x+1][y-1].getStatus() and y > 0:
            count += 1
    except:
        count += 0
    try:
        if cellMatrix[x+1][y+1].getStatus():
            count += 1
    except:
        count += 0
    return count

def draw():
    global current_margin_w, current_margin_h
    
    screen.blit(background,(0,0))

    for x in range(w_num):
        for y in range(h_num):
            counts[x][y] = countArounded(x, y)
            try:
                cellMatrix[x][y].setColor(COLOR[counts[x][y]])
            except:
                print(counts[x][y])
    
    for x in range(w_num):
        for y in range(h_num):
            cellMatrix[x][y].draw()
            if showNum:
                countLabel = font.render(str(counts[x][y]), 1, BLACK_COLOR)
                if counts[x][y] != 0:
                    screen.blit(countLabel, cellMatrix[x][y].getPos())

    if zoomMode:
        pygame.draw.rect(screen, BLACK_COLOR, (current_margin_w-zoomWidth, current_margin_h-zoomWidth, current_screen_w-2*current_margin_w+zoomWidth, current_screen_h-2*current_margin_h+zoomWidth), zoomWidth)
        pygame.draw.rect(screen, bg_color, (0, 0, current_margin_w-zoomWidth, current_screen_h-zoomWidth))
        pygame.draw.rect(screen, bg_color, (0, 0, current_screen_w-zoomWidth, current_margin_h-zoomWidth))
        pygame.draw.rect(screen, bg_color, (current_screen_w - current_margin_w + zoomWidth/2, 0, current_margin_w, current_screen_h))
        pygame.draw.rect(screen, bg_color, (0, current_screen_h - current_margin_h + zoomWidth/2, current_screen_w, current_margin_h))
        
    pygame.display.update()

class cell(object):

    def __init__(self, surface, isOn, rect):
        self.surface = surface
        self.wasOn = isOn
        self.isOn = isOn
        self.rect = rect
        self.color = None

    def setColor(self, color):
        self.color = color

    def zoom(self, rect):
        self.rect = rect

    def getPos(self):
        return (self.rect[0], self.rect[1], self.rect[0] + self.rect[2], self.rect[1] + self.rect[3])

    def getStatus(self):
        return self.wasOn

    def setStatus(self, isOn):
        self.isOn = isOn

    def isClicked(self, pos):
        (x, y, w, h) = self.rect
        px = pos[0]
        py = pos[1]
        clicked = py >= y and \
            py <= y + h and \
            px >= x and \
            px <= x + w
        if clicked:
            self.wasOn = not self.wasOn
            self.isOn = not self.isOn

    def getPos(self):
        return (self.rect[0], self.rect[1])
    
    def draw(self):
        self.wasOn = self.isOn
        if not self.isOn:
            self.color = WHITE_COLOR
        pygame.draw.rect(self.surface, self.color, self.rect)

main()
