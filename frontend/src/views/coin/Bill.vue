<script setup lang="ts">
import {fetchBillAPI} from '../../request/coin/api'
import { onMounted, ref, reactive } from 'vue'
import { ElTable } from 'element-plus'
document.title = "鲸币账单"
let tableData:any = reactive([])
const doRegister = async() => {
    let res = await fetchBillAPI()
    tableData.push(...res)
}
onMounted(doRegister)

const currentRow = ref()
const singleTableRef = ref<InstanceType<typeof ElTable>>()
interface Apply {
    id: number
    repo: string
    role: string
    content: string
    record_time: string
}

const handleCurrentChange = (val: Apply | undefined) => {
  currentRow.value = val
}



</script>

<template>
  <el-table 
  ref="singleTableRef"
  :data="tableData" 
  stripe 
  highlight-current-row
  style="width: 100%"
  @current-change="handleCurrentChange"
  >
    <el-table-column prop="type" label="类型" width="80" />
    <el-table-column prop="content" label="内容" />
    <el-table-column prop="change_amount" label="金额" />
    <el-table-column prop="balance" label="余额" />
    <el-table-column prop="create_time" label="产生时间" />
  </el-table>
</template>

<style lang="scss" scoped>
</style>