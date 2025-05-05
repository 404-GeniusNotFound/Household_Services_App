<template>
  <div class="search-bar">
    <div class="search-container">
      <select v-model="searchType" class="search-dropdown">
        <option value="services">Services</option>
        <option value="service_requests">Service Requests</option>
      </select>

      <input
        type="text"
        v-model="searchQuery"
        placeholder="Enter search text"
        class="search-input"
      />
      <button @click="handleSearch" class="search-button">Search</button>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      searchQuery: "",
      searchType: "services",
    };
  },
  methods: {
    handleSearch() {
      this.$emit("on-search", {
        searchQuery: this.searchQuery,
        searchType: this.searchType,
      });
    },
  },
};
</script>

<style scoped>
.search-bar {
  display: flex;
  justify-content: flex-start; /* Aligns the search bar to the left */
  padding: 20px 0;
  background-color: #f8f9fa;
  border-radius: 8px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
}

.search-container {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 10px;
  background-color: #fff;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  margin-left: 20px; /* Adds a bit of space from the left edge */
}

.search-dropdown {
  padding: 8px 12px;
  font-size: 1em;
  border-radius: 4px;
  border: 1px solid #ddd;
  outline: none;
}

.search-input {
  padding: 8px 12px;
  font-size: 1em;
  border-radius: 4px;
  border: 1px solid #ddd;
  outline: none;
  width: 250px;
}

.search-button {
  padding: 8px 16px;
  font-size: 1em;
  border-radius: 4px;
  border: none;
  background-color: #007bff;
  color: white;
  cursor: pointer;
  transition: background-color 0.3s;
}

.search-button:hover {
  background-color: #0056b3;
}
</style>
