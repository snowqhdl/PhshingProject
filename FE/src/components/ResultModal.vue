<template>
  <div class="modal">
    <div class="inner">
      <img v-if="props.res === 'white site'" src="/check-icon.png" alt="Check Icon" class="verify-icon" />
      <img v-else-if="props.res === 'black site'" src="/x-icon.png" alt="X Icon" class="verify-icon" />
      <img v-else-if="props.res === 'none'"  src="/not-found.png" alt="not found Icon" class="verify-icon" />
      <img v-else-if="props.percent" src="/ai-icon.png" alt="AI Icon" class="verify-icon" />
      <p  v-if="props.res === 'white site'" class="text">
       해당 사이트는 안전합니다. <br> 안심하고 방문하세요!
      </p>
      <p  v-if="props.res === 'black site'" class="text">
        경고! <br> 해당 사이트는 피싱 위험이 확인되었습니다.
      </p>
      <p  v-if="props.res === 'none'" class="text">
        해당 사이트는 존재 하지 않습니다.
      </p>
      <p v-if="props.percent" class="text">AI 분석 결과, 해당 사이트의 위험도는 {{ props.percent }}% 입니다.</p>
      <p v-if="props.percent" class="ai-warn">*AI의 분석 결과는 참고용이니 신중한 판단이 필요합니다.</p>
      <button class="back">X</button>
    </div>
  </div>
</template>

<script setup>
const props = defineProps({ res: String, percent: Number })
</script>
