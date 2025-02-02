import "./assets/main.css";
import Vue3Toastify from "vue3-toastify";
import "jquery"; // Import jQuery
import { createApp } from "vue";
import App from "./App.vue";
import router from "./router";

const app = createApp(App);

app.use(Vue3Toastify, {
  autoClose: 3000,
});

app.use(router);

app.mount("#app");
