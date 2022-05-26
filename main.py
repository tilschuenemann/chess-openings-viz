import chess.pgn
import chess.svg
import chess
import pandas as pd
from treelib import Tree

import io
import os
import re
from cairosvg import svg2png


def gen_hierarchy(openings: str, output_folder: str):
    df = pd.read_csv(openings, sep=";")
    pgnc = list(df["pgn"])
    eco_list = list(df["eco"])

    # placeholders
    # placeholders = {"pgn": "", "name": "root-pl", "eco": -1}
    placeholders = pd.DataFrame()

    def pop_last_move(pgn: str):
        pgn = pgn.split()
        pgn.pop()

        if pgn[-1].isnumeric():
            pgn.pop()

        prev_mov = " ".join(pgn)
        return prev_mov

    # add placeholders for all entries
    counter = 0
    for index, pgn in enumerate(pgnc):
        while len(pgn) > 0:
            pgn = pop_last_move(pgn)

            try:
                pgn_index = pgnc.index(pgn)
                # df.at[index, "parent"] = eco_list[pgn_index]
                break
            except ValueError:
                # add placeholder
                # pl = {"pgn": pgn, "name": df["name"][index], "eco": -1}
                # placeholders.update(pl)
                if pgn == "":
                    continue
                tmp = pd.DataFrame(
                    {"pgn": [pgn], "name": [f"placeholder-{counter}"], "eco": [counter]}
                )
                counter += 1
                placeholders = pd.concat([placeholders, tmp], axis=0, ignore_index=True)
                # pgn_index = None

    # remove duplicate pgns from placeholders
    placeholders.drop_duplicates(subset=["pgn"], keep="first", inplace=True)

    df = pd.concat([df, placeholders], axis=0, ignore_index=True)
    df.sort_values(by="pgn", key=lambda x: x.str.len(), inplace=True)

    # add parent for all entries
    pgnc = list(df["pgn"])
    eco_list = list(df["eco"])

    for index, pgn in enumerate(pgnc):
        while len(pgn) > 0:
            pgn = pop_last_move(pgn)
            try:
                pgn_index = pgnc.index(pgn)
                df.at[index, "parent"] = eco_list[pgn_index]
            except ValueError:
                continue

    df["parent"] = df["parent"].fillna("root")

    # sort df by pgn length to enable bottom up tree building
    df.sort_values(by="pgn", key=lambda x: x.str.len(), inplace=True)

    # add half moves
    def get_hm(pgn: str):
        pgn = pgn.strip()
        return pgn.count(" ") + 1 - int(re.findall(r"\b[0-9]+\b", pgn)[-1])

    df["hm"] = df["pgn"].apply(lambda x: get_hm(x))

    df.to_csv(f"{output_folder}/1-openings_hierarchy.csv", sep=";", index=False)


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

    openings = "data/0-openings.csv"
    output_folder = "output/"
    size = 400
    gen_svgs = True
    gen_pngs = True
    gen_hierarchy(openings, output_folder)

    openings_hierarchy = "output/1-openings_hierarchy.csv"
    gen_images(openings_hierarchy, output_folder, size, gen_svgs, gen_pngs)
    gen_treetxt(openings_hierarchy, output_folder)
