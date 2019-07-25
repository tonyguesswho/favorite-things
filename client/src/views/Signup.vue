<template>
  <div class="row my-5 container">
    <div class="col-md-6 offset-md-5 col-xl-6 offset-xl-5">
      <div class="card">
        <h3 class="text-center my-4">Signup</h3>
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
              placeholder="Name"
              class="form-control"
              v-model="name"
              :class="{
                'is-invalid': errors.name,
                'is-valid': submitted && !errors.name
              }"
            />
            <div class="errors" v-if="errors.name">
              <small
                class="text-danger"
                v-for="error in errors.name"
                :key="error"
                >{{ error }}</small
              >
            </div>
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
              @click="registerUser"
              :disabled="loading"
            >
              <i class="fas fa-spin fa-spinner" v-if="loading"></i>
              {{ loading ? "" : "Signup" }}
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
      name: "",
      email: "",
      password: "",
      errors: {},
      submitted: false,
      loading: false
    };
  },
  methods: {
    async registerUser() {
      try {
        this.loading = true;
        const { data } = await Axios.post(
          `${process.env.VUE_APP_API_URL}/api/user/create/`,
          {
            name: this.name,
            email: this.email,
            password: this.password
          }
        );
        if ((data.status = 201)) {
          localStorage.setItem("user", JSON.stringify(data));
          this.$root.user = data;
          this.submitted = true;
          this.authenticateUser();
          this.loading = false;
          this.$noty.success("Successful Registration");
        }
      } catch (error) {
        this.loading = false;
        this.errors = error.response.data.errors;
        this.$noty.error("Oops Something went wrong");
      }
    },

    async authenticateUser() {
      try {
        const response = await Axios.post(
          `${process.env.VUE_APP_API_URL}/api/user/token/`,
          {
            email: this.email,
            password: this.password
          }
        );
        if (response.status == 200) {
          localStorage.setItem("token", JSON.stringify(response.data.token));
          this.$root.authToken = response.data.token;
          this.$router.push("/favorites");
        }
      } catch (error) {
        this.errors = error.response.data.errors;
        this.$noty.error("Oops Something went wrong");
      }
    }
  }
};
</script>
