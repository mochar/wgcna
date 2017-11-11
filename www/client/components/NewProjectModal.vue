<template>
<div class="modal" id="new-modal" tabindex="-1">
<div class="modal-dialog">
<div class="modal-content">
<div class="modal-body">

    <form id="upload-form" enctype="multipart/form-data" @submit.prevent="submit">

    <h5 class="block-title">New project</h5>

    <div class="card-body">
        <div class="form-group">
            <label>Name</label>
            <input class="form-control" name="name" placeholder="required">
            <!-- <small class="form-text text-muted">We'll never share your email with anyone else.</small> -->
        </div>
        <div class="form-group">
            <label>Short description</label>
            <input class="form-control" name="description">
        </div>
        <div class="form-group">
            <label>Expression data</label>
            <input type="file" class="form-control-file" name="expression">
        </div>
        <div class="form-check">
            <label class="form-check-label">
                <input type="checkbox" checked class="form-check-input">
                Signed network
            </label>
        </div>
    </div>

    <div class="d-flex justify-content-between">
        <button class="btn btn-link" data-dismiss="modal">Cancel</button>
        <button class="btn btn-primary" type="submit" :disabled="loading">
            <span class="fa fa-chevron-right"></span>
            Preprocess
        </button>
    </div>

    </form>
</div>
</div>
</div>
</div>
</template>

<script>
export default {
    data() {
        return {
            loading: false
        }
    },

    methods: {
        submit(event) {
            this.loading = true
            const formData = new FormData(event.srcElement)
            $.post({
                url: `${ROOTURL}/projects/`,
                data: formData,
                async: true,
                cache: false,
                contentType: false,
                processData: false
            }).then(data => {
                const params = { id: data.project.id }
                this.loading = false
                this.$router.push({ name: 'preprocess', params })
                $('#new-modal').modal('hide')
            }, () => {
                this.loading = false
            })
        }
    },

    computed: {
    },

    watch: {
    }
}
</script>

<style>
</style>