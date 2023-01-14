<script>
import { mapActions, mapState } from 'pinia'
import { useUserStore } from '../stores/store'
export default {
  // feed those
  // props: ['channels', 'chatLog'],
  data() {
    return {
      userInput: '',
      lastSub:0,
    }
  },

  computed: {
    ...mapState(useUserStore, ['netResp']),
  },
  mounted(){
    setInterval(()=>{
      if(this.netResp.replace(/\s/g,'').includes(this.userInput.replace(/\s/g,'')))
        return
      // console.log(this.netResp, this.userInput)
      this.assistSend('assist', 'gal', '80', '0.9', this.userInput)
      console.log('sending'+ this.userInput)
    },500)
  },
  updated() {
  },
  methods: {
    ...mapActions(useUserStore, ['assistSend']),
    assistSendWs(){
      /*
      clearTimeout(this.lastSub)
      this.lastSub = setTimeout(()=>{
        this.assistSend('assist', 'gal', '50', '0.9', this.userInput)
      }, 500
      )
*/
      
    },
    recvInput(e){
      this.userInput = e.target.innerText
    },
    syncIn(){
      this.userInput = this.netResp;
    }
  },
}
</script>
<template>
  <div style="position: absolute;height: 90vh;width: 163vh;right: 3vw;background: #ffffff00;top: 5vh;">
    <div style="position:absolute;top: 3%;background: #333333a1;width:100%;height: 92%;backdrop-filter:blur(5px);overflow-y:auto;">
      <div style="position: relative;top: 0%;width: 100%;height: 100%;font-family: font3;font-size: 3vh;font-weight:900;color: #e5e5e56e;left: 0%;">{{netResp}}</div>
      <div contenteditable style="outline:none;position: absolute;top: 0%;width: 100%;height: 100%;font-family: font3;font-size: 3vh;font-weight:900;left: 0%;color: #e5e5e5;" @input="recvInput" @keyup="assistSendWs" @keydown.tab.prevent="syncIn">{{ this.userInput }}</div>
    </div>
    <div
      style="position:absolute;top: 95%;background: #000000a1;width:100%;height: 5%;filter: drop-shadow(rgba(255, 255, 255, 0.3) 14px 11px 4px);left: 0%;">
    </div>
    <div
      style="position:absolute;top: 1%;background: #fffdfdc4;width: 100%;height: 2%;filter: drop-shadow(rgba(255, 255, 255, 0.3) 14px 11px 4px);left: 0%;">
      PUBMED GPT GALACTICA</div>
    <div
      style="position:absolute;top: -6.1%;background: #fffdfdc4;width: 9%;height: 7.1%;filter: drop-shadow(rgba(255, 255, 255, 0.3) 14px 11px 4px);left: 0%;">
      MODEL</div>
  </div>
</template>

<style>

</style>
