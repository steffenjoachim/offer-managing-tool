import { createStore } from "vuex";
import axios from "axios";
import auth from "./modules/auth";
import listings from "./modules/listings";
import messages from "./modules/messages";

export default createStore({
  modules: {
    auth,
    listings,
    messages,
  },
  state: {
    isAdmin: false,
    user: null,
    tokens: null,
  },
  mutations: {
    setAdmin(state, value) {
      state.isAdmin = value;
    },
    setUser(state, user) {
      state.user = user;
    },
    setTokens(state, tokens) {
      state.tokens = tokens;
    },
    clearAuth(state) {
      state.user = null;
      state.isAdmin = false;
      state.tokens = null;
    },
  },
  actions: {
    login({ commit }, { user, tokens }) {
      // Token im localStorage speichern
      localStorage.setItem("access_token", tokens.access);
      localStorage.setItem("refresh_token", tokens.refresh);

      // Axios Default Header setzen
      axios.defaults.headers.common[
        "Authorization"
      ] = `Bearer ${tokens.access}`;

      // Store aktualisieren
      commit("setUser", user);
      commit("setAdmin", user.isAdmin);
      commit("setTokens", tokens);
    },
    logout({ commit }) {
      // Token aus localStorage entfernen
      localStorage.removeItem("access_token");
      localStorage.removeItem("refresh_token");

      // Axios Default Header entfernen
      delete axios.defaults.headers.common["Authorization"];

      // Store zurücksetzen
      commit("clearAuth");
    },
    checkAuth({ commit, dispatch }) {
      const accessToken = localStorage.getItem("access_token");
      const refreshToken = localStorage.getItem("refresh_token");

      if (accessToken && refreshToken) {
        // Axios Default Header setzen
        axios.defaults.headers.common[
          "Authorization"
        ] = `Bearer ${accessToken}`;

        // Benutzerinformationen abrufen
        axios
          .get("http://localhost:8000/api/auth/user/")
          .then((response) => {
            const user = response.data;
            commit("setUser", user);
            commit("setAdmin", user.is_admin || false);
            commit("setTokens", { access: accessToken, refresh: refreshToken });
          })
          .catch(() => {
            // Bei Fehler ausloggen
            dispatch("logout");
          });
      }
    },
  },
  getters: {
    isLoggedIn: (state, getters) => getters["auth/isLoggedIn"],
    username: (state, getters) => getters["auth/username"],
    isAdmin: (state, getters) => getters["auth/isAdmin"],
    currentUser: (state, getters) => getters["auth/currentUser"],
  },
});
