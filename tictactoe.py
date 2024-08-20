# -*- coding: utf-8 -*-
"""
Created on Tue Aug 20 15:52:16 2024
This is a tic tac toe game simulation
@author: eeblake
"""

#import libraries
import pandas as pd

#define functions
#create function to check if what the user inputs is valid (on the board) and the spot is empty
def check_valid(user_spot):
    if user_spot not in board_spots:
        current_value='NO'   
    else:
        current_value=board[user_spot[0]][int(user_spot[1])]
    while (current_value !=' ') or (user_spot not in board_spots):
         if user_spot not in board_spots:
            user_spot=input('Sorry that is not a valid spot. Please pick a valid spot:')
            if user_spot in board_spots:
               current_value=board[user_spot[0]][int(user_spot[1])]
         elif current_value !=' ':
            user_spot=input('Sorry that spot is already taken. Please pick an empty spot:')
            if user_spot in board_spots:
               current_value=board[user_spot[0]][int(user_spot[1])]
    return user_spot

#create function to place a X in a valid,empty spot on the board-Player1
def x_place_piece(user_spot):
    board.loc[int(user_spot[1]), user_spot[0]]='X'

#create function to place a O in a valid,empty spot on the board-Player2
def o_place_pice(user_spot):
    board.loc[int(user_spot[1]), user_spot[0]]='O'

#create function to see if someone has won
def check_win():
    #check columns for three in a row
    win=0
    for c in col:
        if (len(board[c].unique())==1) and ('X' in board[c].unique()):
            print('Game Over. Player 1 wins!')
            win=1
            break  
        elif (len(board[c].unique())==1) and ('O' in board[c].unique()):
            print('Game Over. Player 2 wins!')
            win=1
            break
           
    #check rows for three in a tow
    if win==0:
        for r in row:
            if (len(board.loc[r].unique())==1) and ('X' in board.loc[r].unique()):
                print('Game Over. Player 1 wins!')
                win=1
                break
            elif (len(board.loc[r].unique())==1) and ('O' in board.loc[r].unique()):
                print('Game Over. Player 2 wins!')
                win=1
                break
    #check diagnals for 3 in a row
    if win==0:
       if board['A'][1] =='X' and board['B'][2] =='X' and board['C'][3] =='X':
            print('Game Over. Player 1 wins!')
            win=1
       elif board['A'][1] =='O' and board['B'][2] =='O' and board['C'][3] =='O':
            print('Game Over. Player 2 wins!')
            win=1
       elif board['A'][3] =='X' and board['B'][2] =='X' and board['C'][1] =='X':
            print('Game Over. Player 1 wins!')
            win=1
       elif board['A'][3] =='O' and board['B'][2] =='O' and board['C'][1] =='O':
            print('Game Over. Player 2 wins!')
            win=1
    return win

#initialize 3x3 tic tac toe board
board=pd.DataFrame(columns=['A','B','C'],index=range(1,4)).fillna(' ')
print(board)

#get a list of spots on the board
col=list(board.columns)
row=list(board.index)
board_spots = [x+str(y) for x in col for y in row]

#initialize win and number of spots avaialable variables
win=0
num_avail=len(board_spots)

while win==0 or num_avail<=0:
    #have player 1 pick a position and check if its valid,place on baord
    player_1=input('Player 1 pick a position:')
    player_1_move=check_valid(player_1) #check if spot is valid and empty
    x_place_piece(player_1_move) #place X on spot
    print(board)
    win=check_win() #check win
    #stop game if someone has won
    if win==1:
        break
    #if no one has won take a spot away from avaiable spots
    num_avail-=1

    #if there are still spots available get Player 2 inputs
    if num_avail >0:
        #have player 2 pick a position and check if its valid, place on board
        player_2=input('Player 2 pick a position:') 
        player_2_move=check_valid(player_2) #check if spot is valid and empty
        o_place_pice(player_2_move) #place O on spot
        print(board)
        win=check_win() #check win
        #stop game if someone has won
        if win==1:
            break
        #if no one has won take a spot away from avaiable spots
        num_avail-=1
    #if there are no more avaiable spots on the board and no one has won, it is a tie and end game
    if num_avail==0 and win==0:
        print('Game Over, it is a Tie!')
        break
