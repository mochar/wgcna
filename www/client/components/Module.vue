<template>
<div class="col-3 p-1">
<div class="card card-body p-2" @mouseover="showDetails = true" @mouseout="showDetails = false">
    <div class="d-flex justify-content-between align-items-baseline p-2">
        <h6 class="block-title text-uppercase">
            {{ name }}
        </h6>

        <div class="text-muted d-flex align-items-center">
            <div class="dropdown ml-2" :style="{ opacity: showDetails ? 1 : 0 }">
                <button class="btn btn-link text-muted pr-1 pt-0 pb-0" data-toggle="dropdown">
                    <font-awesome-icon icon="ellipsis-v" />
                </button>
                <div class="dropdown-menu dropdown-menu-right">
                    <a class="dropdown-item" href="#" @click.prevent="">
                        Download expression
                    </a>
                    <a class="dropdown-item" href="#" @click.prevent="">
                        Download feature list
                    </a>
                </div>
            </div>
        </div>
    </div>
    <svg :id="`box-plot-${name}`"></svg>
    <!-- <div v-show="showDetails">
        Legend
    </div> -->
</div>
</div>
</template>

<script>
import boxplot from 'charts/Boxplot.js'
import { scaleOrdinal } from 'd3-scale'
import { schemePastel1 } from 'd3-scale-chromatic'

export default {
    props: ['name', 'data', 'samples', 'groups'],

    data() {
        return {
            showDetails: false
        }
    },

    methods: {
        processData(){
            const bins = this.data.reduce((acc, cur, i) => { 
                acc[this.groupLabels.indexOf(this.groups[i])].data.push(cur)
                return acc
            }, this.groupLabels.map(d => ({ group: d, data: [] })))
            return bins
        },
        createChart() {
            this.chart = boxplot({
                selector: `#box-plot-${this.name}`,
            }).update(this.processData())
        },
        download() {
        }
    },

    computed: {
        groupLabels() {
            return [...new Set(this.groups)]
        }
    },

    watch: {
        groups() {
            this.chart.update(this.processData())
        }
    },

    mounted() {
        this.createChart()
    },

    updated() {
        this.chart.update(this.processData())
    }
}
</script>

<style scoped>
svg#box-plot-* {
    shape-rendering: crispEdges;
}
</style>
