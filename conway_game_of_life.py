import pygame, copy, math, random
pygame.init()

PIXEL_SIZE = 5
WIN_WIDTH = 640
WIN_HEIGHT = 480

#Update every 2ms
REFRESH = 2
TARGET_FPS = 2

class Grid():
    def __init__(self, *args, **kwargs):
        self.grid = [[False for i in range(WIN_HEIGHT // PIXEL_SIZE)] for i in range(WIN_WIDTH // PIXEL_SIZE)]

    def setCell(self, x, y, stat):
        self.grid[x][y] = stat
        
    def getCell(self, x, y):
        return self.grid[x][y]
     
    def countNeighbours(self, x, y):
        try:
            count = 0
            if self.getCell(x-1,y-1): count += 1
            if self.getCell(x,y-1): count += 1
            if self.getCell(x+1,y-1): count += 1
            if self.getCell(x-1,y): count += 1
            if self.getCell(x+1,y): count += 1
            if self.getCell(x-1,y+1): count += 1
            if self.getCell(x,y+1): count += 1
            if self.getCell(x+1,y+1): count += 1
            
        except:
            return 0

        return count


class debugText():
    def __init__(self, screen, clock, active_cells = 0, *args, **kwargs):
        self.screen = screen
        self.clock = clock
        self.active = active_cells
        self.font = pygame.font.SysFont("Monospaced", 20)
    
    def printText(self):
        label_active = self.font.render("Cells: " + str(self.active), 1, (255,255,255))
        label_frameRate = self.font.render("FPS: " + str(self.clock.get_fps()), 1, (255,255,255))
        self.screen.blit(label_active, (8, 8))
        self.screen.blit(label_frameRate, (8, 22))

    def update(self, *args, **kwargs):
        self.screen = kwargs.get("screen",self.screen)
        self.clock = kwargs.get("clock",self.clock)
        self.active = kwargs.get("active",self.active)
 
 
def drawSquare(background, x, y):
    #Random cell colour
    colour = 255,255,255 
    #colour = random.randint(0,255), random.randint(0,255), random.randint(0,255)
    pygame.draw.rect(background, colour, (x * PIXEL_SIZE, y * PIXEL_SIZE, PIXEL_SIZE, PIXEL_SIZE))       


def main():
    screen = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
    
    background = pygame.Surface(screen.get_size())
    background = background.convert()
    background.fill((0, 0, 0))
    
    clock = pygame.time.Clock()

    isActive = True
    actionDown = False
    
    final = pygame.time.get_ticks()
    grid = Grid() 
    debug = debugText(screen, clock)  
    """
    #Create the orginal grid pattern randomly
    for x in range(0, WIN_WIDTH // PIXEL_SIZE):#CHANGED XRANGE TO RANGE
        for y in range(0, WIN_HEIGHT // PIXEL_SIZE):#CHANGED XRANGE TO RANGE
            if random.randint(0, 10) == 1:
                grid.setCell(x, y, True)
                drawSquare(background, x, y)
    """
#Create the orginal grid pattern to be "special"
    for x in range(  (WIN_WIDTH // (2*PIXEL_SIZE))-75 ,(WIN_WIDTH // (2*PIXEL_SIZE))+7 ):
        for y in range((WIN_WIDTH // (2*PIXEL_SIZE))-7 ,(WIN_WIDTH // (2*PIXEL_SIZE))+7):
            #if random.randint(0, 10) == 1:
            grid.setCell(x, y, True)
            drawSquare(background, x, y)

    screen.blit(background, (0, 0)) 
    pygame.display.flip()

    while isActive:
        clock.tick(TARGET_FPS)
        newgrid = Grid()

        if pygame.time.get_ticks() - final > REFRESH:
            numActive = 0
            background.fill((0, 0, 0))

            for x in range(0, WIN_WIDTH // PIXEL_SIZE):#CHANGED XRANGE TO RANGE
                for y in range(0, WIN_HEIGHT // PIXEL_SIZE):#CHANGED XRANGE TO RANGE
                    if grid.getCell(x, y):
                        if grid.countNeighbours(x, y) < 2:
                            newgrid.setCell(x, y, False)

                        elif grid.countNeighbours(x, y) <= 3:
                            newgrid.setCell(x, y, True)
                            numActive += 1
                            drawSquare(background, x, y)

                        elif grid.countNeighbours(x, y) >= 4:
                            newgrid.setCell(x, y, False)

                    else:
                        if grid.countNeighbours(x, y) == 3:
                            newgrid.setCell(x, y, True)
                            numActive += 1
                            drawSquare(background, x, y)

            final = pygame.time.get_ticks() 

        else:
            newgrid = grid
            
        debug.update(active = numActive)

        actionDown = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                isActive = False
                
            elif event.type == pygame.MOUSEBUTTONDOWN:
                actionDown = True

                while actionDown:
                    newgrid.setCell(pygame.mouse.get_pos()[0] / PIXEL_SIZE, 
                    	pygame.mouse.get_pos()[1] // PIXEL_SIZE, True)
                    	
                    drawSquare(background, pygame.mouse.get_pos()[0] / PIXEL_SIZE, 
                    	pygame.mouse.get_pos()[1] // PIXEL_SIZE)
                    
                    for event in pygame.event.get():
                        if event.type == pygame.MOUSEBUTTONUP:
                            actionDown = False
                    
                    screen.blit(background, (0, 0)) 
                    pygame.display.flip()

        #Draws the new grid
        grid = newgrid       

        #Updates screen
        screen.blit(background, (0, 0)) 
        debug.update(active = numActive)
        debug.printText()
        pygame.display.flip()
       
if __name__ == "__main__":
    main()
