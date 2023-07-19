<script setup lang="ts">
import {
  NConfigProvider,
  NLayout,
  NLayoutHeader,
  NLayoutFooter,
  NLayoutSider,
  NSpace,
  darkTheme,
  NMenu,
  NCard,
  NMessageProvider,
  NPageHeader,
} from 'naive-ui'

import {
  h
} from 'vue'
import {
  RouterLink
} from 'vue-router'

const menuOptions = [
  {
    label: () => h(RouterLink, { to: '/cost' }, 'Prompts Cost'),
    key: 'cost',
  },
]

</script>

<template>
  <NConfigProvider
    :theme="darkTheme"
  >
    <NSpace vertical>
      <NLayout>
        <NLayoutHeader inverted bordered >
          <NPageHeader>
            <template #title>
              <span class="text-16">
                Tokenizer Caclulator
              </span>
            </template>
          </NPageHeader>
        </NLayoutHeader>
        <NLayout has-sider>
          <NLayoutSider
            bordered
            show-trigger
            inverted
            collapsed
            :collapsed-width="48"
            :width="240"
          >
            <NMenu inverted :options="menuOptions"></NMenu>
          </NLayoutSider>
          <NLayout>
            <NCard style="min-height: 90vh;">
              <NMessageProvider>
                <router-view></router-view>
              </NMessageProvider>
            </NCard>
          </NLayout>
        </NLayout>
        <NLayoutFooter inverted bordered>
          © 2023 Tokenizer Project. Made with ❤️ by <a href="https://github.com/meduoduo" > Miduoduo </a> community, Inc.
        </NLayoutFooter>
      </NLayout>
    </NSpace>
  </NConfigProvider>
</template>

<style scoped>
.n-layout-header,
.n-layout-footer {
  background: rgba(128, 128, 128, 0.2);
  padding: 16px;
}

.n-layout-sider {
  background: rgba(128, 128, 128, 0.3);
}

.n-layout-content {
  background: rgba(128, 128, 128, 0.4);
}
</style>