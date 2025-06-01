<template>
  <div class="messages-container">
    <el-card class="messages-card">
      <template #header>
        <div class="card-header">
          <el-icon><Message /></el-icon>
          <span>My Messages</span>
        </div>
      </template>

      <div v-if="loading" class="loading-container">
        <el-skeleton :rows="3" animated />
      </div>

      <div v-else-if="error" class="error-container">
        <el-alert :title="error" type="error" :closable="false" show-icon />
      </div>

      <div v-else-if="conversations.length === 0" class="no-messages">
        <el-empty
          description="No Messages so far, start interacting with the community!"
        >
          <!-- Removed button as requested -->
          <!-- <el-button type="primary" @click="navigateToCommunity">
            Zur Community
          </el-button> -->
        </el-empty>
      </div>

      <div v-else class="conversations-list">
        <el-scrollbar height="calc(100vh - 200px)">
          <div
            v-for="conversation in conversations"
            :key="conversation.id"
            class="conversation-item"
            :class="{ unread: !conversation.isRead }"
            @click="openConversation(conversation.id)"
          >
            <div class="conversation-header">
              <span class="participant">{{
                getOtherParticipantUsername(conversation)
              }}</span>
              <span class="timestamp">{{
                formatDate(
                  conversation.last_message
                    ? conversation.last_message.timestamp
                    : null
                )
              }}</span>
            </div>
            <div class="last-message">
              {{
                conversation.last_message ? conversation.last_message.text : ""
              }}
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
    const conversations = computed(
      () => store.getters["messages/allConversations"]
    );
    const currentUser = computed(() => store.getters["auth/currentUser"]);
    const isLoggedIn = computed(() => store.getters["auth/isLoggedIn"]);

    const fetchConversations = async () => {
      try {
        await store.dispatch("messages/fetchConversations");
        console.log("Geladene Konversationen:", conversations.value);
      } catch (error) {
        console.error("Fehler beim Laden der Konversationen:", error);
      }
    };

    const formatDate = (date) => {
      console.log("Incoming date string:", date); // Log the incoming date string
      if (!date) return ""; // Handle null or undefined dates

      const timestamp = Date.parse(date);

      if (isNaN(timestamp)) {
        console.error("Failed to parse date string:", date);
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
      console.log("Conversation data for participant check:", conversation); // Log conversation data
      console.log(
        "Current user data for participant check:",
        currentUser.value
      ); // Log current user data
      if (!currentUser.value || !conversation.participants) return "";

      const otherParticipant = conversation.participants.find(
        (participant) => participant.id !== currentUser.value.id
      );
      console.log("Other participant found:", otherParticipant); // Log found participant

      return otherParticipant
        ? otherParticipant.username
        : "Unknown Participant";
    };

    const openConversation = async (conversationId) => {
      try {
        await store.dispatch("messages/markAsRead", conversationId);
        ElMessage.success("Nachricht als gelesen markiert."); // Add success message
        // TODO: Implement navigation to conversation detail view
        console.log("Öffne Konversation:", conversationId);
        // After marking as read, potentially refetch conversations to update the list state
        // Adding a small delay to allow backend processing before refetching
        setTimeout(() => {
          fetchConversations();
        }, 250);
      } catch (error) {
        console.error("Fehler beim Öffnen der Konversation:", error);
        ElMessage.error("Fehler beim Markieren als gelesen."); // Add error message
      }
    };

    onMounted(() => {
      fetchConversations();
    });

    watch(currentUser, (newUser, oldUser) => {
      if (newUser && !oldUser) {
        console.log("currentUser is now available, fetching conversations...");
        fetchConversations();
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
  border-bottom: 1px solid #ebeef5;
  cursor: pointer;
  position: relative;
  transition: background-color 0.3s;
}

.conversation-item:hover {
  background-color: #f5f7fa;
}

.conversation-item.unread {
  background-color: #f0f9ff;
  font-weight: bold;
}

.conversation-header {
  display: flex;
  justify-content: space-between;
  margin-bottom: 8px;
}

.participant {
  font-weight: bold;
}

.timestamp {
  color: #909399;
  font-size: 0.9em;
}

.last-message {
  color: #606266;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.unread-badge {
  position: absolute;
  top: 16px;
  right: 16px;
}
</style>
