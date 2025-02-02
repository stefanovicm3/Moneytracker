<script setup>
import { onMounted, ref } from "vue";
import axios from "axios";
import Swal from "sweetalert2";
import { useRoute } from "vue-router";
import Navigation from "@/components/Navigation.vue";
import Chart from "chart.js/auto";

const trenutnoStanje = ref(0);
const prihod = ref(0);
const rashod = ref(0);
const korisnici = ref([]);

// Pristupanje 'user_id' iz URL-a
const route = useRoute();
const userId = route.params.user_id;

const fetchKorisnici = async () => {
  try {
    const token = localStorage.getItem("jwt_token");

    if (!token) {
      Swal.fire(
        "Greška",
        "Niste prijavljeni. Molimo prijavite se ponovo.",
        "error"
      );
      return;
    }

    const response = await axios.get("/api/korisnici", {
      headers: { Authorization: `Bearer ${token}` },
    });

    console.log("Odgovor sa servera:", response.data);

    const data = response.data;
    korisnici.value = data.korisnici;

    prihod.value = data.prihod || 0;
    rashod.value = data.rashod || 0;
    trenutnoStanje.value = prihod.value - rashod.value;

    trenutnoStanje.value = trenutnoStanje.value.toFixed(3);

    prihod.value = prihod.value + " RSD";
    rashod.value = rashod.value + " RSD";
    trenutnoStanje.value = trenutnoStanje.value + " RSD";

    setupChart();
  } catch (error) {
    console.error("Greška prilikom dohvatanja transakcije", error);
    Swal.fire("Greška", "Greška prilikom učitavanja transakcije.", "error");
  }
};

const deleteUser = async (id) => {
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
        const token = localStorage.getItem("jwt_token");

        if (!token) {
          Swal.fire(
            "Greška",
            "Niste prijavljeni. Molimo prijavite se ponovo.",
            "error"
          );
          return;
        }

        await axios.delete(`/api/korisnik_brisanje/${id}`, {
          headers: { Authorization: `Bearer ${token}` },
        });

        korisnici.value = korisnici.value.filter(
          (korisnik) => korisnik.id !== id
        );

        Swal.fire("Obrisano!", "Transakcija je uspešno obrisana.", "success");

        fetchKorisnici();
      } catch (error) {
        console.error("Greška prilikom brisanja transakcije", error);
        Swal.fire("Greška", "Greška! Brisanje nije uspelo.", "error");
      }
    }
  });
};

const formatter = new Intl.NumberFormat("sr-RS", {
  minimumFractionDigits: 3,
  maximumFractionDigits: 3,
});

let chartInstance = null;

const setupChart = () => {
  const ctx = document.getElementById("myChart").getContext("2d");

  if (chartInstance) {
    chartInstance.destroy();
  }

  chartInstance = new Chart(ctx, {
    type: "bar",
    data: {
      labels: ["Prihodi", "Rashodi"],
      datasets: [
        {
          label: "Izbor finansija",
          data: [
            parseFloat(prihod.value.replace(" RSD", "").replace(",", ".")),
            parseFloat(rashod.value.replace(" RSD", "").replace(",", ".")),
          ],
          backgroundColor: [
            "rgba(75, 192, 192, 0.2)",
            "rgba(255, 99, 132, 0.2)",
          ],
          borderColor: ["rgba(75, 192, 192, 1)", "rgba(255, 99, 132, 1)"],
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
onMounted(() => {
  fetchKorisnici();
});
</script>

<template>
  <div>
    <Navigation />
    <div style="background-color: #f1f3f5; padding-top: 50px">
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
                  <th>Trenutno stanje</th>
                  <td>
                    <strong>{{ trenutnoStanje }}</strong>
                  </td>
                </tr>
              </thead>
              <tbody>
                <tr>
                  <th>Prihodi</th>
                  <td>
                    <strong>{{ prihod }}</strong>
                  </td>
                </tr>
                <tr>
                  <th>Rashodi</th>
                  <td>
                    <strong>{{ rashod }}</strong>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>

          <div
            class="ms-auto"
            style="
              position: absolute;
              top: 200px;
              right: 10px;
              width: 710px;
              height: 800px;
            "
          >
            <div class="card">
              <div class="card-header">
                <h5>Pregled Finansija</h5>
              </div>
              <div class="card-body">
                <canvas id="myChart"></canvas>
              </div>
            </div>
          </div>
        </div>
      </div>

      <div class="container mt-4 ms-5" style="padding-top: 70px">
        <div class="row">
          <div class="col-md-8 position-relative">
            <router-link
              :to="`/korisnici/dodaj-novi`"
              role="button"
              class="btn btn-primary position-absolute top-0 end-0"
              style="margin-top: -40px; margin-right: 10px"
            >
              Dodaj novu transakciju
            </router-link>

            <table class="table">
              <thead class="thead-dark table-primary">
                <tr>
                  <th scope="col">Naziv</th>
                  <th scope="col">Iznos</th>
                  <th scope="col" class="text-center">Akcija</th>
                </tr>
              </thead>
              <tbody class="table-bordered">
                <tr v-for="korisnik in korisnici" :key="korisnik.id">
                  <td>{{ korisnik.naziv }}</td>
                  <td>
                    <span v-if="korisnik.type === 'rashod'">
                      -{{ korisnik.iznos }} RSD
                    </span>
                    <span v-else>{{ korisnik.iznos }} RSD</span>
                  </td>
                  <td class="text-center">
                    <router-link
                      :to="`/korisnici/pregled/${korisnik.id}`"
                      role="button"
                      class="btn btn-info btn-sm"
                    >
                      <i class="fa-solid fa-eye"></i>
                    </router-link>

                    <router-link
                      :to="`/korisnici/edit/${korisnik.id}`"
                      role="button"
                      class="btn btn-warning btn-sm mx-1"
                    >
                      <i class="fa-solid fa-pen-to-square"></i>
                    </router-link>

                    <button
                      @click="deleteUser(korisnik.id)"
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
  </div>
</template>

<style scoped>
.navbar-nav .nav-link:hover {
  color: #01a2e9 !important;
  background-color: rgba(0, 162, 233, 0.1);
}
</style>
