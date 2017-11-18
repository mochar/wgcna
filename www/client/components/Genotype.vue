<template>
<div class="card card-body block">
    <h6 class="block-title text-uppercase">
        Module Significance
        <span class="fa fa-cog fa-spin" v-if="loading"></span>
    </h6>

    <div v-if="!loading">
        <div class="row" v-if="!showPvalues">
            <div class="col-2 text-muted">
            </div>

            <div class="col-5">
                <div v-for="(sample, i) in samples" :key="sample" style="display: flex; text-align: center">
                    <span style="flex: 1">{{ sample }}</span>
                    <input type="text" style="flex: 1" :value="groups[i]" @keydown="e => change(e, i)" />
                </div>
            </div>

            <div class="col-3">
                <div class="well">
                    <strong>Apply regex</strong><br>
                    <input type="text" placeholder="regex" v-model="pattern">
                    <button class="btn btn-secondary" style="margin-top: .5rem"
                            @click="applyRegex">Apply</button>
                </div>

                <button 
                    style="margin-top: 1rem;"
                    class="btn btn-primary btn-block"
                    :disabled="calculating"
                    @click="calculate">Calculate significance
                </button>
            </div>
        </div>

        <div v-else>
            <dl class="row" style="margin: 1rem">
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
                        <label class="form-check-label">
                            <input class="form-check-input" type="checkbox" value="" v-model="sigOnly">
                            Show signficant modules only
                        </label>
                    </div>
                    <div class="form-check form-check-inline">
                        <label class="form-check-label">
                            <input class="form-check-input" type="checkbox" value="" v-model="columnOnly">
                            Show comparsion groups only
                        </label>
                    </div>
                </dd>
            </dl>
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
            <button @click.prevent="showPvalues = false" class="btn btn-light" v-if="showPvalues">
                <span class="fa fa-angle-double-left"></span>
                Return
            </button>
        </div>
    </div>
</div> 
</template>

<script>
import Significance from 'charts/Significance'

export default {
    data() {
        return {
            samples: [],
            groups: [],
            pattern: '^([A-Za-z\+-]+)',
            calculating: false,
            modules: null,
            pvalues: null,
            eigengenes: null,
            showPvalues: false,
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
        calculate() {
            this.calculating = true
            const formData = new FormData()
            formData.append('groups', this.groups)
            $.post({
                url: `${ROOTURL}/projects/${this.project.id}/genotype`,
                data: formData,
                async: true,
                cache: false,
                contentType: false,
                processData: false
            }).then(data => {
                this.calculating = false
                this.modules = data.modules
                this.pvalues = data.pvalues
                this.eigengenes = data.eigengenes
                this.showPvalues = true
                // this.$emit('done')
            }, () => {
                this.calculating = false
            })
        },
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
        applyRegex() {
            if (!this.pattern) return
            try {
                const re = new RegExp(this.pattern)
                this.groups = this.samples
                    .map(sample => re.exec(sample)[0])
                    .filter(sample => sample)
            } catch(e) {
            }
        },
        change(e, i) {
            this.groups[i] = e.target.value
        },
        selectColumn(column) {
            this.selectedColumn = this.selectedColumn == column ? null : column
        },
        setUp() {
            this.getSamples().then(() => {
                if (this.project.step > 4) {
                    this.getPvalues().then(() => {
                        this.showPvalues = true
                        this.loading = false
                    })
                } else {
                    this.loading = false
                }
            })
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
                this.loading = true
                this.showPvalues = false
                this.setUp()
            }
        }
    },

    created() {
        this.setUp()
    }
}
</script>