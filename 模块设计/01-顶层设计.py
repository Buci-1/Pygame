from define import *
import pygame
from pygame.locals import *
import sys
#一.顶层设计
#生成推盘序列
def getStrartingBoard():
    return [['1','4','7'],['2','5','8'],['3','6','None']]

#静态界面
def drawStaticWin():
    
    #窗口
    WINSET = pygame.display.set_mode((WINWIDTH,WINHEIGHT))
    #名字
    pygame.display.set_caption('推盘游戏')
    #背景图片
    image = pygame.image.load('Pygame\\Image\\androidparty.jpg')
    #绘制到窗口中
    WINSET.blit(image,(0,0))
    
    #新游戏按钮
    new_surf, new_rect =  makeText('新游戏',BTCOLOR,BTTEXTCOLOR,WINHEIGHT-85,WINWIDTH - 40)
    #绘制窗口中
    WINSET.blit(new_surf,new_rect)
    #返回数据
    return WINSET,new_surf,new_rect



#
def makeText():
    pass



#动态界面
def drawBoard(board,msg):
    
    #提示信息
    if msg:
        msg_surf,msg_rect = makeText(msg,MSGCOLOR,None,5,5)
        pygame.image.save(msg_surf,'模块设计\msg.png')
        imaSurf = pygame.image.load('模块设计\msg.png')
        WINSET.blit(imaSurf,msg_rect)

    for i in range(len(board)):
        for j in range(len(board[0])):
            if board[i][j]:
                #绘制方块
                drawTile(i,j,board[i][j])
    #计算方块距离原点的横纵坐标
    left,top = getLeftTopOfTile(0,0)
    width,height = COL*BLOCKSIZE,ROW*BLOCKSIZE

    #绘制外边框
    pygame.draw.rect(WINSET,BDCOLOR,(left-5, top-5,width+11, height+11),4)

#
def drawTile():
    pass


def getLeftTopOfTile():
    pass

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
def getRandomMove():
    pass

#实现本次移动的动画
def slideAnimation():
    pass

#修改推盘序列中元素的序列
def makeMove():
    pass

#接受输入
def getInput(mainBoard):
    #获取事件列表
    events = pygame.event.get()
    #定义变量，保存返回值
    UserInput = None
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



def getSpotClicked():
    pass

def getBlankPosition():
    pass


#输入处理
def processing(userInput,mainBord,msg):
    pass

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
    global WINSET
    global NEW_SURF,NEW_RECT
    WINSET, NEW_SURF, NEW_RECT = drawStaticWin()
    initBoard = getStrartingBoard()
    mainBoard = generateNewPuzzle()
    #提示信息
    msg = None
    #游戏循环
    while True:
        drawBoard(mainBoard,msg)
        checkForQuit()
        userInput = getInput()
        mainBoard,msg = processing(userInput,mainBoard,msg)

        