<!-- src/App.vue -->
<template>
  <div id="app">
    <header class="header">
      <h1>Rural Company</h1>
    </header>
    <main>
      <router-view />
    </main>
    <footer class="footer">
      <p>&copy; 2024 ServiceApp. All rights reserved.</p>
    </footer>
  </div>
</template>

<script>
export default {
  name: "App",
};
</script>

<style lang="scss" scoped>
#app {
  display: flex;
  flex-direction: column;
  min-height: 100vh;
  font-family: "Avenir", Helvetica, Arial, sans-serif;
  color: #2c3e50;
}

.header {
  background-color: black;
  padding: 20px;
  text-align: center;
  color: #ffffff;
}

main {
  flex: 1;
  padding: 20px;
  background-color: #f9f9f9;
}

.footer {
  background-color: #f5f5f5;
  text-align: center;
  padding: 10px 0;
  font-size: 14px;
  color: #777777;
}
</style>
