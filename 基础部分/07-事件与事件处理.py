import pygame

#定义全局变量
WINWIDTH = 640
WINHEIGHT = 480
BGCOLOR = (3,54,73)
#预设频率
FPS = 60
#文本颜色
MSGCOLOR = (3,54,73)
MSGBGCOLOR = (255,255,193)
#定义矩形边长
BLOCKSIZE = 60
#创建游戏窗口
def main():
    #初始化所有模块
    pygame.init()
    #创建时钟对象
    FPSCLOCK = pygame.time.Clock()
    #创建窗体，Surface对象(画布)
    WINSET = pygame.display.set_mode((WINWIDTH,WINHEIGHT))
    #设置窗口标题
    pygame.display.set_caption('推盘游戏')
    
    #图形绘制
    #加载图片
    image = pygame.image.load('基础部分\\androidparty.jpg')
    #绘制绘图(图片对象，图标)
    WINSET.blit(image,(0,0))
    #文本绘制
    #创建字体对象
    BASICFONT = pygame.font.Font('基础部分\STKAITI.TTF',25)
    #渲染文本内容，生成一张图像
    msgSurf = BASICFONT.render('初始化...',True,MSGCOLOR,MSGBGCOLOR)
    #绘制窗口中
    WINSET.blit(msgSurf,(0,0))

    #渲染文本内容，生成一张图片
    autoSurf = BASICFONT.render('自动',True,MSGCOLOR,MSGBGCOLOR)
    #获取矩形属性
    autoRect = autoSurf.get_rect()
    #重置横纵坐标
    autoRect.x = WINWIDTH -autoRect.width -10
    autoRect.y = WINHEIGHT - autoRect.height - 10

    #绘制到窗口中
    WINSET.blit(autoSurf,autoRect)

    #调用copy()方法创建WINSET备份
    baseSurf = WINSET.copy()

    #创建矩形
    blockRect = pygame.Rect(0.5 * (WINWIDTH - BLOCKSIZE),
                            0.5 * (WINHEIGHT - BLOCKSIZE),
                            BLOCKSIZE,BLOCKSIZE)
    

    #绘制数字
    numSurf = BASICFONT.render('5',True,MSGCOLOR,MSGBGCOLOR)
    #获取数字矩形属性
    numRect = numSurf.get_rect()
    #重置横纵坐标
    numRect.x = blockRect.x + 0.5 * (BLOCKSIZE - numRect.width)
    numRect.y = blockRect.y + 0.5 * (BLOCKSIZE - numRect.height)
    
   

    #游戏循环
    while True:
        #绘制矩形
        pygame.draw.rect(WINSET,MSGBGCOLOR,blockRect)
        #添加数字
        WINSET.blit(numSurf,numRect)
         #刷新窗口
        pygame.display.update()
       
        #将备份覆盖到WINSET之上
        WINSET.blit(baseSurf,(0,0))

        #修改矩形和数字的横坐标
        blockRect.x += 1
        numRect.x += 1

        FPSCLOCK.tick(FPS)

        #获取当前时刻产生的所有事件列表
        for event in pygame.event.get():
             #判断按键被按下
             if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    print("上")
                elif event.key == pygame.K_DOWN:
                    print("下")
                elif event.key == pygame.K_ESCAPE:
                    #卸载所有模块
                    pygame.quit()
                    exit() 



if __name__ == '__main__':
    main()

