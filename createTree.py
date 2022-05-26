from cmath import nan, pi
import pandas as pd
from treelib import Node, Tree

tree = Tree()

df=pd.read_csv("./openings_hierarchy _halfmoves.csv", sep=";")


tree.create_node("Root", "root",data={'id': "None" ,"name": "Root",
    "hm": 0 , 'path': './img/root.svg'})
for i in range(len(df)):
    if not pd.notna(df.iloc[i]['parent']):
        tree.create_node( df.iloc[i]['eco'], df.iloc[i]['eco'],parent= 'root',data={'id': df.iloc[i]['eco'], 'path': './img/'+df.iloc[i]['eco']+'.svg', 'name': df.iloc[i]['name'],'hm': int(df.iloc[i]['halfmove'])})
    else:
        tree.create_node( df.iloc[i]['eco'], df.iloc[i]['eco'],parent= df.iloc[i]['parent'],data={'id':df.iloc[i]['eco'], 'path': './img/'+df.iloc[i]['eco']+'.svg', 'name': df.iloc[i]['name'],'hm': int(df.iloc[i]['halfmove'])})
        
#tree.show()
#print(tree.to_dict(with_data=True))
# save as json
with open("tree_halfmoves.json", "w") as f:
    f.write("[")
    f.write(tree.to_json(with_data=True))
    f.write("]")

# save tree to txt file
#tree.save2file('tree.txt')

