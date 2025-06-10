<template>
  <div class="header-container flex-row-start">
    <div class="logo flex-row-start">
      <svg width="14" height="15" viewBox="0 0 14 15" fill="none" xmlns="http://www.w3.org/2000/svg">
        <path fill-rule="evenodd" clip-rule="evenodd" d="M0.333333 0.833333H4.7778V5.2778H9.2222V9.7222H13.6667V14.1667H0.333333V0.833333Z" fill="#121417"/>
      </svg>
      <span class="logo-text">AgentCraft</span>
      <div style="margin-left: auto; gap: 16px; display: flex">
        <v-btn variant="text">Дашборд</v-btn>
        <v-btn variant="text">Агенты</v-btn>
        <v-btn variant="text">Администирование</v-btn>
        <v-btn color="#1A80E5">Новый агент</v-btn>
      </div>
    </div>
  </div>
</template>

<script>

export default {
  name: "HeaderNavigation",
}

</script>

<style scoped>
.header-container {
  width: 100%;
  padding: 12px 40px;
  justify-content: space-between !important;
}

.logo {
  gap: 16px;
  width: 100%;
}

.logo-text {
  font-size: 18px;
  line-height: 24px;
  font-weight: bold;
}
</style>