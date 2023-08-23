<template>
  <div class="modal">
    <div class="inner">
      <p class="text">
        {{ props.res }}
      </p>
      <p v-if="props.percent" class="text">{{ props.percent }}%</p>
      <p v-if="props.percent" class="ai-warn">AI의 분석 결과는 참고용으로만 사용하시길 바랍니다.</p>
      <button class="back">X</button>
    </div>
  </div>
</template>

<script setup>
const props = defineProps({ res: String, percent: Number })
</script>
