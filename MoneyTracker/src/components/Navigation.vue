<script setup>
import { ref } from "vue";
import { useRouter } from "vue-router";
import Swal from "sweetalert2";

const role = ref(localStorage.getItem("role"));
const router = useRouter();

const logout = () => {
  Swal.fire({
    title: "Da li ste sigurni?",
    text: "Odjavljivanjem ćete napustiti sesiju.",
    icon: "warning",
    showCancelButton: true,
    confirmButtonColor: "#3085d6",
    cancelButtonColor: "#d33",
    confirmButtonText: "Da, odjavi me",
    cancelButtonText: "Odustani",
  }).then((result) => {
    if (result.isConfirmed) {
      localStorage.clear();
      router.push("/login");
    }
  });
};
</script>

<template>
  <nav
    class="navbar navbar-expand-lg navbar-light"
    style="background-color: #343a40"
  >
    <img
      src="../assets/konacanlogo2.png"
      alt="Finance Logo"
      class="logo img-fluid"
    />
    <button
      class="navbar-toggler"
      type="button"
      data-bs-toggle="collapse"
      data-bs-target="#navbarSupportedContent"
      aria-controls="navbarSupportedContent"
      aria-expanded="false"
      aria-label="Toggle navigation"
    >
      <span class="navbar-toggler-icon"></span>
    </button>

    <div class="collapse navbar-collapse" id="navbarSupportedContent">
      <ul class="navbar-nav me-auto mb-2 mb-lg-0">
        <li class="nav-item">
          <router-link
            :to="`/korisnici`"
            role="button"
            class="nav-link text-white"
            >Kontrolna tabla</router-link
          >
        </li>
        <li class="nav-item">
          <router-link :to="`/budzet`" role="button" class="nav-link text-white"
            >Budžet</router-link
          >
        </li>
        <li v-if="role === 'admin'" class="nav-item">
          <router-link to="/users" class="nav-link text-white"
            >Svi korisnici</router-link
          >
        </li>
      </ul>
      <form class="d-flex">
        <button
          class="btn"
          style="background-color: #dc3545"
          @click.prevent="logout"
        >
          <i class="fa-solid fa-right-from-bracket rounded"></i> Izlaz
        </button>
      </form>
    </div>
  </nav>
</template>

<style>
.navbar-nav .nav-link:hover {
  color: #01a2e9 !important;
  background-color: rgba(0, 162, 233, 0.1);
}
</style>
