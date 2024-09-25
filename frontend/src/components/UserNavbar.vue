<template>  
    <div>  
      <!-- 导航栏 -->  
      <nav class="p-4 bg-gray-100">  
        <router-link v-if="loginstate.id < 4" class="text-blue-600 mr-4" to="/user/registers">注册列表</router-link>  
        <router-link class="text-blue-600 mr-4" to="/user/changepass">修改密码</router-link>  
        <router-link v-if="loginstate.id < 4" class="text-blue-600 mr-4" to="/user/resetpass">重置密码</router-link>  
        <router-link class="text-blue-600 mr-4" to="/user/editprofile">编辑个人信息</router-link>  
        <router-link class="text-blue-600 mr-4" :to="'/user/profile/' + userid">展示个人信息</router-link>  
        <router-link v-if="loginstate.id < 4" class="text-blue-600" to="/user/all">全部人员</router-link>  
      </nav>  
      
    </div>  
  </template>  
  
  <script setup lang="ts">  
  import { useLoginStore } from "../store";  
  const loginstate = useLoginStore();  
  const userid = loginstate.id;  
  </script>