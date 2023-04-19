import { createApp } from "vue";
import { createRouter, createWebHistory } from "vue-router";
import routes from "virtual:generated-pages";
import App from "./App.vue";
import { Icon } from "@iconify/vue";
import { createAuth0 } from "@auth0/auth0-vue";
import IllestWaveform from "1llest-waveform-vue";
import "1llest-waveform-vue/lib/style.css";
import { createPinia } from "pinia";
import * as components from "vuetify/components";
import * as directives from "vuetify/directives";
import { createVuetify } from "vuetify";
import "@unocss/reset/tailwind.css";
import "./styles/main.css";
import "uno.css";
import "@mdi/font/css/materialdesignicons.css";

const app = createApp(App);
const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes,
});
app
  .use(createPinia())
  .use(IllestWaveform)
  .use(router)
  .use(
    createVuetify({
      components,
      directives,
    })
  )
  .use(
    createAuth0({
      domain: "dev-tvhqmk7a.us.auth0.com",
      clientId: "53p0EBRRWxSYA3mSywbxhEeIlIexYWbs",
      authorizationParams: {
        redirect_uri: window.location.origin,
      },
    })
  )
  .component("Icon", Icon);
app.mount("#app");
