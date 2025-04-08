import { createRouter, createWebHistory } from "vue-router";
import Home from "../views/Home.vue";
import Login from "../views/Login.vue";
import store from "../store";

const routes = [
  {
    path: "/",
    name: "Home",
    component: Home,
    meta: { requiresAuth: true },
  },
  {
    path: "/login",
    name: "Login",
    component: Login,
  },
  {
    path: "/customers",
    name: "Customers",
    component: () => import("../views/Customers.vue"),
    meta: { requiresAuth: true },
  },
  {
    path: "/offers",
    name: "Offers",
    component: () => import("../views/Offers.vue"),
    meta: { requiresAuth: true },
  },
  {
    path: "/templates",
    name: "Templates",
    component: () => import("../views/Templates.vue"),
    meta: { requiresAuth: true, requiresAdmin: true },
  },
];

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes,
});

// Navigation Guard
router.beforeEach((to, from, next) => {
  // Prüfen, ob die Route Authentifizierung erfordert
  if (to.matched.some((record) => record.meta.requiresAuth)) {
    // Prüfen, ob der Benutzer angemeldet ist
    if (!store.getters.isLoggedIn) {
      next({
        path: "/login",
        query: { redirect: to.fullPath },
      });
    } else {
      // Prüfen, ob die Route Admin-Rechte erfordert
      if (to.matched.some((record) => record.meta.requiresAdmin)) {
        if (!store.getters.isAdmin) {
          next({ path: "/" });
        } else {
          next();
        }
      } else {
        next();
      }
    }
  } else {
    next();
  }
});

export default router;
