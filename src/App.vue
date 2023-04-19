<template>
          <nav class="bl fixed bg-white outline text-black sh px-4 py-2 z-50 rounded">
            <RouterLink mx-4 to="/">Home</RouterLink>
            <RouterLink mx-4 to="/piano">Piano</RouterLink>
            <RouterLink mx-4 to="/audio">Audio</RouterLink>
          </nav>
          <RouterView />
          <HAuth />
</template>
<style global>
.router-link-exact-active {
    color: #000;
    font-weight: bold;
}

</style>