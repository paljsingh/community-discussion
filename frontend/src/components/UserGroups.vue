<template>
    <div class="usergroups">
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

    import axiosInstance from '../helpers/interceptor.js';
    import authHandler from '../auth/index.js';

    export default {
        name: 'UserGroups',
        mixins: [authHandler],
        watch: {
            options: {
                handler() {
                    this.fetchData();
                },
                deep: true
            }
        },
        data: function() {
            return {
                items: [],
                headers: [
                    {
                        text: 'User Group',
                        value: 'name',
                    },
                ],
                apiUrl: process.env.VUE_APP_USERGROUPS_API_ENDPOINT,
                search: "",
                options: {},
                total: 0,

            }
        },
        methods: {
            async fetchData() {
                let response = (await axiosInstance.get(this.apiUrl)).data;
                this.items = response.data;
                this.total = response.pagination.total;
                this.size = response.pagination.size;
            },
            handlePageChange(value) {
                console.log(value)
                this.page = value;
            }
        }
    };

</script>

<style scoped>
.usergroups {
    position: fixed;
    width: 250px;
    left: 200px;
    top: 60px;
    font-size: 12px;
    /* background: #000; */
}
</style>