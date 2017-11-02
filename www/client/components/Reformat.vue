<template>
<div>
    <div v-if="!loading">
        <button class="btn btn-secondary" @click="transpose = !transpose">
            <span class="fa fa-retweet fa-lg"></span>
            Swap rows and columns
        </button>

        <div class="d-flex">
            <div class="m-5">
                <h5>Samples</h5>
                <list-editor :list="rowNames" @removed="updateRemovedRowNames"></list-editor>
            </div>

            <div class="m-5">
                <h5>Genes</h5>
                <list-editor :list="colNames" @removed="updateRemovedColNames"></list-editor>
            </div>
        </div>
    </div>

    <button class="btn btn-primary" @click="done" v-if="!loading">Done</button>

    <span class="fa fa-cog fa-spin fa-2x fa-fw" v-if="loading"></span>
</div>
</template>

<script>
import ListEditor from 'components/ListEditor'

export default {
    data() {
        return {
            loading: true,
            transpose: false,
            removedRowNames: [],
            removedColNames: []
        }
    },

    props: ['projectId'],

    components: {
        ListEditor
    },

    created() {
        $.get(`${ROOTURL}/projects/${this.projectId}/expression`).then(data => {
            this.rowNames = data.rowNames
            this.colNames = data.colNames
            this.loading = false
        }, () => {
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
                url: `${ROOTURL}/projects/${this.projectId}/expression`,
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
            console.log('kekd')
            const rowNames = this.rowNames
            this.rowNames = this.colNames
            this.colNames = rowNames
        }
    }
}
</script>