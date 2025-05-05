// src/router/index.js
import { createRouter, createWebHistory } from "vue-router";
import LoginPage from "../components/LoginPage.vue";
import AdminDashboard from "../components/AdminDashboard.vue";
import ProfessionalDashboard from "../components/ProfessionalDashboard.vue";
import CustomerDashboard from "../components/CustomerDashboard.vue";
import CustomerSearch from "../components/CustomerSearch.vue";
import CustomerSignup from "../components/CustomerSignup.vue";
import ProfessionalSignup from "../components/ProfessionalSignup.vue";
import AdminSearch from "../components/AdminSearch.vue";
import ProfessionalSearch from "../components/ProfessionalSearch.vue";

// New imports for summary components
import AdminSummary from "../components/AdminSummary.vue";
import ProfessionalSummary from "../components/ProfessionalSummary.vue";
import CustomerSummary from "../components/CustomerSummary.vue";

const routes = [
  {
    path: "/",
    name: "Login",
    component: LoginPage,
  },
  {
    path: "/admin-dashboard",
    name: "AdminDashboard",
    component: AdminDashboard,
    meta: { requiresAuth: true, role: "admin" },
  },
  {
    path: "/search",
    name: "Search",
    component: AdminSearch, // Use AdminSearch.vue here
  },
  {
    path: "/professional-dashboard",
    name: "ProfessionalDashboard",
    component: ProfessionalDashboard,
    meta: { requiresAuth: true, role: "professional" },
  },
  {
    path: "/professional-search",
    name: "ProfessionalSearch",
    component: ProfessionalSearch, // Route for professional search page
    meta: { requiresAuth: true, role: "professional" },
  },
  {
    path: "/customer-dashboard",
    name: "CustomerDashboard",
    component: CustomerDashboard,
    meta: { requiresAuth: true, role: "customer" },
  },
  {
    path: "/customer/search",
    name: "CustomerSearch",
    component: CustomerSearch, // Ensure this path matches
    meta: { requiresAuth: true, role: "customer" },
  },
  {
    path: "/customer_signup",
    name: "CustomerSignup",
    component: CustomerSignup,
  },
  {
    path: "/professional_signup",
    name: "ProfessionalSignup",
    component: ProfessionalSignup,
  },
  // New routes for summary pages
  {
    path: "/admin-summary",
    name: "AdminSummary",
    component: AdminSummary,
    meta: { requiresAuth: true, role: "admin" },
  },
  {
    path: "/professional-summary",
    name: "ProfessionalSummary",
    component: ProfessionalSummary,
    meta: { requiresAuth: true, role: "professional" },
  },
  {
    path: "/customer-summary",
    name: "CustomerSummary",
    component: CustomerSummary,
    meta: { requiresAuth: true, role: "customer" },
  },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

router.beforeEach((to, from, next) => {
  const userRole = localStorage.getItem("role"); // Adjust to your auth method

  // Check if the route requires authentication
  if (to.meta.requiresAuth) {
    // If user is not logged in, redirect to the login page
    if (!userRole) {
      return next({ name: "Login" });
    }
    // If user is logged in but doesn't have the required role, redirect to login
    if (to.meta.role && to.meta.role !== userRole) {
      return next({ name: "Login" });
    }
  }

  // Proceed to the requested route
  next();
});

export default router;
