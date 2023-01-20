from transformers import AutoTokenizer, AutoModelForCausalLM
import json
import threading
import websocket
import _thread
import time
import rel
from copy import deepcopy

runningAIs=0
text2req = {}
backlog = []
serverws = None

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
    #print('tokenizing', flush=True)
    input_ids = tokenizerfb(context, return_tensors="pt").input_ids.to('cuda')
    #print('done tokenizing', flush=True)
    gen_tokens = modelfb.generate(input_ids,  do_sample=True, temperature=temp, top_k=50, top_p=0.95,  max_time=30.0, max_new_tokens=mNewToken)
    #print('generated text', flush=True)
    gen_text = tokenizerfb.batch_decode(gen_tokens)
    #print('decoding', flush=True)
    return gen_text

def pubmedGPTGetResp( length, temp, text):

        
    context = text
    mNewToken  = length
    #print('tokenizing', flush=True)
    input_ids = tokenizerpubgpt(context, return_tensors="pt").input_ids.to('cuda')
    #print('done tokenizing', flush=True)
    gen_tokens = modelpubgpt.generate(input_ids, do_sample=True,temperature=temp, max_time=30.0, max_new_tokens=mNewToken)
    #print('generated text', flush=True)
    gen_text = tokenizerpubgpt.batch_decode(gen_tokens)
    #print('decoding', flush=True)
    return gen_text
    
def attachAIResp2MsgEntry(texts):
    #print('served a request!', texts)
    #print(text2req)
    for item in texts:
        #if item contains the key of text2req as a substring
        for text in text2req:
            if text not in item:
                continue
            text2req[text]['response'] = item
            serverws.send(json.dumps(text2req[text], ensure_ascii=True))
            

def aiThread(whichAI, aiInput, completionLength,temp):
    #print('ai thread being run!', whichAI, aiInput, completionLength,temp)
    global runningAIs
    if whichAI == 'gal':
        text = galAiGetResp(completionLength,temp,  aiInput)


    if whichAI == 'pubmedGPT':
        text = pubmedGPTGetResp(completionLength,temp,  aiInput)

    attachAIResp2MsgEntry(text)
    runningAIs-=1
    #call aiTHreadLauncher upon finishing up
    aiTheadLauncher()
    return

def aiTheadLauncher():
    global runningAIs
    #if nothing in backlog, return
    if len(backlog) == 0:
        return
    #while running ai <2, do the following:
    while runningAIs < 2:
        #count how many reqs each ai have
        aiReqCount = {'gal':0, 'pubmedGPT':0}
        for i in range(len(backlog)):
            if backlog[i]['ai'] == 'gal':
                aiReqCount['gal']+=1
            if backlog[i]['ai'] == 'pubmedGPT':
                aiReqCount['pubmedGPT']+=1

        #for the ai type with the highest req count, launch ai thread
        if aiReqCount['gal'] > aiReqCount['pubmedGPT']:
            aiType = 'gal'
        else:
            aiType = 'pubmedGPT'
        if aiReqCount[aiType]==0:
            return

        backlog_copy = deepcopy(backlog)
        processedMsg = []
        for item in backlog_copy:
            if item['ai'] == aiType:
                processedMsg.append(item['text'])
                backlog.remove(item)

        #get the longest length in backlog_copy of this ai type
        completionLength = 0
        for item in backlog_copy:
            if item['ai'] == aiType:
                lngth = int(item['len'])
                if lngth > completionLength:
                    completionLength = lngth
        #get the highest temp in backlog_copy of this ai type
        completionTemp = 0
        for item in backlog_copy:
            if item['ai'] == aiType:
                temp = float(item['temp'])
                if temp > completionTemp:
                    completionTemp = temp
        #launch ai thread
        runningAIs+=1

        _thread.start_new_thread(aiThread, (aiType, processedMsg, completionLength, completionTemp))





def on_message(ws, message):
    global backlog
    rx = json.loads(message)
    text2req[rx['text']]=rx
    for item in backlog:
        if item['token'] == rx['token']:
            backlog.remove(item)
    backlog.append(rx)
    aiTheadLauncher()

def on_error(ws, error):
    print(error)

def on_close(ws, close_status_code, close_msg):
    print("### closed ###")

def on_open(ws):
    print("Opened connection")

if __name__ == "__main__":
    #websocket.enableTrace(True)
    serverws = websocket.WebSocketApp("ws://127.0.0.1:8084",
                              on_open=on_open,
                              on_message=on_message,
                              on_error=on_error,
                              on_close=on_close)

    serverws.run_forever(dispatcher=rel, reconnect=5)  # Set dispatcher to automatic reconnection, 5 second reconnect delay if connection closed unexpectedly
    rel.signal(2, rel.abort)  # Keyboard Interrupt
    rel.dispatch()


    


