<template>
<div class="card card-block">
    <div class="row">
        <h5 class="card-title">3. Module-genotype significance</h5>

        <div class="row" v-if="!pvalues">
            <div class="col-xs-3">
                <strong>Samples</strong>
                <ul>
                    <li v-for="sample in samples">{{ sample }}</li>
                </ul>
            </div>

            <div class="col-xs-3">
                <strong>Regex</strong><br>
                <input placeholder="regex" v-model="pattern">
            </div>

            <div class="col-xs-3">
                <strong>Groups</strong>
                <ul>
                    <li v-for="group in groups">{{ group }}</li>
                </ul>
            </div>

            <div class="col-xs-3">
                <button 
                    class="btn btn-primary" 
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
                            v-for="column in columns">{{ pvalues[column][i] | round(3) }}
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
            pattern: '^([A-Za-z\+-]+)',
            calculating: false,
            modules: null,
            pvalues: null
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
        }
    },

    computed: {
        groups() {
            if (!this.pattern) return []
            try {
                const re = new RegExp(this.pattern)
                return this.samples
                    .map(sample => re.exec(sample)[0])
                    .filter(sample => sample)
            } catch(e) {
                return []
            }
        },
        columns() {
            return this.pvalues ? Object.keys(this.pvalues).filter(x => x !='significance') : []
        }
    },

    created() {
        this.getSamples()
        if (this.step > 4) this.getPvalues()
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
</style>