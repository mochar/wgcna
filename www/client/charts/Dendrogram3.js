import { drawAxis, scaleRadial } from 'charts/Functions'

import { selectAll, select, mouse } from 'd3-selection'
import { scaleLinear, scalePoint, scaleQuantize } from 'd3-scale'
import { min, max } from 'd3-array'
import { lineRadial, arc } from 'd3-shape'
import { ribbon } from 'd3-chord'
const d3 = { selectAll, select, mouse, scaleLinear, scalePoint, scaleQuantize, min, max, lineRadial, arc, ribbon }

function flatten(array) {
    return Array.prototype.concat(...array)
}

function dendrogram(settings) {

    let chart = {}

    chart.settings = {
        data: null,
        corrs: null,
        names: null,
        ids: null,
        ratio: null,
        selector: null
    }
    for (var setting in settings) {
        chart.settings[setting] = settings[setting]
    }

    chart.data = chart.settings.data
    chart.corrs = chart.settings.corrs
    chart.names = chart.settings.names
    chart.ids = chart.settings.ids

    function toX(d, i) {
        const moduleName = chart.data[i].ordered[-d - 1]
        const projectId = chart.ids[i]
        return chart.x(`${projectId}_${moduleName}`)
    }

    function buildPositions(z) {
        const data = chart.data[z]

        const positions = data.merge.reduce((prev, cur, i) => {
            const x1 = cur[0] < 0 ? toX(cur[0], z) : prev[cur[0]-1]
            const x2 = cur[1] < 0 ? toX(cur[1], z) : prev[cur[1]-1]
            prev.push(x1 + ((x2 - x1) / 2))
            return prev
        }, [])

        return data.merge.map((d, i) => {
            // Element:
            //                    top
            //      left        -------------- right
            //      bottomleft  |            | 
            //                               | bottomright
            let left = d[0] < 0 ? toX(d[0], z) : positions[d[0]-1],
                top = chart.y(data.height[i]),
                right = d[1] < 0 ? toX(d[1], z) : positions[d[1]-1],
                bottomLeft = d[0] < 0 ? chart.y.range()[0] :
                                    chart.y(data.height[d[0]-1]),
                bottomRight = d[1] < 0 ? chart.y.range()[0] :
                                    chart.y(data.height[d[1]-1])
            return {left, top, right, bottomLeft, bottomRight}
        })
    }

    function nodeSelected() {
        const pier = d3.scaleLinear()
            .domain([Math.PI, -Math.PI])
            .range([0, 2 * Math.PI])
        const pos = d3.mouse(chart.g.node())
        const angle = pier(Math.atan2(pos[0], pos[1]))
        const radius = Math.sqrt(pos[0]**2 + pos[1]**2)
        const module = chart.xRev(angle)
        const [project, name] = module.split('_')
        const trees = d3.selectAll('g.tree')

        // Find modules correlated to the selected module
        /*
        const links = chart.corrs
            .filter(d => d.source === module || d.target == module)
            .map(d => {
                let o = {name: d.source === module ? d.target : d.source, value: d.value}
                o.angle = chart.x(o.name)
                return o
            })
        const text = chart.g.selectAll('text.name').data(links, d => d.name)
        text.exit().remove()
        text.enter().append('text')
            .text(d => d.value.toFixed(2))
            .attr('fill', d => d.value > 0 ? chart.color.range()[2] : chart.color.range()[0])
            .attr('alignment-baseline', 'central')
            .style('dominant-baseline', 'central')
            .each(function(d) {
                const radius = chart.innerRadius + 10
                const x_ = radius * Math.cos(d.angle - Math.PI * .5) + 2
                const y_ = radius * Math.sin(d.angle - Math.PI * .5) + 2

                let degree = angle * 180 / Math.PI - 90
                if (degree >= 180 && degree < 270) degree = -360 + degree

                if (degree <= 90 && degree >= -90) {
                    d3.select(this)
                        .attr('text-anchor', 'begin')
                        .attr('transform', `translate(${x_}, ${y_})rotate(${degree})`)
                } else {
                    degree = (degree > 0 ? -1 : 1) * (180 - Math.abs(degree))
                    d3.select(this)
                        .attr('text-anchor', 'end')
                        .attr('transform', `translate(${x_}, ${y_})rotate(${degree})`)
                }
            })
        */

        // Reset
        chart.g.selectAll('.module').interrupt().transition().attr('r', 2)
        // trees.interrupt().transition().attr('opacity', 1)

        //
        if (radius <= chart.innerRadius && name !== 'dummy') {
            chart.g.select(`#module_${module}`)
                .transition()
                .duration(100)
                .attr('r', 6)
            chart.g.select('text#selected-module')
                .text(name)

            // trees.filter(`:not(.tree_${project})`).transition().attr('opacity', 0.1)
        } else {
            chart.g.select('text#selected-module')
                .text('')
        }
    }

    !function init() {
        chart.height = 100
        chart.width = 100
        chart.margin = {top: 5, right: 5, bottom: 5, left: 5}
        chart.innerRadius = 275
        chart.outerRadius = 400

        
        chart.svg = d3.select(chart.settings.selector)
            .attr('transform', `translate(${chart.margin.left}, ${chart.margin.top})`)
            .on('mousemove', nodeSelected)
        chart.g = chart.svg.append('g')

        // x: projectid_modulename -> node position
        chart.allModules = flatten(chart.data.map((d, i) => {
            const projectId = chart.ids[i]
            return d.ordered
                .map(d2 => `${projectId}_${d2}`)
                .concat(`${projectId}_dummy`)
        }))
        chart.x = d3.scalePoint()
            .domain(chart.allModules)
            .range([0, 2 * Math.PI])
            .padding(.5)

        chart.xRev = d3.scaleQuantize()
            .domain([0, 2 * Math.PI])
            .range(chart.allModules)

        // y: dendrogram height -> radius
        const heights = flatten(chart.data.map(d => d.height))
        const heightMin = d3.min(heights)
        const heightMax = d3.max(heights)
        chart.y = d3.scaleLinear()
            // .domain([Math.max(heightMin - .1 * (heightMax - heightMin), 0), heightMax])
            .domain([heightMin, heightMax])
            .range([chart.innerRadius, chart.outerRadius])
        
        // 
        chart.color = d3.scaleLinear()
            .domain([-1, 0, 1])
            .range(['#C51D1D', 'white', 'steelblue'])

        // Axis
        chart.axis = chart.g.append('g')
            .attr('text-anchor', 'end')
        
        // Selected module
        chart.g.append('text')
            .attr('id', 'selected-module')
            .attr('x', 0)
            .attr('y', 0)
            .style('text-anchor', 'middle')
            .style('font-size', '1.1rem')
  
        resize()
        updateScales()
    }()

    function resize() {
        chart.width_ = Math.round($(chart.settings.selector).parent().width())
        chart.width = chart.width_ - chart.margin.left - chart.margin.right
        chart.height_ = Math.round(chart.settings.ratio * chart.width_)
        chart.height = chart.height_ - chart.margin.top - chart.margin.bottom
        chart.outerRadius = Math.min(chart.width, chart.height) * .5 * .9
        chart.innerRadius = chart.outerRadius / 1.4

        chart.svg.attr('width', chart.width_).attr('height', chart.height_)
        chart.g.attr('transform', `translate(${chart.width / 2}, ${chart.height / 2})`)
    }

    function updateScales() {
    }

    chart.update = function() {
        const line = d3.lineRadial()
        const arc = d3.arc()

        // Trees
        const tree = chart.g.append('g').selectAll('g.tree')
            .data(chart.data.map((d, z) => buildPositions(z)))
        tree.exit().remove()
        const treeEnter = tree.enter().append('g')
            .attr('class', (d, i) => `tree tree_${chart.ids[i]}`)
            .attr('stroke', 'black')

        const group = treeEnter.selectAll('.group').data(d => d)
        group.exit().remove()
        const groupEnter = group.enter().append('g')
            .attr('stroke-width', '1.5')
        groupEnter.append('path')
            .attr('d', d => line([[d.left, d.top], [d.left, d.bottomLeft]]))
        groupEnter.append('path')
            .attr('d', d => line([[d.right, d.top], [d.right, d.bottomRight]]))
        groupEnter.append('path')
            .attr('d', d => arc({innerRadius: d.top, outerRadius: d.top, startAngle: d.left, endAngle: d.right}))

        // Nodes
        const circle = chart.g.append('g').selectAll('circle.module')
            .data(chart.allModules, d => d)
        circle.exit().remove()
        circle.enter().append('circle')
            .filter(d => d.split('_')[1] !== 'dummy')
            .attr('id', d => `module_${d}`)
            .classed('module', true)
            .attr('transform', d => {
                const radius = chart.innerRadius - 15
                const angle = chart.x(d)
                const x_ = radius * Math.cos(angle - Math.PI * .5) + 1
                const y_ = radius * Math.sin(angle - Math.PI * .5) + 1
                return `translate(${x_}, ${y_})`
            })
            .attr('r', 2)
        
        // Links
        const ribbon = d3.ribbon().radius(chart.innerRadius - 25)
        const link = chart.g.append('g').selectAll('d').data(chart.corrs)
        link.exit().remove()
        link.enter().append('path')
            .attr('stroke', d => chart.color(d.value))
            .attr('stroke-width', 2)
            // .attr('opacity', d => Math.log(Math.abs(d.value)) + 1)
            // .attr('opacity', .8)
            .attr('d', d => {
                const sourceAngle = chart.x(d.source)
                const targetAngle = chart.x(d.target)
                return ribbon({
                    source: { startAngle: sourceAngle, endAngle: sourceAngle },
                    target: { startAngle: targetAngle, endAngle: targetAngle }
                })
            })
        
        // Axis
        const yTick = chart.axis
            .selectAll('g')
            // .data(chart.y.ticks(5).slice(1))
            .data(chart.y.ticks(5))
            .enter().append('g')
    
        yTick.append('circle')
            .attr('fill', 'none')
            .attr('stroke', '#000')
            .attr('stroke-opacity', 0.175)
            .attr('r', chart.y)

        yTick.append('text')
            .attr('x', -6)
            .attr('y', d => -chart.y(d))
            .attr('dy', '0.35em')
            .attr('fill', 'none')
            .attr('stroke', '#fff')
            .attr('stroke-width', 5)
            .text(chart.y.tickFormat(10, 's'));
      
        yTick.append('text')
            .attr('x', -6)
            .attr('y', d => -chart.y(d))
            .attr('dy', '0.35em')
            .text(chart.y.tickFormat(10, 's'));
      
        chart.axis.append('text')
            .attr('x', -6)
            .attr('y', d => -chart.y(chart.y.ticks(10).pop()))
            .attr('dy', '-1em')
            .text('Height')
        
        chart.axis.append('path')
            .attr('stroke', 'grey')
            .attr('stroke-width', 1)
            .attr('d', line([[0, chart.y.range()[0]], [0, chart.y.range()[1]]]))
        
        // Labels
        arc.innerRadius(chart.outerRadius+23).outerRadius(chart.outerRadius+23)
        const textPath = treeEnter.append('path')
            .attr('id', (d, i) => `path_${chart.ids[i]}`) 
            .attr('d', (d, i) => { 
                const id = chart.ids[i]
                const modules = chart.data[i].ordered
                const start = chart.x(`${id}_${modules[0]}`)
                const end = chart.x(`${id}_${modules[modules.length - 1]}`)
                return arc({startAngle: start, endAngle: end})
            })
            .attr('stroke-width', 0)
        
        treeEnter.append('text').append('textPath') 
            .attr('xlink:href', (d, i) => `#path_${chart.ids[i]}`)
            .style('text-anchor','middle') 
            .attr('startOffset', (d, i) => {
                const length = textPath._groups[0][i].getTotalLength()
                return length / 4
            })
            .text((d, i) => chart.names[i])

        return chart
    }

    return chart
}

export default dendrogram