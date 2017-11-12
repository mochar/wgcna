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
            <label class="form-check-label">
                <input class="form-check-input" type="radio" name="omic" value="transcriptomics" checked> Transcriptomics
            </label>
        </div>
        <div class="form-check form-check-inline">
            <label class="form-check-label">
                <input class="form-check-input" type="radio" name="omic" value="metabolomics"> Metabolomics
            </label>
        </div>
        <div class="form-check form-check-inline">
            <label class="form-check-label">
                <input class="form-check-input" type="radio" name="omic" value="lipidomcs"> Lipidomics
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
