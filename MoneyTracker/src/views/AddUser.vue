<script setup>
import { ref } from "vue";
import Swal from "sweetalert2";
import { useRouter } from "vue-router";

const user = ref({
  email: "",
  password: "",
  role: "user",
});

const message = ref("");
const messageClass = ref("");

const router = useRouter();

const addUser = async () => {
  try {
    const response = await fetch("/api/add_user", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${localStorage.getItem("jwt_token")}`,
      },
      body: JSON.stringify(user.value),
    });

    if (!response.ok) {
      const errorData = await response.json();
      throw new Error(errorData.error || "Greška prilikom dodavanja korisnika");
    }

    message.value = "Korisnik uspešno dodat!";
    messageClass.value = "alert-success";
    Swal.fire("Uspešno!", "Korisnik je uspešno dodat.", "success");

    user.value = { email: "", password: "", role: "user" };

    router.push("/users");
  } catch (error) {
    message.value = error.message;
    messageClass.value = "alert-danger";
    console.error("Greška:", error);

    Swal.fire(
      "Greška!",
      error.message || "Došlo je do greške prilikom dodavanja korisnika.",
      "error"
    );
  }
};
</script>

<template>
  <div class="container my-5">
    <h1 class="text-center mb-4">Dodaj Novog Korisnika</h1>

    <div v-if="message" :class="messageClass" class="alert">
      {{ message }}
    </div>

    <form @submit.prevent="addUser">
      <div class="mb-3">
        <label for="email" class="form-label">Email</label>
        <input
          v-model="user.email"
          type="email"
          class="form-control"
          id="email"
          name="email"
          required
        />
      </div>
      <div class="mb-3">
        <label for="password" class="form-label">Lozinka</label>
        <input
          v-model="user.password"
          type="password"
          class="form-control"
          id="password"
          name="password"
          required
        />
      </div>
      <div class="mb-3">
        <label for="role" class="form-label">Uloga</label>
        <select
          v-model="user.role"
          class="form-select"
          id="role"
          name="role"
          required
        >
          <option value="user">User</option>
          <option value="admin">Admin</option>
        </select>
      </div>
      <button type="submit" class="btn btn-primary">Dodaj Korisnika</button>
    </form>
  </div>
</template>
