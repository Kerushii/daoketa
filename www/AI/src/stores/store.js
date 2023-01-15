import { ref, computed } from 'vue'
import { defineStore } from 'pinia'

// establish a ws to 192.168.1.114:8080
const socket = new WebSocket("ws://192.168.1.114:8080");
const netResp = ref('');
socket.onopen = function(e) {
  alert("[open] Connection established");
};

socket.onmessage = function(event) {
 //netResp.value = event.data.replace(/\n/g, '</br>');
 netResp.value = event.data
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
  socket.send(msg);
}

function assistSend(action, aiType, completionLength, temp, text){
  sendWS(JSON.stringify({action, aiType, completionLength, temp, text})
  );
}

export const useUserStore = defineStore('user', () => {
  return { netResp, assistSend}
})
