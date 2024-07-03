<template>
    <div>
      <el-button @click="showAddOrderModal">添加</el-button>
      <el-table :data="orderList" border style="width: 100%">
        <el-table-column prop="id" label="ID" />
        <el-table-column prop="user_id" label="用户 ID" />
        <el-table-column prop="itemid" label="商品 ID" />
        <el-table-column prop="quantity" label="数量" />
        <el-table-column prop="order_type" label="订单类型" />
        <el-table-column prop="status" label="状态" />
        <el-table-column prop="toal_price" label="总价" />
        <el-table-column>
          <template #default="scope">
            <el-button @click="showDetailModal(scope.row)" size="small">详情</el-button>
            <el-button @click="deleteOrder(scope.row.id)" size="small">删除</el-button>
          </template>
        </el-table-column>
      </el-table>
  
      <!-- 添加 Order 模态框 -->
      <el-dialog :visible.sync="addOrderModalVisible" title="添加 Order">
        <el-form ref="addOrderForm" :model="addOrderForm" label-width="80px">
          <el-form-item label="用户 ID">
            <el-input v-model="addOrderForm.user_id" />
          </el-form-item>
          <el-form-item label="商品 ID">
            <el-input v-model="addOrderForm.itemid" />
          </el-form-item>
          <el-form-item label="数量">
            <el-input-number v-model="addOrderForm.quantity" />
          </el-form-item>
          <el-form-item label="订单类型">
            <el-input v-model="addOrderForm.order_type" />
          </el-form-item>
          <el-form-item label="状态">
            <el-input v-model="addOrderForm.status" />
          </el-form-item>
          <el-form-item label="总价">
            <el-input-number v-model="addOrderForm.toal_price" />
          </el-form-item>
          <el-form-item label="地址">
            <el-input v-model="addOrderForm.address" />
          </el-form-item>
          <el-form-item label="电话">
            <el-input v-model="addOrderForm.phone" />
          </el-form-item>
          <el-form-item>
            <el-button type="primary" @click="submitAddOrder">提交</el-button>
            <el-button @click="addOrderModalVisible = false">取消</el-button>
          </el-form-item>
        </el-form>
      </el-dialog>
  
      <!-- 详情 Order 模态框 -->
      <el-dialog :visible.sync="detailModalVisible" title="Order 详情">
        <el-form :model="detailOrder" label-width="80px">
          <el-form-item label="用户 ID">
            <el-input v-model="detailOrder.user_id" disabled />
          </el-form-item>
          <el-form-item label="商品 ID">
            <el-input v-model="detailOrder.itemid" disabled />
          </el-form-item>
          <el-form-item label="数量">
            <el-input-number v-model="detailOrder.quantity" disabled />
          </el-form-item>
          <el-form-item label="订单类型">
            <el-input v-model="detailOrder.order_type" disabled />
          </el-form-item>
          <el-form-item label="状态">
            <el-input v-model="detailOrder.status" disabled />
          </el-form-item>
          <el-form-item label="总价">
            <el-input-number v-model="detailOrder.toal_price" disabled />
          </el-form-item>
          <el-form-item label="地址">
            <el-input v-model="detailOrder.address" disabled />
          </el-form-item>
          <el-form-item label="电话">
            <el-input v-model="detailOrder.phone" disabled />
          </el-form-item>
          <el-form-item label="创建时间">
            <el-input v-model="detailOrder.create_time" disabled />
          </el-form-item>
          <el-form-item label="审核 ID">
            <el-input v-model="detailOrder.audit_id" disabled />
          </el-form-item>
          <el-form-item>
            <el-button @click="detailModalVisible = false">关闭</el-button>
          </el-form-item>
        </el-form>
      </el-dialog>
    </div>
  </template>
  
  <script lang="ts">
  import { defineComponent, reactive, ref } from "vue";
  import {
    getOrderAPI,
    getOrderDetalAPI,
    addOrderAPI,
    deleteOrderAPI
  } from "../../request/item/api";
  
  interface Order {
    id: number;
    user_id: number;
    itemid: number;
    quantity: number;
    order_type: string;
    status: string;
    toal_price: number;
    address: string;
    phone: string;
    create_time: Date;
    audit_id: number;
  }
  
  export default defineComponent({
    name: "OrderPage",
    setup() {
      // 初始化数据
      const orderList = reactive<Order[]>([]);
      const addOrderModalVisible = ref(false);
      const detailModalVisible = ref(false);
      const addOrderForm = reactive<Order>({
        id: 0,
        user_id: 0,
        itemid: 0,
        quantity: 0,
        order_type: "",
        status: "",
        toal_price: 0,
        address: "",
        phone: "",
        create_time: new Date(),
        audit_id: 0
      });
      const detailOrder = reactive<Order>({
        id: 0,
        user_id: 0,
        itemid: 0,
        quantity: 0,
        order_type: "",
        status: "",
        toal_price: 0,
        address: "",
        phone: "",
        create_time: new Date(),
        audit_id: 0
      });
  
      // 获取 Order 列表数据
      const getOrders = async () => {
        try {
          const response = await getOrderAPI();
          orderList.values = response.data;
        } catch (error) {
          console.error("获取 Order 列表失败:", error);
        }
      };
  
      // 显示添加 Order 模态框
      const showAddOrderModal = () => {
        addOrderModalVisible.value = true;
      };
  
      // 提交添加 Order
      const submitAddOrder = async () => {
        try {
          const response = await addOrderAPI({ order: addOrderForm });
          if (response.status === 200) {
            addOrderModalVisible.value = false;
            getOrders();
          } else {
            console.error("添加 Order 失败");
          }
        } catch (error) {
          console.error("添加 Order 失败:", error);
        }
      };
  
      // 显示详情模态框
      const showDetailModal = async (order: Order) => {
        try {
          const response = await getOrderDetalAPI({ orderid: order.id });
          detailOrder.value = response.data;
          detailModalVisible.value = true;
        } catch (error) {
          console.error("获取 Order 详情失败:", error);
        }
      };
  
      // 删除 Order
      const deleteOrder = async (id: number) => {
        try {
          const response = await deleteOrderAPI({ orderid: id });
          if (response.status === 200) {
            getOrders();
          } else {
            console.error("删除 Order 失败");
          }
        } catch (error) {
          console.error("删除 Order 失败:", error);
        }
      };
  
      // 页面加载时获取数据
      onMounted(() => {
        getOrders();
      });
  
      return {
        orderList,
        addOrderModalVisible,
        detailModalVisible,
        addOrderForm,
        detailOrder,
        showAddOrderModal,
        submitAddOrder,
        showDetailModal,
        deleteOrder
      };
    }
  });
  </script>
  
  <style scoped>
  
  </style>