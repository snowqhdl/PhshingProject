<template>
  <div class="app">
    <div class="logo" >
    <img src="/logo.png" alt="logo" />
  </div>
  <p class="intro">Check the 'URL' to protect your private information from phishing site.</p>
    <form class="form" @submit.prevent="submit">
      <input class="input" type="text" v-model="urlInput" placeholder="type URL" />
      <button class="button"><img class="icon" src="/search.png" alt="" /></button>
    </form>
  </div>
  <div v-if="result" class="result" @click="close">
    <ResultModal :res="res" :percent="percent" />
  </div>
</template>

<script setup>
import { ref } from 'vue'
import axios from 'axios'

import ResultModal from './components/ResultModal.vue'


const urlInput = ref('')
const result = ref(false)
const res = ref('')
const percent = ref(0)

const close = () => {
  result.value = false
  if (percent.value) {
    percent.value = 0
  }
}

const submit = async () => {
  const { data } = await axios.get(`http://localhost:8080/validation/check?url=${urlInput.value}`)

  result.value = true

  if (data.result) {
    res.value = `PhishNetter's Danger Percent`
    percent.value = data.result
    return
  }

  res.value = data

}
</script>


