<script setup>
import { ref } from "vue";
import { useRouter } from "vue-router";

const email = ref("");
const router = useRouter();

const resetPassword = async () => {
  try {
    const response = await fetch("/api/forgot-password", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ email: email.value }),
    });

    if (response.ok) {
      alert("Link za resetovanje lozinke je poslat na vaš email.");
      router.push("/login");
    } else {
      const errorData = await response.json();
      alert(errorData.message || "Došlo je do greške pri resetovanju lozinke.");
    }
  } catch (error) {
    console.error("Greška pri slanju zahteva:", error);
    alert("Došlo je do greške, pokušajte ponovo.");
  }
};
</script>
<template>
  <div class="container">
    <div class="login-container">
      <h3>Zaboravljena lozinka</h3>
      <form @submit.prevent="resetPassword">
        <div class="mb-3">
          <label for="email" class="form-label">Email</label>
          <input
            type="email"
            class="form-control"
            id="email"
            v-model="email"
            required
            placeholder="Unesite vaš email"
          />
        </div>
        <div class="d-grid">
          <button type="submit" class="btn btn-primary">Resetuj lozinku</button>
        </div>
      </form>
    </div>
  </div>
</template>

<style scoped>
.login-container {
  max-width: 400px;
  margin: 50px auto;
  padding: 20px;
  border: 1px solid #ddd;
  border-radius: 5px;
  background-color: #fff;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}
</style>
