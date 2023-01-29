<template>
    <div @mousemove="onMsmv" @click='rmAnno'>
        
        <div style="position:absolute;width:163vh;height:90vh;top:5vh;right:3vw;">
            <div class="menuEntryOff" v-if="menuEntry != 'model'" style="position:absolute;top:-6.1%;background: rgb(100 100 100);width:9%;height:7.1%;filter:drop-shadow(rgba(0, 0, 0, 0.3) 14px 11px 4px);left: 0%;overflow:hidden;" @click="setMenuEntry('model')">
                <div style="position: absolute;top: 19%;right: 16%;font-family: font2;filter: drop-shadow(rgba(0, 0, 0, 0.6) 10px 9px 4px);font-size: 1.3vh;">MODEL</div>
                <div style="position:absolute;top:49%;left:30%;font-family:font5;text-align:right;width:54%;font-size:0.7vh;filter:drop-shadow(rgba(0, 0, 0, 0.6) 10px 9px 4px);">SET GENERATION CONFIGS</div><img src="/network-wired-solid.svg" style="position:absolute;bottom:16%;left:-3%;height:64%;opacity:0.05;">
            </div>
            <div class="menuEntryOff" v-if="menuEntry != 'gen'" style="position:absolute;top:-6.1%;background: rgb(100 100 100);width:9%;height:7.1%;filter:drop-shadow(rgba(0, 0, 0, 0.3) 14px 11px 4px);left: 9%;overflow:hidden;" @click="setMenuEntry('gen')">
                <div style="position: absolute;top: 19%;right: 16%;font-family: font2;filter: drop-shadow(rgba(0, 0, 0, 0.6) 10px 9px 4px);font-size: 1.3vh;">GENERATION</div>
                <div style="position:absolute;top:49%;left:30%;font-family:font5;text-align:right;width:54%;font-size:0.7vh;filter:drop-shadow(rgba(0, 0, 0, 0.6) 10px 9px 4px);">SET GENERATION CONFIGS</div><img src="/network-wired-solid.svg" style="position:absolute;bottom:16%;left:-3%;height:64%;opacity:0.05;">
            </div>
            <div class="menuEntryOff" v-if="menuEntry != 'file'" style="position:absolute;top:-6.1%;background: rgb(100 100 100);width:9%;height:7.1%;filter:drop-shadow(rgba(0, 0, 0, 0.3) 14px 11px 4px);left: 18%;overflow:hidden;" @click="setMenuEntry('file')">
                <div style="position: absolute;top: 19%;right: 16%;font-family: font2;filter: drop-shadow(rgba(0, 0, 0, 0.6) 10px 9px 4px);font-size: 1.3vh;">FILE</div>
                <div style="position:absolute;top:49%;left:30%;font-family:font5;text-align:right;width:54%;font-size:0.7vh;filter:drop-shadow(rgba(0, 0, 0, 0.6) 10px 9px 4px);">CHANGE THE FILE</div><img src="/network-wired-solid.svg" style="position:absolute;bottom:16%;left:-3%;height:64%;opacity:0.05;">
            </div>
            <div class="menuEntryOn" v-if="menuEntry == 'model'" style="position:absolute;top:-6.1%;background:rgba(255, 253, 253, 0.77);width:9%;height:7.1%;filter:drop-shadow(rgba(255, 255, 255, 0.3) 14px 11px 4px);left:0%;overflow:hidden;">
                <div style="position: absolute;top: 19%;right: 16%;font-family: font2;filter: drop-shadow(rgba(0, 0, 0, 0.6) 10px 9px 4px);font-size: 1.3vh;">MODEL</div>
                <div style="position:absolute;top:49%;left:30%;font-family:font5;text-align:right;width:54%;font-size:0.7vh;filter:drop-shadow(rgba(0, 0, 0, 0.6) 10px 9px 4px);">SELECT MODELS FOR THE BEST PERFORMANCE</div><img src="/network-wired-solid.svg" style="position:absolute;bottom:16%;left:-3%;height:64%;opacity:0.05;">
            </div>
            <div class="menuEntryOn" v-if="menuEntry == 'gen'" style="position:absolute;top:-6.1%;background:rgba(255, 253, 253, 0.77);width:9%;height:7.1%;filter:drop-shadow(rgba(255, 255, 255, 0.3) 14px 11px 4px);left:9%;overflow:hidden;">
                <div style="position: absolute;top: 19%;right: 16%;font-family: font2;filter: drop-shadow(rgba(0, 0, 0, 0.6) 10px 9px 4px);font-size: 1.3vh;">GENERATION</div>
                <div style="position:absolute;top:49%;left:30%;font-family:font5;text-align:right;width:54%;font-size:0.7vh;filter:drop-shadow(rgba(0, 0, 0, 0.6) 10px 9px 4px);">SELECT MODELS FOR THE BEST PERFORMANCE</div><img src="/network-wired-solid.svg" style="position:absolute;bottom:16%;left:-3%;height:64%;opacity:0.05;">
            </div>
            <div class="menuEntryOn" v-if="menuEntry == 'file'" style="position:absolute;top:-6.1%;background:rgba(255, 253, 253, 0.77);width:9%;height:7.1%;filter:drop-shadow(rgba(255, 255, 255, 0.3) 14px 11px 4px);left:18%;overflow:hidden;">


                <div style="position: absolute;top: 19%;right: 16%;font-family: font2;filter: drop-shadow(rgba(0, 0, 0, 0.6) 10px 9px 4px);font-size: 1.3vh;">FILE</div>
                <div style="position:absolute;top:49%;left:30%;font-family:font5;text-align:right;width:54%;font-size:0.7vh;filter:drop-shadow(rgba(0, 0, 0, 0.6) 10px 9px 4px);">CHANGE THE FILE</div><img src="/network-wired-solid.svg" style="position:absolute;bottom:16%;left:-3%;height:64%;opacity:0.05;">
            </div>
            <div class="menuEntrySubOpt" v-if="menuEntry == 'model'" style="position:absolute;top:1%;background:rgb(255 253 253 / 44%);width:100%;height:2%;filter:drop-shadow(rgba(255, 255, 255, 0.3) 14px 11px 4px);left:0%;">

                <div v-if="aiType != 'gal'" style="position:absolute;height:100%;width:13%;/* background:#2196f3; */color: #7c7c7c;padding-right:0.4%;text-align:right;padding-top:1%;top: -68%;font-family:font10;filter:drop-shadow(#2196f352 14px 12px 11px);left:13.4%;font-size: 1.4vh;" @click="setAIType('gal')">GALACTICA</div>
                <div v-if="aiType == 'gal'" style="position:absolute;height:100%;width:13%;background:#2196f3;color:white;padding-right:0.4%;text-align:right;padding-top:1%;top:-26%;font-family:font10;filter:drop-shadow(#2196f352 14px 12px 11px);left:13.4%;font-size: 1.4vh;">GALACTICA</div>
            </div>

            <div class="menuEntrySubOpt" v-if="menuEntry == 'gen'" style="position:absolute;top:1%;background:rgb(255 253 253 / 44%);width:100%;height:2%;filter:drop-shadow(rgba(255, 255, 255, 0.3) 14px 11px 4px);left:0%;">
                <input v-model='completionLen' type="range" min="1" max="1000" class="slider" id="myRange" style="position: absolute; height: 200%; width: 13%;">
                <div style="position: absolute;height: 211%;width: 13%;color: white;/* padding-right: 0.4%; */text-align: right;/* padding-top: 1%; */top: 0%;font-family: font10;filter: drop-shadow(rgba(33, 150, 243, 0.32) 14px 12px 11px);pointer-events: none;overflow:hidden;">

                    <div style="position:absolute;top: 5%;/* left:1%; *//* font-size: 4vh; *//* font-family: font5; */background: #2196f3;font-weight:900;width:10%;height: 224%;"></div>
                    <img src="/brain-solid.svg" style="position:absolute;width: 17%;left: 0%;top: 7%;filter: invert(0.9);opacity:0.5;">
                    <div style="position:absolute;top: -18%;left: 15%;font-size: 4vh;font-family: font5;color: #ffffff75;font-weight:900;">{{ completionLen }}</div>
                    <div style="position:absolute;top: 42%;left: 6%;font-size: 1vh;font-family:font1;background:#2196f3;width: 33%;text-align:center;">LNGH</div>
                </div>
                <input v-model='temp' type="range" min="1" max="99" class="slider" id="myRange" style="position: absolute; height: 200%; width: 13%; left: 13.4%;">
                <div style="position: absolute;height: 211%;width: 13%;color: white;/* padding-right: 0.4%; */text-align: right;/* padding-top: 1%; */top: 0%;font-family: font10;filter: drop-shadow(rgba(33, 150, 243, 0.32) 14px 12px 11px);left: 13.4%;pointer-events: none;overflow:hidden;">

                    <div style="position:absolute;top: 5%;/* left:1%; *//* font-size: 4vh; *//* font-family: font5; */background: #2196f3;font-weight:900;width:70%;height: 224%;"></div>
                    <img src="/brain-solid.svg" style="position:absolute;width: 17%;left: 0%;top: 7%;filter: invert(0.9);opacity:0.5;">
                    <div style="position:absolute;top: -18%;left: 15%;font-size: 4vh;font-family: font5;color: #ffffff75;font-weight:900;">{{ temp }}</div>
                    <div style="position:absolute;top: 42%;left: 6%;font-size: 1vh;font-family:font1;background:#2196f3;width: 33%;text-align:center;">TEMP</div>
                </div>
            </div>

            <div class="menuEntrySubOpt" v-if="menuEntry == 'file'" style="position:absolute;top:1%;background:rgb(255 253 253 / 44%);width:100%;height:2%;filter:drop-shadow(rgba(255, 255, 255, 0.3) 14px 11px 4px);left:0%;">

                <input type="file" id="files" name="filetoupload" style="display:none" @change="sendFile">
                <label for="files" style="position:absolute;height:100%;width:13%;background:#2196f3;color:white;padding-right:0.4%;text-align:right;padding-top:1%;top:-26%;font-family:font10;filter:drop-shadow(#2196f352 14px 12px 11px);font-size: 1.4vh; ">SELECT NEW FILE</label>


            </div>
        </div>
        <div v-if='source1' style="position: absolute;width: 71%;height: 85%;overflow: auto;left: 13%;top: 9%;" @mouseup="getSelected" >
            <vue-pdf-embed :source="source1" />
        </div>
        <input type="file" id="filess" name="filetoupload" style="display:none" @change="sendFile">

        <label v-if='!source1' for="filess" style="position:absolute;width:71%;height:85%;mix-blend-mode:screen;top:12%;left:15%;">
            <div style="position:absolute;font-size: 25vh;font-family:font1;left: calc((100vw - 149vh) / 2);color:white;opacity:50%;top: 21%;width:100vh;">
                选择文件
            </div>
            <div style="position:absolute;font-size: 6vh;font-family: font5;left: calc((101vw - 149vh) / 2);color:white;opacity:50%;top: 59%;width:100vh;">SELECT FILES
            </div><svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 384 512" style="position:absolute;top: 3%;left: 14%;height: 60vh;opacity: 0.2;filter:invert(100);"><!--! Font Awesome Pro 6.2.1 by @fontawesome - https://fontawesome.com License - https://fontawesome.com/license (Commercial License) Copyright 2022 Fonticons, Inc. -->
                <path d="M0 64C0 28.7 28.7 0 64 0H224V128c0 17.7 14.3 32 32 32H384V448c0 35.3-28.7 64-64 64H64c-35.3 0-64-28.7-64-64V64zm384 64H256V0L384 128z"></path>
            </svg>
            <div style="position:absolute;font-size: 6vh;font-family: font5;left: calc((100vw - 149vh) / 2);background:black;opacity:50%;top: 59%;width:100vh;">SELECT FILES
            </div>
        </label>
        <div v-if="numToken" :style="{ position: 'absolute', width: '10vh', top: 'calc(2vh + ' + cursorY + 'px)', left: cursorX + 'px', background: '#2196f3', 'padding-top': '1vh', color:'white', filter: 'drop-shadow(rgba(33, 150, 243, 0.3) 14px 11px 4px)', 'font-family': ' font9','text-align':'right', 'font-size':'1.3vh' }">{{ numToken }}/1024</div>
        <div v-if="parseNet" :style="{ position: 'absolute', width: '16vw', top: 'calc(2vh + ' + cursorY + 'px)', left: cursorX + 'px', background: '#484848f2', padding: '1vh', color:'white', filter: 'drop-shadow(rgba(0, 0, 0, 0.3) 14px 11px 4px)', 'font-family': ' font1','font-size':'1.6vh' }">{{ parseNet }}</div>

    </div>
</template>

<script>
import VuePdfEmbed from 'vue-pdf-embed'
import { mapActions, mapState } from 'pinia'
import { useUserStore } from '../stores/store'
// OR THE FOLLOWING IMPORT FOR VUE 2
// import VuePdfEmbed from 'vue-pdf-embed/dist/vue2-pdf-embed'

export default {
    components: {
        VuePdfEmbed,
    },
    data() {
        return {
            cursorX: 0,
            cursorY: 0,
            selectedText:'',
            aiType: 'gal',
            menuEntry: 'model',
            temp: 0.7,
            completionLen: 100,
        }
    },
    computed: {
        ...mapState(useUserStore, ['netAnnotate', 'annoPdf', 'numToken']),
        parseNet() {
            if (!this.netAnnotate)
                return false
            
            const resp = this.netAnnotate.split("\n")[0]
            return resp
            

        },
        source1() {
            if (!this.annoPdf)
                return
            return '/pdfUploads/' + this.annoPdf

        }
    },
    methods: {
        ...mapActions(useUserStore, ['annotateSend', 'clearnetAnnotate','esToken','clearTokenTrial']),
        sendFile(e) {
            let photo = e.target.files[0];
            let formData = new FormData();
            console.log('posting')
            formData.append("photo", photo);
            fetch('http://mail.eterea.uk:8081/fileupload', { method: "POST", body: formData, mode: 'no-cors', });
        },
        rmAnno(){
            this.rmServAnno
        }, 
        setAIType(aiType) {
            this.aiType = aiType

        },
        setMenuEntry(m) {
            this.menuEntry = m
        },
        rmAnno(){
            this.clearnetAnnotate()
        },
        clearTokenT(){
            this.clearTokenTrial()
        },
        getSelected(event) {
            this.clearTokenT()
            let text = getSelectionText()

            if (!text) {
                this.clearnetAnnotate()
                return
            }
            if (text.length <= 10) {
                this.clearnetAnnotate()
                return
            }
            if (text.length >= 4096)
                return
            /*if(this.selectedText == text)
                return*/
            this.selectedText = text
            function getSelectionText() {
                var text = "";
                if (window.getSelection) {
                    text = window.getSelection().toString();
                } else if (document.selection && document.selection.type != "Control") {
                    text = document.selection.createRange().text;
                }
                
                return text;
            }

            // this.cursorX = event.clientX
            // this.cursorY = event.clientY

            this.annotateSend(this.completionLen, this.temp, text.replace(/\n/g, ' ') + "\n\nTLDR:")
            return


        },
        onMsmv(ev){
            // console.log('ms movin', ev)
            function getSelectionText() {
                var text = "";
                if (window.getSelection) {
                    text = window.getSelection().toString();
                } else if (document.selection && document.selection.type != "Control") {
                    text = document.selection.createRange().text;
                }
                // this.selectedText = text
                return text;
            }
            const text = getSelectionText()
            if(this.selectedText == text)
                return
            this.selectedText = text
            if(getSelectionText()=='')
                return
            this.cursorX = ev.clientX
            this.cursorY = ev.clientY
            const te = getSelectionText()
            // console.log(te)
            this.esToken(te)
        },

    },
}
</script>