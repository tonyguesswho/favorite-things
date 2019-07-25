<template>
  <nav class="navbar navbar-expand-lg navbar-light bg-light">
    <div class="container-fluid">
      <router-link to="/" class="navbar-brand">
        <img
          src="../assets/img/logo.png"
          alt=""
          srcset=""
          width="30px"
          height="30px"
        />
      </router-link>
      <button
        class="navbar-toggler"
        type="button"
        data-toggle="collapse"
        data-target="#navbarSupportedContent"
        aria-controls="navbarSupportedContent"
        aria-expanded="false"
        aria-label="Toggle navigation"
      >
        <span class="navbar-toggler-icon"></span>
      </button>

      <div class="collapse navbar-collapse" id="navbarSupportedContent">
        <ul class="navbar-nav mr-auto">
          <li class="nav-item nav-link">
            <router-link
              to="/favorites"
              v-if="isAuth"
              class="btn btn-outline-dark btn-sm"
              >Favorites</router-link
            >
          </li>
        </ul>
        <ul class="navbar-nav ml-auto">
          <li class="nav-item nav-link">
            <router-link
              to="/login"
              v-if="!isAuth"
              class="btn btn-outline-dark btn-sm"
              >Login</router-link
            >
          </li>
          <li class="nav-item nav-link">
            <router-link
              to="/signup"
              v-if="!isAuth"
              class="btn btn-outline-dark btn-sm"
              >Signup</router-link
            >
          </li>
          <li class="nav-item nav-link">
            <router-link
              to="/favorites/create"
              v-if="isAuth"
              class="btn btn-outline-dark btn-sm"
              >Add Favorite</router-link
            >
          </li>
          <li class="nav-item nav-link">
            <router-link
              to="/logs"
              v-if="isAuth"
              class="btn btn-outline-dark btn-sm"
              >Audit Logs</router-link
            >
          </li>
          <li class="nav-item dropdown" v-if="isAuth">
            <a
              class="nav-link dropdown-toggle"
              href="#"
              id="navbarDropdown"
              role="button"
              data-toggle="dropdown"
              aria-haspopup="true"
              aria-expanded="false"
            >
              Hi {{ $root.user.name }}
            </a>
            <div class="dropdown-menu" aria-labelledby="navbarDropdown">
              <a class="dropdown-item" href="#" @click="logout">Logout</a>
            </div>
          </li>
        </ul>
      </div>
    </div>
  </nav>
</template>

<script>
export default {
  computed: {
    isAuth() {
      return this.$root.authToken;
    }
  },
  methods: {
    logout() {
      localStorage.removeItem("user");
      localStorage.removeItem("token");
      this.$root.authToken = null;
      this.$root.user = {};
      this.$noty.success("Successful Logged Out");
      this.$router.push("/");
    }
  }
};
</script>
