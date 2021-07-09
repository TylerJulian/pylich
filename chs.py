from time import sleep
import chess
import berserk
from lichess.api import current_game, user
import lichess_client
from lichess.format import PGN, SINGLE_PGN, PYCHESS
import datetime

def main():
    #connect to lichess
    session, client = lichess_client.connect_client()
    # get username
    info = client.account.get()
    username = info['id']
    print('Your user id: ', username)
    
    print("Press enter to start")
    input()
    print("waiting for challenge")

    for event in client.board.stream_incoming_events():
        if event['type'] == 'challenge':
            id = event['challenge']['id']
            client.challenges.accept(id)
            print("challenge found")

            current_game = lichess_client.game(client, id, username, (id == client.games.export(event['challenge']['id'])['players']['white']['user']['id']),10)

            current_game.start()

            exit

            
            
        elif event['type'] == 'gameStart':
            print("gamestart")
            


            
    #board = chess.Board()
    #print(board)



if __name__ == "__main__":
    main()