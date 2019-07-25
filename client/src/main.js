import Vue from "vue";
import App from "./App.vue";
import router from "./router";
import VueNoty from "vuejs-noty";
import "vuejs-noty/dist/vuejs-noty.css";

Vue.use(VueNoty, {
  timeout: 4000,
  progressBar: true,
  layout: "topCenter"
});

Vue.config.productionTip = false;
const userData = localStorage.getItem("user");
const token = localStorage.getItem("token");

new Vue({
  router,
  data: {
    user: userData ? JSON.parse(userData) : {},
    authToken: token ? JSON.parse(token) : null
  },
  render: h => h(App)
}).$mount("#app");
