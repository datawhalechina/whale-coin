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
    <el-dialog v-model="addItemModalVisible" title="添加商品">
      <el-form ref="addItemForm" v-model="addItemForm" label-width="80px">
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
        <!-- <el-form-item label="图片">
          <el-upload
            v-model="fileList"
            action="#"
            auto-upload:false
            list-type="picture-card"
            :on-preview="handlePictureCardPreview"
            :on-remove="handleRemove"
            :http-request="addFile"
          >
            <el-icon><Plus /></el-icon>
          </el-upload>
        </el-form-item> -->
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
    <el-dialog v-model="detailModalVisible" title="商品详情">
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
        <!-- <el-form-item label="图片路径">
          <el-input v-model="detailItem.img_path" disabled />
        </el-form-item> -->
        <el-form-item>
          <el-button @click="detailModalVisible = false">关闭</el-button>
        </el-form-item>
      </el-form>
    </el-dialog>
  </div>
</template>
  
  <script lang="ts">
// 导入 Vue 组件的 defineComponent、ref 和 onMounted 函数
import { defineComponent, ref, onMounted } from "vue";
// 导入与项目或应用程序相关的特定 API 函数
import {
  getItemAPI,
  getItemDetal,
  addItemAPI,
  deleteItemAPI,
} from "../../request/item/api";
// 导入 Element Plus 库中的组件，如 ElButton、ElTable、ElForm 和 ElDialog
import { ElButton, ElTable, ElForm, ElDialog, UploadFile } from "element-plus";
// 导入类型定义，以确保类型安全
import type { UploadProps, UploadUserFile } from "element-plus";

// 定义一个接口，以便于描述和使用具有特定属性的对象
interface Item {
  id: number;
  name: string;
  describe: string;
  stock: number;
  create_time?: Date;
  prince: number;
  create_user?: number;
  img_path?: string;
}

export default defineComponent({
  name: "ItemPage",
   setup() {
    // 初始化数据
    // 定义响应式数组，用于存储上传文件列表
    const fileList = ref<UploadUserFile[]>([]);
    // 定义响应式数组，用于存储选中的文件列表，其中文件类型为 File
    const files = ref<File[]>([]);
    // 定义一个响应式的商品列表数组
    const itemList = ref<Item[]>([]);
    // 定义一个响应式布尔值，表示添加商品模态框是否可见
    const addItemModalVisible = ref(false);
    // 定义一个响应式布尔值，表示详情模态框是否可见
    const detailModalVisible = ref(false);
    // 定义一个响应式字符串，用于存储图片的 URL，供预览图片使用
    const dialogImageUrl = ref("");
    // 定义一个响应式布尔值，表示图片预览对话框是否可见
    const dialogImgVisible = ref(false);
    // 定义一个响应式对象，作为添加商品表单的模型，默认值为一个具有初始属性值的商品对象
    const addItemForm = ref<Item>({
      id: 0,
      name: "",
      describe: "",
      stock: 0,
      prince: 0,
      img_path: "",
    });
    // 定义一个响应式对象，作为详情商品表单的模型，默认值为一个具有初始属性值的商品对象
    const detailItem = ref<Item>({
      id: 0,
      name: "",
      describe: "",
      stock: 0,
      prince: 0,
      img_path: "",
    });
    // 获取 Item 列表数据
    // 定义一个异步函数，用于获取商品列表数据
    const getItems = async () => {
      try {
        // 调用 getItemAPI 函数获取数据，并将返回数据赋值给 itemList 变量
        const response = await getItemAPI();
        itemList.value = response.data;
      } catch (error) {
        // 打印错误信息，用于获取商品列表失败时的错误处理
        console.error("获取 Item 列表失败:", error);
      }
    };

    // 处理文件移除事件
    // 定义一个函数，用于处理文件移除事件
    const handleRemove: UploadProps["onRemove"] = (uploadFile: UploadFile) => {
      // 通过过滤 files 数组，移除名字与当前上传文件名字相同的文件，从而更新 files 数组
      files.value = files.value.filter(
        (file: File) => file.name!= uploadFile.name
      );
      // 打印更新后的 files 数组，通常用于调试目的
      console.log(files);
    };

    // 处理图片预览事件
    // 定义一个函数，用于处理图片预览事件
    const handlePictureCardPreview: UploadProps["onPreview"] = (
      uploadFile: UploadFile
    ) => {
      // 打印上传文件对象，通常用于调试目的
      console.log(uploadFile);
      // 将上传文件的 URL 赋值给 dialogImageUrl，以便于在图片预览对话框中显示
      dialogImageUrl.value = uploadFile.url!;
      // 设置 dialogImgVisible 为 true，打开图片预览对话框
      dialogImgVisible.value = true;
    };
    // 显示添加 Item 模态框
    // 定义一个函数，用于显示添加商品模态框
    const showAddItemModal = () => {
      // 设置 addItemModalVisible 为 true，打开添加商品模态框
      addItemModalVisible.value = true;
    };

    // 添加文件到列表
    // 定义一个函数，用于将上传文件添加到 files 列表中
    const addFile = (uploadFile: UploadFile) => {
      // 打印文件对象和当前 files 数组内容，通常用于调试目的
      console.log(uploadFile, files.value);
    };
    // 提交添加 Item
    // 定义一个异步函数，用于提交添加商品的表单
    const submitAddItem = async () => {
      try {
        // 通过调用 addItemAPI 提交表单数据并得到响应
        const response = await addItemAPI({
          name: "name",
          describe: "describe",
          stock: 0,
          prince: 0,
          // files: files, // 处理文件上传的部分
        });
        // 如果响应状态码为 200，表示成功，关闭模态框并刷新商品列表
        if (response.status === 200) {
          addItemModalVisible.value = false;
          getItems();
        } else {
          // 打印错误信息，用于表示添加商品失败
          console.error("添加 Item 失败");
        }
      } catch (error) {
        // 打印错误信息，用于表示添加商品失败时的其他错误处理
        console.error("添加 Item 失败:", error);
      }
    };

    // 显示详情模态框
    // 定义一个异步函数，用于显示详情模态框并加载详情数据
    const showDetailModal = async (item: Item) => {
      try {
        // 通过调用 getItemDetalAPI 获取选中商品的详情数据并得到响应
        const response = await getItemDetal({ itemid: item.id });
        // 将响应数据赋值给 detailItem 变量，用于详情模态框展示
        detailItem.value = response.data;
        // 设置 detailModalVisible 为 true，打开详情模态框
        detailModalVisible.value = true;
      } catch (error) {
        // 打印错误信息，用于表示获取详情失败时的错误处理
        console.error("获取 Item 详情失败:", error);
      }
    };

    // 删除 Item
    let deleteItem = async (id: number) => {
      try {
        // 通过调用 deleteItemAPI 进行删除操作并得到响应
        const response = await deleteItemAPI({ itemid: id });
        // 如果响应状态码为 200，表示成功，刷新商品列表
        if (response.status === 200) {
          getItems();
        } else {
          // 打印错误信息，用于表示删除商品失败
          console.error("删除 Item 失败");
        }
      } catch (error) {
        // 打印错误信息，用于表示删除商品失败时的其他错误处理
        console.error("删除 Item 失败:", error);
      }
    };

    // 页面加载时获取数据
    // 使用 onMounted 生命周期函数，在组件挂载后调用 getItems 函数，用于初始化页面数据
    onMounted(() => {
      getItems();
    });

    // 返回所有定义的变量和方法
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
      handleRemove,
    };
  },

});
</script>
  
  <style scoped>
</style>