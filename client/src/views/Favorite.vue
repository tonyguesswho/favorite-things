<template>
  <div class="container my-5">
    <div class="row">
      <div class="col-md-10 offset-md-1">
        <div class="card" v-if="!loading">
          <div class=" card-header d-flex justify-content-between">
            <span> Category: {{ favorite.category.name }} </span>
            <span class="title font-weight-bolder">
              {{
                favorite.title.charAt(0).toUpperCase() + favorite.title.slice(1)
              }}
            </span>
            <span> Rank: {{ favorite.ranking }} </span>
          </div>
          <div class="card-body">
            <div class="article-content" v-html="favorite.description"></div>
            <div class="card my-4">
              <div class="card-header text-center">
                <h5>More Information</h5>
              </div>
              <div class="card-body">
                <p>
                  Created date:
                  {{ new Date(favorite.createdDate).toDateString() }}
                </p>
                <p>
                  Modified date:
                  {{ new Date(favorite.modifiedDate).toDateString() }}
                </p>
                <div v-if="Object.keys(favorite.metadata).length > 0">
                  <p v-for="(info, key) in favorite.metadata" :key="info">
                    {{ key }}: {{ info }}
                  </p>
                </div>
              </div>
            </div>
          </div>
          <div class="d-flex justify-content-center mb-3">
            <router-link :to="`/favorite/${favorite.id}/edit`" class="link">
              <button class="btn btn-success mt-3 mr-2">Edit</button>
            </router-link>
            <button
              class="btn btn-outline-success mt-3 ml-2"
              @click="$router.go(-1)"
            >
              Back
            </button>
          </div>
        </div>
        <div class="loader text-center" v-else>
          <i class="fas fa-5x fa-spin fa-spinner"></i>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import Axios from "axios";
export default {
  beforeRouteEnter(to, from, next) {
    if (localStorage.getItem("token")) {
      return next();
    } else {
      return next({ path: "/login" });
    }
  },

  mounted() {
    this.getFavorite();
  },
  data() {
    return {
      favorite: {},
      errors: {},
      loading: true
    };
  },

  methods: {
    async getFavorite() {
      try {
        const response = await Axios.get(
          `${process.env.VUE_APP_API_URL}/api/favorite/favorites/${
            this.$route.params.id
          }/`,
          { headers: { Authorization: `Token ${this.$root.authToken}` } }
        );
        this.favorite = response.data.favorite;
        this.loading = false;
      } catch (error) {
        this.errors = error.response.data;
      }
    }
  }
};
</script>
