<script setup>
import { ref, onMounted } from "vue";
import axios from "axios";
import { useRouter } from "vue-router";

const kategorija = ref("");
const novaKategorija = ref("");
const iznos = ref("");
const mesec = ref("");
const godina = ref(new Date().getFullYear());

const kategorije = ref([]);

const years = Array.from({ length: 11 }, (_, i) => 2020 + i);

const router = useRouter();

const loadCategories = async () => {
  try {
    const response = await axios.get("/api/sve-kategorije", {
      headers: {
        Authorization: `Bearer ${localStorage.getItem("jwt_token")}`,
        "Content-Type": "application/json",
      },
    });

    console.log("Sve kategorije sa servera:", response.data);
    if (response.status === 200) {
      kategorije.value = response.data;
    } else {
      console.error("Greška pri učitavanju kategorija:", response.statusText);
    }
  } catch (error) {
    console.error("Greška pri učitavanju kategorija:", error);
  }
};

onMounted(() => {
  loadCategories();
});

const onKategorijaChange = () => {
  if (kategorija.value !== "nova_kategorija") {
    novaKategorija.value = "";
  }
};

const dodajBudzet = async () => {
  const budzetData = {
    kategorija:
      kategorija.value === "nova_kategorija"
        ? novaKategorija.value
        : kategorija.value,
    iznos: iznos.value,
    mesec: mesec.value,
    godina: godina.value,
    nova_kategorija: novaKategorija.value,
  };

  try {
    const token = localStorage.getItem("jwt_token");
    if (!token) {
      alert("Niste prijavljeni. Molimo prijavite se ponovo.");
      return;
    }

    const response = await axios.post("/api/budzet/dodaj", budzetData, {
      headers: { Authorization: `Bearer ${token}` },
    });

    await loadCategories();

    router.push("/budzet");
  } catch (error) {
    console.error("Greška prilikom dodavanja budžeta:", error);
    alert("Došlo je do greške prilikom dodavanja budžeta.");
  }

  kategorija.value = "";
  novaKategorija.value = "";
  iznos.value = "";
  mesec.value = "";
  godina.value = new Date().getFullYear();
};
</script>

<template>
  <div class="container col-lg-2 col-lg-12">
    <div class="my-5">
      <h3>Dodaj budžet</h3>
    </div>

    <form @submit.prevent="dodajBudzet">
      <div class="form-group">
        <label for="kategorija">Kategorija:</label>
        <select
          class="form-control"
          v-model="kategorija"
          @change="onKategorijaChange"
          required
        >
          <option
            v-for="(kategorijaItem, index) in kategorije"
            :key="index"
            :value="kategorijaItem"
          >
            {{ kategorijaItem }}
          </option>
          <option value="nova_kategorija">Nova kategorija</option>
        </select>
      </div>

      <!-- Div za unos nove kategorije -->
      <div v-if="kategorija === 'nova_kategorija'" class="form-group">
        <label for="nova_kategorija">Unesite novu kategoriju:</label>
        <input type="text" class="form-control" v-model="novaKategorija" />
      </div>

      <div class="form-group">
        <label for="iznos">Iznos:</label>
        <input type="number" class="form-control" v-model="iznos" required />
      </div>

      <div class="form-group">
        <label for="mesec">Mesec:</label>
        <select class="form-control" v-model="mesec" required>
          <option value="Januar">Januar</option>
          <option value="Februar">Februar</option>
          <option value="Mart">Mart</option>
          <option value="April">April</option>
          <option value="Maj">Maj</option>
          <option value="Jun">Jun</option>
          <option value="Jul">Jul</option>
          <option value="Avgust">Avgust</option>
          <option value="Septembar">Septembar</option>
          <option value="Oktobar">Oktobar</option>
          <option value="Novembar">Novembar</option>
          <option value="Decembar">Decembar</option>
        </select>
      </div>

      <div class="form-group">
        <label for="godina">Godina:</label>
        <select class="form-control" v-model="godina" required>
          <option v-for="year in years" :key="year" :value="year">
            {{ year }}
          </option>
        </select>
      </div>

      <button type="submit" class="btn btn-primary">Dodaj</button>
    </form>
  </div>
</template>

<style scoped></style>
