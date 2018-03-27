<template>
    <div class="card card-body block">
        <h6 class="block-title">
            {{ title }}
        </h6>
        Project:
        <select class="custom-select" v-model="projectId">
            <option v-for="projectId in projectIds" :key="projectId" :value="projectId">{{ getNameFromId(projectId) }}</option>
        </select>
        Id type:
        <select class="custom-select" v-model="id_type">
            <option v-for="id_type in id_types" :key="id_type" :value="id_type">{{ id_type }}</option>
        </select>
    </div>
</template>

<script>
import { mapState, mapActions, mapGetters } from 'vuex'

export default {
    data() {
        return {
            id_types: ["Euretos synonym"],
            id_type: null,
            projectId: null
        }
    },

    props: ['title'],

    computed: {
        ...mapState(['projectIndex', 'projects']),
        ...mapGetters(['projectIds']),
    },

    watch: {
        id_type: function (val) {
            this.$emit("id_type", val)
        },
        projectId: function (val) {
            this.$emit("projectId", val)
        }
    },

    methods: {
        getNameFromId(project_Id) {
            var returnname = ""
            this.projects.forEach(function(project) {
                if (project.id === project_Id){
                    returnname = project.name
                }
            });
            return returnname
        }
    },

    created() {
        this.id_type = this.id_types[0]
        this.projectId = this.projectIds[0]
    }
}
</script>
