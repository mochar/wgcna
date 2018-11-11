<template>
<ul class="nav nav-tabs top position-relative">
    <li class="nav-item">
        <a 
            class="nav-link" 
            :class="{ active: tab == 'ModuleCreationTab' }" 
            href="#" 
            @click.prevent="$emit('update:tab', 'ModuleCreationTab')">
            <font-awesome-icon icon="certificate" fixed-width size="sm" />
            Generate
        </a>
    </li>
    <li class="nav-item">
        <a 
            class="nav-link" 
            :class="{ disabled: !hasModules, active: tab == 'ModuleInspectionTab' }" 
            href="#" 
            @click.prevent="$emit('update:tab', 'ModuleInspectionTab')">
            <font-awesome-icon :icon="['far', 'eye']" fixed-width size="sm" />
            Inspection
        </a>
    </li>
    <li class="nav-item">
        <a 
            class="nav-link" 
            :class="{ disabled: !hasModules, active: tab == 'ModuleSignificanceTab' }" 
            href="#" 
            @click.prevent="$emit('update:tab', 'ModuleSignificanceTab')">
            <font-awesome-icon icon="chart-bar" fixed-width size="sm" />
            Significance
        </a>
    </li>
</ul>
</template>

<script>
export default {
    props: {
        project: {
            type: Object,
            required: true
        },
        tab: {
            type: String,
            required: true
        }
    },

    computed: {
        hasModules() {
            return this.$store.getters.hasModules
        }
    }
}
</script>


<style scoped>
.nav-link {
    color: #999;
}
</style>