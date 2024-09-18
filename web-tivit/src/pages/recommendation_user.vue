<template>
  <q-page class="q-pa-md flex flex-center">
    <q-card class="q-pa-md" style="max-width: 600px;">
      <!-- Header com mensagem e avatar -->
      <q-card-section class="row items-center q-pb-md">
        <q-avatar size="56px" color="primary" icon="person" />
        <div class="q-ml-md">
          <div class="text-h5">{{ sanitize(jsonData.message) }}</div>
        </div>
      </q-card-section>

      <!-- Informações do usuário -->
      <q-card-section>
        <q-list bordered>
          <q-item>
            <q-item-section avatar>
              <q-icon name="person" />
            </q-item-section>
            <q-item-section>
              <q-item-label><strong>Name:</strong> {{ sanitize(jsonData.data.name) }}</q-item-label>
              <q-item-label caption><strong>Email:</strong> {{ sanitize(jsonData.data.email) }}</q-item-label>
            </q-item-section>
          </q-item>
        </q-list>
      </q-card-section>

      <!-- Separador -->
      <q-separator spaced />

      <!-- Lista de compras -->
      <q-card-section>
        <div class="text-h6 q-mb-md">Purchases</div>
        <q-list bordered>
          <q-item v-for="purchase in jsonData.data.purchases" :key="purchase.id" clickable>
            <q-item-section avatar>
              <q-icon name="shopping_cart" />
            </q-item-section>
            <q-item-section>
              <q-item-label>{{ sanitize(purchase.item) }}</q-item-label>
              <q-item-label caption>Price: ${{ sanitize(purchase.price) }}</q-item-label>
            </q-item-section>
          </q-item>
        </q-list>
      </q-card-section>

      <!-- Recomendations Section -->
      <q-card-section>
        <div class="text-h6 q-mb-md">Recommended Products</div>
        <q-chip
          v-for="(recommendation, index) in recommendations"
          :key="index"
          class="q-mb-xs"
          color="primary"
          text-color="white"
          icon="star"
        >
          {{ sanitize(recommendation) }}
        </q-chip>
      </q-card-section>
    </q-card>
  </q-page>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      jsonData: {
        message: "",
        data: {
          name: "",
          email: "",
          purchases: [],
        },
      },
      recommendations: [],
      loading: true,
      error: null,
    };
  },
  methods: {
    // Método para sanitizar dados antes de exibir
    sanitize(value) {
      const div = document.createElement('div');
      div.textContent = value;
      return div.innerHTML;
    },
    // Método para buscar os dados do usuário da API
    async fetchUserData() {
      try {
        const response = await axios.get('http://localhost:8001/sync-user?username=user&password=userpass');
        this.jsonData = response.data;
        await this.fetchRecommendations(this.jsonData.data.name);
        this.loading = false;
      } catch (error) {
        this.error = 'Failed to load user data.';
        this.loading = false;
      }
    },
    // Método para buscar recomendações da API
    async fetchRecommendations(userName) {
      try {
        const response = await axios.get(`http://localhost:8001/user-recommendations?name=${encodeURIComponent(userName)}`);
        this.recommendations = response.data.recommendations;
      } catch (error) {
        this.error = 'Failed to load recommendations.';
      }
    }
  },
  mounted() {
    // Busca os dados da API assim que o componente for montado
    this.fetchUserData();
  }
};
</script>

<style scoped>
.q-card {
  width: 100%;
  max-width: 600px;
  box-shadow: 0px 4px 12px rgba(0, 0, 0, 0.1);
}
.q-item {
  transition: transform 0.2s;
}
.q-item:hover {
  transform: translateY(-4px);
  box-shadow: 0px 2px 8px rgba(0, 0, 0, 0.2);
}
</style>
