<template>
  <div class="professional-layout">
    <nav class="sidebar">
      <p class="welcome-message">Welcome, {{ professionalName }}</p>
      <router-link to="/professional-dashboard" class="nav-link"
        >Home</router-link
      >
      <router-link to="/professional-search" class="nav-link"
        >Search</router-link
      >
      <router-link to="/professional-summary" class="nav-link"
        >Summary</router-link
      >
      <a href="#" @click.prevent="logout" class="nav-link logout-link"
        >Logout</a
      >
      <button @click="$emit('show-profile-modal')" class="profile-btn">
        Profile
      </button>
    </nav>
    <div class="content">
      <slot />
    </div>
  </div>
</template>

<script>
import axios from "axios";

export default {
  data() {
    return {
      professionalName:
        localStorage.getItem("professionalFullName") || "Professional",
    };
  },
  methods: {
    logout() {
      axios
        .post("http://localhost:5000/logout", {}, { withCredentials: true })
        .then(() => {
          localStorage.removeItem("professionalId");
          localStorage.removeItem("professionalFullName");
          localStorage.removeItem("role");
          this.$router.push({ name: "Login" });
        })
        .catch((error) => {
          console.error("Error logging out:", error);
          alert("An error occurred during logout.");
        });
    },
  },
};
</script>

<style scoped>
.professional-layout {
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

.profile-btn {
  margin-top: 20px;
  font-size: 16px;
  background-color: #007bff;
  color: #fff;
  padding: 10px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  width: 100%;
  text-align: left;
  transition: background-color 0.3s;
}

.profile-btn:hover {
  background-color: #0056b3;
}

.content {
  flex: 1;
  padding: 20px;
  background-color: #f5f5f5;
}
</style>
