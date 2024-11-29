// https://nuxt.com/docs/api/configuration/nuxt-config
export default defineNuxtConfig({
  devtools: { enabled: false },

  compatibilityDate: "2024-08-09",

  modules: ["@pinia/nuxt", "@pinia-plugin-persistedstate/nuxt"],
  ssr: false,

  nitro: {
    esbuild: {
      options: {
        // For native bigints.
        target: "ESNext",
      },
    },
  },
  css: [
    "~/styles/index.scss",
  ],

  runtimeConfig: {
    // Token for accessing admin API
    adminToken: "",
    database: {
      url: "postgres://localhost/landcraft",
      log: false,
    },
  },

})
