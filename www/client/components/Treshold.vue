<template>
<div class="card card-block block">
    <h6 class="block-title">
        SOFT TRESHOLD
        <span class="fa fa-cog fa-spin" v-if="loading"></span>
    </h6>

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
            <h5 class="">Scale independence</h5>
            <scatter 
                v-if="powers"
                :highlight="highlight"
                :xData="powers" 
                :yData="scaleindep">
            </scatter>
        </div>

        <div class="col-4">
            <h5 class="">Mean connectivity</h5>
            <scatter 
                v-if="powers"
                :highlight="highlight"
                :xData="powers" 
                :yData="meank">
            </scatter>
        </div>
    </div>

    <div>
        <button class="btn btn-primary float-right" @click="pick">
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