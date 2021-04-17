import pygame
from copy import deepcopy
from random import randint
#from NumbersObject import Number
import Bot

pygame.init()


class Number (object):
    def __init__(self, num, x, y, width, height, image):
        self.number = num
        self.x = x
        self.y = y
        self.w = width
        self.h = height
        self.image = image
        self.hasMerged = True

    def __eq__(self, other):
        return self.number == other.number

    def draw(self, window):
        pass

    def __str__(self):
        return str(self.number)


window = pygame.display.set_mode((500, 500))
pygame.display.set_caption("2048")

clock = pygame.time.Clock()

links = [0, "2.png", "4.png", "8.png", "16.png", "32.png", "64.png", "128.png", "256.png", "512.png", "1024.png", "2048.png", "4096.png", "8192.png"]
numObjects = [0]

for i in range(1,14):
    numObjects.append(Number(i, 45, 45, 95, 95, links[i]))

board = [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]]
tileToMove = []
#Left, Right, Up, Down
# horizontalMove = [-52.5, 52.5, 0, 0]
# verticalMove = [0, 0, -52.5, 52.5]
horizontalMove = [-105, 105, 0, 0]
verticalMove = [0, 0, -105, 105]

board[0][0] = deepcopy(numObjects[1])
board[1][1] = deepcopy(numObjects[1])
board[2][1] = deepcopy(numObjects[2])
board[2][1].y += 210
board[2][1].x += 105
board[1][1].x += 105
board[1][1].y += 105
# board[3][0] = deepcopy(numObjects[12])
# board[3][0].y += 315

def drawGameWindow():
    window.fill((255, 255, 255))
    pygame.draw.rect(window, (100, 100, 100), (35, 35, 430, 430))

    for i in range(0, 4):
        for j in range (0, 4):
            pygame.draw.rect(window, (200, 200, 200), (45+i*105, 45+j*105, 95, 95))

    for i in range(0, 4):
        for j in range(0, 4):
            if not isinstance(board[i][j], int):
                window.blit(pygame.transform.scale(pygame.image.load(board[i][j].image), (board[i][j].w, board[i][j].h)), (board[i][j].x, board[i][j].y), (0, 0, 95, 95))

    pygame.display.update()

def placeRandomTile():
    emptyRow = []
    emptyCol = []
    for i in range(4):
        for j in range(4):
            if isinstance(board[i][j], int):
                emptyRow.append(i)
                emptyCol.append(j)
    if not emptyCol:
        return
    pos = randint(0, len(emptyCol)-1)
    if randint(0,1) == 1:
        board[emptyRow[pos]][emptyCol[pos]] = Number(1, 45 + emptyCol[pos]*105, 45 + emptyRow[pos]*105, 95, 95, links[1])
    else:
        board[emptyRow[pos]][emptyCol[pos]] = Number(2, 45 + emptyCol[pos] * 105, 45 + emptyRow[pos] * 105, 95, 95, links[2])
    drawGameWindow()

def adjustNewPiece(i, j):
    board[i][j].x += (i)*105
    board[i][j].y += (j)*105


def updateBoard(direction):
    global board
    tileToMove.clear()
    if direction == 0: #Left
        for i in range(4):
            for j in range(1,4):
                if not isinstance(board[i][j], int):
                    if board[i][j].x == 105*j-60:
                        if not isinstance(board[i][j-1], int) and board[i][j] == board[i][j-1]:
                            (board[i][j-1], board[i][j]) = (Number(board[i][j].number+1, 105*j - 60, 45 + 105*i, 95, 95, links[board[i][j].number+1]), 0)
                            board[i][j-1].hasMerged = True
                        else:
                            (board[i][j-1], board[i][j]) = (board[i][j], 0)
        moveLeft()
    elif direction == 1: #Right
        for i in range(4):
            for j in range(1,4):
                if not isinstance(board[i][3-j], int):
                    if board[i][3-j].x == 465 - 105*j:
                        if not isinstance(board[i][4-j], int) and board[i][3-j] == board[i][4-j]:
                            (board[i][4-j], board[i][3-j]) = (Number(board[i][3-j].number+1, 465 - 105*j, 45 + 105*i, 95, 95, links[board[i][3-j].number+1]), 0)
                            board[i][4-j].hasMerged = True
                        else:
                            (board[i][4-j], board[i][3-j]) = (board[i][3-j], 0)
        moveRight()
    elif direction == 2: #Up
        for j in range(4):
            for i in range(1, 4):
                if not isinstance(board[i][j], int):
                    if board[i][j].y == 105*i-60:
                        if not isinstance(board[i-1][j], int) and board[i][j] == board[i-1][j]:
                            (board[i - 1][j], board[i][j]) = (Number(board[i][j].number+1, 45 + (j)*105, 105*i - 60, 95, 95, links[board[i][j].number+1]), 0)
                            board[i-1][j].hasMerged = True
                        else:
                            (board[i-1][j], board[i][j]) = (board[i][j], 0)
        moveUp()
    elif direction == 3: #Down
        for j in range(4):
            for i in range(1, 4):
                if not isinstance(board[3-i][j], int):
                    if board[3-i][j].y == 465-105*i:
                        if not isinstance(board[4-i][j], int) and board[3-i][j] == board[4-i][j]:
                            (board[4-i][j], board[3-i][j]) = (Number(board[3-i][j].number+1, 45 + (j)*105, 465 - 105*i, 95, 95, links[board[3-i][j].number+1]), 0)
                            board[4-i][j].hasMerged = True
                        else:
                            (board[4-i][j], board[3-i][j]) = (board[3-i][j], 0)
        moveDown()
    drawGameWindow()


def moveUp():
    for i in range(1,4):
        for j in range(4):
            if not isinstance(board[i][j], int) and board[i][j].y > 45 and (isinstance(board[i-1][j], int) or (not isinstance(board[i-1][j], int) and board[i-1][j] == board[i][j] and not board[i-1][j].hasMerged and not board[i][j].hasMerged) or (4*(i-1)+j) in tileToMove):
                tileToMove.append(4*i+j)
    return len(tileToMove) == 0

def moveDown():
    for i in range(1,4):
        for j in range(4):
            if not isinstance(board[3-i][j], int) and board[3-i][j].y < 360 and (isinstance(board[4-i][j], int) or (not isinstance(board[4-i][j], int) and board[4-i][j] == board[3-i][j] and not board[4-i][j].hasMerged and not board[3-i][j].hasMerged) or (4*(4-i)+j) in tileToMove):
                tileToMove.append(4*(3-i)+j)
    return len(tileToMove) == 0

def moveRight():
    for i in range(4):
        for j in range(1,4):
            if not isinstance(board[i][3-j], int) and board[i][3-j].x < 360 and (isinstance(board[i][4-j], int) or (not isinstance(board[i][4-j], int) and board[i][4-j] == board[i][3-j] and not board[i][4-j].hasMerged and not board[i][3-j].hasMerged) or (4*(i)+4-j) in tileToMove):
                tileToMove.append(4*i+3-j)
    return len(tileToMove) == 0

def moveLeft():
    for i in range(4):
        for j in range(1,4):
            if not isinstance(board[i][j], int) and board[i][j].x > 45 and (isinstance(board[i][j-1], int) or (not isinstance(board[i][j-1], int) and board[i][j-1] == board[i][j] and not board[i][j-1].hasMerged and not board[i][j].hasMerged) or (4*(i)+j-1) in tileToMove):
                tileToMove.append(4*i+j)
    return len(tileToMove) == 0


def canMove():
    for i in range(4):
        for j in range(4):
            if isinstance(board[i][j], int):
                return True
    for i in range(3):
        for j in range(4):
            if board[i][j] == board[i+1][j]:
                return True
            if board[j][i] == board[j][i+1]:
                return True
    return False

def getScore():
    sum = 0
    for i in range(4):
        for j in range(4):
            sum += 2**board[i][j].number
    return sum

def checkStuff():
    pass

def main():
    #placeRandomTile()
    drawGameWindow()

    currentDirection = -1
    needsTile = False
    shiftingTiles = False
    running = True
    counter = 0
    while running:
        clock.tick(30)

        if canMove():
            events = pygame.event.get()
            for event in events:
                if not shiftingTiles:
                    if event.type == pygame.QUIT:
                        running = False
                    if event.type == pygame.KEYDOWN:
                        shiftingTiles = True
                        pygame.event.clear()
                        if event.key == pygame.K_DOWN:
                            if not moveDown():
                                needsTile = True
                            currentDirection = 3
                            break
                        if event.key == pygame.K_UP:
                            if not moveUp():
                                needsTile = True
                            currentDirection = 2
                            break
                        if event.key == pygame.K_RIGHT:
                            if not moveRight():
                                needsTile = True
                            currentDirection = 1
                            break
                        if event.key == pygame.K_LEFT:
                            if not moveLeft():
                                needsTile = True
                            currentDirection = 0
                            break
        else:
            pygame.event.clear()

        if not tileToMove:
            if needsTile:
                placeRandomTile()
                for i in range(4):
                    for j in range(4):
                        if not isinstance(board[i][j], int):
                            board[i][j].hasMerged = False
                # for i in range(4):
                #     print(str(board[i][0]), str(board[i][1]), str(board[i][2]), str(board[i][3]))
                # print("\n")
                needsTile = False
            counter = 0
            shiftingTiles = False
        else:
            counter += 1
            for tile in tileToMove:
                row = tile // 4
                col = tile % 4
                board[row][col].y += verticalMove[currentDirection]
                board[row][col].x += horizontalMove[currentDirection]
                drawGameWindow()
            if counter != 0 and counter == 1:
                updateBoard(currentDirection)
                counter = 0
        drawGameWindow()

main()
