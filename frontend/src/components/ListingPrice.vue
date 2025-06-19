<div class="listing-price">
  <h3 class="title">Price</h3>
  <p class="amount">€{{ price }}</p>
</div>

<script setup>
const props = defineProps({
  price: {
    type: Number,
    required: true,
  },
});
</script>
