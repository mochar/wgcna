<template>
<div class="card card-block">
    <div class="row">
        <div class="card-title">
            <h5 style="display: inline-block">3. Module-genotype significance</h5>
            <button @click.prevent="showPvalues = false" class="btn btn-link float-xs-right" v-if="showPvalues">
                Return
            </button>
        </div>

        <div class="row" v-if="!showPvalues">
            <div class="col-xs-2 text-muted">
            </div>

            <div class="col-xs-5">
                <div v-for="(sample, i) in samples" style="display: flex; text-align: center">
                    <span style="flex: 1">{{ sample }}</span>
                    <input style="flex: 1" :value="groups[i]" @keydown="e => change(e, i)" />
                </div>
            </div>

            <div class="col-xs-3">
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

        <div id="heatmap" class="row" v-else>
            <div class="col-xs-2">
                <span class="flex col row-label" 
                      v-for="(module, i) in modules"
                      :style="{ 'border-right': `5px solid ${module.substring(2)}` }">
                    {{ module.substring(2) }}
                    <span v-if="pvalues['significance'][i] < 0.05">*</span>
                </span>
            </div>
            <div class="col-xs-10">
                <div>
                    <div v-for="(module, i) in modules" class="flex">
                        <span class="col sig-cell">
                            {{ pvalues['significance'][i] | round(3) }}
                        </span>
                        <span 
                            class="col"
                            :style="pvalToStyle(pvalues[column][i])" 
                            v-for="column in columns">
                            <span v-if="pvalues[column][i] !== 'NA'">{{ pvalues[column][i] | round(3) }}</span>
                        </span>
                    </div>
                </div>
                <div class="flex">
                    <span class="col-label">Significance</span>
                    <span class="col-label" v-for="column in columns">
                        {{ column }}
                    </span>
                </div>
            </div>
        </div>
    </div>
</div> 
</template>

<script>
export default {
    data() {
        return {
            samples: [],
            groups: [],
            pattern: '^([A-Za-z\+-]+)',
            calculating: false,
            modules: null,
            pvalues: null,
            showPvalues: false
        }
    },

    props: ['name', 'step'],

    methods: {
        calculate() {
            this.calculating = true
            const formData = new FormData()
            formData.append('groups', this.groups)
            $.post({
                url: `${ROOTURL}/genotype/${this.name}`,
                data: formData,
                async: true,
                cache: false,
                contentType: false,
                processData: false
            }).then(data => {
                this.calculating = false
                this.modules = data.modules
                this.pvalues = data.pvalues
                this.showPvalues = true
                this.$emit('done')
            })
        },
        getSamples() {
            $.get(`${ROOTURL}/expression/${this.name}`).then(data => {
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
        }
    },

    computed: {
        columns() {
            return this.pvalues ? Object.keys(this.pvalues).filter(x => x !='significance') : []
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
    margin: 1rem 2rem 4rem 2rem;
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