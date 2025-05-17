import { createRouter, createWebHistory } from "vue-router";
import store from "@/store";

const routes = [
  {
    path: "/",
    name: "Home",
    component: () => import("@/core/Home.vue"),
    meta: { requiresAuth: true },
  },
  {
    path: "/login",
    name: "Login",
    component: () => import("@/store/views/Login.vue"),
    meta: { requiresAuth: false },
  },
  {
    path: "/customers",
    name: "Customers",
    component: () => import("@/store/views/Customers.vue"),
    meta: { requiresAuth: true },
  },
  {
    path: "/offers",
    name: "Offers",
    component: () => import("@/store/views/Offers.vue"),
    meta: { requiresAuth: true },
  },
  {
    path: "/templates",
    name: "Templates",
    component: () => import("@/store/views/Templates.vue"),
    meta: { requiresAuth: true, requiresAdmin: true },
  },
];

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes,
});

// Navigation Guards
router.beforeEach((to, from, next) => {
  const isLoggedIn = store.getters["auth/isLoggedIn"];
  const isAdmin = store.getters["auth/isAdmin"];

  // Wenn die Route Auth erfordert und der Benutzer nicht eingeloggt ist
  if (to.meta.requiresAuth && !isLoggedIn) {
    next("/login");
  }
  // Wenn die Route Admin-Rechte erfordert und der Benutzer kein Admin ist
  else if (to.meta.requiresAdmin && !isAdmin) {
    next("/");
  }
  // Wenn der Benutzer eingeloggt ist und versucht, zur Login-Seite zu gehen
  else if (to.path === "/login" && isLoggedIn) {
    next("/");
  }
  // In allen anderen Fällen erlauben
  else {
    next();
  }
});

export default router;
