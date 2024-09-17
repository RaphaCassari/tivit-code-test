<template>
  <q-page class="q-pa-md flex flex-center">
    <q-card class="q-pa-md" style="max-width: 600px;">
      <!-- Header com mensagem e avatar -->
      <q-card-section class="row items-center q-pb-md">
        <q-avatar size="56px" color="primary" icon="admin_panel_settings" />
        <div class="q-ml-md">
          <div class="text-h5">{{ sanitize(jsonData.message) }}</div>
        </div>
      </q-card-section>

      <!-- Informações do administrador -->
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

      <!-- Lista de relatórios -->
      <q-card-section>
        <div class="text-h6 q-mb-md">Recent Reports</div>
        <q-list bordered>
          <q-item v-for="report in jsonData.data.reports" :key="report.id" clickable>
            <q-item-section avatar>
              <q-icon :name="getStatusIcon(report.status)" />
            </q-item-section>
            <q-item-section>
              <q-item-label>{{ sanitize(report.title) }}</q-item-label>
              <q-item-label caption :class="getStatusClass(report.status)">
                Status: {{ sanitize(report.status) }}
              </q-item-label>
            </q-item-section>
            <q-item-section side>
              <q-icon name="chevron_right" />
            </q-item-section>
          </q-item>
        </q-list>
      </q-card-section>

      <!-- Recomendations Section -->
      <q-card-section>
        <div class="text-h6 q-mb-md">Recommended Reports</div>
        <q-chip
          v-for="(recommendation, index) in jsonData.recommendations"
          :key="index"
          class="q-mb-xs"
          color="primary"
          text-color="white"
          icon="assessment"
        >
          {{ sanitize(recommendation) }}
        </q-chip>
      </q-card-section>
    </q-card>
  </q-page>
</template>

<script>
export default {
  data() {
    return {
      jsonData: {
        message: "Hello, admin!",
        data: {
          name: "Admin Master",
          email: "admin@example.com",
          reports: [
            { id: 1, title: "Monthly Sales", status: "Completed" },
            { id: 2, title: "User Activity", status: "Pending" },
          ],
        },
        recommendations: ["User Activity", "Monthly Sales"],
      },
    };
  },
  methods: {
    // Método para sanitizar dados antes de exibir
    sanitize(value) {
      const div = document.createElement('div');
      div.textContent = value;
      return div.innerHTML;
    },
    // Determina o ícone com base no status do relatório
    getStatusIcon(status) {
      return status === "Completed" ? "check_circle" : "hourglass_empty";
    },
    // Aplica classes diferentes com base no status
    getStatusClass(status) {
      return status === "Completed" ? "text-positive" : "text-warning";
    }
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
