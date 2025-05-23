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
  async register({ commit }, credentials) {
    try {
      const response = await axios.post(
        "http://localhost:8000/api/auth/register/",
        credentials
      );
      return response.data;
    } catch (error) {
      console.error("Registration error:", error);
      throw error;
    }
  },

  async login({ commit }, credentials) {
    try {
      const response = await axios.post(
        "http://localhost:8000/api/auth/login/",
        {
          username: credentials.username,
          password: credentials.password,
        }
      );
      const { access, refresh } = response.data;

      // Store tokens in localStorage
      localStorage.setItem("token", access);
      localStorage.setItem("refresh", refresh);

      // Fetch user details
      const userResponse = await axios.get(
        "http://localhost:8000/api/auth/user/",
        {
          headers: {
            Authorization: `Bearer ${access}`,
          },
        }
      );

      // Store user info
      const user = userResponse.data;
      localStorage.setItem("user", JSON.stringify(user));

      // Set axios default header
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
      // Remove tokens from localStorage
      localStorage.removeItem("token");
      localStorage.removeItem("refresh");
      localStorage.removeItem("user");

      // Remove axios default header
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
        // Set axios default header
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
