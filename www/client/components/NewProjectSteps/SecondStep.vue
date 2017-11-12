<template>
<div>
    <div class="form-group">
        <label>Expression data</label>
        <!-- <input type="file" class="form-control-file" name="expression"> -->
        <div class="d-flex align-items-center">
            <label class="form-check-label d-flex align-items-center">
                <input class="form-check-input" type="radio" name="expression-option" value="file" v-model="option">
            </label>
            <input type="file" class="form-control-file ml-2" name="expression" :disabled="option == 'link'">
        </div>
        <div class="d-flex align-items-center mt-3">
            <label class="form-check-label d-flex align-items-center">
                <input class="form-check-input" type="radio" name="expression-option" value="link" v-model="option">
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
