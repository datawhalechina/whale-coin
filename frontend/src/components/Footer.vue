<script setup lang="ts">
  // 从环境中获取 VITE_API_URL 的值
  // const apiUrl = import.meta.env.VITE_API_URL;
</script>

<template>
  <div class="centered-text">
    鲸币 @ 2024
    <!-- <div class="api-url">API URL: {{ apiUrl }}</div>  -->
  </div>
</template>

<style lang="scss" scoped>
.centered-text {
  text-align: center;
}
.api-url {
  margin-top: 1rem; /* 添加一些间距 */
  font-size: 16px; /* 设置字体大小 */
  color: #555; /* 颜色 */
}
</style>
