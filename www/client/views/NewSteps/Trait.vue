<template>
<div class="card card-body block mt-3" :class="{ disabled: disabled }">
    <div class="d-flex justify-content-between align-items-start">
        <h6 class="block-title text-uppercase">
            Traits
        </h6>
    </div>

    <form class="mt-2" enctype="multipart/form-data" @submit.prevent="upload">
        <input type="file" class="form-control-file" name="trait">

        <div class="form-group row mt-3">
            <label for="delim" class="col-sm-1 col-form-label">Delimiter</label>
            <div class="col-sm-1">
                <input type="text" class="form-control" id="delim" name="delim" placeholder="," />
            </div>
        </div>

        <button class="btn btn-light mt-2" type="submit" :disabled="uploading" v-if="!disabled">
            <span class="fa fa-upload"></span>
            Upload / retrieve
        </button>

        <span class="text-danger" style="font-weight: bold">{{ error }}</span>
    </form>

    <div class="d-flex align-items-center mt-4" v-if="types">
        <table class="table table-sm">
            <thead>
                <tr>
                    <th scope="col"></th>
                    <th v-for="(column, i) in data.columns" :key="i" scope="col">
                        {{ column }}
                        <a href="#" @click.prevent="switchType(i)" class="badge badge-pill badge-primary">
                            <span v-if="types[i] === 'N'" title="Nominal (category)">Nominal</span>
                            <span v-else title="Continuous (numeric)">Continuous</span>
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

    <div class="mt-3" v-if="types && !disabled">
        <button class="btn btn-primary" @click="done" :disabled="loading">
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
            uploading: false,
            loading: false,
            types: null,
            error: ''
        }
    },

    props: {
        disabled: Boolean,
        project: String
    },

    methods: {
        upload(event) {
            this.uploading = true
            const formData = new FormData(event.target)
            $.post({
                url: `${ROOTURL}/projects/${this.project}/trait`,
                data: formData,
                async: true,
                cache: false,
                contentType: false,
                processData: false
            }).then(data => {
                this.data = JSON.parse(data)
                this.types = this.$helpers.range(this.data.columns.length).map(() => 'N')
                this.error = ''
                this.uploading = false
            }, data => {
                this.error = data.responseJSON.error
                this.uploading = false
            })
        },
        switchType(index) {
            const newType = this.types[index] === 'N' ? 'C' : 'N'
            this.$set(this.types, index, newType)
        },
        done() {
            this.loading = true
            const formData = new FormData()
            let continuesIndices = []
            for (let index = 0; index < this.types.length; index++) {
                if (this.types[index] === 'C')
                    continuesIndices.push(index)
            }
            formData.append('continues', continuesIndices)
            $.ajax({
                url: `${ROOTURL}/projects/${this.project}/trait`,
                type: 'PUT',
                data: formData,
                async: true,
                cache: false,
                contentType: false,
                processData: false
            }).then(() => {
                this.$emit('done')
                this.loading = false
            }, () => {
                this.loading = false
                alert('nope')
            })
        }
    }
}
</script>

