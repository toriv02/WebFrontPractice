<script setup>
import {computed, onBeforeMount, ref} from 'vue';
import axios from 'axios';
import Cookies from 'js-cookie';
import { storeToRefs } from 'pinia';
import useUserStore from '../stores/userStore';


const kinds = ref ([])




const kindToAdd=ref({})
const kindToEdit=ref({})

const stats=ref({})



const userStore = useUserStore();
const { isSuperuser, users } = storeToRefs(userStore);

const filters = ref({
    name: "",
    user_id: ""
});

onBeforeMount(() => {
  axios.defaults.headers.common['X-CSRFToken'] = Cookies.get("csrftoken");
})



async function fetchKinds(){
  const r =await axios.get("/api/kinds/");
  console.log(r.data);
  kinds.value=r.data;
}



onBeforeMount(async ()=>{
  await fetchKinds()
})

async function onKindAdd(){
  await axios.post(`/api/kinds/`,{
    ...kindToAdd.value,
  });
  
  await fetchKinds();
}



async function onRemoveClick(kind) {
  await axios.delete(`/api/kinds/${kind.id}/`);
  await fetchKinds(); // переподтягиваю
}

async function onKindEditClick(kind) {
  kindToEdit.value = { ...kind };

}
async function onUpdateKind() {
  await axios.put(`/api/kinds/${kindToEdit.value.id}/`, {
    ...kindToEdit.value,
  });
  await fetchKinds();
}

async function fetchStats() {
    const r = await axios.get("/api/kinds/stats/");
    stats.value = r.data;
}



const filteredKinds= computed(() => {
    return kinds.value.filter(kind => {
      const nameMatch = !filters.value.name || (kind.name && kind.name.toLowerCase().includes(filters.value.name.toLowerCase()));
     
      const userMatch = !filters.value.user_id || (kind.user_id && kind.user_id.toString().includes(filters.value.user_id));
      return nameMatch && userMatch ;
    });
});

function resetFilters() {
    filters.value = {
      name: "",
      user_id: ""
    };
}
</script>

<template>
<form @submit.prevent.stop="onKindAdd">
  <div class="row">
    <div class="col">
      <div class="form-floating">
        <input
          type="text"
          class="form-control"
          v-model="kindToAdd.name"
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
    <input type="text" class="form-control" placeholder="Наименование" v-model="filters.name">
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

<div v-for="item in filteredKinds" class="kind-item">
  <div>{{ item.name }}</div>
  <button
    class="btn btn-success"
    @click="onKindEditClick(item)"
    data-bs-toggle="modal"
    data-bs-target="#editKindModal"
  >
    <i class="bi bi-pen-fill"></i>
  </button>
  <button class="btn btn-danger" @click="onRemoveClick(item)">
    <i class="bi bi-x"></i>
  </button>
</div>



<!--модальное окно для редактрования рода-->
<div class="modal fade" id="editKindModal" tabindex="-1">
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
                  v-model="kindToEdit.name"
                />
                <label for="floatingInput">Название</label>
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
            @click="onUpdateKind"s
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
                    <h5 class="modal-title">Статистика рода литературы</h5>
                </div>
                <div class="modal-body">
                    <p>Количество родов литературы: {{ stats.count }}</p>
                    <p>Максимальный ID рода литературы: {{ stats.max }}</p>
                    <p>Минимальный ID рода литературы: {{ stats.min }}</p>
                </div>
                <div class="modal-footer">
                    <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Закрыть</button>
                </div>
            </div>
        </div>
  </div>

</template>


<style lang="scss" scoped>
.kind-item{
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