const { defineConfig } = require("@vue/cli-service");

console.log("Loading vue.config.js");

module.exports = defineConfig({
  transpileDependencies: true,
  lintOnSave: false, // Deaktiviert ESLint-Warnungen während der Entwicklung
  devServer: {
    proxy: "http://127.0.0.1:8000",
  },
});
