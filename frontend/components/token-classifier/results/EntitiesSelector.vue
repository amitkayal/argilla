<template>
  <span class="entities__selector__container">
    <div class="entities__selector">
      <ul v-if="formattedEntities.length" class="entities__selector__options">
        <li v-if="suggestedEntity" @click="selectEntity(suggestedEntity)">
          <entity-label
            :label="suggestedEntity.text"
            shortcut="space"
            :class="[
              'entities__selector__option',
              'suggestion',
              activeEntity === -1 ? 'active' : null,
            ]"
            :color="`color_${suggestedEntity.colorId % $entitiesMaxColors}`"
          />
        </li>
        <li
          v-else-if="lastSelectedEntity.text"
          @click="selectEntity(lastSelectedEntity)"
        >
          <entity-label
            :label="lastSelectedEntity.text"
            shortcut="space"
            :class="[
              'entities__selector__option',
              'suggestion',
              activeEntity === -1 ? 'active' : null,
            ]"
            :color="`color_${lastSelectedEntity.colorId % $entitiesMaxColors}`"
          />
        </li>
        <li
          v-for="(entity, index) in formattedEntities"
          tabindex="0"
          :focused="activeEntity === index"
          :key="index"
          @click="selectEntity(entity)"
        >
          <entity-label
            :label="entity.text"
            :shortcut="activeEntity === index ? 'enter' : entity.shortCut"
            :class="[
              'entities__selector__option',
              activeEntity === index ? 'active' : null,
            ]"
            :color="`color_${entity.colorId % $entitiesMaxColors}`"
          />
        </li>
      </ul>
      <div v-else class="entities__selector--empty">
        <svgicon name="danger" width="17" height="17" />
        <p>No labels available</p>
      </div>
    </div>
  </span>
</template>

<script>
import "assets/icons/danger";
import { mapActions } from "vuex";
export default {
  data: () => ({
    activeEntity: -1,
  }),
  props: {
    dataset: {
      type: Object,
      required: true,
    },
    token: {
      type: Object,
      required: true,
    },
    suggestedLabel: {
      type: String,
    },
    formattedEntities: {
      type: Array,
    },
    showEntitiesSelector: {
      type: Boolean,
      required: true,
    },
  },
  computed: {
    lastSelectedEntity() {
      return this.dataset.lastSelectedEntity;
    },
    suggestedEntity() {
      return this.formattedEntities.find(
        (ent) => ent.text === this.suggestedLabel
      );
    },
  },
  mounted() {
    window.addEventListener("keydown", this.keyDown);
  },
  destroyed() {
    window.removeEventListener("keydown", this.keyDown);
  },
  methods: {
    ...mapActions({
      updateLastSelectedEntity:
        "entities/token_classification/updateLastSelectedEntity",
    }),
    async selectEntity(entityLabel) {
      await this.updateLastSelectedEntity({
        dataset: this.dataset,
        lastSelectedEntity: entityLabel,
      });
      this.token.entity
        ? this.$emit("changeEntityLabel", this.token.entity, entityLabel.text)
        : this.$emit("selectEntity", entityLabel.text);
      this.resetActiveEntity();
    },
    resetActiveEntity() {
      this.activeEntity = -1;
    },
    keyDown(event) {
      const cmd = String.fromCharCode(event.keyCode).toUpperCase();
      if (this.showEntitiesSelector && cmd) {
        const element = document.getElementsByClassName("active");
        event.preventDefault();
        // enter
        if (event.keyCode === 13) {
          if (this.activeEntity !== -1) {
            this.selectEntity(this.formattedEntities[this.activeEntity]);
          }
          //space
        } else if (event.keyCode === 32) {
          if (this.suggestedEntity) {
            this.selectEntity(this.suggestedEntity);
          } else if (this.lastSelectedEntity) {
            this.selectEntity(this.lastSelectedEntity);
          }
          //down
        } else if (
          event.keyCode === 40 &&
          this.activeEntity + 1 < this.formattedEntities.length
        ) {
          this.activeEntity++;
          if (element[0] && element[0].offsetTop >= 90) {
            element[0].parentNode.scrollTop = element[0].offsetTop - 2;
          }
          //up
        } else if (event.keyCode === 38 && this.activeEntity >= 0) {
          this.activeEntity--;
          if (element[0]) {
            element[0].parentNode.scrollTop =
              element[0].offsetTop - element[0].offsetHeight - 8;
          }
        } else {
          const entity = this.formattedEntities.find((t) => t.shortCut === cmd);
          if (entity) {
            this.selectEntity(entity);
          }
        }
      }
    },
  },
};
</script>
<style lang="scss" scoped>
.entities {
  &__selector {
    min-width: 220px;
    background: palette(grey, 600);
    font-weight: 600;
    padding: 0.8em;
    border-radius: $border-radius;
    &__container {
      @include font-size(14px);
      line-height: 1em;
      display: inline-block;
      white-space: pre-line;
      position: absolute;
      left: -30%;
      top: 2em;
      z-index: 9;
    }
    &__options {
      max-height: 142px;
      overflow-y: scroll;
      padding-left: 0;
      margin: 0;
      overscroll-behavior: contain;
      position: relative;
      @extend %hide-scrollbar;
    }
    &__option {
      display: flex;
      margin-bottom: 2px;
      &.suggestion {
        margin-bottom: 0.5em;
      }
      :deep(.shortcut) {
        margin-left: auto;
      }
    }
    &--empty {
      display: flex;
      align-items: center;
      .svg-icon {
        margin-right: 0.5em;
      }
      p {
        margin: 0;
        font-weight: 400;
      }
    }
  }
}
</style>
