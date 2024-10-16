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

const intervalId = ref<number | null>(null);

// 用于存储定时器的id
document.title = "数据更新";

let allData: any = reactive([]);
const doFetch = async () => {
  try {
    const rtn = await fetchAllSuperviseAPI();
    allData.splice(0, allData.length, ...rtn);
    // Clears and fills allData
  } catch (error) {
    const err = error as any;
    ElMessage.error("数据获取失败: " + (err.response?.message || err.message));
  }
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
      "无法检查定时任务状态: " + (err.response?.message || err.message)
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
      const updateResults = response.message;

      manualUpdateMessage.value = updateResults;

      let updateCount = 0;
      intervalId.value = setInterval(async () => {
        updateCount++;
        await doFetch(); // 定时更新前台的数据
        console.log(`更新次数: ${updateCount}`);
      }, 1*60*60*1000); // 
    } else {
      ElMessage.error("定时更新任务 数据拉取错误: " + response.message);
    }
  } catch (error) {
    const err = error as any;
    ElMessage.error(
      "启动定时更新任务失败: " + (err.response?.message || err.message)
    );
  }
};

setInterval(doFetch, 1 * 60 * 1000 + 15000);

// 停止定时拉取任务
const stopScheduledUpdate = async () => {
  try {
    await stopScheduledUpdateAPI();

    // 清除定时器
    if (intervalId.value) {
      clearInterval(intervalId.value);
      intervalId.value = null;
    }
    ElMessage.success("定时更新任务已停止");
    isScheduledRunning.value = false;
  } catch (error) {
    const err = error as any;
    ElMessage.error(
      "停止定时更新任务失败: " + (err.response?.message || err.message)
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
    const updateResults = response.message;
    manualUpdateMessage.value = updateResults;

    if (response.status === "success") {
      await doFetch();
      ElMessage.success("本次手动更新完成");
    } else {
      ElMessage.success("更新未成功");
    }
  } catch (error) {
    const err = error as any;
    ElMessage.error(
      "手动更新任务失败: " + (err.response?.message || err.message)
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

    <!-- 检测定时任务是否在运行 -->
    <p v-if="isScheduledRunning" class="text-green-500 mt-2">
      定时任务正在运行
    </p>
    <p v-else class="text-red-500 mt-2">定时任务未运行</p>


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
