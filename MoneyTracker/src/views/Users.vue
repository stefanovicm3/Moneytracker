<script setup>
import { ref, onMounted } from "vue";
import Swal from "sweetalert2";
import Navigation from "@/components/Navigation.vue";

const users = ref([]);
const token = localStorage.getItem("jwt_token");

if (!token) {
  console.error("Nema JWT tokena! Korisnik nije autentifikovan.");
}

const fetchUsers = async () => {
  try {
    const response = await fetch("/api/users", {
      headers: {
        Authorization: `Bearer ${token}`,
      },
    });

    if (!response.ok) {
      throw new Error("Greška pri učitavanju korisnika");
    }

    const data = await response.json();
    users.value = data;
  } catch (error) {
    console.error("Greška:", error);
  }
};

const deleteUser = (id) => {
  Swal.fire({
    title: "Da li ste sigurni?",
    text: "Brisanjem će ovaj korisnik biti trajno uklonjen.",
    icon: "warning",
    showCancelButton: true,
    confirmButtonColor: "#3085d6",
    cancelButtonColor: "#d33",
    confirmButtonText: "Da, obriši",
    cancelButtonText: "Odustani",
  }).then(async (result) => {
    if (result.isConfirmed) {
      try {
        const response = await fetch(`/api/delete_user/${id}`, {
          method: "DELETE",
          headers: {
            Authorization: `Bearer ${token}`,
          },
        });

        if (response.ok) {
          users.value = users.value.filter((user) => user.id !== id);
          Swal.fire("Obrisano!", "Korisnik je uspešno obrisan.", "success");
        } else {
          throw new Error("Greška prilikom brisanja korisnika");
        }
      } catch (error) {
        console.error("Greška:", error);
        Swal.fire(
          "Greška!",
          "Došlo je do greške prilikom brisanja korisnika.",
          "error"
        );
      }
    }
  });
};

onMounted(() => {
  fetchUsers();
});
</script>
<template>
  <div>
    <Navigation />

    <div
      style="background-color: #f1f3f5; position: relative; padding-top: 50px"
    >
      <div class="container my-5">
        <h1 class="text-center mb-4">Upravljanje Korisnicima</h1>

        <!-- Tabela korisnika -->
        <table class="table table-striped table-bordered">
          <thead class="table-dark">
            <tr>
              <th>ID</th>
              <th>Email</th>
              <th>Uloga</th>
              <th>Akcije</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="user in users" :key="user.id">
              <td>{{ user.id }}</td>
              <td>{{ user.email }}</td>
              <td>{{ user.role }}</td>
              <td>
                <router-link
                  :to="`/edit-user/${user.id}`"
                  class="btn btn-primary btn-sm"
                >
                  Izmeni
                </router-link>

                <button
                  @click="deleteUser(user.id)"
                  class="btn btn-danger btn-sm"
                >
                  Obriši
                </button>
              </td>
            </tr>
          </tbody>
        </table>

        <!-- Dugme za dodavanje novog korisnika -->
        <div class="text-end">
          <router-link to="/add-user" class="btn btn-success">
            Dodaj Novog Korisnika
          </router-link>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.table-dark {
  background-color: #343a40 !important;
  color: #fff;
}

.table-dark th,
.table-dark td {
  text-align: center;
}

.btn:hover {
  filter: brightness(1.1);
}
</style>
