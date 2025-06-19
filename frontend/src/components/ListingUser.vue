<div class="listing-user">
  <el-avatar
    v-if="user.avatar"
    :src="user.avatar"
    :alt="user.username"
    class="user-avatar"
  />
  <el-avatar v-else class="user-avatar">
    {{ userInitials }}
  </el-avatar>
  <div class="user-info">
    <span class="username">{{ user.username }}</span>
    <span class="member-since">Member since {{ memberSince }}</span>
  </div>
</div>

<script setup>
import { computed } from "vue";
import { format } from "date-fns";

const props = defineProps({
  user: {
    type: Object,
    required: true,
  },
});

const userInitials = computed(() => {
  const { username } = props.user;
  return username
    .split(" ")
    .map((name) => name[0])
    .join("")
    .toUpperCase();
});

const memberSince = computed(() => {
  return format(new Date(props.user.date_joined), "MMMM yyyy");
});
</script> 