<template>
  <!-- <el-row>
    <el-col :lg="3" :md="6" :sm="9" :xs="12">
      <a href="/">
       <img src="/logo.png" class="logo" alt="你好" />
        <h3>鲸币</h3>
      </a>
    </el-col>
    <el-col :lg="9" :md="12" :sm="15" :xs="18">
      
      <el-menu
        :default-active="activeIndex"
        mode="horizontal"
        @select="handleSelect"
        style="width: 50%"
        router
      >
        <el-menu-item index="/">第一</el-menu-item>
        <el-menu-item index="/">第二</el-menu-item>
      </el-menu>
    </el-col>

    <el-col :lg="3" :md="6" :sm="9" :xs="12">
      <el-link style="float: right;margin-top:20px;" type="primary">
        <Login />
      </el-link>
    </el-col>
  </el-row> -->
  <el-container>
    <el-header>
      <div class="header-container">
        <a href="/">
          <!-- <img src="/logo.png" class="logo" alt="你好" /> -->
          <h2 class="text-2xl text-bold text-sky-600">鲸币</h2>
        </a>
        <!-- 电脑端菜单 -->
        <el-menu
          :default-active="activeIndex"
          class="el-menu-demo"
          mode="horizontal"
          @select="handleSelect"
          :ellipsis="false"
        >
          <el-menu-item index="1"><router-link to="/">首页</router-link></el-menu-item>
          <el-menu-item index="2">课程</el-menu-item>
          <el-menu-item index="3">资源</el-menu-item>
          <el-menu-item index="4"><Login /></el-menu-item>
        </el-menu>
        <div class="menu-icon-container">
          <el-icon class="menu-icon" @click="drawer = true"><Fold /></el-icon>
        </div>
      </div>
    </el-header>
    <!-- 手机端菜单 -->
    <el-drawer v-model="drawer" direction="rtl" size="80%">
      <el-menu :default-active="activeIndex" @select="handleSelect">
        <el-menu-item index="1">首页</el-menu-item>
        <el-menu-item index="2">课程</el-menu-item>
        <el-menu-item index="3">资源</el-menu-item>
        <el-menu-item index="Login"><Login /></el-menu-item>
        <el-sub-menu index="5">
          <template #title>
            <el-icon><icon-menu /></el-icon>
            <span>编程语言</span>
          </template>
          <el-menu-item index="5-1">JavaScript</el-menu-item>
          <el-menu-item index="5-2">Python</el-menu-item>
          <el-menu-item index="5-3">Java</el-menu-item>
        </el-sub-menu>
        <el-sub-menu index="6">
          <template #title>
            <el-icon><icon-menu /></el-icon>
            <span>框架</span>
          </template>
          <el-menu-item index="6-1">Vue.js</el-menu-item>
          <el-menu-item index="6-2">React</el-menu-item>
          <el-menu-item index="6-3">Angular</el-menu-item>
        </el-sub-menu>
      </el-menu>
    </el-drawer>
  </el-container>
</template>

<script setup lang="ts">
import { ref } from "vue";
import Login from "./Login.vue";
import { Menu as IconMenu, Fold } from "@element-plus/icons-vue";

const activeIndex = ref("1");
const drawer = ref(false);

const handleSelect = (key: string, keyPath: string[]) => {
  console.log(key, keyPath);
  // 选择登录时不收缩drawer
  if (key !== "Login") {
    drawer.value = false;
  }
};
</script>
<style lang="scss" scoped>
img.logo {
  padding-top: 10px;
  height: 40px;
  vertical-align: middle;
}
.logo {
  will-change: filter;
  transition: filter 300ms;
}
.logo:hover {
  filter: drop-shadow(0 0 2em #646cffaa);
}
.logo.vue:hover {
  filter: drop-shadow(0 0 2em #42b883aa);
}
.el-main {
  background-color: #e9eef3;
  color: #333;
}

.header-container {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.logo {
  font-size: 1.5em;
  font-weight: bold;
}

.el-menu-demo {
  flex-grow: 1;
  justify-content: flex-end;
}

.menu-icon-container {
  display: none;
}

.menu-icon {
  font-size: 24px;
  cursor: pointer;
}

.image {
  width: 100%;
  display: block;
}

.bottom {
  margin-top: 13px;
  line-height: 12px;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.button {
  padding: 0;
  min-height: auto;
}

@media screen and (max-width: 768px) {
  .el-menu-demo {
    display: none;
  }

  .menu-icon-container {
    display: block;
  }
}
</style>
