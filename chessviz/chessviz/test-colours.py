import pandas as pd
import random


df = pd.read_csv("../output/04-lichess-openings.csv", sep=";")

df2 = df.drop_duplicates(subset="eco", keep="first")


def gen_random_color():
    return "#%06x" % random.randint(0, 0xFFFFFF)


res = [gen_random_color() for i in range(len(df2.index))]

df2["color"] = res


df = df.merge(df2[["eco", "color"]], how="left")

print(df)
