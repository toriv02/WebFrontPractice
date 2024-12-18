import { createRouter, createWebHistory } from 'vue-router'
import BooksView from '../views/BooksView.vue';
import FormsView from '../views/FormsView.vue';
import KindsView from '../views/KindsView.vue';
import AuthorsView from '../views/AuthorsView.vue';
import PublishingHousesViewew from '../views/PublishingHousesView.vue';
import MatterssView from '../views/MattersView.vue';
import LoginView from '@/views/LoginView.vue';
import ErrorView from '@/views/ErrorView.vue';

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: "/",
      name: "BooksView",
      component: BooksView
    },
    {
      path: "/kinds",
      name: "KindsView",
      component: KindsView
    },
    {
      path: "/authors",
      name: "AuthorsView",
      component: AuthorsView
    },
    {
      path: "/forms",
      name: "FormsView",
      component: FormsView
    },
    {
      path: "/publishinghouses",
      name: "PublishingHousesView",
      component: PublishingHousesViewew
    },
    {
      path: "/matters",
      name: "MatterssView",
      component: MatterssView
    },
    {
      path: "/login",
      name: "LoginView",
      component: LoginView
    },
    {
      path: '/:pathMatch(.*)*', // this is a catch all route
      name: 'not-found',
      component: ErrorView
    }
  ]
})

export default router
