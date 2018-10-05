<template>
<page>
    <div class="card card-body block">
        <div class="d-flex justify-content-between align-items-start">
            <h6 class="block-title text-uppercase">
                Cross-correlate
            </h6>
        </div>
        <p class="card-text">
            Correlate module eigengenes of paired sets.
        </p>
        <div>
            <add-project-block 
                :deletable="false"
                :showAdd="false"
                :projects="filteredProjects"
                @selected="p => $set(selected, 0, p)">
            </add-project-block>
            <add-project-block 
                :deletable="false"
                :showAdd="n_projects == 2"
                :projects="filteredProjects"
                :init="1"
                @selected="p => $set(selected, 1, p)"
                @add="n_projects++">
            </add-project-block>
            <add-project-block 
                v-for="i in $helpers.range(2, n_projects)"
                :key="i"
                :deletable="true"
                :showAdd="n_projects == i + 1"
                :projects="filteredProjects"
                @selected="p => $set(selected, i, p)"
                @add="n_projects++">
            </add-project-block>
            <div class="d-flex align-items-center mt-3">
                <label class="mr-2">Minimum correlation</label>
                <div class="form-group mr-2">
                    <input type="number" class="form-control" id="min-correlation" 
                           placeholder="0.5" step=".1" min="0" max="1">
                </div>
            </div>
        </div>
        <div>
            <button class="btn btn-light" @click="plot" :disabled="loading">
                <font-awesome-icon icon="sync" spin fixed-width v-if="loading" />
                <font-awesome-icon icon="check" fixed-width v-else />
                Plot
            </button>
        </div>
    </div>

    <!-- <span v-if="matching">{{ matching }}</span> -->

    <div class="card card-body block mt-2 mb-5" style="border: none">
        <svg id="cross-plot" v-show="show"></svg>
    </div>
</page>
</template>

<script>
import AddProjectBlock from 'components/Integrate/AddProjectBlock'
import Page from './Page'
import dendrogram from 'charts/Dendrogram3.js'
import { mapState, mapActions, mapGetters } from 'vuex'
import Vue from 'vue'

export default {
    data() {
        return {
            show: false,
            selected: [],
            loading: false,
            n_projects: 2,
            matching: null
        }
    },

    components: {
        AddProjectBlock,
        Page
    },

    methods: {
        plot() {
            this.loading = true
            const selectedIds = this.selected.map(d => d.id)
            $.getJSON(`${ROOTURL}/crosscorrelate`, {projects: selectedIds}).then(data => {
                this.matching = data.matching
                this.data = data
                this.show = true
                const minCorrelation = $('#min-correlation').val() || 0.5
                $('#cross-plot').empty()
                const chart = dendrogram({
                    selector: '#cross-plot',
                    data: data.data.map(d => d.clusterData),
                    names: data.data.map(d => d.project.name),
                    ids: data.data.map(d => d.project.id),
                    corrs: data.crosscorrs.filter(d => Math.abs(d.value) >= minCorrelation),
                    ratio: 0.8
                })
                Vue.nextTick(() => {
                    chart.update()
                    this.loading = false
                })
            })
        }
    },

    computed: {
        ...mapState(['projects']),
        names() {
            return this.$store.state.names
        },
        filteredProjects() {
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
img {
    max-width: 80%;
    max-height: 80%;
}

text {
    font-size: 12px;
}

line {
    shape-rendering: crispEdges;
}
</style>