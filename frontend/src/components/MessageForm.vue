<template>
  <div class="message-form">
    <h3>Send Message</h3>
    <textarea v-model="messageContent" placeholder="Your message..."></textarea>
    <button @click="sendMessage">Send</button>
  </div>
</template>

<script>
export default {
  name: "MessageForm",
  props: {
    recipient: {
      type: String,
      required: true,
    },
  },
  data() {
    return {
      messageContent: "",
    };
  },
  methods: {
    sendMessage() {
      if (this.messageContent.trim()) {
        this.$emit("message-sent", {
          content: this.messageContent.trim(),
        });
        this.messageContent = "";
      }
    },
  },
};
</script>

<style scoped>
.message-form {
  margin: 20px;
  padding: 15px;
  border: 1px solid #ccc;
  border-radius: 5px;
}

textarea {
  width: 100%;
  height: 100px;
  margin-bottom: 10px;
  padding: 8px;
  border: 1px solid #ddd;
  border-radius: 4px;
}

button {
  background-color: #4caf50;
  color: white;
  padding: 10px 15px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

button:hover {
  background-color: #45a049;
}
</style>
