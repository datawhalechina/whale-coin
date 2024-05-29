<script setup lang="ts">
import { useLoginStore } from "../../store";
import {getProfileAPI} from '../../request/user/api'
import { reactive, onMounted, computed } from 'vue'
import { useRoute } from 'vue-router'
document.title = "个人信息"
const route = useRoute()
const loginstate = useLoginStore();
const current_userid = loginstate.id
const userid = Number(route.params.id)
const fileList = reactive([
  {
    name: 'food.jpeg',
    url: 'https://fuss10.elemecdn.com/3/63/4e7f3a15429bfda99bce42a18cdd1jpeg.jpeg?imageMogr2/thumbnail/360x360/format/webp/quality/100',
  }
])

const form = reactive({
  name: '',
  region: '',
  gender: '',
  desc: '',
})

const who =computed(()=>{
  if (current_userid==userid){
    return '我'
  } else if (current_userid!=userid && form.gender=='男'){
    return '他'
  } else if (current_userid!=userid && form.gender=='女'){
    return '她'
  } else {
    return 'TA'
  }
})

const getProfile = async () => {
  let res = await getProfileAPI({userid:userid})
  form.name = res.name
  form.region = res.location
  form.gender = res.gender
  form.desc = res.desc
  fileList.length = 0
  fileList.push(...res.profiles)
  console.log(res.profiles)
  
}


onMounted(()=>{
  getProfile()
})



</script>

<template>
    <div>名字：{{ form.name }}</div>
    <div>性别：{{ form.gender }}</div>
    <div>居住地：{{ form.region }}</div>
    <div>相册：</div>
    <div class="demo-image">
        <div v-for="pic in fileList" :key="pic.name" class="block">
        <el-image 
        style="width: 100px; height: 100px" 
        :preview-src-list="[loginstate.iframeurl+'/'+pic.url]"
        :max-scale="7"
        :min-scale="0.2"
        :src="loginstate.iframeurl+'/'+pic.url" 
        :fit="'scale-down'"/>
        </div>
    </div>
    <h2>{{ who }}的简介</h2>
    <div style="white-space: pre-wrap;">{{ form.desc }}</div>

    

</template>

<style lang="scss" scoped>
.demo-image .block {
  padding: 30px 0;
  text-align: center;
  border-right: solid 1px var(--el-border-color);
  display: inline-block;
  width: 20%;
  box-sizing: border-box;
  vertical-align: top;
}
.demo-image .block:last-child {
  border-right: none;
}
</style>