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
          <div
            v-for="(conversation, index) in conversations"
            :key="conversation.id"
            class="conversation-item"
            :class="{ unread: conversation.unreadCount > 0 }"
            @click="openConversation(conversation.id)"
          >
            <div class="conversation-header">
              <div class="conversation-info-block">
                <div class="listing-title">
                  {{ conversation.listing ? conversation.listing.title : "" }}
                </div>
                <div class="sender-info">
                  {{ conversationDisplayTextsLocal[index] }}
                </div>
              </div>
              <div class="header-right">
                <span class="timestamp">
                  {{ formatDate(conversation.last_message?.timestamp || null) }}
                </span>
              </div>
            </div>
            <div class="last-message-box">
              <div
                class="last-message"
                :class="{ 'is-unread': conversation.unreadCount > 0 }"
              >
                {{
                  conversation.last_message
                    ? conversation.last_message.text ||
                      (conversation.last_message.file
                        ? "[Datei angehängt]"
                        : "")
                    : ""
                }}
              </div>
              <span
                v-if="conversation.unreadCount === 0"
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
import { ref, onMounted, computed, watch, nextTick } from "vue";
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
    const isAuthReady = computed(() => store.getters["auth/isAuthReady"]);

    const conversations = computed(() => {
      // Ensure conversations is always an array
      const allConversations = store.getters["messages/allConversations"] || [];
      return allConversations.filter(
        (conversation) => conversation.last_message
      );
    });

    const currentUser = computed(() => {
      const user = store.getters["auth/currentUser"];
      return user;
    });

    // New reactive variable to hold display texts
    const conversationDisplayTextsLocal = ref([]);

    // New computed property to calculate display texts based on conversations and currentUser
    const calculatedConversationDisplayTexts = computed(() => {
      // Check if both conversations and user are available before calculating display texts
      if (
        conversations.value &&
        conversations.value.length > 0 &&
        currentUser.value
      ) {
        const currentUserId = currentUser.value.id;
        return conversations.value.map((conversation) => {
          if (!conversation.last_message) {
            return "";
          }

          const senderId = Number(conversation.last_message.sender?.id);

          if (
            isNaN(senderId) ||
            typeof conversation.last_message.sender?.id === "undefined"
          ) {
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
      } else {
        // Return an empty array or null when conditions are not met
        return []; // Or null, depending on how you want to handle the intermediate state
      }
    });

    // Watch conversations and currentUser indirectly by watching calculatedConversationDisplayTexts
    watch(calculatedConversationDisplayTexts, (newDisplayTexts) => {
      // Update the local reactive variable with the calculated texts
      conversationDisplayTextsLocal.value = newDisplayTexts;
    });

    // Watch for authentication status and user data to trigger conversation fetch
    watch(
      [isAuthReady, currentUser],
      ([newIsAuthReady, newCurrentUser]) => {
        if (newIsAuthReady && newCurrentUser && newCurrentUser.id) {
          console.log(
            "MessagesView: Auth ready and user logged in, fetching conversations."
          );
          store.dispatch("messages/fetchConversations");
        } else if (newIsAuthReady && !newCurrentUser) {
          console.log(
            "MessagesView: Auth ready but user NOT logged in, clearing conversations."
          );
          // Auth is ready but no user is logged in, clear conversations
          store.commit("messages/SET_CONVERSATIONS", []);
        } else {
          console.log("MessagesView: Auth NOT ready yet.");
          // Auth is not ready yet, keep current state (e.g., loading spinner)
        }
      },
      { immediate: true } // Run immediately on component mount
    );

    const currentDisplayState = computed(() => {
      // 1. Priority: Loading State
      // Show loading if the message store is loading OR if auth is not ready yet
      if (loading.value || !isAuthReady.value) {
        return "loading";
      }
      // 2. Priority: Error State
      if (error.value) {
        return "error";
      }
      // 3. Priority: No Messages State
      if (conversations.value.length === 0) {
        return "no-messages";
      }
      // 4. Default: List State
      return "list";
    });

    const deleteDialogVisible = ref(false);
    const conversationToDeleteId = ref(null);

    const confirmDelete = (conversationId) => {
      conversationToDeleteId.value = conversationId;
      deleteDialogVisible.value = true;
    };

    const handleDeleteDialogClose = () => {
      deleteDialogVisible.value = false;
      conversationToDeleteId.value = null;
    };

    const deleteConversation = async () => {
      if (conversationToDeleteId.value) {
        try {
          await store.dispatch(
            "messages/deleteConversation",
            conversationToDeleteId.value
          );
          ElMessage.success("Conversation deleted successfully!");
          handleDeleteDialogClose();
        } catch (err) {
          ElMessage.error("Failed to delete conversation.");
          console.error("Error deleting conversation:", err);
        }
      }
    };

    const openConversation = (conversationId) => {
      router.push(`/my-messages/${conversationId}`);
    };

    // Format date for display
    const formatDate = (dateString) => {
      if (!dateString) return "";
      const date = new Date(dateString);
      return date.toLocaleDateString() + " " + date.toLocaleTimeString();
    };

    const navigateToCommunity = () => {
      router.push("/"); // Adjust as per your community route
    };

    return {
      currentDisplayState,
      loading,
      error,
      conversations,
      openConversation,
      deleteDialogVisible,
      confirmDelete,
      handleDeleteDialogClose,
      deleteConversation,
      formatDate,
      navigateToCommunity,
      conversationDisplayTextsLocal,
      currentUser,
    };
  },
};
</script>

<style scoped>
.messages-container {
  padding: 20px;
  max-width: 1000px;
  margin: 0 auto;
}

.messages-card {
  border-radius: 8px;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.1);
}

.card-header {
  display: flex;
  align-items: center;
  font-size: 20px;
  font-weight: bold;
  color: #333;
}

.card-header .el-icon {
  margin-right: 10px;
  font-size: 24px;
}

.loading-container,
.error-container,
.no-messages {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 200px;
}

.conversations-list {
  margin-top: 10px;
}

.conversation-item {
  padding: 15px;
  border-bottom: 1px solid #eee;
  cursor: pointer;
  transition: background-color 0.2s ease;
  position: relative;
}

.conversation-item:hover {
  background-color: #f5f5f5;
}

.conversation-item.unread {
  background-color: #e6f7ff; /* Light blue background for unread */
}

.conversation-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 5px;
}

.conversation-info-block {
  flex-grow: 1;
}

.listing-title {
  font-size: 16px;
  font-weight: bold;
  color: #333;
  margin-bottom: 3px;
}

.sender-info {
  font-size: 14px;
  color: #666;
}

.header-right {
  display: flex;
  flex-direction: column;
  align-items: flex-end;
}

.timestamp {
  font-size: 12px;
  color: #999;
  white-space: nowrap;
}

.last-message-box {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.last-message {
  flex-grow: 1;
  font-size: 14px;
  color: #555;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.last-message.is-unread {
  font-weight: bold;
}

.delete-x {
  margin-left: 10px;
  color: #999;
  font-size: 18px;
  cursor: pointer;
  line-height: 1;
  padding: 2px 5px;
  border-radius: 50%;
  transition: background-color 0.2s ease;
}

.delete-x:hover {
  background-color: #f0f0f0;
  color: #333;
}

.delete-x-inner {
  display: block;
}
</style>
