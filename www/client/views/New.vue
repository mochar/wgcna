<template>
<div class="mb-5"> 
    <div class="alert alert-warning alert-dismissible fade show" v-if="!$store.state.projects.length">
        You currently have no projects. Start by setting up one by providing the necessary information as prompted below.
        <button type="button" class="close" data-dismiss="alert" aria-label="Close">
            <span aria-hidden="true">&times;</span>
        </button>
    </div>

    <info @done="infoDone" :disabled="infoDisabled"></info>
    <expression :project="project.id" @done="expressionDone" :disabled="expressionDisabled" v-if="expressionShow"></expression>
    <trait :project="project.id" @done="traitDone" :disabled="traitDisabled" v-if="traitShow"></trait>
    <outliers :project="project.id" @done="finish" v-if="outliersShow"></outliers>
</div>
</template>

<script>
import Info from 'views/NewSteps/Info'
import Expression from 'views/NewSteps/Expression'
import Trait from 'views/NewSteps/Trait'
import Outliers from 'views/NewSteps/Outliers'

export default {
    name: 'new',

    data() {
        return {
            project: null,
            infoDisabled: false,
            expressionDisabled: false,
            expressionShow: false,
            traitDisabled: false,
            traitShow: false,
            outliersShow: false
        }
    },

    components: {
        Info,
        Expression,
        Trait,
        Outliers
    },

    methods: {
        infoDone(project) {
            this.infoDisabled = true
            this.project = project
            this.expressionShow = true
        },
        expressionDone() {
            this.expressionDisabled = true
            this.traitShow = true
        },
        traitDone() {
            this.traitDisabled = true
            this.outliersShow = true
        },
        finish() {
            this.$store.commit('setProjectLoading', false)
            this.$store.dispatch('getProjects').then(() => {
                this.$store.commit('setProjectLoading', false)
                this.$router.push({ name: 'analyze', params: { id: this.project.id }})
            })
        }
    }
}
</script>

<style>
.disabled {
    opacity: .5;
    pointer-events: none;
}
</style>
