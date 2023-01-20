from transformers import AutoTokenizer, AutoModelForCausalLM
import json
import threading
import websocket
import _thread
import time
import rel
from copy import deepcopy

runningAIs=0
text2token = {}
backLog = []

print('py init', flush=True)
max_memory_mapping = {0: "24GB", 1: "24GB"}
tokenizerfb = AutoTokenizer.from_pretrained("facebook/galactica-6.7b")
modelfb = AutoModelForCausalLM.from_pretrained("facebook/galactica-6.7b", device_map="auto",  max_memory=max_memory_mapping)

tokenizerpubgpt = AutoTokenizer.from_pretrained("stanford-crfm/pubmedgpt",  device_map="auto",  max_memory=max_memory_mapping)
modelpubgpt = AutoModelForCausalLM.from_pretrained("stanford-crfm/pubmedgpt").to('cuda')
print('py ready', flush=True)



def galAiGetResp( length, temp, text):

        
    context = text
    mNewToken  = length
    print('tokenizing', flush=True)
    input_ids = tokenizerfb(context, return_tensors="pt").input_ids.to('cuda')
    print('done tokenizing', flush=True)
    gen_tokens = modelfb.generate(input_ids,  do_sample=True, temperature=temp, top_k=50, top_p=0.95,  max_time=30.0, max_new_tokens=mNewToken)
    print('generated text', flush=True)
    gen_text = tokenizerfb.batch_decode(gen_tokens)
    print('decoding', flush=True)
    return gen_text

def pubmedGPTGetResp( length, temp, text):

        
    context = text
    mNewToken  = length
    #print('tokenizing', flush=True)
    input_ids = tokenizerpubgpt(context, return_tensors="pt").input_ids.to('cuda')
    #print('done tokenizing', flush=True)
    gen_tokens = modelpubgpt.generate(input_ids, do_sample=True,temperature=temp, max_time=30.0, max_new_tokens=mNewToken,)
    #print('generated text', flush=True)
    gen_text = tokenizerpubgpt.batch_decode(gen_tokens)
    #print('decoding', flush=True)
    return gen_text
    
def attachAIResp2MsgEntry(texts, processedMsg):
    respDict = {}
    #print(repr(msg))
    #print(repr(texts))
    for i in range(len(texts)):
        for singleMsg in processedMsg:
            if processedMsg[singleMsg]['text'] in texts[i]:
                respDict[singleMsg] = texts[i]
            
    print(json.dumps(respDict, ensure_ascii=True), flush=True)

def aiThread(whichAI, pubMedInput, galAIInput, completionLength, processedMsg, threadActive):
    global aiRunning


    if whichAI == 'gal':
        text = galAiGetResp(completionLength,temp,  galAIInput)


    if whichAI == 'pubmedGPT':
        text = pubmedGPTGetResp(completionLength,temp,  pubMedInput)

    attachAIResp2MsgEntry(text, processedMsg)
    aiRunning[threadActive]=False
    #call aiTHreadLauncher upon finishing up
    return

def aiTheadLauncher():
    #if nothing in backlog, return
    #while running ai <2, do the following:
        #count how many reqs each ai have
        #for the ai type with the highest req count, launch ai thread
        #delete the elements in the list that have this ai type
        #go to the next loop




def on_message(ws, message):
    rx = json.loads(rx)
    text2token[rx.text]=rx
    backlog.append(rx)
    aiTheadLauncher()

def on_error(ws, error):
    print(error)

def on_close(ws, close_status_code, close_msg):
    print("### closed ###")

def on_open(ws):
    print("Opened connection")

if __name__ == "__main__":
    websocket.enableTrace(True)
    ws = websocket.WebSocketApp("ws://127.0.0.1:8083",
                              on_open=on_open,
                              on_message=on_message,
                              on_error=on_error,
                              on_close=on_close)

    ws.run_forever(dispatcher=rel, reconnect=5)  # Set dispatcher to automatic reconnection, 5 second reconnect delay if connection closed unexpectedly
    rel.signal(2, rel.abort)  # Keyboard Interrupt
    rel.dispatch()


    


