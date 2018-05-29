import * as d3 from 'd3'
import { drawAxis, scaleRadial } from 'charts/Functions'

function dendrogram(settings) {

    let chart = {}

    chart.settings = {
        data: null,
        names: null,
        ratio: null,
        selector: null
    }
    for (var setting in settings) {
        chart.settings[setting] = settings[setting]
    }

    chart.data = chart.settings.data

    function toX(d, i) {
        // return chart.x[i](chart.data[i].labels[-d - 1]) + (chart.x[i].bandwidth() / 2)
        return chart.x[i](chart.data[i].ordered[-d - 1])
    }

    function buildPositions(z) {
        return chart.data[z].merge.reduce((prev, cur, i) => {
            const x1 = cur[0] < 0 ? toX(cur[0], z) : prev[cur[0]-1]
            const x2 = cur[1] < 0 ? toX(cur[1], z) : prev[cur[1]-1]
            prev.push(x1 + ((x2 - x1) / 2))
            return prev
        }, [])
    }

    !function init() {
        chart.height = 100
        chart.width = 100
        chart.margin = {top: 5, right: 5, bottom: 5, left: 5}
        chart.innerRadius = 275
        chart.outerRadius = 400

        chart.svg = d3.select(chart.settings.selector)
            .attr('transform', `translate(${chart.margin.left}, ${chart.margin.top})`)
        chart.g = chart.svg.append('g')

        // chart.x = chart.data.map(d => d3.scaleBand().paddingOuter(.6))
        chart.x = chart.data.map(d => d3.scalePoint().padding(.8))
        chart.y = chart.data.map(d => d3.scaleLinear().interpolate(d3.interpolateRound))

        resize()
        updateScales()
    }()

    function resize() {
        chart.width_ = Math.round($(chart.settings.selector).parent().width())
        chart.width = chart.width_ - chart.margin.left - chart.margin.right
        chart.height_ = Math.round(chart.settings.ratio * chart.width_)
        chart.height = chart.height_ - chart.margin.top - chart.margin.bottom
        chart.outerRadius = Math.min(chart.width, chart.height) * .45

        chart.svg.attr('width', chart.width_).attr('height', chart.height_)
        chart.g.attr('transform', `translate(${chart.width / 2}, ${chart.height / 2})`)
    }

    function updateScales() {
        // const heights = Array.prototype.concat(...chart.data.map(d => d.height))
        // const heightMin = d3.min(heights)
        // const heightMax = d3.max(heights)

        for (let i = 0; i < chart.data.length; i++) {
            chart.x[i]
                .domain(chart.data[i].ordered)
                .range([0, chart.width])
            let heightMin = d3.min(chart.data[i].height)
            let heightMax = d3.max(chart.data[i].height)
            chart.y[i]
                .domain([Math.max(heightMin - .1 * (heightMax - heightMin), 0), heightMax])
                .range([chart.height, 0])
        }
    }

    function divide() {
        const data = chart.data.map(d => d.labels.length)
        const arcs = d3.pie().padAngle(0)(data)
        return arcs
    }

    chart.update = function() {
        let x = d3.scaleLinear()
            .domain([0, chart.width])
        let y = d3.scaleLinear()
            .range([chart.innerRadius, chart.outerRadius])
        let line = d3.lineRadial()
            .angle(d => x(d[0]))
            .radius(d => y(d[1]))
        let arc = d3.arc()

        const arcs = divide()
        for (let z = 0; z < arcs.length; z++) {
            x.range([arcs[z].startAngle, arcs[z].endAngle])
            y.domain(chart.y[z].range())

            let positions = buildPositions(z)
            let locations = chart.data[z].merge.map((d, i) => {
                // Element:
                //                    top
                //      left        -------------- right
                //      bottomleft  |            | 
                //                               | bottomright
                let left = d[0] < 0 ? toX(d[0], z) : positions[d[0]-1],
                    top = chart.y[z](chart.data[z].height[i]),
                    right = d[1] < 0 ? toX(d[1], z) : positions[d[1]-1],
                    bottomLeft = d[0] < 0 ? chart.y[z].range()[0] :
                                        chart.y[z](chart.data[z].height[d[0]-1]),
                    bottomRight = d[1] < 0 ? chart.y[z].range()[0] :
                                        chart.y[z](chart.data[z].height[d[1]-1])

                return {left, top, right, bottomLeft, bottomRight}
            })

            // draw
            const project = chart.g.append('g').classed('project', true)

            const group = project.selectAll('.group').data(locations)
            group.exit().remove()
            const groupEnter = group.enter().append('g')
                .attr('stroke', 'black')
                .attr('stroke-width', '1.5')
            groupEnter.append('path')
                .attr('d', d => line([[d.left, d.top], [d.left, d.bottomLeft]]))
            groupEnter.append('path')
                .attr('d', d => line([[d.right, d.top], [d.right, d.bottomRight]]))
            groupEnter.append('path')
                .attr('d', d => arc({innerRadius: y(d.top), outerRadius: y(d.top), startAngle: x(d.left), endAngle: x(d.right)}))

            const circle = project.selectAll('circle.module').data(chart.data[z].ordered)
            circle.exit().remove()
            circle.enter().append('circle')
                .classed('module', true)
                .attr('transform', d => {
                    const radius = chart.innerRadius - 15
                    const angle = x(chart.x[z](d))
                    const x_ = radius * Math.cos(angle - Math.PI * .5) + 1
                    const y_ = radius * Math.sin(angle - Math.PI * .5) + 1
                    return `translate(${x_}, ${y_})`
                })
                .attr('r', 2)
        }

        return chart
    }

    return chart
}

export default dendrogram