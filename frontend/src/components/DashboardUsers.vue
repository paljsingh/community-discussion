<template>
    <div class="dashboard-users">
        <h4>Communities</h4>
        <label for="text-users">How many users to create?</label>
        <input type="text" id="text-users" v-model="num_communities" placeholder=num_users />
        <button id="button-users" class="ui primary button" role="button" v-on:click="create_users()" >
            Go
        </button>

        <div class="field" id="alert">
            <v-alert dense text type="success">
                Created "users.length" users.
            </v-alert>
        </div>
    </div>
</template>