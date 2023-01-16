<script setup>
import { RouterLink, RouterView } from 'vue-router'
</script>

<template>
  <header>

  </header>
  AI
  <div style="position:absolute;width:100%;height:100%;background:black;overflow:hidden;top:0%;left:0;">
    <img src="gothic-dark-sky-death-brass-wallpaper-trees-religion-grave-angels-wallpapers-photography-wings-cemetery-graveyard.jpg" style="width:100%;position:absolute;top:0;filter:brightness(80%)">
    <RouterView />

    <div class="navigat" style="position:absolute;top:0;left:2%;height:100%;width:40vh;transform: perspective(59vh);transform-style:preserve-3d;pointer-events: none;">
      <div style="position:absolute;height:80%;top:10%;width: 1px;left:4vw;background: #ffffff2b;"></div>
      <RouterLink to="/assist" class="button" style="pointer-events: auto; position: absolute; top: 20%; left: 10%; height: 10%; width: 70%; background: rgba(241, 241, 241, 0.74); transform: rotateY(7deg); filter: drop-shadow(rgba(255, 255, 255, 0.3) 14px 11px 4px);overflow:hidden;">
        <div style="position:absolute;top: -4%;left: 25%;font-weight:900;color: #000000db;font-family: font8;font-size: 7vh;filter: drop-shadow(rgba(0, 0, 0, 0.6) 14px 11px 8px);">支援</div>
        <div style="position:absolute;bottom: 4%;left: 25%;font-weight:900;color: #000000db;font-family: font11;font-size: 1vh;letter-spacing: 0.1vh;filter: drop-shadow(rgba(0, 0, 0, 0.6) 14px 11px 8px);">SENTENCE COMPLETION</div>
        <div style="position:absolute;bottom: 49%;right: 7%;font-weight:900;color: #000000db;font-family: font10;font-size: 1vh;letter-spacing: 0.1vh;transform: rotateZ(90deg);background: #000000a3;color:white;padding:1%;filter: drop-shadow(rgba(0, 0, 0, 0.6) 14px -11px 8px);">ASSIST #0</div><img style="position:absolute;top: -4%;left: -6%;opacity: 0.1;width: 46%;" src="/handshake-angle-solid.svg">
      </RouterLink>
      <RouterLink to="/annotate" class="button" style="pointer-events: auto; position:absolute;top: 34%;left:10%;height:10%;width:70%;background: #f1f1f1bd;transform: rotateY(7deg);filter: drop-shadow(14px 11px 4px rgba(255,255,255,0.3));overflow:hidden;"> 
    <div style="position:absolute;top: -4%;left: 25%;font-weight:900;color: #000000db;font-family: font8;font-size: 7vh;filter: drop-shadow(rgba(0, 0, 0, 0.6) 14px 11px 8px);">要約</div>
<div style="position:absolute;bottom: 4%;left: 25%;font-weight:900;color: #000000db;font-family: font11;font-size: 1vh;letter-spacing: 0.1vh;filter: drop-shadow(rgba(0, 0, 0, 0.6) 14px 11px 8px);">SCIENCE IN A NUTSHELL</div><div style="position:absolute;bottom: 49%;right: 7%;font-weight:900;color: #000000db;font-family: font10;font-size: 1vh;letter-spacing: 0.1vh;transform: rotateZ(90deg);background: #000000a3;color:white;padding:1%;filter: drop-shadow(rgba(0, 0, 0, 0.6) 14px -11px 8px);">SUMRZ #1</div><img style="position:absolute;top: 0%;left: -2%;opacity: 0.1;width: 26%;" src="/book-solid.svg">
      </RouterLink>
      <div class="sep" style="position:absolute;top: 83%;left: 35%;height: 0.1%;width: 79%;background: #ffffffad;transform: rotateY(7deg);filter: drop-shadow(14px 11px 4px rgba(255,255,255,0.8));">
      </div>
    </div>
  </div>

</template>

<style scoped>

</style>
