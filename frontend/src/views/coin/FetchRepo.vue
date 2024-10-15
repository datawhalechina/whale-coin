<script setup lang="ts">
import {
  startScheduledUpdateAPI,
  isScheduledUpdateRunningAPI,
  stopScheduledUpdateAPI,
  executeUpdateAPI,
} from "../../request/coin/api";
import { onMounted, ref } from "vue";
import { ElMessage } from "element-plus";
import { fetchAllSuperviseAPI } from "../../request/coin/api";

import { reactive } from "vue";
import { ElTable } from "element-plus";

document.title = "数据更新";

let allData: any = reactive([]);
const doFetch = async () => {
  let rtn = await fetchAllSuperviseAPI();
  allData.push(...rtn);
};
onMounted(doFetch);

// 定义变量来跟踪当前的定时任务状态和手动更新状态
const isScheduledRunning = ref(false);
const isManualUpdating = ref(false); // 用于跟踪手动更新的状态
const manualUpdateMessage = ref(""); // 用于显示手动更新的状态信息

// 组件挂载时检查是否有运行的定时任务
onMounted(() => {
  checkScheduledStatus();
});

// 检查当前定时任务状态的函数
const checkScheduledStatus = async () => {
  try {
    const response = await isScheduledUpdateRunningAPI();
    const is_running = response?.is_running;
    isScheduledRunning.value = is_running;

    if (is_running) {
      ElMessage.success("任务正在运行");
    } else {
      ElMessage.info("任务没有运行");
    }
  } catch (error) {
    const err = error as any;
    ElMessage.error(
      "无法检查定时任务状态: " + (err.response?.data?.message || err.message)
    );
    isScheduledRunning.value = false;
  }
};

// 开始定时拉取任务
const startScheduledUpdate = async () => {
  try {
    ElMessage.success("定时更新任务已启动");
    isScheduledRunning.value = true;

    const response = await startScheduledUpdateAPI();

    if (response.status === "success") {
      const updateResults = response.data;

      manualUpdateMessage.value = updateResults.join("\n");


      
    } else {
      ElMessage.error("定时更新任务 数据拉取错误: " + response.message);
    }
  } catch (error) {
    const err = error as any;
    ElMessage.error(
      "启动定时更新任务失败: " + (err.response?.data?.message || err.message)
    );
  }
};

const fetchLatestUpdates = async () => {
  try {
    const response = await fetch("http://localhost:8008/get-latest-updates");
    const res = await response.json();
    console.log("res is", res);

    if (res && res.status === "success") {
      console.log("最新更新的数据：", res.data);
      const updateResults = res.data;

      manualUpdateMessage.value = updateResults.join("\n");
      // 更新前端显示的数据
    } else {
      console.error("获取最新数据失败：", res.message);
    }
  } catch (error) {
    console.error("请求错误：", error);
  }
};

// 每隔15秒请求一次后端以获取最新数据
setInterval(fetchLatestUpdates, 15000);

// 停止定时拉取任务
const stopScheduledUpdate = async () => {
  try {
    await stopScheduledUpdateAPI();
    ElMessage.success("定时更新任务已停止");
    isScheduledRunning.value = false;
  } catch (error) {
    const err = error as any;
    ElMessage.error(
      "停止定时更新任务失败: " + (err.response?.data?.message || err.message)
    );
  }
};

// 手动更新任务
const executeUpdate = async () => {
  try {
    isManualUpdating.value = true;
    manualUpdateMessage.value = "正在一次性更新数据...";

    // 调用后端更新api
    const response = await executeUpdateAPI();

    if (response.status === "success") {
      const updateResults = response.data;
      manualUpdateMessage.value =
        "本次手动更新完成，更新了" + updateResults.join("\n");
    } else {
      manualUpdateMessage.value = "更新失败";
    }
    ElMessage.success("本次手动更新完成");
  } catch (error) {
    const err = error as any;
    ElMessage.error(
      "手动更新任务失败: " + (err.response?.data?.message || err.message)
    );
    manualUpdateMessage.value = "手动更新任务失败";
  } finally {
    isManualUpdating.value = false;
  }
};
</script>

<template>
  <div class="flex flex-col items-center justify-center space-y-2 p-4">
    <div class="flex flex-row items-center justify-center space-x-4">
      <!-- 开始定时拉取按钮 -->
      <el-button
        v-if="!isScheduledRunning"
        type="success"
        @click="startScheduledUpdate"
        class="w-48"
      >
        开始定时拉取
      </el-button>

      <!-- 停止定时拉取按钮 -->
      <el-button
        v-if="isScheduledRunning"
        type="danger"
        @click="stopScheduledUpdate"
        class="w-48"
      >
        停止定时拉取
      </el-button>

      <!-- 手动拉取按钮 -->
      <el-button
        type="primary"
        :disabled="isManualUpdating"
        @click="executeUpdate"
        class="w-48"
      >
        手动拉取
      </el-button>
    </div>

    <!-- 状态信息文本 -->
    <p v-if="manualUpdateMessage" class="text-gray-500 mt-2">
      {{ manualUpdateMessage }}
    </p>

    <br />
    <h2 class="text-center">全部鲸币申请</h2>
    <el-table :data="allData" stripe highlight-current-row style="width: 100%">
      <el-table-column prop="user_name" label="申请人" />
      <el-table-column prop="repo" label="仓库" width="80" />
      <el-table-column prop="role" label="角色" />
      <el-table-column prop="content" label="内容" />
      <el-table-column prop="amount" label="数额" />
      <el-table-column prop="record_time" label="产生时间" />
      <el-table-column prop="apply_status" label="申请状态" />
      <el-table-column prop="apply_time" label="申请时间" />
      <el-table-column prop="decision" label="审批决定" />
    </el-table>
  </div>
</template>

<!-- Tailwind CSS 样式直接在类中定义，无需额外的 style 标签 -->
