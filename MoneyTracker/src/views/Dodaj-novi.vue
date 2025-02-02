<script setup>
import { ref } from "vue";
import axios from "axios";
import { useRouter } from "vue-router";

const naziv = ref("");
const iznos = ref("");
const tip = ref("prihod");

const router = useRouter();

const dodajNovuTransakciju = async () => {
  const transakcijaData = {
    naziv: naziv.value,
    iznos: iznos.value,
    tip: tip.value,
  };

  try {
    const token = localStorage.getItem("jwt_token");
    if (!token) {
      alert("Niste prijavljeni. Molimo prijavite se ponovo.");
      return;
    }

    await axios.post("/api/dodaj-novi", transakcijaData, {
      headers: { Authorization: `Bearer ${token}` },
    });

    router.push("/korisnici");
  } catch (error) {
    console.error("Greška prilikom dodavanja transakcije:", error);
    alert("Došlo je do greške prilikom dodavanja transakcije.");
  }

  naziv.value = "";
  iznos.value = "";
  tip.value = "prihod";
};
</script>

<template>
  <div class="container col-lg-2 col-lg-12">
    <div class="my-5">
      <h3>Nova transakcija</h3>
    </div>

    <form @submit.prevent="dodajNovuTransakciju">
      <div class="form-group">
        <label for="naziv">Naziv</label>
        <input type="text" class="form-control" v-model="naziv" required />
      </div>

      <div class="form-group">
        <label for="iznos">Iznos</label>
        <input type="text" class="form-control" v-model="iznos" required />
      </div>

      <div class="form-group">
        <label for="tip">Tip transakcije</label>
        <select class="form-control" v-model="tip" required>
          <option value="prihod">Prihod</option>
          <option value="rashod">Rashod</option>
        </select>
      </div>

      <button type="submit" class="btn btn-primary">Sačuvaj</button>
    </form>
  </div>
</template>

<style scoped></style>
