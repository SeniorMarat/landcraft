<script setup lang="ts">
const name = ref("")
</script>

<template lang="pug">
.test
  pre {{ name }}
  o-field(label="Name" variant="info")
    o-input(v-model="name" icon-right="search")
</template>

<style module lang="scss">
.test {
  color: red;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  margin-left: 50px;
  padding-left: 50px;
}
</style>
