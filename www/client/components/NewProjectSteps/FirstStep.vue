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
                <input class="custom-control-input" type="radio" name="omic" value="transcriptomics" checked>
                <span class="custom-control-indicator"></span>
                <span class="custom-control-description">Transcriptomics</span>
            </label>
        </div>
        <div class="form-check form-check-inline">
            <label class="custom-control custom-radio">
                <input class="custom-control-input" type="radio" name="omic" value="metabolomics">
                <span class="custom-control-indicator"></span>
                <span class="custom-control-description">Metabolomics</span>
            </label>
        </div>
        <div class="form-check form-check-inline">
            <label class="custom-control custom-radio">
                <input class="custom-control-input" type="radio" name="omic" value="lipidomics">
                <span class="custom-control-indicator"></span>
                <span class="custom-control-description">Lipidomics</span>
            </label>
        </div>
    </div>

    <div v-if="false">
    <button class="btn btn-link" @click="advanced = true" v-if="!advanced">
        <span class="fa fa-angle-double-right"></span>
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
