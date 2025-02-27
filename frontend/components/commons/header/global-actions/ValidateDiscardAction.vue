<!--
  - coding=utf-8
  - Copyright 2021-present, the Recognai S.L. team.
  -
  - Licensed under the Apache License, Version 2.0 (the "License");
  - you may not use this file except in compliance with the License.
  - You may obtain a copy of the License at
  -
  -     http://www.apache.org/licenses/LICENSE-2.0
  -
  - Unless required by applicable law or agreed to in writing, software
  - distributed under the License is distributed on an "AS IS" BASIS,
  - WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
  - See the License for the specific language governing permissions and
  - limitations under the License.
  -->

<template>
  <div
    class="validate-discard-actions"
    :class="[
      selectedRecords.length ? '' : 'validate-discard-actions--disabled',
    ]"
  >
    <base-checkbox
      v-model="allSelected"
      :disabled="!visibleRecords.length"
      class="list__item__checkbox"
    ></base-checkbox>
    <slot name="first" :selectedRecords="selectedRecords" />
    <base-button
      :disabled="!allowValidation"
      class="primary outline small validate-discard-actions__button"
      @click="onValidate"
      >Validate</base-button
    >
    <base-button
      class="primary outline small validate-discard-actions__button"
      @click="onDiscard"
      >Discard</base-button
    >
    <slot name="last" :selectedRecords="selectedRecords" />
    <p v-if="selectedRecords.length" class="validate-discard-actions__text">
      Actions will apply to the
      <span>{{ selectedRecords.length }} records</span> selected
    </p>
  </div>
</template>
<script>
import { mapActions } from "vuex";
import "assets/icons/math-plus";
import "assets/icons/refresh";

export default {
  props: {
    dataset: {
      type: Object,
      required: true,
    },
    position: {
      type: String,
      default: "before",
    },
    allowValidation: {
      type: Boolean,
      default: true,
    },
  },
  data: () => ({
    allSelected: false,
  }),
  computed: {
    visibleRecords() {
      return this.dataset.visibleRecords;
    },
    selectedRecords() {
      // Return selected records.
      return this.visibleRecords.filter((record) => record.selected);
    },
  },
  watch: {
    visibleRecords(newValue) {
      this.allSelected = newValue.length
        ? newValue.every((record) => record.selected)
        : false;
    },
    allSelected(allSelected) {
      if (
        allSelected ||
        this.visibleRecords.every((record) => record.selected)
      ) {
        this.updateRecords({
          dataset: this.dataset,
          records: this.visibleRecords.map((record) => {
            return { ...record, selected: this.allSelected };
          }),
        });
      }
    },
  },
  methods: {
    ...mapActions({
      updateRecords: "entities/datasets/updateDatasetRecords",
    }),
    onDiscard() {
      this.$emit("discard-records", this.selectedRecords);
    },
    async onValidate() {
      this.$emit("validate-records", this.selectedRecords);
    },
  },
};
</script>
<style lang="scss" scoped>
.validate-discard-actions {
  display: flex;
  align-items: center;
  width: 100%;
  .re-checkbox {
    position: relative;
    left: 0;
    top: 0;
    margin: 0 $base-space 0 0;
  }
  &__select {
    margin-left: 0.8em;
    :deep(.dropdown__header) {
      max-height: 33px;
      font-weight: 500;
      min-width: 170px;
      @include font-size(13px);
      border: 1px solid palette(blue, 500);
      color: palette(blue, 500);
      &:after {
        border-color: palette(blue, 500);
      }
    }
  }
  &__button {
    margin-left: $base-space;
    margin-right: $base-space;
    cursor: pointer;
    &:hover {
      border-color: $primary-color;
    }
    &:first-of-type {
      margin-right: 0;
    }
  }
  &__text {
    @include font-size(13px);
    margin: 0 $base-space;
    color: $black-54;
    span {
      font-weight: 700;
      color: $black-54;
    }
  }
  &--disabled {
    .validate-discard-actions__button,
    .validate-discard-actions__select {
      pointer-events: none;
      opacity: 0.5;
    }
  }
}
</style>
