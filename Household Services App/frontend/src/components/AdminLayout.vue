<template>
  <div class="admin-layout">
    <nav class="sidebar">
      <p class="welcome-message">Welcome to Admin</p>
      <router-link to="/admin-dashboard" class="nav-link">Home</router-link>
      <router-link to="/search" class="nav-link">Search</router-link>
      <router-link to="/admin-summary" class="nav-link">Summary</router-link>
      <a href="#" @click.prevent="logout" class="nav-link logout-link"
        >Logout</a
      >
    </nav>

    <div class="content">
      <slot />
    </div>
  </div>
</template>

<script>
import axios from "axios";

export default {
  methods: {
    logout() {
      axios
        .post("http://localhost:5000/logout")
        .then(() => {
          localStorage.removeItem("role");
          this.$router.push({ name: "Login" });
        })
        .catch((error) => {
          console.error("Logout error:", error);
          alert("An error occurred while logging out.");
        });
    },
  },
};
</script>

<style scoped>
.admin-layout {
  display: flex;
}

.sidebar {
  width: 200px;
  padding: 20px;
  background-color: #333;
  color: #fff;
  display: flex;
  flex-direction: column;
  align-items: flex-start;
}

.welcome-message {
  font-size: 18px;
  font-weight: 600;
  margin-bottom: 20px;
}

.nav-link {
  color: #fff;
  text-decoration: none;
  padding: 10px 0;
  font-size: 16px;
  width: 100%;
  text-align: left;
}

.nav-link:hover {
  background-color: #444;
  padding-left: 10px;
  transition: 0.3s;
}

.logout-link {
  color: #ff4d4f;
  margin-top: auto;
}

.content {
  flex: 1;
  padding: 20px;
  background-color: #f5f5f5;
}
</style>
