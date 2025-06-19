<div class="listing-list">
  <div v-if="loading" class="loading">
    <el-skeleton :rows="3" animated />
  </div>
  <div v-else-if="error" class="error">
    {{ error }}
  </div>
  <div v-else-if="listings.length === 0" class="empty">
    No listings found.
  </div>
  <div v-else class="listings-grid">
    <listing-card
      v-for="listing in listings"
      :key="listing.id"
      :listing="listing"
      @click="viewListing(listing.id)"
    />
  </div>
</div>

<script setup>
import { ref, onMounted } from "vue";
import { useRouter } from "vue-router";
import ListingCard from "./ListingCard.vue";
import axios from "axios";

const props = defineProps({
  endpoint: {
    type: String,
    required: true,
  },
});

const router = useRouter();
const listings = ref([]);
const loading = ref(true);
const error = ref(null);

const fetchListings = async () => {
  try {
    loading.value = true;
    error.value = null;
    const response = await axios.get(props.endpoint);
    listings.value = response.data.results.map((listing) => ({
      ...listing,
      created_at: listing.created_at || null,
      title: listing.title,
      description: listing.description,
      price: listing.price,
      category: listing.category,
      images: listing.images,
    }));
  } catch (err) {
    error.value = "Error loading listings";
    console.error("Error loading listings:", err);
  } finally {
    loading.value = false;
  }
};

const viewListing = (id) => {
  router.push(`/listing/${id}`);
};

onMounted(() => {
  fetchListings();
});
</script> 