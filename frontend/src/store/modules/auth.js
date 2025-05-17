import axios from "axios";

const state = {
  token: localStorage.getItem("token") || null,
  user: JSON.parse(localStorage.getItem("user")) || null,
};

const getters = {
  isLoggedIn: (state) => !!state.token,
  username: (state) => state.user?.username || "",
  isAdmin: (state) => state.user?.isAdmin || false,
};

const actions = {
  async login({ commit }, credentials) {
    try {
      const response = await axios.post(
        "http://localhost:8000/api/auth/login/",
        credentials
      );
      const { access, refresh } = response.data;

      // Token im localStorage speichern
      localStorage.setItem("token", access);
      localStorage.setItem("refresh", refresh);

      // User-Informationen speichern
      const user = {
        username: credentials.username,
        isAdmin: false, // Wird später vom Backend gesetzt
      };
      localStorage.setItem("user", JSON.stringify(user));

      // Axios Default Header setzen
      axios.defaults.headers.common["Authorization"] = `Bearer ${access}`;

      commit("SET_AUTH", { token: access, user });
      return response.data;
    } catch (error) {
      console.error("Login error:", error);
      throw error;
    }
  },

  async logout({ commit }) {
    try {
      // Token aus localStorage entfernen
      localStorage.removeItem("token");
      localStorage.removeItem("refresh");
      localStorage.removeItem("user");

      // Axios Default Header entfernen
      delete axios.defaults.headers.common["Authorization"];

      commit("CLEAR_AUTH");
    } catch (error) {
      console.error("Logout error:", error);
      throw error;
    }
  },

  async checkAuth({ commit }) {
    try {
      const token = localStorage.getItem("token");
      const user = JSON.parse(localStorage.getItem("user"));

      if (token && user) {
        // Axios Default Header setzen
        axios.defaults.headers.common["Authorization"] = `Bearer ${token}`;
        commit("SET_AUTH", { token, user });
      }
    } catch (error) {
      console.error("Check auth error:", error);
      commit("CLEAR_AUTH");
    }
  },
};

const mutations = {
  SET_AUTH(state, { token, user }) {
    state.token = token;
    state.user = user;
  },
  CLEAR_AUTH(state) {
    state.token = null;
    state.user = null;
  },
};

export default {
  namespaced: true,
  state,
  getters,
  actions,
  mutations,
};
