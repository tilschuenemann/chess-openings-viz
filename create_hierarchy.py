import pandas as pd
import os

df = pd.read_csv("openings.csv",sep=";")

pgnc = list(df["pgn"])
eco_list = list(df["eco"])

for index,row in enumerate(pgnc):
    
    # to evaluate parent the last move gets undone
    # eventually the move indicator also has to be removed
    pgn = row.split()
    pgn.pop()
    
    if pgn[-1].isnumeric():
        pgn.pop()

    prev_mov = " ".join(pgn)
    
    # lookup eco of parent by previous move

    try:
        pgn_index = pgnc.index(prev_mov)
        df.at[index,"parent"] = eco_list[pgn_index]
    except ValueError:
        pgn_index = None


# sort df by pgn length to enable bottom up tree building
df.sort_values(by="pgn", key=lambda x: x.str.len(),inplace=True)

df.to_csv("openings_hierarchy.csv",sep=";",index=False)