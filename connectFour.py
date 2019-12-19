import pygame, sys, random
from pygame.locals import *

FPS = 30
ROW = 7
COL = 7
SQSZ = 80
WINHEI = SQSZ * ROW
WINWID = SQSZ * COL
CIRSZ = 40

TAN = (210,180,140)
SADDLEBROWN = (139,69,19)
VIOLET = (238,130,238)
STALEBLUE = (106,90,205)
WHITE = (255,255,255)

P1 = VIOLET
P2 = STALEBLUE
SQCLR  = SADDLEBROWN
BGCLR = TAN

def main():
    global screen, FPSCLOCK
    pygame.init()
    FPSCLOCK = pygame.time.Clock()
    screen = pygame.display.set_mode((WINHEI, WINWID))
    pygame.display.set_caption('Connect Four')
    myFont = pygame.font.SysFont('Calibri', 30, bold = True)
    textSurf = myFont.render('New Game', True, SADDLEBROWN)
    textRect = textSurf.get_rect()
    textRect.topleft = (5, 5)
    
    
    board = createBoard(ROW, COL)
    playerCount = 0
    curPlayer = None
    pClr = None
    pos  = None
    moved = True        
    drawBoard(board)
    while True:
        if moved:
            if playerCount%2 ==0:
                curPlayer = 1
                pClr = P1
                pos = 3
                moved = False
                drawBoard(board)
                drawCir(0,pos,pClr)
            else:
                curPlayer = 2
                pClr = P2
                pos = 3
                moved = False
                drawBoard(board)
                drawCir(0,pos,pClr)
            if playerCount == 0:
                screen.blit(textSurf, textRect)
        else:
            if curPlayer == 1:
                for event in pygame.event.get():
                    if event.type == QUIT:
                        pygame.quit()
                        sys.exit()
                    if event.type == KEYDOWN:
                        if event.key == K_RIGHT:
                            pos += 1 
                            if pos == 7:
                                pos = 6
                            drawBoard(board)
                            drawCir(0,pos, pClr)
                        if event.key == K_LEFT:
                            pos -= 1
                            if pos == -1:
                                pos = 0
                            drawBoard(board)
                            drawCir(0,pos, pClr)
                        if event.key == K_DOWN:
                            if checkAvailSpot(board, pos):
                                board = addMove(board, pos, curPlayer)
                                drawBoard(board)
                                if checkForWin(board) != None:
                                    row, col, direction = checkForWin(board)
                                    winAnimation(board, row, col, direction, pos, pClr)
                                    printBoard(board)
                                    pygame.time.wait(1000)
                                    
                                    board = createBoard(ROW, COL)
                                    playerCount = 0
                                    moved = True        
                                    drawBoard(board)
                                    screen.blit(textSurf, textRect)
                                    
                                else:
                                    moved = True
                                    playerCount += 1      
                            else:  
                                fullColAnimation(pos)  
                                drawBoard(board)
                                drawCir(0,pos, pClr)  
            elif curPlayer == 2:   
                pos  = random.randint(0,6)
                while not checkAvailSpot(board, pos):
                    pos  = random.randint(0,6)
                board = addMove(board, pos, curPlayer)
                drawBoard(board)
                if checkForWin(board) != None:
                    row, col, direction = checkForWin(board)
                    winAnimation(board, row, col, direction, pos, pClr)
                    board = createBoard(ROW, COL)
                    playerCount = 0
                    moved = True        
                    drawBoard(board)
                    screen.blit(textSurf, textRect)
                    
                else:
                    moved = True
                    playerCount += 1
        
        pygame.display.update()
        FPSCLOCK.tick(FPS)

def createBoard(row, col):
    initBoard = [[0 for _ in range(col)] for _ in range(row)]
    return initBoard
def drawBoard(board):
    screen.fill(BGCLR)
    pygame.draw.rect(screen, SQCLR, (0,CIRSZ*2,CIRSZ*2*ROW,CIRSZ*2*COL))
    center = CIRSZ
    for r in range(1,ROW):
        for c in range(COL):
            if board[r][c] == 0:
                pygame.draw.circle(screen, BGCLR, (center*(2*c+1), center*(2*r+1)), CIRSZ)
            elif board[r][c] == 1:
                pygame.draw.circle(screen, P1, (center*(2*c+1), center*(2*r+1)), CIRSZ)
            elif board[r][c] == 2:
                pygame.draw.circle(screen, P2, (center*(2*c+1), center*(2*r+1)), CIRSZ)
def drawCir(row, pos, pClr):
    pygame.draw.circle(screen, pClr, (CIRSZ*(2*pos+1), CIRSZ*(2*row+1)), CIRSZ)
def checkAvailSpot(board, pos):
    for r in range(1, ROW):
        if board[r][pos] == 0:
            return True
    return False
def fullColAnimation(pos):
    pygame.draw.rect(screen, (230,0,0),(CIRSZ*2*pos, CIRSZ*2, CIRSZ*2, CIRSZ*(ROW-1)*2), 3)
    pygame.display.update()
    FPSCLOCK.tick(FPS)
    pygame.time.wait(150)
def addMove(board, pos, player):
    for r in range(ROW-1,0,-1):
        if board[r][pos] == 0:
            board[r][pos] = player
            break
    return board
def checkForWin(board):
    #check horizontally
    for r in range(1, ROW):
        for c in range(4):
            if board[r][c] == board[r][c+1] == board[r][c+2] == board[r][c+3] != 0:
                return (r,c,0)
    #check vertically
    for c in range(COL):
        for r in range(1, 4):
            if board[r][c] == board[r+1][c] == board[r+2][c] == board[r+3][c] != 0:
                return (r,c,1)
    #check diagonally
    for r in [1,2,3]:
        for c in [3,4,5,6]:
            if board[r][c] == board[r+1][c-1] == board[r+2][c-2] == board[r+3][c-3] != 0:
                return (r,c,2)
    for r in [4,5,6]:
        for c in [3,4,5,6]:
            if board[r][c] == board[r-1][c-1] == board[r-2][c-2] == board[r-3][c-3] != 0:
                return (r,c,3)
    return None
def winAnimation(board, row, col, direction, pos, pClr):
    if direction == 0:
        for _ in range (5):
            for i in range (4):
                pygame.draw.circle(screen, WHITE, (CIRSZ*(2*(col+i)+1), CIRSZ*(2*row+1)), CIRSZ)
                pygame.display.update()
                FPSCLOCK.tick(FPS)
                pygame.time.wait(50)
            drawBoard(board)
            drawCir(row,pos,pClr)
            pygame.display.update()
            FPSCLOCK.tick(FPS)
            pygame.time.wait(80)
    if direction == 1:
        for _ in range (5):
            for i in range (4):
                pygame.draw.circle(screen, WHITE, (CIRSZ*(2*(col)+1), CIRSZ*(2*(row+i)+1)), CIRSZ)
                pygame.display.update()
                FPSCLOCK.tick(FPS)
                pygame.time.wait(50)
            drawBoard(board)
            drawCir(row,pos,pClr)
            pygame.display.update()
            FPSCLOCK.tick(FPS)
            pygame.time.wait(80)
    if direction == 2:
        for _ in range (5):
            for i in range (4):
                pygame.draw.circle(screen, WHITE, (CIRSZ*(2*(col-i)+1), CIRSZ*(2*(row+i)+1)), CIRSZ)
                pygame.display.update()
                FPSCLOCK.tick(FPS)
                pygame.time.wait(50)
            drawBoard(board)
            drawCir(row,pos,pClr)
            pygame.display.update()
            FPSCLOCK.tick(FPS)
            pygame.time.wait(80)
    if direction == 3:
        for _ in range (5):
            for i in range (4):
                pygame.draw.circle(screen, WHITE, (CIRSZ*(2*(col-i)+1), CIRSZ*(2*(row-i)+1)), CIRSZ)
                pygame.display.update()
                FPSCLOCK.tick(FPS)
                pygame.time.wait(50)
            drawBoard(board)
            drawCir(row,pos,pClr)
            pygame.display.update()
            FPSCLOCK.tick(FPS)
            pygame.time.wait(80)  
def printBoard(board):
    for row in board:
        print(row)






if __name__ == '__main__':
    main()
    