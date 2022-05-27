#from cairosvg import svg2png
import chess.pgn
import chess.svg
import chess
import pandas as pd
from treelib import Tree

import io
import os
import re

def pop_last_move(pgn: str) -> str:
    """Pops the last move from string with PGN notation. Works for move
    notations:
    1. d4
    1 d4

    Empty strings will be returned with "".

    Paramters
    -------
    pgn: str
        string with pgn notation

    Returns
    -------
    str
        string with pgn notation without the last move

    """

    if not (pgn and pgn.strip()):
        return ""

    pgn = pgn.split()

    pgn.pop()

    if pgn[-1].isnumeric() or pgn[-1].replace(".","").isnumeric():
        pgn.pop()

    prev_mov = " ".join(pgn)
    return prev_mov

def get_moves(pgn: str) -> int:
    """Calculates the amount of moves for a given string with PGN 
    notation.

    Paramters
    -------
    pgn: str
        string with pgn notation

    Returns
    -------
    int
        amount of half-moves
    """
    pgn = pgn.strip()
    return pgn.count(" ") + 1 - int(re.findall(r"\b\d+\b", pgn)[-1])

def gen_hierarchy(df: pd.DataFrame) -> pd.DataFrame:
    """Reads openings file, adds parent reference by pgn, adds half moves and writes to disk.
    
    If there is no index for the parent move, a placeholders gets added.

    After that, the lookup is performed again and the parent reference 
    gets added in another column.

    Parameters
    -------
    df: pd.DataFrame
        df with columns eco, pgn, name
    
    Returns 
    -------
    pd.DataFrame
        openings with move count, parent column and placeholders for
        missing entries
    """

    if set(['eco','pgn',"name"]).issubset(df.columns) is False:
        exit("malformed openings format: eco, pgn and name columns are needed")

    pgnc = list(df["pgn"])

    placeholders = pd.DataFrame()

    # add placeholders for all entries
    # TODO there is probably a better way to do this
    counter = 0
    for index, pgn in enumerate(pgnc):
        while len(pgn) > 0:
            pgn = pop_last_move(pgn)

            try:
                pgn_index = pgnc.index(pgn)
                break
            except ValueError:
                if pgn == "":
                    continue
                tmp = pd.DataFrame(
                    {"pgn": [pgn], "name": [f"placeholder-{counter}"], "eco": [counter]}
                )
                counter += 1
                placeholders = pd.concat([placeholders, tmp], axis=0, ignore_index=True)

    # remove duplicate pgns from placeholders
    placeholders.drop_duplicates(subset=["pgn"], keep="first", inplace=True)
    df = pd.concat([df, placeholders], axis=0, ignore_index=True)

    df["parent"] = df["pgn"].apply(lambda x : pop_last_move(x))
    df["move_count"] = df["pgn"].apply(lambda x: get_moves(x))

    # sort df by pgn length to enable bottom up tree building
    df.sort_values(by="pgn", key=lambda x: x.str.len(), inplace=True)

    return df


def gen_images(
    openings_hierarchy: str,
    output_folder: str,
    size: int,
    gen_svgs: bool,
    gen_pngs: bool,
):

    if gen_svgs is False and gen_pngs is False:
        exit("specify whether to generate svgs or pngs")
    elif os.path.exists(openings_hierarchy) is False:
        exit("openings hierarchy file doesnt exist")

    df = pd.read_csv(openings_hierarchy, sep=";")

    for row in df.itertuples():
        tmp_pgn = io.StringIO(row.pgn)
        tmp_eco = str(row.eco)

        # there have been bad pgns throwing errors because of wrong syntax
        try:
            game = chess.pgn.read_game(tmp_pgn)
            board = game.board()
            for move in game.mainline_moves():
                board.push(move)
        except Exception:
            print(f"failure for row: {row}")

        board_svg = chess.svg.board(board, size=size)

        if gen_svgs:
            f = open(f"{output_folder}/{tmp_eco}.svg", "w")
            f.write(board_svg)
            f.close()

        if gen_pngs:
            svg2png(bytestring=board_svg, write_to=f"{output_folder}/{tmp_eco}.png")


def gen_treetxt(openings_hierarchy: str, output_folder: str):
    df = pd.read_csv(openings_hierarchy, sep=";")

    df.sort_values(by="pgn", key=lambda x: x.str.len(), inplace=True)

    tree = Tree()

    eco_list = list(df["eco"])
    parent_list = list(df["parent"])

    tree.create_node("i am root", "root")

    for index, element in enumerate(eco_list):
        if pd.isna(parent_list[index]):
            tree.create_node(element, element, "root")
            continue

        tree.create_node(element, element, parent_list[index])

    tree.save2file(f"{output_folder}/tree.txt")


if __name__ == "__main__":

    openings = pd.read_csv("data/0-openings.csv",sep=";")
    new_openings = gen_hierarchy(openings)
    new_openings.to_csv("output/3-openings.csv",sep=";",index=False)


    #size = 400
    #gen_svgs = True
    #gen_pngs = True
    

    #openings_hierarchy = "output/1-openings_hierarchy.csv"
    #gen_images(openings_hierarchy, output_folder, size, gen_svgs, gen_pngs)
    #gen_treetxt(openings_hierarchy, output_folder)
