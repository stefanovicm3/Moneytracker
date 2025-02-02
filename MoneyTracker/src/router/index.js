import { createRouter, createWebHistory } from "vue-router";
import Korisnici from "@/views/Korisnici.vue";
import DodajNovi from "@/views/Dodaj-novi.vue";
import KorisnikIzmena from "@/views/Korisnik-izmena.vue";
import KorisnikPregled from "@/views/Korisnik-pregled.vue";
import Login from "@/views/Login.vue";
import BudzetModel from "../views/Budzet-model.vue";
import Budzet from "../views/Budzet.vue";
import DodajBudzet from "../views/Dodaj-budzet.vue";
import EditUser from "../views/EditUser.vue";
import IzmeniBudzet from "../views/Izmeni-budzet.vue";
import IzmeniPotrosnju from "../views/Izmeni-potrosnju.vue";
import Register from "../views/Register.vue";
import Users from "../views/Users.vue";
import AddUser from "../views/AddUser.vue";
import ForgotPassword from "@/views/Forgot-password.vue";

const routes = [
  { path: "/", redirect: "/login" },
  { path: "/korisnici", name: "Korisnici", component: Korisnici },
  { path: "/korisnici/dodaj-novi", name: "DodajNovi", component: DodajNovi },
  {
    path: "/korisnici/pregled/:userId",
    name: "KorisnikPregled",
    component: KorisnikPregled,
  },
  {
    path: "/korisnici/edit/:userId",
    name: "KorisnikIzmena",
    component: KorisnikIzmena,
  },
  { path: "/login", name: "Login", component: Login },
  { path: "/budzet", name: "Budzet", component: Budzet },
  { path: "/budzet-model", name: "BudzetModel", component: BudzetModel },
  { path: "/budzet/dodaj", name: "DodajBudzet", component: DodajBudzet },
  {
    path: "/izmeni-budzet/:budgetId",
    name: "IzmeniBudzet",
    component: IzmeniBudzet,
  },
  {
    path: "/izmeni-potrosnju",
    name: "IzmeniPotrosnju",
    component: IzmeniPotrosnju,
  },
  { path: "/register", name: "Register", component: Register },
  { path: "/users", name: "Users", component: Users },
  { path: "/edit-user/:userId", name: "EditUser", component: EditUser },
  {
    path: "/add-user",
    name: "AddUser",
    component: AddUser,
  },
  {
    path: "/forgot-password",
    name: "ForgotPassword",
    component: ForgotPassword,
  },
];

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes,
});

// Provera autentifikacije pre pristupa rutama
router.beforeEach((to, from, next) => {
  const token = localStorage.getItem("jwt_token");
  const publicRoutes = ["Login", "Register", "ForgotPassword"]; // Dozvoljene rute

  if (!token && !publicRoutes.includes(to.name)) {
    next({ name: "Login" });
  } else {
    next();
  }
});

export default router;
