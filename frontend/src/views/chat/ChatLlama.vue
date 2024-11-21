<script setup>
import { ref } from 'vue'

const question = ref('')
const answer = ref('')
const loading = ref(false)

async function handleSubmit() {
  if (!question.value.trim()) return
  
  loading.value = true
  answer.value = ''
  
  try {
    const response = await fetch(`http://localhost:5000/stream_chat?param=${encodeURIComponent(question.value)}`)
    
    const reader = response.body.getReader()
    const decoder = new TextDecoder('utf-8')
    
    while (true) {
      const { done, value } = await reader.read()
      
      if (done) break
      
      // 直接解码并追加文本
      const text = decoder.decode(value)
      answer.value += text
    }
  } catch (error) {
    console.error('Error:', error)
    answer.value = '错误: 无法连接到服务器.'
  } finally {
    loading.value = false
  }
}
</script>

<template>
  <div class="min-h-screen bg-gray-50 py-8 px-4">
    <div class="max-w-3xl mx-auto">
      <!-- 标题 -->
      <h1 class="text-3xl font-bold text-center text-gray-800 mb-8">
        AI 聊天界面
      </h1>
      
      <!-- 输入区域 -->
      <div class="bg-white rounded-lg shadow-md p-6">
        <div class="flex space-x-4">
          <input
            v-model="question"
            type="text"
            placeholder="请输入您的问题..."
            @keyup.enter="handleSubmit"
            :disabled="loading"
            class="flex-1 px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent outline-none transition disabled:bg-gray-100"
          />
          <button
            @click="handleSubmit"
            :disabled="loading || !question.trim()"
            class="px-6 py-2 bg-blue-500 text-white rounded-lg hover:bg-blue-600 focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 transition disabled:bg-blue-300 disabled:cursor-not-allowed"
          >
            <span v-if="loading">
              <svg class="animate-spin h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
              </svg>
            </span>
            <span v-else>发送</span>
          </button>
        </div>
        
        <!-- 回答区域 -->
        <div 
          v-if="answer" 
          class="mt-6 bg-gray-50 rounded-lg p-4 animate-fade-in"
        >
          <div class="prose max-w-none">
            <div class="whitespace-pre-wrap text-gray-700 leading-relaxed">
              {{ answer }}
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<style>
@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateY(10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.animate-fade-in {
  animation: fadeIn 0.3s ease-out;
}
</style>