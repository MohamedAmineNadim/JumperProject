import PIL, pygame
from pygame.locals import *
from PIL import Image, GifImagePlugin
from pygame.constants import QUIT

pygame.init()
clock = pygame.time.Clock()
fps = 8
screen = pygame.display.set_mode((1500,800))

img_list = []
img = Image.open("C:\\Users\\HP Victus\\Desktop\\GIFs\\GIF_Nature.gif")
frm = img.n_frames
for frame in range(0,frm):
    img.seek(frame)
    img_list.append(img)
    #img.save(f"C:\\Users\\HP Victus\\Desktop\\GIFs\\GIF_Nature{frame}.png")

class Animation():
    def __init__(self,x,y):
        self.animation = []
        self.index = 0
        for frame in range(0,7):
            image = pygame.image.load(f"C:\\Users\\HP Victus\\Desktop\\GIFs\\GIF_Nature{frame}.png")
            image= pygame.transform.scale(image,(800,650))
            self.animation.append(image)
        self.image=self.animation[self.index]
        self.rect=self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def disp(self,scn):
        self.image = self.animation[self.index%7]
        an.index+=1
        scn.blit(self.image,self.rect)



an = Animation(0,0)
run = True

iter = 0
while run:
    clock.tick(fps)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    an.disp(screen)
    print(iter)
    iter += 1
    pygame.display.update()

pygame.quit()