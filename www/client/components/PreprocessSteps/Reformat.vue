<template>
<div>
    <span class="fa fa-refresh fa-spin" v-if="loading"></span>
    <div v-else>
        <reformat-popover 
            name="Samples"
            :removedIndices="removedRowIndices"
            :list="rowNames"
            @selected="i => selectRemovedIndex('row', i)"
            @removed="indices => removedRowIndices = indices">
        </reformat-popover>
        <reformat-popover 
            :name="cols"
            :removedIndices="removedColIndices"
            :list="colNames"
            @selected="i => selectRemovedIndex('col', i)"
            @removed="indices => removedColIndices = indices">
        </reformat-popover>
        <button class="btn btn-light" @click="transpose = !transpose">
            <span class="fa fa-retweet fa-lg"></span>
            Swap rows and columns
        </button>
    </div>
</div>
</template>

<script>
import ReformatPopover from 'components/PreprocessSteps/ReformatPopover'

export default {
    data() {
        return {
            loading: true,
            transpose: false,
            rowNames: null,
            colNames: null,
            removedRowIndices: [],
            removedColIndices: []
        }
    },

    props: ['projectId', 'go', 'url', 'cols'],

    components: {
        ReformatPopover
    },

    methods: {
        done() {
            const formData = new FormData()
            formData.append('row', this.removedRowIndices.map(i => this.rowNames[i]))
            formData.append('col', this.removedColIndices.map(i => this.colNames[i]))
            formData.append('transpose', this.transpose)
            $.ajax({
                url: `${ROOTURL}/projects/${this.projectId}/${this.url}`,
                type: 'PUT',
                data: formData,
                async: true,
                cache: false,
                contentType: false,
                processData: false
            }).then(() => {
                this.$emit('done')
            }, () => {
                alert('nope')
            })
        },
        getSamplesGenes() {
            $.get(`${ROOTURL}/projects/${this.projectId}/${this.url}`).then(data => {
                this.rowNames = data.rowNames
                this.colNames = data.colNames
            }, () => {
            }).then(() => {
                this.loading = false
                this.$emit('loaded')
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
        },
        go() {
            if (this.go) this.done()
        }
    },

    created() {
        this.getSamplesGenes()
    }
}
</script>
