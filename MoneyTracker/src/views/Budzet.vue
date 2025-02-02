<script setup>
import Navigation from "@/components/Navigation.vue";
import { ref, onMounted, watch } from "vue";
import axios from "axios";
import Swal from "sweetalert2";
import IzmeniPotrosnjuModal from "@/components/IzmeniPotrosnjuModal.vue";
import ModalPotrosnja from "@/components/ModalPotrosnja.vue";
import { Chart } from "chart.js";

const userId = ref(null);

const token = localStorage.getItem("jwt_token");
if (token) {
  try {
    const decodedToken = JSON.parse(atob(token.split(".")[1]));

    userId.value = decodedToken.id;
  } catch (error) {
    console.error("Greška pri dekodiranju tokena:", error);
  }
}
const budzeti = ref([]);
const potrosnje = ref([]);
const ukupniBudzet = ref(0);
const ukupnaPotrosnja = ref(0);
const otvorenModal = ref(false);
const izabraniBudzet = ref(null);
const modalOtvoren = ref(false);
const potrosnjaData = ref(null);
const potrosnja = ref({
  iznos: "",
  mesec: "",
  godina: "",
  kategorija: "",
});

const fetchPodaci = async () => {
  try {
    const budzetiResponse = await axios.get(`/api/budzet`, {
      headers: { Authorization: `Bearer ${token}` },
    });

    const potrosnjeResponse = await axios.get(`/api/budzet`, {
      headers: { Authorization: `Bearer ${token}` },
    });

    const formatter = new Intl.NumberFormat("sr-RS", {
      minimumFractionDigits: 0,
      maximumFractionDigits: 0,
    });

    if (Array.isArray(budzetiResponse.data.budzeti)) {
      budzeti.value = budzetiResponse.data.budzeti;
      let ukupno = budzeti.value.reduce((acc, curr) => {
        const iznos = parseFloat(
          curr.iznos.replace(/\./g, "").replace(",", ".")
        );
        return acc + (isNaN(iznos) ? 0 : iznos);
      }, 0);

      ukupniBudzet.value = formatter.format(ukupno);
    } else {
      console.error("Podaci nisu u očekivanom formatu.");
      Swal.fire("Greška", "Podaci nisu u očekivanom formatu.", "error");
    }

    if (Array.isArray(potrosnjeResponse.data.potrosnje)) {
      potrosnje.value = potrosnjeResponse.data.potrosnje;
      let ukupno = potrosnje.value.reduce((acc, curr) => {
        const iznos = parseFloat(
          curr.iznos.replace(/\./g, "").replace(",", ".")
        );
        return acc + (isNaN(iznos) ? 0 : iznos);
      }, 0);

      ukupnaPotrosnja.value = formatter.format(ukupno);
    } else {
      console.error("Potrošnje nisu u očekivanom formatu.");
    }

    createChart();
  } catch (error) {
    console.error("Greška:", error);
    Swal.fire(
      "Greška",
      "Došlo je do greške prilikom učitavanja podataka.",
      "error"
    );
  }
};

const obrisiBudzet = async (id) => {
  Swal.fire({
    title: "Da li ste sigurni?",
    text: "Ova akcija je nepovratna!",
    icon: "warning",
    showCancelButton: true,
    cancelButtonText: "Ne, odustani",
    confirmButtonText: "Da, obriši!",
    reverseButtons: true,
  }).then(async (result) => {
    if (result.isConfirmed) {
      try {
        await axios.delete(`/api/budzet/obrisi/${id}`, {
          headers: { Authorization: `Bearer ${token}` },
        });
        fetchPodaci();
        Swal.fire("Obrisano!", "Budžet je uspešno obrisan.", "success");
      } catch (error) {
        console.error("Greška pri brisanju budžeta:", error);
        Swal.fire("Greška", "Greška! Brisanje nije uspelo.", "error");
      }
    }
  });
};

const otvoriModal = (budzet) => {
  if (budzet) {
    izabraniBudzet.value = budzet;
    otvorenModal.value = true;
  }
};

const otvoriIzmeniPotrosnjuModal = (potrosnja) => {
  if (potrosnja) {
    console.log("Podaci za potrošnju:", potrosnja);
    potrosnjaData.value = potrosnja;
    modalOtvoren.value = true;
  }
};

const obrisiPotrosnju = async (id) => {
  Swal.fire({
    title: "Da li ste sigurni?",
    text: "Ova akcija je nepovratna!",
    icon: "warning",
    showCancelButton: true,
    cancelButtonText: "Ne, odustani",
    confirmButtonText: "Da, obriši!",
    reverseButtons: true,
  }).then(async (result) => {
    if (result.isConfirmed) {
      try {
        const response = await axios.post(
          `api/potrosnja/obrisi/${id}`,
          {},
          {
            headers: {
              Authorization: `Bearer ${token}`,
            },
          }
        );

        fetchPodaci();
        Swal.fire("Obrisano!", "Potrošnja je uspešno obrisana.", "success");
      } catch (error) {
        console.error("Greška pri brisanju potrošnje:", error);
        Swal.fire(
          "Greška",
          "Došlo je do greške pri brisanju potrošnje.",
          "error"
        );
      }
    }
  });
};

onMounted(() => {
  fetchPodaci();
});

const formatter = new Intl.NumberFormat("sr-RS", {
  minimumFractionDigits: 3,
  maximumFractionDigits: 3,
});

let chartInstance = null;

const createChart = () => {
  const ctx = document.getElementById("budzetGrafikon").getContext("2d");

  if (chartInstance) {
    chartInstance.destroy();
  }

  const kategorije = [
    ...new Set([
      ...potrosnje.value.map((p) => p.kategorija),
      ...budzeti.value.map((b) => b.kategorija),
    ]),
  ];

  const potrosnjaPoKategoriji = kategorije.map((kategorija) => {
    return potrosnje.value
      .filter((p) => p.kategorija === kategorija)
      .reduce((acc, curr) => acc + parseFloat(curr.iznos.replace(",", ".")), 0);
  });

  const budzetPoKategoriji = kategorije.map((kategorija) => {
    return budzeti.value
      .filter((b) => b.kategorija === kategorija)
      .reduce((acc, curr) => acc + parseFloat(curr.iznos.replace(",", ".")), 0);
  });

  chartInstance = new Chart(ctx, {
    type: "bar",
    data: {
      labels: kategorije,
      datasets: [
        {
          label: "Budžet",
          data: budzetPoKategoriji,
          backgroundColor: "rgba(75, 192, 192, 0.2)",
          borderColor: "rgba(75, 192, 192, 1)",
          borderWidth: 1,
        },
        {
          label: "Potrošnja",
          data: potrosnjaPoKategoriji,
          backgroundColor: "rgba(255, 99, 132, 0.2)",
          borderColor: "rgba(255, 99, 132, 1)",
          borderWidth: 1,
        },
      ],
    },
    options: {
      scales: {
        y: {
          beginAtZero: true,
          ticks: {
            callback: function (value) {
              return formatter.format(value) + " RSD";
            },
          },
        },
      },
      plugins: {
        legend: {
          display: true,
          position: "top",
        },
        tooltip: {
          callbacks: {
            label: function (context) {
              return (
                context.dataset.label +
                ": " +
                formatter.format(context.raw) +
                " RSD"
              );
            },
          },
        },
      },
    },
  });
};

onMounted(fetchPodaci);

const osveziPodatke = () => {
  fetchPodaci();
};
</script>

<template>
  <div>
    <ModalPotrosnja
      ref="modalPotrosnja"
      :otvoren="otvorenModal"
      :budzet="izabraniBudzet"
      :userId="userId"
      :token="token"
      @zatvoriModal="otvorenModal = false"
      @osveziPodatke="fetchPodaci"
    />
    <IzmeniPotrosnjuModal
      ref="modalIzmeniPotrosnju"
      :otvoren="modalOtvoren"
      :potrosnjaData="potrosnjaData"
      @zatvoriModal="modalOtvoren = false"
      @osveziPodatke="osveziPodatke"
    />
    <Navigation />

    <div
      style="background-color: #f1f3f5; position: relative; padding-top: 50px"
    >
      <div class="container-fluid mt-1">
        <div class="d-flex align-items-start">
          <div class="me-5">
            <img
              src="../assets/profilna123.jpg"
              alt="Profilna slika"
              class="img-thumbnail rounded-circle mt-3 ms-4"
            />
          </div>

          <div style="width: 300px">
            <table class="table table-bordered mt-5">
              <thead>
                <tr>
                  <th>Ukupni Budžet</th>
                  <td>
                    <strong>{{ ukupniBudzet }} RSD</strong>
                  </td>
                </tr>
              </thead>
              <tbody>
                <tr>
                  <th>Ukupna potrošnja</th>
                  <td>
                    <strong>{{ ukupnaPotrosnja }} RSD</strong>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>

          <div
            class="ms-auto"
            style="
              position: absolute;
              top: 100px;
              right: 10px;
              width: 710px;
              height: 800px;
            "
          >
            <div class="card">
              <div class="card-header">
                <h5>Budžet i Potrošnja</h5>
              </div>
              <div class="card-body">
                <canvas id="budzetGrafikon"></canvas>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- OVDE KRECE DRUGA TABELA -->
    <div class="container mt-4 ms-5" style="padding-top: 70px">
      <div class="row">
        <div class="col-md-8 position-relative">
          <router-link
            :to="`/budzet/dodaj`"
            role="button"
            class="btn btn-primary position-absolute top-0 end-0"
            style="margin-top: -40px; margin-right: 10px"
          >
            Dodaj novi budžet
          </router-link>

          <!-- Tabela -->
          <table class="table">
            <thead class="thead-dark table-primary">
              <tr>
                <th scope="col">Kategorija</th>
                <th scope="col">Iznos</th>
                <th scope="col">Mesec</th>
                <th scope="col">Godina</th>
                <th scope="col" class="text-center">Akcija</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="budzet in budzeti" :key="budzet.id">
                <td>{{ budzet.kategorija }}</td>
                <td>{{ budzet.iznos }} RSD</td>
                <td>{{ budzet.mesec }}</td>
                <td>{{ budzet.godina }}</td>
                <td class="text-center">
                  <router-link
                    :to="`/izmeni-budzet/${budzet.id}`"
                    role="button"
                    class="btn btn-warning btn-sm mx-1"
                  >
                    <i class="fa-solid fa-pen-to-square"></i>
                  </router-link>

                  <button
                    @click="obrisiBudzet(budzet.id)"
                    class="btn btn-danger btn-sm mx-1"
                  >
                    <i class="fas fa-trash"></i>
                  </button>
                  <button
                    @click="otvoriModal(budzet)"
                    class="btn btn-info btn-sm mx-1"
                  >
                    Unesi potrošnju
                  </button>
                </td>
              </tr>

              <tr
                class="table-danger"
                v-for="potrosnja in potrosnje"
                :key="potrosnja.id"
              >
                <td>{{ potrosnja.kategorija }}</td>
                <td>-{{ potrosnja.iznos }} RSD</td>
                <td>{{ potrosnja.mesec }}</td>
                <td>{{ potrosnja.godina }}</td>
                <td class="text-center">
                  <button
                    @click="otvoriIzmeniPotrosnjuModal(potrosnja)"
                    class="btn btn-warning btn-sm mx-1"
                  >
                    <i class="fa-solid fa-pen-to-square"></i>
                  </button>
                  <button
                    @click="obrisiPotrosnju(potrosnja.id)"
                    class="btn btn-danger btn-sm mx-1"
                  >
                    <i class="fas fa-trash"></i>
                  </button>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>
  </div>
</template>
