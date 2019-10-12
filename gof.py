import sys
import ast
import os, time

"""
*Init game field (board)
*Game field will be a matrix RowsxCols
"""
def initBoard(board, rows=10, cols=10):
    for i in range(rows):
        tmp = []
        for j in range(cols):
            tmp.append(0)
        board.append(tmp)

"""
*Configure board with config matrix
*:param config is a matrix that rappresent a pattern
*ex. [[0],[],[2,3]] there is a life in cell at row 0 and col 0, at row 2 and col 2 and 3
"""
def configBoard(board, config):
    for i in range(len(config)):
        for j in range(len(config[i])):
            board[i][config[i][j]] = 1

"""
*print board
*:param symbol_life what symbol show at living cell
*:param symbol_die what symbol show at free cell
"""
def printBoard(board,symbol_life=1,symbol_die=0):
    symbols = [symbol_die,symbol_life]
    for i in range(len(board)):
        for j in range(len(board[i])):
            print(symbols[int(board[i][j])], end="")
        print ("")

"""
*Make a generation
"""
def step(board):
    tmp = []
    initBoard(tmp,len(board),len(board))
    for i in range(len(board)):
        for j in range(len(board)):
            tmp[i][j] = check(board,i,j)
    return tmp

"""
*count of neighborns of cell at i,j
"""
def count(board,i,j):
    count = 0
    #Case NW
    if i == 0 and j == 0:
        for r in range(i,i+2):
            for c in range(j,j+2):
                if not(r==i and c==j):
                    if board[r][c] == 1:
                        count += 1
    #Case SW
    elif i == len(board)-1 and j == 0:
        for r in range(i-1,i+1):
            for c in range(j,j+2):
                if not(r==i and c==j):
                    if board[r][c] == 1:
                        count += 1
    #Case SE
    elif i == len(board)-1 and j == len(board[0])-1:
        for r in range(i-1,i+1):
            for c in range(j-1,j+1):
                if not(r==i and c==j):
                    if board[r][c] == 1:
                        count += 1
    #Case NE
    elif i == 0 and j == len(board[0])-1:
        for r in range(i,i+2):
            for c in range(j-1,j+1):
                if not(r==i and c==j):
                    if board[r][c] == 1:
                        count += 1

    #Case first row
    elif i == 0:
        for r in range(i,i+2):
            for c in range(j-1,j+2):
                if not(r==i and c==j):
                    if board[r][c] == 1:
                        count += 1
    #Case last row
    elif i == len(board)-1:
        for r in range(i-1,i+1):
            for c in range(j-1,j+2):
                if not(r==i and c==j):
                    if board[r][c] == 1:
                        count += 1
    #Case first col
    elif j == 0:
        for r in range(i-1,i+2):
            for c in range(j,j+2):
                if not(r==i and c==j):
                    if board[r][c] == 1:
                        count += 1
    #Case last col
    elif j == len(board[0])-1:
        for r in range(i-1,i+2):
            for c in range(j-1,j+1):
                if not(r==i and c==j):
                    if board[r][c] == 1:
                        count += 1

    #Case other
    else:
        for r in range(i-1,i+2):
            for c in range(j-1,j+2):
                if not(r==i and c==j):
                    if board[r][c] == 1:
                        count += 1
    return count

"""
*check if board is total free
"""
def checkIfFinish(board):
    for i in range(len(board)):
        for j in range(len(board[i])):
            if board[i][j] == 1:
                return False
    return True

"""
*Check if cell at i,j has to live or to die
*Return 0 if has to die
*Return 1 if has to live
"""
def check(board,i,j):
    #Case free space
    around = count(board,i,j)
    if board[i][j] == 0:
        if around == 3:
            return 1
        else:
            return 0
    #Case not free space
    else:
        if around == 2 or around == 3:
            return 1
        else:
            return 0

"""
*import a single pattern from file
"""
def importPattern(fileName,patternName="SNAKE"):
    with open(fileName,'r') as f:
        for line in f:
            tmp = line[line.find(";")+2:-1]
            if tmp == patternName:
                return line[:line.find(";")]

"""
*Create a dict with all written pattern in file
"""
def createDictPatterns(fileName):
    patterns = dict()
    with open(fileName,'r') as f:
        for line in f:
            name = str(line[line.find(";")+2:-1])
            pattern = line[:line.find(";")]
            patterns[name] = pattern
    return patterns

"""
*Add a pattern in config at indx,indy
"""
def addPattern(config,pattern,indx=0, indy=0):
    pattern = ast.literal_eval(pattern)
    for col in pattern:
        for i in range(len(col)):
            col[i] = col[i]+indy
        config[indx]=col
        indx += 1
    pass

"""
*Init a config file
*[[],[],[],[]]
"""
def createBaseConfig(board):
    config = []
    tmp = []
    for i in range(len(board)):
        config.append(tmp)
    return config

def createConfig (fileName, patterns, config):
    with open(fileName,'r') as f:
        for line in f:
            if "#" not in line[0]:
                split = line.split()
                patternName = split[0]
                x = int(split[1])
                y = int(split[2])
                addPattern(config, patterns[patternName], x, y)

"""
*Start the game
*:param sec refresh timing
*:param finish at what generation stop, 0 if forever
"""
def start(board,sec=1.0, finish=0):
    i = 1
    while (not (checkIfFinish(board)) and (i <= finish or finish == 0)):
        print("---------#" + str(i) + " gen------------")
        printBoard(board, "#", ".")
        board = step(board)
        time.sleep(sec)
        os.system('clear')
        i += 1

ROWS = 20
COLS = 20
SECS = 0.4
PATTERNSFILE = "patterns.ini"
CONFIGFILE = "field.ini"

helpMenu = "USAGE:\n"
helpMenu += "python3 gameoflife.py [[OPTIONS1],[...]]\n"
helpMenu += "OPTIONS:\n"
helpMenu += "--rows <n>: set field rows number\n"
helpMenu += "--cols <n>: set feld cols number\n"
helpMenu += "--config <file>: set file of config, see doc to see how to write\n"
helpMenu += "--patterns <file>: set file of patterns, see doc to see how to write\n"
helpMenu += "--secs <f>: set refesh frequency\n"
helpMenu += "--stop <n>: stop at n generation\n"
helpMenu += "example: python3 gof.py --rows20 --cols20 --config file.ini --patterns file2.ini --secs 0.2 --stop 10\n"
helpMenu += ""

opts = "".join(sys.argv).split("--")

for opt in opts:
    if "help" in opt:
        print(helpMenu)
        exit()
    if "rows" in opt:
        ROWS = int(opt[opt.index("rows")+4:])
    if "cols" in opt:
        COLS = int(opt[opt.index("cols")+4:])
    if "secs" in opt:
        SECS = float(opt[opt.index("secs")+4:])
    if "config" in opt:
        CONFIGFILE = str(opt[opt.index("config")+6:])
    if "patterns" in opt:
        PATTERNSFILE = int(opt[opt.index("patterns")+8:])
    if "stop" in opt:
        STOP = int(opt[opt.index("stop")+4:])

#INITS
patterns = createDictPatterns(PATTERNSFILE)
board = []
initBoard(board,ROWS,COLS)
myConfig = createBaseConfig(board)
createConfig(CONFIGFILE,patterns, myConfig)

#add configure to board and start game
configBoard(board, myConfig)
printBoard(board)
start(board,sec=SECS)
