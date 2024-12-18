<script setup>
import {computed, onBeforeMount, ref} from 'vue';
import axios from 'axios';
import Cookies from 'js-cookie';
import { storeToRefs } from 'pinia';
import useUserStore from '../stores/userStore';


const forms = ref ([])

const stats=ref({})


const formToAdd=ref({})
const formToEdit=ref({})





const userStore = useUserStore();
const { isSuperuser, users } = storeToRefs(userStore);

const filters = ref({
    name: "",
    user_id: ""
});

onBeforeMount(() => {
  axios.defaults.headers.common['X-CSRFToken'] = Cookies.get("csrftoken");
})



async function fetchForms(){
  const r =await axios.get("/api/forms/");
  console.log(r.data);
  forms.value=r.data;
}

onBeforeMount(async ()=>{
  await fetchForms()
})

async function onFormAdd() {
  await axios.post("/api/forms/", {
    ...formToAdd.value,
  });
  await fetchForms(); // переподтягиваю
}
async function onRemoveClick(form) {
  await axios.delete(`/api/forms/${form.id}/`);
  await fetchForms(); // переподтягиваю
}

async function onFormEditClick(form) {
  formToEdit.value = { ...form };

}
async function onUpdateForm() {
  await axios.put(`/api/forms/${formToEdit.value.id}/`, {
    ...formToEdit.value,
  });
  await fetchForms();
}

async function fetchStats() {
    const r = await axios.get("/api/forms/stats/");
    stats.value = r.data;
}


const filteredForms = computed(() => {
    return forms.value.filter(form => {
      const nameMatch = !filters.value.name || (form.name && form.name.toLowerCase().includes(filters.value.name.toLowerCase()));
      const userMatch = !filters.value.user_id || (form.user_id && form.user_id.toString().includes(filters.value.user_id));
      return nameMatch  && userMatch ;
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
<form @submit.prevent.stop="onFormAdd">
  <div class="row">
    <div class="col">
      <div class="form-floating">
        <input
          type="text"
          class="form-control"
          v-model="formToAdd.name"
          required
        />
        <label for="floatingInput">Наименование</label>
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

<div v-for="item in filteredForms" class="form-item">
  <div>{{ item.name }}</div>
  <button
    class="btn btn-success"
    @click="onFormEditClick(item)"
    data-bs-toggle="modal"
    data-bs-target="#editFormModal"
  >
    <i class="bi bi-pen-fill"></i>
  </button>
  <button class="btn btn-danger" @click="onRemoveClick(item)">
    <i class="bi bi-x"></i>
  </button>
</div>


<!-- модальное окно для редактирования формы-->
<div class="modal fade" id="editFormModal" tabindex="-1">
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
                  v-model="formToEdit.name"
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
            @click="onUpdateForm"
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
                    <h5 class="modal-title">Статистика форм</h5>
                </div>
                <div class="modal-body">
                    <p>Количество форм: {{ stats.count }}</p>
                    <p>Максимальный ID формы: {{ stats.max }}</p>
                    <p>Минимальный ID формы: {{ stats.min }}</p>
                </div>
                <div class="modal-footer">
                    <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Закрыть</button>
                </div>
            </div>
        </div>
  </div>



</template>


<style lang="scss" scoped>
.form-item{
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
