<script setup>
import {computed, onBeforeMount, ref} from 'vue';
import axios from 'axios';
import Cookies from 'js-cookie';
import { storeToRefs } from 'pinia';
import useUserStore from '../stores/userStore';


const publishingHouses = ref ([])



const publishingHouseToAdd=ref({})
const publishingHouseToEdit=ref({})
const publishingHousePictureRef=ref('')
const publishingHouseAddImageUrl=ref('')

const publishingHousePeactureShow=ref('')

const stats=ref({})

const publishingHouseEditImageURL=ref('')
const publishingHousePictureRefEdit=ref('')


const userStore = useUserStore();
const { isSuperuser, users } = storeToRefs(userStore);

const filters = ref({
    name: "",
    year_of_foundation: "",
    user_id: ""
});

onBeforeMount(() => {
  axios.defaults.headers.common['X-CSRFToken'] = Cookies.get("csrftoken");
})


async function fetchPublishingHouses(){
  const r =await axios.get("/api/publishinghouses/");
  console.log(r.data);
  publishingHouses.value=r.data;
}


onBeforeMount(async ()=>{
  await fetchPublishingHouses()
})

async function onPublishingHouseAdd() {
  const formData=new FormData();
  if(publishingHousePictureRef.value && publishingHousePictureRef.value.files.length>0){
    formData.append('picture', publishingHousePictureRef.value.files[0])
  }

  formData.set('name',publishingHouseToAdd.value.name)
  formData.set('year_of_foundation',publishingHouseToAdd.value.year_of_foundation)


  await axios.post("/api/publishinghouses/", formData,{
    headers:{
      'Content-type': 'multipart/form-data'
    }
  });
  await fetchPublishingHouses(); // переподтягиваю

}
async function onRemoveClick(publishingHouse) {
  await axios.delete(`/api/publishinghouses/${publishingHouse.id}/`);
  await fetchPublishingHouses(); // переподтягиваю
}

async function onPublishingHouseEditClick(publishingHouse) {
  publishingHouseToEdit.value = { ...publishingHouse };
  publishingHouseEditImageURL.value=publishingHouse.picture;
}

async function onUpdatePublishingHouse() {
  const formData=new FormData();
  
  if(publishingHousePictureRefEdit.value && publishingHousePictureRefEdit.value.files.length>0){
    formData.append('picture', publishingHousePictureRefEdit.value.files[0])
  }

  formData.set('name',publishingHouseToEdit.value.name)
  formData.set('year_of_foundation',publishingHouseToEdit.value.year_of_foundation)

  await axios.put(`/api/publishinghouses/${publishingHouseToEdit.value.id}/`, formData,{
    headers:{
      'Content-type': 'multipart/form-data'
    }
  });
  await fetchPublishingHouses();
}

async function publishingHouseAddPitureChange() {
  if(publishingHousePictureRef.value && publishingHousePictureRef.value.files.length>0){
    publishingHouseAddImageUrl.value=URL.createObjectURL(publishingHousePictureRef.value.files[0])
  }
}

async function showPicture(picture) {
  publishingHousePeactureShow.value=picture
}

async function publishingHousesEditPictureChange() {
  if(publishingHousePictureRefEdit.value && publishingHousePictureRefEdit.value.files.length>0){
    publishingHouseEditImageURL.value=URL.createObjectURL(publishingHousePictureRefEdit.value.files[0])
  }
}

async function fetchStats() {
    const r = await axios.get("/api/publishinghouses/stats/");
    stats.value = r.data;
}





const filteredPublishingHouses = computed(() => {
  return publishingHouses.value.filter(house => {
    const nameMatch = !filters.value.name || (house.name && house.name.toLowerCase().includes(filters.value.name.toLowerCase()));
    const yearMatch = !filters.value.year_of_foundation || (house.year_of_foundation && house.year_of_foundation.toString().includes(filters.value.year_of_foundation));
    const userMatch = !filters.value.user_id || (house.user_id && house.user_id.toString().includes(filters.value.user_id));

    return nameMatch && yearMatch && userMatch;
});
});
function resetFilters() {
    filters.value = {
      name: "",
      year_of_foundation: "",
      user_id: ""
    };
}


</script>

<template>
<form @submit.prevent.stop="onPublishingHouseAdd">
  <div class="row">
    <div class="col">
      <div class="form-floating">
        <input
          type="text"
          class="form-control"
          v-model="publishingHouseToAdd.name"
          required
        />
        <label for="floatingInput">Наименование</label>
      </div>
    </div>
    

    <div class="col">
      <div class="form-floating">
        <input
          type="text"
          class="form-control"
          v-model="publishingHouseToAdd.year_of_foundation"
          required
        />
        <label for="floatingInput">Год основания</label>
      </div>
    </div>

    <div class="col-autho">
      <input class="form-control" type="file" ref="publishingHousePictureRef" @change="publishingHouseAddPitureChange">
    </div>

    <div class="col-autho">
      <img :src="publishingHouseAddImageUrl" style="max-height: 60px;" alt="">
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
    <input type="text" class="form-control" placeholder="Название" v-model="filters.name">
  </div>
  <div class="col">
    <input type="text" class="form-control" placeholder="Год основания" v-model="filters.year_of_foundation">
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

<div v-for="item in filteredPublishingHouses" class="publishingHouse-item">
  <div class="publishingHouse-info">
    <span>{{ item.name }}</span>
    <span>{{ item.year_of_foundation }}</span>
  </div>
  <div v-show="item.picture" class="publishingHouse-image">
    <img :src="item.picture" style="max-height: 60px;"
        @click="showPicture(item.picture)"
        data-bs-toggle="modal"
        data-bs-target="#showPictureModal"
      >
  </div>
  <div class="publishingHouse-actions">
    <button
      class="btn btn-success"
      @click="onPublishingHouseEditClick(item)"
      data-bs-toggle="modal"
      data-bs-target="#editPublishingHouseModal"
    >
      <i class="bi bi-pen-fill"></i>
    </button>
    <button class="btn btn-danger" @click="onRemoveClick(item)">
      <i class="bi bi-x"></i>
    </button>
  </div>
</div>

<!-- модальное окно для для редоктирования идания-->
<div class="modal fade" id="editPublishingHouseModal" tabindex="-1">
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
          <div class="row p-1">
            
            <div class="col">
              <div class="form-floating">
                <input
                  type="text"
                  class="form-control"
                  v-model="publishingHouseToEdit.name"
                  required
                />
                <label for="floatingInput">Наименование</label>
              </div>
            </div>
            

            <div class="col">
              <div class="form-floating">
                <input
                  type="text"
                  class="form-control"
                  v-model="publishingHouseToEdit.year_of_foundation"
                  required
                />
                <label for="floatingInput">Год основания</label>
              </div>
            </div>

          </div>

          <div class="row p-1">
                  <div class="col-6">
                    <input class="form-control" type="file" ref="publishingHousePictureRefEdit"
                         @change="publishingHousesEditPictureChange">
                  </div>
                  <div class="col-auto">
                    <img v-if="publishingHouseEditImageURL" :src="publishingHouseEditImageURL" style="max-height: 60px;"
                    alt="">
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
            @click="onUpdatePublishingHouse"
          >
            Сохранить
          </button>
        </div>
      </div>
    </div>
</div>


<!--модальное окно картинки-->
<div class="modal fade" id="showPictureModal" tabindex="-1">
    <div class="modal-dialog">
      <div class="modal-content">
        <div class="modal-header">
          <h1 class="modal-title fs-5" id="exampleModalLabel">
            картинка
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
            <div v-show="publishingHousePeactureShow"><img :src="publishingHousePeactureShow" ></div>
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
          
        </div>
      </div>
    </div>
</div>



  <!-- Модальное окно для статистики -->
  <div class="modal fade" id="statsModal" tabindex="-1" role="dialog">
        <div class="modal-dialog" role="document">
            <div class="modal-content">
                <div class="modal-header">
                    <h5 class="modal-title">Статистика Издания</h5>
                </div>
                <div class="modal-body">
                    <p>Количество Изданий: {{ stats.count }}</p>
                    <p>Максимальный год основания: {{ stats.max }}</p>
                    <p>Минимальный год основания: {{ stats.min }}</p>
                    <p>Средний год основания: {{ stats.avg }}</p>
                </div>
                <div class="modal-footer">
                    <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Закрыть</button>
                </div>
            </div>
        </div>
  </div>


</template>


<style lang="scss" scoped>

.publishingHouse-item {
  padding: 0.5rem;
  margin: 0.5rem 0;
  border: 1px solid silver;
  border-radius: 8px;
  display: flex;
  align-items: center;
  gap: 1rem;
}
.publishingHouse-info{
  display: flex;
  flex-wrap: wrap;
  gap:0.5rem;
  flex: 1;
}
.publishingHouse-image{
  flex: none;
  margin-right: 0.5rem;
}
.publishingHouse-actions{
  flex: none;
  display: flex;
  gap: 0.5rem;
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
