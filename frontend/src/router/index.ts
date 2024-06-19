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
                path: "user",
                // 命名
                name: "User",
                component: () => import("../views/user/Center.vue"),
                beforeEnter: (to, from, next) => {
                    // 这里是示例，实际情况下，你需要根据你的应用逻辑来判断用户是否已经登录
                    const isAuthenticated = false;
                    if (isAuthenticated) {
                        next();
                    } else {
                        next('/login');
                    }
                },
                children: [
                    {
                        path: "registers",
                        // 命名
                        name: "Register",
                        component: () => import("../views/user/Registers.vue"),
                    },
                    {
                        path: "changepass",
                        // 命名
                        name: "Changepass",
                        component: () => import("../views/user/Changepass.vue"),
                    },
                    {
                        path: "resetpass",
                        // 命名
                        name: "Resetpass",
                        component: () => import("../views/user/Resetpass.vue"),
                    },
                    {
                        path: "editprofile",
                        // 命名
                        name: "Editprofile",
                        component: () => import("../views/user/Editprofile.vue"),
                    },
                    {
                        path: "profile/:id",
                        // 命名
                        name: "Profile",
                        component: () => import("../views/user/Profile.vue"),
                    },
                    {
                        path: "all",
                        // 命名
                        name: "All",
                        component: () => import("../views/user/All.vue"),
                    },
                ]
            },
            {
                path: "coin",
                // 命名
                name: "Coin",
                component: () => import("../views/coin/Apply.vue"),
                children: [
                    {
                        path: "apply",
                        // 命名
                        name: "Apply",
                        component: () => import("../views/coin/Apply.vue"),
                    },
                    {
                        path: "supervise",
                        // 命名
                        name: "Supervise",
                        component: () => import("../views/coin/Supervise.vue"),
                    },
                    {
                        path: "consume",
                        // 命名
                        name: "Consume",
                        component: () => import("../views/coin/Consume.vue"),
                    },
                    {
                        path: "bill",
                        // 命名
                        name: "Bill",
                        component: () => import("../views/coin/Bill.vue"),
                    },
                ]
            },
        ]
    },
];

const router = createRouter({
    // 路由模式
    history: createWebHistory(),
    routes,
});

export default router;
