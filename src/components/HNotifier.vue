<script setup lang="ts">
import { useStore } from "~/composables";
const { state } = useStore();
</script>
<template>
  <section>
    <VCard
      style="z-index: 9999"
      v-for="(n, index) in state.notifications"
      :style="{ top: index * 15 + 'px' }"
      :class="n.status"
      class="noti"
    >
      {{ n.message }}
      <Icon
        :icon="
          n.status === 'error'
            ? 'mdi-alert-circle'
            : n.status === 'warning'
            ? 'mdi-alert'
            : n.status === 'success'
            ? 'mdi-check-circle'
            : 'mdi-information-variant'
        "
        class="rf scale cp tr absolute"
        @click="state.notifications.pop()"
      />
    </VCard>
  </section>
</template>
<style scoped>
.noti {
  @apply tr fixed m-4 py-4 px-2 row center sh border-2 border-solid w-96;
}
.info {
  @apply border-teal-700 bg-gray-300 text-teal-700;
}
.success {
  @apply border-green-700 bg-lime-300 text-green-700;
}
.warning {
  @apply border-orange-500 bg-yellow-300 text-orange-500;
}
.error {
  @apply border-red-800 bg-red-300 text-red-800;
}
</style>
