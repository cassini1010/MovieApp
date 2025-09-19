<template>
  <!-- <nav>
    <router-link to="/">Home</router-link>
  </nav> -->
  <div id="app">
    <h1>Movie</h1>

  <!-- Filters -->
    <div class="filters">
      <input v-model="filters.genre" placeholder="Genre" />
      <input v-model="filters.actor" placeholder="Actor" />
      <input v-model="filters.director" placeholder="Director" />
      <input v-model="filters.year" type="number" placeholder="Year" />
      <button @click="fetchMovies">Apply Filters</button>
      <button @click="clearFilters">Clear</button>
    </div>



  <table class="movie-table">
  <thead>
    <tr>
      <th>Title</th>
      <th>Release Year</th>
      <th>Summary</th>
      <th>Director</th>
      <th>Actors</th>
      <th>Genres</th>
    </tr>
  </thead>
  <tbody>
    <tr v-for="movie in movies" :key="movie.id">
      <td>{{ movie.title }}</td>
      <td>{{ movie.releaseYear }}</td>
      <td>{{ movie.summary }}</td>
      <td>{{ movie.director?.name || 'N/A' }}</td>
      <td>{{ movie.actors.map(a => a.name).join(", ") }}</td>
      <td>{{ movie.genres.map(g => g.genre_type).join(", ") }}</td>
    </tr>
  </tbody>
</table>

<!-- <vue-awesome-paginate
    :total-items="50"
    :items-per-page="5"
    :max-pages-shown="5"
    v-model="currentPage"
    @click="onClickHandler"
  /> -->



  </div>
  <router-view/>
</template>


<script>

import axios from "axios";
// import { ref } from "vue";

// const onClickHandler = (page: number) => {
//     console.log(page);
//   };

// const currentPage = ref(1);

export default {
  name: 'App',
  data() {
    return {
      movies: [],
      filters: {
        genre: "",
        actor: "",
        director: "",
        year: ""
      }
    };
  },
  methods: {
    async fetchMovies() {
      try {
        // Only send params that have values
        const params = {};
        if (this.filters.genre) params.genre = this.filters.genre;
        if (this.filters.actor) params.actor = this.filters.actor;
        if (this.filters.director) params.director = this.filters.director;
        if (this.filters.year) params.year = Number(this.filters.year);

        const response = await axios.get(`http://localhost:8000/movie`, { params });
        console.log("Movies API response:", response.data);
        this.movies = response.data;
      } catch (error) {
        console.error("Error fetching movies:", error);
      }
    },
    clearFilters() {
      this.filters = { genre: "", actor: "", director: "", year: "" };
      this.fetchMovies(); // reload all movies
    },
  },
  mounted() {
    this.fetchMovies(); // Load movies on startup
    }
}
</script>


<style lang="scss">
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
