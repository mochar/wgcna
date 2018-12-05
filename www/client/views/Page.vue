<template>
<div>
    <div v-if="show">
        <slot></slot>
    </div>
    <!-- <slot v-if="showPage">...</slot> -->
    <div class="w-100 h-100 d-flex flex-column justify-content-center align-items-center" 
         style="color: rgba(0,0,0,.3)" v-else>
        <div>
            <font-awesome-icon icon="circle" size="lg" />
            <font-awesome-icon icon="circle" size="lg" class="ml-2 mr-2" />
            <font-awesome-icon icon="circle" size="lg" />
        </div>
        <strong class="d-flex mt-2">Loading</strong>
    </div>
</div>
</template>

<script>
export default {
    props: {
        show: {
            type: Boolean,
            default: true
        }
    },

    watch: {
        show() {
            console.log('showPage? ', this.show)
        }
    },

    created() {
        console.log('Meme?' + this.show)
    }
}
</script>
