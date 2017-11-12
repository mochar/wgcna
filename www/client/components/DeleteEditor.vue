<template>
<div class="ml-5 mr-5 w-100">
    <div class="d-flex justify-content-between align-items-center">
        <h5>
            <slot></slot>
        </h5>
        <input type="text" placeholder="search" v-model="searchTerm">
    </div>

    <div v-for="(item, i) in paginatedList" :key="item" class="item d-flex align-items-center justify-content-between" 
            @click="$emit('selected', i)">
        <span>{{ item }}</span>
        <div>
            <span class="fa fa-trash fa-lg text-danger" v-if="removedIndices.includes(i)"></span>
        </div>
    </div>

    <div class="card-body d-flex justify-content-between">
        <div>
            <a href="#" @click.prevent="prevPage" v-if="canPrev"> &larr; Prev </a>
            <span v-else> &larr; Prev </span>
        </div>

        <div class="text-center">
            <span>{{ page }}</span><span> / {{ pages }} </span>
        </div>
        
        <div>
            <a href="#" class="float-right" @click.prevent="nextPage" v-if="canNext"> Next &rarr; </a>
            <span class="float-right" v-else> Next &rarr; </span>
        </div>
    </div>
</div>
</template>

<script>
export default {
    data() {
        return {
            searchTerm: '',
            items: 15,
            page: 1
        }
    },

    props: ['list', 'removedIndices'],

    methods: {
        prevPage() {
            if (this.canPrev) this.page = this.page - 1
        },
        nextPage() {
            if (this.canNext) this.page = this.page + 1
        }
    },

    computed: {
        searchedList() {
            if (this.searchTerm === '') 
                return this.list
            else 
                return this.list.filter(item => item.search(this.searchTerm) > -1)
        },
        pages() {
            return Math.ceil(this.searchedList.length / this.items)
        },
        offset() {
            return (this.page - 1) * this.items
        },
        paginatedList() {
            return this.searchedList.slice(this.offset, this.offset + this.items + 1)
        },
        canPrev() {
            return this.page > 1
        },
        canNext() {
            return this.page < this.pages
        }
    }
}
</script>

<style>
.item {
    cursor: pointer;
    padding-top: .3rem;
    padding-bottom: .3rem;
}
.item:hover {
    background-color: #eee;
}
</style>