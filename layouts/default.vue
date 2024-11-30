<template lang="pug">
.layout
  .main
    .page: nuxt-page
</template>

<style module lang="scss">
.layout {
  display: flex;
  height: 100svh;
}

.main {
  flex: 1;
  display: flex;
  flex-direction: column;
}

.page {
  flex: 1;
  overflow-y: auto;
}
</style>
