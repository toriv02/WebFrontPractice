<script setup>
import {computed, onBeforeMount, ref} from 'vue';
import axios from 'axios';
import _ from 'lodash';
import Cookies from 'js-cookie';
import { storeToRefs } from 'pinia';
import useUserStore from '../stores/userStore';

const books = ref ([])
const kinds = ref ([])
const authors = ref ([])
const forms = ref ([])
const publishingHouses = ref ([])
const matters = ref ([])


const bookToAdd=ref({})
const bookToEdit=ref({})

const stats = ref({})


const userStore = useUserStore();
const { isSuperuser, users } = storeToRefs(userStore);

const filters = ref({
    title: "",
    year_of_publication: "",
    author_FK: "",
    matter_FK: "",
    form_FK: "",
    kind_FK: "",
    publishingHouse_FK: "",
    user_id: ""
});

onBeforeMount(() => {
  axios.defaults.headers.common['X-CSRFToken'] = Cookies.get("csrftoken");
})


async function fetchBooks(){
  const r =await axios.get("/api/books/");
  console.log(r.data);
  books.value=r.data;
}
async function fetchKinds(){
  const r =await axios.get("/api/kinds/");
  console.log(r.data);
  kinds.value=r.data;
}
async function fetchAuthors(){
  const r =await axios.get("/api/authors/");
  console.log(r.data);
  authors.value=r.data;
}

async function fetchForms(){
  const r =await axios.get("/api/forms/");
  console.log(r.data);
  forms.value=r.data;
}
async function fetchPublishingHouses(){
  const r =await axios.get("/api/publishinghouses/");
  console.log(r.data);
  publishingHouses.value=r.data;
}

async function fetchMatters(){
  const r =await axios.get("/api/matters/");
  console.log(r.data);
  matters.value=r.data;
}

onBeforeMount(async ()=>{
  await userStore.fetchUser();
    if (isSuperuser.value) {
        await userStore.fetchUsers();
    }
  await fetchBooks()
  await fetchKinds()
  await fetchAuthors()
  await fetchForms()
  await fetchPublishingHouses()
  await fetchMatters()
})

async function onBookAdd() {
  await axios.post("/api/books/", {
    ...bookToAdd.value,
  });
  await fetchBooks();
}
async function onRemoveClick(book) {
  await axios.delete(`/api/books/${book.id}/`);
  await fetchBooks(); // переподтягиваю
}

async function onBookEditClick(book) {
  bookToEdit.value = { 
    ...book, 
    author_FK_id: book.author_FK.id,
    matter_FK_id: book.matter_FK.id,
    form_FK_id: book.form_FK.id,
    kind_FK_id: book.kind_FK.id,
    publishingHouse_FK_id: book.publishingHouse_FK.id,
  };

}
async function onUpdateBook() {
  await axios.put(`/api/books/${bookToEdit.value.id}/`, {
    ...bookToEdit.value,
  });
  await fetchBooks();
}


async function fetchStats() {
    const r = await axios.get("/api/books/stats/");
    stats.value = r.data;
}

async function exportToExcel() {
    const response = await axios.get("/api/books/export-excel/", { responseType: "blob" });
    const url = window.URL.createObjectURL(new Blob([response.data]));
    const link = document.createElement("a");
    link.href = url;
    link.setAttribute("download", "books.xlsx");
    document.body.appendChild(link);
    link.click();
}

async function exportToWord() {
    const response = await axios.get("/api/books/export-word/", { responseType: "blob" });
    const url = window.URL.createObjectURL(new Blob([response.data]));
    const link = document.createElement("a");
    link.href = url;
    link.setAttribute("download", "books.docx");
    document.body.appendChild(link);
    link.click();
}




const filteredBooks = computed(() => {
    return books.value.filter(book => {
      const titleMatch = !filters.value.title || (book.title && book.title.toLowerCase().includes(filters.value.title.toLowerCase()));
      const yearMatch = !filters.value.year_of_publication || (book.year_of_publication && book.year_of_publication.toString().includes(filters.value.year_of_publication));
      const authorMatch = !filters.value.author_FK || (book.author_FK && book.author_FK.id && book.author_FK.id.toString().includes(filters.value.author_FK));
      const matterMatch = !filters.value.matter_FK || (book.matter_FK && book.matter_FK.id && book.matter_FK.id.toString().includes(filters.value.matter_FK));
      const formMatch = !filters.value.form_FK || (book.form_FK && book.form_FK.id && book.form_FK.id.toString().includes(filters.value.form_FK));
      const kindMatch = !filters.value.kind_FK || (book.kind_FK && book.kind_FK.id && book.kind_FK.id.toString().includes(filters.value.kind_FK));
      const publishingHouseMatch = !filters.value.publishingHouse_FK || (book.publishingHouse_FK && book.publishingHouse_FK.id && book.publishingHouse_FK.id.toString().includes(filters.value.publishingHouse_FK));
      const userMatch = !filters.value.user_id || (book.user_id && book.user_id.toString().includes(filters.value.user_id));
      return titleMatch && yearMatch && authorMatch && matterMatch  && formMatch && kindMatch && publishingHouseMatch && userMatch ;
    });
});

function resetFilters() {
    filters.value = {
      title: "",
      year_of_publication: "",
      author_FK: "",
      matter_FK: "",
      form_FK: "",
      kind_FK: "",
      publishingHouse_FK: "",
      user_id: ""
    };
}



async function copyText(text) {
   try {
        await navigator.clipboard.writeText(text);

    } catch (err) {}
}


 function copyBookInfo(item) {
     const bookInfo =  `${item.title} - ${item.year_of_publication},  ${item.kind_FK?.name || ""} ${item.matter_FK?.title || ""}, ${item.form_FK?.name || ""} (${item.publishingHouse_FK?.name || ""}) - ${item.author_FK?.name?.[0] || ""}${item.author_FK?.surname?.[0] || ""}. ${item.author_FK?.patronymic || ""}`;
       copyText(bookInfo);
 }

</script>

<template>
<form @submit.prevent.stop="onBookAdd">
  <div class="row">
    <div class="col">
      <div class="form-floating">
        <input
          type="text"
          class="form-control"
          v-model="bookToAdd.title"
          required
        />
        <label for="floatingInput">Заголовок</label>
      </div>
    </div>

    <div class="col">
      <div class="form-floating">
        <input
          type="text"
          class="form-control"
          v-model="bookToAdd.year_of_publication"
          required
        />
        <label for="floatingInput">Год публикации</label>
      </div>
    </div>

    <div class="col-auto">
      <div class="form-floating">
        <select class="form-select" v-model="bookToAdd.kind_FK_id" required>
          <option :value="k.id" v-for="k in kinds" :key="k.id">{{ k.name }}</option>
        </select>
        <label for="floatingInput">Жанр</label>
      </div>
    </div>
    
    <div class="col-auto">
      <div class="form-floating">
        <select class="form-select" v-model="bookToAdd.author_FK_id" required>
          <option :value="a.id" v-for="a in authors" :key="a.id">{{ a.name[0]+'.'+a.surname[0]+'. '+ a.patronymic }}</option>
        </select>
        <label for="floatingInput">Автор</label>
      </div>
    </div>

    <div class="col-auto">
      <div class="form-floating">
        <select class="form-select" v-model="bookToAdd.form_FK_id" required>
          <option :value="fr.id" v-for="fr in forms" :key="fr.id">{{ fr.name }}</option>
        </select>
        <label for="floatingInput">Форма</label>
      </div>
    </div>

    <div class="col-auto">
      <div class="form-floating">
        <select class="form-select" v-model="bookToAdd.publishingHouse_FK_id" required>
          <option :value="p.id" v-for="p in publishingHouses" :key="p.id">{{ p.name }}</option>
        </select>
        <label for="floatingInput">Издание</label>
      </div>
    </div>

    <div class="col-auto">
      <div class="form-floating">
        <select class="form-select" v-model="bookToAdd.matter_FK_id" required>
          <option :value="m.id" v-for="m in matters" :key="m.id">{{ m.title }}</option>
        </select>
        <label for="floatingInput">Вид</label>
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
  <button class="btn btn-secondary me-2" @click="exportToExcel">
    Сохранить как Excel
  </button>

  <button class="btn btn-secondary me-2" @click="exportToWord">
    Сохранить как Word
  </button>

  <button class="btn btn-info" @click="fetchStats()" data-bs-toggle="modal"
  data-bs-target="#statsModal">Статистика</button>
</div>

<h4>Фильтрация</h4>
<div class="row mb-3 mt-3">
  <div class="col">
    <input type="text" class="form-control" placeholder="Название" v-model="filters.title">
  </div>
  <div class="col">
    <input type="text" class="form-control" placeholder="Год публикации" v-model="filters.year_of_publication">
  </div>
    <div class="col">
      <select class="form-select" v-model="filters.author_FK">
        <option value="">Авторы</option>
        <option v-for="author in authors" :key="author.id" :value="author.id">{{ author.name }}</option>
      </select>
    </div>
    <div class="col">
      <select class="form-select" v-model="filters.matter_FK">
        <option value="">Рода</option>
        <option v-for="matter in matters" :key="matter.id" :value="matter.id">{{ matter.title }}</option>
      </select>
    </div>
    <div class="col">
       <select class="form-select" v-model="filters.form_FK">
        <option value="">Формы</option>
        <option v-for="form in forms" :key="form.id" :value="form.id">{{ form.name }}</option>
      </select>
    </div>
      <div class="col">
       <select class="form-select" v-model="filters.kind_FK">
        <option value="">Виды</option>
        <option v-for="kind in kinds" :key="kind.id" :value="kind.id">{{ kind.name }}</option>
      </select>
    </div>
    <div class="col">
      <select class="form-select" v-model="filters.publishingHouse_FK">
         <option value="">Издательства</option>
        <option v-for="publishingHouse in publishingHouses" :key="publishingHouse.id" :value="publishingHouse.id">{{ publishingHouse.name }}</option>
      </select>
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


<div v-for="item in filteredBooks"  class="book-item">
  <div class="book-info">
    <span>{{ item.title  }}</span> 
    <span>{{ item.year_of_publication }}</span>   
    <span>{{ item.kind_FK?.name || "" }}</span>
    <span>{{ item.matter_FK?.title || "" }}</span>
    <span>{{ item.form_FK?.name || "" }}</span>
    <span>{{ item.publishingHouse_FK?.name || "" }}</span>
    <span>{{ item.author_FK?.name?.[0] || "" }}{{ item.author_FK?.surname?.[0] || "" }}. {{item.author_FK?.patronymic || ""}}</span>
  </div>  
  <div class="book-actions">
    <button
        class="btn btn-success"
        @click="onBookEditClick(item)"
        data-bs-toggle="modal"
        data-bs-target="#editBookModal"
    >
        <i class="bi bi-pen-fill"></i>
      </button>
      <button class="btn btn-danger" @click="onRemoveClick(item)">
        <i class="bi bi-x"></i>
      </button>
      <button class="btn btn-info" @click="copyBookInfo(item)">
        <i class="bi bi-copy"></i>
      </button>
  </div>
</div>


<!--модальное окно для редактирования киги-->
<div class="modal fade" id="editBookModal" tabindex="-1">
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
                  v-model="bookToEdit.title"
                />
                <label for="floatingInput">Название</label>
              </div>
            </div>

            <div class="col">
              <div class="form-floating">
                <input
                  type="text"
                  class="form-control"
                  v-model="bookToEdit.year_of_publication"
                />
                <label for="floatingInput">Год публикации</label>
              </div>
            </div>
            
            <div class="col-auto">
              <div class="form-floating">
                <select class="form-select" v-model="bookToEdit.author_FK_id">
                  <option :value="a.id" v-for="a in authors" :key="a.id">
                    {{ a.name[0]+'.'+a.surname[0]+'. '+ a.patronymic }}
                  </option>
                </select>
                <label for="floatingInput">Автор</label>
              </div>
            </div>
            
            <div class="col-auto">
              <div class="form-floating">
                <select class="form-select" v-model="bookToEdit.kind_FK_id">
                  <option :value="k.id" v-for="k in kinds" :key="k.id">
                    {{ k.name }}
                  </option>
                </select>
                <label for="floatingInput">Жанр</label>
              </div>
            </div>
            
            <div class="col-auto">
              <div class="form-floating">
                <select class="form-select" v-model="bookToEdit.form_FK_id">
                  <option :value="fr.id" v-for="fr in forms" :key="fr.id">
                    {{ fr.name }}
                  </option>
                </select>
                <label for="floatingInput">Форма</label>
              </div>
            </div>

            <div class="col-auto">
              <div class="form-floating">
                <select class="form-select" v-model="bookToEdit.publishingHouse_FK_id">
                  <option :value="p.id" v-for="p in publishingHouses" :key="p.id">
                    {{ p.name }}
                  </option>
                </select>
                <label for="floatingInput">Издание</label>
              </div>
            </div>

            <div class="col-auto">
              <div class="form-floating">
                <select class="form-select" v-model="bookToEdit.matter_FK_id">
                  <option :value="m.id" v-for="m in matters" :key="m.id">
                    {{ m.title }}
                  </option>
                </select>
                <label for="floatingInput">Вид</label>
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
            @click="onUpdateBook"
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
                    <h5 class="modal-title">Статистика книг</h5>
                </div>
                <div class="modal-body">
                    <p>Количество книг: {{ stats.count }}</p>
                    <p>Максимальный год выпсука: {{ stats.max }}</p>
                    <p>Минимальный год выпсука: {{ stats.min }}</p>
                    <p>Средний год выпсука: {{ stats.avg }}</p>
                </div>
                <div class="modal-footer">
                    <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Закрыть</button>
                </div>
            </div>
        </div>
    </div>

</template>


<style lang="scss" scoped>
.book-item {
  padding: 0.5rem;
  margin: 0.5rem 0;
  border: 1px solid silver;
  border-radius: 8px;
  display: flex;
  align-items: center;
  gap: 1rem;
}
.book-info{
  display: flex;
  flex-wrap: wrap;
  gap:0.5rem;
  flex: 1;
}
.book-actions{
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
