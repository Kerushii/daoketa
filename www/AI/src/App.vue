<script>
import { RouterLink, RouterView } from 'vue-router'
import { mapActions, mapState } from 'pinia'
import { useUserStore } from './stores/store'

export default {
  // feed those
  // props: ['channels', 'chatLog'],
  data() {
    return {
      username: '',
      userName2beSubmitted:'',
      password:'',
      activeSelector:'ass',
    }
  },

  computed: {
    ...mapState(useUserStore, ['netRespAssist','loggedIn']),

  },
  mounted() {

  },
  updated() {
  },
  methods: {
    ...mapActions(useUserStore, [ 'login']),
    setActiveSelector(se){
this.activeSelector=se;
    },
    submitUsrName(){
      this.userName2beSubmitted = this.username

      console.log('received username')
    },
    clearunsuccessfulLogin(){
      if(this.loggedIn)
        return
      this.userName2beSubmitted=''
    },
    logMeIn(){
      this.login(this.userName2beSubmitted, this.password)
    }

  },
}
</script>

<template>
  <header>

  </header>
  AI
  <div style="position:absolute;width:100%;height:100%;background:black;overflow:hidden;top:0%;left:0;" @click='clearunsuccessfulLogin'>
    <img src="/gothic-dark-sky-death-brass-wallpaper-trees-religion-grave-angels-wallpapers-photography-wings-cemetery-graveyard.jpg" style="width:100%;position:absolute;top:0;filter:brightness(80%)">
    <RouterView />

    <div class="navigat" style="position:absolute;top:0;left:2%;height:100%;width:40vh;transform: perspective(59vh);transform-style:preserve-3d;pointer-events: none;">
      <div style="position:absolute;height:80%;top:10%;width: 1px;left:4vw;background: #ffffff2b;"></div>
      <RouterLink to="/assist" :class="{acti: activeSelector =='ass',inacti: activeSelector !=='ass', }" style="pointer-events: auto; position: absolute; top: 20%; left: 10%; height: 10%; width: 70%; background: rgba(241, 241, 241, 0.74); transform: rotateY(7deg); filter: drop-shadow(rgba(255, 255, 255, 0.3) 14px 11px 4px);overflow:hidden;" @click='setActiveSelector("ass")'>
        <div style="position:absolute;top: -4%;left: 25%;font-weight:900;color: #000000db;font-family: font8;font-size: 7vh;filter: drop-shadow(rgba(0, 0, 0, 0.6) 14px 11px 8px);">支援</div>
        <div style="position:absolute;bottom: 4%;left: 25%;font-weight:900;color: #000000db;font-family: font11;font-size: 1vh;letter-spacing: 0.1vh;filter: drop-shadow(rgba(0, 0, 0, 0.6) 14px 11px 8px);">SENTENCE COMPLETION</div>
        <div style="position:absolute;bottom: 49%;right: 7%;font-weight:900;color: #000000db;font-family: font10;font-size: 1vh;letter-spacing: 0.1vh;transform: rotateZ(90deg);background: #000000a3;color:white;padding:1%;filter: drop-shadow(rgba(0, 0, 0, 0.6) 14px -11px 8px);">ASSIST #0</div><img style="position:absolute;top: -4%;left: -6%;opacity: 0.1;width: 46%;" src="/handshake-angle-solid.svg">
      </RouterLink>
      <RouterLink to="/annotate" :class="{acti: activeSelector =='anno',inacti: activeSelector !=='anno', }" style="pointer-events: auto; position:absolute;top: 34%;left:10%;height:10%;width:70%;background: #f1f1f1bd;transform: rotateY(7deg);filter: drop-shadow(14px 11px 4px rgba(255,255,255,0.3));overflow:hidden;"  @click='setActiveSelector("anno")'>
        <div style="position:absolute;top: -4%;left: 25%;font-weight:900;color: #000000db;font-family: font8;font-size: 7vh;filter: drop-shadow(rgba(0, 0, 0, 0.6) 14px 11px 8px);">要約</div>
        <div style="position:absolute;bottom: 4%;left: 25%;font-weight:900;color: #000000db;font-family: font11;font-size: 1vh;letter-spacing: 0.1vh;filter: drop-shadow(rgba(0, 0, 0, 0.6) 14px 11px 8px);">SCIENCE IN A NUTSHELL</div>
        <div style="position:absolute;bottom: 49%;right: 7%;font-weight:900;color: #000000db;font-family: font10;font-size: 1vh;letter-spacing: 0.1vh;transform: rotateZ(90deg);background: #000000a3;color:white;padding:1%;filter: drop-shadow(rgba(0, 0, 0, 0.6) 14px -11px 8px);">SUMRZ #1</div><img style="position:absolute;top: 0%;left: -2%;opacity: 0.1;width: 26%;" src="/book-solid.svg">
      </RouterLink>
      <div class="sep" style="position:absolute;top: 83%;left: 35%;height: 0.1%;width: 79%;background: #ffffffad;transform: rotateY(7deg);filter: drop-shadow(14px 11px 4px rgba(255,255,255,0.8));">
      </div>
    </div>
  </div>
  <div style="position:absolute;/* background: white; */width: 32vh;height: 5vh;overflow:hidden;right: 3%;top: 0%;mix-blend-mode:screen;">
    <input type="text" v-model='username' placeholder="LOGIN" style="position:absolute;border:0;outline:0;background:transparent;font-family: font2;font-size: 3vh;color:white;text-align:center;width:100%;" @keypress.enter.stop ="submitUsrName">
    <div v-if="userName2beSubmitted" style="position:absolute;height:100%;width:100%;">
    <input   v-model='password' type="password" placeholder='password' style="position:absolute;border:0;outline:0;background:transparent;font-family: font8;font-size: 0.5vh;color: white;text-align:center;width:100%;top: 32%;background:black;width: 100%;font-weight:900;letter-spacing: 0.8vh;right:0;" @keypress.enter.stop ="logMeIn"></div>

    <div v-if="!userName2beSubmitted" style="position:absolute;border:0;outline:0;background:transparent;font-family: font8;font-size: 0.9vh;color: black;text-align:center;width:100%;top: 71%;background: white;width: 100%;font-weight:900;letter-spacing: 1.4vh;right: 0%;text-align:center;padding-right: 0vh;">CONNECTION</div>
    <div v-if="userName2beSubmitted && !loggedIn" style="position:absolute;border:0;outline:0;background:transparent;font-family: font8;font-size: 0.9vh;color: black;text-align:center;width:100%;top: 71%;background: white;width: 100%;font-weight:900;letter-spacing: 1.4vh;right: 0%;text-align:center;padding-right: 0vh;">INPUT PASSWORD</div>
    <div v-if="userName2beSubmitted && loggedIn" style="position:absolute;border:0;outline:0;background:transparent;font-family: font8;font-size: 0.9vh;color: black;text-align:center;width:100%;top: 71%;background: white;width: 100%;font-weight:900;letter-spacing: 1.4vh;right: 0%;text-align:center;padding-right: 0vh;">CONNECTED</div>

  </div>
</template>

<style scoped>
.acti{
  opacity:1;
}

.inacti{
  opacity:0.5;
}
</style>
