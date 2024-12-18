<script setup>
import {computed, onBeforeMount, ref} from 'vue';
import axios from 'axios';
import Cookies from 'js-cookie';
import { storeToRefs } from 'pinia';
import useUserStore from '../stores/userStore';



const matters = ref ([])



const matterToAdd=ref({})
const matterToEdit=ref({})

const stats=ref({})



const userStore = useUserStore();
const { isSuperuser, users } = storeToRefs(userStore);

const filters = ref({
    title: "",
    user_id: ""
});

onBeforeMount(() => {
  axios.defaults.headers.common['X-CSRFToken'] = Cookies.get("csrftoken");
})


async function fetchMatters(){
  const r =await axios.get("/api/matters/");
  console.log(r.data);
  matters.value=r.data;
}

onBeforeMount(async ()=>{
  await fetchMatters()
})

async function onMatterAdd() {
  await axios.post("/api/matters/", {
    ...matterToAdd.value,
  });
  await fetchMatters(); // переподтягиваю
}

async function onRemoveClick(matter) {
  await axios.delete(`/api/matters/${matter.id}/`);
  await fetchMatters(); // переподтягиваю
}

async function onMatterEditClick(matter) {
  matterToEdit.value = { ...matter };

}
async function onUpdateMatter() {
  await axios.put(`/api/matters/${matterToEdit.value.id}/`, {
    ...matterToEdit.value,
  });
  await fetchMatters();
}

async function fetchStats() {
    const r = await axios.get("/api/matters/stats/");
    stats.value = r.data;
}




const filteredMatters = computed(() => {
    return matters.value.filter(matter => {
    const titleMatch = !filters.value.title || (matter.title && matter.title.toLowerCase().includes(filters.value.title.toLowerCase()));
    const userMatch = !filters.value.user_id || (matter.user_id && matter.user_id.toString().includes(filters.value.user_id));

    return titleMatch && userMatch;
    });
});

function resetFilters() {
    filters.value = {
      title: "",
      user_id: ""
    };
}
</script>


<template>
<form @submit.prevent.stop="onMatterAdd">
  <div class="row">
    <div class="col">
      <div class="form-floating">
        <input
          type="text"
          class="form-control"
          v-model="matterToAdd.title"
          required
        />
        <label for="floatingInput">Название</label>
      </div>
    </div>
   
    
    <div class="col-auto">
      <button class="btn btn-primary">
        Добавить
      </button>
    </div>
  </div>
</form>


<div class="col-auto d-flex justify-content-end mt-2">
  <button class="btn  btn-info" @click="fetchStats()" data-bs-toggle="modal"
  data-bs-target="#statsModal">Статистика</button>
</div>

<h4>Фильтрация</h4>
<div class="row mb-3 mt-3">
  <div class="col">
    <input type="text" class="form-control" placeholder="Наименование" v-model="filters.title">
  </div>
  <div class="col">
        <select class="form-select" v-model="filters.user_id">
        <option value="">Users</option>
          <option v-for="user in users" :key="user.id" :value="user.id">
              {{ user.username }}
         </option>
       </select>
    </div>
  <div class="col-auto">
    <button class="btn btn-primary" @click="resetFilters">Сбросить</button>
  </div>
</div>


<div v-for="item in filteredMatters" class="matter-item">
  <div>{{ item.title }}</div>
  <button
    class="btn btn-success"
    @click="onMatterEditClick(item)"
    data-bs-toggle="modal"
    data-bs-target="#editMatterModal"
  >
    <i class="bi bi-pen-fill"></i>
  </button>
  <button class="btn btn-danger" @click="onRemoveClick(item)">
    <i class="bi bi-x"></i>
  </button>
</div>

<!-- модальное окно для редактирования жанра-->
<div class="modal fade" id="editMatterModal" tabindex="-1">
    <div class="modal-dialog">
      <div class="modal-content">
        <div class="modal-header">
          <h1 class="modal-title fs-5" id="exampleModalLabel">
            редактировать
          </h1>
          <button
            type="button"
            class="btn-close"
            data-bs-dismiss="modal"
            aria-label="Close"
          ></button>
        </div>
        <div class="modal-body">
          <div class="row">
            <div class="col">
              <div class="form-floating">
                <input
                  type="text"
                  class="form-control"
                  v-model="matterToEdit.title"
                />
                <label for="floatingInput">Наименование</label>
              </div>
            </div>


          </div>
        </div>
        <div class="modal-footer">
          <button
            type="button"
            class="btn btn-secondary"
            data-bs-dismiss="modal"
          >
            Закрыть
          </button>
          <button
            data-bs-dismiss="modal"
            type="button"
            class="btn btn-primary"
            @click="onUpdateMatter"
          >
            Сохранить
          </button>
        </div>
      </div>
    </div>
</div>



<!-- Модальное окно для статистики -->
<div class="modal fade" id="statsModal" tabindex="-1" role="dialog">
        <div class="modal-dialog" role="document">
            <div class="modal-content">
                <div class="modal-header">
                    <h5 class="modal-title">Статистика жанров</h5>
                </div>
                <div class="modal-body">
                    <p>Количество жанров: {{ stats.count }}</p>
                    <p>Максимальный ID жанр: {{ stats.max }}</p>
                    <p>Минимальный ID жанр: {{ stats.min }}</p>
                </div>
                <div class="modal-footer">
                    <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Закрыть</button>
                </div>
            </div>
        </div>
  </div>

  
</template>


<style lang="scss" scoped>
.matter-item{
  padding: 0.5rem;
  margin: 0.5rem 0;
  border: 1px solid silver;
  border-radius: 8px;
  display: grid;
  grid-template-columns: 1fr auto auto;
  gap: 8px;
}

.row{
  margin-top:10px;
}
.row > div {
  margin-bottom: 1rem;
}

.row > div:last-child {
  margin-bottom: 0;
}

.row > div > .form-floating {
    margin-bottom: 1rem;
}

.row > div > .form-floating:last-child {
    margin-bottom: 0;
}

.form-floating label {
  margin-bottom: 0.5rem; 
}
</style>