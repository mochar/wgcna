<template>
<div class="row mb-2">
    <div class="col-5">
        <projects-dropdown 
            class="w-100" 
            :projects="projects"
            :init="init"
            @selected="p => $emit('selected', p)">
        </projects-dropdown>
    </div>
    <div class="col-1 d-flex align-items-center justify-content-end">
        Modules: 
    </div>
    <div class="col-4">
        <projects-dropdown 
            class="w-100" 
            :circle="false"
            :projects="[{name: 'All'}]">
        </projects-dropdown>
    </div>
    <div class="col-2">
        <button class="btn btn-light" v-if="showAdd" @click="$emit('add')">
            <font-awesome-icon icon="plus" />
        </button>
        <button v-if="!showAdd && deletable" type="button" class="close" data-dismiss="alert"
            :style="{'float': 'initial', 'line-height': 'initial'}">
            <span>&times;</span>
        </button>
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
