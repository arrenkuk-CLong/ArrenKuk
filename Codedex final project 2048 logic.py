#Codedex final project: 2048 - Logic
import pygame #Game Cg
import random #Random # placement
import math #Math of 2048

#game Settings/configuration----------------------------------------------------------------
pygame.init() 
FPS = 60
WIDTH,HEIGHT = 800, 800 #Size of the pygame
Rows = 4 #Rows 
Cols = 4 #Columns
GRID_HEIGHT = HEIGHT / Rows #200.0
GRID_WIDTH = WIDTH / Cols #200.0

Board_Color = (187, 173, 160) #Board background color
Thickness = 10
Background_Color = (205, 193, 180)
Font_Color = (119, 110, 101) #Black

Screen = pygame.display.set_mode((WIDTH,HEIGHT)) #Screen size
pygame.display.set_caption('2048') #Name of window

FONT = pygame.font.SysFont("arialbold", 60, bold=True) #Setting the font 
Move = 10 #Move velocity for blocks 


#Getting the tiles down----------------------------------------------------------------------------------------
class Tile:
    COLOURS = [
        (237, 229, 218), #2
        (238, 225, 201), #4
        (243, 178, 122), #8
        (246, 150, 101), #16
        (247, 124, 95), #32
        (247, 95, 59,), #64
        (237, 208, 115), #128
        (237, 204, 99), #256
        (236, 202, 80), #512
    ]

    def __init__(self, value, row, col): #self is the first parameter
        self.value = value
        self.row = row #4 rows
        self.col = col #4 columns
        self.x = col * GRID_WIDTH   
        self.y = row * GRID_HEIGHT 

    def get_color(self): #base the color on the value of the tile (using logs)
        color_index = int(math.log2(self.value)) - 1 #equation
        color = self.COLOURS[color_index]
        return color

    def draw(self, window): #draw text on top of the rectangle
        color = self.get_color()
        pygame.draw.rect(window, color, (self.x, self.y, GRID_WIDTH, GRID_HEIGHT))
        text = FONT.render(str(self.value), 1, Font_Color) #writes the text
        window.blit(text, 
                    (self.x + (GRID_WIDTH / 2 - text.get_width() / 2), 
                     self.y + (GRID_HEIGHT / 2 - text.get_height() / 2),
                     ),
                     ) #Set location of text

    def set_pos(self, ceil=False):
        if ceil: #round up
            self.row = math.ceil(self.y / GRID_HEIGHT) #row (height) y CEIL
            self.col = math.ceil(self.x / GRID_WIDTH) #col (width) x CEIL
        else: #round down
            self.row = math.floor(self.y / GRID_HEIGHT) # Row floor
            self.col = math.floor(self.x / GRID_WIDTH) # col floor

    def move(self, delta):
        self.x += delta[0]
        self.y += delta[1]

#Intitate game & drawing the grid------------------------------------------------------------------------------

def grid(screen): #Drawing everything on the screen
    #Rows
    for row in range(1, Rows): #1 bcz we don't need to draw the top line
        y = row * GRID_HEIGHT
        pygame.draw.line(screen, Board_Color, (0, y), (WIDTH, y), Thickness) #Line always starts at 0 (x) and Width (x)
    #Columns
    for col in range(1, Cols): #1 bcz we don't need to draw the top line
        x = col * GRID_WIDTH
        pygame.draw.line(screen, Board_Color, (x, 0), (x, HEIGHT), Thickness)

    pygame.draw.rect(screen, Board_Color, (0, 0, WIDTH, HEIGHT), Thickness) #rectangle, setting border thickness, dimensions, and position on pygame

def draw(screen, tiles): #Function draws everything on pygame
    screen.fill(Background_Color) #Background

    for tile in tiles.values(): #Draws the tile on top of the grid when loading in
        tile.draw(screen)

    grid(screen) #Grid/outline over the backgound
    pygame.display.update() #applies it to the screen (overides)



#random generation of tiles
def get_random_pos(tiles):
    row = None
    col = None
    while True: 
        row = random.randrange(0, Rows) #generates up to 3
        col = random.randrange(0, Cols)
        
        if f"{row}{col}" not in tiles: #detects whether or not a tile already exists in where this function is generating
            break

    return row, col

#Merging/control
#things to consider: Merging order and many differen scenarios
def move_tiles(screen, tiles, clock, direction):
    updated = True
    blocks = set()

    if direction == 'left':
        sort_func = lambda x: x.col #parameter and return col in same line
        reverse = False
        delta = (-Move, 0)
        boundary_check = lambda tile: tile.col == 0
        get_next_tile = lambda tile: tiles.get(f"{tile.row}{tile.col - 1}")
        merge_check = lambda tile, next_tile: tile.x > next_tile.x + Move #Only merge when the tile (being moved, has merged far enough into the other tile
        move_check = lambda tile, next_tile: tile.x > next_tile.x + GRID_WIDTH + Move
        ceil = True

    elif direction == 'right':
        sort_func = lambda x: x.col 
        reverse = True #Reverse order_
        delta = (Move, 0) #Positive cuz right direction
        boundary_check = lambda tile: tile.col == Cols - 1
        get_next_tile = lambda tile: tiles.get(f"{tile.row}{tile.col + 1}") #reverse
        merge_check = lambda tile, next_tile: tile.x > next_tile.x + Move 
        move_check = lambda tile, next_tile: tile.x + GRID_WIDTH + Move < next_tile.x + GRID_WIDTH + Move
        ceil = False #round down for right side


    elif direction == 'up':
        sort_func = lambda x: x.row
        reverse = False 
        delta = (0, -Move) #negative move velocity cause we moving up
        boundary_check = lambda tile: tile.row == 0
        get_next_tile = lambda tile: tiles.get(f"{tile.row - 1}{tile.col}") #reverse
        merge_check = lambda tile, next_tile: tile.y > next_tile.y + Move  #use y cause we moving up
        move_check = lambda tile, next_tile: tile.y > next_tile.y + GRID_HEIGHT + Move
        ceil = True #round down for right side 

    elif direction == 'down':
        sort_func = lambda x: x.row
        reverse = True 
        delta = (0, Move) #negative move velocity cause we moving up
        boundary_check = lambda tile: tile.row == Rows - 1 #boundary - 1
        get_next_tile = lambda tile: tiles.get(f"{tile.row + 1}{tile.col}") #Add 1 to move down a row
        merge_check = lambda tile, next_tile: tile.y < next_tile.y - Move  #use y cause we moving up
        move_check = lambda tile, next_tile: tile.y +GRID_HEIGHT + Move < next_tile.y 
        ceil = False #round down for right side 

    #Checks the whole merge & movement process
    while updated: 
        clock.tick(FPS) #tick by Frames
        updated = False
        sorted_tiles = sorted(tiles.values(), key=sort_func, reverse=reverse)

        for i, tile in enumerate(sorted_tiles): #Get index and tile object
            if boundary_check(tile): 
                continue

            next_tile = get_next_tile(tile) #getting the next tile
            if not next_tile:
                tile.move(delta)
            #if we do have a next tile: Then we do the merge operation below
            elif tile.value == next_tile.value and tile not in blocks and next_tile not in blocks:
                if merge_check(tile, next_tile): #checks if we are merging
                    tile.move(delta) #continues if yes
                else:
                    next_tile.value *= 2
                    sorted_tiles.pop(i) #index
                    blocks.add(next_tile) #makes sure it doesn't merge again
            elif move_check(tile, next_tile):
                tile.move(delta)
            else:
                if tile.value == 2048:
                    print("You win!")
                continue 


            tile.set_pos(ceil)
            updated = True #loops
        
        update_tiles(screen, tiles, sorted_tiles)
        draw(screen, tiles)
    end_move(tiles)

def end_move(tiles): #checks whether or not the games over
    if len(tiles) == 16: #the entire board is full of tiles that cant merge
        return "lost"
    
    row, col = get_random_pos(tiles)
    tiles[f"{row}{col}"] = Tile(random.choice([2, 4]), row, col)
    return "continue"



def update_tiles(screen, tiles, sorted_tiles):
    tiles.clear() #removes everything from dictionary
    for tile in sorted_tiles:
        tiles[f"{tile.row}{tile.col}"] = tile

def generate_tiles():
    tiles = {} #store tiles 
    for _ in range(2): 
        row, col = get_random_pos(tiles) #random row and random column for a tile to spawn
        tiles[f"{row}{col}"] = Tile(2, row, col) #converts the row and col# to a string --> tile object with a starting value of 2
    
    return tiles

#main loop
def main(screen):
    clock = pygame.time.Clock() #Set timer/stopwatch
    run = True

    tiles = generate_tiles()

    while run:
        clock.tick(FPS) #FPS = 60, it is universal

        #If event recieved is quit, then while loop breaks/ends
        for event in pygame.event.get(): #fetches all events from pygame
            if event.type == pygame.QUIT:
                run = False
                break

            if event.type == pygame.KEYDOWN: #Event (arrowkeys)
                if event.key == pygame.K_LEFT:
                    move_tiles(screen, tiles, clock, "left") #call the function (left)
                if event.key == pygame.K_RIGHT:
                    move_tiles(screen, tiles, clock, "right") #call the function (left)
                if event.key == pygame.K_UP:
                    move_tiles(screen, tiles, clock, "up") #call the function (left)
                if event.key == pygame.K_DOWN:
                    move_tiles(screen, tiles, clock, "down") #call the function (left)
        draw(screen, tiles)
        
    pygame.quit

#Driver Code
if __name__ == '__main__':
    main(Screen)
