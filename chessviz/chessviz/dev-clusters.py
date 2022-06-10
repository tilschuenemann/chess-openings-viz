#%%
import pandas as pd

df= pd.read_csv("./shared/lichess_hierarchy.csv",sep=";")
df2=  df[df["complex"] != "P00"].groupby(
    ["complex"], as_index=False).size().sort_values(by="size", ascending=False,axis="index").reset_index(drop="True")


test=  df.loc[df[df["complex"] != "P00"].groupby('complex').move_count.idxmin()].reset_index(drop="True")

result = df2.merge(test[["complex","pgn"]],on="complex",how="left")
print(result)

#df.to_json("../../shared/clusters.json", orient="records", indent=2)
# %%
