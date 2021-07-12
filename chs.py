from time import sleep
import chess
import berserk
from lichess.api import current_game, user
import lichess_client
from lichess.format import PGN, SINGLE_PGN, PYCHESS
import datetime

def main():
    #connect to lichess
    session, client, board = lichess_client.connect_client()
    # get username
    info = client.account.get()
    username = info['id']
    print('Your user id: ', username)
    
    print("Which mode would you like to start with?")
    print("1: challenge")
    print("2: Rapid 10 min")
    print("3: classical 30 min")
    print("4: bots")
    mode = input()

    print("waiting for challenge")
    

    if (mode == '1'):
        for event in client.board.stream_incoming_events():
            if event['type'] == 'challenge':
                id = event['challenge']['id']
                client.challenges.accept(id)
                print("challenge found")

                current_game = lichess_client.game(client, id, username, (username == client.games.export(event['challenge']['id'])['players']['white']['user']['id']),10)

                current_game.start()

                exit()
    if (mode == '2'):
        test = board.stream_incoming_events()
        for event in test:
            print("searching")
            print(berserk.clients.Board.seek(client.board, 10, 0))
            print("found")
            print("game")
            if event['type'] == 'gameStart':
                id = event['game']['id']
                print("id: ", id)
                print("game found")

                current_game = lichess_client.game(client, id, username, (username == client.games.export(event['game']['id'])['players']['white']['user']['id']),10)

                current_game.start()

                exit()




            
    #board = chess.Board()
    #print(board)


if __name__ == "__main__":
    main()