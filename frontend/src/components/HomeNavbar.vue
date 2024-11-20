<script setup lang="ts">
import { computed } from "vue";
import { useLoginStore } from "../store";

const loginstate = useLoginStore();
const userId = loginstate.id;
console.log('loginstate.iframeurl123', loginstate.iframeurl)

// 定义链接并根据 userId 进行过滤
const links = computed(() =>
  [
    { label: "鲸币申请", href: "/coin/apply" },
    { label: "鲸币审批", href: "/coin/supervise", visible: userId < 4 },
    { label: "鲸币消费", href: "/coin/consume" },
    { label: "鲸币账单", href: "/coin/bill" },
    { label: "鲸币商品", href: "/item/item" },
    { label: "鲸币订单", href: "/item/order" },
    { label: "更新数据", href: "/coin/fetchrepo" , visible: userId < 4 },
    { label: "chat", href: "/chat/Chat" , },
  ].filter((link) => link.visible !== false)
); // 过滤不可见的链接
</script>

<template>
  <div>
    <router-link
      v-for="link in links"
      :key="link.label"
      :to="link.href"
      class="inline-block px-4 py-2 mx-2 my-4 rounded-md bg-custom-color text-white"
    >
      {{ link.label }}
    </router-link>
  </div>
</template>

<style scoped>
/* 你可以在这里定义你的样式 */
</style>
