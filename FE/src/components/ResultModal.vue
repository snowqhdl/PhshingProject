<template>
  <div class="modal">
    <div class="inner">
      <p class="text">
        {{ props.res }}
      </p>
      <p v-if="props.percent" class="text">{{ props.percent }}%</p>
      <button class="back">X</button>
    </div>
  </div>
</template>

<script setup>
const props = defineProps({ res: String, percent: Number })
</script>
