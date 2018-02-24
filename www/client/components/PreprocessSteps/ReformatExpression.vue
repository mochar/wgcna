<template>
<div>
    <div class="preprocess-component">
        <div class="d-flex align-items-center">
            <div>
                <span>{{ samples }} samples, </span>
                <span>{{ genes }} genes</span>
            </div>
            <button class="btn btn-light" @click="transpose = !transpose">
                <span class="fa fa-retweet fa-lg"></span>
                Swap rows and columns
            </button>
        </div>
    </div>
    <div class="mt-2">
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
            loading: false, // setting up
            busy: false, // doing the thing
            transpose: false
        }
    },

    props: ['project'],

    methods: {
        go() {
            this.busy = true
            const formData = new FormData()
            formData.append('transpose', this.transpose)
            $.ajax({
                url: `${ROOTURL}/projects/${this.project.id}/expression`,
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
        }
    },

    computed: {
        genes() {
            return this.transpose ? this.project.samples : this.project.genes
        },
        samples() {
            return this.transpose ? this.project.genes : this.project.samples
        }
    }
}
</script>
