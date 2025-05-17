<template>
  <el-card class="base-card" :class="customClass">
    <template #header v-if="$slots.header">
      <div class="card-header">
        <slot name="header"></slot>
      </div>
    </template>
    <slot></slot>
  </el-card>
</template>

<script>
export default {
  name: "BaseCard",
  props: {
    customClass: {
      type: String,
      default: "",
    },
  },
};
</script>

<style scoped>
.base-card {
  margin-bottom: 1rem;
}

.card-header {
  display: flex;
  align-items: center;
  gap: 8px;
}
</style>
