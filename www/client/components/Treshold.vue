<template>
<div class="card card-block block">
    <h6 class="block-title">SOFT TRESHOLD</h6>

    <span class="fa fa-cog fa-spin fa-2x fa-fw" v-if="loading"></span>
    <div class="row" v-else>
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

    props: ['project', 'selected'],

    methods: {
        pick(power) {
            const formData = new FormData()
            formData.append('power', power)
            $.ajax({
                type: 'POST',
                url: `${ROOTURL}/projects/${this.project.id}/tresholds`,
                data: formData,
                async: true,
                cache: false,
                contentType: false,
                processData: false
            }).then(() => {
                this.$emit('done', power)
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
        name() {
            this.getValues()
        }
    },

    computed: {
        highlight() {
            if (this.hovered) {
                return this.hovered
            } else if (this.project.power) {
                return this.project.power
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