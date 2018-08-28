
var svg = d3.select('svg')
    .attr('width', width)
    .attr('height', height);

var nodes_data = graph['nodes'];
var links_data = graph['links'];
var simulation = d3.forceSimulation().nodes(nodes_data); // Set up the simulation

// Add forces, we're going to add a charge to each node, also going to add a centering force
simulation
    .force('charge_force', d3.forceManyBody().strength(-100))
    .force('center_force', d3.forceCenter(width/2, height/2))
    .force("links", d3.forceLink(links_data).id(function(d) {return d.id;}));


simulation.on('tick', tickActions); // Add tick instructions
var g = svg.append("g").attr("class", "everything"); // Add encompassing group for the zoom

// Draw circles for the nodes
var node = g.append('g')
    .attr('class', 'nodes')
    .selectAll('circle')
    .data(nodes_data)
    .enter()
    .append('circle')
    .attr('r', 5)
    .style("fill", function (d) {return d.color;});

// Draw lines for the links
var link = g.append('g')
    .attr('class', 'links')
    .selectAll('line')
    .data(links_data)
    .enter().append('line')
    .attr('stroke-width', 2);

// Add drag capabilities
var drag_handler = d3.drag()
    .on("start", drag_start)
    .on("drag", drag_drag)
    .on("end", drag_end);

drag_handler(node);

var zoom_handler = d3.zoom().on("zoom", zoom_actions); // Add zoom capabilities
zoom_handler(svg);

/** Functions **/

// Drag functions, d is the node
function drag_start(d) {
 if (!d3.event.active) simulation.alphaTarget(0.3).restart();
    d.fx = d.x;
    d.fy = d.y;
}

// Make sure you can't drag the circle outside the box
function drag_drag(d) {
  d.fx = d3.event.x;
  d.fy = d3.event.y;
}

function drag_end(d) {
  if (!d3.event.active) simulation.alphaTarget(0);
  d.fx = null;
  d.fy = null;
}

// Zoom functions
function zoom_actions(){
    g.attr("transform", d3.event.transform)
}

function tickActions() {
    // Update circle positions each tick of the simulation
    node
        .attr("cx", function(d) { return d.x; })
        .attr("cy", function(d) { return d.y; });

    // Update link positions
    link
        .attr("x1", function(d) { return d.source.x; })
        .attr("y1", function(d) { return d.source.y; })
        .attr("x2", function(d) { return d.target.x; })
        .attr("y2", function(d) { return d.target.y; });
}
