<template>
  <div class="search-container">
    <select v-model="searchType" class="dropdown">
      <option value="date">Date</option>
      <option value="location">Location (Address or Pin Code)</option>
      <option value="customer_name">Customer Name</option>
    </select>
    <input
      type="text"
      v-model="searchQuery"
      placeholder="Search service requests"
      class="search-input"
    />
    <button @click="handleSearch" class="search-button">Search</button>
  </div>
</template>

<script>
export default {
  data() {
    return {
      searchQuery: "",
      searchType: "date",
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
.search-container {
  display: flex;
  gap: 10px;
  align-items: center;
  margin-bottom: 20px;
}

.dropdown {
  padding: 8px;
  font-size: 1em;
  border-radius: 4px;
  border: 1px solid #ccc;
}

.search-input {
  padding: 8px;
  font-size: 1em;
  width: 200px;
  border-radius: 4px;
  border: 1px solid #ccc;
}

.search-button {
  padding: 8px 12px;
  font-size: 1em;
  background-color: #007bff;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

.search-button:hover {
  background-color: #0056b3;
}
</style>
