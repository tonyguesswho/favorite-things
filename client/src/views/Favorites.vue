<template>
  <div>
    <div class="d-flex justify-content-end container my-4" v-if="!loading">
      <button class="btn btn-outline-success btn-sm mr-auto" @click="getAll">
        View All
      </button>
      <p class="mr-3 mt-2">Filter By</p>
      <select class="mr-4" v-model="categoryId">
        <option value="select">Select a Category</option>
        <option
          :value="category.id"
          v-for="category in categories"
          :key="category.id"
        >
          {{ category.name }}
        </option>
      </select>
      <button
        class="btn btn-outline-success btn-sm mr-3"
        @click="getFavoriteThings()"
      >
        Apply
      </button>
    </div>
    <div class="row" v-if="!loading && favoriteThings.favorites.length > 0">
      <div
        class="col-md-8 offset-md-2"
        v-for="(favorite, index) in favoriteThings.favorites"
        :key="favorite.id"
      >
        <FavoriteThing
          :favorite="favorite"
          @delete="handleDelete(index, favorite.id)"
          @edit="handleEdit(favorite.id)"
        />
      </div>
    </div>
    <div class="loader text-center">
      <i class="fas fa-spin fa-5x fa-spinner" v-if="loading"></i>
    </div>
    <div
      class="text-center"
      v-if="!loading && favoriteThings.favorites.length < 1"
    >
      <p class="my-4">No Data Available</p>
      <router-link to="/favorites/create">
        <button type="button" class="btn  btn-outline-info">
          Add Favorite
        </button>
      </router-link>
    </div>
    <div
      class="d-flex justify-content-between container mb-4 "
      v-if="!loading && favoriteThings.favorites.length > 0"
    >
      <button
        @click="getPrev"
        class="btn btn-info"
        :disabled="favoriteThings.links.previous === null"
      >
        Prev Page
      </button>
      <button
        @click="getNext"
        class="btn btn-info"
        :disabled="favoriteThings.links.next === null"
      >
        Next Page
      </button>
    </div>
  </div>
</template>

<script>
import Axios from "axios";
import FavoriteThing from "@/components/FavoriteThing.vue";
export default {
  components: {
    FavoriteThing
  },
  beforeRouteEnter(to, from, next) {
    if (localStorage.getItem("token")) {
      return next();
    } else {
      return next({ path: "/login" });
    }
  },

  mounted() {
    this.getFavoriteThings();
    this.getCategories();
  },

  data() {
    return {
      errors: {},
      favoriteThings: {},
      loading: true,
      categoryId: "select",
      categories: {}
    };
  },

  methods: {
    async getFavoriteThings(
      url = `${process.env.VUE_APP_API_URL}/api/favorite/favorites/`
    ) {
      if (this.categoryId !== "select") {
        url = `${
          process.env.VUE_APP_API_URL
        }/api/favorite/favorites/?category_id=${this.categoryId}`;
      }
      try {
        this.loading = true;
        const response = await Axios.get(url, {
          headers: { Authorization: `Token ${this.$root.authToken}` }
        });
        this.loading = false;
        this.favoriteThings = response.data;
      } catch (error) {
        this.errors = error.response.data;
      }
    },
    async getNext() {
      await this.getFavoriteThings(this.favoriteThings.links.next);
    },
    async getPrev() {
      await this.getFavoriteThings(this.favoriteThings.links.previous);
    },
    async getAll() {
      this.categoryId = "select";
      await this.getFavoriteThings();
    },
    async getCategories() {
      try {
        const response = await Axios.get(
          `${process.env.VUE_APP_API_URL}/api/category/categories/`,
          { headers: { Authorization: `Token ${this.$root.authToken}` } }
        );
        this.categories = response.data;
      } catch (error) {
        this.$noty.error("An error occurred");
      }
    },
    async handleDelete(index, id) {
      this.$delete(this.favoriteThings.favorites, index);
      try {
        await Axios.delete(
          `${process.env.VUE_APP_API_URL}/api/favorite/favorites/${id}/`,
          { headers: { Authorization: `Token ${this.$root.authToken}` } }
        );
        await this.getFavoriteThings();
        this.$noty.success("Successfully deleted favorite");
      } catch (error) {
        this.$noty.error("Error occured");
      }
    }
  }
};
</script>

<style scoped>
.btn-warning {
  color: #ffffff;
}
</style>
