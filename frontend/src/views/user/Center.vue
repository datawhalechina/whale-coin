<script setup lang="ts">
import { useLoginStore } from "../../store";
document.title = "个人中心"
const loginstate = useLoginStore();
const userid = loginstate.id
</script>

<template>
    <el-link v-if="loginstate.id<4" type="primary" href="/user/registers" >注册列表</el-link>
    <br />
    <el-link type="primary" href="/user/changepass" >修改密码</el-link>
    <br />
    <div v-if="loginstate.id<4"><el-link type="primary" href="/user/resetpass" >重置密码</el-link></div>
    <el-link type="primary" href="/user/editprofile" >编辑个人信息</el-link>
    <br />
    <el-link type="primary" :href="'/user/profile/'+userid" >展示个人信息</el-link>
    <br />
    <el-link v-if="loginstate.id<4" type="primary" href="/user/all" >全部人员</el-link>

    
</template>

<style lang="scss" scoped>
</style>