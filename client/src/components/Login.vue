<template>
<v-container>
    <v-main>
    <div class="login">
        <!-- <section class="section">
        <div class="container"> -->
            <v-toolbar-title><strong>Login</strong></v-toolbar-title>
            <v-card-text style="margin-top: 20px;">
            <v-form>
            <div class="field">
                <label class="label is-large" for="username"></label>
                    <v-text-field outlined label="Username" name="username" type="username" class="input is-large" id="username" prepend-icon="mdi-account" v-model="username"></v-text-field>
            </div>
            <div class="field">
                <label class="label is-large" for="password"></label>
                <div class="control">
                    <v-text-field outlined prepend-icon="mdi-lock" label="Password" name="password" :append-icon="show3 ? 'mdi-eye' : 'mdi-eye-off'" :rules="[rules.required, rules.min]" :type="show3 ? 'text' : 'password'" hint="At least 8 characters" class="input-group--focused" @click:append="show3 = !show3"
                    v-model="password"></v-text-field>
                </div>
            </div>
            <div class="text-center">
                <v-btn style="margin: 5px;" @click="authenticate">Login</v-btn>
                <v-btn style="margin: 5px;" @click="register">Register</v-btn>
            </div>
            </v-form>
            </v-card-text>
        <!-- </div>
        </section> -->
    </div>
    </v-main>
    </v-container>
</template>

<script>
export default {
    name: 'Login',
    data() {
    return {
        username: '',
        password: '',
        proccessing: false,
        show3: false,
        rules: {
          required: (value) => !!value || 'Required.',
          min: (v) => v.length >= 8 || 'Min 8 characters',
          emailMatch: () => ('The email and password you entered don\'t match'),
        },
    };
    },
};
</script>

<style scoped>
.login {
    width: 500px;
    height: 400px;
    border: 1px solid #cccccc;
    background-color: #000000;
    margin: auto;
    margin-top: 80px;
    padding: 20px;
}
.input-form {
    margin-bottom: 9px;
}
</style>
