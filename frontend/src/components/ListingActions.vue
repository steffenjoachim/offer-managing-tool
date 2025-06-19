<div class="listing-actions">
      <el-button
        type="primary"
        size="small"
        @click="handleView"
      >
        View
      </el-button>
      <el-button
        v-if="isOwner"
        type="warning"
        size="small"
        @click="handleEdit"
      >
        Edit
      </el-button>
      <el-button
        v-if="isOwner"
        type="danger"
        size="small"
        @click="handleDelete"
      >
        Delete
      </el-button>
      <el-button
        v-if="!isOwner"
        type="success"
        size="small"
        @click="handleContact"
      >
        Contact
      </el-button>
      <el-button
        v-if="!isOwner"
        type="info"
        size="small"
        @click="handleWatchlist"
      >
        {{ isInWatchlist ? "Remove from Watchlist" : "Add to Watchlist" }}
      </el-button>
    </div>

<script setup>
import { computed } from "vue";
import { useRouter } from "vue-router";
import { useStore } from "vuex";
import { ElMessageBox } from "element-plus";

const props = defineProps({
  listing: {
    type: Object,
    required: true,
  },
  isOwner: {
    type: Boolean,
    default: false,
  },
  isInWatchlist: {
    type: Boolean,
    default: false,
  },
});

const emit = defineEmits([
  "view",
  "edit",
  "delete",
  "contact",
  "watchlist-toggle",
]);

const router = useRouter();
const store = useStore();

const handleView = () => {
  router.push(`/listing/${props.listing.id}`);
};

const handleEdit = () => {
  router.push(`/listing/${props.listing.id}/edit`);
};

const handleDelete = async () => {
  try {
    await ElMessageBox.confirm(
      "Are you sure you want to delete this listing?",
      "Warning",
      {
        confirmButtonText: "Delete",
        cancelButtonText: "Cancel",
        type: "warning",
      }
    );
    emit("delete", props.listing.id);
  } catch {
    // User cancelled the deletion
  }
};

const handleContact = () => {
  router.push(`/messages/new?listing=${props.listing.id}`);
};

const handleWatchlist = () => {
  emit("watchlist-toggle", props.listing.id);
};
</script>
