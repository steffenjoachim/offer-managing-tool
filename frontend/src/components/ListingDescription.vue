<div class="listing-description">
  <h3 class="title">Description</h3>
  <p class="content">{{ description }}</p>
</div>

<script setup>
const props = defineProps({
  description: {
    type: String,
    required: true,
  },
});
</script>
