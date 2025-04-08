const { defineConfig } = require("@vue/cli-service");

module.exports = defineConfig({
  transpileDependencies: true,
  lintOnSave: false, // Deaktiviert ESLint-Warnungen während der Entwicklung
});
