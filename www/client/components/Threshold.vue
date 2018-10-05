<template>
<div class="card card-body block">
    <div class="d-flex justify-content-between align-items-start">
        <h6 class="block-title">
            SOFT TRESHOLD
            <font-awesome-icon icon="cog" spin v-if="loading" />
        </h6>

        <div class="text-muted d-flex align-items-center">
            <font-awesome-icon icon="info" class="text-muted" />
            <div class="dropdown ml-2">
                <button class="btn btn-link text-muted pr-1 pt-0 pb-0" data-toggle="dropdown">
                    <font-awesome-icon icon="ellipsis-v" />
                </button>
                <div class="dropdown-menu dropdown-menu-right">
                    <h6 class="dropdown-header">Download plot</h6>
                    <a class="dropdown-item" href="#" @click.prevent="downloadPlot(0, 'scale_independence')">
                        Scale independence
                    </a>
                    <a class="dropdown-item" href="#" @click.prevent="downloadPlot(1, 'mean_connectivity')">
                        Mean connectivity
                    </a>
                </div>
            </div>
        </div>
    </div>

    <p class="card-text">
        Pick a threshold which will be used to power-transform the gene correlations in order to reduce inherent biological noise.
    </p>

    <div class="row" v-if="!loading">
        <div class="col-4">
            <table class="table table-hover table-sm">
                <thead>
                    <th>Power</th>
                    <th>Scale independence</th>
                    <th>Mean connectivity</th>
                </thead>
                <tbody>
                    <tr v-for="(power, i) in powers" 
                        :key="i"
                        :style="{ 'font-weight': power == highlight ? 'bold' : 'normal',
                                  'color': power == highlight || power == project.power ? 'red' : 'black' }"
                        @click="selected = power"
                        @mouseover="hovered = power"
                        @mouseout="hovered = null">
                        <td>{{ power }}</td>
                        <td>{{ scaleindep[i] | round(3) }}</td>
                        <td>{{ meank[i] | round(3) }}</td>
                    </tr>
                </tbody>
            </table>
        </div>

        <div class="col-4">
            <scatter 
                v-if="powers"
                yLabel="Scale independence"
                :highlight="highlight"
                :xData="powers" 
                :yData="scaleindep">
            </scatter>
        </div>

        <div class="col-4">
            <scatter 
                v-if="powers"
                yLabel="Mean connectivity"
                :highlight="highlight"
                :xData="powers" 
                :yData="meank">
            </scatter>
        </div>
    </div>

    <div class="block-action-div">
        <button class="btn btn-light" :disabled="!buttonReady" @click="pick">
            <font-awesome-icon icon="check" />
            Select
        </button>
    </div>
</div>
</template>

<script>
import Scatter from 'charts/Scatter'

export default {
    data() {
        return {
            powers: null,
            scaleindep: null,
            meank: null,
            loading: true,
            hovered: null,
            selected: null
        }
    },

    components: {
        Scatter
    },

    props: ['project', 'update'],

    methods: {
        pick() {
            const formData = new FormData()
            formData.append('power', this.selected)
            this.$helpers.post(formData, this.project.id, 'tresholds')
            .then(() => {
                this.$emit('done', this.selected)
            }, () => {
                console.log('error')
            })
        },
        getValues() {
            $.get(`${ROOTURL}/projects/${this.project.id}/tresholds`).then(data => {
                this.powers = data.powers
                this.scaleindep = data.scaleindep
                this.meank = data.meank
                this.loading = false
            })
        },
        downloadPlot(svgIndex, filename) {
            const svgEl = $(this.$el).find('svg')[svgIndex]
            this.$helpers.downloadSvg(svgEl, filename)
        }
    },

    created() {
        this.getValues()
    },

    watch: {
        project() {
            if (this.update) {
                this.loading = true
                this.getValues()
            }
        }
    },

    computed: {
        highlight() {
            if (this.hovered) {
                return this.hovered
            } else if (this.selected) {
                return this.selected
            } else if (this.project.power) {
                return this.project.power
            } else {
                return null
            }
        },
        buttonReady() {
            return this.selected && this.project.power != this.selected
        }
    }
}
</script>

<style scoped>
.table > tbody {
    cursor: pointer;
}
</style>
