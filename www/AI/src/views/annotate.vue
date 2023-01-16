<template>
    <div>
        <div style="position: absolute;width: 71%;height: 85%;overflow: auto;left: 13%;top: 9%;" @mouseup="getSelected">
            <vue-pdf-embed :source="source1" />
        </div>
        <div v-if="parseNet" :style="{ position: 'absolute',width:'16vw', top: 'calc(2vh + '+cursorY+'px)', left: cursorX+'px', background:'grey'}">{{ parseNet }}</div>

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
            source1: '/public/pdfUploads/fExam.pdf',
            cursorX: 0,
            cursorY: 0,
            aiType: 'gal',
        }
    },
    computed: {
        ...mapState(useUserStore, ['netAnnotate']),
        parseNet(){
            if(!this.netAnnotate)
                return false
            if(!this.netAnnotate.includes('TLDR:'))
                return false
            let resp = this.netAnnotate.split("TLDR:")[1]
            let actualResp = resp.split("\n")[0]
            return actualResp
        }
    },
    methods: {
        ...mapActions(useUserStore, ['assistSend', 'clearnetAnnotate']),
        getSelected(event) {
            let text = getSelectionText()
            if(text.length<=10){
            this.clearnetAnnotate()
                return}
            if(text.length>=1000)
                return
            function getSelectionText() {
                var text = "";
                if (window.getSelection) {
                    text = window.getSelection().toString();
                } else if (document.selection && document.selection.type != "Control") {
                    text = document.selection.createRange().text;
                }
                return text;
            }

            this.cursorX = event.clientX
            this.cursorY = event.clientY
            // console.log(getSelectionText(), event.clientX, event.clientY)
            this.assistSend('annotate', 'gal', 100, 0.7, text.replace(/\n/g, ' ')+"\n\nTLDR:")
        }

    },
}
</script>