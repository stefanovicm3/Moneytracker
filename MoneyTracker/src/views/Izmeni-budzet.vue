<script setup>
import { ref, onMounted } from "vue";
import { useRoute, useRouter } from "vue-router";

const kategorija = ref("");
const novaKategorija = ref("");
const iznos = ref("");
const mesec = ref("");
const godina = ref("");
const kategorije = ref([]);
const months = [
  "Januar",
  "Februar",
  "Mart",
  "April",
  "Maj",
  "Jun",
  "Jul",
  "Avgust",
  "Septembar",
  "Oktobar",
  "Novembar",
  "Decembar",
];
const years = Array.from({ length: 11 }, (_, i) => 2020 + i);

const route = useRoute();
const router = useRouter();

const formatNumber = (number) => {
  return new Intl.NumberFormat("sr-RS", {
    minimumFractionDigits: 0,
    maximumFractionDigits: 2,
  }).format(number);
};

const cleanInputAmount = (input) => {
  if (typeof input !== "string") {
    input = String(input);
  }

  return parseFloat(input.replace(/\./g, "").replace(",", "."));
};
const loadBudgetData = async () => {
  const budgetId = route.params.budgetId;
  console.log("Budžet ID:", budgetId);

  try {
    const response = await fetch(`/api/budzet/${budgetId}`, {
      method: "GET",
      headers: {
        Authorization: `Bearer ${localStorage.getItem("jwt_token")}`,
        "Content-Type": "application/json",
      },
    });

    if (response.ok) {
      const budgetData = await response.json();
      console.log("Podaci budžeta:", budgetData);

      kategorija.value = budgetData.kategorija;
      iznos.value = parseFloat(
        budgetData.iznos.replace(".", "").replace(",", ".")
      );
      mesec.value = budgetData.mesec;
      godina.value = budgetData.godina;

      kategorije.value = await loadCategories();
    } else {
      console.error("Greška pri učitavanju budžeta:", response.statusText);
    }
  } catch (error) {
    console.error("Greška pri učitavanju budžeta:", error);
  }
};

const loadCategories = async () => {
  try {
    const response = await fetch(`/api/kategorije`, {
      method: "GET",
      headers: {
        Authorization: `Bearer ${localStorage.getItem("jwt_token")}`,
        "Content-Type": "application/json",
      },
    });

    if (response.ok) {
      const categories = await response.json();
      return categories;
    } else {
      console.error("Greška pri učitavanju kategorija:", response.statusText);
      return [];
    }
  } catch (error) {
    console.error("Greška pri učitavanju kategorija:", error);
    return [];
  }
};

onMounted(() => {
  loadBudgetData();
});

const onKategorijaChange = () => {
  if (kategorija.value !== "nova_kategorija") {
    novaKategorija.value = "";
  }
};

const izmeniBudzet = async () => {
  const budzetData = {
    kategorija:
      kategorija.value === "nova_kategorija"
        ? novaKategorija.value
        : kategorija.value,
    iznos: cleanInputAmount(iznos.value),
    mesec: mesec.value,
    godina: godina.value,
  };

  try {
    const response = await fetch(
      `/api/budzet/izmeni/${route.params.budgetId}`,
      {
        method: "POST",
        headers: {
          Authorization: `Bearer ${localStorage.getItem("jwt_token")}`,
          "Content-Type": "application/json",
        },
        body: JSON.stringify(budzetData),
      }
    );

    if (response.ok) {
      console.log("Budžet uspešno izmenjen!");
      router.push("/budzet");
    } else {
      const responseText = await response.text();
      console.error("Greška pri izmeni budžeta:", responseText);
    }
  } catch (error) {
    console.error("Greška pri slanju podataka za izmenu budžeta:", error);
  }
};
</script>

<template>
  <div class="container col-lg-2 col-lg-12">
    <div class="my-5">
      <h3>Izmeni budžet</h3>
    </div>

    <form @submit.prevent="izmeniBudzet">
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
        <input
          type="text"
          class="form-control"
          v-model="iznos"
          @input="cleanInputAmount"
          required
        />
      </div>

      <div class="form-group">
        <label for="mesec">Mesec:</label>
        <select class="form-control" v-model="mesec" required>
          <option v-for="month in months" :key="month" :value="month">
            {{ month }}
          </option>
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

      <button type="submit" class="btn btn-primary">Izmeni</button>
    </form>
  </div>
</template>

<style scoped></style>
