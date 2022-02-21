
// import json file tree.json

//const fs = require('fs');
//const path = require('path');
//var d3 = require('d3');


//const treeData = JSON.parse(fs.readFileSync('./tree.json', 'utf8'));


//const svg = document.getElementById('tree')
//console.log(svg)
    // printing the tree datastructure
    //console.log(treeData);

    const height = 200;
    const width = 1000;



fetch("../tree.json")
.then(response => {
   return response.json();
})
.then(data => {
    

    const keys = Object.keys(data)[0];
    data = data[keys];
    console.log(data)

    var svg = d3.select("svg"),
    width = +svg.attr("width"),
    height = +svg.attr("height"),
    g = svg.append("g").attr("transform", "translate(32," + (height / 2) + ")");

    
    
});