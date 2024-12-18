<script setup>
import { storeToRefs } from 'pinia';
import useUserStore from '@/stores/userStore';
import axios from 'axios';
import { useRouter } from 'vue-router';
import { ref } from 'vue';
import Cookies from 'js-cookie';
import { toast } from 'vue3-toastify';

const username = ref("");
const pas = ref("");
const otp = ref("");
const router = useRouter();
const showOtpInput = ref(false);
const userStore = useUserStore();
const { isAuthenticated } = storeToRefs(userStore);

let optKey = ref('');

async function login() {
    const csrfToken = Cookies.get('csrftoken');
    try {
        // 1. Аутентификация по логину и паролю
        const response = await axios.post("/api/user/login/", {
            user: username.value,
            password: pas.value
        }, {
            headers: {
                'X-CSRFToken': csrfToken
            }
        });

        if (response.status===200) {
            toast("Вы успешно прошли базовую аутентификацию");
            await getOptKey();
            showOtpInput.value = true;
        } else {
             toast("Неверные имя пользователя или пароль");
        }

    } catch (error) {
        console.error("Ошибка входа:", error);
        toast("Ошибка входа");
    }
}

async function getOptKey() {
    try {
        const response = await axios.get("/api/user/get-opt-key/");
        if (response.data.opt_key) {
            optKey.value = response.data.opt_key;
            toast("Теперь нужно ввести OTP");
        }
    } catch (e) {
        console.error(e);
        router.push("/");
        toast("Ошибка при получении opt key");
    }
}

async function sendOtp() {
    const csrfToken = Cookies.get('csrftoken');
    try {
        // 2. Проверка OTP
        const response = await axios.post("/api/user/otp-login/", {
            key: otp.value
        }, {
            headers: {
                'X-CSRFToken': csrfToken
            }
        });
        if (response.data.success) {
            toast("OTP прошла проверку, вы успешно вошли");
            // 3. Устанавливаем пользователя
            await userStore.fetchUser();
            router.push("/");

        } else {
           toast("Неверный OTP");
        }

    } catch (e) {
        console.error("Ошибка при отправке OTP", e);
        toast("Ошибка при отправке OTP");
    }
}
</script>

<template>
    <section class="vh-75 gradient-custom">
     <div class="container py-5 h-100">
         <div class="row d-flex justify-content-center align-items-center h-100">
             <div class="col-10 col-md-6 col-lg-5 col-xl-4">
                 <div class="card custom-bg text-white" style="border-radius: 1rem;">
                     <div class="card-body p-4 text-center">
                         <div class="mb-md-4 mt-md-2 pb-3">
                             <h2 class="fw-bold mb-2 text-uppercase">Login</h2>
                             <div class="form-outline form-white mb-3">
                                 <input v-model="username" id="Login" class="form-control form-control-sm" />
                                 <label class="form-label" for="Login">Username</label>
                             </div>
                             <div class="form-outline form-white mb-3">
                                 <input type="password" v-model="pas" id="typePasswordX"
                                     class="form-control form-control-sm" />
                                 <label class="form-label" for="typePasswordX">Password</label>
                             </div>
                              <div v-if="showOtpInput" class="form-outline form-white mb-3">
                                 <input type="text" v-model="otp" id="otpInput"
                                     class="form-control form-control-sm" />
                                 <label class="form-label" for="otpInput">OTP</label>
                             </div>
                             <button @click="login" class="btn btn-outline-light btn-sm px-4"
                                 type="submit">Login</button>
                         </div>
                     </div>
                 </div>
             </div>
         </div>
     </div>
 </section>
 <ToastContainer/>
</template>

<style>
.vh-75 {
   height: 75vh;
 }

 .custom-bg {
   background-color: #343a40;
   border-radius: 1rem;
   height: 300px;
 }

 .card-body {
   padding: 1.5rem;
 }

 .btn-outline-light {
   color: #ffff;
   border-color: #ffff;
 }

 .btn-outline-light:hover {
   background-color: lightslategrey;
   color: #ffff;
 }
</style>