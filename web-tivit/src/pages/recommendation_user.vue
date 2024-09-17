<template>
  <q-page class="q-pa-md flex flex-center">
    <q-card class="q-pa-md" style="max-width: 600px;">
      <!-- Header com mensagem e avatar -->
      <q-card-section class="row items-center q-pb-md">
        <q-avatar size="56px" color="primary" icon="person" />
        <div class="q-ml-md">
          <div class="text-h5">{{ jsonData.message }}</div>
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
              <q-item-label><strong>Name:</strong> {{ jsonData.data.name }}</q-item-label>
              <q-item-label caption><strong>Email:</strong> {{ jsonData.data.email }}</q-item-label>
            </q-item-section>
          </q-item>
        </q-list>
      </q-card-section>

      <!-- Separador -->
      <q-separator spaced />

      <!-- Lista de compras -->
      <q-card-section>
        <div class="text-h6 q-mb-md">Recent Purchases</div>
        <q-list bordered>
          <q-item v-for="purchase in jsonData.data.purchases" :key="purchase.id" clickable>
            <q-item-section avatar>
              <q-icon name="shopping_cart" />
            </q-item-section>
            <q-item-section>
              <q-item-label>{{ purchase.item }}</q-item-label>
              <q-item-label caption>{{ formatCurrency(purchase.price) }}</q-item-label>
            </q-item-section>
            <q-item-section side>
              <q-icon name="chevron_right" />
            </q-item-section>
          </q-item>
        </q-list>
      </q-card-section>

      <!-- Recomendations Section -->
      <q-card-section>
        <div class="text-h6 q-mb-md">Recommended Products</div>
        <q-chip
          v-for="(recommendation, index) in jsonData.recommendations"
          :key="index"
          class="q-mb-xs"
          color="primary"
          text-color="white"
          icon="thumb_up"
        >
          {{ recommendation }}
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
        message: "Hello, user!",
        data: {
          name: "John Doe",
          email: "john@example.com",
          purchases: [
            { id: 1, item: "Laptop", price: 2500 },
            { id: 2, item: "Smartphone", price: 1200 },
          ],
        },
        recommendations: ["Tablet", "Smartwatch"],
      },
    };
  },
  methods: {
    formatCurrency(value) {
      return `R$ ${value.toFixed(2)}`;
    },
  },
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
