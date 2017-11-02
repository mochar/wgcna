<template>
<svg :width="width_" :height="height_">
    <g :transform="`translate(${margin.left}, ${margin.top})`">
        <g id="axis-top" class="axis axis--x"></g>
        <g id="axis-bottom" class="axis axis--x" :transform="`translate(0, ${height})`"></g>
    </g>
</svg>
</template>

<script>
import * as d3 from 'd3'

export default {
    data() {
        return {
            // Actual width/height of svg
            height_: 100,
            width_: 100,
            // Margin-less 
            height: 100,
            width: 100,

            svg: null,
            g: null,
            size: 75,
            margin: {top: 80, right: 5, bottom: 80, left: 35},
            color: d3.scaleOrdinal(d3.schemeCategory20c)
        }
    },

    props: ['eigengenes', 'modules', 'pvalues', 'samples', 'groups', 'column', 'sigOnly', 'columnOnly'],

    methods: {
        resize() {
            this.width_ = $(this.$el).parent().width()
            this.height_ = this.modules.length * this.size
            this.width = this.width_ - this.margin.left - this.margin.right
            this.height = this.height_ - this.margin.top - this.margin.bottom
        },
        updatePlot() {
            this.color.domain(this.group)
            const y = d3.scaleBand() // placement module eigengene
                .domain(this.modules)
                .range([this.height, 0])
            const y1 = d3.scaleLinear() // placement y value 
                .domain([-1, 1])
                .range([(this.size / 2) * -1, this.size / 2])
            const x = d3.scaleBand() // Eigengene region
                .domain(this.sortedSamples)
                .range([0, this.width * .8])
                .paddingInner(0.05)
            const r = d3.scaleLinear() // P-value circle size
                .domain([0, 3])
                .range([1, 10])

            const data = this.modules.map(module => {
                const eigengene = this.eigengenes[module]
                const values = this.sortIndices.map(i => {
                    return { val: eigengene[i], group: this.groups[i], sample: this.samples[i] }
                })
                return { module, values }
            })

            const group = this.g.selectAll('g.eigengene').data(data, d => `${d.module}:${this.column}`)
            group.exit().remove()
            const groupAll = group.enter().append('g').classed('eigengene', true)
                .attr('transform', d => `translate(0,${y(d.module) + this.size / 2})`)
              .merge(group)
            const rect = groupAll.selectAll('rect').data(d => d.values, d => d.sample)
            rect.exit().remove()
            rect.enter().append('rect')
                // .attr('stroke', ' black')
                .attr('stroke', d => d3.rgb(this.color(d.group)).darker(3))
              .merge(rect)
                .attr('x', (d, i) => x(this.sortedSamples[i]))
                .attr('y', (d, i) => y1(Math.min(0, d.val)))
                .attr('width', x.bandwidth())
                .attr('height', (d, i) => Math.abs(y1(d.val) - y1(0)))
                .attr('fill', (d, i) => {
                    const color = this.color(d.group)
                    if (!this.column) return color
                    return this.columnGroups.includes(d.group) ? color : 'grey'
                })
            const circle = groupAll.datum((d, i) => i).append('circle')
                .attr('cx', this.width * .9)
                .attr('cy', 0)
                .attr('r', d => {
                    const p = this.column ? this.pvalues[this.column][d] : this.pvalues.significance[d]
                    return p === 'NA' ? r(2) :  r(-Math.log10(p))
                })
            
            const axis = d3.axisBottom(x).tickSizeInner(-this.height)
            this.g.select('#axis-bottom').call(axis)
              .selectAll("text")  
                .style("text-anchor", "end")
                .attr("dx", "-.8em")
                .attr("dy", ".15em")
                .attr("transform", "rotate(-45)")
                .attr('textLength', this.size * 0.75)
            this.g.select('#axis-top').call(d3.axisTop(x))
              .selectAll("text")  
                .style("text-anchor", "start")
                .attr("dx", ".8em")
                .attr("dy", ".15em")
                .attr("transform", "rotate(-45)")
                .attr('textLength', this.size * 0.75)
        }
    },

    mounted() {
        this.svg = d3.select(this.$el)
        this.resize()
        this.g = this.svg.select('g')
        this.updatePlot()
    },

    computed: {
        sortIndices() {
            let mapped = this.groups.map(function(d, i) {
                return { index: i, value: d }
            })
            mapped.sort(function(a, b) {
                if (a.value > b.value) return 1
                if (a.value < b.value) return -1
                return 0
            })
            return mapped.map(d => d.index)
        },
        sortedGroups() {
            return this.sortIndices.map(i => this.groups[i])
        },
        sortedSamples() {
            return this.sortIndices.map(i => this.samples[i])
        },
        group() {
            return [...new Set(this.sortedGroups)]
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

.axis--x .tick line {
  stroke: #000;
  stroke-opacity: 0.15;
}
</style>