/*
*    main.js
*    Mastering Data Visualization with D3.js
*    2.5 - Activity: Adding SVGs to the screen
*/

var bar = [25, 20, 10, 12, 15]
var ys = [50, 60, 70, 80, 90]

var svg = d3.select('#chart-area')
    .append('svg')
        .attr('width', 400)
        .attr('height', 400);

var foo = svg.selectAll('circle')
    .data(bar)

foo.enter().append('circle')
    // .attr('x', 50)
    // .attr('y', 0)
    // .attr('width', 50)
    // .attr('height', 100)
    // .attr('fill', 'blue')
    .attr('cx', (_, i) => {
        // console.log("Item: " + d, "Index: " + i)
        return (i * 50) + 50
    })
    .attr('cy', (_, i) => {
        return ys[i]
    })
    .attr('r', (d) => {
        // console.log(d)
        return d
    })
    .attr('fill', 'blue');