<template>
  <p class="records-counter" v-if="total > 0">
    Records ({{ total | formatNumber }})
  </p>
</template>

<script>
export default {
  props: {
    total: {
      type: Number,
      required: true,
    },
  },
};
</script>

<style lang="scss" scoped>
.records-counter {
  color: $black-54;
  margin-left: auto;
  margin-right: 0;
  display: block;
  text-align: right;
  @include font-size(13px);
}
</style>
