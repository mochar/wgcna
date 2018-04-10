<template>
<div>
    <button class="btn btn-light btn-block dropdown-toggle text-left d-flex justify-content-between align-items-center" 
            style="margin-right: -1px" data-toggle="dropdown">
        <span v-if="project">
            <span class="fa fa-circle fa-fw" :class="`text-${project.omic}`"></span>
            <span>{{ project.name }}</span>
            <span v-show="project.description" class="text-muted">- {{ project.description }}</span>
        </span>
        <span class="fa fa-cog fa-spin" v-else></span>
    </button>
    <div class="dropdown-menu w-100">
        <!-- <span class="m-3">Projects</span> -->
        <a class="dropdown-item" href="#" v-for="(p, i) in projects" :key="p.id" @click.prevent="select(p)">
            <div class="d-flex justify-content-between align-items-center">
                <span>{{ p.name }}</span>
                <span class="badge badge-pill badge-light bg-main" :class="`bg-${p.omic}`">
                    {{ p.omic }}
                </span>
            </div>
            <div class="d-flex justify-content-between align-items-center">
                <small class="text-secondary">{{ p.description}}</small>
            </div>
        </a>
    </div>
</div>
</template>

<script>
export default {
    data() {
        return {
            project: null
        }
    },

    props: {
        projects: Array,
        init: Number
    },

    methods: {
        select(p) {
            this.project = p
            this.$emit('selected', p)
        }
    },

    created() {
        this.project = this.init ? this.projects[this.init] : this.projects[0]
    }
}
</script>
