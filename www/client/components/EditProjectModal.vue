<template>
<div class="modal" id="edit-modal" tabindex="-1">
<div class="modal-dialog">
<div class="modal-content">
<div class="modal-body">
    <div class="d-flex justify-content-between align-items-baseline">
        <h5 class="block-title">Edit project</h5>
    </div>

    <form id="edit-form" enctype="multipart/form-data" @submit.prevent="submit">
        <div class="card-body">
            <div class="form-group">
                <input class="form-control" name="name" placeholder="Name">
            </div>
            <div class="form-group">
                <input class="form-control" name="description" placeholder="Description">
            </div>
        </div>

        <button class="btn btn-link text-normal" data-dismiss="modal">
            Cancel
        </button>
        <div class="float-right">
            <button class="btn btn-link text-normal" @click.prevent="del" :disabled="loading">
                Delete
            </button>
            <button class="btn btn-primary" type="submit" :disabled="loading">
                Update
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
            loading: false,
        }
    },

    methods: {
        submit(event) {
        },
        del() {
            this.loading = true
            $.ajax({
                type: 'DELETE',
                url: `${ROOTURL}/projects/${this.project.id}`
            }).then(() => {
                this.loading = false
            }, () => {
                this.loading = false
            })
        }
    },

    computed: {
        project() {
            return this.$store.getters.project
        }
    }
}
</script>