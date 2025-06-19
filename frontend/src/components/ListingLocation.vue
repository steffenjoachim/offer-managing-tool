<div class="listing-location">
  <h3 class="title">Location</h3>
  <p class="content">{{ location }}</p>
</div>

<script setup>
const props = defineProps({
  location: {
    type: String,
    required: true,
  },
});
</script>
