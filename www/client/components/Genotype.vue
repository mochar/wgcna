<template>
<div class="card card-body block">
    <div class="d-flex justify-content-between align-items-start">
        <h6 class="block-title text-uppercase">
            Module Significance
            <font-awesome-icon icon="cog" spin v-if="loading" />
        </h6>
        <div class="text-muted d-flex align-items-center">
            <div class="dropdown ml-2">
                <button class="btn btn-link text-muted pr-1 pt-0 pb-0" data-toggle="dropdown">
                    <font-awesome-icon icon="ellipsis-v" />
                </button>
                <div class="dropdown-menu  dropdown-menu-right">
                    <h6 class="dropdown-header">Download plot</h6>
                    <a class="dropdown-item" href="#" @click.prevent="downloadPlot">
                        Significance
                    </a>
                </div>
            </div>
        </div>
    </div>

    <p class="card-text">
        The trait is statistically tested for a significant difference in values between groups.
    </p>

    <div v-if="!loading" class="mt-2">
        <!-- <dl class="row" style="margin: 1rem">
            <dt class="col-2">Comparison</dt>
            <dd class="col-10">
                <ul class="nav justify-content-left">
                    <li class="nav-item" v-for="column in columns" :key="column">
                        <a class="nav-link" :class="{'active': column == selectedColumn}" 
                            href="#" @click.prevent="selectColumn(column)">{{ column }}</a>
                    </li>
                </ul>
            </dd>
            <dt class="col-2">Options</dt>
            <dd class="col-10">
                <div class="form-check form-check-inline">
                    <label class="custom-control custom-checkbox">
                        <input class="custom-control-input" type="checkbox" v-model="sigOnly">
                        <span class="custom-control-indicator"></span>
                        <span class="custom-control-description">Show signficant modules only</span>
                    </label>
                </div>
                <div class="form-check form-check-inline">
                    <label class="custom-control custom-checkbox">
                        <input class="custom-control-input" type="checkbox" v-model="columnOnly">
                        <span class="custom-control-indicator"></span>
                        <span class="custom-control-description">Show comparsion groups only</span>
                    </label>
                </div>
            </dd>
        </dl> -->
        <significance
            :pvalues="pvalues" 
            :eigengenes="eigengenes"
            :samples="samples"
            :modules="modules"
            :groups="groups"
            :column="selectedColumn"
            :sigOnly="sigOnly"
            :columnOnly="columnOnly">
        </significance>
        <!-- <button @click.prevent="showPvalues = false" class="btn btn-light" v-if="showPvalues"> -->
        <button @click.prevent="$emit('back')" class="btn btn-light">
            <font-awesome-icon icon="angle-double-left" />
            Return
        </button>
    </div>
    <span v-else>loading</span>
</div> 
</template>

<script>
import Significance from 'charts/Significance'

export default {
    data() {
        return {
            samples: [],
            groups: [],
            modules: null,
            pvalues: null,
            eigengenes: null,
            selectedColumn: null,
            sigOnly: false,
            columnOnly: false,
            loading: true
        }
    },

    components: {
        Significance
    },

    props: ['project', 'update'],

    methods: {
        getSamples() {
            return $.get(`${ROOTURL}/projects/${this.project.id}/expression`).then(data => {
                this.samples = data.rowNames
            })
        },
        getPvalues() {
            return $.get(`${ROOTURL}/projects/${this.project.id}/genotype`).then(data => {
                this.modules = data.modules
                this.pvalues = data.pvalues
                this.eigengenes = data.eigengenes
                this.groups = data.groups
            })
        },
        selectColumn(column) {
            this.selectedColumn = this.selectedColumn == column ? null : column
        },
        setUp() {
            this.getSamples().then(() => {
                this.getPvalues().then(() => {
                    this.loading = false
                })
            })
        },
        downloadPlot() {
            const svgEl = $(this.$el).find('svg')[0]
            this.$helpers.downloadSvg(svgEl, 'significance')
        }
    },

    computed: {
        columns() {
            const columns = this.pvalues ? Object.keys(this.pvalues).filter(x => x !='significance') : []
            // this.selectedColumn = columns[0]
            return columns
        }
    },

    watch: {
        project() {
            if (this.update) {
                // this.loading = true
                // this.showPvalues = false
                // this.setUp()
            }
        }
    },

    created() {
        this.setUp()
    }
}
</script>
