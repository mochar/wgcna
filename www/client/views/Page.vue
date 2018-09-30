<template>
<div>
    <slot v-if="!$store.state.projectLoading && requirement">...</slot>
    <div class="w-100 h-100 d-flex flex-column justify-content-center align-items-center" 
         style="color: rgba(0,0,0,.3)" v-if="$store.state.projectLoading">
        <div>
            <span class="fa fa-circle fa-lg"></span>
            <span class="fa fa-circle fa-lg ml-2 mr-2"></span>
            <span class="fa fa-circle fa-lg"></span>
        </div>
        <strong class="d-flex mt-2">Loading</strong>
    </div>
</div>
</template>

<script>
export default {
    props: {
        requirement: {
            type: Boolean,
            default: true
        }
    }
}
</script>
