<div class="listing-card">
  <img
    v-if="listing.images && listing.images.length > 0"
    :src="listing.images[0].image"
    :alt="listing.title"
    class="listing-image"
  />
  <div class="listing-info">
    <h3 class="listing-title">{{ listing.title }}</h3>
    <p class="listing-price">€{{ listing.price }}</p>
    <p class="listing-description">{{ listing.description }}</p>
    <p class="listing-category">{{ listing.category }}</p>
    <p class="listing-date">
      Created: {{ formatDate(listing.created_at) }}
    </p>
  </div>
</div> 