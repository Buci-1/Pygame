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
    image = pygame.image.load('Image\\androidparty.jpg')
    #绘制绘图(图片对象，图标)
    WINSET.blit(image,(0,0))
    #文本绘制
    #创建字体对象
    BASICFONT = pygame.font.Font('STKAITI.TTF',25)
    #渲染文本内容，生成一张图像
    msgSurf = BASICFONT.render('初始化...',True,MSGCOLOR,MSGBGCOLOR)
    #绘制窗口中
    WINSET.blit(msgSurf,(0,0))
    
    #刷新窗口
    pygame.display.update()
    i=0
    #游戏循环
    while True:
        i += 1
        print(i)

        FPSCLOCK.tick(FPS)
    #卸载所有模块
    pygame.quit()
if __name__ == '__main__':
    main()

