import pandas as pd
import numpy as np


df = pd.DataFrame(
    [
        [np.nan, 2, np.nan, 0],
        [3, 4, np.nan, 1],
        [np.nan, np.nan, np.nan, np.nan],
        [np.nan, 3, np.nan, 4],
    ],
    columns=list("ABCD"),
)

df.at[0, "A"] = 100

print(df)
