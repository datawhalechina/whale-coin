<script setup lang="ts">
import {fetchItemAPI} from '../../request/item/api'
import { onMounted, ref, reactive } from 'vue'
import { ElTable , ElTableColumn, ElButton } from 'element-plus'
document.title = "商品清单"
let tableData:any = reactive([])
const getItem = async() => {
    let res = await fetchItemAPI()
    tableData.push(...res)
}
onMounted(getItem)

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

const showDetails = (item) => {
  
};

const deleteItem = (index) => {
  tableData.value.splice(index, 1);
};

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
    <el-table-column prop="name" label="商品名称" width="80" />
    <el-table-column prop="stock" label="库存" />
    <el-table-column prop="prince" label="单价" />
    <el-table-column prop="create_time" label="创建时间" />
    <el-table-column prop="create_time" label="产生时间" />
    <el-table-column label="操作" width="180">
      <template #default="{ row, $index }">
        <!-- 详情按钮 -->
        <el-button size="small" type="text" @click="showDetails(row)">
          详情
        </el-button>
        <!-- 删除按钮 -->
        <el-button
          size="small"
          type="text"
          style="color: #f56c6c"
          @click="deleteItem($index)"
        >
          删除
        </el-button>
      </template>
    </el-table-column>
  </el-table>
</template>

<style lang="scss" scoped>
</style>