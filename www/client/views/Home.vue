<template>
<div>
    <div class="d-flex justify-content-between align-items-center top">
        <h3>WGCNA</h3>

        <div class="btn-group">
            <button class="btn btn-primary" style="border-top-width: 1px" 
                    @click="generateReport">
                Generate report
            </button>
            <button class="btn btn-secondary" data-toggle="modal" data-target="#export-modal"
                    :disabled="step < 4">
                Export modules
            </button>
            <select v-model="name" id="name-select" class="btn btn-secondary">
                <option v-for="name in names">{{ name }}</option>
            </select>
        </div>

        <router-link to="/new" class="btn btn-primary">
            <span class="fa fa-plus"></span>
            New
        </router-link>
    </div>

    <treshold 
        :name="name" 
        :selected="power" 
        v-if="step > 0" 
        @done="x => { power = x; step = 2 }">
    </treshold>
    <cluster 
        :name="name" 
        :power="power"
        :step="step"
        v-if="step > 1"
        @cutting="step = 3"
        @done="step = 4">
    </cluster>
    <genotype
        :name="name" 
        :step="step"
        @done="step = 5"
        v-if="step > 3">
    </genotype>

    <export-modal :name="name" v-if="step > 3"></export-modal>
</div>
</template>

<script>
import Treshold from '../components/Treshold'
import Cluster from '../components/Cluster'
import Genotype from '../components/Genotype'
import Annotation from '../components/Annotation'
import ExportModal from 'components/ExportModal'

export default {
    data() {
        return {
            name: null,
            names: [],
            power: null,
            step: 0
        }
    },

    components: {
        Treshold,
        Cluster,
        Genotype,
        Annotation,
        ExportModal
    },

    methods: {
        generateReport() {
            const url = `${ROOTURL}/report/${this.name}`
            window.open(url)
        }
    },

    watch: {
        name() {
            this.step = 0
            $.getJSON(`${ROOTURL}/info/${this.name}`).then(data => {
                this.power = data.power
                this.step = data.step
            })
        }
    },

    created() {
        $.getJSON(`${ROOTURL}/expression/`).then(data => {
            this.names = data.names.sort((a, b) => a < b ? -1 : 1)
            if (this.names.length > 0) this.name = this.names[0]
            else this.$router.push('/new')
        })
    }
}
</script>

<style>
#name-select:active:hover {
    background-color: white;
}

.block {
    margin-bottom: 1rem;
}

.top {
    margin-bottom: 1rem;
}
</style>