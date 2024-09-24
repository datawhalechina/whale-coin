<script setup lang="ts">
import Header from './Header.vue'
import NewHeader from './NewHeader.vue';
import Footer from './Footer.vue'
import Main from './Main.vue'
</script>

<template>
  <el-container>
      <el-header>
        <Header />
        <!-- <NewHeader /> -->
      </el-header>

      <el-main>
       <Main />
        <router-view></router-view>
      </el-main>
      <el-footer>
        <Footer />
      </el-footer>
    </el-container>
</template>

<style lang="scss" scoped>

</style>