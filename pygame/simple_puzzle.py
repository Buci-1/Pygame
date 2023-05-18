import pygame
from pygame.locals import *
import sys

import random
WINWIDTH = 640
WINHEIGHT = 480
ROW = 3
COL = 3
BLANK = None
#-------颜色-------
DARKGRAY = (60,60,60)
WHITE = (255,255,255)
YELLOW = (255,255,193)
GRAY = (128,128,128)
BRIGHTBLUE = (138,228,221)
#-------颜色变量------
BLANKCOLOR = DARKGRAY
MSGCOLOR = WHITE
BTCOLOR = YELLOW
BTTEXTCOLOR = GRAY
BDCOLOR = BRIGHTBLUE

#-------静态常量-------
BLOCKSIZE = 80 #滑块边长
FPS = 60
UP = 'up'
DOWN = 'down'
LEFT = 'left'
RIGHT = 'right'
NEWGAME = 'newgame'
AUTOMOVE = random.randint(50,100)


#一.顶层设计
#生成推盘序列
def getStrartingBoard():
    return [['1','4','7'],['2','5','8'],['3','6',BLANK]]

#静态界面
def drawStaticWin():
    
    #窗口
    WINSET = pygame.display.set_mode((WINWIDTH,WINHEIGHT))
    #名字
    pygame.display.set_caption('推盘游戏')
    #背景图片
    image = pygame.image.load('androidparty.jpg')
    #绘制到窗口中
    WINSET.blit(image,(0,0))
    
    #新游戏按钮
    new_surf, new_rect =  makeText('新游戏',BTTEXTCOLOR,BTCOLOR,WINWIDTH-85,WINHEIGHT - 40)
    #绘制窗口中
    WINSET.blit(new_surf,new_rect)
    #返回数据
    return WINSET,new_surf,new_rect



#
def makeText(text,tColor,btColor,top,left):
    textSurf = BASICFONT.render(text,True,tColor,btColor)
    textRect = textSurf.get_rect()
    textRect.topleft = (top,left)
    return textSurf,textRect



#动态界面
def drawBoard(board,msg):

    #使用备份覆盖WINSET
    WINSET.blit(STATITCSURF,(0,0))


    #提示信息
    if msg:
        msg_surf,msg_rect = makeText(msg,MSGCOLOR,None,5,5)
        pygame.image.save(msg_surf,'msg.png')
        imaSurf = pygame.image.load('msg.png')
        WINSET.blit(imaSurf,msg_rect)

    for i in range(len(board)):
        for j in range(len(board[0])):
            if board[i][j]:
                #绘制方块
                drawTile(i,j,board[i][j])
    #计算方块距离原点的横纵坐标f
    left,top = getLeftTopOfTile(0,0)
    width,height = COL*BLOCKSIZE,ROW*BLOCKSIZE

    #绘制外边框
    pygame.draw.rect(WINSET,BDCOLOR,(left-5, top-5,width+11, height+11),4)

#在窗口的坐标(tilex,tiley)处绘制方块
def drawTile(tilex,tiley,number,adjx=0,adjy=0):
    left,top = getLeftTopOfTile(tilex,tiley)
    pygame.draw.rect(WINSET,BTCOLOR,(left+adjx,top+adjy,BLOCKSIZE,BLOCKSIZE))
    textSurf = BASICFONT.render(str(number),True,BTTEXTCOLOR)
    textRect = textSurf.get_rect()
    textRect.center = left+int(BLOCKSIZE/2)+adjx,top+int(BLOCKSIZE/2)+adjy
    WINSET.blit(textSurf,textRect) 


def getLeftTopOfTile(tilex,tiley):
    #拼图距离窗口边缘的距离
    xMargin = int((WINWIDTH - (BLOCKSIZE*COL + (COL-1)))/2)
    yMargin = int((WINHEIGHT - (BLOCKSIZE*ROW + (ROW-1)))/2)
    left = xMargin + (tilex*BLOCKSIZE) + (tilex-1)
    top = yMargin + (tiley*BLOCKSIZE) + (tiley-1)
    return left,top

#初始化
def generateNewPuzzle(numSlides):
    
    #获取拼图的矩阵
    mainBoard = getStrartingBoard()
    #绘制动态的推盘
    drawBoard(mainBoard,'')

    #记录上一次移动的方向
    lastMove = None

    #循环
    for i in range(numSlides):
        #获取每次随机移动的方向
        move = getRandomMove(mainBoard, lastMove)
        #实现本次移动的动画
        slideAnimation(mainBoard,move,'初始化...',int(BLOCKSIZE/3))
        #修改推盘序列中元素的序列
        makeMove(mainBoard,move)
        #记录本次产生的以东方方向
        lastMove = move 

    #返回最终的序列
    return mainBoard



#获取随机移动的方向
def getRandomMove(board,lastMove=None):
    validMovs = [UP,DOWN,LEFT,RIGHT]
    #从列表中删除被取消资格的移动方向
    if lastMove == UP or not isValidMove(board,DOWN):
        validMovs.remove(DOWN)
    if lastMove == DOWN or not isValidMove(board,UP):
        validMovs.remove(UP)
    if lastMove == LEFT or not isValidMove(board,RIGHT):
        validMovs.remove(RIGHT)
    if lastMove == RIGHT or not isValidMove(board,LEFT):
        validMovs.remove(LEFT)
    return random.choice(validMovs)


#根据空白块的位置移动的方向判断本次移动是否为有效移动
def isValidMove(board,move):
    blankx,blanky = getBlankPosition(board)
    if move == UP:
        return blanky != len(board[0])-1
    if move == DOWN:
        return blanky != 0
    if move == LEFT:
        return blankx != len(board)-1
    if move == RIGHT:
        return blankx != 0
    



#实现本次移动的动画
def slideAnimation(board,direction,msg,animationSpeed):
    blankx,blanky = getBlankPosition(board)

    if direction == UP:
        movex,movey = blankx,blanky+1
    elif direction == DOWN:
        movex,movey = blankx,blanky-1
    elif direction == LEFT:
        movex,movey = blankx+1,blanky
    elif direction == RIGHT:
        movex,movey = blankx-1,blanky
    
    #基础准备
    drawBoard(board,msg)
    BASESURF = WINSET.copy()

    #在要移动的拼图块上绘制空白块
    moveLeft,moveTop = getLeftTopOfTile(movex,movey)   
    pygame.draw.rect(BASESURF,BDCOLOR,(moveLeft,moveTop,BLOCKSIZE,BLOCKSIZE))

    #在移动路径上连续绘制被移动的方块
    for i in range(0,BLOCKSIZE,animationSpeed):
        checkForQuit()
        WINSET.blit(BASESURF,(0,0))
        if direction == UP:
            drawTile(movex,movey,board[movex][movey],0,-i)
        if direction == DOWN:
            drawTile(movex,movey,board[movex][movey],0,i)
        if direction == LEFT:
            drawTile(movex,movey,board[movex][movey],-i,0)
        if direction == RIGHT:
            drawTile(movex,movey,board[movex][movey],i,0)
        pygame.display.update()
        FPSCLOCK.tick(FPS)



#修改推盘序列中元素的序列
def makeMove(board,move):
    blankx,blanky = getBlankPosition(board)
    if move == UP:
        board[blankx][blanky],board[blankx][blanky+1] = board[blankx][blanky+1],board[blankx][blanky]
    elif move == DOWN:
        board[blankx][blanky],board[blankx][blanky-1] = board[blankx][blanky-1],board[blankx][blanky]
    elif move == LEFT:
        board[blankx][blanky],board[blankx+1][blanky] = board[blankx+1][blanky],board[blankx][blanky]
    elif move == RIGHT:
        board[blankx][blanky],board[blankx-1][blanky] = board[blankx-1][blanky],board[blankx][blanky]

#接受输入
def getInput(mainBoard):
    #获取事件列表
    events = pygame.event.get()
    #定义变量，保存返回值
    userInput = None
    #循环遍历事件列表
    for event in events:
        if event.type == MOUSEBUTTONUP:
            #根据x,y坐标，获取方块再推盘中的位置
            spotx, spoty = getSpotClicked(mainBoard,event.pos[0],event.pos[1])
            
            #新游戏
            if (spotx, spoty) == (None,None) and NEW_RECT.collidepoint(event.pos):
                userInput = NEWGAME
            else:
                if mainBoard == getStrartingBoard():
                    break
            #获取空白拼图的位置
            blankx, blanky = getBlankPosition(mainBoard)
            if spotx == blankx + 1 and spoty == blanky:
                userInput = LEFT
            elif spotx == blankx - 1 and spoty == blanky:
                userInput = RIGHT
            elif spotx == blankx and spoty == blanky + 1:
                userInput = UP
            elif spotx == blankx and spoty == blanky - 1:
                userInput = DOWN

    return userInput


#根据x,y坐标,获取方块在推盘中的位置-----【getinput】的子层
def getSpotClicked(board,x,y):
    for tilex in range(len(board)):
        for tiley in range(len(board[0])):
            left,top = getLeftTopOfTile(tilex,tiley)
            tileRect = pygame.Rect(left,top,BLOCKSIZE,BLOCKSIZE)
            if tileRect.collidepoint(x,y):
                return (tilex,tiley)
    return (None,None)


#获取空白拼图的位置
def getBlankPosition(board):
    for x in range(COL):
        for y in range(ROW):
            if board[x][y] == BLANK:
                return (x,y)


#输入处理
def processing(userInput,mainBord,msg):
    #判断游戏是否完成
    if mainBord == getStrartingBoard():
        msg = '完成'
    else:
        msg = "通过鼠标移动方块！"

    if userInput:
        #功能按钮
        if userInput == NEWGAME:
            intBoard = getStrartingBoard()
            mainBord = generateNewPuzzle(AUTOMOVE)
        else:
            slideAnimation(mainBord,userInput,msg,8)
            makeMove(mainBord,userInput)
    return mainBord,msg

#游戏退出
def checkForQuit():
    
    for event in pygame.event.get(QUIT):
        terminate()
    
    for event in pygame.event.get(KEYUP):
        if event.key == K_ESCAPE:
            terminate()
        pygame.event.post(event)

#终止操作
def terminate():
    pygame.quit()
    sys.exit()


#main()函数组织程序结构
def main():
    #全局变量
    global WINSET,FPSCLOCK,BASICFONT,STATITCSURF
    global NEW_SURF,NEW_RECT
    #初始化pygame模块
    pygame.init()
    #定义时钟对象
    FPSCLOCK = pygame.time.Clock()
    #定义字体对象
    BASICFONT = pygame.font.Font('STKAITI.TTF',25)




    WINSET, NEW_SURF, NEW_RECT = drawStaticWin()
    #将静态创就作为底板
    STATITCSURF = WINSET.copy()

    initBoard = getStrartingBoard()
    mainBoard = generateNewPuzzle(AUTOMOVE)
    #提示信息
    msg = None
    #游戏循环
    while True:
        FPSCLOCK.tick(FPS)
        drawBoard(mainBoard,msg)
        #更新显示
        pygame.display.update()
        checkForQuit()
        userInput = getInput(mainBoard)
        mainBoard,msg = processing(userInput,mainBoard,msg)

        
if __name__ == '__main__':
    main()
