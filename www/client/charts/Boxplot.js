import { selectAll, select } from 'd3-selection'
import { scaleLinear, scaleBand, scaleOrdinal } from 'd3-scale'
import { quantile } from 'd3-array'
import { schemePastel1 } from 'd3-scale-chromatic'
import { axisTop } from 'd3-axis'
const d3 = { selectAll, select, scaleLinear, scaleBand, scaleOrdinal, quantile, schemePastel1, axisTop }

function boxplot(settings) {
    let chart = {}

    chart.settings = {
        data: null,
        groups: null,
        selector: null,
        boxSize: 50
    }
    for (var setting in settings) {
        chart.settings[setting] = settings[setting]
    }

    chart.data = chart.settings.data
    chart.groups = chart.settings.groups

    !function init() {
        chart.margin = {top: 20, right: 5, bottom: 0, left: 5}
        chart.svg = d3.select(chart.settings.selector)
        chart.g = chart.svg.append('g')
        chart.gAxis = chart.svg.append('g')

        chart.x = d3.scaleLinear().domain([-1, 1])
        chart.y = d3.scaleBand().domain(chart.groups).padding(.2)
        chart.c = d3.scaleOrdinal().domain(chart.groups).range(d3.schemePastel1)

        chart.axis = g => g
            .attr('transform', `translate(0,${chart.margin.top})`)
            .call(d3.axisTop(chart.x).ticks(2, '.0f'))

        chart.data = chart.data.map((bin, i) => {
            bin.sort((a, b) => a - b)
            const min = bin[0]
            const max = bin[bin.length - 1]
            const q1 = d3.quantile(bin, 0.25)
            const q2 = d3.quantile(bin, 0.50)
            const q3 = d3.quantile(bin, 0.75)
            const iqr = q3 - q1
            const r0 = Math.max(min, q1 - iqr * 1.5)
            const r1 = Math.min(max, q3 + iqr * 1.5)
            bin.quaritiles = [q1, q2, q3]
            bin.range = [r0, r1]
            bin.outliers = bin.filter(x => x < r0 || x > r1)
            bin.group = chart.groups[i]
            return bin
        })

        resize()
    }()

    function resize() {
        chart.width = Math.round($(chart.settings.selector).parent().width())
        chart.height = chart.settings.boxSize * chart.data.length
        chart.svg.attr('width', chart.width).attr('height', chart.height)
        chart.x.rangeRound([chart.margin.left, chart.width - chart.margin.right])
        chart.y.rangeRound([chart.height - chart.margin.bottom, chart.margin.top])
    }

    chart.update = function() {
        const g = chart.g
          .selectAll('g')
          .data(chart.data, d => d.group)
        
        g.exit().remove()

        const gEnter = g.enter().append('g')

        gEnter.append('line')
            .attr('stroke', 'black')
            .attr('x1', d => chart.x(d.range[0]))
            .attr('x2', d => chart.x(d.range[1]))
            .attr('y1', d => chart.y(d.group) + (chart.y.bandwidth() * .5))
            .attr('y2', d => chart.y(d.group) + (chart.y.bandwidth() * .5))
        
        gEnter.append('rect')
            .attr('fill', d => chart.c(d.group))
            .attr('x', d => chart.x(d.quaritiles[0]))
            .attr('width', d => chart.x(d.quaritiles[2]) - chart.x(d.quaritiles[0]))
            .attr('y', (d, i) => chart.y(d.group))
            .attr('height', (d, i) => chart.y.bandwidth())

        gEnter.append('line')
            .attr('stroke', 'black')
            .attr('stroke-width', 2)
            .attr('x1', d => chart.x(d.quaritiles[1]))
            .attr('x2', d => chart.x(d.quaritiles[1]))
            .attr('y1', (d, i) => chart.y(d.group))
            .attr('y2', (d, i) => chart.y(d.group) + chart.y.bandwidth())

        gEnter.append("g")
            .attr('fill', d => chart.c(d.group))
            .attr("fill-opacity", 1)
            .attr("stroke", "none")
            .attr("transform", d => `translate(0,${chart.y(d.group) + (chart.y.bandwidth() * .5)})`)
          .selectAll("circle")
          .data(d => d.outliers)
          .enter().append("circle")
            .attr("r", 3)
            .attr("cx", d => chart.x(d))
            .attr("cy", () => (Math.random() - 0.5) * 4)

        chart.gAxis.call(chart.axis)
        
        return chart
    }

    return chart
}

export default boxplot