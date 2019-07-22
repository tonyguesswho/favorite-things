<template>
  <div>
    <div class="row container my-4">
      <div class="col-md-9 offset-md-3">
        <div
          class="card my-3 text-center"
          v-for="log in logs"
          :key="log.history_id"
        >
          <p class="card-header">
            {{ new Date(log.history_date).toUTCString() }} - Favorite thing with
            title {{ log.title }} was {{ getType(log.history_type) }}
          </p>
        </div>
      </div>
    </div>
    <div class="loader text-center">
      <i class="fas fa-spin fa-5x fa-spinner" v-if="loading"></i>
    </div>
    <div class="text-center" v-if="!loading && logs.length < 1">
      <p class="my-4">No Data Available</p>
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
    this.getLogs();
  },

  data() {
    return {
      errors: {},
      logs: [],
      loading: true
    };
  },

  methods: {
    async getLogs(
      url = `${process.env.VUE_APP_API_URL}/api/favorite/history/`
    ) {
      try {
        this.loading = true;
        const response = await Axios.get(url, {
          headers: { Authorization: `Token ${this.$root.authToken}` }
        });
        this.loading = false;
        this.logs = response.data;
      } catch (error) {
        this.errors = error.response.data.errors;
      }
    },
    getType(action) {
      if (action == "+") {
        return "Created";
      } else if (action == "-") {
        return "Deleted";
      } else {
        return "Updated";
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
