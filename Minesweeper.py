import random
import re


#let's create a board object to represent the minesweeper game
#this is so that we can just say "create a new board object" ,or
#"dig here", " render this object for this game"
class Board :

    def __init__(self, dim_size , num_bombs):
        # let's keep track of these parameters they will be helpful later
        self.dim_size = dim_size
        self.num_bombs = num_bombs

        #let's create a board
        # we plant the bombs here
        self.board = self.make_new_board()
        self.assign_values_to_board()

        #initialize a set to keep track of which locations we have uncovered
        # we'll save (row , col ) tuples into this set
        self.dug = set()


    def assign_values_to_board(self):
        #now that we have bombs planted , let's assign a number 0-8 for all the empty spaces which represents how many neighbouring bombs there are.
        # We can precompute these and it will save us some effort checking what's around the board later on.
        for r in range(self.dim_size):
            for c in range(self.dim_size):
                if self.board[r][c]== "*":
                    continue
                self.board[r][c]= self.get_num_neighboring_bombs(r,c)

    def get_num_neighboring_bombs(self,row,column):
        # we iterate through each position and calculate the sum.
        # be careful to not go out of bound
        num_neighboring_bombs = 0
        for r in range(max(0,row-1) ,min(self.dim_size-1,(row+1))+1):
            for c in range(max(0,column-1), min(self.dim_size-1,(column+1))+1):
                if r == row and c == column:
                    continue # the position where we are checking
                if self.board[r][c] == '*':
                    num_neighboring_bombs +=1
        return num_neighboring_bombs

    def make_new_board(self):
        #Construct a new Board based on the dim size and num bombs
        # we should build the list of lists here
        # generate a new board
        board =[[None for _ in range(self.dim_size)] for _ in range(self.dim_size)]

        #plant the bombs
        # own code with no help *********************************
        # for bomb_planted in range(self.num_bombs):
        #     bomb_location = random.choice((self.dim_size*2)-1)
        #     while bomb_location == '*': # if a bomb is already planted
        #         bomb_location = random.randint(0,(self.dim_size ** 2) - 1)
        #     self.board[bomb_location//self.dim_size] [bomb_location% self.dim_size]= '*'
        # return board

        # kylie Ying's code
        #  planting the bombs
        bombs_planted = 0
        while bombs_planted < self.num_bombs:
            loc = random.randint(0, self.dim_size ** 2 - 1)  # return a random integer N such that a <= N <= b
            row = loc // self.dim_size  # we want the number of times dim_size goes into loc to tell us what row to look at
            col = loc % self.dim_size  # we want the remainder to tell us what index in that row to look at

            if board[row][col] == '*':
                # this means we've actually planted a bomb there already so keep going
                continue

            board[row][col] = '*'  # plant the bomb
            bombs_planted += 1

        return board

    def dig(self, row, column):
        #dig at that location
        #return True if successful dig , False if dug bomb

        # a few scenarios
        # hit bomb -> game over
        # dig at location with neighboring bombs -> finish dig
        # dig at location with no neighboring bombs -> recursively dig bobms
        self.dug.add((row, column)) # keep track that we dug here
        if self.board[row][column] == "*":
            return False
        elif self.board[row][column] >0:
            return True
        # if self.board == 0 ( None ) no bombs and no neighboring bombs
        for r in range(max(0, row - 1), min(self.dim_size - 1, (row + 1) )+1):
            for c in range(max(0, column - 1), min(self.dim_size - 1, (column + 1) )+1):
                if (r,c) in self.dug:
                    continue
                self.dig(r,c)
        return True
    #print function totally copied from kylie Ying's work
    def __str__(self): #print the board
        visible_board = [[None for _ in range(self.dim_size)] for _ in range(self.dim_size)]
        for row in range(self.dim_size):
            for col in range(self.dim_size):
                if (row,col) in self.dug:
                    visible_board[row][col] = str(self.board[row][col])
                else:
                    visible_board[row][col] = " "
            # put this together in a string
        string_rep = ''
        # get max column widths for printing
        widths = []
        for idx in range(self.dim_size):
            columns = map(lambda x: x[idx], visible_board)
            widths.append(
                len(
                    max(columns, key=len)
                )
            )

        # print the csv strings
        indices = [i for i in range(self.dim_size)]
        indices_row = '   '
        cells = []
        for idx, col in enumerate(indices):
            format = '%-' + str(widths[idx]) + "s"
            cells.append(format % (col))
        indices_row += '  '.join(cells)
        indices_row += '  \n'

        for i in range(len(visible_board)):
            row = visible_board[i]
            string_rep += f'{i} |'
            cells = []
            for idx, col in enumerate(row):
                format = '%-' + str(widths[idx]) + "s"
                cells.append(format % (col))
            string_rep += ' |'.join(cells)
            string_rep += ' |\n'

        str_len = int(len(string_rep) / self.dim_size)
        string_rep = indices_row + '-' * str_len + '\n' + string_rep + '-' * str_len

        return string_rep



def play (dim_size =10 , num_bombs = 10):
        #step 1 : create the board and plant the bombs
        board = Board(dim_size, num_bombs)

        #Step 2 : show the user the board and ask for where they want to dig
        #step 3a: if location is a bomb , show game over message
        # step 3b: if location is not a bomb dig recursively until each square is at least next to  a bomb
        #step 4 : repeat step 2 and 3a/b until there are no more places to dig
        safe = True
        while len(board.dug)< board.dim_size**2 - num_bombs:
            print(board)
            user_input = re.split(',(\\s)*', input("where would you like to dig? input as row ,col:"))
            row,col = int(user_input[0]),int(user_input[-1])
            if row < 0 or row >= board.dim_size or col < 0 or col >= dim_size:
                print("Invalid location. Try again.")
                continue
            safe = board.dig(row,col)
            if not safe:
                # digging a bomb
                break
        if safe :
            print("GG")
        else:
            print("Game over , you stepped on Foooking mine !")
            board.dug = [(r,c) for r in range(board.dim_size) for c in range(board.dim_size)]
            print(board)


if __name__ == '__main__': # good practice :)
    play()