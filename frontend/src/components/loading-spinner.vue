<template>
  <div class="spinner-wrap">
    <div class="spinner"></div>
  </div>
</template>

<style scoped>
.spinner-wrap {
  display: flex;
  justify-content: center;
  padding: 3rem 0;
}

.spinner {
  width: 24px;
  height: 24px;
  border: 2px solid var(--border);
  border-top-color: var(--accent);
  border-radius: 50%;
  animation: spin 0.6s linear infinite;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}
</style>
