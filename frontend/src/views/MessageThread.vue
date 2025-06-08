<template>
  <div class="message-thread-container">
    <el-card class="message-thread-card">
      <template #header>
        <div class="card-header">
          <el-button @click="goBack" icon="el-icon-back" circle></el-button>
          <span>{{ listingTitle }}</span>
        </div>
      </template>

      <div v-if="loading" class="loading-container">
        <el-skeleton :rows="5" animated />
      </div>

      <div v-else-if="error" class="error-container">
        <el-alert :title="error" type="error" :closable="false" show-icon />
      </div>

      <div v-else-if="messages.length === 0" class="no-messages">
        <el-empty
          description="Keine Nachrichten in dieser Konversation."
        ></el-empty>
      </div>

      <div v-else class="messages-list">
        <div
          v-for="message in messages"
          :key="message.id"
          :class="[
            'message-item',
            message.sender.id === currentUserId ? 'sent' : 'received',
          ]"
        >
          <div class="message-content">
            <p class="message-sender">{{ message.sender.username }}</p>
            <p class="message-text">{{ message.text }}</p>
            <span class="message-timestamp">{{
              new Date(message.timestamp).toLocaleString()
            }}</span>
          </div>
        </div>
      </div>

      <div class="message-input-area">
        <el-input
          v-model="newMessageContent"
          placeholder="Ihre Nachricht..."
          @keyup.enter="sendMessage"
        ></el-input>
        <el-button type="primary" @click="sendMessage">Senden</el-button>
      </div>
    </el-card>
  </div>
</template>

<script>
import { ref, onMounted, computed, watch, nextTick } from "vue";
import { useRoute, useRouter } from "vue-router";
import { useStore } from "vuex";
import { ElMessage } from "element-plus";
import { ArrowLeft } from "@element-plus/icons-vue"; // Importiere den Icon

export default {
  name: "MessageThread",
  components: {
    ArrowLeft, // Registriere den Icon als Komponente
  },
  props: {
    conversationId: {
      type: String,
      required: true,
    },
  },
  setup(props) {
    const route = useRoute();
    const router = useRouter();
    const store = useStore();

    const conversation = computed(
      () => store.getters["messages/currentConversation"]
    );
    const messages = computed(() => conversation.value?.messages || []);
    const listingTitle = computed(
      () => conversation.value?.listing?.title || "Konversation"
    );
    const loading = computed(() => store.getters["messages/isLoading"]);
    const error = computed(() => store.getters["messages/errorMessage"]);
    const newMessageContent = ref("");

    const currentUserId = computed(() => store.getters["auth/currentUser"]?.id);

    const fetchCurrentConversation = async () => {
      try {
        await store.dispatch(
          "messages/fetchConversation",
          props.conversationId
        );
      } catch (err) {
        ElMessage.error("Fehler beim Laden der Konversation.");
        console.error("Error fetching conversation:", err);
      }
    };

    const sendMessage = async () => {
      if (!newMessageContent.value.trim()) {
        ElMessage.warning("Nachricht kann nicht leer sein.");
        return;
      }

      try {
        await store.dispatch("messages/sendMessage", {
          conversationId: props.conversationId,
          message: newMessageContent.value.trim(),
        });
        newMessageContent.value = "";
        // Nach dem Senden erneut die Konversation laden, um die neue Nachricht anzuzeigen
        await fetchCurrentConversation();
      } catch (err) {
        ElMessage.error("Fehler beim Senden der Nachricht.");
        console.error("Error sending message:", err);
      }
    };

    const goBack = () => {
      router.push({ name: "Messages" });
    };

    onMounted(() => {
      fetchCurrentConversation();
    });

    // Optional: Beobachten, ob sich die Nachrichtenliste ändert, um zum Ende zu scrollen
    watch(
      messages,
      () => {
        nextTick(() => {
          const messagesList = document.querySelector(".messages-list");
          if (messagesList) {
            messagesList.scrollTop = messagesList.scrollHeight;
          }
        });
      },
      { deep: true }
    );

    return {
      messages,
      loading,
      error,
      newMessageContent,
      currentUserId,
      sendMessage,
      goBack,
      listingTitle,
    };
  },
};
</script>

<style scoped>
.message-thread-container {
  padding: 20px;
  max-width: 800px;
  margin: 0 auto;
}

.message-thread-card {
  height: calc(100vh - 120px); /* Adjust based on header/footer */
  display: flex;
  flex-direction: column;
}

.card-header {
  display: flex;
  align-items: center;
  font-size: 18px;
  font-weight: bold;
  color: #333;
}

.card-header .el-button {
  margin-right: 10px;
}

.messages-list {
  flex-grow: 1;
  overflow-y: auto;
  padding: 15px;
  background-color: #f9f9f9;
  border-radius: 4px;
  margin-bottom: 10px;
}

.message-item {
  display: flex;
  margin-bottom: 10px;
}

.message-item.sent {
  justify-content: flex-end;
}

.message-item.received {
  justify-content: flex-start;
}

.message-content {
  max-width: 70%;
  padding: 10px 15px;
  border-radius: 15px;
  line-height: 1.4;
  word-wrap: break-word;
  position: relative;
}

.message-item.sent .message-content {
  background-color: #e0f2fe; /* Light blue for sent messages */
  color: #333;
}

.message-item.received .message-content {
  background-color: #f0f0f0; /* Light gray for received messages */
  color: #333;
}

.message-sender {
  font-weight: bold;
  margin-bottom: 5px;
  font-size: 13px;
  color: #555;
}

.message-item.sent .message-sender {
  text-align: right;
}

.message-text {
  margin: 0;
  font-size: 15px;
}

.message-timestamp {
  font-size: 10px;
  color: #888;
  margin-top: 5px;
  display: block;
  text-align: right;
}

.message-input-area {
  display: flex;
  padding: 10px 15px;
  border-top: 1px solid #eee;
}

.message-input-area .el-input {
  flex-grow: 1;
  margin-right: 10px;
}

.loading-container,
.error-container,
.no-messages {
  flex-grow: 1;
  display: flex;
  align-items: center;
  justify-content: center;
}
</style>
