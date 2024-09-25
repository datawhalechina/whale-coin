<script setup lang="ts">
import Header from "./Header.vue";
import Footer from "./Footer.vue";
import UserNavbar from "./UserNavbar.vue";
</script>

<template>
  <el-container>
    <el-header>
      <Header />
    </el-header>

    <el-main>
      <UserNavbar />
      <router-view></router-view>
    </el-main>
    <el-footer>
      <Footer />
    </el-footer>
  </el-container>
</template>

<style lang="scss" scoped></style>
