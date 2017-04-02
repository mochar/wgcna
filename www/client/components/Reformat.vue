<template>
<div>
    <div class="row" v-if="!loading">
        <div class="col-6">
            <label class="form-check-label">
                <input class="form-check-input" type="checkbox" v-model="transpose"> Transpose
            </label>
            <br/>
        </div>

        <div class="col-3">
            <h5>Rows</h5>
            <list-editor :list="rowNames" @removed="updateRemovedRowNames"></list-editor>
        </div>

        <div class="col-3">
            <h5>Columns</h5>
            <list-editor :list="colNames" @removed="updateRemovedColNames"></list-editor>
        </div>
    </div>

    <button class="btn btn-primary" @click="done" v-if="!loading">Done</button>

    <span class="fa fa-cog fa-spin fa-2x" v-if="loading"></span>
</div>
</template>

<script>
import ListEditor from '../components/ListEditor'

export default {
    data() {
        return {
            loading: true,
            transpose: false,
            removedRowNames: [],
            removedColNames: []
        }
    },

    props: ['name'],

    components: {
        ListEditor
    },

    created() {
        $.get(`${ROOTURL}/expression/${this.name}`).then(data => {
            this.rowNames = data.rowNames
            this.colNames = data.colNames
            this.loading = false
        })
    },

    methods: {
        done() {
            const formData = new FormData()
            formData.append('row', this.removedRowNames)
            formData.append('col', this.removedColNames)
            formData.append('transpose', this.transpose)
            $.ajax({
                url: `${ROOTURL}/expression/${this.name}`,
                type: 'PUT',
                data: formData,
                async: true,
                cache: false,
                contentType: false,
                processData: false
            }).then(() => {
                console.log('success')
                this.$emit('done')
            }, () => {
                console.log('nope')
                alert('nope')
            })
        },
        updateRemovedRowNames(removed) {
            this.removedRowNames = removed
        },
        updateRemovedColNames(removed) {
            this.removedColNames = removed
        }
    },

    watch: {
        transpose() {
            const rowNames = this.rowNames
            this.rowNames = this.colNames
            this.colNames = rowNames
        }
    }
}
</script>