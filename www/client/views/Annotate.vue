<template>
    <div>
        <div class="d-flex justify-content-between align-items-center top">
            <h3>Annotate</h3>
            <select v-model="name" id="name-select" class="btn btn-secondary">
                <option v-for="name in names">{{ name }}</option>
            </select>
            <router-link to="/annotatenew" class="btn btn-primary">
                <span class="fa fa-plus"></span>
                New
            </router-link>
        </div>
        <ModuleBrowser
            :name="name">
        </ModuleBrowser>
    </div>
</template>

<script>
import ModuleBrowser from '../components/ModuleBrowser'

export default {
    data() {
        return {
            name: null,
            names: [],
        }
    },

    components: {
        ModuleBrowser
    },

    created() {
        $.getJSON(`${ROOTURL}/module-lists/`).then(data => {
            this.names = data.names.sort((a, b) => a < b ? -1 : 1)
            if (this.names.length > 0) this.name = this.names[0]
            else this.$router.push('/annotatenew')
        })
    }
}
</script>
