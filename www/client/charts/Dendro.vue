<template>
<div class="dendro">
    <canvas class="main"></canvas>
    <canvas class="cut"></canvas>
</div>
</template>

<script>
import * as d3 from 'd3'
import { drawAxis } from 'charts/Functions'

export default {
    data() {
        return {
            cutline: null,
            cutlineset:null,
            clusters: null,
            largestCluster: null
        }
    },

    props: {
        clusterData: Object,
        cuttable: Boolean,
        labels: Boolean,
        ratio: Number,
        colors: Object
    },

    methods: {
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
            this.width_ = Math.round($(this.$el).parent().width())
            this.width = this.width_ - this.margin.left - this.margin.right
            if (this.colors)
                this.colorsHeight = Object.keys(this.colors).length * this.colorHeight
            this.height_ = Math.round(this.ratio * this.width_)
            this.height_ += this.colorsHeight  + this.colorsMargin
            this.height = this.height_ - this.margin.top - this.margin.bottom
        },
        setupCanvas() {
            // After resize, canvas is clear. Therefore setup again every resize
            this.canvas.width = this.width_
            this.canvas.height = this.height_
            this.context.translate(this.margin.left + .5, this.margin.top + .5)
            this.context.font = 'normal 12px sans-serif'

            this.cutCanvas.width = this.width_
            this.cutCanvas.height = this.y.range()[0]
            this.cutContext.translate(this.margin.left + .5, this.margin.top + .5)
            this.cutContext.lineWidth = 2
            this.cutContext.strokeStyle = 'red'
        },
        toX(d) {
            return this.x(this.clusterData.labels[-d - 1]) + (this.x.bandwidth() / 2)
        },
        updateScales() {
            this.x
                .domain(this.clusterData.ordered)
                .range([0, this.width-25])

            const heightMin = d3.min(this.clusterData.height)
            const heightMax = d3.max(this.clusterData.height)
            this.y
                .domain([Math.max(heightMin - 0.1 * (heightMax - heightMin), 0), heightMax])
                // .domain([0, d3.max(this.clusterData.height)])
                .range([this.height - this.colorsHeight - this.colorsMargin, 0])
            this.yReverse
                .domain(this.y.range())
                .range(this.y.domain())
        },
        updatePlot() {
            const positions = this.buildPositions()

            // draw
            drawAxis(this.y, this.context, true, 'Height')

            this.context.beginPath()
            for (let i = 0; i < this.clusterData.merge.length; i++) {
                // Element:
                //                    top
                //      left        -------------- right
                //      bottomleft  |            | 
                //                               | bottomright

                let d = this.clusterData.merge[i],
                    left = d[0] < 0 ? this.toX(d[0]) : positions[d[0]-1],
                    top = this.y(this.clusterData.height[i]),
                    right = d[1] < 0 ? this.toX(d[1]) : positions[d[1]-1],
                    bottomLeft = d[0] < 0 ? this.y(this.clusterData.height[i])+5 :
                                        this.y(this.clusterData.height[d[0]-1]),
                    bottomRight = d[1] < 0 ? this.y(this.clusterData.height[i])+5 :
                                        this.y(this.clusterData.height[d[1]-1])
                
                // Avoid anti aliasing effects
                left = Math.round(left)
                right = Math.round(right)
                
                // Horizontal line
                this.context.moveTo(left, top)
                this.context.lineTo(right, top)
                
                // Left line
                this.context.moveTo(left, top)
                this.context.lineTo(left, bottomLeft)

                // Right line
                this.context.moveTo(right, top)
                this.context.lineTo(right, bottomRight)
            }
            this.context.stroke()

            if (this.labels) this.updateLabels()
            if (this.colors) this.updateColors()
        },
        updateLabels() {

        },
        updateColors() {
            const yCluster = d3.scaleBand()
                .domain(Object.keys(this.colors))
                .range([this.height, this.height - this.colorsHeight])

            drawAxis(yCluster, this.context, false)

            this.context.beginPath()
            Object.keys(this.colors).forEach((d, i) => {
                let values = this.colors[d],
                    y = yCluster(d)
                values.forEach((val, j) => {
                    let x = this.x(this.clusterData.ordered[j]),
                        width = this.x.bandwidth() + this.x.padding() * 2 + 1,
                        height = this.colorHeight
                    this.context.fillStyle = val
                    this.context.fillRect(x, y, width, height)
                })
            })
            this.context.fill()
        }
    },

    mounted() {
        this.canvas = d3.select(this.$el).select('canvas.main').node()
        this.context = this.canvas.getContext('2d')

        this.cutCanvas = d3.select(this.$el).select('canvas.cut').node()
        this.cutContext = this.cutCanvas.getContext('2d')

        this.height = 100
        this.width = 100
        this.colorHeight = 20
        this.colorsHeight = 0
        this.colorsMargin = 50
        this.cutHeight = null
        this.margin = {top: 10, right: 5, bottom: 5, left: 100}

        this.x = d3.scaleBand().paddingOuter(.5)
        this.y = d3.scaleLinear().interpolate(d3.interpolateRound)
        this.yReverse = d3.scaleLinear().interpolate(d3.interpolateRound)

        if (this.cuttable) {
            d3.select(this.cutCanvas).on('mousemove', () => {
                const newHeight = d3.event.offsetY - this.margin.top
                this.cutContext.clearRect(-.5, -.5 - this.margin.top, 
                    this.cutCanvas.width, this.cutCanvas.height + this.margin.top)
                this.cutContext.beginPath()
                this.cutContext.moveTo(0, newHeight)
                this.cutContext.lineTo(this.cutCanvas.width, newHeight)
                if (this.cutHeight) {
                    this.cutContext.moveTo(0, this.cutHeight)
                    this.cutContext.lineTo(this.cutCanvas.width, this.cutHeight)
                }
                this.cutContext.stroke()
            }).on('click', () => {
                this.cutHeight = d3.event.offsetY - this.margin.top
                console.log(this.yReverse(this.cutHeight))
                this.cutContext.moveTo(0, this.cutHeight)
                this.cutContext.lineTo(this.cutCanvas.width, this.cutHeight)
            })
        }

        this.resize()
        this.updateScales()
        this.setupCanvas()
        this.updatePlot()
    },

    watchh: {
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
.dendro {
    position: relative;
}

.dendro canvas {
}

.dendro canvas.main {
    z-index: 1;
}
.dendro canvas.cut {
    position: absolute;
    z-index: 2;
    left: 0;
}
</style>
