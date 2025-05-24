import axios from "axios";
import store from "../index"; // Importieren Sie den Haupt-Store

const state = {
  listings: [],
  loading: false,
  error: null,
};

const getters = {
  allListings: (state) => state.listings,
  isLoading: (state) => state.loading,
  error: (state) => state.error,
};

const actions = {
  async fetchListings({ commit }) {
    console.log("Fetching listings..."); // Debugging-Ausgabe
    commit("setLoading", true);
    try {
      // Token aus dem Haupt-Store abrufen
      const token = store.getters["auth/accessToken"];
      const headers = token ? { Authorization: `Bearer ${token}` } : {};

      console.log("Attempting to fetch listings with axios..."); // Neue Debugging-Ausgabe
      const response = await axios.get("http://localhost:8000/api/listings/", {
        headers: headers,
      });
      commit("setListings", response.data);
      return response.data;
    } catch (error) {
      console.error("Error fetching listings:", error); // Erweiterte Fehlerausgabe
      commit(
        "setError",
        error.response?.data?.detail || "Failed to fetch listings"
      );
      throw error;
    } finally {
      commit("setLoading", false);
    }
  },

  async createListing({ commit }, formData) {
    commit("setLoading", true);
    try {
      // Token aus dem Haupt-Store abrufen
      const token = store.getters["auth/accessToken"];

      const response = await axios.post(
        "http://localhost:8000/api/listings/",
        formData,
        {
          headers: {
            "Content-Type": "multipart/form-data",
            Authorization: `Bearer ${token}`, // Token manuell hinzufügen
          },
        }
      );
      commit("addListing", response.data);
      return response.data;
    } catch (error) {
      commit(
        "setError",
        error.response?.data?.detail || "Failed to create listing"
      );
      throw error;
    } finally {
      commit("setLoading", false);
    }
  },
};

const mutations = {
  setListings(state, listings) {
    state.listings = listings;
  },
  addListing(state, listing) {
    state.listings.unshift(listing);
  },
  setLoading(state, loading) {
    state.loading = loading;
  },
  setError(state, error) {
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
