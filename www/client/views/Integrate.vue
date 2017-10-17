<template>
<div>
    <div class="d-flex justify-content-between align-items-center top">
        <h3>WGCNA</h3>

        <div>
        </div>

        <router-link to="/" class="btn btn-secondary">
            Back
        </router-link>
    </div>

    <div class="row">
        <div class="col-3">
            <div class="card card-block block">
                <h5 class="card-title">Data</h5>

                <div class="btn-group">
                    <select v-model="plotName" class="btn btn-secondary w-100">
                        <option v-for="name in names">{{ name }}</option>
                    </select>
                    <button class="btn btn-primary" @click="addName">
                        +
                    </button>
                </div>

                <div>
                    <span v-for="name in plotNames">
                        {{ name }}
                    </span>
                </div>

                <button class="btn btn-primary" @click="plot">Plot</button>
            </div>
        </div>

        <div class="col-9">
            <div class="card card-block block">
                <correlation :data="plotData" :names="plotNames"></correlation>
            </div>
        </div>
    </div>
</div>
</template>

<script>
import Correlation from 'charts/Correlation'

export default {
    data() {
        return {
            plotName: null,
            // plotNames: [],
            plotNames: ['AUC Lipidomics', 'AUC Metabolomics'],
            plotData: null
        }
    },

    components: {
        Correlation
    },

    methods: {
        addName() {
            const index = this.plotNames.indexOf(this.plotName)
            if (index > -1) this.plotNames.splice(index, 1)
            else this.plotNames.push(this.plotName)
        },
        plot() {
            const names = this.plotNames
            $.getJSON(`${ROOTURL}/correlate`, {names}).then(data => {
                this.plotData = data
            })
        }
    },

    computed: {
        names() {
            return this.$store.state.names
        }
    },

    watch: {
        names() {
            this.plotName = this.names[0]
        }
    },

    created() {
        this.plotName = this.names[0]
    }
}
</script>

<style>
</style>