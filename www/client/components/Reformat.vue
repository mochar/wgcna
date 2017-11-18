<template>
<div class="card card-body">
    <h6 class="block-title">
        REFORMAT
        <!-- <span class="fa fa-lg fa-cog fa-spin float-right" v-if="loading"></span> -->
        <button class="btn btn-light float-right" @click="transpose = !transpose">
            <span class="fa fa-retweet fa-lg"></span>
            Swap rows and columns
        </button>
    </h6>

    <div class="d-flex" v-if="!loading">
        <delete-editor 
            :list="rowNames" 
            :removedIndices="removedRowIndices" 
            @selected="i => selectRemovedIndex('row', i)"
            @removed="indices => removedRowIndices = indices">
            Samples
        </delete-editor>
        <delete-editor 
            :list="colNames" 
            :removedIndices="removedColIndices"
            @selected="i => selectRemovedIndex('col', i)"
            @removed="indices => removedColIndices = indices">
            Genes
        </delete-editor>
    </div>

    <div class="block-action-div">
        <button class="btn btn-light" @click="done" v-if="!loading">
            <span class="fa fa-check"></span>
            Done
        </button>
    </div>

    <span class="fa fa-cog fa-spin fa-2x fa-fw" v-if="loading"></span>
</div>
</template>

<script>
import DeleteEditor from 'components/DeleteEditor'

export default {
    data() {
        return {
            loading: true,
            transpose: false,
            rowNames: [],
            colNames: [],
            removedRowIndices: [],
            removedColIndices: []
        }
    },

    props: ['projectId'],

    components: {
        DeleteEditor
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
            formData.append('row', this.removedRowIndices.map(i => this.rowNames[i]))
            formData.append('col', this.removedColIndices.map(i => this.colNames[i]))
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
        selectRemovedIndex(dim, index) {
            if (dim === 'row') {
                const i = this.removedRowIndices.indexOf(index)
                if (i === -1) this.removedRowIndices.push(index)
                else this.removedRowIndices.splice(i, 1)
            } else {
                const i = this.removedColIndices.indexOf(index)
                if (i === -1) this.removedColIndices.push(index)
                else this.removedColIndices.splice(i, 1)
            }
        }
    },

    watch: {
        transpose() {
            const rowNames = this.rowNames
            this.rowNames = this.colNames
            this.colNames = rowNames

            const rowIndices = this.removedRowIndices
            this.removedRowIndices = this.removedColIndices
            this.removedColIndices = rowIndices
        }
    }
}
</script>