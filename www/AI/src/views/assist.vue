<script>
import { mapActions, mapState } from 'pinia'
import { useUserStore } from '../stores/store'
export default {
  // feed those
  // props: ['channels', 'chatLog'],
  data() {
    return {
      userInput: '',
      querry:0,
      aiType: 'gal',
      menuEntry: 'model',
      completionLen: 50,
      temp: 90,
      continuousIntegration: false,
    }
  },

  computed: {
    ...mapState(useUserStore, ['netRespAssist']),
    netProcess() {
      function removeLastn(input) {
        var str = input
        var word = '\n';
        var newWord = '';

        // find the index of last time word was used
        // please note lastIndexOf() is case sensitive
        var n = str.lastIndexOf(word);

        // slice the string in 2, one from the start to the lastIndexOf
        // and then replace the word in the rest
        str = str.slice(0, n) + str.slice(n).replace(word, newWord);
        return str
      }
      // split this.userinput into 2 parts: the last 1024 letters and all the previous letters

      return this.userInput + this.netRespAssist
    }
  },
  mounted() {
    let currentInput = ''
    this.querry = setInterval(() => {

      if(currentInput == this.userInput)
        return
      if(!this.continuousIntegration)
        return
      function removeLastn(input) {
        var str = input
        var word = '\n';
        var newWord = '';

        // find the index of last time word was used
        // please note lastIndexOf() is case sensitive
        var n = str.lastIndexOf(word);

        // slice the string in 2, one from the start to the lastIndexOf
        // and then replace the word in the rest
        str = str.slice(0, n) + str.slice(n).replace(word, newWord);
        return str
      }


      this.assistSend(this.aiType, this.completionLen, this.temp / 100,  this.userInput )
      //this.assistSend(this.aiType, this.completionLen, this.temp / 100, removeLastn(this.userInput)) //when we send, replace all br with \n so ai can understand
      // console.log('sending' + this.userInput)
      currentInput = this.userInput
    }, 1000)
  
  },
  unmounted(){
    clearInterval(this.querry)
  },
  updated() {
  },
  methods: {
    ...mapActions(useUserStore, ['assistSend']),
    setAIType(aiType) {
      this.aiType = aiType

    },
    setMenuEntry(m) {
      this.menuEntry = m
    },
    ifIShouldSend(){
      const cur = this.userInput
      setTimeout(()=>{
        if (cur ==this.userInput)
          this.assistSend(this.aiType, this.completionLen, this.temp / 100,  this.userInput )
        
      }, 1000)
    },

    syncIn() {
      this.userInput = this.userInput+this.netRespAssist //when we insert, all userinputs become </br> instead
    },
    setCI(p) {
      this.continuousIntegration = p
    },

  },
}
</script>
<template>
  <div style="position: absolute;height: 90vh;width: 163vh;right: 3vw;background: #ffffff00;top: 5vh;">
    <div class="typeArea" style="position: absolute;top: 5%;background: rgb(51 51 51 / 91%);width: 100%;height: 92%;backdrop-filter: blur(5px);overflow-y: auto;">
      <textarea  style="white-space: pre-line; background: transparent; position: relative;top: 0%;width: 93%;height: 99999%;font-family: font3;font-size: 3vh;font-weight:900;color: #e5e5e56e;left: 0%;padding:3%;">{{ netProcess }}</textarea>
      <textarea v-model='userInput' style="background: transparent;outline: none; position: absolute; top: 0%; width: 93%; height: 99999%; font-family: font3; font-size: 3vh; font-weight: 900; left: 0%; color: rgb(229, 229, 229); padding: 3%;filter:drop-shadow(rgba(255, 255, 255, 0.3) 14px 11px 4px);" @keydown.tab.prevent="syncIn" @keyup="ifIShouldSend"></textarea>
    </div>
    <div style="position: absolute;top: 97%;background: rgba(0, 0, 0, 0.63);width: 100%;height: 5%;filter: drop-shadow(rgba(255, 255, 255, 0.3) 14px 11px 4px);left: 0%;">
    </div>
    <div class="menuEntryOff" v-if="menuEntry != 'model'" style="position:absolute;top:-6.1%;background: rgb(100 100 100);width:9%;height:7.1%;filter:drop-shadow(rgba(0, 0, 0, 0.3) 14px 11px 4px);left: 0%;overflow:hidden;" @click="setMenuEntry('model')">
      <div style="position: absolute;top: 19%;right: 16%;font-family: font2;filter: drop-shadow(rgba(0, 0, 0, 0.6) 10px 9px 4px);font-size: 1.3vh;">MODEL</div>
      <div style="position:absolute;top:49%;left:30%;font-family:font5;text-align:right;width:54%;font-size:0.7vh;filter:drop-shadow(rgba(0, 0, 0, 0.6) 10px 9px 4px);">SET GENERATION CONFIGS</div><img src="/network-wired-solid.svg" style="position:absolute;bottom:16%;left:-3%;height:64%;opacity:0.05;">
    </div>
    <div class="menuEntryOff" v-if="menuEntry != 'gen'" style="position:absolute;top:-6.1%;background: rgb(100 100 100);width:9%;height:7.1%;filter:drop-shadow(rgba(0, 0, 0, 0.3) 14px 11px 4px);left: 9%;overflow:hidden;" @click="setMenuEntry('gen')">
      <div style="position: absolute;top: 19%;right: 16%;font-family: font2;filter: drop-shadow(rgba(0, 0, 0, 0.6) 10px 9px 4px);font-size: 1.3vh;">GENERATION</div>
      <div style="position:absolute;top:49%;left:30%;font-family:font5;text-align:right;width:54%;font-size:0.7vh;filter:drop-shadow(rgba(0, 0, 0, 0.6) 10px 9px 4px);">SET GENERATION CONFIGS</div><img src="/network-wired-solid.svg" style="position:absolute;bottom:16%;left:-3%;height:64%;opacity:0.05;">
    </div>
    <div class="menuEntryOff" v-if="menuEntry != 'sys'" style="position:absolute;top:-6.1%;background: rgb(100 100 100);width:9%;height:7.1%;filter:drop-shadow(rgba(0, 0, 0, 0.3) 14px 11px 4px);left: 18%;overflow:hidden;" @click="setMenuEntry('sys')">
      <div style="position: absolute;top: 19%;right: 16%;font-family: font2;filter: drop-shadow(rgba(0, 0, 0, 0.6) 10px 9px 4px);font-size: 1.3vh;">SYSTEM</div>
      <div style="position:absolute;top:49%;left:30%;font-family:font5;text-align:right;width:54%;font-size:0.7vh;filter:drop-shadow(rgba(0, 0, 0, 0.6) 10px 9px 4px);">SET HOW THE SYSTEM BEHAVES</div><img src="/network-wired-solid.svg" style="position:absolute;bottom:16%;left:-3%;height:64%;opacity:0.05;">
    </div>
    <div class="menuEntryOn" v-if="menuEntry == 'model'" style="position:absolute;top:-6.1%;background:rgba(255, 253, 253, 0.77);width:9%;height:7.1%;filter:drop-shadow(rgba(255, 255, 255, 0.3) 14px 11px 4px);left:0%;overflow:hidden;">
      <div style="position: absolute;top: 19%;right: 16%;font-family: font2;filter: drop-shadow(rgba(0, 0, 0, 0.6) 10px 9px 4px);font-size: 1.3vh;">MODEL</div>
      <div style="position:absolute;top:49%;left:30%;font-family:font5;text-align:right;width:54%;font-size:0.7vh;filter:drop-shadow(rgba(0, 0, 0, 0.6) 10px 9px 4px);">SELECT MODELS FOR THE BEST PERFORMANCE</div><img src="/network-wired-solid.svg" style="position:absolute;bottom:16%;left:-3%;height:64%;opacity:0.05;">
    </div>
    <div class="menuEntryOn" v-if="menuEntry == 'gen'" style="position:absolute;top:-6.1%;background:rgba(255, 253, 253, 0.77);width:9%;height:7.1%;filter:drop-shadow(rgba(255, 255, 255, 0.3) 14px 11px 4px);left:9%;overflow:hidden;">
      <div style="position: absolute;top: 19%;right: 16%;font-family: font2;filter: drop-shadow(rgba(0, 0, 0, 0.6) 10px 9px 4px);font-size: 1.3vh;">GENERATION</div>
      <div style="position:absolute;top:49%;left:30%;font-family:font5;text-align:right;width:54%;font-size:0.7vh;filter:drop-shadow(rgba(0, 0, 0, 0.6) 10px 9px 4px);">SELECT MODELS FOR THE BEST PERFORMANCE</div><img src="/network-wired-solid.svg" style="position:absolute;bottom:16%;left:-3%;height:64%;opacity:0.05;">
    </div>
    <div class="menuEntryOn" v-if="menuEntry == 'sys'" style="position:absolute;top:-6.1%;background:rgba(255, 253, 253, 0.77);width:9%;height:7.1%;filter:drop-shadow(rgba(255, 255, 255, 0.3) 14px 11px 4px);left:18%;overflow:hidden;">
      <div style="position: absolute;top: 19%;right: 16%;font-family: font2;filter: drop-shadow(rgba(0, 0, 0, 0.6) 10px 9px 4px);font-size: 1.3vh;">SYSTEM</div>
      <div style="position:absolute;top:49%;left:30%;font-family:font5;text-align:right;width:54%;font-size:0.7vh;filter:drop-shadow(rgba(0, 0, 0, 0.6) 10px 9px 4px);">SELECT MODELS FOR THE BEST PERFORMANCE</div><img src="/network-wired-solid.svg" style="position:absolute;bottom:16%;left:-3%;height:64%;opacity:0.05;">
    </div>
    <div class="menuEntrySubOpt" v-if="menuEntry == 'model'" style="position:absolute;top:1%;background:rgb(255 253 253 / 44%);width:100%;height:2%;filter:drop-shadow(rgba(255, 255, 255, 0.3) 14px 11px 4px);left:0%;">
      <div v-if="aiType != 'pubmedGPT'" style="position:absolute;height:100%;width:13%;/* background:#2196f3; */color: #7c7c7c;padding-right:0.4%;text-align:right;padding-top:1%;top: -68%;font-family:font10;filter:drop-shadow(#2196f352 14px 12px 11px);font-size: 1.4vh;" @click="setAIType('pubmedGPT')">PUBMEDGPT</div>
      <div v-if="aiType == 'pubmedGPT'" style="position:absolute;height:100%;width:13%;background:#2196f3;color:white;padding-right:0.4%;text-align:right;padding-top:1%;top:-26%;font-family:font10;filter:drop-shadow(#2196f352 14px 12px 11px);font-size: 1.4vh;">PUBMEDGPT</div>
      <div v-if="aiType != 'gal'" style="position:absolute;height:100%;width:13%;/* background:#2196f3; */color: #7c7c7c;padding-right:0.4%;text-align:right;padding-top:1%;top: -68%;font-family:font10;filter:drop-shadow(#2196f352 14px 12px 11px);left:13.4%;font-size: 1.4vh;" @click="setAIType('gal')">GALACTICA</div>
      <div v-if="aiType == 'gal'" style="position:absolute;height:100%;width:13%;background:#2196f3;color:white;padding-right:0.4%;text-align:right;padding-top:1%;top:-26%;font-family:font10;filter:drop-shadow(#2196f352 14px 12px 11px);left:13.4%;font-size: 1.4vh;">GALACTICA</div>
    </div>

    <div class="menuEntrySubOpt" v-if="menuEntry == 'gen'" style="position:absolute;top:1%;background:rgb(255 253 253 / 44%);width:100%;height:2%;filter:drop-shadow(rgba(255, 255, 255, 0.3) 14px 11px 4px);left:0%;">
      <input v-model='completionLen' type="range" min="1" max="1000" class="slider" id="myRange" style="position: absolute; height: 200%; width: 13%;">
      <div style="position: absolute;height: 211%;width: 13%;color: white;/* padding-right: 0.4%; */text-align: right;/* padding-top: 1%; */top: 0%;font-family: font10;filter: drop-shadow(rgba(33, 150, 243, 0.32) 14px 12px 11px);pointer-events: none;overflow:hidden;">

        <div style="position:absolute;top: 5%;/* left:1%; *//* font-size: 4vh; *//* font-family: font5; */background: #2196f3;font-weight:900;width:5%;height: 224%;"></div>
        <img src="/brain-solid.svg" style="position:absolute;width: 17%;left: 0%;top: 7%;filter: invert(0.9);opacity:0.5;">
        <div style="position:absolute;top: -18%;left: 15%;font-size: 4vh;font-family: font5;color: #ffffff75;font-weight:900;">{{ completionLen }}</div>
        <div style="position:absolute;top: 42%;left: 6%;font-size: 1vh;font-family:font1;background:#2196f3;width: 33%;text-align:center;">LNGH</div>
      </div>
      <input v-model='temp' type="range" min="1" max="99" class="slider" id="myRange" style="position: absolute; height: 200%; width: 13%; left: 13.4%;">
      <div style="position: absolute;height: 211%;width: 13%;color: white;/* padding-right: 0.4%; */text-align: right;/* padding-top: 1%; */top: 0%;font-family: font10;filter: drop-shadow(rgba(33, 150, 243, 0.32) 14px 12px 11px);left: 13.4%;pointer-events: none;overflow:hidden;">

        <div style="position:absolute;top: 5%;/* left:1%; *//* font-size: 4vh; *//* font-family: font5; */background: #2196f3;font-weight:900;width:90%;height: 224%;"></div>
        <img src="/brain-solid.svg" style="position:absolute;width: 17%;left: 0%;top: 7%;filter: invert(0.9);opacity:0.5;">
        <div style="position:absolute;top: -18%;left: 15%;font-size: 4vh;font-family: font5;color: #ffffff75;font-weight:900;">{{ temp }}</div>
        <div style="position:absolute;top: 42%;left: 6%;font-size: 1vh;font-family:font1;background:#2196f3;width: 33%;text-align:center;">TEMP</div>
      </div>
    </div>

    <div class="menuEntrySubOpt" v-if="menuEntry == 'sys'" style="position:absolute;top:1%;background:rgb(255 253 253 / 44%);width:100%;height:2%;filter:drop-shadow(rgba(255, 255, 255, 0.3) 14px 11px 4px);left:0%;">
      <div v-if="!continuousIntegration" style="position:absolute;height:100%;width:13%;/* background:#2196f3; */color: #7c7c7c;padding-right:0.4%;text-align:right;padding-top:1%;top: -68%;font-family:font10;filter:drop-shadow(#2196f352 14px 12px 11px);font-size: 1.4vh;" @click="setCI(true)">CI</div>
      <div v-if="continuousIntegration" style="position:absolute;height:100%;width:13%;background:#2196f3;color:white;padding-right:0.4%;text-align:right;padding-top:1%;top:-26%;font-family:font10;filter:drop-shadow(#2196f352 14px 12px 11px); font-size: 1.4vh;" @click="setCI(false)">CI</div>
    </div>

  </div>
</template>

<style>
input[type='range'] {
  overflow: hidden;
  width: 80px;
  -webkit-appearance: none;
  background-color: transparent;
}



input[type='range']::-webkit-slider-thumb {
  width: 2px;
  -webkit-appearance: none;
  height: 10px;
  cursor: ew-resize;
  background: #ffffff;
  box-shadow: -20vh 0 0 20vh #2196f3;
}
</style>
