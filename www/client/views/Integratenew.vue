<template>
    <div>
        <div class="d-flex justify-content-between align-items-center top">
            <h3>Integrate</h3>
            <div id="upload-form" class="card">
                <form class="d-flex align-items-center" enctype="multipart/form-data" @submit.prevent="uploadModule">
                    <input type="text" class="form-control" name="name" placeholder="Name">
                    <button type="submit" class="btn btn-primary" :disabled="loading">Submit</button>
                </form>
            </div>
            <router-link to="/integrate" class="btn btn-secondary">
                Cancel
            </router-link>
        </div>

    </div>
</template>

<script>
export default {
    data() {
        return {
            name: null,
            loading: false
        }
    },

    methods: {
        uploadModule() {
            this.loading = true
            const formData = new FormData(event.srcElement)
            $.post({
                url: `${ROOTURL}/module-lists/`,
                data: formData,
                async: true,
                cache: false,
                contentType: false,
                processData: false
            }).then(data => {
                this.loading = false
            })

        }
    }
}
</script>

<style>
#new {

}

#upload-form {
    padding: .15rem;
}

#upload-form input[type="file"] {
    margin: 0 .25rem;
}
</style>
