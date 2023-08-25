import random
import pygame

pygame.init()
#Informations sur la fenêtre
tile_size = 32
nrow = 10
ncol = 10
pos = [(i,j) for i in range(nrow) for j in range(ncol)]
nbombs = 10
grid = []
bombs = []
timer = pygame.time.Clock()
up_border = 100
border = 16
width = 2*border + ncol*tile_size
height = up_border + nrow*tile_size + border
window = pygame.display.set_mode((width,height))
pygame.display.set_caption("Démineur")

img_empty = pygame.image.load("Images/empty.png")
img_flag = pygame.image.load("Images/flag.png")
img_grid = pygame.image.load("Images/Grid.png")
img_1 = pygame.image.load("Images/grid1.png")
img_2 = pygame.image.load("Images/grid2.png")
img_3 = pygame.image.load("Images/grid3.png")
img_4 = pygame.image.load("Images/grid4.png")
img_5 = pygame.image.load("Images/grid5.png")
img_6 = pygame.image.load("Images/grid6.png")
img_7 = pygame.image.load("Images/grid7.png")
img_8 = pygame.image.load("Images/grid8.png")
img_mine = pygame.image.load("Images/mine.png")
img_mineClicked = pygame.image.load("Images/mineClicked.png")
img_mineFalse = pygame.image.load("Images/mineFalse.png")

def write_txt(txt, size, v_offset=0):
    textbox = pygame.font.SysFont("Calibri",size,True).render(txt,True,(0,0,0))
    rect = textbox.get_rect()
    rect.center = (width/2,up_border/2+border/2+nrow*tile_size/2+v_offset)
    window.blit(textbox,rect)

class Tile:

    def __init__(self,row,col,number):
        self.row = row
        self.col = col
        self.flag = False
        self.clicked = False
        self.bombwrong = False
        self.bombclick = False
        self.number = number   #-1 pour bombe
        self.rect = pygame.Rect(border+self.col*tile_size,up_border+self.row*tile_size,tile_size,tile_size)

    def show_image(self):

        if self.bombwrong == True:
            window.blit(img_mineFalse,self.rect)
        
        else:
            if self.clicked:
                if self.number == -1:
                    if self.bombclick:
                        window.blit(img_mineClicked,self.rect)
                    else:
                        window.blit(img_mine,self.rect)
                
                elif self.number == 0:
                    window.blit(img_empty,self.rect)
                elif self.number == 1:
                    window.blit(img_1,self.rect)
                elif self.number == 2:
                    window.blit(img_2,self.rect)
                elif self.number == 3:
                    window.blit(img_3,self.rect)
                elif self.number == 4:
                    window.blit(img_4,self.rect)
                elif self.number == 5:
                    window.blit(img_5,self.rect)
                elif self.number == 6:
                    window.blit(img_6,self.rect)
                elif self.number == 7:
                    window.blit(img_7,self.rect)
                elif self.number == 8:
                    window.blit(img_8,self.rect)

            elif self.flag:
                window.blit(img_flag,self.rect)
            else:
                window.blit(img_grid,self.rect)

    
    def reveal(self):
        self.clicked = True
        if self.number == 0:
            for x in range(-1,2):
                if self.row+x >= 0 and self.row+x < nrow:
                    for y in range(-1,2):
                        if self.col+y >= 0 and self.col+y < ncol:
                            if not grid[self.row+x][self.col+y].clicked:
                                grid[self.row+x][self.col+y].reveal()
        
        elif self.number == -1:
            for bomb in bombs:
                if not grid[bomb[0]][bomb[1]].clicked:
                    grid[bomb[0]][bomb[1]].reveal()

    def update(self):
        if self.number != -1:
            for x in range(-1,2):
                if self.row+x >= 0 and self.row+x < nrow:
                    for y in range(-1,2):
                        if self.col+y >= 0 and self.col+y < ncol:
                            if grid[self.row+x][self.col+y].number == -1:
                                self.number += 1

def loop():
    n_clicks = 0
    state = "playing"
    global grid
    global bombs
    grid = []
    time = 0
    bombs_left = nbombs

    #Bombs generation
    
    bombs = random.sample(pos,nbombs)
    
    #Grid generation
    for i in range(nrow):
        line = []
        for j in range(ncol):
            if (i,j) in bombs:
                line.append(Tile(i,j,-1))
            else:
                line.append(Tile(i,j,0))
        
        grid.append(line)

    #Setting all numbers
    for row in grid:
        for tile in row:
            tile.update()

    #Loop
    while state != "exit":
        window.fill((192,192,192))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                state = "exit"
            
            if state == "lose" or state == "win":
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        state = "exit"
                        loop()
            
            else:
                if event.type == pygame.MOUSEBUTTONUP:
                    for row in grid:
                        for tile in row:
                            if tile.rect.collidepoint(event.pos):
                                if event.button == 1:
                                    #L-click
                                    n_clicks += 1
                                    tile.reveal()
                                    if n_clicks == 1 and tile.number != 0 and not tile.clicked:
                                        state = "exit"
                                        loop()
                                    
                                    elif tile.number == -1:
                                        state = "lose"
                                        tile.bombclick = True
                                
                                elif event.button == 3:
                                    if not tile.clicked:
                                        if tile.flag:
                                            tile.flag = False
                                            bombs_left += 1
                                        
                                        else:
                                            tile.flag = True
                                            bombs_left -= 1
        
        win = True
        for line in grid:
            for tile in line:
                tile.show_image()
                if tile.number != -1 and not tile.clicked:
                    win = False
        
        if win and state != "exit":
            state = "win"

        # Draw Texts
        if state != "lose" and state != "win":
            time += 1
        elif state == "lose":
            write_txt("Game Over", 50)
            write_txt("R pour rejouer", 35, 50)
            for i in grid:
                for j in i:
                    if j.flag and j.number != -1:
                        j.bombwrong = True
        else:
            write_txt("Gagné", 50)
            write_txt("R pour rejouer", 35, 50)
        
        s = "Timer:{0}".format(time//15)
        text = pygame.font.SysFont("Calibri", 20).render(s, True, (0, 0, 0))
        window.blit(text, (border, border))
        # Draw mine left
        text = pygame.font.SysFont("Calibri", 20).render("Bombs left:{0}".format(bombs_left), True, (0, 0, 0))
        window.blit(text, (width - border - 100, border))

        pygame.display.update()

        timer.tick(15)  

loop()
pygame.quit()
quit()