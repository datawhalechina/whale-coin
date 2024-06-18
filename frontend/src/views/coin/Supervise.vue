<script setup lang="ts">
import {fetchSuperviseAPI, handleSuperviseAPI, addEventAPI} from '../../request/coin/api'
import { onMounted, ref, reactive } from 'vue'
import { ElTable } from 'element-plus'
document.title = "鲸币审批"
let tableData:any = reactive([])
const doRegister = async() => {
    let res = await fetchSuperviseAPI()
    tableData.push(...res)
}
onMounted(doRegister)

const dialogFormVisible = ref(false)
const formLabelWidth = '70px'
const diaglogwidth = '370px'

const form = reactive({
  name: '',
  content: '',
  coin:0
})

const currentRow = ref()
const singleTableRef = ref<InstanceType<typeof ElTable>>()
interface Supervise {
    id: number
    user_id: number
    user_name: string
    repo: string
    role: string
    content: string
    record_time: string
    apply_status:boolean
    apply_time:string
}

const handleCurrentChange = (val: Supervise | undefined) => {
  currentRow.value = val
}

const add = () => {
    dialogFormVisible.value = true;
}



const submit = async() => {
  let res = await addEventAPI({"user_id":2, "content":form.content, "amount":form.coin})
  if (res.code == 200) {
    let temp = {
      id:res.coin_id,
      user_name: form.name,
      user_id:0,
      content: form.content,
      amount: form.coin,
      balance:res.balance,
      record_time:new Date()
    }
    tableData.splice(0, 0, temp)
    dialogFormVisible.value = false
    currentRow.value.balance = res.balance
    currentRow.value.id = res.consume_id
    form.name = ''
    form.content = ''
    form.coin = 0
  }
}




const activate_user = async ()=> {
    // let msg = "确定要同意该鲸币申请-"+currentRow.value.repo+"吗？"
    var coin = prompt('请确认要结算的鲸币数量', '1');
    if (coin && coin.length>0) {
        console.log("同意")
        let res = await handleSuperviseAPI({"action":"grant", "notes":"同意", "id":currentRow.value.id, "amount":Number(coin)})
        if (res.code == 200) {
            let index = tableData.indexOf(currentRow.value);
            if (index > -1) {
                tableData.splice(index, 1);
            }
        }
        
    }
}

const delete_user = async ()=> {
    let msg = "确定拒绝该鲸币申请-"+currentRow.value.repo+"吗？"
    if (confirm(msg)==true) {
        console.log("取消")
        let res = await handleSuperviseAPI({"action":"reject", "notes":currentRow.value.notes, "id":currentRow.value.id, "amount":currentRow.value.amount})
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
    <div>
    <el-button type="primary" @click="add">新增</el-button>
    <el-button v-if="currentRow" type="primary" @click="activate_user">同意</el-button>
    <el-button v-if="currentRow" type="primary" @click="delete_user">拒绝</el-button>
    </div>
  <el-table 
  ref="singleTableRef"
  :data="tableData" 
  stripe 
  highlight-current-row
  style="width: 100%"
  @current-change="handleCurrentChange"
  >
    <el-table-column prop="user_name" label="申请人" />
    <el-table-column prop="repo" label="仓库" width="180" />
    <el-table-column prop="role" label="角色" />
    <el-table-column prop="content" label="内容" />
    <el-table-column prop="record_time" label="产生时间" />
    <el-table-column prop="apply_status" label="申请状态" />
    <el-table-column prop="apply_time" label="申请时间" />
  </el-table>

  <el-dialog v-model="dialogFormVisible" :width="diaglogwidth" :center="true" title="鲸币新增">
    <el-form :model="form">
      <el-form-item label="名字" :label-width="formLabelWidth">
        <el-input v-model="form.name" autocomplete="off" />
      </el-form-item>
      <el-form-item label="内容" :label-width="formLabelWidth">
        <el-input v-model="form.content" autocomplete="off"/>
      </el-form-item>
      <el-form-item label="鲸币" :label-width="formLabelWidth">
        <el-input v-model="form.coin" autocomplete="off"/>
      </el-form-item>
    </el-form>
    <template #footer>
      <span class="dialog-footer">
        <el-button type="primary" @click="submit">确定</el-button>
      </span>
    </template>
  </el-dialog>
</template>

<style lang="scss" scoped>
</style>