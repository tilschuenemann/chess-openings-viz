fetch("../treeData_V2.json")
.then(response => {
   return response.json();
})
.then(data => {
    //console.log(data);
    //console.log("children" in data[0][Object.keys(data[0])[0]])

    data.map(function insertP(d,lastHM=0){

            return {
                id: d.id,
                path: d.path,
                name: d.name,
                hm: d.hm,
                children: ()=>{
                    d.children.array.forEach(element => {
                        if (element.hm > d.hm+1){
                            d.children={
                                id="None",
                                path="../img/placeholder.svg",
                                name="placeholder",
                                hm=d.hm+1,
                                children: element
                            }
                        }
                        });
                    
                }
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