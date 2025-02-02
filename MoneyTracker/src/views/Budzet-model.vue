<script setup>
import { ref } from "vue";
import { useRouter } from "vue-router";
import axios from "axios";
import Swal from "sweetalert2";

// const props = defineProps({
//   budzet: Object,
//   token: String,
//   osveziPodatke: Function,
// });

// const router = useRouter();

// const potrosnja = ref({
//   potroseno: "",
//   mesec: "",
//   godina: "",
//   kategorija: props.budzet.kategorija,
// });

// const zatvoriModal = () => {
//   const modalElement = document.getElementById("potrosnjaModal");
//   const modal = bootstrap.Modal.getInstance(modalElement);
//   modal.hide();
// };

// const unesiPotrosnju = async () => {
//   try {
//     const response = await axios.post(
//       `/api/budzeti/${props.budzet.id}/potrosnja`,
//       potrosnja.value,
//       {
//         headers: {
//           Authorization: `Bearer ${props.token}`,
//           "Content-Type": "application/json",
//         },
//       }
//     );

//     if (response.status === 200) {
//       Swal.fire("Uspešno!", "Potrošnja je uspešno unesena.", "success");
//       zatvoriModal();

//       props.osveziPodatke();

//       router.push({ path: "/budzeti" });
//     } else {
//       Swal.fire("Greška", "Došlo je do greške pri unosu potrošnje.", "error");
//     }
//   } catch (error) {
//     console.error("Greška pri slanju podataka:", error);
//     Swal.fire("Greška", "Došlo je do greške pri slanju podataka.", "error");
//   }
// };
</script>

<template>
  <!-- <div
    class="modal fade"
    id="potrosnjaModal"
    tabindex="-1"
    aria-labelledby="potrosnjaModalLabel"
    aria-hidden="true"
  >
    <div class="modal-dialog">
      <div class="modal-content">
        <div class="modal-header">
          <h5 class="modal-title" id="potrosnjaModalLabel">
            Unesite potrošnju za {{ budzet.kategorija }}
          </h5>
          <button
            type="button"
            class="btn-close"
            @click="zatvoriModal"
            aria-label="Close"
          ></button>
        </div>
        <div class="modal-body">
          <form @submit.prevent="unesiPotrosnju">
            <div class="mb-3">
              <label for="potroseno" class="form-label">Iznos potrošen</label>
              <input
                type="number"
                class="form-control"
                v-model="potrosnja.potroseno"
                id="potroseno"
                required
              />
            </div>

            <div class="mb-3">
              <label for="mesec" class="form-label">Mesec</label>
              <input
                type="text"
                class="form-control"
                v-model="potrosnja.mesec"
                id="mesec"
                required
              />
            </div>

            <div class="mb-3">
              <label for="godina" class="form-label">Godina</label>
              <input
                type="text"
                class="form-control"
                v-model="potrosnja.godina"
                id="godina"
                required
              />
            </div>

            <input type="hidden" v-model="potrosnja.kategorija" />

            <button type="submit" class="btn btn-primary">Sačuvaj</button>
          </form>
        </div>
      </div>
    </div>
  </div> -->
</template>

<style scoped></style>
