<template>
    <v-col class="content">
        <div class="col1">
            <v-card dark>
                <v-card-title dark>
                    <v-text-field
                        v-model="search"
                        append-icon="mdi-magnify"
                        label="Search"
                        single-line
                        hide-details
                        v-on:change="this.fetchData"
                        dark
                    ></v-text-field>
                </v-card-title>
                <v-data-table
                    :items="items"
                    :headers="headers"
                    :options.sync="options"

                    item-key="name"
                    v-model="selected"
                    @click:row="handleClick"
                    
                    :footer-props="{
                        'items-per-page-text':'',
                        'items-per-page-options': []
                    }"
                    @update:pagination="handlePageChange"
                    :server-items-length="total"

                    class="elevation-1"
                    loading
                    :loading-text="loading_text"
                    dense
                    dark
                >
                </v-data-table>
            </v-card>
        </div>
        <div class="col2">
            <Posts :community="this.selected" v-if="this.selected.length > 0" />
            <ImagePosts :community="this.selected" v-if="this.selected.length > 0" />
            <VideoPosts :community="this.selected" v-if="this.selected.length > 0" />
        </div>
    </v-col>
</template>

<script>
    import axiosInstance from '../helpers/interceptor';
    import Posts from './Posts.vue';
    import ImagePosts from './ImagePosts.vue';
    import VideoPosts from './VideoPosts.vue';

    export default {
        name: 'Communities',
        watch: {
            options: {
                handler() {
                    this.fetchData();
                },
                deep: true
            }
        },
        components: {Posts, ImagePosts, VideoPosts},
        data: function() {
            return {
                items: [],
                loading_text: "Loading... Please wait",
                selected: [],
                singleSelect: true,

                headers: [
                    {
                        text: 'Community',
                        value: 'name',
                    },
                    {
                        text: 'Tags',
                        value: 'tags',
                    },
                ],
                apiUrl: process.env.VUE_APP_COMMUNITIES_API_ENDPOINT,
                search: "",
                total: 0,
                page: 1,
                perPage: 10,
                options: {}
            }
        },
        methods: {
            async fetchData () {
                let params = Object.assign({}, this.options, {'name': this.search});
                let response = (await axiosInstance.get(this.apiUrl, {params: params})).data;
                this.items = response.data;

                this.total = response.pagination.total;
                this.size = (response.pagination.total-1) / response.pagination.page + 1;

                if (this.total == 0) {
                    this.loading_text = "no communities."
                }

            },
            handlePageChange(value) {
                this.page = value;
            },
            handleClick(selectedCommunity) {
                this.selected = [selectedCommunity];
            },
        }
    };

</script>

<style scoped>
.content {
    position: relative;
    left: 10px;
}
.col1 {
    position: relative;
    width: 20%;
    float: left;
    margin: 20px 0px 10px 0px;
}
.col2 {
    position: relative;
    float: left;
    width: 70%;
    padding: 10px 0px 10px 0px;
}
</style>