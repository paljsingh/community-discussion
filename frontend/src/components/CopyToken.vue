<template>
    <div v-if="usertype === 'okta'" class="copy-token">
        <input type="text" v-model="mutableItem.token" hidden>
        <v-btn type="button" v-clipboard:copy="item.token" @click="snackbar = true">
            <v-icon dark>mdi-content-copy</v-icon>
        </v-btn>
        <v-snackbar v-model="snackbar" :timeout="timeout">
            Token Copied to clipboard.
        </v-snackbar>

    </div>
</template>

<script>
    import Vue from 'vue';
    import VueClipboard from 'vue-clipboard2';
    VueClipboard.config.autoSetContainer = true
    Vue.use(VueClipboard)
    import authHandler from '../auth/index.js';

    export default {
        name: 'CopyToken',
        mixins: [authHandler],
        props: ['item'],
        data: function() {
            return {
                snackbar: false,
                timeout: 1000,
                mutableItem: this.item,
            }
        },
    };
</script>

<style scoped>
.copy-token{
    position: relative;
    float: left;
    width: 20%;
    font-size: 12px;
    background: #000;
}
</style>