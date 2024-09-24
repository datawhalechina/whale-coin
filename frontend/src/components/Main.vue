<script setup lang="ts">  
import { useLoginStore } from "../store";  
const loginstate = useLoginStore();  
const userid = loginstate.id  
</script>  

<template>  
  <div>hello!</div>  
  <div><router-link to="/coin/apply" target="_blank">鲸币申请</router-link></div>  
  <div v-if="userid < 4"><router-link to="/coin/supervise" target="_blank">鲸币审批</router-link></div>  
  <div><router-link to="/coin/consume" target="_blank">鲸币消费</router-link></div>  
  <div><router-link to="/coin/bill" target="_blank">鲸币账单</router-link></div>  
  <div><router-link to="/item/item" target="_blank">鲸币商品</router-link></div>  
  <div><router-link to="/item/order" target="_blank">鲸币订单</router-link></div>  
</template>  

<style lang="scss" scoped>  
</style>