<template>
<div class="card card-block">
    <div class="row">
        <h5 class="card-title">1. Soft treshold</h5>

        <span class="fa fa-cog fa-spin fa-2x" v-if="loading"></span>

        <div v-else>
        <div class="col-xs-4">
            <table class="table table-hover table-sm">
                <thead>
                    <th>Power</th>
                    <th>Scale independence</th>
                    <th>Mean connectivity</th>
                </thead>
                <tbody>
                    <tr v-for="(power, i) in powers" 
                        :style="{ 'font-weight': power == highlight ? 'bold' : 'normal',
                                  'color': power == highlight ? 'red' : 'black' }"
                        @click="pick(power)"
                        @mouseover="hovered = power"
                        @mouseout="hovered = null">
                        <td>{{ power }}</td>
                        <td>{{ scaleindep[i] | round(3) }}</td>
                        <td>{{ meank[i] | round(3) }}</td>
                    </tr>
                </tbody>
            </table>
        </div>

        <div class="col-xs-4">
            <h4 class="text-xs-center">Scale independence</h4>
            <scatter 
                v-if="powers"
                :highlight="highlight"
                :xData="powers" 
                :yData="scaleindep">
            </scatter>
        </div>

        <div class="col-xs-4">
            <h4 class="text-xs-center">Mean connectivity</h4>
            <scatter 
                v-if="powers"
                :highlight="highlight"
                :xData="powers" 
                :yData="meank">
            </scatter>
        </div>
        </div>
    </div>
</div>
</template>

<script>
import Scatter from '../charts/Scatter'

export default {
    data() {
        return {
            powers: null,
            scaleindep: null,
            meank: null,
            loading: true,
            hovered: null
        }
    },

    components: {
        Scatter
    },

    props: ['name', 'selected'],

    methods: {
        pick(power) {
            const formData = new FormData()
            formData.append('power', power)
            $.ajax({
                type: 'POST',
                url: `${ROOTURL}/tresholds/${this.name}`,
                data: formData,
                async: true,
                cache: false,
                contentType: false,
                processData: false
            }).then(() => this.$emit('done', power))
        },
        getValues() {
            $.get(`${ROOTURL}/tresholds/${this.name}`).then(data => {
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
        name() {
            this.getValues()
        }
    },

    computed: {
        highlight() {
            if (this.hovered) {
                return this.hovered
            } else if (this.selected) {
                return this.selected
            } else {
                return null
            }
        }
    }
}
</script>

<style scoped>
.table > tbody {
    cursor: pointer;
}
</style>