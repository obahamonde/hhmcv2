<template>
    <div v-if="show" col start dark:invert br bg-gray-100 fixed sh p-4 rounded m-4 mx-24 fade-in-right>
      <strong>{{ auth0User.name }}</strong>
      <strong>{{ auth0User.email }}</strong>
      <button
        row
        icon
        @click="logout()"
        v-if="isAuthenticated"
        text="red"
        hover:text-red-700
      >
        <Icon icon="mdi-logout" x2 text-warning hover:text-danger />
      </button>
    </div>
    <button
      rf
      @click="loginWithRedirect()"
      v-if="!isAuthenticated"
      x4
      m-4
      fixed
      br
      fade-in-up
    >
      <Icon icon="mdi-login" x2 text-success hover:text-primary />
    </button>
    <div @click="show = !show" cp m-4 fixed br z-50 fade-in-up>
      <img :src="auth0User.picture" :alt="auth0User.name" v-if="isAuthenticated" rf sh x4 />
    </div>
  </template>
  <script setup lang="ts">
  import { useAuth0 } from "@auth0/auth0-vue";
  const {
    user: auth0User,
    isAuthenticated,
    loginWithRedirect,
    logout,
    getAccessTokenSilently,
  } = useAuth0();
  const show = ref(false);
  const { notify, setState } = useStore();
  onMounted(async () => {
    if (isAuthenticated) {
      await postUser();
    }
  });
  
  const postUser = async () => {
    const token = await getAccessTokenSilently();
    const { data } = await useFetch(
        `/api/auth?token=${token}`
    ).json()
    const user = unref(data);
      setState({ user });
      notify(`Welcome ${user.name}!`, "success");
    
    }

  </script>