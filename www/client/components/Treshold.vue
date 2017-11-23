<template>
<div class="card card-body block">
    <div class="d-flex justify-content-between">
        <h6 class="block-title">
            SOFT TRESHOLD
            <span class="fa fa-cog fa-spin" v-if="loading"></span>
        </h6>

        <div class="text-muted d-flex align-items-center">
            <span class="fa fa-info text-muted"></span>
            <div class="dropdown ml-2">
                <button class="btn btn-link text-muted pr-1 pt-0 pb-0" data-toggle="dropdown">
                    <span class="fa fa-ellipsis-v"></span>
                </button>
                <div class="dropdown-menu  dropdown-menu-right">
                    <a class="dropdown-item" href="#" @click.prevent="downloadPlot">
                        <span class="fa fa-download"></span>
                        Download plot
                    </a>
                </div>
            </div>
        </div>
    </div>

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
            <span class="h5">Scale independence</span>
            <scatter 
                v-if="powers"
                :highlight="highlight"
                :xData="powers" 
                :yData="scaleindep">
            </scatter>
        </div>

        <div class="col-4">
            <span class="h5">Mean connectivity</span>
            <scatter 
                v-if="powers"
                :highlight="highlight"
                :xData="powers" 
                :yData="meank">
            </scatter>
        </div>
    </div>

    <div class="block-action-div">
        <button class="btn btn-light" :disabled="!buttonReady" @click="pick">
            <span class="fa fa-check"></span>
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
            $.ajax({
                type: 'POST',
                url: `${ROOTURL}/projects/${this.project.id}/tresholds`,
                data: formData,
                async: true,
                cache: false,
                contentType: false,
                processData: false
            }).then(() => {
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
        downloadPlot() {
            const svgEl = $(this.$el).find('svg')[0]
            this.$helpers.downloadSvg(svgEl, 'scale_independence.svg')
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