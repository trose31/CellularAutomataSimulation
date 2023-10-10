import numpy as np
import pygame
import sys

def test(n):
    immune = immunised(n)
    
    cells = [[None]*n for i in range (n)]
    
    for i in range(0,n):
        for j in range(0,n):
            cells[i][j] = Cell(i,j,0,0)
    
    for (a,b) in immune:
        cells[a][b].state = 2
    
    startx = np.random.randint(0,n)
    starty = np.random.randint(0,n)
    cells[startx][starty].state = 1
    
    #cells = run(n,cells)
    cells = display(n,cells)
    print(score(n,cells))

def score(n, cells):
    score = 0
    for row in cells:
        for cell in row:
            if cell.state == 0:
                score+=1
    return score

def run(n, cells):
    while (checkend(n,cells)):
        cells = update(n, cells)
    return cells

def checkend(n, cells):
    flag = False
    for i in range (0,n):
        for j in range (0,n):
            if (cells[i][j].state==1):
                flag = True
    return flag

def display(n, cells):
    pygame.init()
    clock = pygame.time.Clock()
    
    screen_width = n*16
    screen_height = n*16
    screen = pygame.display.set_mode((screen_width,screen_height))
    pygame.display.set_caption('Population')

    bg_color = pygame.Color('grey12')
    
    healthy = (0,255,0)
    infected = (255,0,0)
    immune = (100,100,255)
    
    colours = [healthy,infected,immune]
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
                
        screen.fill(bg_color)
        
        for i in range (0,n):
            for j in range (0,n):
                x = 16*i
                y = 16*j
                col = cells[i][j].state
                square = pygame.Rect(x,y,15,15)
                pygame.draw.rect(screen,colours[col],square)
                
        pygame.display.flip()
        cells = update(n, cells)
        clock.tick(4)
        
    return cells
        
def update(n, cells):
    trans = 0.75
    stay = 1
    vuln = 0.7
    
    ncells = [[None]*n for i in range (n)]
    
    for i in range (0,n):
        for j in range (0,n):
            
            patient = cells[i][j]
            
            ncells[i][j] = Cell(patient.x, patient.y, patient.state, patient.duration)
            
            npatient = ncells[i][j]
            ran = np.random.uniform(0,1)
            
            if patient.state == 0:
                viralload = vir(i, j, cells, n)
                if ((ran*viralload*trans) > vuln):
                    npatient.state = 1
            
            if patient.state == 1:
                patient.duration+=1
                if (patient.duration > ran*5*stay):
                    npatient.duration = 0
                    npatient.state = 2
                
            
    return ncells
    
def vir(x, y, cells, n):
    neighbours = [(x-1,y-1),(x,y-1),(x+1,y-1),(x-1,y),(x+1,y),
                  (x-1,y+1),(x,y+1),(x+1,y+1)]
    sum = 0
    for (a,b) in neighbours:
        if ((0<=a) and (a < n) and (0<= b) and (b < n)):
            if (cells[a][b].state==1):
                sum+=1
    return sum
    
def immunised(n):
    immune = []
    natimmun = n*n/5
    i = 0 
    while (i < natimmun):
        x = np.random.randint(0,n)
        y = np.random.randint(0,n)
        immune.append((x,y))
        i += 1
        
    return immune

    
class Cell:
    def __init__(self, x, y, state, duration):
        self.x = int(x)
        self.y = int(y)
        self.duration = int(duration)
        self.state = int(state)
        
    def update(self, state):
        self.state = state
    
        
test(32)
