<template>
<div class="modal" id="export-modal" tabindex="-1">
<div class="modal-dialog">
<div class="modal-content">
<div class="modal-body">

    <h5 class="modal-title">Export modules</h5>

    <div class="card-body">
        <div class="d-flex justify-content-center">
            <div class="btn-group">
                <button class="btn btn-secondary format" :class="{active: format == 'A'}" 
                        @click="format = 'A'">
                    <p>modules.csv</p>
                    <hr>
                    <div v-if="step > 4">
                        <p>gene,module,pvalue</p>
                        <p>gene,module,pvalue</p>
                    </div>
                    <div v-else>
                        <p>gene,module</p>
                        <p>gene,module</p>
                    </div>
                    <p>...</p>
                </button>
                <button class="btn btn-secondary format" :class="{active: format == 'B'}" 
                        @click="format = 'B'">
                    <p>module_A.txt</p>
                    <hr>
                    <p>gene</p>
                    <p>gene</p>
                    <p>...</p>
                </button>
            </div>
        </div>

        <div class="form-check m-3" style="text-align: center" :class="{'text-muted': !hasPValues}">
            <label class="form-check-label">
                <input class="form-check-input" type="checkbox" v-model="sigOnly" :disabled="!hasPValues">
                Show significant only
            </label>
        </div>


        <table class="table table-hover table-sm" style="margin-top: 1rem">
            <thead>
                <th></th>
                <th>Module</th>
                <th># genes</th>
            </thead>
            <tbody>
                <tr v-for="m in showModules" @click="select(m.module)">
                    <td v-show="format == 'A'">
                        <input type="checkbox" :checked="selected.includes(m.module)">
                    </td>
                    <td v-show="format == 'B'">
                        <input type="radio" :checked="module_ == m.module">
                    </td>
                    <td>{{ m.module }}</td>
                    <td>{{ m.size }}</td>
                </tr>
            </tbody>
        </table>
    </div>

    <div class="d-flex justify-content-between">
        <button class="btn btn-link" data-dismiss="modal">Cancel</button>
        <button class="btn btn-primary" @click="export_" :disabled="exportDisabled">Export</button>
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
            format: 'A',
            module_: null,
            selected: [],
            sigOnly: false
        }
    },

    props: ['name', 'step', 'modules'],

    methods: {
        select(module_) {
            if (this.format == 'A') {
                const index = this.selected.indexOf(module_)
                if (index > -1) this.selected.splice(index, 1) 
                else this.selected.push(module_)
            } else {
                this.module_ = module_
            }
        },
        export_() {
            let url = `${ROOTURL}/export/${this.name}?format=${this.format}`
            if (this.format == 'A') url += `&filter=${this.selected.join(',')}`
            else url += `&module=${this.module_}`
            window.open(url)
        }
    },

    computed: {
        exportDisabled() {
            return this.format == 'A' ? false : !this.module_
        },
        showModules() {
            return this.sigOnly ? this.modules.filter(m => m.pvalue && m.pvalue < .05) : 
                                  this.modules
        },
        hasPValues() {
            return this.step > 4
        }
    },

    watch: {
        name() {
            this.format =  'A'
            this.selected = []
            this.module_ = null
        }
    }
}
</script>

<style scoped>
.format {
    text-align: left;
}

.format p {
    margin: 0;
}

.format > hr {
    margin-top: 0;
}

.format > p:first-child {
    color: black;
    font-weight: bold;
}

.active {
    color: #292b2c !important;
    background-color: #e6e6e6 !important;
}
</style>

<style scoped>
tr {
    cursor: pointer;
}
</style>