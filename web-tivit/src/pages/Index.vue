<template>
  <q-page class="q-pa-md flex flex-center">
    <q-card class="q-pa-md" style="max-width: 800px;">
      <!-- Header com logo e título -->
      <q-card-section class="row items-center justify-center q-pb-md">
        <div class="q-ml-md text-center">
          <div class="text-h4 q-mb-md">Welcome to the Tivit App!</div>
          <div class="text-subtitle2">Manage your purchases, track reports, and get personalized recommendations.</div>
        </div>
      </q-card-section>

      <!-- Separador -->
      <q-separator spaced />

      <!-- Cards com funcionalidades principais -->
      <q-card-section class="q-pt-md">
        <div class="row justify-around">
          <!-- User Management -->
          <q-card class="q-pa-sm" style="width: 240px" clickable>
            <q-card-section class="row items-center">
              <q-avatar size="56px" color="secondary">
                <q-icon name="person" />
              </q-avatar>
              <div class="q-ml-md">
                <div class="text-h6">User Panel</div>
                <div class="text-caption">Manage your account and purchases.</div>
              </div>
            </q-card-section>
          </q-card>

          <!-- Admin Management -->
          <q-card class="q-pa-sm" style="width: 240px" clickable>
            <q-card-section class="row items-center">
              <q-avatar size="56px" color="primary">
                <q-icon name="admin_panel_settings" />
              </q-avatar>
              <div class="q-ml-md">
                <div class="text-h6">Admin Panel</div>
                <div class="text-caption">Track reports and activities.</div>
              </div>
            </q-card-section>
          </q-card>
        </div>
      </q-card-section>

      <!-- Separador -->
      <q-separator spaced />

      <!-- Recomendação Geral -->
      <q-card-section class="q-pt-md">
        <div class="text-h6 q-mb-md">Featured Recommendations</div>
        <q-list bordered>
          <q-item clickable v-ripple>
            <q-item-section avatar>
              <q-icon name="star" color="warning" />
            </q-item-section>
            <q-item-section>
              <q-item-label>Top Products</q-item-label>
              <q-item-label caption>Check out our most popular products.</q-item-label>
            </q-item-section>
          </q-item>

          <q-item clickable v-ripple>
            <q-item-section avatar>
              <q-icon name="trending_up" color="positive" />
            </q-item-section>
            <q-item-section>
              <q-item-label>Sales Report</q-item-label>
              <q-item-label caption>View detailed sales reports and analytics.</q-item-label>
            </q-item-section>
          </q-item>
        </q-list>
      </q-card-section>
    </q-card>
  </q-page>
</template>

<script>
export default {
  name: 'PageIndex'
}
</script>

<style scoped>
.q-page {
  background-color: #f5f5f5;
}
.q-card {
  box-shadow: 0px 4px 12px rgba(0, 0, 0, 0.1);
  transition: transform 0.2s ease;
}
.q-card:hover {
  transform: translateY(-4px);
  box-shadow: 0px 8px 16px rgba(0, 0, 0, 0.2);
}
.q-avatar {
  box-shadow: 0px 4px 8px rgba(0, 0, 0, 0.1);
}
</style>
