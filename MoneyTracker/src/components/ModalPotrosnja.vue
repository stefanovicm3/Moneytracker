<script setup>
import { ref, defineProps, defineEmits, watchEffect } from "vue";
import axios from "axios";

const props = defineProps({
  otvoren: Boolean,
  budzet: Object,
  userId: Number,
  token: String,
});

const emit = defineEmits(["zatvoriModal", "osveziPodatke"]);

const novaPotrosnja = ref({
  potroseno: "",
  mesec: "",
  godina: "",
  kategorija: "",
});

watchEffect(() => {
  if (props.otvoren) {
    novaPotrosnja.value.kategorija = props.budzet?.kategorija || "";
  }
});

const dodajPotrosnju = async () => {
  if (
    !novaPotrosnja.value.potroseno ||
    !novaPotrosnja.value.mesec ||
    !novaPotrosnja.value.godina ||
    !novaPotrosnja.value.kategorija
  ) {
    console.error("Sva polja moraju biti popunjena");
    console.log("Podaci koji se šalju na server:", novaPotrosnja.value);
    return;
  }

  try {
    const response = await axios.post(
      `/api/budzet/potrosnja/${props.budzet.id}`,
      novaPotrosnja.value,
      {
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${props.token}`,
        },
      }
    );

    if (response.status !== 200) {
      throw new Error("Greška pri dodavanju potrošnje");
    }

    novaPotrosnja.value = {
      potroseno: "",
      mesec: "",
      godina: "",
      kategorija: "",
    };
    emit("zatvoriModal");
    emit("osveziPodatke");
  } catch (error) {
    console.error("Greška:", error);
  }
};
</script>

<template>
  <div
    v-if="otvoren"
    class="modal fade show"
    tabindex="-1"
    id="potrosnjaModal"
    style="display: block; background-color: rgba(0, 0, 0, 0.6)"
  >
    <div class="modal-dialog modal-lg">
      <div class="modal-content">
        <div class="modal-header">
          <h5 class="modal-title">
            Unesite potrošnju za {{ budzet?.kategorija }}
          </h5>
          <button
            type="button"
            class="btn-close"
            @click="$emit('zatvoriModal')"
          ></button>
        </div>
        <div class="modal-body">
          <form @submit.prevent="dodajPotrosnju">
            <div class="mb-3">
              <label for="potroseno" class="form-label">Iznos potrošen</label>
              <input
                type="number"
                class="form-control"
                id="potroseno"
                v-model="novaPotrosnja.potroseno"
                required
              />
            </div>

            <div class="mb-3">
              <label for="mesec" class="form-label">Mesec</label>
              <select
                class="form-control"
                id="mesec"
                v-model="novaPotrosnja.mesec"
                required
              >
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

            <div class="mb-3">
              <label for="godina" class="form-label">Godina</label>
              <input
                type="number"
                class="form-control"
                id="godina"
                v-model="novaPotrosnja.godina"
                required
              />
            </div>

            <div class="mb-3">
              <label for="kategorija" class="form-label">Kategorija</label>
              <input
                type="text"
                class="form-control"
                id="kategorija"
                :value="novaPotrosnja.kategorija"
                readonly
              />
            </div>

            <button type="submit" class="btn btn-primary">Sačuvaj</button>
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

.modal.fade.show {
  background-color: rgba(0, 0, 0, 0.6);
}

.modal-content {
  border-radius: 10px;
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.3);
}

.modal-body {
  padding: 30px;
}
</style>
