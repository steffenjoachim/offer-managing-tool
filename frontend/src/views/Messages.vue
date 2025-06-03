<template>
  <div class="messages-container">
    <el-card class="messages-card">
      <template #header>
        <div class="card-header">
          <el-icon><Message /></el-icon>
          <span>My Messages</span>
        </div>
      </template>

      <div v-if="currentDisplayState === 'loading'" class="loading-container">
        <el-skeleton :rows="3" animated />
      </div>

      <div v-else-if="currentDisplayState === 'error'" class="error-container">
        <el-alert :title="error" type="error" :closable="false" show-icon />
      </div>

      <div
        v-else-if="currentDisplayState === 'no-messages'"
        class="no-messages"
      >
        <el-empty
          description="No Messages so far, start interacting with the community!"
        >
          <!-- Removed button as requested -->
          <!-- <el-button type="primary" @click="navigateToCommunity">
            Zur Community
          </el-button> -->
        </el-empty>
      </div>

      <div
        v-else-if="currentDisplayState === 'list'"
        class="conversations-list"
      >
        <el-scrollbar height="calc(100vh - 200px)">
          <div style="font-size: 10px; color: purple">
            Debug conversationDisplayTexts: {{ conversationDisplayTexts }}
          </div>
          <div
            v-for="(conversation, index) in conversations"
            :key="conversation.id"
            class="conversation-item"
            :class="{ unread: !conversation.isRead }"
            @click="openConversation(conversation.id)"
          >
            <div class="conversation-header">
              <div class="conversation-info-block">
                <div class="listing-title">
                  {{ conversation.listing ? conversation.listing.title : "" }}
                </div>
                <div class="sender-info">
                  {{ conversationDisplayTexts[index] }}
                  <span style="font-size: 10px; color: brown">
                    (Debug text: {{ conversationDisplayTexts[index] }})
                  </span>
                </div>
              </div>
              <div class="header-right">
                <span class="timestamp">
                  {{
                    formatDate(
                      conversation.last_message
                        ? conversation.last_message.timestamp
                        : null
                    )
                  }}
                </span>
              </div>
            </div>
            <div class="last-message-box">
              <div class="last-message">
                {{
                  conversation.last_message
                    ? conversation.last_message.text
                    : ""
                }}
              </div>
              <span
                class="delete-x"
                @click.stop="confirmDelete(conversation.id)"
                title="Delete conversation"
                tabindex="0"
                role="button"
                aria-label="Delete conversation"
              >
                <span class="delete-x-inner">×</span>
              </span>
            </div>
            <el-badge
              v-if="conversation.unreadCount > 0"
              :value="conversation.unreadCount"
              class="unread-badge"
            />
          </div>
        </el-scrollbar>
      </div>
    </el-card>
    <el-dialog
      v-model="deleteDialogVisible"
      title="Delete Conversation"
      width="30%"
      :before-close="handleDeleteDialogClose"
    >
      <span>Are you sure you want to delete this conversation?</span>
      <template #footer>
        <el-button @click="handleDeleteDialogClose">Cancel</el-button>
        <el-button type="danger" @click="deleteConversation">Delete</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script>
import { ref, onMounted, computed, watch } from "vue";
import { useRouter } from "vue-router";
import { useStore } from "vuex";
import { Message } from "@element-plus/icons-vue";
import { ElMessage } from "element-plus";

export default {
  name: "MessagesView",
  components: {
    Message,
  },
  setup() {
    const router = useRouter();
    const store = useStore();

    const loading = computed(() => store.getters["messages/isLoading"]);
    const error = computed(() => store.getters["messages/errorMessage"]);

    const isLoggedIn = computed(() => store.getters["auth/isLoggedIn"]);

    const conversations = computed(() => {
      console.log(
        "Computed conversations evaluated:",
        "Store data length:",
        store.getters["messages/allConversations"]?.length
      );
      return store.getters["messages/allConversations"];
    });

    const currentUser = computed(() => {
      console.log(
        "Computed currentUser evaluated:",
        store.getters["auth/currentUser"]
      );
      // Ensure currentUser is reactive to changes in the store
      return store.getters["auth/currentUser"];
    });

    const conversationDisplayTexts = computed(() => {
      console.log(
        "Computed conversationDisplayTexts evaluated:",
        "Conversations:",
        conversations.value?.length
      );

      // Return empty array immediately if no conversations or currentUser is not available
      if (
        !conversations.value ||
        conversations.value.length === 0 ||
        currentUser.value === null
      ) {
        return [];
      }

      // Now that we know currentUser is not null, it's safe to access its properties
      const currentUserId = currentUser.value.id;

      return conversations.value.map((conversation) => {
        if (!conversation.last_message) {
          return "";
        }

        const senderId = Number(conversation.last_message.sender?.id);

        if (isNaN(senderId)) {
          return "";
        }

        if (senderId === currentUserId) {
          const recipientUsername =
            conversation.last_message.empfaenger?.username ||
            "Empfänger unbekannt";
          return `to: ${recipientUsername}`;
        } else {
          const senderUsername =
            conversation.last_message.sender?.username || "Sender unbekannt";
          return `sender: ${senderUsername}`;
        }
      });
    });

    // Flag to prevent fetching conversations multiple times
    const hasFetchedConversations = ref(false); // Resetting to a simpler flag

    // Watch for changes in isLoggedIn and currentUser, mainly to handle logout
    watch([isLoggedIn, currentUser], ([newIsLoggedIn, newUser]) => {
      console.log(
        "currentUser or isLoggedIn watched:",
        "newUser:",
        newUser,
        "newIsLoggedIn:",
        newIsLoggedIn,
        "hasFetchedConversations:",
        hasFetchedConversations.value
      );

      if (!newIsLoggedIn || !newUser) {
        // If user logs out or currentUser becomes null/undefined, reset state
        console.log(
          "User logged out or user object became null/undefined, resetting fetched flag."
        );
        hasFetchedConversations.value = false;
        // Optionally clear conversations from store here if needed on logout
        // store.commit("messages/SET_CONVERSATIONS", []);
      }
      // Initial fetching is handled in onMounted now
    });

    const currentDisplayState = computed(() => {
      console.log(
        "Computed currentDisplayState evaluated:",
        "loading:",
        loading.value,
        "error:",
        error.value,
        "isLoggedIn:",
        isLoggedIn.value,
        "currentUser:",
        currentUser.value !== null, // Check if currentUser is not null/undefined
        "conversations.length:",
        conversations.value?.length
      );

      // 1. Priority: Loading State
      // Show loading if the message store is loading OR if user is logged in but currentUser object is not yet available
      // We also show loading if the user is logged in but conversations haven't been fetched yet
      if (
        loading.value ||
        (isLoggedIn.value && currentUser.value === null) ||
        (isLoggedIn.value && !hasFetchedConversations.value)
      ) {
        console.log(
          "Display state is loading due to loading state, missing currentUser, or conversations not yet fetched for logged in user."
        );
        return "loading";
      }

      // 2. Priority: Error State
      if (error.value) {
        console.log("Display state is error.");
        return "error";
      }

      // 3. Priority: User not logged in (should be handled by router guard, but as a fallback)
      if (!isLoggedIn.value) {
        console.log(
          "Display state is loading because user is not logged in (should be handled by router guard)."
        );
        return "loading"; // Or potentially a different state if app allows visiting this page when logged out
      }

      // 4. Priority: Messages available
      if (conversations.value?.length > 0) {
        console.log("Display state is list.");
        return "list";
      }

      // 5. Last Priority: No messages
      if (conversations.value?.length === 0) {
        console.log("Display state is no-messages.");
        return "no-messages";
      }

      // Fallback for unexpected states
      console.log("Display state is fallback loading.");
      return "loading";
    });

    const deleteDialogVisible = ref(false);
    const conversationToDelete = ref(null);

    const fetchConversations = async () => {
      store.commit("messages/SET_LOADING", true);
      try {
        await store.dispatch("messages/fetchConversations");
      } catch (error) {
        console.error("Fehler beim Laden der Konversationen:", error);
        store.commit(
          "messages/SET_ERROR",
          error.message || "Fehler beim Laden der Konversationen."
        );
      } finally {
        store.commit("messages/SET_LOADING", false);
      }
    };

    const formatDate = (date) => {
      if (!date) return "";

      const timestamp = Date.parse(date);

      if (isNaN(timestamp)) {
        return "Invalid Date";
      }

      const options = {
        day: "2-digit",
        month: "2-digit",
        year: "numeric",
        hour: "2-digit",
        minute: "2-digit",
      };
      return new Date(timestamp).toLocaleDateString("de-DE", options);
    };

    const getOtherParticipantUsername = (conversation) => {
      if (!currentUser.value || !conversation.participants) return "";
      if (conversation.participants.length === 1) {
        return conversation.participants[0].username;
      }
      const otherParticipant = conversation.participants.find(
        (participant) => participant.id !== currentUser.value.id
      );
      return otherParticipant
        ? otherParticipant.username
        : "Unknown Participant";
    };

    const openConversation = async (conversationId) => {
      try {
        await store.dispatch("messages/markAsRead", conversationId);
        ElMessage.success("Message marked as read.");
        console.log("Öffne Konversation:", conversationId);
        setTimeout(() => {
          fetchConversations();
        }, 250);
      } catch (error) {
        console.error("Fehler beim Öffnen der Konversation:", error);
        ElMessage.error("Failed to mark message as read.");
      }
    };

    const confirmDelete = (conversationId) => {
      conversationToDelete.value = conversationId;
      deleteDialogVisible.value = true;
    };
    const handleDeleteDialogClose = () => {
      deleteDialogVisible.value = false;
      conversationToDelete.value = null;
    };
    const deleteConversation = async () => {
      try {
        await store.dispatch(
          "messages/deleteConversation",
          conversationToDelete.value
        );
        ElMessage.success("Conversation deleted.");
      } catch (error) {
        ElMessage.error("Failed to delete conversation.");
      } finally {
        handleDeleteDialogClose();
      }
    };

    onMounted(() => {
      console.log("onMounted: Initialization complete.");
      // On mount, check if the user is already logged in and the user object is available
      // If so, and conversations haven't been fetched yet, fetch them.
      if (
        isLoggedIn.value &&
        currentUser.value !== null &&
        !hasFetchedConversations.value
      ) {
        console.log(
          "onMounted: User is logged in and user object available, fetching conversations."
        );
        fetchConversations();
        hasFetchedConversations.value = true; // Set flag after initiating fetch
      } else {
        console.log(
          "onMounted: User not logged in or currentUser not available yet, or conversations already fetched."
        );
      }
    });

    return {
      loading,
      error,
      conversations,
      formatDate,
      getOtherParticipantUsername,
      openConversation,
      isLoggedIn,
      currentUser,
      conversationDisplayTexts,
      deleteDialogVisible,
      conversationToDelete,
      confirmDelete,
      handleDeleteDialogClose,
      deleteConversation,
      currentDisplayState,
    };
  },
};
</script>

<style scoped>
.messages-container {
  max-width: 800px;
  margin: 0 auto;
  padding: 20px;
}

.messages-card {
  margin-bottom: 20px;
}

.card-header {
  display: flex;
  align-items: center;
  gap: 8px;
}

.loading-container {
  padding: 20px;
}

.error-container {
  padding: 20px;
}

.no-messages {
  padding: 40px 0;
}

.conversations-list {
  margin-top: 16px;
}

.conversation-item {
  padding: 16px;
  background: #f0f9ff;
  margin-bottom: 8px;
  border-radius: 6px;
  border: 1px solid #e0e0e0;
  cursor: pointer;
  position: relative;
  transition: background-color 0.3s;
}

.conversation-item:hover {
  background-color: #eaf6ff;
}

.conversation-item.unread {
  background-color: #e3f2fd;
  font-weight: bold;
}

.conversation-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 8px;
}

.conversation-info-block {
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  gap: 2px;
}

.listing-title {
  color: #409eff;
  font-weight: 500;
  margin-bottom: 2px;
}

.sender-info {
  color: #909399;
  font-size: 0.95em;
  font-weight: normal;
  color: #909399;
}

.header-right {
  display: flex;
  flex-direction: column;
  align-items: flex-end;
  min-width: 120px;
}

.timestamp {
  color: #909399;
  font-size: 0.9em;
  margin-bottom: 2px;
}

.last-message-box {
  display: flex;
  align-items: flex-end;
  position: relative;
}

.last-message {
  color: #606266;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  flex: 1;
}

.delete-x {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 16px;
  height: 16px;
  border: 1px solid #bbb;
  border-radius: 4px;
  background: #fff;
  cursor: pointer;
  position: absolute;
  right: 12px;
  bottom: 6px;
  transition: background 0.2s, color 0.2s;
  box-sizing: border-box;
  padding: 0;
  outline: none;
}
.delete-x-inner {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 100%;
  height: 100%;
  font-size: 13px;
  line-height: 1;
  color: #888;
  user-select: none;
}
.delete-x:hover .delete-x-inner {
  color: #d32f2f;
}
.delete-x:hover {
  border-color: #d32f2f;
  background: #fbe9e7;
}

.unread-badge {
  position: absolute;
  top: 16px;
  right: 16px;
}
</style>
