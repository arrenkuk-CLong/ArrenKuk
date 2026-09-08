#Arren Kuk
#04/02/2026 #Last edited 05/03/2026
#    COLOURS = [
#        (237, 229, 218), #2
#        (238, 225, 201), #4
#        (243, 178, 122), #8
#        (246, 150, 101), #16
#        (247, 124, 95), #32
#        (247, 95, 59,), #64
#        (237, 208, 115), #128
#        (237, 204, 99), #256
#        (236, 202, 80), #512
# Problem = It merges from [0, 4, 4, 4] to [0, 0, 0, 8], not [0, 0, 4, 8], in other words - it deletes the num (bug FIXED)
#_____________________________________________________________________


import random
import os

class Gm2048:
    #Class initiate
    def __init__(self):
        self.grid = [[0] * 4 for _ in range(4)]  #Sets all tiles in range (loop 4 times) to be zero
        self.score = 0 
        self.reset_color = '\033[0m' #Text color 
        self.tile()  # Game starts with two tiles
        self.tile()  # call Func twice
    
    #Spawn Tiles
    def tile(self):
        empty = [(x, y) for x in range(4) for y in range(4) if self.grid[x][y] == 0] #scans the x(rows) and y(columns) once to see if their emptu (= 0)
        if empty:
            x, y = random.choice(empty) #Randomly choose a bracket/tile from collected empty tiles earlier
            if random.random() < 0.9: #Generates a rand num of either 2 (90% Chance), or 4 (10% Chance)
                self.grid[x][y] = 2 #access row and column
            else: 
                self.grid[x][y] = 4
                
    #Display Function
    def display(self):
        os.system('cls' if os.name == 'nt' else 'clear') #From import os - clears the terminal for every display iteration
        print(f"2048 Score: {self.score}{self.reset_color}")  # This should work if self.score is defined
        print("=" * 25)
        for row in self.grid:  #Outer loop - Rows
            print("|", end="")  #End parameter prevents newline
            for num in row:   #Inner loop - number and cells in row 
                if num == 0:    #Building grid based on all tiles == 0  
                    print("     |", end="") 
                else:
                    style = self.colors(num) #Set global variable  for color func
                    print(f"{style}{num:5}{self.reset_color}|", end="") #if not zero, the f-string will add the random value | Each tile holds exactly 5 spaces 
            print("\n" + "-" * 25) #prints underlines for each row in self.grid
        print("Controls: w(up) a(left) s(down) d(right) q(quit)") #Remind: Use .lower

    #Color text function
    def colors(self, num): #Colors stored using dictionary storing RGB Vals
        text_color = { 
            2: '\033[38;2;237;229;218m',   # (237, 229, 218)
            4: '\033[38;2;238;225;201m',   # (238, 225, 201)
            8: '\033[38;2;243;178;122m',   # (243, 178, 122)
            16: '\033[38;2;246;150;101m',  # (246, 150, 101)
            32: '\033[38;2;247;124;95m',   # (247, 124, 95)
            64: '\033[38;2;247;95;59m',    # (247, 95, 59)
            128: '\033[38;2;237;208;115m', # (237, 208, 115)
            256: '\033[38;2;237;204;99m',  # (237, 204, 99)
            512: '\033[38;2;236;202;80m',  # (236, 202, 80)
            1024: '\033[38;2;236;196;0m',  # Darker yellow
            2048: '\033[38;2;255;215;0m',  # Bright gold
            }
        
        text = text_color.get(num, '\033[38;2;249;246;242m') #Retreieves Default color
        return text

    #Moving Tiles (WASD)
    def move_tiles(self, direction):
        updated = False
        grid_copy = [row[:] for row in self.grid]

        if direction in ['w', 's']:  # Vertical moves
            for col in range(4):
                #Key w - normal merge logic
                col_vals = [self.grid[row][col] for row in range(4)]
                #Key s - reverse merge logic
                if direction == 's': 
                    col_vals.reverse() #Reverse the orientation to allow column for merge
                new_vals = self.merge_tile(col_vals)
                if direction == 's':
                    new_vals.reverse() #Restore the original orientation after new vals are merged/updated from the merge function
                for row in range(4): #Update all 4 rows
                    if self.grid[row][col] != new_vals[row]:
                        updated = True
                    self.grid[row][col] = new_vals[row] #Replace old with new vals
        
        else:  # Horizontal moves
            for row in range(4):
                #Key a - also normal merge logic
                row_vals = self.grid[row][:] #Create Copy of Row - avoid modifying original while processing
                #Key d - reverse merge logic
                if direction == 'd': #reverse of a
                    row_vals.reverse()
                new_vals = self.merge_tile(row_vals)
                if direction == 'd':
                    new_vals.reverse()
                for col in range(4): #Update all 4 cols
                    if self.grid[row][col] != new_vals[col]:
                        updated = True
                    self.grid[row][col] = new_vals[col]

        if updated and grid_copy != self.grid:
            self.tile()
            return True #Updated
        return False #Not updated

    #Merge Logic (l -> R, T -> B)
    def merge_tile(self, line):
        line = [x for x in line if x] #Filters and creates List of Non-Zeroes
        merge = [] 
          
        i = len(line) - 1 #Start processing from the last index
        while i >= 0:
            if i > 0 and line[i] == line[i-1]: #Check if the tile and the one before it has the same value (therefore can merge)
                merge.insert(0, line[i] * 2) #Double val & insert 
                self.score += line[i] * 2 
                i -= 2 #Skip the merge tile's indexes
            else:
                merge.insert(0, line[i]) #No Merge
                i -= 1 #Move unmerged tile by 1 (dec)
    
        
        #Fill Zeroes 
        merge.extend([0]*(4-len(merge))) #Extend to add the merged list directly to the real (display) list [0, 0, 0, 0] Restores line back to length 4
        return merge
    
    #MGame over detection
    def lose(self):
        if any(0 in row for row in self.grid): #Checks "any" empty cells - zero = empty 
            return False
        
        for row in range(4): #Checks for any possible merges (Even if all tiles are used. there can be possible merges)
            for col in range(4):
                val = self.grid[row][col]
                if (row < 3 and val == self.grid[row+1][col]) or \
                    (col < 3 and val == self.grid[row][col+1]): #Prevent index error 
                    return False
        return True

    def play(self): #player inputs
        while True:
            self.display()
            if self.lose():
                print("There are no more moves, take the L!")
                break
            move = ('') #Assign as String 
            move = input('\nMove: w, a, s, d: ').lower() 
            if move == 'q':
                print("Game has ended")
                break
            if move in ['w', 'a', 's', 'd']: #Validates input before initiating the function
                self.move_tiles(move)
            else:
                print("Invalid move")


# Game initiate (run the class)
if __name__ == "__main__":
    game = Gm2048()
    game.play()
