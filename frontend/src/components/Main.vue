<script setup lang="ts">
import { useLoginStore } from "../store";
const loginstate = useLoginStore();
const userid = loginstate.id

</script>

<template>
  <div>hello!</div>
  <div><el-link type="primary" href="/coin/apply" target="_blank">鲸币申请</el-link></div>
  <div><el-link v-if="loginstate.id<4" type="primary" href="/coin/supervise" target="_blank">鲸币审批</el-link></div>
  <div><el-link type="primary" href="/coin/consume" target="_blank">鲸币消费</el-link></div>
  <div><el-link type="primary" href="/coin/bill" target="_blank">鲸币账单</el-link></div>
  <div><el-link type="primary" href="/item/item" target="_blank">鲸币商品</el-link></div>
  <div><el-link type="primary" href="/item/order" target="_blank">鲸币订单</el-link></div>
  <div class="">
    <router-link
      v-for="link in links"
      :key="link.label"
      :to="link.href"
      class="inline-block px-4 py-2 mx-2 my-4 rounded-md bg-custom-color text-white"
    >
      {{ link.label }}
    </router-link>
    <router-view></router-view>
  </div>
</template>

<script>
export default {
  data() {
    return {
      links: [
        { label: '鲸币申请', href: '/coin/apply' },
        { label: '鲸币审批', href: '/coin/supervise' },
        { label: '鲸币消费', href: '/coin/consume' },
        { label: '鲸币账单', href: '/coin/bill' },
        { label: '鲸币商品', href: '/item/item' },
        { label: '鲸币订单', href: '/item/order' },
      ],
    };
  },
};
</script>
