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
          <el-button @click="showDetailModal(scope.row)" size="small"
            >详情</el-button
          >
          <el-button @click="deleteOrder(scope.row.id)" size="small"
            >删除</el-button
          >
        </template>
      </el-table-column>
    </el-table>

    <!-- 添加 Order 模态框 -->
    <el-dialog v-model="addOrderModalVisible" title="添加 Order">
      <el-form :model="addOrderForm" label-width="80px">
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
    // 导入需要的 Vue 功能
    import { defineComponent, ref, onMounted } from "vue";
    // 导入与订单相关的 API
    document.title = "鲸币订单"
    import {
      getOrderAPI,
      getOrderDetalAPI,
      addOrderAPI,
      deleteOrderAPI,
    } from "../../request/item/api";

    /**
     * 定义订单接口，包含订单的所有属性
     */
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
      audit_id: number;
      create_time: Date;
    }

    // 定义 Vue 组件
    export default defineComponent({
      name: "OrderPage",
      setup() {
        // 初始化数据
        const orderList = ref<Order[]>([]);
        const addOrderModalVisible = ref(false);
        const detailModalVisible = ref(false);
        const addOrderForm = ref<Order>({
          id: 0,
          user_id: 0,
          itemid: 0,
          quantity: 0,
          order_type: "",
          status: "",
          toal_price: 0,
          address: "",
          phone: "",
          audit_id: 0,
          create_time: new Date(),
        });
        const detailOrder = ref<Order>({
          id: 0,
          user_id: 0,
          itemid: 0,
          quantity: 0,
          order_type: "",
          status: "",
          toal_price: 0,
          address: "",
          phone: "",
          audit_id: 0,
          create_time: new Date(),
        });

        /**
         * 获取订单列表数据的异步函数
         * 如果获取成功，更新 orderList 的值，否则抛出错误并记录日志
         */
        const getOrders = async () => {
          try {
            const response = await getOrderAPI();
            orderList.value = response.data;
          } catch (error) {
            console.error("获取 Order 列表失败:", error);
          }
        };

        /**
         * 显示添加订单模态框的函数
         * 通过修改变量 addOrderModalVisible 的值来显示模态框
         */
        const showAddOrderModal = () => {
          addOrderModalVisible.value = true;
        };

        /**
         * 提交添加订单的异步函数
         * 如果添加成功，关闭模态框并刷新订单列表，否则抛出错误并记录日志
         */
        const submitAddOrder = async () => {
          try {
            const response = await addOrderAPI({
              quantity: addOrderForm.value.quantity,
              itemid: addOrderForm.value.itemid,
              address: addOrderForm.value.address,
              phone: addOrderForm.value.phone,
              status: addOrderForm.value.status,
              order_type: addOrderForm.value.order_type,
              toal_price: addOrderForm.value.toal_price,
              user_id: addOrderForm.value.user_id,
            });
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

        /**
         * 显示详情模态框的异步函数
         * 根据 order.id 获取订单详情，更新 detailOrder 的值并显示模态框
         */
        const showDetailModal = async (order: Order) => {
          try {
            const response = await getOrderDetalAPI({ orderid: order.id });
            detailOrder.value = response.data;
            detailModalVisible.value = true;
          } catch (error) {
            console.error("获取 Order 详情失败:", error);
          }
        };

        // 删除订单的异步函数
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

        // 返回组件所需的响应式数据和函数
        return {
          orderList,
          addOrderModalVisible,
          detailModalVisible,
          addOrderForm,
          detailOrder,
          showAddOrderModal,
          submitAddOrder,
          showDetailModal,
          deleteOrder,
        };
      },
    });
</script>

  
  <style scoped>
</style>