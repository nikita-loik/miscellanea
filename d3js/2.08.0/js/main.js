/*
*    main.js
*    Mastering Data Visualization with D3.js
*    2.8 - Activity: Your first visualization!
*/

// goo = d3.json('data/buildings.json').then(moo => {
//     moo.forEach(d => {
//         d.height = Number(d.height)
//     })
//     console.log(moo)
//     })
d3.json('data/buildings.json').then(function(json){
    data = data.concat(json);
    render(data);
});

console.log(data)
const svg = d3.select('#chart-area')
    .append('svg')
    .attr('width', 500)
    .attr('height', 500);

const foo = svg.selectAll('rect')
    // .data(moo)

foo.enter().append('rect')
    .attr('x', 50)
    .attr('y', 0)
    .attr('width', 50)
    .attr('height', 100)
    .attr('fill', 'blue')

// foo.enter().append('rect')
//     .attr('x', 50)
//     .attr('y', 0)
//     .attr('width', 50)
//     .attr('height', 100)
//     .attr('fill', 'red')
    // .attr('x', (_, i) => {
    //     console.log("Item: " + d, "Index: " + i)
    //     return (i * 50) + 50
    // })
    // .attr('y', (_, i) => {
    //     return 0
    // })
    // .attr('width', 50)
    // .attr('height', (d) => {d.height})
    // .attr('fill', 'blue')