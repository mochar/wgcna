<template>
<div class="card card-block">
    <div class="row">
        <h5 class="card-title">3. Module-genotype significance</h5>

        <div class="row">
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

        <div v-if="pvalues" style="overflow-x: auto">
            <table class="table">
                <thead>
                    <th v-for="module in modules">{{ module.substring(2) }}</th>
                </thead>
                <tbody>
                    <tr>
                        <td v-for="pvalue in pvalues">{{ pvalue|round(3) }}</td>
                    </tr>
                </tbody>
            </table>
        </div>
    </div>
</div> 
</template>

<script>
export default {
    data() {
        return {
            samples: [],
            levels: [],
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
                this.levels = [...new Set(this.samples)]
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
        }
    },

    created() {
        this.getSamples()
        if (this.step > 4) this.getPvalues()
    }
}
</script>