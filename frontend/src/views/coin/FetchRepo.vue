<script setup lang="ts">
import { 
  startScheduledUpdateAPI,
  isScheduledUpdateRunningAPI,
  stopScheduledUpdateAPI,
  executeUpdateAPI 
} from '../../request/coin/api';
import { onMounted, ref } from 'vue';
import { ElMessage } from 'element-plus';

// 定义变量来跟踪当前的定时任务状态和手动更新状态
const isScheduledRunning = ref(false);
const isManualUpdating = ref(false); // 用于跟踪手动更新的状态
const manualUpdateMessage = ref(''); // 用于显示手动更新的状态信息

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
      ElMessage.success('任务正在运行');
    } else {
      ElMessage.info('任务没有运行');
    }
  } catch (error) {
    const err = error as any;
    ElMessage.error('无法检查定时任务状态: ' + (err.response?.data?.message || err.message));
    isScheduledRunning.value = false;
  }
};

// 开始定时拉取任务
const startScheduledUpdate = async () => {
  try {
    await startScheduledUpdateAPI();
    ElMessage.success('定时更新任务已启动');
    isScheduledRunning.value = true;
  } catch (error) {
    const err = error as any;
    ElMessage.error('启动定时更新任务失败: ' + (err.response?.data?.message || err.message));
  }
};

// 停止定时拉取任务
const stopScheduledUpdate = async () => {
  try {
    await stopScheduledUpdateAPI();
    ElMessage.success('定时更新任务已停止');
    isScheduledRunning.value = false;
  } catch (error) {
    const err = error as any;
    ElMessage.error('停止定时更新任务失败: ' + (err.response?.data?.message || err.message));
  }
};

// 手动更新任务
const executeUpdate = async () => {
  try {
    isManualUpdating.value = true;
    manualUpdateMessage.value = '正在一次性更新数据...';

    await executeUpdateAPI();
    
    ElMessage.success('本次手动更新完成');
    manualUpdateMessage.value = '本次手动更新完成';
  } catch (error) {
    const err = error as any;
    ElMessage.error('手动更新任务失败: ' + (err.response?.data?.message || err.message));
    manualUpdateMessage.value = '手动更新任务失败';
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
    </div>
  </template>
  

<!-- Tailwind CSS 样式直接在类中定义，无需额外的 style 标签 -->
