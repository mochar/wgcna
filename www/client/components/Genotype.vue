<template>
<div class="card card-block block">
    <h6 class="block-title">
        Module-genotype significance
        <!-- <span class="fa fa-cog fa-spin" v-if="loading"></span> -->
    </h6>

    <div>
        <div class="row" v-if="!showPvalues">
            <div class="col-2 text-muted">
            </div>

            <div class="col-5">
                <div v-for="(sample, i) in samples" :key="sample" style="display: flex; text-align: center">
                    <span style="flex: 1">{{ sample }}</span>
                    <input style="flex: 1" :value="groups[i]" @keydown="e => change(e, i)" />
                </div>
            </div>

            <div class="col-3">
                <div class="well">
                    <strong>Apply regex</strong><br>
                    <input placeholder="regex" v-model="pattern">
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
            <button @click.prevent="showPvalues = false" class="btn btn-link float-right" v-if="showPvalues">
                <span class="fa fa-angle-double-left"></span>
                Return
            </button>
        </div>

        <!-- <div id="heatmap" class="row" v-else>
            <div class="col-2">
                <span class="flex col row-label" 
                      :title="module.substring(2)"
                      v-for="(module, i) in modules"
                      :key="module"
                      :style="{ 'border-right': `5px solid ${module.substring(2)}` }">
                    {{ module.substring(2) }}
                    <span v-if="pvalues['significance'][i] < 0.05" style="position: absolute">*</span>
                </span>
            </div>
            <div class="col-10">
                <div>
                    <div v-for="(module, i) in modules" :key="module" class="flex">
                        <span class="col sig-cell">
                            {{ pvalues['significance'][i] | round(3) }}
                        </span>
                        <span 
                            class="col"
                            :style="pvalToStyle(pvalues[column][i])" 
                            v-for="column in columns"
                            :key="column">
                            <span v-if="pvalues[column][i] !== 'NA'">{{ pvalues[column][i] | round(3) }}</span>
                        </span>
                    </div>
                </div>
                <div class="flex">
                    <span class="col-label">Significance</span>
                    <span class="col-label" v-for="column in columns" :key="column">
                        {{ column }}
                    </span>
                </div>
            </div>
        </div> -->
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
            columnOnly: false
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
            $.get(`${ROOTURL}/projects/${this.project.id}/expression`).then(data => {
                this.samples = data.rowNames
            })
        },
        getPvalues() {
            $.get(`${ROOTURL}/genotype/${this.name}`).then(data => {
                this.modules = data.modules
                this.pvalues = data.pvalues
            })
        },
        pvalToStyle(pvalue) {
            if (pvalue === 'NA' || pvalue > .05) return { 'background-color': 'white'}
            else return { 'background-color': '#ED4337', color: 'black' }
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
            this.groups[i] = e.srcElement.value
        },
        selectColumn(column) {
            this.selectedColumn = this.selectedColumn == column ? null : column
        }
    },

    computed: {
        columns() {
            const columns = this.pvalues ? Object.keys(this.pvalues).filter(x => x !='significance') : []
            // this.selectedColumn = columns[0]
            return columns
        }
    },

    created() {
        this.getSamples()
        if (this.step > 4) {
            this.getPvalues()
            this.showPvalues = true
        } 
    }
}
</script>

<style scoped>
#heatmap {
    margin: 0 2rem 4rem 2rem;
}

.flex {
    display: flex;
}

.col {
    flex: 1;
    padding: .2rem 1.5rem;
}

.col-label {
    flex: 1;
    transform: rotate(-40deg) translate(-65%, -50%);
    text-align: right;
}

.row-label {
    text-align: right;
    display: block;
}

.sig-cell {
    border-right: 1px solid #bbb;
}

.well {
    background-color: #efefef;
    padding: .5rem 1rem 1rem;
}
</style>