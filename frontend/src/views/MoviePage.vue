<template>
  <div id="app">
    <h1>Movie</h1>
    <!-- This is for the movie grid view -->
    <div class="movie-grid">
      <div v-for="movie in movies" :key="movie.id" class="movie-card">
        <img :src="`http://localhost:8000/static/${movie.thumbnail}`" alt="thumbnail" class="thumbnail"
          style="width: 300px; height: auto; border-radius: 8px;" />
        <div class="movie-details">
          <h3 class="title">{{ movie.title }}</h3>
          <p class="year">📅 {{ movie.releaseYear }}</p>
          <p class="director">🎬 {{ movie.director.name }}</p>
        </div>
      </div>
    </div>
    <div>
      <button @click="prevPage" style="margin-right: 10px;">Previous</button>
      <button @click="nextPage">Next</button>
    </div>
    <router-view />
  </div>
</template>


<script>

import axios from "axios";


export default {
  data() {
    return {
      movies: [],
      limit: 10,
      offset: 0
      // filters: {
      //   genre: "",
      //   actor: "",
      //   director: "",
      //   year: ""
      // }
    };
  },
  methods: {
    async fetchMovies() {
      try {
        // Only send params that have values
        // const params = {};
        // if (this.filters.genre) params.genre = this.filters.genre;
        // if (this.filters.actor) params.actor = this.filters.actor;
        // if (this.filters.director) params.director = this.filters.director;
        // if (this.filters.year) params.year = Number(this.filters.year);

        const response = await axios.get(`http://localhost:8000/movie/`, {
          params: {
            limit: this.limit,
            offset: this.offset
          }
        });
        console.log("Movies API response:", response.data);
        this.movies = response.data;
      } catch (error) {
        console.error("Error fetching movies:", error);
      }
    },
    nextPage() {
      this.offset += this.limit;
      this.fetchMovies();
    },
    prevPage() {
      this.offset = Math.max(0, this.offset - this.limit);
      this.fetchMovies();
    }
    // clearFilters() {
    //   this.filters = { genre: "", actor: "", director: "", year: "" };
    //   this.fetchMovies(); // reload all movies
    // },
  },
  mounted() {
    this.fetchMovies(); // Load movies on startup
  }
}
</script>


<style lang="scss">
.movie-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
  gap: 20px;
  padding: 20px;
}

.movie-card {
  background: #fff;
  border-radius: 12px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
  overflow: hidden;
  transition: transform 0.2s ease;
}

.movie-card:hover {
  transform: translateY(-5px);
}

.thumbnail {
  width: 100%;
  height: 300px;
  object-fit: cover;
}

.movie-details {
  padding: 10px;
  text-align: center;
}

.title {
  font-size: 1.2rem;
  font-weight: bold;
  margin: 8px 0 4px;
}

.year,
.director {
  font-size: 0.9rem;
  color: #666;
}


.pagination-container {
  display: flex;

  column-gap: 10px;
}

.paginate-buttons {
  height: 40px;

  width: 40px;

  border-radius: 20px;

  cursor: pointer;

  background-color: rgb(242, 242, 242);

  border: 1px solid rgb(217, 217, 217);

  color: black;
}

.paginate-buttons:hover {
  background-color: #d8d8d8;
}

.active-page {
  background-color: #3498db;

  border: 1px solid #3498db;

  color: white;
}

.active-page:hover {
  background-color: #2988c8;
}

.movie-table {
  width: 100%;
  border-collapse: collapse;
  margin-top: 20px;
  font-family: Arial, sans-serif;
}

.movie-table th,
.movie-table td {
  border: 1px solid #ddd;
  padding: 12px;
  text-align: left;
}

.movie-table th {
  background-color: #42b983;
  color: white;
  font-weight: bold;
}

.movie-table tr:nth-child(even) {
  background-color: #f9f9f9;
}

.movie-table tr:hover {
  background-color: #f1f1f1;
  transition: background 0.3s;
}

#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
}

nav {
  padding: 30px;

  a {
    font-weight: bold;
    color: #2c3e50;

    &.router-link-exact-active {
      color: #42b983;
    }
  }
}

button {
  padding: 10px 20px;
  font-size: 16px;
  background: #42b983;
  color: white;
  border: none;
  border-radius: 5px;
  cursor: pointer;
}

.filters {
  margin-bottom: 20px;
}

.filters input {
  margin-right: 10px;
  padding: 8px;
}

.filters button {
  margin-right: 10px;
  padding: 8px 16px;
  background: #42b983;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

.filters button:hover {
  background: #369f6b;
}
</style>
