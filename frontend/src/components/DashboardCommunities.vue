<template>
    <div class="dashboard-communities">
        <h4>Communities</h4>
        <label for="text-communities">How many communities to create?</label>
        <input type="text" id="text-communities" v-model="num_communities" placeholder=num_communities />
        <button id="button-communities" class="ui primary button" role="button" v-on:click="create_communities()" >
            Go
        </button>

        <div class="field" id="alert">
            <v-alert dense text type="success">
                Created "communities.length" communities.
            </v-alert>
        </div>
    </div>
</template>