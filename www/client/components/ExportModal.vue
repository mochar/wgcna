<template>
<div class="modal" id="export-modal" tabindex="-1">
<div class="modal-dialog">
<div class="modal-content">
<div class="modal-body">

    <h5 class="modal-title">Export modules</h5>

    <div class="card-block">
        <div class="d-flex justify-content-center">
            <div class="btn-group">
                <button class="btn btn-secondary format" :class="{active: format == 'A'}" 
                        @click="format = 'A'">
                    <p>modules.csv</p>
                    <hr>
                    <p>gene,module</p>
                    <p>gene,module</p>
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

        <table class="table table-hover table-sm" style="margin-top: 1rem">
            <thead>
                <th></th>
                <th>Module</th>
                <th># genes</th>
            </thead>
            <tbody>
                <tr v-for="m in modules" @click="select(m)">
                    <td v-show="format == 'A'">
                        <input type="checkbox" :checked="selected.includes(m)">
                    </td>
                    <td v-show="format == 'B'">
                        <input type="radio" :checked="module_ == m">
                    </td>
                    <td>{{ m }}</td>
                    <td>x</td>
                </tr>
            </tbody>
        </table>
    </div>

    <div class="d-flex justify-content-between">
        <button class="btn btn-link" data-dismiss="modal">Cancel</button>
        <button class="btn btn-primary">Export</button>
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
            modules: [],
            module_: null,
            selected: []
        }
    },

    props: ['name'],

    methods: {
        getColors() {
            if (this.name) {
                $.getJSON(`${ROOTURL}/export/${this.name}`).then(data => {
                    this.modules = data.modules
                })
            }
        },
        select(module_) {
            if (this.format == 'A') {
                const index = this.selected.indexOf(module_)
                if (index > -1) this.selected.splice(index, 1) 
                else this.selected.push(module_)
            } else {
                this.module_ = module_
            }
        },
        export() {
            $.getJSON(`${ROOTURL}/export/${this.name}`, {format: this.format}).then(() => {
                
            })
        }
    },

    created() {
        this.getColors()
    },

    watch: {
        name() {
            this.format =  'A'
            this.modules = []
            this.selected = []
            this.module_ = null
            this.getColors()
        }
    }
}
</script>

<style>
.format {
    text-align: left;
}

.format > p {
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