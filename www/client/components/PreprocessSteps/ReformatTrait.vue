<template>
<div>
    <div class="preprocess-component">
        <span class="fa fa-refresh fa-spin" v-if="loading"></span>
        <div class="d-flex align-items-center" v-else>
            <table class="table table-sm">
                <thead>
                    <tr>
                        <th scope="col"></th>
                        <th v-for="(column, i) in data.columns" :key="i" scope="col">
                            {{ column }}
                            <a href="#" @click.prevent="switchType(i)" class="badge badge-pill badge-primary">
                                <span v-if="types[i] === 'N'" title="Nominal (category)">N</span>
                                <span v-else title="Continuous (numeric)">C</span>
                            </a>
                        </th>
                    </tr>
                </thead>
                <tbody>
                    <tr v-for="(index, i) in data.index" :key="i">
                        <th scope="row">{{ index }}</th>
                        <td v-for="d in data.data[i]" :key="d">
                            {{ d }}
                        </td>
                    </tr>
                </tbody>
            </table>
        </div>
    </div>
    <div class="mt-2" v-show="!loading">
        <button class="btn btn-light" :disabled="busy" @click="go">
            <span class="fa fa-check"></span>
            OK
        </button>
    </div>
</div>
</template>

<script>
export default {
    data() {
        return {
            loading: true, // setting up
            busy: false, // doing the thing
            types: [],
        }
    },

    props: ['project'],

    methods: {
        go() {
            this.busy = true
            const formData = new FormData()
            let continuesIndices = []
            for (let index = 0; index < this.types.length; index++) {
                if (this.types[index] === 'C')
                    continuesIndices.push(index)
            }
            formData.append('continues', continuesIndices)
            $.ajax({
                url: `${ROOTURL}/projects/${this.project.id}/trait`,
                type: 'PUT',
                data: formData,
                async: true,
                cache: false,
                contentType: false,
                processData: false
            }).then(() => {
                this.$emit('done')
            }, () => {
                this.busy = false
                alert('nope')
            })
        },
        switchType(index) {
            const newType = this.types[index] === 'N' ? 'C' : 'N'
            this.$set(this.types, index, newType)
        }
    },

    computed: {
    },

    created() {
        $.get(`${ROOTURL}/projects/${this.project.id}/trait`).then(data => {
            this.types = this.$helpers.range(data.columns.length).map(() => 'N')
            this.data = data
            this.loading = false
        }, () => {
            this.loading = false
        })
    }
}
</script>