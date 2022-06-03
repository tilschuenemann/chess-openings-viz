const nodeWidth = 40
const nodeHeight = 90
const highlightSize = 2

const maxNodesPerRow = 600

const imageDims = nodeWidth - highlightSize


const margin = { top: 20, right: 120, bottom: 20, left: 120 }


fetch("../tree.json")
    .then(response => {
        return response.json();
    })
    .then(data => {

        const root = data[0].children[7];
        root.x0 = 0;
        root.y0 = 0;//width / 2;

        // generate tree layeout depending on node size
        var tree = d3.layout.tree()
            .nodeSize([nodeWidth, nodeHeight])
            .separation(function (a, b) { return (a.parent == b.parent ? 1.1 : 1.1); })
        console.log(tree)

        var nodes = tree.nodes(root),
            links = tree.links(nodes);
        console.log(nodes)

        var x_max = d3.max(nodes, function(d) {
            return +d.x;
         })
        var x_min = d3.min(nodes, function(d) {
           return +d.x;
         });

        var y_max = d3.max(nodes, function(d) {
            return +d.y;
         })
        var y_min = d3.min(nodes, function(d) {
           return +d.y;
         });

        const boundingbox = {x_max: x_max, x_min:x_min,y_max:y_max,y_min:y_min }
        
        console.log(boundingbox)
        
        const width = (boundingbox.x_max-boundingbox.x_min) + nodeWidth // - margin.right - margin.left
        const height = (boundingbox.y_max-boundingbox.y_min) + nodeHeight
        const maxNodesPerCol =  d3.max(nodes, function(d) {
            return +d.depth+1;
          });



        var line = d3.link(d3.curveBumpY)
            .x(function (d) { return d.x; })
            .y(function (d) { return d.y; })
        console.log(line)

        // setup svg 
        const svg = d3.select("body").append("svg")
            .attr("width", width + margin.right + margin.left)
            .attr("height", height + margin.top + margin.bottom)
            .attr("id", "svg")
            .append("g")
            .attr("transform", "translate(" + margin.left + "," + margin.top + ")");


        svg.selectAll("rect")
            .data([...Array(maxNodesPerCol).keys()])
            .enter().append("rect")
            .attr("x", 0)
            .attr("y", function (d) { return d * nodeHeight; })
            .attr("width", width+nodeWidth)
            .attr("height", nodeHeight)
            .attr("fill", function (d) { return (d % 2 ? "#333333" : "#eeeeee") })
            //.attr('transform', (d) => `translate(0,0)`)
            //.attr('transform', (d) => `translate(0, -${ nodeHeight * 2.25})`)
            .style("stroke", (d) => d.color)
            .style("stroke-width", "1px")
            .style("opacity", "0.9")


        // render links with color depending on depth
        svg.selectAll("path")
            .data(links)
            .enter().append("path")
            .attr("d", line)
            .attr('transform', d => `translate(${Math.abs(boundingbox.x_min)+nodeWidth/2+nodeWidth/2}, ${2 * nodeHeight / 4})`)
            .style("fill", "none")
            .style("stroke", d => (d.source.color))
            .style("stroke-width", highlightSize + "px");

        const g = svg.selectAll('g')
            .data(nodes)
            .enter()
            .append('g')
            .attr('transform', d => `translate(${Math.abs(boundingbox.x_min)+nodeWidth/2+nodeWidth/2+d.x}, ${d.y + nodeHeight / 4})`)
            .style("opacity", d => (d.name == "P00" ? "0.5" : "1"))
            .style("fill-opacity", d => (d.name == "P00" ? "0.5" : "1"))

        g.append('text')
            //.attr("transform", function (d) { return "translate(0,12)"; })
            .attr("dy", 0)
            .text(d => d.name)
            .style("font-size", "0.3em")
            .attr("text-anchor", "middle")
            .attr("y", nodeHeight * 0.5)
            .style("visibility", d => (d.name == "P00" ? "hidden" : "visible"))
            .style("fill-opacity", d => (d.name == "P00" ? "0" : "1"))
            .call(wrap, 50);

        g.append('rect')
            .attr("width", nodeWidth)
            .attr("height", nodeWidth)
            .style("fill", (d) => (d.color))
            .attr('transform', d => "translate(-" + nodeWidth / 2 + ",-" + highlightSize / 2 + ")")
            .attr("rx", "1")
            .style("opacity", d => (d.name == "P00" ? "0.5" : "1"))
            .style("fill-opacity", d => (d.name == "P00" ? "0.5" : "1"))

        const board = g.append('image')
            .attr('xlink:href', d => "../" + d.path)
            .attr('width', imageDims)
            .attr('height', imageDims)
            .attr('loading', "lazy")
            .attr("transform", function (d) { return "translate(-" + imageDims / 2 + ",0)"; })
            .style("fill-opacity", d => (d.name == "P00" ? "0.5" : "1"))

            
        function wrap(text, width) {
            text.each(function () {
                var text = d3.select(this),
                    words = text.text().split(/\s+/).reverse(),
                    word,
                    line = [],
                    lineNumber = 0,
                    lineHeight = 1.1, // ems
                    y = text.attr("y"),
                    dy = parseFloat(text.attr("dy")),
                    tspan = text.text(null).append("tspan").attr("x", 0).attr("y", y).attr("dy", dy + "em");
                while (word = words.pop()) {
                    line.push(word);
                    tspan.text(line.join(" "));
                    if (tspan.node().getComputedTextLength() > width) {
                        line.pop();
                        tspan.text(line.join(" "));
                        line = [word];
                        tspan = text.append("tspan").attr("x", 0).attr("y", y).attr("dy", ++lineNumber * lineHeight + dy + "em").text(word);
                    }
                }
            });
        }

        /*
        const board = g.append('g')
            .attr('width', 20)
            .attr('height',20)
            .attr("transform", function(d) { return "translate(-10,0)"; })
            .attr("id", d=>d.id)
        
        
        nodes.forEach(function(d) {
            const dom_elements= d3.xml( "../" + d.path).mimeType("image/svg+xml").get(function(error, xml) {
                if (error) throw error;
                console.log(xml)
                //xml.setAttribute("category","food");
                document.getElementById(d.id).appendChild(xml.documentElement);
            });
        
        
        });*/

    });


