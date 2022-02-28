const { readFile, writeFile } = require('fs/promises');

const placeholderTemplate = {
  id: 'P00',
  path: './img/placeholder.svg',
  name: 'placeholder'
}

readFile("./treeData.json", "utf8")
  .then(data => {
    const tree = JSON.parse(data)

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
    /*
            function download(content, fileName, contentType) {
            var a = document.createElement("a");
            var file = new Blob([content], {type: contentType});
            a.href = URL.createObjectURL(file);
            a.download = fileName;
            a.click();
        }
        download(JSON.stringify(data_new), 'json.json', 'text/plain');*/
  });