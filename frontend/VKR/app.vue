<template>
  <NuxtLayout>
    <v-app>
      <NuxtPage />
    </v-app>
  </NuxtLayout>
</template>

<style>
@import url('https://fonts.googleapis.com/css2?family=Manrope:wght@200..800&display=swap');

:root {
  --blue: #1A80E5;
  --black: #121417;
  --gray: #637587;
  --white: white;
  --gray-light: #F0F2F4;
  --login-gray: #E5E8EB;
}

NuxtPage {
  font-family: 'Manrope', 'Times New Roman', sans-serif;
  font-size: 16px;
  line-height: 24px;
  color: var(--black);
}

.center-content-container {
  width: 960px;
}

.small-text-gray {
  font-size: 14px;
  line-height: 21px;
  color: var(--gray);
}

.small-text-black {
  font-size: 14px;
  line-height: 21px;
  color: var(--black);
}

.small-text-bold {
  font-size: 14px;
  line-height: 21px;
  font-weight: bold;
}

.title {
  font-size: 32px;
  line-height: 40px;
  color: var(--black);
}

.main-page-container {
  width: 100%;
  height: 100%;
  gap: 40px;
}

.flex-column-start {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: start;
}

.flex-column-center {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
}

.flex-column-end {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: end;
}

.flex-row-start {
  display: flex;
  flex-direction: row;
  align-items: center;
  justify-content: start;
}

.flex-row-center {
  display: flex;
  flex-direction: row;
  align-items: center;
  justify-content: center;
}

.flex-row-end {
  display: flex;
  flex-direction: row;
  align-items: center;
  justify-content: end;
}
</style>