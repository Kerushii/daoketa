import { ref, computed } from 'vue'
import { defineStore } from 'pinia'

// establish a ws to 192.168.1.114:8080
const socket = new WebSocket("ws://mail.eterea.uk:8083");
const netRespAssist = ref('');
const netAnnotate = ref('');
const loggedIn = ref(false)
const annoPdf = ref('')
const token = ref('')
const numToken = ref(0)
socket.onopen = function(e) {
  alert("[open] Connection established");
};

socket.onmessage = function(event) {
 //netResp.value = event.data.replace(/\n/g, '</br>');
 // netResp.value = event.data
 let data = JSON.parse(event.data)
 let action = data["action"]
 console.log(data)
 switch(action)
{
  case 'token':
    token.value = data.parameters.token

    break
  case 'remotePDF4Annotate':
    annoPdf.value = data.parameters.fName
    break
  case 'useAI4Annotate':
    netAnnotate.value = data.parameters.text
    break
  case 'useAI4Assist':
    netRespAssist.value = data.parameters.text
    break
  case 'loggedIn':
    loggedIn.value = true
    break
  case 'trialToken':
    numToken.value = data.parameters.text
    break
}
};

socket.onclose = function(event) {
  if (event.wasClean) {
    alert(`[close] Connection closed cleanly, code=${event.code} reason=${event.reason}`);
  } else {
    // e.g. server process killed or network down
    // event.code is usually 1006 in this case
    alert('[close] Connection died');
  }
};

socket.onerror = function(error) {
  alert(`[error]`);
};

function sendWS(msg) {
  console.log('sending', JSON.stringify(msg))
  socket.send(JSON.stringify(msg));
}

function assistSend(ai, len, temp, text){
  sendWS({'action':'useAI4Assist', 'parameters':{token: token.value, ai, len, temp, text}})
}

function annotateSend(completionLen, temp, text){
  sendWS({'action':'useAI4Annotate', 'parameters':{token: token.value,"ai":"gal", len:completionLen, temp, text}})
}

function esToken(text){
  sendWS({'action':'trialToken', 'parameters':{token: token.value,"ai":"gal", text}})
}

function login(passwd, usr){
  sendWS({action:'login', parameters:{passwd,usr}})
}


function clearnetAnnotate(){
  netAnnotate.value = false
}

function clearTokenTrial(){
  numToken.value = false
}

export const useUserStore = defineStore('user', () => {
  return { netRespAssist,netAnnotate, assistSend, clearnetAnnotate, login, loggedIn,annoPdf,numToken, annotateSend, esToken,clearTokenTrial}
})
