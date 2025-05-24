<template>
  <div class="home-container">
    <h1 class="section-title">Recommended Listings for You</h1>

    <el-row :gutter="10">
      <el-col
        v-for="listing in listings"
        :key="listing.id"
        :xs="12"
        :sm="8"
        :md="6"
        :lg="4"
      >
        <el-card class="listing-card" :body-style="{ padding: '0px' }">
          <img
            :src="
              Array.isArray(listing.bilder) && listing.bilder.length > 0
                ? listing.bilder[0].bild
                : typeof listing.bilder === 'string'
                ? listing.bilder
                : '/images/placeholder-image.svg'
            "
            class="listing-image"
            @error="handleImageError"
            alt="Anzeigenbild"
          />
          <div class="listing-info">
            <h3 class="listing-title">{{ listing.titel }}</h3>
            <p class="listing-price">€{{ listing.preis }}</p>
          </div>
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>

<script>
import { ref, onMounted } from "vue";
import { useStore } from "vuex";

export default {
  name: "HomePage",
  setup() {
    const store = useStore();
    const listings = ref([]);

    const handleImageError = (e) => {
      console.error("Bild konnte nicht geladen werden:", e);
      e.target.src = "/images/placeholder-image.svg";
    };

    const fetchListings = async () => {
      try {
        const response = await store.dispatch("listings/fetchListings");
        console.log("Anzeigen geladen:", response);
        listings.value = response;
      } catch (error) {
        console.error("Fehler beim Laden der Anzeigen:", error);
      }
    };

    onMounted(() => {
      fetchListings();
    });

    return {
      listings,
      handleImageError,
    };
  },
};
</script>

<style scoped>
.home-container {
  padding: 20px;
}

.section-title {
  margin-bottom: 24px;
  font-size: 24px;
  font-weight: 600;
  color: #303133;
}

.listing-card {
  margin-bottom: 10px;
  transition: transform 0.3s;
}

.listing-card:hover {
  transform: translateY(-5px);
}

.listing-image {
  width: 100%;
  height: 200px;
  object-fit: cover;
  object-position: 50% 30%;
}

.listing-info {
  padding: 14px;
}

.listing-title {
  margin: 0;
  font-size: 16px;
  font-weight: 500;
  color: #303133;
}

.listing-price {
  margin: 8px 0 0;
  font-size: 18px;
  font-weight: 600;
  color: #409eff;
}
</style>
