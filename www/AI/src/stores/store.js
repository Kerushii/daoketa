import { ref, computed } from 'vue'
import { defineStore } from 'pinia'

// establish a ws to 192.168.1.114:8080
const socket = new WebSocket("ws://mail.eterea.uk:8083");
const netRespAssist = ref('');
const netAnnotate = ref('');
const loggedIn = ref(false)
const annoPdf = ref('')

socket.onopen = function(e) {
  alert("[open] Connection established");
};

socket.onmessage = function(event) {
 //netResp.value = event.data.replace(/\n/g, '</br>');
 // netResp.value = event.data
 let data = JSON.parse(event.data)
 let action = data["action"].replace('username', '')
 console.log(data)
 switch(action)
{
  case 'remotePDF4Annotate':
    annoPdf.value = data.parameters.fName
  case 'annotate':
    netAnnotate.value = data.parameters.data
    break
  case 'assist':
    netRespAssist.value = data.parameters.data
    break
  case 'loggedIn':
    loggedIn.value = true
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
  socket.send(JSON.stringify(msg));
}

function assistSend(action, aiType, completionLength, temp, text){
  sendWS({'action':'useAI', 'parameters':{userNameAction:'username'+action,aiType, completionLength, temp, text}})
}



function login(passwd, usr){
  sendWS({action:'login', parameters:{passwd,usr}})
}


function clearnetAnnotate(){
  netAnnotate.value = false
}

export const useUserStore = defineStore('user', () => {
  return { netRespAssist,netAnnotate, assistSend, clearnetAnnotate, login, loggedIn,annoPdf}
})
