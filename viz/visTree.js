
const margin = {top: 20, right: 120, bottom: 20, left: 120}
const width = 5000 - margin.right - margin.left
const height = 1000 - margin.top - margin.bottom


fetch("../treeData.json")
.then(response => {
   return response.json();
})
.then(data => {


    const root = data[0];
    root.x0 = 0;
    root.y0 = width / 2;

    // setup svg 
    const svg = d3.select("body").append("svg")
            .attr("width", width + margin.right + margin.left)
            .attr("height", height + margin.top + margin.bottom)
        .append("g")
            .attr("transform", "translate(" + margin.left + "," + margin.top + ")");

    // generate tree layeout depending on node size
    var tree = d3.layout.tree()
        .nodeSize([22,35])
        .separation(function(a, b) { return (a.parent == b.parent ? 1.10 : 1.20); })

    


    var nodes = tree.nodes(root),
        links = tree.links(nodes);
    
    console.log(nodes)
    var line = d3.link(d3.curveBumpY)
        .x(function(d) { return d.x; })
        .y(function(d) { return d.y; })
        
    console.log(line)

    // render links with color depending on depth
    svg.selectAll("path")
        .data(links)
        .enter().append("path")
        .attr("d", line)
        .attr('transform', d => `translate(${width/2},0)`)
        .style("fill", "none")
        .style("stroke", function getColor(d) {
            if ("color" in d.source) {
                return d.source["color"];
            }
            else {
                if ("parent" in d.source) {
                    const data={
                        source: d.source.parent,
                    }
                    return getColor(data);
                }
                else {
                    return "DarkSalmon";
                }
            }
        })
        .style("stroke-width", "2px");
    
    const g = svg.selectAll('g')
        .data(nodes)
        .enter()
        .append('g')
        .attr('transform', d => `translate(${d.x+width/2},${d.y})`)

   g.append('text')
        .attr("transform", function(d) { return "translate(0,12)"; })
        .text(d => d.name.substring(0,20))
        .style("font-size", "0.2em")
        .attr("text-anchor", "middle")
        .attr("y","12")
    
    g.append('rect')
        .attr("width", "22")
        .attr("height", "22")
        .style("fill",function getColor(d) {
            if ("color" in d) {
                return d["color"];
            }
            else {
                if ("parent" in d) {
                    return getColor(d.parent);
                }
                else {
                    return "DarkSalmon";
                }
            }
        })
        .attr('transform', d => `translate(-11,-1)`)
        .attr("rx", "1")
        

    const board = g.append('image')
        .attr('xlink:href', d => "../" + d.path)
        .attr('width', 20)
        .attr('height',20)
        .attr("transform", function(d) { return "translate(-10,0)"; })
        .attr("outline", "6px black");
        
    
});


