<script setup>
import { ref, onMounted } from "vue";
import { useRoute } from "vue-router";
import { Toast } from "bootstrap";

const getUserIdFromToken = () => {
  const token = localStorage.getItem("jwt_token");

  if (!token) {
    throw new Error("Token nije pronađen.");
  }

  try {
    const decodedToken = JSON.parse(atob(token.split(".")[1]));

    if (!decodedToken.id) {
      throw new Error("ID korisnika nije pronađen u tokenu.");
    }

    return decodedToken.id;
  } catch (error) {
    throw new Error("Greška pri dekodiranju JWT tokena: " + error.message);
  }
};

const route = useRoute();

const korisnik = ref({
  naziv: "",
  iznos: "",
  type: "",
  id: "",
});

const toastElement = ref(null);

const fetchKorisnikData = async () => {
  const korisnikId = route.params.userId;
  const token = localStorage.getItem("jwt_token");

  if (!token) {
    console.error("Token nije pronađen.");
    return;
  }

  try {
    const userIdFromToken = getUserIdFromToken();

    const response = await fetch(`/api/korisnik_pregled/${korisnikId}`, {
      method: "GET",
      headers: {
        Authorization: `Bearer ${token}`,
      },
    });

    const data = await response.json();

    if (response.ok) {
      korisnik.value = data;
      const toast = new Toast(toastElement.value);
      toast.show();
    } else {
      console.error("Greška: ", data.error);
    }
  } catch (error) {
    console.error("Greška pri učitavanju korisnika:", error);
  }
};

onMounted(() => {
  fetchKorisnikData();
});
</script>

<template>
  <div class="container col-lg-6">
    <h3>Pregled transakcije</h3>

    <table class="table">
      <thead>
        <tr>
          <th>Naziv</th>
          <td>{{ korisnik.naziv }}</td>
        </tr>
      </thead>
      <tbody>
        <tr>
          <th>Iznos</th>
          <td>
            <span v-if="korisnik.type === 'prihod'">+{{ korisnik.iznos }}</span>
            <span v-else>{{ korisnik.iznos }}</span>
          </td>
        </tr>
        <tr>
          <th>Tip</th>
          <td>{{ korisnik.type }}</td>
        </tr>
      </tbody>
    </table>

    <router-link :to="`/korisnici/edit/${korisnik.id}`" class="btn btn-primary">
      Izmeni
    </router-link>
  </div>

  <div class="toast-container position-fixed top-0 end-0 p-3">
    <div
      id="successToast"
      class="toast align-items-center text-bg-success border-0"
      role="alert"
      aria-live="assertive"
      aria-atomic="true"
      ref="toastElement"
    >
      <div class="d-flex">
        <div class="toast-body">Podaci o korisniku uspešno učitani!</div>
        <button
          type="button"
          class="btn-close btn-close-white me-2 m-auto"
          data-bs-dismiss="toast"
          aria-label="Close"
        ></button>
      </div>
    </div>
  </div>
</template>
