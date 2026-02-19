<script setup>
const props = defineProps({
  tag: { type: Object, required: true },
  active: { type: Boolean, default: false },
})
</script>

<template>
  <span
    class="badge"
    :class="{ active }"
    :style="{
      '--tag-color': tag.color,
      borderColor: active ? tag.color : 'transparent',
      background: active ? tag.color + '22' : tag.color + '11',
    }"
  >
    {{ tag.name }}
  </span>
</template>

<style scoped>
.badge {
  font-family: var(--font-mono);
  font-size: 0.7rem;
  font-weight: 500;
  padding: 0.2rem 0.5rem;
  border-radius: 4px;
  border: 1px solid transparent;
  color: var(--tag-color);
  cursor: pointer;
  transition: all 0.15s ease;
  user-select: none;
}

.badge:hover {
  border-color: var(--tag-color);
  background: var(--tag-color);
  color: var(--bg);
}

.badge.active {
  border-color: var(--tag-color);
}
</style>
