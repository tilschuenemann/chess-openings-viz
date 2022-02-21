from cmath import nan, pi
import pandas as pd
from treelib import Node, Tree

tree = Tree()

df=pd.read_csv("./openings_hierarchy.csv", sep=";")


tree.create_node("Root", "root")
for i in range(len(df)):
    if not pd.notna(df.iloc[i]['parent']):
        tree.create_node( df.iloc[i]['eco'], df.iloc[i]['eco'],parent= 'root',data={'id': df.iloc[i]['eco'], 'path': './img/'+df.iloc[i]['eco']+'.svg', 'name': df.iloc[i]['name']})
    else:
        tree.create_node( df.iloc[i]['eco'], df.iloc[i]['eco'],parent= df.iloc[i]['parent'],data={'id':df.iloc[i]['eco'], 'path': './img/'+df.iloc[i]['eco']+'.svg', 'name': df.iloc[i]['name']})
        
tree.show()

#print(tree.to_dict(with_data=True))
# save as json
with open("tree.json", "w") as f:
   f.write(tree.to_json(with_data=True))

# save tree to txt file
#tree.save2file('tree.txt')

