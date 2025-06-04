import axios from "axios";

const state = {
  token: localStorage.getItem("token") || null,
  user: JSON.parse(localStorage.getItem("user")) || null,
};

const getters = {
  isLoggedIn: (state) => !!state.user,
  username: (state) => state.user?.username || "",
  isAdmin: (state) => state.user?.isAdmin || false,
  accessToken: (state) => state.token,
  currentUser: (state) => state.user,
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
      // 1. Login-Request an Backend
      const response = await axios.post(
        "http://localhost:8000/api/auth/login/",
        credentials
      );
      const { access, refresh } = response.data;

      // 2. User-Info holen
      const userResponse = await axios.get(
        "http://localhost:8000/api/auth/user/",
        {
          headers: {
            Authorization: `Bearer ${access}`,
          },
        }
      );
      const user = userResponse.data;

      // 3. Tokens und User speichern
      localStorage.setItem("access_token", access);
      localStorage.setItem("refresh_token", refresh);
      axios.defaults.headers.common["Authorization"] = `Bearer ${access}`;
      commit("setUser", user);
      commit("setAdmin", user.isAdmin);
      commit("setTokens", { access, refresh });
      return { user, tokens: { access, refresh } };
    } catch (error) {
      console.error("Login error:", error);
      throw error;
    }
  },

  logout({ commit }) {
    console.log("Auth Store: logout action called.");
    localStorage.removeItem("access_token");
    localStorage.removeItem("refresh_token");

    delete axios.defaults.headers.common["Authorization"];

    commit("CLEAR_AUTH");
    console.log("Auth Store: Auth data cleared from store.");
  },

  async checkAuth({ commit, dispatch }) {
    console.log("Auth Store: checkAuth action called.");
    const accessToken = localStorage.getItem("access_token");
    const refreshToken = localStorage.getItem("refresh_token");

    if (accessToken && refreshToken) {
      console.log("Auth Store: Tokens found in localStorage.");
      axios.defaults.headers.common["Authorization"] = `Bearer ${accessToken}`;

      try {
        const response = await axios.get(
          "http://localhost:8000/api/auth/user/"
        );
        const user = response.data;
        console.log("Auth Store: User data fetched from backend:", user);
        commit("setUser", user);
        commit("setAdmin", user.is_admin || false);
        commit("setTokens", { access: accessToken, refresh: refreshToken });
        console.log(
          "Auth Store: User and tokens set in store after checkAuth."
        );
      } catch (error) {
        console.error(
          "Auth Store: Error fetching user data during checkAuth:",
          error
        );
        dispatch("logout");
      }
    } else {
      console.log(
        "Auth Store: No tokens found in localStorage. User not logged in."
      );
      commit("CLEAR_AUTH");
    }
  },
};

const mutations = {
  SET_AUTH(state, { token, user }) {
    state.token = token;
    state.user = user;
    console.log("Auth Store Mutation: SET_AUTH called with user:", user);
  },
  CLEAR_AUTH(state) {
    state.token = null;
    state.user = null;
    console.log("Auth Store Mutation: CLEAR_AUTH called.");
  },
  setUser(state, user) {
    state.user = user;
    console.log("Auth Store Mutation: setUser called with user:", user);
  },
  setAdmin(state, value) {
    state.isAdmin = value;
  },
  setTokens(state, tokens) {
    state.tokens = tokens;
  },
};

export default {
  namespaced: true,
  state,
  getters,
  actions,
  mutations,
};
