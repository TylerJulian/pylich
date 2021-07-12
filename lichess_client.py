import chess
import berserk
import datetime
from time import sleep

from lichess.api import current_game


def connect_client():
    #requires a api token from https://lichess.org/account/oauth/token
    #create a file named lichess.token and copy your api token into it.
    with open('./lichess.token') as f:
        token = f.read()

    #connects to lichess using lichess.
    session = berserk.TokenSession(token)
    client = berserk.clients.Client(session)
    board = berserk.clients.Board(session)

    return session, client, board

class game():
    def __init__(self, client, id, username, is_white, start_time):
        self.id = id
        self.client = client
        self.username = username
        self.is_white = is_white
        #0 is white, 1 is black
        self.clock = (datetime.datetime(2000, 1,1,0,start_time,0), datetime.datetime(2000, 1,1,0,start_time,0))
        self.current_board = chess.Board()
        self.stream = self.client.board.stream_game_state(self.id)
        self.current_command = ""
        self.your_turn = False
        self.turn_count = 0

    def start(self):
        if self.is_white == True:
            self.your_turn = True
            print("white")
        else:
            self.your_turn = False
            print("black")
        self.update_display()
        for event in self.stream:
            print("loop")
            
            if event['type'] == 'gameState':
                print("gamestate")
                print(event["moves"])
                if(self.your_turn != True):
                    if(event["moves"].split()[-1] == self.current_command):
                        pass
                    else:
                        self.current_board.push_uci(event["moves"].split()[-1])
                        self.update_display()
                        self.turn_count = self.turn_count + 1
                        self.your_turn = True
                if(self.your_turn == True): 
                    self.parse_input()
                    self.update_display()
                    self.your_turn = False
                    self.turn_count = self.turn_count + 1


    def update_display(self):
        #prints the board and adds a gap between next state.
        print(self.current_board)
        print("")

    def parse_input(self):
        self.current_command = input("your move?")
        if(self.current_command == 'quit'):
            self.client.board.resign_game(self.id)
            exit()
        self.client.board.make_move(self.id, self.current_command)
        current_move = chess.Move.from_uci(self.current_command)
        self.current_board.push(current_move)  # Make the move
        self.client.board.post_message(self.id,"hello")
        self.update_display()