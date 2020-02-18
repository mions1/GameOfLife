# GUIDE

It's a simple game of life (see online) program made using python3.

There are 3 files:
- --gof.py: It's the game. Run with python3 gof.py for default settings. Run with --help option to see more options
- --patterns.ini: Configuration file where you can design your own blocks. Later, will show syntax
- --filed.ini: Configuraion file where you can design game's field, joining block desinged in patterns.ini and setting their position
    
Patterns.ini:
    <design>; <name>
    ex. [[0,1],[0,1]]; BLOCK
    
    <design> is a matrix. Outside list defined how much cols, inside list define where, in the col, there are "#"
        ex: 
            [[0,1],[1,2],[3]]; MY-BLOCK
            It's a block with 3 cols ([ [],[],[] ]) and 4 rows (because max y index is 3 (see last col))
            And it will be:
                  012
                0 #--
                1 ##-
                2 -#-
                3 --#
