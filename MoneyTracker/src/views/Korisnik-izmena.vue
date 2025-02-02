<script setup>
import { ref, onMounted } from "vue";
import { useRoute, useRouter } from "vue-router";
import axios from "axios";
import { Toast } from "bootstrap";

const route = useRoute();
const router = useRouter();

const korisnik = ref({
  naziv: "",
  iznos: "",
  type: "",
});

const userId = ref(null); 

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

const fetchKorisnikData = async () => {
  try {
    const userId = route.params.userId;

    const response = await axios.get(`/api/korisnik_izmena/${userId}/preuzmi`, {
      headers: {
        Authorization: `Bearer ${localStorage.getItem("jwt_token")}`,
      },
    });

    korisnik.value = response.data; 
  } catch (error) {
    console.error("Greška pri učitavanju korisnika:", error);
    alert("Došlo je do greške prilikom preuzimanja podataka.");
  }
};

const toastElement = ref(null);

const updateKorisnikData = async () => {
  const token = localStorage.getItem("jwt_token");
  if (!token) {
    alert("Niste prijavljeni. Molimo prijavite se ponovo.");
    return;
  }

  const userId = route.params.userId;
  const updatedData = {
    naziv: korisnik.value.naziv,
    iznos: korisnik.value.iznos,
    type: korisnik.value.type,
  };

  try {
    const response = await axios.post(
      `/api/korisnik_izmena/${userId}/izmeni`,
      updatedData,
      {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      }
    );

    const toast = new Toast(toastElement.value);
    toast.show();

    setTimeout(() => {
      router.push("/korisnici");
    }, 2000); 
  } catch (error) {
    console.error("Greška pri ažuriranju korisnika:", error);
    alert("Došlo je do greške pri ažuriranju korisnika.");
  }
};

onMounted(() => {
  fetchKorisnikData();
});
</script>

<template>
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
        <div class="toast-body">Izmena uspešno sačuvana!</div>
        <button
          type="button"
          class="btn-close btn-close-white me-2 m-auto"
          data-bs-dismiss="toast"
          aria-label="Close"
        ></button>
      </div>
    </div>
  </div>
  <div class="container col-lg-6">
    <h3>Izmena transakcije</h3>

    <form @submit.prevent="updateKorisnikData">
      <div class="form-group">
        <label for="naziv">Naziv</label>
        <input
          type="text"
          class="form-control"
          v-model="korisnik.naziv"
          required
        />
      </div>

      <div class="form-group">
        <label for="iznos">Iznos</label>
        <input
          type="number"
          class="form-control"
          v-model="korisnik.iznos"
          required
        />
      </div>

      <div class="form-group">
        <label for="tip">Tip</label>
        <select class="form-control" v-model="korisnik.type" required>
          <option value="prihod">Prihod</option>
          <option value="rashod">Rashod</option>
        </select>
      </div>

      <button type="submit" class="btn btn-primary">Sacuvaj izmene</button>
    </form>
  </div>
</template>
