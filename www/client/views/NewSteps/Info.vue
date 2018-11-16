<template>
<div class="card card-body block" :class="{ disabled: disabled }">
    <div class="d-flex justify-content-between align-items-start">
        <h6 class="block-title text-uppercase">
            Project information
        </h6>
    </div>

    <form class="mt-2 mb-1" enctype="multipart/form-data" @submit.prevent="submit">
        <div class="form-group row">
            <label class="col-2 col-form-label">Name</label>
            <div class="col-10">
                <input type="text" name="name" class="form-control">
            </div>
        </div>
        <div class="form-group row">
            <label class="col-2 col-form-label">Description</label>
            <div class="col-10">
                <input type="text" name="description" class="form-control">
            </div>
        </div>
        <fieldset class="form-group">
            <div class="row">
                <label class="col-2 col-form-label">Type</label>
                <div class="col-10">
                    <div class="custom-control custom-radio pl-0 mb-1" v-for="tag in Object.keys($store.state.tags)" :key="tag">
                        <button class="btn btn-light" @click.prevent="selectedTag = tag">
                            <font-awesome-icon 
                                :icon="[tag ===  selectedTag ? 'fas' : 'far', 'circle']"
                                :color="$store.state.tags[tag]" 
                                fixed-width />
                            {{ tag }}
                        </button>
                    </div>
                    <div class="mt-3">
                        <input v-model="newTag" placeholder="New tag" > 
                        <button class="btn btn-light btn-sm" v-show="newTag" @click.prevent="addColor">
                            <font-awesome-icon icon="plus" />
                            Add
                        </button>
                        <div v-if="newTag !== ''">
                            <compact  v-model="color" />
                        </div>
                    </div>
                </div>
            </div>
        </fieldset>

        <button class="btn btn-primary mt-4" type="submit" :disabled="submitting" v-if="!disabled">
            <font-awesome-icon icon="check" />
            OK
        </button>

        <div class="mt-3">
            <span v-if="error" class="text-danger">{{ error }}</span>
        </div>
    </form>
</div>
</template>

<script>
import { Compact } from 'vue-color'

export default {
    data() {
        return {
            submitting: false,
            addingColor: false,
            error: '',
            selectedTag: null,
            newTag: '',
            color: { hex: '#194d33' },
            error: ''
        }
    },

    components: { Compact },

    props: {
        disabled: Boolean
    },

    methods: {
        submit(event) {
            this.submitting = true
            const formData = new FormData(event.target)
            if (this.selectedTag) formData.append('tag', this.selectedTag)
            this.$helpers.post(formData)
            .always(() => this.submitting = false)
            .done(data => {
                this.$emit('done', data.project)
                this.error = ''
            })
            .fail(error => {
                this.error = error.responseJSON.error
            })
        },
        addColor() {
            this.addingColor = true
            const data = { name: this.newTag, color: this.color.hex }
            $.ajax({
                url: `${ROOTURL}/tags`,
                method: 'POST',
                dataType: 'json', 
                cache: false,
                contentType: false,
                processData: false,
                data: JSON.stringify(data)
            })
            .done(data => this.$store.commit('addTag', data))
        }
    },
    
    watch: {
        addingColor() {
            if (!this.addingColor) {
                this.newTag = ''
            }
        }
    }
}
</script>

<style>
.vc-compact {
    margin-top: .5rem;
    box-shadow: initial !important;
}
</style>
