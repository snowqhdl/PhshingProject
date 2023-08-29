<template>
  <div class="app">
    <div class="logo" >
    <img src="/logo.png" alt="logo" />
  </div>
    <form class="form" @submit.prevent="submit">
      <input class="input" type="text" v-model="urlInput" placeholder="여기에 URL을 입력해서 확인하고 당신의 개인 정보를 보호하세요."/>
      <button class="button"><img class="icon" src="/search.png" alt="" /></button>
    </form>
    <div v-if="showMessage" class="message">
      URL을 입력해 주세요.
    </div>
    <div v-if="showWarning" class="warning">
      'http://' 혹은 'https://'를 URL에 입력하세요.
    </div>
  </div>
  <div v-if="result" class="result" @click="close">
    <ResultModal :res="res" :percent="percent" />
  </div>
  <p class="trust-message">저희의 데이터베이스와 AI는 꾸준히 업데이트 되어 최신의 위협을 탐지합니다.</p>
</template>

<script setup>
import { ref } from 'vue'
import axios from 'axios'
import ResultModal from './components/ResultModal.vue'


const urlInput = ref('')
const result = ref(false)
const res = ref('')
const percent = ref(0)
const showMessage = ref(false)
const showWarning = ref(false)


const close = () => {
  result.value = false
  if (percent.value) {
    percent.value = 0
  }
}

const submit = async () => {  
  if (!urlInput.value) {
    showMessage.value = true;
    setTimeout(() => {    
      showMessage.value = false;
    }, 1500);
    return;
  } else{
    showMessage.value = false;
  }
  if (!urlInput.value.startsWith('http://') && !urlInput.value.startsWith('https://')) {
    showWarning.value = true; 
    setTimeout(() => {    
      showWarning.value = false;
    }, 1500);
    return;
  } else {
    showWarning.value = false; 
  }
  
  const { data } = await axios.get(`http://ec2-43-200-169-122.ap-northeast-2.compute.amazonaws.com:8080/validation/check?url=${urlInput.value}`)

  result.value = true

  if (data.result) {
    res.value = `PhishNetter AI 분석 결과 피싱 사이트일 확률`
    percent.value = data.result
    return
  }

  res.value = data

}
</script>
