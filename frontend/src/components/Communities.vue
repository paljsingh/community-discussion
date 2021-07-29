<template>
    <div class="communities">
        <vuetable ref="vuetable"
            class="communities"
            :api-url="'http://127.0.0.1:5000/api/v1/communities'"
            :fields="fields"
            :current-page="0"
            :per-page="20"
            filter=""
            data-path="communities"
            pagination-path=""
            >
        </vuetable>
    </div>
</template>

<script>
    import axios from 'axios';

    export default {
        name: 'Communities',
        props: ['token', 'usertype'],
        data: function() {
            return {
                communities: [],
                fields: [
                    {
                      name: 'name',
                      title: 'Community Name'
                    },
                    {
                      name: 'description',
                      title: 'Description'
                    },
                    {
                      name: 'created_by',
                      title: 'Created By'
                    },
                    {
                      name: 'created_on',
                      title: 'Created On'
                    },
                    {
                      name: 'join',
                      title: 'Join Community'
                    },
                ]
            }
        },
        methods: {
            async get_communities () {
                try {
                    const response = await axios.get(process.env.VUE_APP_COMMUNITIES_API_ENDPOINT)
                    this.communities = response.data.communities
                } catch (e) {
                    console.error(e)
                    this.failed = true
                }
            }
        }
    };

</script>

<style scoped>
.communities {
    position: relative;
    float: left;
    width: 80%;
}
</style>