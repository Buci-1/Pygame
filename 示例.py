"""推盘游戏"""
import pygame, sys, random, time
from pygame.locals import *

"""定义变量"""
WINWIDTH = 640  # 窗口宽度
WINHEIGHT = 480  # 窗口高度
BLOCKSIZE = 80  # 定义矩形边长
ROW = 3
COL = 3
BLANK = None
# -----颜色预设-----
DARKGRAY = (60, 60, 60)
WHITE = (255, 255, 255)
YELLOW = (255, 255, 193)
GRAY = (128, 128, 128)
BRIGHTBLUE = (138, 228, 221)
# -----颜色变量-----
BLANKCOLOR = DARKGRAY  # 预设背景颜色
MSGCOLOR = WHITE  # 设置字体颜色
MSGBGCOLOR = YELLOW  # 按钮背景颜色
BTCOLOR = YELLOW  # 按钮底色
BTTEXTCOLOR = GRAY  # 选项字体颜色
BDCOLOR = BRIGHTBLUE
# ----静态常量----
UP = 'up'
DOWN = 'down'
LEFT = 'left'
RIGHT = 'right'
NEWGAME = 'newgame'
AUTOMOVE = random.randint(50, 100)
print(AUTOMOVE)
FPS = 60  # 预设频率
"""END"""


# -----------------------主程序------------------------------------------------
def main():
    global FPSCLOCK, WINSET, STATICSURF, BASICFONT
    global NEW_SURF, NEW_RECT
    global SOLVEDBOARD
    '''游戏流程，游戏的框架先放进去，然后填充'''
    pygame.init()  # 初始化所有模块
    FPSCLOCK = pygame.time.Clock()  # 创建clock模块
    BASICFONT = pygame.font.Font('STKAITI.TTF', 25)  # 创建字体对象
    # 初始化
    initBorad = getStartingBoard()
    print(initBorad)
    WINSET, NEW_SURF, NEW_RECT = drawStaticWin()
    STATICSURF = WINSET.copy()
    mainBoard = generateNewPuzzle(AUTOMOVE)
    msg = None
    while True:
        FPSCLOCK.tick(FPS)
        drawBoard(mainBoard, msg)  # 根据初始拼图信息与提示信息，绘制游戏界面
        pygame.display.update()
        # 判断是否结束游戏
        checkForQuit()  # 判断是否接收到终止信息
        userInput = getInput(mainBoard)  # 获取用户输入
        mainBoard, msg = processing(userInput, mainBoard, msg)


# -------------------------【-----------------顶层设计-----------------】---------------------------
# 现在这个函数更像是getIpnut()的功能，除去功能按键的部分的话完全就是了
# 修改一下，返回userInput变量，这个变量分为移动和功能两种
# 如果是移动，则是移动方向；如果是功能，则


def getInput(mainBoard):
    events = pygame.event.get()
    userInput = None
    for event in events:  # 时间处理循环
        if event.type == MOUSEBUTTONUP:  # 如果有鼠标点击后抬起事件，获取抬起时的坐标
            spotx, spoty = getSpotClicked(mainBoard, event.pos[0], event.pos[1])  # 获取点击位置与方块的关系
            if (spotx, spoty) == (None, None) and NEW_RECT.collidepoint(event.pos):  # 如果坐标不在拼图区域,且点击的是新游戏
                userInput = NEWGAME
            else:
                if mainBoard == getStartingBoard():  # 如果已经完成，点击非选项时不移动
                    break
                # 检查点击的位置是否在blank旁边
                blankx, blanky = getBlankPosition(mainBoard)
                if spotx == blankx + 1 and spoty == blanky:  # 如果在blank右边
                    userInput = LEFT  # 移动方向设为向左
                elif spotx == blankx - 1 and spoty == blanky:  # 在blank左边
                    userInput = RIGHT  # 往右边移动
                elif spotx == blankx and spoty == blanky - 1:  # 在blank上面
                    userInput = DOWN
                elif spotx == blankx and spoty == blanky + 1:  # 在blank下面
                    userInput = UP
    return userInput


def processing(userInput, mainBoard, msg):
    # 判断游戏是否完成
    if mainBoard == getStartingBoard():  # 如果当前拼图与初始拼图一致
        msg = 'finished！'
    else:
        msg = '通过鼠标移动方块。'

    if userInput:  # 先判断是否为有效操作
        # -----功能按钮-----
        if userInput == NEWGAME:
            initBoard = getStartingBoard()
            mainBoard = generateNewPuzzle(AUTOMOVE)
        # 方块移动
        else:
            slideAnimation(mainBoard, userInput, msg, 8)
            makeMove(mainBoard, userInput)
    return mainBoard, msg


# -----------------------【---View视图----】--------------------------
# 创建静态窗口
def drawStaticWin():
    # 窗口静态部分绘制
    winSet = pygame.display.set_mode((WINWIDTH, WINHEIGHT))  # 创建窗口
    pygame.display.set_caption('数字推盘')  # 设置名字
    image = pygame.image.load('Image\\androidparty.jpg')  # 绘制背景
    winSet.blit(image, (0, 0))
    # 按钮创建
    new_surf, new_rect = makeText('新游戏', BTTEXTCOLOR, BTCOLOR, WINWIDTH - 85, WINHEIGHT - 40)
    winSet.blit(new_surf, new_rect)
    return winSet, new_surf, new_rect


# 求推盘中的方块board[tilex,tiley)与窗口左和上的距离
def getLeftTopOfFile(tilex, tiley):
    # 拼图距离窗口边缘的距离
    xMargin = int((WINWIDTH - (BLOCKSIZE * COL + (COL - 1))) / 2)
    yMargin = int((WINHEIGHT - (BLOCKSIZE * ROW + (ROW - 1))) / 2)
    left = xMargin + (tilex * BLOCKSIZE) + (tilex - 1)
    top = yMargin + (tiley * BLOCKSIZE) + (tiley - 1)
    return left, top


# 创建字体图像并设置位置
def makeText(text, tColor, btColor, top, left):
    textSurf = BASICFONT.render(text, True, tColor, btColor)
    textRect = textSurf.get_rect()
    textRect.topleft = (top, left)
    return textSurf, textRect


# 绘制拼图块
# 在窗口的坐标(tilex,tiley)处绘制拼图块
def drawTile(tilex, tiley, number, adjx=0, adjy=0):
    left, top = getLeftTopOfFile(tilex, tiley)
    pygame.draw.rect(WINSET, BTCOLOR, (left + adjx, top + adjy, BLOCKSIZE, BLOCKSIZE))
    textSurf = BASICFONT.render(str(number), True, BTTEXTCOLOR)
    textRect = textSurf.get_rect()
    textRect.center = left + int(BLOCKSIZE / 2) + adjx, top + int(BLOCKSIZE / 2) + adjy
    WINSET.blit(textSurf, textRect)


# 绘制面板
def drawBoard(board, msg):
    WINSET.blit(STATICSURF, (0, 0))
    if msg:  # 提示信息
        msgSurf, msgRect = makeText(msg, MSGCOLOR, None, 5, 5)
        pygame.image.save(msgSurf, 'msg.png')
        imgSurf = pygame.image.load('msg.png')
        WINSET.blit(imgSurf, msgRect)
    for i in range(len(board)):  # 绘制推盘
        for j in range(len(board[0])):
            if board[i][j]:
                drawTile(i, j, board[i][j])
    left, top = getLeftTopOfFile(0, 0)
    width = COL * BLOCKSIZE
    height = ROW * BLOCKSIZE
    # 绘制外边框
    pygame.draw.rect(WINSET, BDCOLOR, (left - 5, top - 5, width + 11, height + 11), 4)


# 幻灯片动画
def slideAnimation(board, direction, msg, animationSpeed):
    blankx, blanky = getBlankPosition(board)
    # 因为是以列为单位的，所以和按行的不一样
    if direction == UP:
        movex = blankx
        movey = blanky + 1
    elif direction == DOWN:
        movex = blankx
        movey = blanky - 1
    elif direction == LEFT:
        movex = blankx + 1
        movey = blanky
    elif direction == RIGHT:
        movex = blankx - 1
        movey = blanky
    # 基础准备
    drawBoard(board, msg)
    BASECURF = WINSET.copy()  # SURFACE.blit()创建surface对象的复制
    # 在要移动的拼图块上绘制空白块
    moveLeft, moveTop = getLeftTopOfFile(movex, movey)
    pygame.draw.rect(BASECURF, BLANKCOLOR, (moveLeft, moveTop, BLOCKSIZE, BLOCKSIZE))

    # 在移动路径上连续绘制被移动的方块
    for i in range(0, BLOCKSIZE, animationSpeed):
        checkForQuit()
        WINSET.blit(BASECURF, (0, 0))
        if direction == UP:
            drawTile(movex, movey, board[movex][movey], 0, -i)
        if direction == DOWN:
            drawTile(movex, movey, board[movex][movey], 0, i)
        if direction == LEFT:
            drawTile(movex, movey, board[movex][movey], -i, 0)
        if direction == RIGHT:
            drawTile(movex, movey, board[movex][movey], i, 0)
        pygame.display.update()
        FPSCLOCK.tick(FPS)


# -----------------------【---子层设计----】--------------------------
# 根据x,y坐标，获取方块在拼图中的位置--------【getInput】的子层
def getSpotClicked(board, x, y):
    for tilex in range(len(board)):
        for tiley in range(len(board[0])):
            left, top = getLeftTopOfFile(tilex, tiley)
            tileRect = pygame.Rect(left, top, BLOCKSIZE, BLOCKSIZE)
            if tileRect.collidepoint(x, y):  # 若果哦x,y在碎方块内
                return tilex, tiley
    return None, None


# 生成顺序推盘---【processing】的子层-----算是数据生成，models部分
def getStartingBoard():
    # 例如row为3，col为3，则返回
    # returns [[1, 4, 7], [2, 5, 8], [3, 6, BLANK]]
    initBoard = []
    for i in range(COL):
        i = i + 1
        column = []
        for j in range(ROW):
            column.append(i)
            i += COL  # 因为按列添加而非顺序添加，所以加COL而非1
        initBoard.append(column)  # 添加整列到作为一个元素
    initBoard[ROW - 1][COL - 1] = BLANK
    return initBoard


# 交换拼图列表中的元素位置---------【processing】的子层
def makeMove(board, move):
    blankx, blanky = getBlankPosition(board)
    if move == UP:
        board[blankx][blanky], board[blankx][blanky + 1] = board[blankx][blanky + 1], board[blankx][blanky]
    elif move == DOWN:
        board[blankx][blanky], board[blankx][blanky - 1] = board[blankx][blanky - 1], board[blankx][blanky]
    elif move == LEFT:
        board[blankx][blanky], board[blankx + 1][blanky] = board[blankx + 1][blanky], board[blankx][blanky]
    elif move == RIGHT:
        board[blankx][blanky], board[blankx - 1][blanky] = board[blankx - 1][blanky], board[blankx][blanky]


# 生成新的拼图---【processing】子层
def generateNewPuzzle(numSlides):
    # 从起始配置中，使拼图移动numSlides次，并为这些移动设置动画
    mainBoard = getStartingBoard()  # 获取拼图矩阵
    drawBoard(mainBoard, '')
    lastMove = None
    for i in range(numSlides):
        move = getRandMove(mainBoard, lastMove)
        slideAnimation(mainBoard, move, '初始化...', animationSpeed=int(BLOCKSIZE / 3))
        makeMove(mainBoard, move)
        lastMove = move
    return mainBoard


# -----------------------【---第3层设计----】---------------------------------------
# 随机移动拼图
# 最近一次移动方向为上，或者向下不是有效移动---------generateNewPuzzle的子层
def getRandMove(board, lastMove=None):
    validMoves = [UP, DOWN, LEFT, RIGHT]
    # 从列表中删除被取消资格的移动方向
    if lastMove == UP or not isValidMove(board, DOWN):
        validMoves.remove(DOWN)
    if lastMove == DOWN or not isValidMove(board, UP):
        validMoves.remove(UP)
    if lastMove == LEFT or not isValidMove(board, RIGHT):
        validMoves.remove(RIGHT)
    if lastMove == RIGHT or not isValidMove(board, LEFT):
        validMoves.remove(LEFT)
    return random.choice(validMoves)


# -----------------------【---第4层设计----】---------------------------------------------
# 获取空白拼图块在拼图中的位置
def getBlankPosition(board):
    for x in range(COL):
        for y in range(ROW):
            if board[x][y] == BLANK:
                return (x, y)


# 根据空白块的位置和移动的方向判断本次移动是否为有效移动---genRandomMove()的子层
def isValidMove(board, move):
    blankx, blanky = getBlankPosition(board)
    if move == UP:
        return blanky != len(board[0]) - 1
    if move == DOWN:
        return blanky != 0
    if move == LEFT:
        return blankx != len(board) - 1
    if move == RIGHT:
        return blankx != 0


# --------------------游戏主循环控制--------------------
# 因为任何时候都可以退出，所有不应该放在游戏功能的事件处理中，
# 而应该放在游戏主循环中
# 退出判断
def checkForQuit():
    for event in pygame.event.get(QUIT):  # 获取所有会导致退出的事件
        terminate()  # 为任何退出事件执行退出操作
    for event in pygame.event.get(KEYUP):  # 接收所有按键ESC
        if event.key == K_ESCAPE:  # 如果安装了
            terminate()
        pygame.event.post(event)  # 发送事件到消息队列


def terminate():
    pygame.quit()
    sys.exit()


if __name__ == '__main__':
    main()
