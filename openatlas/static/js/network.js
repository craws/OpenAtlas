
var svg = d3.select('svg'), width = +svg.attr('width'), height = +svg.attr('height');
var nodes_data = graph['nodes']
var links_data = graph['links']
var simulation = d3.forceSimulation().nodes(nodes_data); // Set up the simulation

// Add forces, we're going to add a charge to each node, also going to add a centering force
simulation
    .force('charge_force', d3.forceManyBody())
    .force('center_force', d3.forceCenter(width/2, height/2));

// Draw circles for the nodes
var node = svg.append('g')
    .attr('class', 'nodes')
    .selectAll('circle')
    .data(nodes_data)
    .enter()
    .append('circle')
    .attr('r', 5)
    .attr('fill', 'red');

simulation.on('tick', tickActions); // add tick instructions

// Create the link force, we need the id accessor to use named sources and targets
var link_force = d3.forceLink(links_data).id(function(d) { return d.id; })

// Add a links force to the simulation, specify links in d3.forceLink argument
simulation.force('links', link_force)

// Draw lines for the links
var link = svg.append('g')
    .attr('class', 'links')
    .selectAll('line')
    .data(links_data)
    .enter().append('line')
    .attr('stroke-width', 2);

function tickActions() {
    // Update circle positions each tick of the simulation
    node
        .attr('cx', function(d) { return d.x; })
        .attr('cy', function(d) { return d.y; });

    // Update link positions
    // Simply tells one end of the line to follow one node around and the other end of the line to follow the other node around
    link
        .attr('x1', function(d) { return d.source.x; })
        .attr('y1', function(d) { return d.source.y; })
        .attr('x2', function(d) { return d.target.x; })
        .attr('y2', function(d) { return d.target.y; });

}
