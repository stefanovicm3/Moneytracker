<script setup>
import { ref } from "vue";
import { useRouter } from "vue-router";
import axios from "axios";

const email = ref("");
const password = ref("");
const showPassword = ref(false);
const rememberMe = ref(false);
const flashMessages = ref([]);

const router = useRouter();

const decodeToken = (token) => {
  const payload = token.split(".")[1];
  const decoded = JSON.parse(atob(payload));
  return decoded;
};

const handleLogin = async () => {
  try {
    const response = await axios.post("http://localhost:5000/login", {
      email: email.value,
      password: password.value,
    });

    console.log("Odgovor sa servera:", response.data);

    const token = response.data.token;
    if (token) {
      localStorage.setItem("jwt_token", token);

      const decodedToken = decodeToken(token);
      localStorage.setItem("role", decodedToken.role);

      console.log(
        "Token sačuvan u localStorage:",
        localStorage.getItem("jwt_token")
      );
      console.log(
        "Rola sačuvana u localStorage:",
        localStorage.getItem("role")
      );

      if (response.data.message === "Login successful") {
        router.push("/korisnici");
      } else {
        flashMessages.value = ["Pogrešan email ili lozinka"];
      }
    } else {
      console.log("Token nije prisutan u odgovoru sa servera");
    }
  } catch (error) {
    console.error("Greška prilikom prijavljivanja:", error);
    flashMessages.value = [
      error.response
        ? error.response.data.message
        : "Greška prilikom prijavljivanja.",
    ];
  }
};

const togglePasswordVisibility = () => {
  showPassword.value = !showPassword.value;
};
</script>

<template>
  <div class="container">
    <div v-if="flashMessages.length" class="alert alert-danger" role="alert">
      <strong v-for="(message, index) in flashMessages" :key="index">{{
        message
      }}</strong>
    </div>

    <div class="login-container">
      <div class="brand-logo">
        <img
          src="../assets/logo-removebg-preview.png"
          alt="Finance Logo"
          class="logo-sm img-fluid logo"
        />
      </div>
      <form @submit.prevent="handleLogin">
        <div class="mb-3">
          <label for="email" class="form-label">Email</label>
          <input
            type="text"
            class="form-control"
            id="email"
            v-model="email"
            placeholder="Enter your email"
            required
          />
        </div>

        <div class="mb-3">
          <label for="password" class="form-label">Password</label>
          <input
            :type="showPassword ? 'text' : 'password'"
            class="form-control"
            id="password"
            v-model="password"
            placeholder="Enter your password"
            required
          />
          <!-- Show password checkbox -->
          <div class="form-check">
            <input
              type="checkbox"
              class="form-check-input"
              id="show-password"
              v-model="showPassword"
              @click="togglePasswordVisibility"
            />
            <label class="form-check-label" for="show-password"
              >Prikaži lozinku</label
            >
          </div>
        </div>

        <!-- Remember Me -->
        <div class="mb-3 form-check">
          <input
            type="checkbox"
            class="form-check-input"
            id="remember"
            v-model="rememberMe"
          />
          <label class="form-check-label" for="remember">Remember me</label>
        </div>

        <!-- Login Button -->
        <div class="d-grid">
          <button type="submit" class="btn btn-primary">Login</button>
        </div>

        <!-- Additional Links -->
        <div class="mt-3 text-center">
          <small>
            <router-link :to="`/forgot-password`" class="text-decoration-none">
              Forgot Password?
            </router-link>
            |
            <router-link :to="`/register`" class="text-decoration-none"
              >Sign Up</router-link
            >
          </small>
        </div>
      </form>
    </div>
  </div>
</template>

<style scoped>
.login-container {
  background-color: #fff;
  padding: 30px;
  width: 1300px;
  border-radius: 8px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
}
.logo {
  width: 40rem;
  height: auto;
}
</style>
