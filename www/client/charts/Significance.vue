<template>
<svg :width="width" :height="height">
    <g :transform="`translate(${margin.left}, ${margin.top})`">
        <g class="axis axis--x" :transform="`translate(0, ${height-110})`"></g>
    </g>
</svg>
</template>

<script>
import * as d3 from 'd3'

export default {
    data() {
        return {
            svg: null,
            g: null,
            height: 100,
            width: 100,
            size: 75,
            margin: {top: 40, right: 5, bottom: 10, left: 35},
            color: d3.scaleOrdinal(d3.schemeCategory20c)
        }
    },

    props: ['eigengenes', 'modules', 'pvalues', 'samples', 'groups', 'column'],

    methods: {
        resize() {
            this.width = $(this.$el).parent().width() - this.margin.left - this.margin.right
            this.height = (this.modules.length * this.size) - this.margin.top - this.margin.bottom
            this.height += 110 // axis bottom
        },
        updatePlot() {
            this.color.domain(this.group)
            const y = d3.scaleBand() // placement module eigengene
                .domain(this.modules)
                .range([this.height-60, 0])
            const y1 = d3.scaleLinear() // placement y value 
                .domain([-1, 1])
                .range([(this.size / 2) * -1, this.size / 2])
            const x = d3.scaleBand() 
                .domain(this.samples)
                .range([0, this.width * .5])
                // .paddingInner(0.06)
            
            const line = this.g.selectAll('line.sample-line').data(this.samples, d => d)
            line.exit().remove()
            const lineEnter = line.enter().append('line').classed('sample-line', true)
                .attr('y2', 0)
                .attr('stroke', '#eee')
              .merge(line)
                .attr('x1', (d, i) => x(this.samples[i]) + (x.bandwidth() / 2))
                .attr('y1', (d, i) => this.height - 110)
                .attr('x2', (d, i) => x(this.samples[i]) + (x.bandwidth() / 2))

            
            const data = this.modules.map(module => {
                const values = this.eigengenes[module].map((e, i) => { 
                    return { val: e, module, group: this.groups[i], sample: this.samples[i]}
                })
                return { module, values }
            })

            const group = this.g.selectAll('g.eigengene').data(data, d => `${d.module}:${this.column}`)
            group.exit().remove()
            const groupEnter = group.enter().append('g').classed('eigengene', true)
                .attr('transform', d => `translate(0,${y(d.module)})`)
            const rect = groupEnter.selectAll('rect').data(d => d.values, d => d.sample)
            rect.exit().remove()
            rect.enter().append('rect')
                .attr('stroke', ' black')
                // .attr('stroke', d => d3.rgb(this.color(d.group)).darker(3))
              .merge(rect)
                .attr('x', (d, i) => x(this.samples[i]))
                .attr('y', (d, i) => y1(Math.min(0, d.val)))
                .attr('width', x.bandwidth())
                .attr('height', (d, i) => Math.abs(y1(d.val) - y1(0)))
                .attr('fill', (d, i) => {
                    console.log('fill')
                    const color = this.color(d.group)
                    if (!this.column) return color
                    return this.columnGroups.includes(d.group) ? color : 'grey'
                    // return color
                })
            
            this.g.select('g.axis--x').call(d3.axisBottom(x))
              .selectAll("text")  
                .style("text-anchor", "end")
                .attr("dx", "-.8em")
                .attr("dy", ".15em")
                .attr("transform", "rotate(-45)" );
        }
    },

    mounted() {
        this.svg = d3.select(this.$el)
        this.resize()
        this.g = this.svg.select('g')
        this.updatePlot()
    },

    computed: {
        group() {
            return [...new Set(this.groups)]
        },
        columnGroups() {
            return this.column ? this.column.split(' vs ') : []
        }
    },

    watch: {
        column() {
            this.updatePlot()
        },
    }
}
</script>

<style>
rect {
    shape-rendering: crispEdges;
}
</style>