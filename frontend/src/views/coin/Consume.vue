<script setup lang="ts">
import {fetchConsumeAPI, handleConsumeAPI} from '../../request/coin/api'
import { onMounted, ref, reactive } from 'vue'
import { ElTable } from 'element-plus'
document.title = "鲸币消费"
let tableData:any = reactive([])
const doRegister = async() => {
    let res = await fetchConsumeAPI()
    tableData.push(...res)
}
onMounted(doRegister)

const dialogFormVisible = ref(false)
const formLabelWidth = '70px'
const diaglogwidth = '370px'

const form = reactive({
  name: '',
  product: '',
  price:0
})

const currentRow = ref()
const singleTableRef = ref<InstanceType<typeof ElTable>>()
interface Consume {
    id: number
    user_name: string
    user_id: number
    content: string
    amount:number
    balance:number
    record_time: string
}

const handleCurrentChange = (val: Consume | undefined) => {
  currentRow.value = val
}

const add = () => {
    dialogFormVisible.value = true;
}

const submit = async() => {
  let res = await handleConsumeAPI({"user_id":2, "content":form.product, "amount":form.price})
  if (res.code == 200) {
    let temp = {
      id:res.consume_id,
      user_name: form.name,
      user_id:0,
      content: form.product,
      amount: form.price,
      balance:res.balance,
      record_time:new Date()
    }
    tableData.splice(0, 0, temp)
    dialogFormVisible.value = false
    currentRow.value.balance = res.balance
    currentRow.value.id = res.consume_id
    form.name = ''
    form.product = ''
    form.price = 0
  }
}




</script>




<template>
   <div>
    <div>
    <el-button type="primary" @click="add">新增</el-button>
    </div>
  <el-table 
  ref="singleTableRef"
  :data="tableData" 
  stripe 
  highlight-current-row
  style="width: 100%"
  @current-change="handleCurrentChange"
  >
    <el-table-column prop="user_name" label="名字" width="80" />
    <el-table-column prop="content" label="消费事项" />
    <el-table-column prop="amount" label="消费金额" />
    <el-table-column prop="record_time" label="消费时间" />
  </el-table>

  <el-dialog v-model="dialogFormVisible" :width="diaglogwidth" :center="true" title="鲸币消费">
    <el-form :model="form">
      <el-form-item label="名字" :label-width="formLabelWidth">
        <el-input v-model="form.name" autocomplete="off" />
      </el-form-item>
      <el-form-item label="商品" :label-width="formLabelWidth">
        <el-input v-model="form.product" autocomplete="off"/>
      </el-form-item>
      <el-form-item label="价格" :label-width="formLabelWidth">
        <el-input v-model="form.price" autocomplete="off"/>
      </el-form-item>
    </el-form>
    <template #footer>
      <span class="dialog-footer">
        <el-button type="primary" @click="submit">确定</el-button>
      </span>
    </template>
  </el-dialog>
   </div>
</template>

<style lang="scss" scoped>
</style>