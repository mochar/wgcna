<template>
<div>
    <div class="form-group">
        <label>Name</label>
        <input class="form-control" name="name" placeholder="required">
    </div>
    <div class="form-group">
        <label>Short description</label>
        <input class="form-control" name="description">
    </div>
    <div class="form-group">
        <label>Omics</label>
        <br>
        <div class="form-check form-check-inline">
            <label class="custom-control custom-radio">
                <input id="trans-radio" class="custom-control-input" type="radio" name="omic" value="transcriptomics" checked>
                <label class="custom-control-label" for="trans-radio">Transcriptomics</label>
            </label>
        </div>
        <div class="form-check form-check-inline">
            <label class="custom-control custom-radio">
                <input id="met-radio" class="custom-control-input" type="radio" name="omic" value="metabolomics">
                <label class="custom-control-label" for="met-radio">Metabolomics</label>
            </label>
        </div>
        <div class="form-check form-check-inline">
            <label class="custom-control custom-radio">
                <input id="lip-radio" class="custom-control-input" type="radio" name="omic" value="lipidomics">
                <label class="custom-control-label" for="lip-radio">Lipidomics</label>
            </label>
        </div>
    </div>

    <div v-if="false">
    <button class="btn btn-link" @click="advanced = true" v-if="!advanced">
        <font-awesome-icon icon="angle-double-right" />
        Advanced
    </button>
    <div v-else>
        <hr>

        <div class="form-check">
            <label class="form-check-label">
                <input type="checkbox" checked class="form-check-input">
                Signed network
            </label>
        </div>
    </div>
    </div>
</div>
</template>

<script>
export default {
    data() {
        return {
            advanced: false
        }
    }
}
</script>
