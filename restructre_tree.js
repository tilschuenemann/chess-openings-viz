fetch("../tree_halfmoves.json")
.then(response => {
   return response.json();
})
.then(data => {
    console.log(data);
    console.log("children" in data[0][Object.keys(data[0])[0]])

    const data_new = data.map(function createDS(item){
        return {
            id: item[Object.keys(item)[0]].data.id,
            path: item[Object.keys(item)[0]].data.path,
            name: item[Object.keys(item)[0]].data.name,
            hm: item[Object.keys(item)[0]].data.hm,
            children:  ("children" in item[Object.keys(item)[0]] ? item[Object.keys(item)[0]].children.map(createDS) : [])
        }
    })

    console.log(data_new)
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