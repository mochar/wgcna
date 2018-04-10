<template>
<div>
    <div class="card card-body block">
        <div class="d-flex justify-content-between align-items-start">
            <h6 class="block-title text-uppercase">
                Cross-correlate
            </h6>
        </div>
        <p class="card-text">
            Correlate module eigengenes of paired sets.
        </p>
        <div class="row">
            <div class="col-5">
                <add-project-block 
                    :deletable="false"
                    :showAdd="false"
                    :projects="filteredProjects"
                    @selected="p => $set(selected, 0, p)">
                </add-project-block>
                <add-project-block 
                    :deletable="false"
                    :showAdd="true"
                    :projects="filteredProjects"
                    :init="1"
                    @selected="p => $set(selected, 1, p)">
                </add-project-block>
            </div>
        </div>
        <div>
            <button class="btn btn-light" @click="plot" :disabled="loading">
                <span class="fa fa-refresh fa-spin fa-fw" v-if="loading"></span>
                <span class="fa fa-check fa-fw" v-else></span>
                Plot
            </button>
        </div>
    </div>

    <div class="card card-body block mt-2">
        <correlation :data="plotData" :names="[]"></correlation>
    </div>
</div>
</template>

<script>
import Correlation from 'charts/Correlation'
import AddProjectBlock from 'components/Integrate/AddProjectBlock'
import { mapState, mapActions, mapGetters } from 'vuex'

export default {
    data() {
        return {
            plotData: null,
            selected: [],
            loading: false
        }
    },

    components: {
        Correlation,
        AddProjectBlock
    },

    methods: {
        plot() {
            this.loading = true
            const selectedIds = this.selected.map(d => d.id)
            console.log(selectedIds)
            $.getJSON(`${ROOTURL}/crosscorrelate`, {projects: selectedIds}).then(data => {
                this.plotData = data
                this.loading = false
            })
        }
    },

    computed: {
        ...mapState(['projects']),
        names() {
            return this.$store.state.names
        },
        filteredProjects() {
            console.log('kek')
            const chosen = this.selected.filter(d => d).map(d => d.id)
            return this.projects.filter(d => !chosen.includes(d.id))
        }
    },

    created() {
        this.project = this.projects[0]
    }
}
</script>

<style>
</style>