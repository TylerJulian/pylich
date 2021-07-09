import chess
import lichess.api
import berserk
def main():
    #requires a api token from https://lichess.org/account/oauth/token
    #create a file named lichess.token and copy your api token into it.
    with open('./lichess.token') as f:
        token = f.read()

    #connects to lichess using lichess.
    session = berserk.TokenSession(token)
    client = berserk.Client(session)




    #board = chess.Board()
    #print(board)



if __name__ == "__main__":
    main()