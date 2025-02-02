<script setup>
import { ref } from "vue";
import axios from "axios";
import { useRouter } from "vue-router";

const email = ref("");
const password = ref("");
const confirmPassword = ref("");
const showPassword = ref(false);
const showConfirmPassword = ref(false);
const router = useRouter();

const handleRegister = async () => {
  if (password.value !== confirmPassword.value) {
    alert("Lozinke se ne podudaraju!");
    return;
  }

  try {
    // Slanje podataka sa lozinkom kao 'lozinka'
    const response = await axios.post("/api/register", {
      email: email.value,
      lozinka: password.value, // Koristi 'lozinka' kao parametar
    });

    // Spremanje JWT tokena u localStorage
    localStorage.setItem("jwt_token", response.data.token);

    // Preusmeravanje na login stranicu
    router.push("/login");
  } catch (error) {
    console.error("Greška pri registraciji:", error);

    // Prikazivanje odgovarajuće greške korisniku
    if (error.response && error.response.data.error) {
      alert(error.response.data.error); // Prikazivanje greške sa servera
    } else {
      alert("Došlo je do greške pri registraciji. Pokušajte ponovo.");
    }
  }
};
</script>

<template>
  <div class="container">
    <div class="login-container">
      <!-- Logo -->
      <div class="brand-logo text-center mb-4">
        <img
          src="../assets/logo-removebg-preview.png"
          alt="Finance Logo"
          class="logo-sm img-fluid"
        />
      </div>

      <!-- Registration Form -->
      <form
        @submit.prevent="handleRegister"
        class="border p-4 rounded shadow-sm bg-light"
      >
        <!-- Email -->
        <div class="mb-3">
          <label for="email" class="form-label">Email</label>
          <input
            type="email"
            class="form-control"
            id="email"
            v-model="email"
            placeholder="Unesi svoj email"
            required
          />
        </div>

        <!-- Password -->
        <div class="mb-3">
          <label for="password" class="form-label">Lozinka</label>
          <input
            :type="showPassword ? 'text' : 'password'"
            class="form-control"
            id="password"
            v-model="password"
            placeholder="Unesi svoju lozinku"
            required
          />
          <div class="form-check">
            <input
              type="checkbox"
              class="form-check-input"
              id="show-password"
              v-model="showPassword"
            />
            <label class="form-check-label" for="show-password"
              >Prikaži lozinku</label
            >
          </div>
        </div>

        <!-- Confirm Password -->
        <div class="mb-3">
          <label for="confirm-password" class="form-label"
            >Potvrdi lozinku</label
          >
          <input
            :type="showConfirmPassword ? 'text' : 'password'"
            class="form-control"
            id="confirm-password"
            v-model="confirmPassword"
            placeholder="Potvrdi svoju lozinku"
            required
          />
          <div class="form-check">
            <input
              type="checkbox"
              class="form-check-input"
              id="show-confirm-password"
              v-model="showConfirmPassword"
            />
            <label class="form-check-label" for="show-confirm-password"
              >Prikaži potvrdu lozinke</label
            >
          </div>
        </div>

        <!-- Submit Button -->
        <div class="d-grid">
          <button type="submit" class="btn btn-primary">Registruj se</button>
        </div>

        <!-- Login Redirect -->
        <div class="mt-3 text-center">
          <small>
            <span>Već imate nalog? </span>
            <router-link to="/login" class="text-decoration-none"
              >Prijavite se</router-link
            >
          </small>
        </div>
      </form>
    </div>
  </div>
</template>

<style scoped>
.login-container {
  max-width: 400px;
  margin: 0 auto;
}
</style>
