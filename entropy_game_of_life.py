import pygame, copy, math, random
pygame.init()
import numpy as np 
import itertools
import d4_Ehalf

##NOTE: make sure [WIN_WIDTH//PIXEL_SIZE mod d =0]
d = 4 #the dim used in computing the number of configurations and edges is d^2.
dim = d**2
PIXEL_SIZE = 10
WIN_WIDTH = 400
WIN_HEIGHT = 400

print("WIN_HEIGHT//PIXEL_SIZE:",WIN_HEIGHT//PIXEL_SIZE)
#Update every 2ms
REFRESH = 10
TARGET_FPS = 10
Color_screen=(49,150,100)
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

    def fun_line():
        #d = 8 #the dim used in computing the number of configurations and edges is d^2. 
        delta = d*PIXEL_SIZE
        x1 = d*PIXEL_SIZE
        y1 = d*PIXEL_SIZE
        while x1 in range(0,WIN_WIDTH) or y1 in range(0,WIN_HEIGHT):
            pygame.draw.line(screen, (239, 23, 23),  (x1, 0),(x1,WIN_HEIGHT))
            x1 = x1+ delta  
            pygame.draw.line(screen, (239, 23, 23),  (0, y1),(WIN_WIDTH, y1))
            y1 = y1+ delta
    screen = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
    screen.fill(Color_screen)

    background = pygame.Surface(screen.get_size())
    background = background.convert()
    background.fill((0, 0, 0))

    clock = pygame.time.Clock()

    isActive = True
    actionDown = False
    
    #computing the E matrix (half of it due to right->left symmetry)
    E=fun_edge(dim)
 
    final = pygame.time.get_ticks()
    grid = Grid() 
    debug = debugText(screen, clock)  
#Create the orginal grid pattern to be "special"
    #for x in range(  (WIN_WIDTH // (2*PIXEL_SIZE))-30 ,(WIN_WIDTH // (2*PIXEL_SIZE))+100):
        #for y in range((WIN_WIDTH // (2*PIXEL_SIZE))-30 ,(WIN_WIDTH // (2*PIXEL_SIZE))+100):
    for x in range(WIN_WIDTH//PIXEL_SIZE-30,WIN_WIDTH//PIXEL_SIZE-10):
        for y in range(WIN_HEIGHT//PIXEL_SIZE-30,WIN_HEIGHT//PIXEL_SIZE-10):
            if random.randint(0, 10) <=5:
                grid.setCell(x, y, True)
                drawSquare(background, x, y)
    screen.blit(background, (0, 0))
    fun_line()
    pygame.display.flip()
    while isActive:
        clock.tick(TARGET_FPS)
        newgrid = Grid()
##check the values of aliv beighbors with the original rules laterrr

        if pygame.time.get_ticks() - final > REFRESH:
            #print("pygame.time.get_ticks():",pygame.time.get_ticks())
            numActive = 0
            background.fill((0, 0, 0))
            for x in range(0, WIN_WIDTH // PIXEL_SIZE):
                for y in range(0, WIN_HEIGHT // PIXEL_SIZE):
	            #if the central cell is alive:		
                    if grid.getCell(x, y): 
                        #print("x:",x)
                        #print("y:",y)
                        if grid.countNeighbours(x, y) < 2:
                            newgrid.setCell(x, y, False)

                        elif grid.countNeighbours(x, y) <= 3:
                            newgrid.setCell(x, y, True)
                            numActive += 1
                            drawSquare(background, x, y)

                        elif grid.countNeighbours(x, y) >= 4:
                            newgrid.setCell(x, y, False)
                    #if the central cell is not alive:  
                    else:
                        if grid.countNeighbours(x, y) == 3:
                            newgrid.setCell(x, y, True)
                            numActive += 1
                            drawSquare(background, x, y)
            final = pygame.time.get_ticks() 
            #S_pop = population_entropy(grid,E)
            #print("S_pop:",S_pop)
            S_edge = edge_entropy(grid,E)
            print("S_edge:",S_edge)
        
        
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
        fun_line()
        #pygame.draw.line(screen, (239, 23, 23), (30, 0), (30, 480))
        pygame.display.flip()

#the following three functions are used for computing matrix E, used for computing Boltzmann entropy with
#macrostate=population, macrostate=number of edges, and macrostate=population and #number of edges

##for finding the number of configuration, given the dimension of the 
##coarse-grained box the number of alive cells. 
def fun_config(dim, s):
    list_config=[]
    rng=list(range(2))*dim
    l=set(i for i in itertools.combinations(rng, dim) if sum(i)==s)
    iter = int(np.sqrt(dim))
    for j in l:
        nested_l=[j[i:i+iter] for i in range(0, len(j), iter)]
        list_config.append(nested_l)
    return list_config
##for finding the number of edges for a given configuration
def number_edge(d):
    count=0
    #[number_edge(d[j]) for i in range(0,len(a)) for j in range(0,len(a)) if a[i][j]==1]
    for i in range(0,len(d)):
        for j in range(0,len(d)):
            if d[i][j]==1:
                if j+1<len(d) and d[i][j+1]==0: count+=1
                if i+1<len(d) and d[i+1][j]==0: count+=1 
                if i-1>=0 and d[i-1][j]==0: count+=1 
                if j-1>=0 and d[i][j-1]==0: count+=1 
    return count
##########update this part of the code
##outputting matrix E
def fun_edge(dim):
    print("np.sqrt(dim):",np.sqrt(dim))
    if np.sqrt(dim)==4:
        E=d4_Ehalf.matrix_four()
    else:
        N = int(np.sqrt(dim))
        E = np.zeros((2*N*(N+1)-4*N+1, int(dim/2)+1))#max number of edges in an NXN box:2*N*(N+1)-4*N+1
        extra_array = np.zeros(dim+1)
        #define matrix E: 
        #rows: number of configurations corresponding to having e edges.
        #coloumns: number of configurations corresponding to having l live_cells.
        #E[e edges][l live_cells]
        for live_cell in range(int(dim/2)+1):
            config=fun_config(dim, live_cell)
            for j in range(len(config)):
                number_edges = number_edge(config[j])
                E[number_edges][live_cell] += 1      
    print(E)
    return E


#computing entropy; macrostate = population of a given box with dim=d^2
#counting the number of alive cells in each box:
def population_entropy(grid,E):
    S_pop = 0
    for x in range(0, WIN_WIDTH//PIXEL_SIZE  , d):
        #print("x:",x)
        for y in range(0, WIN_HEIGHT//PIXEL_SIZE  , d):
            #print("y:",y)
            box_count = 0
            volume = 0
            for xx in range(x, x+d):
                #print("xx:",xx)
                for yy in range(y, y+d):
                    #print("yy:",yy)
                    if grid.getCell(xx, yy): box_count += 1 #counting the number of live cells in a given box
            #print("count:",box_count)
            if box_count <= (dim//2): volume = np.sum(E, axis=0)[box_count]
            else: volume = np.sum(E, axis=0)[dim-box_count]
            S_pop += np.log(volume)
    print("S_pop:",S_pop)
    return S_pop
    

#computing entropy; macrostate = population of a given box with dim=d^2
#counting the number of alive cells in each box:
def edge_entropy(grid,E):
    S_edge = 0
    for x in range(0, WIN_WIDTH//PIXEL_SIZE , d):
        for y in range(0, WIN_HEIGHT//PIXEL_SIZE , d):
            edge_count = 0
            volume = 0
            for xx in range(x, x+d):
                for yy in range(y, y+d):
                    if grid.getCell(xx, yy):
                        if yy+1<y+d and not grid.getCell(xx, yy+1): edge_count+=1
                        if xx+1<x+d and not grid.getCell(xx+1,yy): edge_count+=1 
                        if xx-1>=x and not grid.getCell(xx-1,yy): edge_count+=1
                        if yy-1>=y and not grid.getCell(xx, yy-1): edge_count+=1 
            if dim%2 == 0: volume = (np.sum(E, axis=1)[edge_count])*2 - E[edge_count][dim//2]
            else: volume = (np.sum(E, axis=1)[edge_count])*2 
            S_edge += np.log(volume)
    return S_edge














if __name__ == "__main__":
    main()
