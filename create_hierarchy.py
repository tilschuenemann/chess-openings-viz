import pandas as pd
import os

df = pd.read_csv("openings.csv",sep=";")

df = df.astype({"parent": str})

pgnc = list(df["pgn"])
eco_list = list(df["eco"])


def poplastMove(pgn_str):
    pgn = pgn_str.split()
    pgn.pop()
    if pgn[-1].isnumeric():
        pgn.pop()
    prev_mov = " ".join(pgn)
    return prev_mov



for index,pgn in enumerate(pgnc):
    print(index)
    # to evaluate parent the last move gets undone
    # eventually the move indicator also has to be removed
    
    isdone=False
    while (len(pgn) > 0) and (not isdone):
        pgn=poplastMove(pgn)

    # lookup eco of parent by previous move

        try:
            pgn_index = pgnc.index(pgn)
            print("Found: ", eco_list[pgn_index])
            df.at[index,"parent"] = eco_list[pgn_index]
            isdone = True
            break
        except ValueError:
            pgn_index = None


# sort df by pgn length to enable bottom up tree building
df.sort_values(by="pgn", key=lambda x: x.str.len(),inplace=True)

df.to_csv("openings_hierarchy.csv",sep=";",index=False)

