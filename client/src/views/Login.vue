<template>
  <div class="row my-5 container">
    <div class="col-md-6 offset-md-5 col-xl-6 offset-xl-5">
      <div class="card">
        <h3 class="text-center my-4">Login</h3>
        <div class="card-body">
          <div class="errors" v-if="errors.error">
            <small
              class="text-danger"
              v-for="error in errors.error"
              :key="error"
              >{{ error }}</small
            >
          </div>
          <div class="form-group">
            <input
              type="text"
              placeholder="Email"
              class="form-control"
              v-model="email"
              :class="{
                'is-invalid': errors.email,
                'is-valid': submitted && !errors.email
              }"
            />
            <div class="errors" v-if="errors.email">
              <small
                class="text-danger"
                v-for="error in errors.email"
                :key="error"
                >{{ error }}</small
              >
            </div>
          </div>
          <div class="form-group">
            <input
              type="password"
              placeholder="Password"
              class="form-control"
              v-model="password"
              :class="{
                'is-invalid': errors.password,
                'is-valid': submitted && !errors.password
              }"
            />
            <div class="errors" v-if="errors.password">
              <small
                class="text-danger"
                v-for="error in errors.password"
                :key="error"
                >{{ error }}</small
              >
            </div>
          </div>
          <div class="form-group text-center">
            <button
              class="btn btn-success form-control"
              @click="loginUser"
              :disabled="loading"
            >
              <i class="fas fa-spin fa-spinner" v-if="loading"></i>
              {{ loading ? "" : "Login" }}
            </button>
          </div>
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
      return next({ path: "/" });
    }
    next();
  },
  data() {
    return {
      email: "",
      password: "",
      errors: {},
      submitted: false,
      loading: false
    };
  },
  methods: {
    async loginUser() {
      try {
        this.loading = true;
        const { data } = await Axios.post(
          `${process.env.VUE_APP_API_URL}/api/user/token/`,
          {
            email: this.email,
            password: this.password
          }
        );
        localStorage.setItem("token", JSON.stringify(data.token));
        this.$root.authToken = data.token;
        this.getUserDetails(data.token);
        this.submitted = true;
        this.loading = false;
        this.$noty.success("Login Successful");
      } catch (error) {
        this.errors = error.response.data.errors;
        this.loading = false;
        this.$noty.error("Oops Something went wrong");
      }
    },
    async getUserDetails(token) {
      try {
        const { data } = await Axios.get(
          `${process.env.VUE_APP_API_URL}/api/user/me/`,
          { headers: { Authorization: `Token ${token}` } }
        );
        localStorage.setItem("user", JSON.stringify(data));
        this.$root.user = data;
        this.$router.push("/favorites");
      } catch (error) {
        this.loading = false;
        this.errors = error.response.data.errors;
        this.$noty.error("Oops Something went wrong");
      }
    }
  }
};
</script>
