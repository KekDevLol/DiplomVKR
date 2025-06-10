<template>
  <div class="main-page-container flex-column-start">
    <header-navigation />
    <div class="center-content-container py-5">
      <div class="pb-3">
        <div class="login-btn-container flex-row-start">
          <v-tabs v-model="tab" color="black">
            <v-tab class="login-btn" value="login" >Авторизация</v-tab>
            <v-tab class="login-btn" value="sign">Регистрация</v-tab>
          </v-tabs>
        </div>
      </div>
      <v-tabs-window v-model="tab">
        <v-tabs-window-item value="login">
          <div class="text-field-container px-4 pt-3">
            <label for="email-login">Email</label>
            <v-text-field
                v-model="email"
                class="login-text-field pt-2"
                placeholder="Ваш email"
                id="email-login"
                variant="outlined"
            />
          </div>
          <div class="text-field-container px-4 pt-3">
            <label for="email-login">Пароль</label>
            <v-text-field
                v-model="password"
                class="login-text-field pt-2"
                placeholder="Ваш пароль"
                id="email-login"
                variant="outlined"
            />
          </div>
          <v-btn class="login-btn-auth">Вход</v-btn>
        </v-tabs-window-item>
        <v-tabs-window-item value="sign">
          <div class="text-field-container px-4 pt-3">
            <label for="email-login">Email</label>
            <v-text-field
                v-model="email"
                class="login-text-field pt-2"
                placeholder="Ваш email"
                id="email-login"
                variant="outlined"
            />
          </div>
          <div class="text-field-container px-4 pt-3">
            <label for="email-login">Пароль</label>
            <v-text-field
                v-model="password"
                class="login-text-field pt-2"
                placeholder="Ваш пароль"
                id="email-login"
                variant="outlined"
            />
          </div>
          <div class="text-field-container px-4 pt-3">
            <label for="email-login-confirm">Пароль</label>
            <v-text-field
                v-model="confirmPassword"
                class="login-text-field pt-2"
                placeholder="Подтверждение пароля"
                id="email-login-confirm"
                variant="outlined"
            />
          </div>
          <v-btn class="login-btn-auth">Вход</v-btn>
        </v-tabs-window-item>
      </v-tabs-window>
    </div>
  </div>
</template>

<script>
import HeaderNavigation from "../components/HeaderNavigation.vue";

export default {
  name: "Login",
  components: {
    Header: HeaderNavigation,
  },
  data() {
    return {
      tab: null,
      email: null,
      password: null,
      confirmPassword: null,
    }
  },
  watch: {
    tab(val) {
      console.log(val)
    }
  }
}
</script>

<style scoped>
.login-btn-auth {
  padding: 0 16px;
  background-color: #1A80E5;
  color: white;
  border-radius: 20px;
  width: 480px;
  height: 40px;
}

.login-btn-container {
  gap: 32px;
  padding: 0 16px;
  border-bottom: 1px solid var(--login-gray);
}

.text-field-container {
  width: 480px;
}

.login-text-field :deep .v-field {
  border: 1px solid #DBE0E5 !important;
  border-radius: 12px !important;
  height: 56px;
}

.login-btn {
  text-transform: none;
  height: 53px;
}
</style>