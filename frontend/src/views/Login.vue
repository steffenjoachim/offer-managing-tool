<template>
  <v-container class="fill-height" fluid>
    <v-row align="center" justify="center">
      <v-col cols="12" sm="8" md="4">
        <v-card class="elevation-12">
          <v-toolbar color="primary" dark flat>
            <v-toolbar-title>Anmeldung</v-toolbar-title>
          </v-toolbar>
          <v-card-text>
            <v-form @submit.prevent="login">
              <v-text-field
                v-model="username"
                label="Benutzername"
                name="username"
                prepend-icon="mdi-account"
                type="text"
                required
              ></v-text-field>
              <v-text-field
                v-model="password"
                label="Passwort"
                name="password"
                prepend-icon="mdi-lock"
                type="password"
                required
              ></v-text-field>
            </v-form>
          </v-card-text>
          <v-card-actions>
            <v-spacer></v-spacer>
            <v-btn color="primary" @click="login">Anmelden</v-btn>
          </v-card-actions>
          <v-card-text v-if="error" class="text-center red--text">
            {{ error }}
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
import axios from "axios";

export default {
  name: "Login",
  data() {
    return {
      username: "",
      password: "",
      error: null,
    };
  },
  methods: {
    async login() {
      try {
        this.error = null;
        const response = await axios.post(
          "http://localhost:8000/api/auth/login/",
          {
            username: this.username,
            password: this.password,
          }
        );

        // Token im Store speichern
        this.$store.dispatch("login", {
          user: {
            username: this.username,
            isAdmin: false, // Wird später vom Backend gesetzt
          },
          tokens: response.data,
        });

        // Zur Startseite navigieren
        this.$router.push("/");
      } catch (error) {
        this.error =
          "Anmeldung fehlgeschlagen. Bitte überprüfen Sie Ihre Eingaben.";
        console.error("Login error:", error);
      }
    },
  },
};
</script>
