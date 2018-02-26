<template>
<div class="ordinal-trait">
    <div class="ordinal-choice">
        <div class="custom-control custom-checkbox">
            <input type="checkbox" class="custom-control-input" :id="id" v-model="isOrdinal">
            <label class="custom-control-label" :for="id">{{ trait }}</label>
        </div>
    </div>
    <div class="p-3" v-if="isOrdinal && variables_">
        <draggable v-model="variables_" @start="drag=true" @end="drag=false">
            <div v-for="variable in variables_" :key="variable" class="variable">
                {{ variable }}
            </div>
        </draggable>
    </div>
</div>
</template>

<script>
import draggable from 'vuedraggable'

export default {
    data() {
        return {
            isOrdinal: false,
            drag: false,
            variables_: null
        }
    },

    props: ['trait', 'variables'],

    components: {
        draggable
    },

    computed: {
        id() {
            return `ordinal-${this.trait}`
        }
    },

    watch: {
        isOrdinal() {
            if (this.isOrdinal) {
                this.$emit('ordinal', this.variables_)
            } else {
                this.$emit('nominal')
            }
        },
        variables_() {
            if (this.isOrdinal) 
                this.$emit('ordinal', this.variables_)
        }
    },
    
    created() {
        this.variables_ = this.variables
    }
}
</script>

<style>
.ordinal-trait {
    background-color: #f6f6f6;
    margin-bottom: .5rem;
}

.ordinal-choice {
    padding: .3rem 1rem;
}

.variable {
    cursor: pointer;
    background-color: #f6f6f6;
    padding: .5rem 1rem;
}
.variable:hover {
    background: #fafafa;
}
</style>
