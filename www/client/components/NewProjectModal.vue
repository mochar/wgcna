<template>
<div class="modal" id="new-modal" tabindex="-1">
<div class="modal-dialog">
<div class="modal-content">
<div class="modal-body">
    <div class="d-flex justify-content-between align-items-baseline">
        <h5 class="block-title">New project</h5>

        <button type="button" class="close" data-dismiss="modal" aria-label="Close">
            <span>&times;</span>
        </button>
    </div>

    <form id="upload-form" enctype="multipart/form-data" @submit.prevent="submit">

        <div class="card-body">
            <first-step v-show="step == 'FirstStep'"></first-step>
            <second-step v-show="step == 'SecondStep'"></second-step>
            <third-step v-show="step == 'ThirdStep'"></third-step>
        </div>

        <div class="float-right">
            <button class="btn btn-light" @click.prevent="back" :disabled="step == 'FirstStep'">
                Back
            </button>
            <button class="btn btn-primary" @click.prevent="next" v-if="step != 'ThirdStep'">
                Next
            </button>
            <button class="btn btn-primary" type="submit" :disabled="loading" v-else>
                <span class="fa fa-chevron-right"></span>
                Preprocess
            </button>
        </div>
    </form>
</div>
</div>
</div>
</div>
</template>

<script>
import FirstStep from 'components/NewProjectSteps/FirstStep'
import SecondStep from 'components/NewProjectSteps/SecondStep'
import ThirdStep from 'components/NewProjectSteps/ThirdStep'

export default {
    data() {
        return {
            loading: false,
            step: 'FirstStep'
        }
    },

    components: {
        FirstStep,
        SecondStep,
        ThirdStep
    },

    methods: {
        submit(event) {
            this.loading = true
            const formData = new FormData(event.target)
            $.post({
                url: `${ROOTURL}/projects/`,
                data: formData,
                async: true,
                cache: false,
                contentType: false,
                processData: false
            }).then(data => {
                const params = { id: data.project.id }
                this.loading = false
                this.$router.push({ name: 'preprocess', params })
                $('#new-modal').modal('hide')
            }, () => {
                this.loading = false
            })
        },
        next() {
            switch (this.step) {
                case 'FirstStep':
                    this.step = 'SecondStep'
                    break;
                case 'SecondStep':
                    this.step = 'ThirdStep'
                default:
                    break
            }
        },
        back() {
            switch (this.step) {
                case 'SecondStep':
                    this.step = 'FirstStep'
                    break;
                case 'ThirdStep':
                    this.step = 'SecondStep'
                default:
                    break
            }
        }
    }
}
</script>

<style>
</style>