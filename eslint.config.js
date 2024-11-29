import config from "@antfu/eslint-config"
import simpleImportSort from "eslint-plugin-simple-import-sort"
import vuePug from "eslint-plugin-vue-pug"

export default config(
  {
    plugins: {
      "simple-import-sort": simpleImportSort,
    },
    formatters: {
      css: true,
    },
    stylistic: {
      quotes: "double",
    },
    rules: {
      "style/max-len": ["error", { code: 120, ignoreUrls: true }],
      "no-alert": "warn",

      "jsonc/indent": ["error", 2],
      "style/quotes": ["error", "double", { avoidEscape: true, allowTemplateLiterals: true }],

      "vue/html-quotes": "off",
      "no-multi-str": "off",
      "vue/custom-event-name-casing": "off",
      "eqeqeq": "warn",
      "no-cond-assign": "warn",
      "no-unmodified-loop-condition": "warn",
      "node/prefer-global/buffer": "warn",
      "node/prefer-global/process": "warn",
      "regexp/no-unused-capturing-group": "warn",
      "ts/no-use-before-define": "warn",
      "unused-imports/no-unused-vars": "warn",
      "vue/eqeqeq": "warn",
      "vue/no-restricted-v-bind": "warn",
      "vue/no-unused-refs": "warn",

    },
  },
  {
    // vue-pug doesn't support eslint flat config
    // this is hand-crafted from eslint-plugin-vue-pug/lib/configs/base.js
    // see. https://github.com/rashfael/eslint-plugin-vue-pug/issues/28
    name: "vue-pug",
    files: ["**/*.vue"],
    languageOptions: {
      parserOptions: {
        templateTokenizer: { pug: "vue-eslint-parser-template-tokenizer-pug" },
      },
    },
    plugins: {
      "vue-pug": vuePug,
    },
    rules: {
      // base
      "vue/component-name-in-template-casing": "off",
      "vue/html-self-closing": "off",
      "vue/html-end-tags": "off",
      "vue/html-indent": "off",
      "vue/multiline-html-element-content-newline": "off",
      "vue/singleline-html-element-content-newline": "off",
      // vue3-essential
      "vue-pug/no-parsing-error": "error",
      // vue3-strongly-recommended
      "vue-pug/no-pug-control-flow": "warn",
    },
  },
  {
    files: ["**/*.vue"],
    rules: {
      // <component-name>
      "vue/component-name-in-template-casing": ["error", "kebab-case"],
      // allow v-for without :key
      "vue/require-v-for-key": "off",
    },
  },
)
