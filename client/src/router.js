import Vue from "vue";
import Router from "vue-router";
import Login from "./views/Login.vue";
import Signup from "./views/Signup.vue";
import Home from "./views/Home.vue";
import Favorites from "./views/Favorites.vue";
import Favorite from "./views/Favorite.vue";
import CreateFavorite from "./views/CreateFavorite.vue";
import EditFavorite from "./views/EditFavorite.vue";
import Logs from "./views/AuditLogs.vue";

Vue.use(Router);

export default new Router({
  mode: "history",
  base: process.env.BASE_URL,
  routes: [
    {
      path: "/login",
      component: Login
    },
    {
      path: "/signup",
      component: Signup
    },
    {
      path: "/",
      component: Home
    },
    {
      path: "/favorites",
      component: Favorites
    },
    {
      path: "/favorites/create",
      component: CreateFavorite
    },
    {
      path: "/favorite/:id",
      component: Favorite
    },
    {
      path: "/favorite/:id/edit",
      component: EditFavorite
    },
    {
      path: "/logs",
      component: Logs
    }
  ]
});
