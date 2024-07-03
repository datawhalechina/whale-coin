<template>
  <div>
    <el-button @click="showAddItemModal">添加</el-button>
    <el-table :data="itemList" border style="width: 100%">
      <el-table-column prop="id" label="ID" />
      <el-table-column prop="name" label="名称" />
      <el-table-column prop="describe" label="描述" />
      <el-table-column prop="stock" label="库存" />
      <el-table-column prop="prince" label="价格" />
      <el-table-column>
        <template #default="scope">
          <el-button @click="showDetailModal(scope.row)" size="small"
            >详情</el-button
          >
          <el-button @click="deleteItem(scope.row.id)" size="small"
            >删除</el-button
          >
        </template>
      </el-table-column>
    </el-table>

    <!-- 添加 Item 模态框 -->
    <el-dialog v-model="addItemModalVisible" title="添加 Item">
      <el-form ref="addItemForm" :model="addItemForm" label-width="80px">
        <el-form-item label="名称">
          <el-input v-model="addItemForm.name" />
        </el-form-item>
        <el-form-item label="描述">
          <el-input v-model="addItemForm.describe" />
        </el-form-item>
        <el-form-item label="库存">
          <el-input-number v-model="addItemForm.stock" />
        </el-form-item>
        <el-form-item label="价格">
          <el-input-number v-model="addItemForm.prince" />
        </el-form-item>
        <el-form-item label="图片">
          <el-upload
            v-model:file-list="fileList"
            action="#"
            auto-upload:false
            list-type="picture-card"
            :on-preview="handlePictureCardPreview"
            :on-remove="handleRemove"
            :http-request="addFile"
          >
            <el-icon><Plus /></el-icon>
          </el-upload>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="submitAddItem">提交</el-button>
          <el-button @click="addItemModalVisible = false">取消</el-button>
        </el-form-item>
      </el-form>
    </el-dialog>

    <el-dialog v-model="dialogImgVisible" class="image-dialog">
      <img
        style="width: 100%; height: 100%"
        w-full
        :src="dialogImageUrl"
        alt="Preview Image"
      />
    </el-dialog>

    <!-- 详情 Item 模态框 -->
    <el-dialog v-model="detailModalVisible" title="Item 详情">
      <el-form :model="detailItem" label-width="80px">
        <el-form-item label="名称">
          <el-input v-model="detailItem.name" disabled />
        </el-form-item>
        <el-form-item label="描述">
          <el-input v-model="detailItem.describe" disabled />
        </el-form-item>
        <el-form-item label="库存">
          <el-input-number v-model="detailItem.stock" disabled />
        </el-form-item>
        <el-form-item label="价格">
          <el-input-number v-model="detailItem.prince" disabled />
        </el-form-item>
        <el-form-item label="创建时间">
          <el-input v-model="detailItem.create_time" disabled />
        </el-form-item>
        <el-form-item label="创建用户">
          <el-input v-model="detailItem.create_user" disabled />
        </el-form-item>
        <el-form-item label="图片路径">
          <el-input v-model="detailItem.img_path" disabled />
        </el-form-item>
        <el-form-item>
          <el-button @click="detailModalVisible = false">关闭</el-button>
        </el-form-item>
      </el-form>
    </el-dialog>
  </div>
</template>
  
  <script lang="ts">
import { defineComponent, reactive, ref, onMounted } from "vue";
import {
  getItemAPI,
  getItemDetal,
  addItemAPI,
  deleteItemAPI,
} from "../../request/item/api";
import { ElButton, ElTable, ElForm, ElDialog, ElMessage } from "element-plus";
import type { UploadProps, UploadUserFile } from "element-plus";

interface Item {
  id: number;
  name: string;
  describe: string;
  stock: number;
  create_time: Date;
  prince: number;
  create_user: number;
  img_path: string;
}

export default defineComponent({
  name: "ItemPage",
  setup() {
    // 初始化数据
    const fileList = ref<UploadUserFile[]>([]);
    let files = ref<File[]>([]);
    const itemList = reactive<Item[]>([]);
    const addItemModalVisible = ref(false);
    const detailModalVisible = ref(false);
    const dialogImageUrl = ref("");
    const dialogImgVisible = ref(false);
    const addItemForm = reactive<Item>({
      id: 0,
      name: "",
      describe: "",
      stock: 0,
      create_time: new Date(),
      prince: 0,
      create_user: 0,
      img_path: "",
    });
    const detailItem = reactive<Item>({
      id: 0,
      name: "",
      describe: "",
      stock: 0,
      create_time: new Date(),
      prince: 0,
      create_user: 0,
      img_path: "",
    });
    // 获取 Item 列表数据
    const getItems = async () => {
      try {
        const response = await getItemAPI();
        itemList.values = response.data;
      } catch (error) {
        console.error("获取 Item 列表失败:", error);
      }
    };

    const handleRemove: UploadProps["onRemove"] = (uploadFile, uploadFiles) => {
      console.log(uploadFiles.raw);
    };

    const handlePictureCardPreview: UploadProps["onPreview"] = (uploadFile) => {
      console.log(uploadFile);
      dialogImageUrl.value = uploadFile.url!;
      dialogImgVisible.value = true;
    };
    // 显示添加 Item 模态框
    const showAddItemModal = () => {
      addItemModalVisible.value = true;
    };

    const addFile:UploadProps['onChange']= (uploadFile)=>{
      files.value.push(uploadFile.file)
      console.log(uploadFile)
    }
    // 提交添加 Item
    const submitAddItem = async () => {
      try {
        const response = await addItemAPI({
          item: addItemForm,
          files: files, // 处理文件上传的部分
        });
        if (response.status === 200) {
          addItemModalVisible.value = false;
          getItems();
        } else {
          console.error("添加 Item 失败");
        }
      } catch (error) {
        console.error("添加 Item 失败:", error);
      }
    };

    // 显示详情模态框
    const showDetailModal = async (item: Item) => {
      try {
        const response = await getItemDetal({ itemid: item.id });
        detailItem.value = response.data;
        detailModalVisible.value = true;
      } catch (error) {
        console.error("获取 Item 详情失败:", error);
      }
    };

    // 删除 Item
    const deleteItem = async (id: number) => {
      try {
        const response = await deleteItemAPI({ itemid: id });
        if (response.status === 200) {
          getItems();
        } else {
          console.error("删除 Item 失败");
        }
      } catch (error) {
        console.error("删除 Item 失败:", error);
      }
    };

    // 页面加载时获取数据
    onMounted(() => {
      getItems();
    });

    return {
      itemList,
      addItemModalVisible,
      detailModalVisible,
      addItemForm,
      detailItem,
      fileList,
      dialogImageUrl,
      dialogImgVisible,
      showAddItemModal,
      submitAddItem,
      showDetailModal,
      deleteItem,
      handlePictureCardPreview,
      addFile,
      handleRemove
    };
  },
});
</script>
  
  <style scoped>
</style>