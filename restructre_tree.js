const { readFile, writeFile } = require('fs/promises');

// Converts JSON stucture to d3 readable json file
// inserts placholder Templateboards where no consecutive halfemoves exists

const placeholderTemplate = {
  id: 'P00',
  path: './img/placeholder.svg',
  name: 'placeholder'
}

readFile("./tree_halfmoves.json", "utf8")
  .then(data => {
    
    
    const data_json = JSON.parse(data)
    const tree = data_json.map(function createDS_step_one(item){
      return {
          id: item[Object.keys(item)[0]].data.id,
          path: item[Object.keys(item)[0]].data.path,
          name: item[Object.keys(item)[0]].data.name,
          hm: item[Object.keys(item)[0]].data.hm,
          children:  ("children" in item[Object.keys(item)[0]] ? item[Object.keys(item)[0]].children.map(createDS_step_one) : [])
      }
    })


    //console.log(tree)


    const createDS = (parentHM) => (item) => {
      let { children, ...data } = item;

      const nPlaceholders = data.hm - 1 - parentHM

      return Array.from(Array(nPlaceholders >= 0 ? nPlaceholders : 0))
        .reduce((children, _, i) => {
          return [{
            ...placeholderTemplate,
            hm: data.hm - i - 1,
            children,
          }]
        }, [{ ...data, ...(children ? { children: children.map(createDS(data.hm)) } : {}) }])[0];
    }

    const treeNew = tree.map(createDS(-1))

    return writeFile("./treeDataNew.json", JSON.stringify(treeNew, null, 2))
  
  });