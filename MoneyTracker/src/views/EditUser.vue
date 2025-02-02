<script setup>
import { ref, onMounted } from "vue";
import { useRoute, useRouter } from "vue-router";
import Swal from "sweetalert2";

const email = ref("");
const password = ref("");
const role = ref("user");

const route = useRoute();
const router = useRouter();

const loadUserData = async () => {
  try {
    const response = await fetch(`/api/users/${route.params.userId}`, {
      method: "GET",
      headers: {
        Authorization: `Bearer ${localStorage.getItem("jwt_token")}`,
        "Content-Type": "application/json",
      },
    });

    if (response.ok) {
      const userData = await response.json();
      email.value = userData.email;
      role.value = userData.role;
    } else {
      Swal.fire({
        title: "Greška!",
        text: "Nismo mogli da učitamo podatke o korisniku.",
        icon: "error",
      });
    }
  } catch (error) {
    console.error("Greška pri učitavanju korisničkih podataka:", error);
    Swal.fire({
      title: "Greška!",
      text: "Došlo je do greške prilikom učitavanja podataka.",
      icon: "error",
    });
  }
};

onMounted(() => {
  loadUserData(route.params.userId);
});

const updateUser = async () => {
  try {
    const response = await fetch(`/api/edit_user/${route.params.userId}`, {
      method: "POST",
      headers: {
        Authorization: `Bearer ${localStorage.getItem("jwt_token")}`,
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        email: email.value,
        password: password.value,
        role: role.value,
      }),
    });

    if (response.ok) {
      Swal.fire({
        title: "Uspešno!",
        text: "Korisnik je uspešno izmenjen.",
        icon: "success",
      }).then(() => {
        router.push("/users");
      });
    } else {
      Swal.fire({
        title: "Greška!",
        text: "Došlo je do greške prilikom izmene korisnika.",
        icon: "error",
      });
    }
  } catch (error) {
    console.error("Greška prilikom ažuriranja korisnika:", error);
    Swal.fire({
      title: "Greška!",
      text: "Došlo je do greške u vezi sa serverom.",
      icon: "error",
    });
  }
};
</script>
<template>
  <div class="container my-5">
    <h1 class="text-center mb-4">Izmeni Korisnika</h1>

    <form @submit.prevent="updateUser">
      <div class="mb-3">
        <label for="email" class="form-label">Email</label>
        <input
          type="email"
          class="form-control"
          id="email"
          v-model="email"
          required
        />
      </div>
      <div class="mb-3">
        <label for="password" class="form-label">Lozinka</label>
        <input
          type="password"
          class="form-control"
          id="password"
          v-model="password"
          required
        />
      </div>
      <div class="mb-3">
        <label for="role" class="form-label">Uloga</label>
        <select class="form-select" id="role" v-model="role" required>
          <option value="user">User</option>
          <option value="admin">Admin</option>
        </select>
      </div>
      <button type="submit" class="btn btn-primary">Izmeni Korisnika</button>
    </form>
  </div>
</template>
