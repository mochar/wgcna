<template>
<div>
    <div class="form-group">
        <label>Expression data</label>
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
        <small class="form-text text-muted">Table can be transposed and further refined later on.</small>
    </div>
</div>
</template>

<script>
export default {
    data() {
        return {
            option: 'file'
        }
    }
}
</script>
