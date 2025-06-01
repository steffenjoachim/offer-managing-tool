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

  async sendMessage({ commit }, { conversationId, message }) {
    commit("SET_LOADING", true);
    try {
      const response = await axios.post(
        `http://127.0.0.1:8000/api/messages/conversations/${conversationId}/messages/`,
        {
          content: message,
        }
      );
      commit("ADD_MESSAGE", response.data);
      return response.data;
    } catch (error) {
      commit(
        "SET_ERROR",
        error.response?.data?.detail || "Fehler beim Senden der Nachricht"
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
};

const mutations = {
  SET_CONVERSATIONS(state, conversations) {
    state.conversations = conversations;
  },
  SET_CURRENT_CONVERSATION(state, conversation) {
    state.currentConversation = conversation;
  },
  SET_LOADING(state, loading) {
    state.loading = loading;
  },
  SET_ERROR(state, error) {
    state.error = error;
  },
  ADD_MESSAGE(state, message) {
    if (state.currentConversation) {
      state.currentConversation.messages.push(message);
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
