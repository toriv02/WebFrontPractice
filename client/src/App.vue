<script setup>
import { onBeforeMount } from 'vue';
import axios from 'axios';
import Cookies from 'js-cookie';
import { storeToRefs } from 'pinia';
import useUserStore from './stores/userStore';
import {useRouter, useRoute} from "vue-router";
import 'bootstrap/dist/js/bootstrap.bundle.min'



const userStore=useUserStore();
const {
    isAuthenticated,
    username,
    userId
}=storeToRefs(userStore)
const router = useRouter();
const route = useRoute();

onBeforeMount(() => {
  axios.defaults.headers.common['X-CSRFToken'] = Cookies.get("csrftoken");
})

async function logout() {
  const csrfToken = Cookies.get('csrftoken');
  try {
    const response = await axios.post('/api/user/logout/', {}, {
      headers: {
        'X-CSRFToken': csrfToken
      }
    });
    if (response.data.success) {
      userStore.resetUser();
      
    }
    window.location.reload();
  } catch (error) {
    console.error('Ошибка выхода:', error);
  }
}

const isActive = (routePath) => {
  return route.path === routePath;
};
</script>
<template>
  
  <div class="container">
    <nav class="navbar navbar-expand-lg navbar-dark bg-dark">
      <div class="container-fluid">
        <a class="navbar-brand" href="/"> Пользователь {{ username ? username : "не определён" }}</a>
        <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav"
                aria-controls="navbarNav" aria-expanded="false" aria-label="Toggle navigation">
          <span class="navbar-toggler-icon"></span>
        </button>
        <div class="collapse navbar-collapse" id="navbarNav">
          <ul class="navbar-nav me-auto mb-2 mb-lg-0">
            <li class="nav-item" :class="{ 'active': isActive('/') }">
              <router-link class="nav-link" to="/">Книги</router-link>
            </li>
            <li class="nav-item" :class="{ 'active': isActive('/kinds') }">
              <router-link class="nav-link" to="/kinds">Род литературы</router-link>
            </li>
            <li class="nav-item" :class="{ 'active': isActive('/authors') }">
              <router-link class="nav-link" to="/authors">Автор</router-link>
            </li>
            <li class="nav-item" :class="{ 'active': isActive('/forms') }">
              <router-link class="nav-link" to="/forms">Форма</router-link>
            </li>
            <li class="nav-item" :class="{ 'active': isActive('/publishinghouses') }">
              <router-link class="nav-link" to="/publishinghouses">Издание</router-link>
            </li>
            <li class="nav-item" :class="{ 'active': isActive('/matters') }">
              <router-link class="nav-link" to="/matters">Жанр</router-link>
            </li>
          </ul>

          <ul class="navbar-nav ms-auto">
            <li v-if="!isAuthenticated" class="nav-item">
              <router-link class="nav-link" to="/login">Войти</router-link>
            </li>
            <li v-if="isAuthenticated" class="nav-item">
               <a class="nav-link" href="#" @click.prevent="logout">выйти</a>
            </li>

            <li class="nav-item">
               <a class="nav-link" href="/admin">Админка</a>
            </li>

          </ul>
        </div>
      </div>
    </nav>
  </div>

  


  
  <div class="container">
    <router-view/>
  </div>
</template>



