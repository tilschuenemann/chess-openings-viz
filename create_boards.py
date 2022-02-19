import chess.pgn
import chess.svg
import chess
import pandas as pd
import io


df = pd.read_csv("openings_hierarchy.csv",sep=";")

for row in df.itertuples():

    tmp_pgn = io.StringIO(row.pgn)
    tmp_eco = str(row.eco)
    
    # there have been bad pgns throwing errors because of wrong syntax
    try:
        game = chess.pgn.read_game(tmp_pgn)

        board = game.board()
        
        for move in game.mainline_moves():
                board.push(move)
    except:
        print(row)



    board_svg = chess.svg.board(board, size = 400)

    f = open("img/"+tmp_eco+".svg","w")
    f.write(board_svg)
    f.close()

    # remainder for debugging errors
    print("success for "+tmp_eco)