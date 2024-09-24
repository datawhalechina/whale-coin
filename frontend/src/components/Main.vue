<template>
  <div class="">
    <router-link
      v-for="link in links"
      :key="link.label"
      :to="link.href"
      class="inline-block px-4 py-2 mx-2 my-4 rounded-md bg-custom-color text-white"
    >
      {{ link.label }}
    </router-link>
    <router-view></router-view>
  </div>
</template>

<script>
export default {
  data() {
    return {
      links: [
        { label: '鲸币申请', href: '/coin/apply' },
        { label: '鲸币审批', href: '/coin/supervise' },
        { label: '鲸币消费', href: '/coin/consume' },
        { label: '鲸币账单', href: '/coin/bill' },
        { label: '鲸币商品', href: '/item/item' },
        { label: '鲸币订单', href: '/item/order' },
      ],
    };
  },
};
</script>
