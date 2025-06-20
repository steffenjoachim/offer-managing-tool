<template>
  <div class="message-thread-container">
    <el-card class="message-thread-card">
      <template #header>
        <div class="card-header">
          <span>{{ listingTitle }}</span>
          <el-button
            class="close-thread-button"
            @click="goBack"
            icon="Close"
          ></el-button>
        </div>
      </template>

      <div v-if="loading" class="loading-container">
        <el-skeleton :rows="5" animated />
      </div>

      <div v-else-if="error" class="error-container">
        <el-alert :title="error" type="error" :closable="false" show-icon />
      </div>

      <div v-else-if="messages.length === 0" class="no-messages">
        <el-empty description="No Messages yet in this Conversation"></el-empty>
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
            <p class="message-text" v-if="message.content">
              {{ message.content }}
            </p>
            <div v-if="message.file" class="message-file">
              <img
                v-if="isImage(message.file)"
                :src="getFileUrl(message.file)"
                alt="Attached Image"
                class="attached-image"
                @click="showImage(message.file)"
              />
              <a
                v-else
                :href="getFileUrl(message.file)"
                target="_blank"
                class="attached-file-link"
              >
                <el-icon><Document /></el-icon> {{ getFileName(message.file) }}
              </a>
            </div>
            <span class="message-timestamp">{{
              formatDate(message.created_at)
            }}</span>
          </div>
        </div>
      </div>

      <div class="message-input-area">
        <el-input
          v-model="newMessageContent"
          placeholder="Enter Message..."
        ></el-input>
        <div class="file-input-wrapper">
          <label for="file-upload" class="file-input-label">Select File</label>
          <input
            type="file"
            id="file-upload"
            @change="handleFileChange"
            accept="image/*,application/pdf"
            ref="fileInput"
            class="file-input"
          />
          <span v-if="selectedFile" class="file-name">{{
            selectedFile.name
          }}</span>
        </div>
        <el-button type="primary" @click="sendMessage">Send</el-button>
      </div>
    </el-card>

    <el-image-viewer
      v-if="showImageViewer"
      :url-list="[currentImage]"
      @close="closeImageViewer"
    />
  </div>
</template>

<script>
import { ref, onMounted, computed, watch, nextTick } from "vue";
import { useRoute, useRouter } from "vue-router";
import { useStore } from "vuex";
import { ElMessage, ElImageViewer } from "element-plus";
import { Close, Document, Message } from "@element-plus/icons-vue";

export default {
  name: "MessageThread",
  components: {
    Close,
    Document,
    ElImageViewer,
    Message,
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
    const selectedFile = ref(null);
    const fileInput = ref(null);

    const showImageViewer = ref(false);
    const currentImage = ref("");

    const currentUserId = computed(() => store.getters["auth/currentUser"]?.id);

    const fetchCurrentConversation = async () => {
      try {
        await store.dispatch(
          "messages/fetchConversation",
          props.conversationId
        );
        await store.dispatch("messages/markAsRead", props.conversationId);
        // scrollToBottom(); // Scroll to bottom after fetching
        error.value = null;
      } catch (err) {
        ElMessage.error("Fehler beim Laden der Konversation.");
        console.error("Error fetching conversation:", err);
      }
    };

    const handleFileChange = (event) => {
      selectedFile.value = event.target.files[0];
    };

    const sendMessage = async () => {
      if (!newMessageContent.value.trim() && !selectedFile.value) {
        ElMessage.warning(
          "Nachricht kann nicht leer sein und keine Datei wurde ausgewählt."
        );
        return;
      }

      const messageData = new FormData();
      if (newMessageContent.value.trim()) {
        messageData.append("content", newMessageContent.value.trim());
      }
      if (selectedFile.value) {
        messageData.append("file", selectedFile.value);
      }

      try {
        await store.dispatch("messages/sendMessage", {
          conversationId: props.conversationId,
          messageData: messageData,
        });

        newMessageContent.value = "";
        selectedFile.value = null;
        if (fileInput.value) {
          fileInput.value.value = "";
        }

        await fetchCurrentConversation();
      } catch (err) {
        ElMessage.error("Fehler beim Senden der Nachricht.");
        console.error("Error sending message:", err);
      }
    };

    const goBack = () => {
      router.push({ name: "Messages" });
    };

    const showImage = (imageUrl) => {
      currentImage.value = imageUrl;
      showImageViewer.value = true;
    };

    const closeImageViewer = () => {
      showImageViewer.value = false;
      currentImage.value = "";
    };

    const isImage = (fileName) => {
      if (!fileName) return false;
      const imageExtensions = [
        ".jpg",
        ".jpeg",
        ".png",
        ".gif",
        ".bmp",
        ".webp",
        ".svg",
      ];
      const lowerCaseFileName = fileName.toLowerCase();
      return imageExtensions.some((ext) => lowerCaseFileName.endsWith(ext));
    };

    const getFileName = (fileUrl) => {
      if (!fileUrl) return "Datei";
      try {
        const url = new URL(fileUrl);
        const pathSegments = url.pathname.split("/");
        return pathSegments[pathSegments.length - 1];
      } catch (e) {
        return fileUrl.split("/").pop();
      }
    };

    const getFileUrl = (file) => {
      if (!file) return "";
      if (file.startsWith("http")) return file;
      // Passe ggf. die URL an, falls nur ein relativer Pfad geliefert wird
      return `http://localhost:8000${file}`;
    };

    // Format date for display
    const formatDate = (dateString) => {
      if (!dateString) return "";
      const date = new Date(dateString);
      const day = String(date.getDate()).padStart(2, "0");
      const month = String(date.getMonth() + 1).padStart(2, "0");
      const year = date.getFullYear();
      const hours = String(date.getHours()).padStart(2, "0");
      const minutes = String(date.getMinutes()).padStart(2, "0");
      return `${day}.${month}.${year} – ${hours}:${minutes} Uhr`;
    };

    // Initial fetch and scroll
    onMounted(() => {
      fetchCurrentConversation();
    });

    // Scroll to bottom when messages change
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
      selectedFile,
      fileInput,
      showImageViewer,
      currentImage,
      currentUserId,
      sendMessage,
      handleFileChange,
      goBack,
      listingTitle,
      isImage,
      getFileName,
      showImage,
      closeImageViewer,
      formatDate,
      getFileUrl,
    };
  },
};
</script>

<style scoped>
.message-thread-container {
  padding: 20px;
  max-width: 800px;
  margin: 0 auto;
  min-height: calc(100vh - 100px);
  display: flex;
  flex-direction: column;
}

.message-thread-card {
  flex-grow: 1;
  display: flex;
  flex-direction: column;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-size: 18px;
  font-weight: bold;
  color: #333;
}

.card-header span {
  flex-grow: 1;
}

.close-thread-button {
  margin-left: 10px;
  padding: 0;
  height: 25px;
  width: 25px;
  min-width: unset;
  border-radius: 50%;
  color: #f56c6c;
  border: 1px solid #f56c6c;
  background-color: transparent;
  transition: background-color 0.2s ease, color 0.2s ease;
}

.close-thread-button:hover {
  background-color: #fef0f0;
  color: #f56c6c;
}

.close-thread-button .el-icon {
  font-size: 14px;
}

.loading-container,
.error-container,
.no-messages {
  flex-grow: 1;
  display: flex;
  justify-content: center;
  align-items: center;
}

.messages-list {
  flex-grow: 1;
  overflow-y: auto;
  padding: 15px;
  background-color: #f9f9f9;
  border-radius: 4px;
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
  background-color: #e0f2fe;
  color: #333;
}

.message-item.received .message-content {
  background-color: #f0f0f0;
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
  word-break: break-word;
}

.message-timestamp {
  font-size: 10px;
  color: #888;
  margin-top: 5px;
  display: block;
  text-align: right;
}

.message-file {
  margin-top: 5px;
}

.attached-image {
  max-width: 200px;
  max-height: 150px;
  width: auto;
  height: auto;
  border-radius: 4px;
  margin-top: 5px;
  cursor: pointer;
  object-fit: contain;
}

.attached-file-link {
  display: inline-flex;
  align-items: center;
  color: #409eff;
  text-decoration: none;
  margin-top: 5px;
}

.attached-file-link:hover {
  text-decoration: underline;
}

.attached-file-link .el-icon {
  margin-right: 5px;
}

.message-input-area {
  display: flex;
  padding: 10px;
  gap: 10px;
  border-top: 1px solid #eee;
  align-items: center;
}

.el-input {
  flex-grow: 1;
}

.file-input-wrapper {
  display: flex;
  align-items: center;
  gap: 10px;
  flex-shrink: 0;
}

.file-input {
  display: none;
}

.file-input-label {
  background-color: #409eff;
  color: white;
  padding: 8px 12px;
  border-radius: 4px;
  cursor: pointer;
  font-size: 14px;
  white-space: nowrap;
  flex-shrink: 0;
}

.file-input-label:hover {
  background-color: #337ecc;
}

.file-name {
  font-size: 14px;
  color: #555;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  flex-grow: 1;
  max-width: 150px;
}
</style>
