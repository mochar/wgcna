<template>
<div>
    <div v-if="list">
        <input class="form-control" type="text" placeholder="search" v-model="searchTerm">

        <button 
            class="btn btn-danger btn-block" 
            :disabled="!selected.length"
            @click="removeSelected">Remove
        </button>

        <div v-for="item in paginatedList" class="item">
            <label class="form-check-label">
                <input 
                    class="form-check-input" 
                    :id="item"
                    :value="item"
                    type="checkbox" 
                    v-model="selected"> {{ item }}
            </label>
        </div>

        <div class="card-block d-flex justify-content-between">
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
    <div v-else>
        <span> None </span>
    </div>
</div>
</template>

<script>
export default {
    data() {
        return {
            searchTerm: '',
            items: 15,
            page: 1,
            selected: [],
            removed: []
        }
    },

    props: ['list'],

    methods: {
        prevPage() {
            if (this.canPrev) this.page = this.page - 1
        },
        nextPage() {
            if (this.canNext) this.page = this.page + 1
        },
        removeSelected() {
            this.removed = [...this.removed, ...this.selected]
            this.selected = []
        }
    },

    computed: {
        withoutRemoved() {
            return this.list.filter(item => this.removed.indexOf(item) === -1)
        },
        searchedList() {
            if (this.searchTerm === '') 
                return this.withoutRemoved
            else 
                return this.withoutRemoved.filter(item => item.search(this.searchTerm) > -1)
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
    },

    watch: {
        removed() {
            this.$emit('removed', this.removed)
        }
    }
}
</script>

<style>
.item {
    padding: .5rem;
}
</style>