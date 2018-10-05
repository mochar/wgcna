<template>
<svg :width="width_" :height="height_">
    <g :transform="`translate(${margin.left}, ${margin.top})`">
        <text text-anchor="middle" :transform="`translate(-55,${(height - colorsHeight) /2})rotate(-90)`" style="font-size: 1rem">
            Height
        </text>
        <g id="tree-axis" class="axis axis--y"></g>
        <g id="colors-axis" class="axis axis--y" v-if="colors"></g>
        <line id="cutline" stroke="red" opacity="0.8" x1="0" :x2="width" v-if="cuttable"></line>
        <line id="cutlineset" stroke="red" stroke-width="2" v-if="cuttable && cutHeight" x1="0" :x2="width"
            :y1="cutHeight" :y2="cutHeight"></line>
        <g id="clusters"></g>
    </g>
</svg>
</template>

<script>
import { scaleBand, scaleLinear } from 'd3-scale'
import { axisLeft } from 'd3-axis'
import { select, event } from 'd3-selection'
import { min, max } from 'd3-array'
import { formatPrefix } from 'd3-format'
const d3 = { scaleBand, scaleLinear, axisLeft, select, event, min, max, formatPrefix }

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
            cutline: null,
            cutlineset:null,
            cutHeight: null,
            x: d3.scaleBand().range([0, this.width]).paddingOuter(.5),
            y: d3.scaleLinear().range([this.height, 0]),
            axis: d3.axisLeft(this.y),
            margin: {top: 10, right: 5, bottom: 5, left: 100},
            clusters: null,
            largestCluster: null,

            colorHeight: 20,
            colorsHeight: 0,
            colorsMargin: 50
        }
    },

    props: ['clusterData', 'cuttable', 'labels', 'ratio', 'colors'],

    methods: {
        updateCutLine() {
            const ordered = this.clusterData.ordered
            const newHeight = d3.event.offsetY - this.margin.top
            this.cutline
                .attr('y1', newHeight)
                .attr('y2', newHeight)
        },
        cut(event) {
            this.cutHeight = d3.event.offsetY - this.margin.top
            this.cutHeight = this.cutline.attr('y1')
            console.log(this.cutHeight)
            const reverseY = d3.scaleLinear()
                .domain(this.y.range())
                .range(this.y.domain())
            this.generateClusters(reverseY(this.cutHeight))
        },
        generateClusters(cutHeight) {
            const cutMerges = this.clusterData.merge.reduce((prevs, cur, i) => {
                if (this.clusterData.height[i] >= cutHeight) {
                    if (!prevs.includes(i + 1)) prevs.push(i + 1)
                    if (cur[0] > 0 && !prevs.includes(cur[0])) prevs.push(cur[0])
                    if (cur[1] > 0 && !prevs.includes(cur[1])) prevs.push(cur[1])
                }
                return prevs
            }, [])

            let mergeToClust = {}
            let labelClusters = this.clusterData.labels.map(d => 0)
            let mergeClusters = this.clusterData.merge.map(d => 0)
            let curClust = 0
            for (let i = this.clusterData.merge.length - 1; i >= 0; i--) {
                let cluster
                if (cutMerges.includes(i + 1)) {
                    cluster = ++curClust
                    mergeClusters[i] = curClust
                } else {
                    cluster = mergeClusters[i]
                }

                const merge = this.clusterData.merge[i]
                if (merge[0] < 0) {
                    labelClusters[-merge[0] - 1] = cluster
                } else if (this.clusterData.height[merge[0]-1] <= cutHeight) {
                    mergeClusters[merge[0] - 1] = cluster
                }
                if (merge[1] < 0) {
                    labelClusters[-merge[1] - 1] = cluster
                } else if (this.clusterData.height[merge[1]-1] <= cutHeight) {
                    mergeClusters[merge[1] - 1] = cluster
                }
            }

            this.clusters = {labelClusters, mergeClusters}
            this.largestCluster = this.$helpers.mode([...labelClusters])
            this.$emit('cutted', this.clusterData.labels.filter((d, i) => {
                return this.clusters.labelClusters[i] !== this.largestCluster
            }))
            this.updatePlot()
        },
        buildPositions() {
            const labels = this.clusterData.labels
            return this.clusterData.merge.reduce((prev, cur, i) => {
                const x1 = cur[0] < 0 ? this.toX(cur[0]) : prev[cur[0]-1]
                const x2 = cur[1] < 0 ? this.toX(cur[1]) : prev[cur[1]-1]
                prev.push(x1 + ((x2 - x1) / 2))
                return prev
            }, [])
        },
        resize() {
            this.width_ = $(this.$el).parent().width()
            this.width = this.width_ - this.margin.left - this.margin.right
            if (this.colors)
                this.colorsHeight = Object.keys(this.colors).length * this.colorHeight
            this.height_ = this.ratio * this.width_ 
            this.height_ += this.colorsHeight  + this.colorsMargin
            this.height = this.height_ - this.margin.top - this.margin.bottom
        },
        toX(d) {
            return this.x(this.clusterData.labels[-d - 1]) + (this.x.bandwidth() / 2)
        },
        updatePlot() {
            this.x
                .domain(this.clusterData.ordered)
                .range([0, this.width-25])

            const heightMin = d3.min(this.clusterData.height)
            const heightMax = d3.max(this.clusterData.height)
            this.y
                .domain([Math.max(heightMin - 0.1 * (heightMax - heightMin), 0), heightMax])
                // .domain([0, d3.max(this.clusterData.height)])
                .range([this.height - this.colorsHeight - this.colorsMargin, 0])
            
            this.axis.scale(this.y)
            if (heightMin > 1000) this.axis.tickFormat(d3.formatPrefix('.0', 1e3))
            this.g.select('#tree-axis').call(this.axis)

            const labels = this.clusterData.labels
            const positions = this.buildPositions()

            const group = this.g.selectAll('.group')
                .data(this.clusterData.merge, d => `${d[0]}_${d[1]}`)
            group.exit().remove()
            const groupEnter = group.enter().append('g').classed('tree-line', true)
            groupEnter.append('line')
                .attr('x1', d => d[0] < 0 ? this.toX(d[0]) : positions[d[0]-1])
                .attr('x2', d => d[1] < 0 ? this.toX(d[1]) : positions[d[1]-1])
                .attr('y1', (d, i) => this.y(this.clusterData.height[i]))
                .attr('y2', (d, i) => this.y(this.clusterData.height[i]))
                .attr('stroke', (d, i) => {
                    if (!this.clusters) return 'black'
                    const leftCluster = d[0] < 0 ? this.clusters.labelClusters[-d[0] - 1] : 
                                                   this.clusters.mergeClusters[d[0] - 1]
                    const rightCluster = d[1] < 0 ? this.clusters.labelClusters[-d[1] - 1] : 
                                                    this.clusters.mergeClusters[d[1] - 1]
                    if (leftCluster !== rightCluster) return 'black'
                    return leftCluster === this.largestCluster ? 'red' : 'black'
                })
            // Left
            groupEnter.append('line')
                .attr('x1', d => d[0] < 0 ? this.toX(d[0]) : positions[d[0]-1])
                .attr('x2', d => d[0] < 0 ? this.toX(d[0]) : positions[d[0]-1])
                .attr('y1', (d, i) => this.y(this.clusterData.height[i]))
                .attr('y2', (d, i) => {
                    if (d[0] < 0) return this.y(this.clusterData.height[i])+5
                    return this.y(this.clusterData.height[d[0]-1])
                })
                .attr('stroke', (d, i) => {
                    if (!this.clusters) return 'black'
                    const cluster = d[0] < 0 ? this.clusters.labelClusters[-d[0] - 1] : 
                                               this.clusters.mergeClusters[d[0] - 1]
                    return cluster === this.largestCluster ? 'red' : 'black'
                })
            if (this.labels) {
                groupEnter.append('text')
                    .attr('transform', (d, i) => {
                        const x = d[0] < 0 ? this.toX(d[0]) : positions[d[0]-1]
                        const y = this.y(this.clusterData.height[i])
                        return `translate(${x-3},${y+10})rotate(90)`
                    })
                    .text((d, i) => {
                        if (d[0] > 0) return ''
                        return this.clusterData.labels[-d[0] - 1]
                    })
            }
            // Right
            groupEnter.append('line') 
                .attr('x1', d => d[1] < 0 ? this.toX(d[1]) : positions[d[1]-1])
                .attr('x2', d => d[1] < 0 ? this.toX(d[1]) : positions[d[1]-1])
                .attr('y1', (d, i) => this.y(this.clusterData.height[i]))
                .attr('y2', (d, i) => {
                    if (d[1] < 0) return this.y(this.clusterData.height[i])+5
                    return this.y(this.clusterData.height[d[1]-1])
                })
                .attr('stroke', (d, i) => {
                    if (!this.clusters) return 'black'
                    const cluster = d[1] < 0 ? this.clusters.labelClusters[-d[1] - 1] : 
                                               this.clusters.mergeClusters[d[1] - 1]
                    return cluster === this.largestCluster ? 'red' : 'black'
                })
            if (this.labels) {
                groupEnter.append('text')
                    .attr('transform', (d, i) => {
                        const x = d[1] < 0 ? this.toX(d[1]) : positions[d[1]-1]
                        const y = this.y(this.clusterData.height[i])
                        return `translate(${x-3},${y+10})rotate(90)`
                    })
                    .text((d, i) => {
                        if (d[1] > 0) return ''
                        return this.clusterData.labels[-d[1] - 1]
                    })
            }

            if (this.colors) this.updateColors()
        },
        updateColors() {
            const yCluster = d3.scaleBand()
                .domain(Object.keys(this.colors))
                .range([this.height, this.height - this.colorsHeight])

            const axis = d3.axisLeft(yCluster)
            this.g.select('#colors-axis').call(axis)

            const data = Object.keys(this.colors).map(color => { 
                return { color, values: this.colors[color] }
            })

            const group = this.g.select('g#clusters').selectAll('g').data(data, d => d.color)
            group.exit().remove()
            const groupEnter = group.enter().append('g')
                .attr('transform', d => `translate(0,${yCluster(d.color)})`)
            const groupAll = groupEnter.merge(group)
            const rect = groupAll.selectAll('rect').data(d => d.values, d => d)
            rect.exit().remove()
            const rectEnter = rect.enter().append('rect')
                .attr('fill', d => d)
                .attr('stroke', d => d)
                .attr('x', (d, i) => this.x(this.clusterData.ordered[i]))
                .attr('y', 0)
                .attr('width', this.x.bandwidth() + this.x.padding() * 2)
                .attr('height', this.colorHeight)
        }
    },

    mounted() {
        this.svg = d3.select(this.$el)
        this.resize()
        this.g = this.svg.select('g')
        if (this.cuttable) {
            this.svg.on('mousemove', this.updateCutLine)
            this.svg.on('click', this.cut)
        }
        this.cutline = this.g.select('line#cutline')
        this.cutlineset = this.g.select('line#cutlineset')
        this.updatePlot()
        this.updateColors()
    },

    watch: {
        clusterData() {
            if (!this.clusterData) return
            this.updatePlot()
        },
        colors() {
            if (this.colors) {
                this.resize()
                this.updateColors()
            }
        }
    }
}
</script>

<style>
text {
    font-size: 12px;
}

line {
    shape-rendering: crispEdges;
}

#colors-axis line {
    stroke: #fff !important;
}
</style>