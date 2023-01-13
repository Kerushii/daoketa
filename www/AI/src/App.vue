<script setup>
import { RouterLink, RouterView } from 'vue-router'
</script>

<template>
  <header>

  </header>
  AI
  <div style="position:absolute;width:100%;height:100%;background:black;overflow:hidden;top:0%;left:0;">
    <img src="gothic-dark-sky-death-brass-wallpaper-trees-religion-grave-angels-wallpapers-photography-wings-cemetery-graveyard.jpg"
      style="width:100%;position:absolute;top:0;filter:brightness(80%)">
    <RouterView />

    <div class="navigat"
      style="position:absolute;top:0;left:2%;height:100%;width:40vh;transform: perspective(59vh);transform-style:preserve-3d;">
      <div style="position:absolute;height:80%;top:10%;width: 1px;left:4vw;background: #ffffff2b;"></div>
      <RouterLink to="/assist" class="button"
        style="position:absolute;top:20%;left:10%;height:10%;width:70%;background: #f1f1f1bd;transform: rotateY(7deg);filter: drop-shadow(14px 11px 4px rgba(255,255,255,0.3));"> ASSIST
      </RouterLink>
      <RouterLink to="/annotate" class="button"
        style="position:absolute;top: 34%;left:10%;height:10%;width:70%;background: #f1f1f1bd;transform: rotateY(7deg);filter: drop-shadow(14px 11px 4px rgba(255,255,255,0.3));"> ANNOTATE
      </RouterLink>
      <div class="sep"
        style="position:absolute;top: 83%;left: 35%;height: 0.1%;width: 79%;background: #ffffffad;transform: rotateY(7deg);filter: drop-shadow(14px 11px 4px rgba(255,255,255,0.8));">
      </div>
    </div>
  </div>

</template>

<style scoped>

</style>
