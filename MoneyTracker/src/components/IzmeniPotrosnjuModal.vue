<script setup>
import { ref, defineProps, defineEmits, onMounted, nextTick } from "vue";
import axios from "axios";

const props = defineProps({
  otvoren: Boolean,
  potrosnjaData: Object,
});

const emit = defineEmits(["zatvoriModal", "osveziPodatke"]);

const kategorija = ref("");
const novaKategorija = ref("");
const iznos = ref("");
const mesec = ref("");
const godina = ref("");
const kategorije = ref([]);

const modalRef = ref(null);

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

onMounted(() => {
  console.log("Potrošnja u modal:", props.potrosnjaData);

  if (
    props.potrosnjaData &&
    props.potrosnjaData.kategorija &&
    props.potrosnjaData.iznos
  ) {
    kategorija.value = props.potrosnjaData.kategorija;
    iznos.value = props.potrosnjaData.iznos;
    mesec.value = props.potrosnjaData.mesec || "";
    godina.value = props.potrosnjaData.godina || "";
  } else {
    kategorija.value = "";
    iznos.value = "";
    mesec.value = "";
    godina.value = "";
  }

  loadCategories();
});
import { watch } from "vue";

watch(
  () => props.potrosnjaData,
  (newData) => {
    if (newData) {
      kategorija.value = newData.kategorija;
      iznos.value = newData.iznos;
      mesec.value = newData.mesec || "";
      godina.value = newData.godina || "";
    }
  },
  { immediate: true }
);

const loadCategories = async () => {
  try {
    const response = await fetch("/api/kategorije", {
      method: "GET",
      headers: {
        Authorization: `Bearer ${localStorage.getItem("jwt_token")}`,
        "Content-Type": "application/json",
      },
    });

    if (response.ok) {
      const categories = await response.json();
      kategorije.value = categories;
      console.log("Učitane kategorije:", kategorije.value);
    } else {
      console.error("Greška pri učitavanju kategorija:", response.statusText);
    }
  } catch (error) {
    console.error("Greška pri učitavanju kategorija:", error);
  }
};

const onKategorijaChange = () => {
  if (kategorija.value !== "nova_kategorija") {
    novaKategorija.value = "";
  }
};

const izmeniPotrosnju = async () => {
  const potrosnjaData = {
    kategorija:
      kategorija.value === "nova_kategorija"
        ? novaKategorija.value
        : kategorija.value,
    iznos: iznos.value,
    mesec: mesec.value, // Dodaj mesec
    godina: godina.value, // Dodaj godina
  };

  try {
    const response = await axios.put(
      `/api/potrosnja/izmeni/${props.potrosnjaData.id}`,
      potrosnjaData,
      {
        headers: {
          Authorization: `Bearer ${localStorage.getItem("jwt_token")}`,
        },
      }
    );

    if (response.status === 200) {
      emit("osveziPodatke");
      emit("zatvoriModal");
    } else {
      console.error("Greška pri izmeni potrošnje:", response.statusText);
    }
  } catch (error) {
    console.error("Greška pri slanju podataka za izmenu potrošnje:", error);
  }
};

const zatvoriModal = () => {
  emit("zatvoriModal");
};
</script>

<template>
  <div
    v-if="otvoren"
    class="modal fade show"
    tabindex="-1"
    id="izmeniPotrosnjuModal"
    style="display: block; background-color: rgba(0, 0, 0, 0.6)"
  >
    <div class="modal-dialog modal-lg">
      <div class="modal-content">
        <div class="modal-header">
          <h5 class="modal-title">Izmeni potrošnju</h5>
          <button
            type="button"
            class="btn-close"
            @click="zatvoriModal"
          ></button>
        </div>
        <div class="modal-body">
          <form @submit.prevent="izmeniPotrosnju">
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

            <div v-if="kategorija === 'nova_kategorija'" class="form-group">
              <label for="nova_kategorija">Unesite novu kategoriju:</label>
              <input
                type="text"
                class="form-control"
                v-model="novaKategorija"
              />
            </div>

            <div class="form-group">
              <label for="iznos">Iznos:</label>
              <input
                type="number"
                class="form-control"
                v-model="iznos"
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
      </div>
    </div>
  </div>
</template>

<style scoped>
.modal-dialog.modal-lg {
  max-width: 80%;
}
.modal-content {
  border-radius: 10px;
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.3);
}
.modal-body {
  padding: 30px;
}
</style>
