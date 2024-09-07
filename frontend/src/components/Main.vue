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
</template>

<style lang="scss" scoped>

</style>
