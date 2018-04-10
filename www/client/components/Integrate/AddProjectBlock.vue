<template>
<div class="row mb-2">
    <div class="col-10">
        <projects-dropdown 
             class="w-100" 
            :projects="projects"
            :init="init"
            @selected="p => $emit('selected', p)">
        </projects-dropdown>
    </div>
    <div class="col-2">
    <button class="btn btn-light" v-if="showAdd">
        <span class="fa fa-plus"></span>
    </button>
    <span v-if="!showAdd && deletable">&times;</span>
    </div>
</div>
</template>

<script>
import ProjectsDropdown from 'components/ProjectsDropdown'

export default {
    props: {
        deletable: Boolean,
        showAdd: Boolean,
        projects: Array,
        init: Number
    },

    components: {
        ProjectsDropdown
    },

    created() {
        const project = this.init ? this.projects[this.init] :  this.projects[0]
        this.$emit('selected', project)
    }
}
</script>
