import { createRouter, createWebHistory } from "vue-router";
import Home from "../views/Home.vue";
import Login from "../views/Login.vue";
import Register from "../views/Register.vue";
import CreateListing from "../views/CreateListing.vue";
import Messages from "../views/Messages.vue";
import EditListing from "../views/EditListing.vue";
import store from "../store";

const routes = [
  {
    path: "/",
    name: "Home",
    component: Home,
  },
  {
    path: "/login",
    name: "Login",
    component: Login,
    meta: { requiresGuest: true },
  },
  {
    path: "/register",
    name: "Register",
    component: Register,
    meta: { requiresGuest: true },
  },
  {
    path: "/create-listing",
    name: "CreateListing",
    component: CreateListing,
    meta: { requiresAuth: true },
  },
  {
    path: "/my-messages",
    name: "Messages",
    component: Messages,
    meta: { requiresAuth: true },
  },
  {
    path: "/my-messages/:conversationId",
    name: "MessageThread",
    component: () =>
      import(
        /* webpackChunkName: "message-thread" */ "../views/MessageThread.vue"
      ),
    props: true,
    meta: { requiresAuth: true },
  },
  {
    path: "/my-watchlist",
    name: "Watchlist",
    component: () =>
      import(/* webpackChunkName: "watchlist" */ "../views/Watchlist.vue"),
    meta: { requiresAuth: true },
  },
  {
    path: "/my-listings",
    name: "MyListings",
    component: () =>
      import(/* webpackChunkName: "my-listings" */ "../views/MyListings.vue"),
    meta: { requiresAuth: true },
  },
  {
    path: "/listing/:id",
    name: "ListingDetail",
    component: () =>
      import(
        /* webpackChunkName: "listing-detail" */ "../views/ListingDetail.vue"
      ),
    props: true,
  },
  {
    path: "/edit-listing/:id",
    name: "EditListing",
    component: EditListing,
    props: true,
    meta: { requiresAuth: true },
  },
  {
    path: "/about",
  },
];

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes,
});

// Navigation Guards
router.beforeEach((to, from, next) => {
  const isLoggedIn = store.getters["auth/isLoggedIn"];

  if (to.matched.some((record) => record.meta.requiresAuth)) {
    if (!isLoggedIn) {
      next("/login");
    } else {
      next();
    }
  } else if (to.matched.some((record) => record.meta.requiresGuest)) {
    if (isLoggedIn) {
      next("/");
    } else {
      next();
    }
  } else {
    next();
  }
});

export default router;
