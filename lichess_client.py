import chess
import berserk
import datetime
from time import sleep


def connect_client():
    #requires a api token from https://lichess.org/account/oauth/token
    #create a file named lichess.token and copy your api token into it.
    with open('./lichess.token') as f:
        token = f.read()

    #connects to lichess using lichess.
    session = berserk.TokenSession(token)
    client = berserk.Client(session)
    board = berserk.clients.Board(session)

    return session, client

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

    def start(self):
        if self.is_white == True:
            print("white")
        else:
            print("black")

        print(self.current_board)
        print("")
        command = input("your move?")
        self.client.board.make_move(self.id, command)
        current_move = chess.Move.from_uci(command)
        self.current_board.push(current_move)  # Make the move
        self.client.board.post_message(self.id,"hello")

        for event in self.stream:
            if event['type'] == 'gameState':
                print(self.current_board)
                self.current_board.push_uci(event["moves"].split()[-1])
                print(self.current_board)
                print("")
                sleep(10)
                self.client.board.resign_game(self.id)
                print("lost game")


