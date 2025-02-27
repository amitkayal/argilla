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
  <span class="span__text">
    <entity-highlight
      v-if="token.entity"
      :class="[
        'color_' + (tag_color % this.$entitiesMaxColors),
        matchQueryClass,
      ]"
      :span="token"
      :dataset="dataset"
      :record="record"
    /><template v-else v-for="t in token.tokens">{{ t.text }}</template
    ><template>{{ token.charsBetweenTokens }}</template>
  </span>
</template>

<script>
export default {
  props: {
    record: {
      type: Object,
      required: true,
    },
    dataset: {
      type: Object,
      required: true,
    },
    token: {
      type: Object,
      required: true,
    },
  },
  computed: {
    tag_color() {
      return this.dataset.entities.filter(
        (entity) => entity.text === this.token.entity.label
      )[0].colorId;
    },
    queryScore() {
      return this.dataset.query.score;
    },
    matchQueryClass() {
      if (this.queryScore) {
        const score = this.token.entity.score;
        return score >= this.queryScore.from && score <= this.queryScore.to
          ? undefined
          : "excluded";
      }
    },
  },
};
</script>
<style lang="scss" scoped>
.entities {
  &__selector {
    position: absolute;
    left: -35%;
    top: 1em;
    min-width: 220px;
    z-index: 9;
    background: palette(grey, 600);
    font-weight: 600;
    padding: 0.8em;
    border-radius: 1px;
    &__container {
      @include font-size(14px);
      line-height: 1em;
      display: inline-block;
      white-space: pre-line;
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
      transition: all 0.2s ease;
      padding: 0.5em;
      position: relative;
      cursor: pointer;
      margin-top: 2px;
      margin-bottom: 2px;
      &.suggestion {
        margin-bottom: 0.5em;
      }
      span {
        cursor: pointer !important;
      }
    }
  }
}
.span {
  position: relative;
  display: inline;
  line-height: 18px;
  font-size: 0;
  &__text {
    display: inline;
    position: relative;
    @include font-size(16px);
    margin: 0 -1.5px;
    padding: 0 1.5px;
  }
  &__whitespace {
    @include font-size(16px);
    cursor: default !important;
  }
}

// highlight word with overlay
.zindex3 {
  z-index: 3;
}
.selected {
  cursor: pointer;
  position: relative;
  background: palette(grey, 600);
  .prediction :deep(.highlight__content) {
    background: palette(grey, 600);
  }
  .span__text {
    background: palette(grey, 600);
  }
  .span__whitespace {
    background: palette(grey, 600);
  }
}
.last-selected {
  .span__whitespace {
    background: none;
  }
}
// .span span {
//   display: inline;
// }
.list__item--annotation-mode span span {
  cursor: text;
}
.entity {
  &.non-selectable,
  &.non-selectable--show-sort-code {
    cursor: default;
    pointer-events: none;
  }
  &__sort-code {
    margin-left: auto;
    margin-right: 0;
    .non-selectable & {
      display: none;
    }
  }
}
// ner colors

$colors: 50;
$hue: 360;
@for $i from 1 through $colors {
  $rcolor: hsla(($colors * $i) + calc($hue * $i / $colors), 100%, 88%, 1);
  .color_#{$i - 1} {
    &.annotation :deep(.highlight__content) {
      background: $rcolor;
    }
    &.prediction :deep(.highlight__content) {
      padding-bottom: 3px;
      border-bottom: 5px solid $rcolor;
      position: relative;
      &:after {
        content: "";
        border-top: 1px solid darken($rcolor, 50%);
        position: absolute;
        top: 26px;
        left: 0;
        right: 0;
      }
    }
    &.annotation :deep(.highlight__tooltip:after) {
      border-color: $rcolor transparent transparent transparent;
    }
    &.prediction :deep(.highlight__tooltip:after) {
      border-color: transparent transparent $rcolor transparent;
    }
    &.excluded :deep() {
      .highlight__content {
        &:after {
          content: none;
        }
      }
    }
    &.active,
    &.tag:hover {
      border: 2px solid darken($rcolor, 50%);
    }
  }
  .tag.color_#{$i - 1} span {
    background: $rcolor;
  }
  .entities__selector__option.color_#{$i - 1} {
    background: $rcolor;
    border: 2px solid $rcolor;
  }
  .entities__selector__option.color_#{$i - 1} {
    &:active,
    &.active,
    &:hover {
      border: 2px solid mix(black, $rcolor, 20%);
    }
  }
  .color_#{$i - 1} :deep(.highlight__tooltip) {
    background: $rcolor;
  }
}
</style>
