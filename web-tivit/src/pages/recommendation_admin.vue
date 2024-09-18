<template>
  <q-page class="q-pa-md flex flex-center">
    <q-card class="q-pa-md" style="max-width: 600px;">
      <!-- Header com mensagem e avatar -->
      <q-card-section class="row items-center q-pb-md">
        <q-avatar size="56px" color="secondary" icon="admin_panel_settings" />
        <div class="q-ml-md">
          <div class="text-h5">{{ sanitize(jsonData.message) }}</div>
        </div>
      </q-card-section>

      <!-- Informações do administrador -->
      <q-card-section>
        <q-list bordered>
          <q-item>
            <q-item-section avatar>
              <q-icon name="admin_panel_settings" />
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

      <!-- Lista de relatórios -->
      <q-card-section>
        <div class="text-h6 q-mb-md">Reports</div>
        <q-list bordered>
          <q-item v-for="report in jsonData.data.reports" :key="report.id" clickable>
            <q-item-section avatar>
              <q-icon name="description" />
            </q-item-section>
            <q-item-section>
              <q-item-label>{{ sanitize(report.title) }}</q-item-label>
              <q-item-label caption>Status: {{ sanitize(report.status) }}</q-item-label>
            </q-item-section>
          </q-item>
        </q-list>
      </q-card-section>

      <!-- Recomendations Section -->
      <q-card-section>
        <div class="text-h6 q-mb-md">Recommended Reports</div>
        <q-chip
          v-for="(recommendation, index) in recommendations"
          :key="index"
          class="q-mb-xs"
          color="secondary"
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
          reports: [],
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
    // Método para buscar os dados do administrador da API
    async fetchAdminData() {
      try {
        const response = await axios.get('http://localhost:8001/sync-admin?username=admin&password=adminpass');
        this.jsonData = response.data;
        await this.fetchRecommendations(this.jsonData.data.name);
        this.loading = false;
      } catch (error) {
        this.error = 'Failed to load admin data.';
        this.loading = false;
      }
    },
    // Método para buscar recomendações da API
    async fetchRecommendations(adminName) {
      try {
        const response = await axios.get(`http://localhost:8001/admin-recommendations?name=${encodeURIComponent(adminName)}`);
        this.recommendations = response.data.recommendations;
      } catch (error) {
        this.error = 'Failed to load recommendations.';
      }
    }
  },
  mounted() {
    // Busca os dados da API assim que o componente for montado
    this.fetchAdminData();
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
