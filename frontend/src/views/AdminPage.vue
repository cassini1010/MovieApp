<template>
  <div class="p-6">
    <h2 class="text-2xl font-bold mb-4">Admin Panel</h2>

    <!-- Add Movie Form -->
    <form @submit.prevent="addMovie" class="admin-form">
      <!-- Title -->
      <div>
        <label class="form-label">Title</label>
        <input v-model="newMovie.title" placeholder="Title" class="form-input" />
      </div>

      <!-- Director -->
      <div>
        <label class="form-label">Director</label>
        <input v-model="newMovie.director" placeholder="Director" class="form-input" />
      </div>

      <!-- Release Year -->
      <div>
        <label class="form-label">Release Year</label>
        <input v-model.number="newMovie.releaseYear" type="number" placeholder="Release Year" class="form-input" />
      </div>

      <!-- Actors -->
      <div>
        <label class="form-label">Actors (comma separated)</label>
        <input v-model="actorsInput" placeholder="e.g. Tom Hanks, Meryl Streep" class="form-input" />
      </div>

      <!-- Genres -->
      <div>
        <label class="form-label">Genres (comma separated)</label>
        <input v-model="genresInput" placeholder="e.g. Comedy, Drama" class="form-input" />
      </div>

      <!-- Summary -->
      <div>
        <label class="form-label">Summary</label>
        <textarea v-model="newMovie.summary" placeholder="Summary" class="form-textarea"></textarea>
      </div>

      <!-- Thumbnail -->
      <div>
        <label class="form-label">Thumbnail</label>
        <input type="file" @change="onFileChange" class="form-file" />
      </div>

      <!-- Submit -->
      <div class="flex justify-end">
        <button type="submit" class="btn-primary">Add Movie</button>
      </div>
    </form>



    <!-- Movies List with Delete -->
    <h3 class="text-xl font-semibold mb-2">Existing Movies</h3>
    <table class="min-w-full border">
      <thead>
        <tr class="bg-gray-200">
          <th class="p-2 border">Thumbnail</th>
          <th class="p-2 border">Title</th>
          <!-- <th class="p-2 border">Year</th> -->
          <th class="p-2 border">Actions</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="movie in movies" :key="movie.id" class="border-b">
          <td class="p-2 border">
            <img :src="`http://localhost:8000/static/${movie.thumbnail}`" alt="Thumbnail"
              class="w-16 h-16 object-cover" style="width: 300px; height: auto; border-radius: 8px;" />
          </td>
          <td class="p-2 border">{{ movie.title }}</td>
          <td class="p-2 border">
            <button @click="deleteMovie(movie.id)" class="bg-red-600 text-white px-3 py-1 rounded">
              Delete
            </button>
          </td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script>
import axios from "axios";

export default {
  data() {
    return {
      movies: [],
      newMovie: {
        title: "",
        director: "",
        releaseYear: "",
        actors: [],
        genres: [],
        summary: ""
      },
      thumbnailFile: null,
    };
  },
  mounted() {
    this.fetchMovies();
  },
  methods: {
    async fetchMovies() {
      const response = await axios.get("http://localhost:8000/movie");
      this.movies = response.data;
    },
    onFileChange(event) {
      this.thumbnailFile = event.target.files[0];
    },
    async addMovie() {
      this.newMovie.actors = this.actorsInput.split(",").map(a => a.trim()).filter(a => a);
      this.newMovie.genres = this.genresInput.split(",").map(g => g.trim()).filter(g => g);


      const formData = new FormData();
      formData.append("title", this.newMovie.title);
      formData.append("director", this.newMovie.director);
      formData.append("releaseYear", this.newMovie.releaseYear);
      formData.append("actors", this.newMovie.actors);
      formData.append("genres", this.newMovie.genres);
      formData.append("summary", this.newMovie.summary);
      if (this.thumbnailFile) {
        formData.append("thumbnail", this.thumbnailFile);
      }

      await axios.post("http://localhost:8000/movie", formData, {
        headers: { "Content-Type": "multipart/form-data" },
      });

      this.newMovie = { title: "", release_year: "" };
      this.thumbnailFile = null;
      this.fetchMovies(); // refresh list
    },
    async deleteMovie(id) {
      await axios.delete(`http://localhost:8000/movie/${id}`);
      this.fetchMovies();
    },
  },
};
</script>

<style scoped>
/* Admin container */
.p-6 {
  background: #f9fafb;
  min-height: 100vh;
  font-family: 'Inter', system-ui, sans-serif;
}

/* Form styling */
form {
  background: #ffffff;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
  transition: transform 0.2s ease, box-shadow 0.2s ease;
}

form:hover {
  transform: translateY(-1px);
  box-shadow: 0 6px 16px rgba(0, 0, 0, 0.08);
}

/* Inputs */
input[type="text"],
input[type="number"],
input[type="file"] {
  border-radius: 8px;
  border: 1px solid #d1d5db;
  transition: border 0.2s ease, box-shadow 0.2s ease;
}

input:focus {
  outline: none;
  border-color: #3b82f6;
  box-shadow: 0 0 0 2px rgba(59, 130, 246, 0.3);
}

/* Buttons */
button {
  font-weight: 600;
  transition: background 0.2s ease, transform 0.1s ease;
}

button:hover {
  filter: brightness(0.95);
}

button:active {
  transform: scale(0.97);
}

/* Table */
table {
  background: #fff;
  border-radius: 8px;
  overflow: hidden;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.05);
}

thead {
  background: #e5e7eb;
}

th {
  font-weight: 600;
  text-transform: uppercase;
  font-size: 0.85rem;
  color: #374151;
}

tbody tr:hover {
  background: #f3f4f6;
}

/* Thumbnail image */
img {
  border-radius: 6px;
  box-shadow: 0 2px 6px rgba(0, 0, 0, 0.1);
}

.admin-form {
  display: grid;
  gap: 16px;
  background: #ffffff;
  padding: 20px;
  border-radius: 12px;
  box-shadow: 0 6px 14px rgba(0, 0, 0, 0.06);
  max-width: 600px;
  margin: 0 auto 2rem auto;
}

.form-label {
  display: block;
  font-weight: 600;
  margin-bottom: 6px;
  font-size: 0.95rem;
  color: #1f2937;
  /* slate-800 */
}

.form-input,
.form-textarea,
.form-file {
  width: 100%;
  padding: 10px 12px;
  border-radius: 8px;
  border: 1px solid #d1d5db;
  font-size: 0.95rem;
  background: #f9fafb;
  transition: border-color 0.2s ease, box-shadow 0.2s ease;
}

.form-input:focus,
.form-textarea:focus,
.form-file:focus {
  outline: none;
  border-color: #3b82f6;
  /* blue-500 */
  box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.25);
  background: #fff;
}

.form-textarea {
  resize: vertical;
  min-height: 100px;
}

.btn-primary {
  background: linear-gradient(180deg, #3b82f6, #2563eb);
  color: #fff;
  font-weight: 600;
  padding: 10px 18px;
  border-radius: 8px;
  border: none;
  cursor: pointer;
  transition: background 0.2s ease, transform 0.1s ease;
}

.btn-primary:hover {
  filter: brightness(1.05);
}

.btn-primary:active {
  transform: scale(0.98);
}
</style>
