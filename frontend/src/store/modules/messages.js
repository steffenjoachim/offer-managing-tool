import axios from "axios";

const state = {
  conversations: [],
  currentConversation: null,
  loading: false,
  error: null,
};

const getters = {
  allConversations: (state) => state.conversations,
  currentConversation: (state) => state.currentConversation,
  isLoading: (state) => state.loading,
  hasError: (state) => state.error !== null,
  errorMessage: (state) => state.error,
  unreadCount: (state) =>
    state.conversations.filter((conv) => !conv.isRead).length,
};

const actions = {
  async fetchConversations({ commit }) {
    commit("SET_LOADING", true);
    try {
      const response = await axios.get(
        "http://127.0.0.1:8000/api/messages/conversations/"
      );
      commit("SET_CONVERSATIONS", response.data);
      return response.data;
    } catch (error) {
      commit(
        "SET_ERROR",
        error.response?.data?.detail || "Fehler beim Laden der Konversationen"
      );
      throw error;
    } finally {
      commit("SET_LOADING", false);
    }
  },

  async fetchConversation({ commit }, conversationId) {
    commit("SET_LOADING", true);
    try {
      const response = await axios.get(
        `http://127.0.0.1:8000/api/messages/conversations/${conversationId}/`
      );
      commit("SET_CURRENT_CONVERSATION", response.data);
      return response.data;
    } catch (error) {
      commit(
        "SET_ERROR",
        error.response?.data?.detail || "Fehler beim Laden der Konversation"
      );
      throw error;
    } finally {
      commit("SET_LOADING", false);
    }
  },

  async sendMessage({ commit, rootGetters }, { conversationId, content }) {
    console.log("Debug (messages.js - sendMessage): Starte sendMessage", {
      conversationId,
      content,
    });
    commit("SET_LOADING", true);
    try {
      const token = rootGetters["auth/accessToken"];
      if (!token) {
        console.error(
          "Debug (messages.js - sendMessage): Access token nicht gefunden."
        );
        throw new Error("Authentifizierungstoken nicht gefunden.");
      }
      axios.defaults.headers.common["Authorization"] = `Bearer ${token}`;

      const response = await axios.post(
        `http://127.0.0.1:8000/api/messages/conversations/${conversationId}/messages/`,
        { text: content } // Backend erwartet 'text' für den Nachrichteninhalt
      );
      console.log(
        "Debug (messages.js - sendMessage): Nachricht erfolgreich gesendet.",
        response.data
      );
      // Aktualisiere die Konversation mit der neuen Nachricht
      commit("ADD_MESSAGE_TO_CONVERSATION", {
        conversationId,
        message: response.data,
      });
      return response.data;
    } catch (error) {
      console.error(
        "Debug (messages.js - sendMessage): Fehler beim Senden der Nachricht:",
        error.response?.data || error.message
      );
      commit(
        "SET_ERROR",
        error.response?.data?.detail || "Fehler beim Senden der Nachricht."
      );
      throw error;
    } finally {
      commit("SET_LOADING", false);
      console.log(
        "Debug (messages.js - sendMessage): sendMessage abgeschlossen."
      );
    }
  },

  async sendMessageToListing({ commit, dispatch }, { listingId, content }) {
    commit("SET_LOADING", true);
    try {
      // Zuerst eine neue Konversation erstellen
      const conversationResponse = await axios.post(
        "http://localhost:8000/api/messages/conversations/",
        {
          listing: listingId,
          participants: [], // Das Backend wird den aktuellen Benutzer automatisch hinzufügen
        }
      );

      const conversationId = conversationResponse.data.id;

      // Dann die Nachricht in der neuen Konversation senden
      const response = await axios.post(
        `http://localhost:8000/api/messages/conversations/${conversationId}/messages/`,
        {
          text: content,
        }
      );

      // Aktualisiere die Konversationsliste
      await dispatch("fetchConversations");
      return response.data;
    } catch (error) {
      console.error(
        "Fehler beim Senden der Nachricht:",
        error.response?.data || error
      );
      throw error;
    } finally {
      commit("SET_LOADING", false);
    }
  },

  async markAsRead({ commit }, conversationId) {
    try {
      await axios.post(
        `http://127.0.0.1:8000/api/messages/conversations/${conversationId}/mark_as_read/`
      );
      commit("MARK_CONVERSATION_AS_READ", conversationId);
    } catch (error) {
      commit(
        "SET_ERROR",
        error.response?.data?.detail || "Fehler beim Markieren als gelesen"
      );
      throw error;
    }
  },

  async deleteConversation({ dispatch }, conversationId) {
    await axios.delete(
      `http://127.0.0.1:8000/api/messages/conversations/${conversationId}/`
    );
    await dispatch("fetchConversations");
  },
};

const mutations = {
  SET_CONVERSATIONS(state, conversations) {
    state.conversations = conversations;
    state.error = null;
  },
  SET_CURRENT_CONVERSATION(state, conversation) {
    state.currentConversation = conversation;
    state.error = null;
  },
  SET_LOADING(state, loading) {
    state.loading = loading;
  },
  SET_ERROR(state, error) {
    state.error = error;
  },
  ADD_MESSAGE_TO_CONVERSATION(state, { conversationId, message }) {
    console.log(
      "Debug (messages.js - ADD_MESSAGE_TO_CONVERSATION): Nachricht hinzufügen zu Konversation",
      conversationId,
      message
    );
    const conversation = state.conversations.find(
      (conv) => conv.id === conversationId
    );
    if (conversation) {
      conversation.messages.push(message);
      conversation.last_message = message;
      // Sortiere Konversationen, damit die zuletzt aktualisierte oben steht
      state.conversations.sort(
        (a, b) =>
          new Date(b.last_message.timestamp) -
          new Date(a.last_message.timestamp)
      );
    }
  },
  MARK_CONVERSATION_AS_READ(state, conversationId) {
    const conversation = state.conversations.find(
      (c) => c.id === conversationId
    );
    if (conversation) {
      conversation.isRead = true;
      conversation.unreadCount = 0;
    }
  },
};

export default {
  namespaced: true,
  state,
  getters,
  actions,
  mutations,
};
