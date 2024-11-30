<script setup lang="ts">
const name = ref("")

async function create_job(prompt: string) {
  await $fetch("/api/job/", {
    method: "POST",
    body: {
      args: prompt,
    },
  })
}
</script>

<template lang="pug">
.test
  o-field(label="Name" variant="info")
    o-input(v-model="name" icon-right="search")
    o-button(@click="create_job(name)") Click Me
</template>

<style module lang="scss">
.test {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  margin-left: 50px;
  padding-left: 50px;
}
</style>
