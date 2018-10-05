<template>
<div class="card card-body block" :class="{ disabled: disabled }">
    <div class="d-flex justify-content-between align-items-start">
        <h6 class="block-title text-uppercase">
            Project information
        </h6>
    </div>

    <form class="mt-2 mb-1" enctype="multipart/form-data" @submit.prevent="submit">
        <div class="form-row">
            <div class="col-5">
                <input type="text" name="name" class="form-control" placeholder="Name">
            </div>
            <div class="col-7">
                <input type="text" name="description" class="form-control" placeholder="Description">
            </div>
        </div>
        <div class="form-row pl-2 mt-3">
            <div class="form-check form-check-inline" v-for="omic in ['transcriptomics', 'lipidomics', 'metabolomics']" :key="omic">
                <input class="form-check-input" type="radio" name="omic" :id="omic" :value="omic">
                <label class="form-check-label" :for="omic">{{ omic }}</label>
            </div>
        </div>

        <button class="btn btn-primary mt-4" type="submit" :disabled="submitting" v-if="!disabled">
            <font-awesome-icon icon="check" />
            OK
        </button>
    </form>
</div>
</template>

<script>
export default {
    data() {
        return {
            submitting: false,
            error: ''
        }
    },

    props: {
        disabled: Boolean
    },

    methods: {
        submit(event) {
            this.submitting = true
            const formData = new FormData(event.target)
            this.$helpers.post(formData)
            .then(data => {
                this.submitting = false
                this.$emit('done', data.project)
            }, () => {
                this.submitting = false
            })
        }
    }
}
</script>