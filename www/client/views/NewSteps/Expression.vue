<template>
<div class="card card-body block mt-3" :class="{ disabled: disabled }">
    <div class="d-flex justify-content-between align-items-start">
        <h6 class="block-title text-uppercase">
            Expression data
        </h6>
    </div>

    <form class="mt-2" enctype="multipart/form-data" @submit.prevent="upload">
        <div class="d-flex align-items-center">
            <label class="custom-control custom-radio">
                <input name="expression-option" type="radio" class="custom-control-input" value="file" v-model="option">
                <span class="custom-control-label"></span>
            </label>
            <input type="file" class="form-control-file ml-2" name="expression" :disabled="option == 'link'">
        </div>
        <div class="d-flex align-items-center mt-3">
            <label class="custom-control custom-radio">
                <input name="expression-option" type="radio" class="custom-control-input" value="link" v-model="option">
                <span class="custom-control-label"></span>
            </label>
            <input class="form-control ml-2" placeholder="Direct link" name="expression-link" :disabled="option == 'file'">
        </div>
        <div class="form-group row mt-3">
            <label for="delim" class="col-sm-1 col-form-label">Delimiter</label>
            <div class="col-sm-1">
                <input type="text" class="form-control" id="delim" name="delim" placeholder="," />
            </div>
        </div>

        <button class="btn btn-light mt-2" type="submit" :disabled="uploading" v-if="!disabled">
            <font-awesome-icon icon="upload" />
            Upload / retrieve
        </button>
    </form>

    <div class="mt-4 mb-3" v-if="dims">
        <span v-if="transpose">
            Matrix contains <strong>{{ dims.samples }} features</strong> and <strong>{{ dims.features }} samples</strong>.
        </span>
        <span v-else>
            Matrix contains <strong>{{ dims.features }} features</strong> and <strong>{{ dims.samples }} samples</strong>.
        </span>
        <button class="btn btn-light" @click="transpose = !transpose" v-if="!disabled">
            <font-awesome-icon icon="retweet" size="lg" />
            Swap rows and columns
        </button>
    </div>

    <div v-if="dims">
        <font-awesome-icon icon="sync" spin v-if="evaluating" />
        <div v-else>
            <span>In terms of missing values:</span>
            <span v-if="evaluation.allOK">All OK</span>
            <div v-else>
                <list-popover name="bad samples" :list="transpose ? evaluation.badGenes : evaluation.badSamples"></list-popover>
                <list-popover name="bad features" :list="transpose ? evaluation.badSamples: evaluation.badGenes"></list-popover>
                These are removed from the expression file.
            </div>
        </div>
    </div>

    <div class="mt-4" v-if="!disabled && dims && !evaluating">
        <button class="btn btn-primary" @click="done" :disabled="loading">
            <font-awesome-icon icon="check" />
            OK
        </button>
    </div>
</div>
</template>

<script>
import ListPopover from 'components/ListPopover'

export default {
    data() {
        return {
            option: 'file',
            uploading: false,
            dims: null,
            transpose: false,
            evaluating: false,
            evaluation: null,
            loading: false
        }
    },

    props: {
        disabled: Boolean,
        project: String
    },

    components: {
        ListPopover
    },

    methods: {
        upload(event) {
            this.uploading = true
            this.dims = null
            this.transpose = false
            const formData = new FormData(event.target)
            this.$helpers.post(formData, this.project, 'expression')
            .then(data => {
                this.dims = { samples: data.samples, features: data.features }
                this.uploading = false
                this.evaluating = true
                this.checkSamplesGenes()
            }, () => {
                this.uploading = false
            })
        },
        checkSamplesGenes() {
            this.evaluating = true
            $.get(`${ROOTURL}/projects/${this.project}/goodsamplesgenes`).then(data => {
                this.allOK = data.allOK
                this.badSamples = data.badSamples
                this.badGenes = data.badGenes
                this.evaluation = { allOK: data.allOK, badSamples: data.badSamples, 
                    badGenes: data.badGenes}
                this.evaluating = false
            })
        },
        done() {
            if (!this.transpose) {
                this.$emit('done')
                return
            }
            this.loading = true
            const formData = new FormData()
            formData.append('transpose', this.transpose)
            this.$helpers.put(formData, this.project, 'expression')
            .then(() => {
                this.loading = false
                this.$emit('done')
            }, () => {
                this.loading = false
                alert('nope')
            })
        }
    }
}
</script>