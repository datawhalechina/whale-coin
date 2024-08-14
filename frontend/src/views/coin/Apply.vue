<script setup lang="ts">
// 导入用于获取鲸币申请列表的 API 请求函数和处理申请的 API 请求函数
import { fetchApplyAPI, handleApplyAPI } from "../../request/coin/api";
// 导入 Vue.js 中的 onMounted 生命周期钩子、ref 函数和 reactive 函数
import { onMounted, ref, reactive } from "vue";
// 导入 Element Plus 中的 ElTable 组件
import { ElTable } from "element-plus";
// 设置当前文档的标题为 "鲸币申请"
document.title = "鲸币申请";
// 使用 reactive 函数创建一个响应式对象，来保存表格数据，并初始化为一个空数组
let tableData: any = reactive([]);
// 定义一个异步函数 doRegister，用于获取数据并更新 tableData
const doRegister = async () => {
  // 调用 fetchApplyAPI 函数获取数据，并等待响应
  let res = await fetchApplyAPI();
  // 将获取到的数据累加到 tableData 数组中
  tableData.push(...res);
};
// 在页面挂载后执行 doRegister 函数
onMounted(doRegister);

// 使用 ref 函数创建一个响应式变量，用于保存当前选中行的数据
const currentRow = ref();
// 使用 ref 函数创建一个响应式变量，用于保存 ElTable 组件的引用
const singleTableRef = ref<InstanceType<typeof ElTable>>();
// 定义一个接口 Apply，描述申请数据的结构
interface Apply {
  // 申请记录的唯一标识符
  id: number;
  // 仓库名称
  repo: string;
  // 角色
  role: string;
  title: string;
  url: string;
  // 申请内容
  content: string;
  // 记录时间
  record_time: string;
}
// 定义一个函数 handleCurrentChange，用来监听表格行的选中事件，并更新 currentRow 变量
const handleCurrentChange = (val: Apply | undefined) => {
  // 更新当前行数据
  currentRow.value = val;
};

// 定义一个异步函数 activate_user，用来处理申请操作
const activate_user = async () => {
  // 弹出确认框，询问是否确定申请该鲸币申请
  let msg = "确定要申请该鲸币申请-" + currentRow.value.repo + "吗？";
  if (confirm(msg) == true) {
    console.log("激活");
    // 调用handleApplyAPI函数，传入参数{"action":"apply", "id":currentRow.value.id}，并等待返回结果
    let res = await handleApplyAPI({
      action: "apply",
      id: currentRow.value.id,
    });
    // 判断返回结果中的code字段是否为200
    if (res.code == 200) {
      // 在tableData数组中查找currentRow.value的索引
      let index = tableData.indexOf(currentRow.value);
      // 如果找到了索引
      if (index > -1) {
        // 将找到的元素从tableData数组中移除
        tableData.splice(index, 1);
      }
    }
  }
};

// 定义一个异步函数 delete_user，用来处理取消申请操作
const delete_user = async () => {
  // 弹出确认框，询问是否确定取消该鲸币申请
  let msg = "确定要取消该鲸币申请-" + currentRow.value.repo + "吗？";
  if (confirm(msg) == true) {
    console.log("取消");
    // 调用 handleApplyAPI 函数，传入取消操作的参数
    let res = await handleApplyAPI({
      action: "cancel",
      id: currentRow.value.id,
    });
    // 如果返回结果的 code 为 200，表示取消成功
    if (res.code == 200) {
      // 在 tableData 中查找当前行的索引
      let index = tableData.indexOf(currentRow.value);
      // 如果索引存在（即找到了当前行）
      if (index > -1) {
        // 从 tableData 中删除当前行
        tableData.splice(index, 1);
      }
    }
  }
};
</script>

<template>
  <div>
    <div v-if="currentRow">
      <el-button type="primary" @click="activate_user">申请</el-button>
      <el-button type="primary" @click="delete_user">取消</el-button>
    </div>
    <el-table
      ref="singleTableRef"
      :data="tableData"
      stripe
      highlight-current-row
      style="width: 100%"
      @current-change="handleCurrentChange"
    >
      <el-table-column prop="repo" label="仓库" width="180" />
      <el-table-column prop="role" label="角色" />
      <el-table-column prop="title" label="title" />
      <el-table-column prop="url" label="url" />
      <el-table-column prop="content" label="内容" />
      <el-table-column prop="record_time" label="产生时间" />
    </el-table>
  </div>
</template>

<style lang="scss" scoped></style>
