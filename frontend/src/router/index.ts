import { createRouter, createWebHistory, RouteRecordRaw } from "vue-router";

 
// 路由类型:RouteRecordRaw
const routes: Array<RouteRecordRaw> = [
  {
    path: "/",
    // 命名
    name: "index",
    component: () => import("../components/Layout.vue"),
    children: [
        {
            path: "/",
            // 命名
            name: "Home",
            component: () => import("../views/Home.vue"),
        },
        {
          path: "/user",
          // 命名
          name: "User",
          component: () => import("../views/user/Center.vue"),
        },
        
       
    ]
  },
  {
    path:'/',
    component: () => import('@/components/UserLayout.vue'),
    children:[
      {
        path: "/user/registers",
          // 命名
          name: "Register",
          component: () => import("../views/user/Registers.vue"),
        },
        {
          path: "/user/changepass",
          // 命名
          name: "Changepass",
          component: () => import("../views/user/Changepass.vue"),
        },
        {
          path: "/user/resetpass",
          // 命名
          name: "Resetpass",
          component: () => import("../views/user/Resetpass.vue"),
        },
        {
          path: "/user/editprofile",
            // 命名
            name: "Editprofile",
            component: () => import("../views/user/Editprofile.vue"),
        },
        {
          path: "/user/profile/:id",
            // 命名
            name: "Profile",
            component: () => import("../views/user/Profile.vue"),
        },
        {
          path: "/user/all",
          // 命名
          name: "All",
          component: () => import("../views/user/All.vue"),
        },
      
    ]
    
  },
  {
    path:'/',
    component: () => import('@/components/HomeLayout.vue'),
    children:[
      {
        path: "/coin/apply",
        // 命名
        name: "Apply",
        component: () => import("../views/coin/Apply.vue"),
      },
      {
        path: "/coin/supervise",
        // 命名
        name: "Supervise",
        component: () => import("../views/coin/Supervise.vue"),
      },
      {
        path: "/coin/consume",
        // 命名
        name: "Consume",
        component: () => import("../views/coin/Consume.vue"),
      },
      {
        path: "/coin/bill",
        // 命名
        name: "Bill",
        component: () => import("../views/coin/Bill.vue"),
      },
      {
        path: "/item/item",
        // 命名
        name: "Item",
        component: () => import("../views/item/Item.vue"),
      },
      {
        path: "/item/order",
        // 命名
        name: "Order",
        component: () => import("../views/item/Order.vue"),
      },
      {
        path: "/coin/fetchrepo",
        // 命名
        name: "Order",
        component: () => import("../views/coin/FetchRepo.vue"),
      },
    ]
    
  }
  
  
  
];
 
const router = createRouter({
  // 路由模式
  history: createWebHistory(),
  routes,
});
 
export default router;