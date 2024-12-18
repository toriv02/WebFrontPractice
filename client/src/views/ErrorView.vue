<template>
    <div class="error-page">
      <div class="container">
        <div class="jumbotron">
          <h1 class="display-4">{{ errorTitle }}</h1>
          <p class="lead">{{ errorMessage }}</p>
          <hr class="my-4">
          <div class="video-container">
            <iframe
              width="560"
              height="315"
              :src="videoUrl"
              frameborder="0"
              allowfullscreen
            ></iframe>
          </div>
          <p class="lead mt-4">
            <button class="btn btn-primary btn-lg" @click="goHome" role="button">
              Вернуться на главную
            </button>
            <button class="btn btn-secondary btn-lg mx-2" @click="refreshPage" role="button">
              Обновить страницу
            </button>
          </p>
        </div>
      </div>
    </div>
  </template>
  
  <script setup>
  import { ref } from "vue";
  import { useRouter } from "vue-router";
  import { useRoute } from 'vue-router'
  
  const router = useRouter();
  const route = useRoute()
  const errorTitle = ref(route.params.errorTitle ?? "Упс! Произошла ошибка");
  const errorMessage = ref(route.params.errorMessage ?? "Похоже, что-то пошло не так.");
  const videoUrl = ref("https://www.youtube.com/embed/xvFZjo5PgG0?autoplay=1&mute=1");
  
  function goHome() {
    router.push("/");
  }
  function refreshPage() {
     window.location.reload();
  }
  </script>
  <style scoped>
  .error-page {
      display: flex;
      justify-content: center;
      align-items: center;
      min-height: 100vh; /* Используем min-height для контента */
      background-color: #f8f9fa; /* Светлый фон */
  }
  
  .jumbotron {
    background-color: #fff;
    border-radius: 10px;
    padding: 2rem;
    box-shadow: 0 4px 8px rgba(0,0,0,0.1);
    text-align: center;
  }
  
  .video-container {
    margin: 20px auto; /* Центрируем контейнер и добавляем отступ сверху и снизу */
    display: flex; /* Для центрирования iframe */
    justify-content: center; /* Для центрирования iframe */
  }
  </style>