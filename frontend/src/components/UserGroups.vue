<template>
    <v-col class="content">
        <v-card dark>
            <v-card-title dark>
                <v-text-field
                    v-model="search"
                    append-icon="mdi-magnify"
                    label="Search"
                    single-line
                    hide-details
                    dark
                    v-on:change="this.fetchData"
                ></v-text-field>
            </v-card-title>

            <v-data-table
                :items="items"
                :headers="headers"
                :options.sync="options"
                :server-items-length="total"
                hide-default-header
                class="elevation-1"
                loading
                :loading-text="loading_text"
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
        </v-card>
    </v-col>
</template>

<script>

    import axiosInstance from '../helpers/interceptor.js';
    import authHelper from '../helpers/auth.js';

    export default {
        name: 'UserGroups',
        mixins: [authHelper],
        watch: {
            options: {
                handler() {
                    this.fetchData();
                },
                deep: true
            },
        },
        data: function() {
            return {
                items: [],
                loading_text: "Loading... Please wait",
                selected: null,
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
                let params = Object.assign({}, this.options, {'name': this.search});
                let response = (await axiosInstance.get(this.apiUrl, {params: params})).data;
                this.items = response.data;

                this.total = response.pagination.total;
                this.size = (response.pagination.total-1) / response.pagination.page + 1;

                if (this.total == 0) {
                    this.loading_text = "no usergroups."
                }
            },
            handlePageChange(value) {
                this.page = value;
            },
            handleClick(selectedUsergroup) {
                this.selected = [selectedUsergroup];
            },

        }
    };

</script>

<style scoped>
.content {
    position: relative;
    width: 300px;
    left: 10px;
}
</style>