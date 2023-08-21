<template>
  <div class="modal">
    <div class="inner">
      <p class="text">
        {{ props.res }}
      </p>
      <p v-if="props.percent" class="text">{{ props.percent }}%</p>
      <img class="back" src="/arrow-left.png" alt="" />
    </div>
  </div>
</template>

<script setup>
const props = defineProps({ res: String, percent: Number })
</script>
