import { createApp } from "vue";
import App from "./App.vue";
import router from "./router";
import store from "./store";
// Entferne Importe für i18n
// import { createI18n } from 'vue-i18n';
// import messages from "./i18n"; // Importieren Sie das messages-Objekt

// Element Plus
import ElementPlus from "element-plus";
import "element-plus/dist/index.css";
import * as ElementPlusIconsVue from "@element-plus/icons-vue";

const app = createApp(App);

// Registriere alle Icons
for (const [key, component] of Object.entries(ElementPlusIconsVue)) {
  app.component(key, component);
}

// Entferne Erstellung und Verwendung der i18n-Instanz
// const i18n = createI18n({
//   legacy: false, // Verwenden Sie die Composition API
//   locale: "de",
//   fallbackLocale: "de",
//   messages, // Verwenden Sie das importierte messages-Objekt
//   // globalInjection: true // Optional: Machen Sie $t etc. global verfügbar (kann bei legacy: false weggelassen werden, wenn useI18n verwendet wird)
// });

// app.use(i18n);
app.use(store);
app.use(router);
app.use(ElementPlus);

app.mount("#app");
