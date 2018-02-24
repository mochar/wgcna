<template>
<div class="card card-body mb-5">
    <h6 class="block-title">
        PREPROCESS
    </h6>

    <div v-if="!project">
        <span class="fa fa-refresh fa-spin text-main"></span>
    </div>
    <div v-else>
        <span>
            <span class="fa fa-circle-o text-secondary" v-if="step < 2"></span>
            <span class="fa fa-check-circle-o text-main" v-else></span>
            <span class="ml-1">Expression data format</span>
        </span>
        <div v-if="step > 1">
            <div class="preprocess-component border-main"></div>
            <span>
                <span class="fa fa-circle-o text-secondary" v-if="step < 3"></span>
                <span class="fa fa-check-circle-o text-main" v-else></span>
                <span class="ml-1">Good genes and samples</span>
            </span>
        </div>
        <div v-if="project.trait && step > 2">
            <div class="preprocess-component border-main"></div>
            <span>
                <span class="fa fa-circle-o text-secondary" v-if="step < 4"></span>
                <span class="fa fa-check-circle-o text-main" v-else></span>
                <span class="ml-1">Trait data format</span>
            </span>
        </div>
        <div v-if="project.trait ? step > 3 : step > 2">
            <div class="preprocess-component border-main"></div>
            <span>
                <span class="fa fa-circle-o text-secondary" v-if="project.trait ? step < 5 : step < 4"></span>
                <span class="fa fa-check-circle-o text-main" v-else></span>
                <span class="ml-1">Outlier Removal</span>
            </span>
        </div>
        <component 
            v-if="project.id"
            :is="current" 
            :project="project"
            @done="next">
        </component>
        <div class="mt-2" v-if="step > steps.length">
            <button class="btn btn-primary" :disabled="loading" @click="done">
                <span class="fa fa-chevron-right"></span>
                Analyze
            </button>
        </div>
    </div>
</div>
</template>

<script>
import ReformatExpression from 'components/PreprocessSteps/ReformatExpression'
import ReformatTrait from 'components/PreprocessSteps/ReformatTrait'
import GoodGenes from 'components/PreprocessSteps/GoodGenes'
import Outliers from 'components/PreprocessSteps/Outliers'

export default {
    data() {
        return {
            step: 1,
            project: null,
            loading: false,
            finished: false
        }
    },

    components: {
        ReformatExpression,
        ReformatTrait,
        GoodGenes,
        Outliers
    },

    methods: {
        next() {
            this.step++
            if (this.step > this.steps.length)
                this.finished = true
        },
        done() {
            this.loading = true
            this.$store.dispatch('getProjects').then(() => {
                this.$router.push({ name: 'analyze', params: { id: this.project.id }})
            })
        },
        setProject() {
            const projectId = this.$route.params.id
            $.getJSON(`${ROOTURL}/projects/${projectId}`).then(data => {
                this.project = data.project
            })
        }
    },

    computed: {
        current() {
            return this.project ? this.steps[this.step - 1] : null
        },
        steps() {
            if (!this.project) return null
            let steps = ['ReformatExpression', 'GoodGenes']
            if (this.project.trait)
                steps.push('ReformatTrait')
            steps.push('Outliers')
            return steps
        }
    },
    
    created() {
        this.setProject()
    }
}
</script>

<style>
.preprocess-component {
    border-left: 2px solid #ccc;
    padding: 1.25rem 0 1rem 1rem;
    margin-left: .4rem;
}
</style>