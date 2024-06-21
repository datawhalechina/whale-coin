<script setup lang="ts">
import {fetchApplyAPI, handleApplyAPI} from '../../request/coin/api'
import { onMounted, ref, reactive } from 'vue'
import { ElTable } from 'element-plus'
document.title = "鲸币申请"
let tableData:any = reactive([])
const doRegister = async() => {
    let res = await fetchApplyAPI()
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

const activate_user = async ()=> {
    let msg = "确定要申请该鲸币申请-"+currentRow.value.repo+"吗？"
    if (confirm(msg)==true) {
        console.log("激活")
        let res = await handleApplyAPI({"action":"apply", "id":currentRow.value.id})
        if (res.code == 200) {
            let index = tableData.indexOf(currentRow.value);
            if (index > -1) {
                tableData.splice(index, 1);
            }
        }
        
    }
}

const delete_user = async ()=> {
    let msg = "确定要取消该鲸币申请-"+currentRow.value.repo+"吗？"
    if (confirm(msg)==true) {
        console.log("取消")
        let res = await handleApplyAPI({"action":"cancel", "id":currentRow.value.id})
        if (res.code == 200) {
            let index = tableData.indexOf(currentRow.value);
            if (index > -1) {
                tableData.splice(index, 1);
            }
        }
    }
}

</script>

<template>
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
    <el-table-column prop="content" label="内容" />
    <el-table-column prop="record_time" label="产生时间" />
  </el-table>
</template>

<style lang="scss" scoped>
</style>