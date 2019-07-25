import Vue from "vue";
import App from "./App.vue";
import router from "./router";
//import store from "./store";
import VueNoty from "vuejs-noty";
import "vuejs-noty/dist/vuejs-noty.css";
Vue.use(VueNoty);

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
