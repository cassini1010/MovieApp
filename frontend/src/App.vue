<template>
  <div id="app">
    <nav class="navbar">
      <router-link to="/" class="nav-link">Movies</router-link>
      <router-link to="/admin" class="nav-link">Admin</router-link>
    </nav>
    <router-view />
  </div>
</template>

<style scoped>
.navbar {
  display: flex;
  justify-content: center;   /* center the links horizontally */
  gap: 2rem;                 /* spacing between links */
  background-color: #1e293b; /* dark navy */
  padding: 1rem 2rem;
  border-bottom: 2px solid #334155;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
}

.nav-link {
  color: #f1f5f9;            /* light text */
  text-decoration: none;
  font-weight: 600;
  font-size: 1.1rem;
  transition: color 0.2s ease, border-bottom 0.2s ease;
  padding-bottom: 2px;
}

.nav-link:hover {
  color: #38bdf8;            /* light blue on hover */
  border-bottom: 2px solid #38bdf8;
}

.router-link-active {
  color: #38bdf8;            /* highlight active page */
  border-bottom: 2px solid #38bdf8;
}
</style>
