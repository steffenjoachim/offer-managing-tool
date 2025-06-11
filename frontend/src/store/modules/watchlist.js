import axios from "axios";

const state = {
  watchlist: [],
  loading: false,
  error: null,
};

const getters = {
  allWatchlistItems: (state) => state.watchlist,
  isLoading: (state) => state.loading,
  hasError: (state) => state.error !== null,
  errorMessage: (state) => state.error,
};

const actions = {
  async addListingToWatchlist({ commit, rootGetters }, listingId) {
    commit("SET_LOADING", true);
    try {
      const token = rootGetters["auth/accessToken"];
      if (!token) {
        throw new Error("Authentifizierungstoken nicht gefunden.");
      }
      axios.defaults.headers.common["Authorization"] = `Bearer ${token}`;

      const response = await axios.post(`/api/watchlist/items/`, {
        listing_id: listingId,
      });
      commit("ADD_LISTING_TO_WATCHLIST", response.data.listing);
      return true;
    } catch (error) {
      console.error("Fehler beim Hinzufügen zur Merkliste:", error);
      commit(
        "SET_ERROR",
        error.response?.data?.detail || "Fehler beim Hinzufügen zur Merkliste."
      );
      throw error;
    } finally {
      commit("SET_LOADING", false);
    }
  },

  async removeListingFromWatchlist({ commit, rootGetters }, listingId) {
    commit("SET_LOADING", true);
    try {
      const token = rootGetters["auth/accessToken"];
      if (!token) {
        throw new Error("Authentifizierungstoken nicht gefunden.");
      }
      axios.defaults.headers.common["Authorization"] = `Bearer ${token}`;

      await axios.delete(`/api/watchlist/items/${listingId}/remove/`);
      commit("REMOVE_LISTING_FROM_WATCHLIST", listingId);
      return true;
    } catch (error) {
      console.error("Fehler beim Entfernen aus der Merkliste:", error);
      commit(
        "SET_ERROR",
        error.response?.data?.detail ||
          "Fehler beim Entfernen aus der Merkliste."
      );
      throw error;
    } finally {
      commit("SET_LOADING", false);
    }
  },

  async fetchWatchlist({ commit, rootGetters }) {
    commit("SET_LOADING", true);
    try {
      const token = rootGetters["auth/accessToken"];
      if (!token) {
        throw new Error("Authentifizierungstoken nicht gefunden.");
      }
      axios.defaults.headers.common["Authorization"] = `Bearer ${token}`;

      const response = await axios.get("/api/watchlist/items/");
      commit("SET_WATCHLIST", response.data);

      return response.data;
    } catch (error) {
      console.error("Fehler beim Abrufen der Merkliste:", error);
      commit(
        "SET_ERROR",
        error.response?.data?.detail || "Fehler beim Abrufen der Merkliste."
      );
      throw error;
    } finally {
      commit("SET_LOADING", false);
    }
  },
};

const mutations = {
  SET_WATCHLIST(state, items) {
    state.watchlist = items;
    state.error = null;
  },
  ADD_LISTING_TO_WATCHLIST(state, listing) {
    if (!state.watchlist.some((item) => item.id === listing.id)) {
      state.watchlist.push(listing);
    }
    state.error = null;
  },
  REMOVE_LISTING_FROM_WATCHLIST(state, listingId) {
    state.watchlist = state.watchlist.filter((item) => item.id !== listingId);
    state.error = null;
  },
  SET_LOADING(state, loading) {
    state.loading = loading;
  },
  SET_ERROR(state, error) {
    state.error = error;
  },
};

export default {
  namespaced: true,
  state,
  getters,
  actions,
  mutations,
};
