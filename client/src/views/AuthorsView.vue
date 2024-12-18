<script setup>
import {computed, onBeforeMount, ref} from 'vue';
import axios from 'axios';
import Cookies from 'js-cookie';
import { storeToRefs } from 'pinia';
import useUserStore from '../stores/userStore';



const authors = ref ([])


const authorToAdd=ref({})
const authorToEdit=ref({})

const authorPictureRef=ref('')
const authorAddImageUrl=ref('')

const authorPeactureShow=ref('')

const stats=ref({})

const authorEditImageURL=ref('')
const authorPictureRefEdit=ref('')


const userStore = useUserStore();
const { isSuperuser, users } = storeToRefs(userStore);

const filters = ref({
    name: "",
    surname: "",
    patronymic: "",
    years_of_life: "",
    user_id: ""
});

onBeforeMount(() => {
  axios.defaults.headers.common['X-CSRFToken'] = Cookies.get("csrftoken");
})


async function fetchAuthors(){
  const r =await axios.get("/api/authors/");
  console.log(r.data);
  authors.value=r.data;
}


onBeforeMount(async ()=>{
  await fetchAuthors()
})

async function onAuthorAdd() {
  const formData=new FormData();
  
  //вытаскиваем выбранный файл с формы
  if (authorPictureRef.value && authorPictureRef.value.files.length > 0) {
    formData.append('picture',authorPictureRef.value.files[0]);
  }
  //явно привязываем поля
  formData.set('name',authorToAdd.value.name)
  formData.set('surname',authorToAdd.value.surname)
  formData.set('patronymic',authorToAdd.value.patronymic)
  formData.set('years_of_life',authorToAdd.value.years_of_life)

  //указываем что тправляем данные с файлом
  await axios.post("/api/authors/", formData,{
    headers:{
      'Content-type': 'multipart/form-data'
    }
  });
  await fetchAuthors(); 
}

async function onRemoveClick(author) {
  await axios.delete(`/api/authors/${author.id}/`);
  await fetchAuthors(); // переподтягиваю
}

async function onAuthorEditClick(author) {
  authorToEdit.value = { ...author };
  authorEditImageURL.value=author.picture;
}

async function onUpdateAuthor() {
  const formData=new FormData();
  
  //вытаскиваем выбранный файл с формы
  if (authorPictureRefEdit.value && authorPictureRefEdit.value.files.length > 0) {
    formData.append('picture',authorPictureRefEdit.value.files[0]);
  }
  //явно привязываем поля
  formData.set('name',authorToEdit.value.name)
  formData.set('surname',authorToEdit.value.surname)
  formData.set('patronymic',authorToEdit.value.patronymic)
  formData.set('years_of_life',authorToEdit.value.years_of_life)

  //указываем что тправляем данные с файлом
  await axios.put(`/api/authors/${authorToEdit.value.id}/`, formData,{
    headers:{
      'Content-type': 'multipart/form-data'
    }
  });
  await fetchAuthors(); 
}

async function  authorAddPictureChange() {
  if (authorPictureRef.value && authorPictureRef.value.files.length > 0) {
    authorAddImageUrl.value=URL.createObjectURL(authorPictureRef.value.files[0])
  }
}

async function showPicture(picture) {
  authorPeactureShow.value=picture
}


async function authorsEditPictureChange(){
  if (authorPictureRefEdit.value && authorPictureRefEdit.value.files.length > 0) {
        authorEditImageURL.value = URL.createObjectURL(authorPictureRefEdit.value.files[0]);
    }
}

async function fetchStats() {
    const r = await axios.get("/api/authors/stats/");
    stats.value = r.data;
}


const filteredAuthors = computed(() => {
    return authors.value.filter(author=> {
      const nameMatch = !filters.value.name || (author.name && author.name.toLowerCase().includes(filters.value.name.toLowerCase()));
      const surnameMatch = !filters.value.surname || (author.surname && author.surname.toLowerCase().includes(filters.value.surname.toLowerCase()));
      const patronymicMatch = !filters.value.patronymic || (author.patronymic && author.patronymic.toLowerCase().includes(filters.value.patronymic.toLowerCase()));
      const yearsMatch = !filters.value.years_of_life || (author.years_of_life && author.years_of_life.toString().includes(filters.value.years_of_life));
      const userMatch = !filters.value.user_id || (author.user_id && author.user_id.toString().includes(filters.value.user_id));

      return nameMatch && surnameMatch && patronymicMatch && yearsMatch && userMatch;
    });
});

function resetFilters() {
    filters.value = {
      name: "",
      surname: "",
      patronymic: "",
      years_of_life: "",
      user_id: ""
    };
}

</script>




<template>
<form @submit.prevent.stop="onAuthorAdd">
  <div class="row">
    <div class="col">
      <div class="form-floating">
        <input
          type="text"
          class="form-control"
          v-model="authorToAdd.name"
          required
        />
        <label for="floatingInput">Имя</label>
      </div>
    </div>

    <div class="col">
      <div class="form-floating">
        <input
          type="text"
          class="form-control"
          v-model="authorToAdd.surname"
          required
        />
        <label for="floatingInput">Фамилия</label>
      </div>
    </div>

    <div class="col">
      <div class="form-floating">
        <input
          type="text"
          class="form-control"
          v-model="authorToAdd.patronymic"
          required
        />
        <label for="floatingInput">Отчество</label>
      </div>
    </div>

    <div class="col">
      <div class="form-floating">
        <input
          type="text"
          class="form-control"
          v-model="authorToAdd.years_of_life"
          required
        />
        <label for="floatingInput">Годы Жизни</label>
      </div>
    </div>
    
    <div class="col-autho">
      <input class="form-control" type="file" ref="authorPictureRef" @change="authorAddPictureChange">
    </div>

    <div class="col-autho">
      <img :src="authorAddImageUrl" style="max-height: 60px;" alt="">
    </div>

    <div class="col-auto">
      <button class="btn btn-primary">
        Добавить
      </button>
    </div>
  </div>
</form>

<div class="col-auto d-flex justify-content-end mt-2">
  <button class="btn btn-info" @click="fetchStats()" data-bs-toggle="modal"
  data-bs-target="#statsModal">Статистика</button>
</div>

<h4>Фильтрация</h4>
<div class="row mb-3 mt-3">
  <div class="col">
    <input type="text" class="form-control" placeholder="Имя" v-model="filters.name">
  </div>
  <div class="col">
    <input type="text" class="form-control" placeholder="Фамилия" v-model="filters.surname">
  </div>
  <div class="col">
    <input type="text" class="form-control" placeholder="Отчество" v-model="filters.patronymic">
  </div>
    <div class="col">
    <input type="text" class="form-control" placeholder="Годы жизни" v-model="filters.years_of_life">
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



<div v-for="item in filteredAuthors" class="author-item">
  <div class="author-info">
    <span>{{ item.name }}</span>
    <span>{{ item.surname }}</span>
    <span>{{ item.patronymic }}</span>
    <span>{{ item.years_of_life }}</span>
  </div>
  <div v-show="item.picture" class="author-image">
      <img :src="item.picture" style="max-height: 60px;"
            @click="showPicture(item.picture)"
            data-bs-toggle="modal"
            data-bs-target="#showPictureModal"
      >
  </div>
  <div class="author-actions">
      <button
          class="btn btn-success"
          @click="onAuthorEditClick(item)"
          data-bs-toggle="modal"
          data-bs-target="#editAuthorModal"
      >
          <i class="bi bi-pen-fill"></i>
      </button>
      <button class="btn btn-danger" @click="onRemoveClick(item)">
          <i class="bi bi-x"></i>
      </button>
  </div>
</div>




<!--модальное окно автора-->
<div class="modal fade" id="editAuthorModal" tabindex="-1">
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
                  v-model="authorToEdit.name"
                  required
                />
                <label for="floatingInput">Имя</label>
              </div>
            </div>

            <div class="col">
              <div class="form-floating">
                <input
                  type="text"
                  class="form-control"
                  v-model="authorToEdit.surname"
                  required
                />
                <label for="floatingInput">Фамилия</label>
              </div>
            </div>

            <div class="col">
              <div class="form-floating">
                <input
                  type="text"
                  class="form-control"
                  v-model="authorToEdit.patronymic"
                  required
                />
                <label for="floatingInput">Отчество</label>
              </div>
            </div>

            <div class="col">
              <div class="form-floating">
                <input
                  type="text"
                  class="form-control"
                  v-model="authorToEdit.years_of_life"
                  required
                />
                <label for="floatingInput">Годы Жизни</label>
              </div>
            </div>
          </div>
          <div class="row p-1">
                  <div class="col-6">
                    <input class="form-control" type="file" ref="authorPictureRefEdit"
                         @change="authorsEditPictureChange">
                  </div>
                  <div class="col-auto">
                    <img v-if="authorEditImageURL" :src="authorEditImageURL" style="max-height: 60px;"
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
            @click="onUpdateAuthor"
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
            <div v-show="authorPeactureShow"><img :src="authorPeactureShow" ></div>
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
                    <h5 class="modal-title">Статистика Автроров</h5>
                </div>
                <div class="modal-body">
                    <p>Количество Автроров: {{ stats.count }}</p>
                    <p>Максимальный ID Автрора: {{ stats.max }}</p>
                    <p>Минимальный ID Автрора: {{ stats.min }}</p>
                </div>
                <div class="modal-footer">
                    <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Закрыть</button>
                </div>
            </div>
        </div>
  </div>

</template>


<style lang="scss" scoped>
.author-item {
  padding: 0.5rem;
  margin: 0.5rem 0;
  border: 1px solid silver;
  border-radius: 8px;
  display: flex;
  align-items: center;
  gap: 1rem;
}
.author-info{
  display: flex;
  flex-wrap: wrap;
  gap:0.5rem;
  flex: 1;
}
.author-image{
  flex: none;
  margin-right: 0.5rem;
}
.author-actions{
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
