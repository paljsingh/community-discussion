<template>
    <div class="communities">
        <v-data-table
            :items="items"
            :headers="headers"
            :options.sync="options"
            :server-items-length="total"
            hide-default-header
            class="elevation-1"
            loading
            loading-text="Loading... Please wait"
            dense
            :search="search"
            :footer-props="{
                'items-per-page-text':'',
                'items-per-page-options': []
            }"
            @update:pagination="handlePageChange"
            dark
        >
        </v-data-table>
    </div>
</template>

<script>
    import axios from '../helpers/interceptor';

    export default {
        name: 'Communities',
        watch: {
            options: {
                handler() {
                    this.get_communities();
                },
                deep: true
            }
        },
        data: function() {
            return {
                items: [],
                headers: [
                    {
                        text: 'Community',
                        value: 'name',
                    },
                ],
                apiUrl: process.env.VUE_APP_COMMUNITIES_API_ENDPOINT,
                search: "",
                options: {},
                total: 0,
            }
        },
        created() {
            this.force_update;
        },
        methods: {
            async get_communities () {
                try {
                    const response = await axios.get(this.apiUrl)
                    this.communities = response.data.communities
                } catch (e) {
                    console.error(e)
                    this.failed = true
                }
            },
            handlePageChange(value) {
                console.log(value)
                this.page = value;
            },

        }
    };

</script>

<style scoped>
.communities {
    position: fixed;
    width: 250px !important;
    left: 200px !important;
    top: 100px !important;
    font-size: 12px;
    /* background: #000; */
}
</style>