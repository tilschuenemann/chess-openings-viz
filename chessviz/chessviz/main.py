from cairosvg import svg2png
import chess.pgn
import chess.svg
import chess
import networkx as nx
import numpy as np
import pandas as pd
from treelib import Tree
from PIL import Image

import io
import json
import random
import re


def get_lichess_openings() -> pd.DataFrame:
    """Downloads and merges public lichess opening datasets and writes them to
    disk.
    """
    lichess_openings = [
        "https://raw.githubusercontent.com/lichess-org/chess-openings/master/a.tsv",
        "https://raw.githubusercontent.com/lichess-org/chess-openings/master/b.tsv",
        "https://raw.githubusercontent.com/lichess-org/chess-openings/master/c.tsv",
        "https://raw.githubusercontent.com/lichess-org/chess-openings/master/d.tsv",
        "https://raw.githubusercontent.com/lichess-org/chess-openings/master/e.tsv",
    ]

    df = pd.DataFrame()

    for opening in lichess_openings:
        tmp = pd.read_csv(opening, sep="\t")
        df = pd.concat([df, tmp], axis=0)

    df.to_csv("../data/00-lichess-openings.csv", sep=";")
    return df


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

    if pgn[-1].isnumeric() or pgn[-1].replace(".", "").isnumeric():
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

    if set(["eco", "pgn", "name"]).issubset(df.columns) is False:
        exit("malformed openings format: eco, pgn and name columns are needed")

    pgnc = list(df["pgn"])

    placeholders = pd.DataFrame()

    # add placeholders for all entries
    # TODO there is probably a better way to do this
    for index, pgn in enumerate(pgnc):
        while len(pgn) > 0:
            pgn = pop_last_move(pgn)

            try:
                pgnc.index(pgn)
                break
            except ValueError:
                if pgn == "":
                    continue
                tmp = pd.DataFrame({"pgn": [pgn], "name": ["P00"], "eco": [None]})
                placeholders = pd.concat([placeholders, tmp], axis=0, ignore_index=True)

    # remove duplicate pgns from placeholders
    placeholders.drop_duplicates(subset=["pgn"], keep="first", inplace=True)
    df = pd.concat([df, placeholders], axis=0, ignore_index=True)

    df["parent"] = df["pgn"].apply(lambda x: pop_last_move(x))
    df["move_count"] = df["pgn"].apply(lambda x: get_moves(x))

    df["id"] = range(0, df["pgn"].size)
    df["path"] = df["id"].apply(lambda x: "img/" + str(x) + ".webp")

    # add root
    root_row = pd.DataFrame(
        {
            "eco": ["empty"],
            "name": ["empty"],
            "pgn": ["root"],
            "parent": ["empty"],
            "move_count": ["empty"],
            "path": ["empty"],
            "id": [-1],
        }
    )

    df = pd.concat([df, root_row], axis=0)
    df["parent"] = df["parent"].replace("", "root")

    df.sort_values(by="pgn", inplace=True)

    # add random color by eco
    def gen_random_color():
        # random.seed("d4")
        return "#%06x" % random.randint(0, 0xFFFFFF)

    eco_df = df.drop_duplicates(subset="eco", keep="first")
    eco_df["color"] = [gen_random_color() for i in range(len(eco_df.index))]
    eco_df.loc[eco_df["name"] == "P00", "color"] = None

    df = df.merge(eco_df[["eco", "color"]], how="left")
    df = df.fillna(method="ffill", axis=0)

    # sort df by pgn length to enable bottom up tree building
    df.sort_values(by="pgn", key=lambda x: x.str.len(), inplace=True)

    return df


def gen_images(
    df: pd.DataFrame,
    output_folder: str,
    size: int,
    gen_svgs: bool,
    gen_pngs: bool,
):
    """
    Generates SVG / PNG files for all PGNs found in the df and saves them to
    output_folder.

    Parameters
    -------
    df: pd.DataFrame
        input df with pgn column
    output_folder: str
        folder where images are saved to
    size: int
        final file dimensions in pixels
    gen_svgs: bool
        should SVG files be generated from the df?
    gen_pngs: bool
        should PNG files be generated from the df?
    """

    if gen_svgs is False and gen_pngs is False:
        exit("specify whether to generate svgs or pngs")

    for index, row in enumerate(df.itertuples()):
        tmp_pgn = io.StringIO(row.pgn)

        # there have been bad pgns throwing errors because of wrong syntax
        try:
            game = chess.pgn.read_game(tmp_pgn)
            board = game.board()
            for move in game.mainline_moves():
                board.push(move)
        except Exception:
            print(f"failure for row: {row}")

        if row.pgn == "root":
            continue
            # board_svg = chess.svg.board(board, size=size)
        else:
            last_move = board.peek()
            color = row.color
            highlight = {"square light lastmove": color, "square dark lastmove": color}

            board_svg = chess.svg.board(
                board, size=size, lastmove=last_move, colors=highlight
            )

        if gen_svgs:
            f = open(f"{output_folder}/{row.id:.0f}.svg", "w")
            f.write(board_svg)
            f.close()

        if gen_pngs:
            fname = f"{output_folder}/{row.id:.0f}"
            svg2png(bytestring=board_svg, write_to=fname + ".png")

            # img = Image.open(fname + ".png")
            # img.save(fname + ".webp", format="webp")


def gen_treetxt(df: pd.DataFrame, output_folder: str):
    # df.sort_values(by="pgn", key=lambda x: x.str.len(), inplace=True)

    tree = Tree()
    tree.create_node(tag="empty", identifier="empty")  # root node

    pgn_list = list(df["pgn"])
    parent_list = list(df["parent"])

    for index, element in enumerate(pgn_list):
        tree.create_node(tag=element, identifier=element, parent=parent_list[index])

    tree.save2file(f"{output_folder}/tree.txt")


def gen_treejson(df: pd.DataFrame, output_folder: str):
    if (
        set(["eco", "pgn", "name", "parent", "path", "move_count"]).issubset(df.columns)
        is False
    ):
        exit("malformed format")

    g = nx.from_pandas_edgelist(df, "parent", "pgn", create_using=nx.DiGraph())
    d = {
        v: {"id": e, "path": p, "name": n, "move_count": m, "index": i, "color": c}
        for v, e, n, p, m, i, c in zip(
            df.pgn, df.eco, df.name, df.path, df.move_count, df.id, df.color
        )
    }
    nx.set_node_attributes(g, d)
    out = [
        nx.tree_data(
            g,
            "root",
            ident="id",
            children="children",
        )
    ]

    with open(f"{output_folder}/tree.json", "w") as outfile:
        json.dump(out, outfile)


if __name__ == "__main__":
    lichess = get_lichess_openings()
    lichess = gen_hierarchy(lichess)
    lichess.to_csv("../output/04-lichess-openings.csv", sep=";", index=False)

    gen_treejson(lichess, "../output/")

    gen_images(lichess, "../output/img", 100, False, True)
    # gen_treetxt(lichess, "../output/")
