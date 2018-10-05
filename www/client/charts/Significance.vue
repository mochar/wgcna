<template>
<svg :width="width_" :height="height_">
    <g :transform="`translate(${margin.left}, ${margin.top})`">
        <g id="axis-top" class="axis axis--x"></g>
        <g id="axis-bottom" class="axis axis--x" :transform="`translate(0, ${height})`"></g>
        <text :transform="`translate(${width * .8}, -15)`" text-anchor="middle" style="font-size: 1rem">
            {{ column ? 'Wilcoxon' : 'Kruskal-Wallis' }}
        </text>
        <!-- <text :transform="`translate(${width * .9}, -15)`" text-anchor="middle" style="font-size: 1rem">
            Module
        </text> -->
    </g>
</svg>
</template>

<script>
import { select } from 'd3-selection'
import { scaleOrdinal, scaleBand, scaleLinear } from 'd3-scale'
import { schemePastel1 } from 'd3-scale-chromatic'
import { rgb } from 'd3-color'
import { axisBottom, axisTop } from 'd3-axis'
import 'd3-transition'
const d3 = { select, scaleOrdinal, scaleBand, scaleLinear, schemePastel1, rgb, axisBottom, axisTop }

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
            margin: {top: 30, right: 5, bottom: 25, left: 35},
            color: d3.scaleOrdinal(d3.schemePastel1)
        }
    },

    props: ['eigengenes', 'modules', 'pvalues', 'samples', 'groups', 'column', 'sigOnly', 'columnOnly'],

    methods: {
        resize(length) {
            this.width_ = $(this.$el).parent().width()
            this.width = this.width_ - this.margin.left - this.margin.right
            // this.width *= .8
            this.height = length * this.size
            this.height_ = this.height + this.margin.top + this.margin.bottom
        },
        updatePlot() {
            /// Build data
            const data = this.modules.reduce((build, module, i) => {
                const significance = this.pvalues.significance[i]
                if (this.sigOnly && significance > 0.05) return build
                const eigengene = this.eigengenes[module]
                let p = this.column ? this.pvalues[this.column][i] : significance
                p = p === 'NA' ? null : p

                let valuesByGroup = this.groupShow.map(group => ({ group, values: []}))
                for (let index = 0; index < this.sortIndices.length; index++) {
                    const j = this.sortIndices[index]
                    const item = { val: eigengene[j], group: this.groups[j], sample: this.samples[j] }
                    if (this.groupShow.includes(item.group))
                        valuesByGroup[this.groupShow.indexOf(item.group)].values.push(item)
                }

                build.push({ module, significance, valuesByGroup, i, p })
                return build
            }, [])

            this.resize(data.length)

            /// Set up scales
            this.color.domain(this.group)
            const y = d3.scaleBand() // placement module eigengene
                .domain(data.map(d => d.module))
                .rangeRound([this.height, 0])
            const y1 = d3.scaleLinear() // placement y value 
                .domain([-1, 1])
                .range([(this.size / 2) * -1, this.size / 2])
            const x = d3.scaleBand() // Eigengene region
                .domain(this.groupShow)
                .rangeRound([0, this.width * .7])
                .paddingInner(0.1)
            const r = d3.scaleLinear() // P-value circle size
                .domain([0, 3])
                .range([1, 15])
            const xScaleByGroup = {} 
            for (let index = 0; index < data[0].valuesByGroup.length; index++) {
                const groupValues = data[0].valuesByGroup[index]
                const scale = d3.scaleBand()
                    .domain(groupValues.values.map(x => x.sample))
                    .rangeRound([0, x.bandwidth()])
                    .paddingInner(0.05)
                xScaleByGroup[groupValues.group] = scale
            }

            /// Build plot
            // Each row is one eigengene
            const group = this.g.selectAll('g.eigengene').data(data, d => d.module)
            group.exit().remove()
            const groupEnter = group.enter().append('g').classed('eigengene', true)
                .attr('transform', d => `translate(0,${y(d.module) + this.size / 2})`)
            const groupAll = groupEnter.merge(group)

            // Each main column is one group
            const colgroup = groupAll.selectAll('g').data(d => d.valuesByGroup, d => d.group)
            colgroup.transition()
                .attr('transform', d => `translate(${x(d.group)}, 0)`)
            colgroup.exit().remove()
            const colgroupEnter = colgroup.enter().append('g')
                .attr('transform', d => `translate(${x(d.group)}, 0)`)
            const colgroupAll = colgroupEnter.merge(colgroup)

            // Each rect (eigengene value) per sample
            const rect = colgroupAll.selectAll('rect').data(d => d.values, d => d.sample)
            rect.transition()
                .attr('x', d => xScaleByGroup[d.group](d.sample))
                .attr('width', d => xScaleByGroup[d.group].bandwidth())
                .attr('height', d => Math.abs(y1(d.val) - y1(0)))
            rect.exit().remove()
            rect.enter().append('rect')
                .attr('stroke', d => d3.rgb(this.color(d.group)).darker(2))
                .attr('x', d => xScaleByGroup[d.group](d.sample))
                .attr('width', d => xScaleByGroup[d.group].bandwidth())
                .attr('height', d => Math.abs(y1(d.val) - y1(0)))
              .merge(rect)
                .attr('y', d => y1(Math.min(0, d.val)))
                .attr('fill', (d, i) => {
                    const color = this.color(d.group)
                    if (!this.column) return color
                    return this.columnGroups.includes(d.group) ? color : 'grey'
                })
            
            // p-val circles
            /*
            const circle = groupAll.selectAll('circle').data(d => [d], d => `${d.module}_${this.column}`)
            circle.enter().append('circle')
                .attr('cx', this.width * .85)
                .attr('cy', 0)
              .merge(circle).transition()
                .attr('r', d => d.p ? r(-Math.log10(d.p)) : 0)
            */
            const text = groupAll.selectAll('text').data(d => [d], d => `${d.module}_${this.column}`)
            text.enter().append('text')
                .attr('x', this.width * .8)
                .attr('y', 5)
                .attr('text-anchor', 'middle')
              .merge(text)
                .attr('fill', d => d.p && d.p < 0.05 ? '#333' : 'grey' )
                .style('font-size', '1rem')
                .text(d => d.p ? parseFloat(d.p).toFixed(4) : 'NA')

            const text2 = groupAll.selectAll('text.mod').data(d => [d], d => `${d.module}_${this.column}`)
            text2.enter().append('text')
                .classed('mod', true)
                .attr('x', this.width * .9)
                .attr('y', 5)
              .merge(text2)
                .style('font-size', '1rem')
                .text(d => d.module)
            
            /// Axes and labels
            const axis = d3.axisBottom(x).tickSizeInner(-this.height)
            this.g.select('#axis-bottom').transition().call(axis)
              .selectAll('text')  
                .style('text-anchor', 'middle')
            this.g.select('#axis-top').transition().call(d3.axisTop(x))
              .selectAll('text')  
                .style('text-anchor', 'middle')
        }
    },

    mounted() {
        this.svg = d3.select(this.$el)
        this.resize(this.modules.length)
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
        },
        groupShow() {
            // We use group.filter instead of columnGroups because we want to keep the order
            return this.columnOnly && this.columnGroups.length > 0 ? 
                this.group.filter(g => this.columnGroups.includes(g)) : this.group
        }
    },

    watch: {
        column() {
            this.updatePlot()
        },
        sigOnly() {
            this.updatePlot()
        },
        columnOnly() {
            this.updatePlot()
        }
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