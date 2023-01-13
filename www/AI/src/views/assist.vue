<script>
import { mapActions, mapState } from 'pinia'
import { useUserStore } from '../stores/store'
export default {
  // feed those
  // props: ['channels', 'chatLog'],
  data() {
    return {
      userInput: '',
    }
  },
  computed: {
    ...mapState(useUserStore, ['netResp']),
  },
  updated() {
  },
  methods: {
    ...mapActions(useUserStore, ['assistSend']),
    assistSendWs(){
      // console.log(this.userInput)
      this.assistSend('assist', 'gal', '50', '0.9', this.userInput)
    }
  },
}
</script>
<template>
  <div style="position: absolute;height: 90vh;width: 163vh;right: 3vw;background: #ffffff00;top: 5vh;">
    <div style="position:absolute;top: 3%;background: #333333a1;width:100%;height: 92%;backdrop-filter:blur(5px);">
      <div style="position:absolute;top:0%;width:100%;height:100%;">{{netResp}}</div>
      <textarea style="background: transparent;resize: none;border: 0 none;outline: none;position:absolute;top:0%;width:100%;height:100%;" v-model="userInput" @keypress="assistSendWs">user RESPONSE</textarea>
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
