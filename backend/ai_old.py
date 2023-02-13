from transformers import AutoTokenizer, AutoModelForCausalLM, OPTForCausalLM


import json
import threading
import websocket
import _thread
import time
import rel
from copy import deepcopy

runningAIs=0
runningAIsTokenOnly=0

text2req = {}
text2tokenreq = {}

backlog = []
backlogTokenOnly=[]

serverws = None


print('py init', flush=True)


tokenizerpubgpt = AutoTokenizer.from_pretrained("stanford-crfm/pubmedgpt", truncation_side='left', model_max_length=1024)
tokenizerpubgpt.padding_side = 'right'
tokenizerpubgpt.add_special_tokens({'pad_token': '[PAD]'})
tokenizerpubgpt.pad_token_id = 1
modelpubgpt = AutoModelForCausalLM.from_pretrained("stanford-crfm/pubmedgpt",).to('cuda:1')



tokenizerfb = AutoTokenizer.from_pretrained("facebook/galactica-6.7b", use_fast=False, truncation_side='left', model_max_length=1024)
tokenizerfb.add_special_tokens({'pad_token': '[PAD]'})
tokenizerfb.pad_token_id = 1
tokenizerfb.padding_side = 'left'
modelfb = OPTForCausalLM.from_pretrained("facebook/galactica-6.7b", device_map="auto")
#modelfb = deepspeed.init_inference(modelfb,mp_size=world_size,dtype=torch.float,replace_method='auto',replace_with_kernel_inject=True)

#modelfb = OPTForCausalLM.from_pretrained("facebook/galactica-6.7b", device_map="auto",  max_memory=max_memory_mapping)



print('py ready', flush=True)

    




#############################################################################################
def attachAIResp2MsgEntry(texts):
    org = texts[0]
    gen = texts[1]
    for i, val in enumerate(org):
        for text in text2req:
            if val in text:
                text2req[text]['response'] = gen[i]
                serverws.send(json.dumps(text2req[text], ensure_ascii=True))

def galAiGetResp( length, temp, text):
    context = text
    mNewToken  = length
    #print('tokenizing', flush=True)
    input_ids = tokenizerfb(context, return_tensors="pt", padding=True).input_ids.to(modelfb.device)
    if len(input_ids[0])>1024:
        return
    #print('done tokenizing', flush=True)
    #gen_tokens = modelfb.generate(input_ids,  do_sample=True, temperature=temp, top_k=50, top_p=0.95,  max_time=30.0, max_new_tokens=mNewToken)
    gen_tokens = modelfb.generate(input_ids,  do_sample=True, temperature=temp, top_k=50, top_p=0.95,  max_time=30.0, max_new_tokens=mNewToken)

    #print('generated text', flush=True)
    gen_text = tokenizerfb.batch_decode(gen_tokens[:, input_ids.shape[1]:])
    orgTxt = tokenizerfb.batch_decode(input_ids)
    #print('decoding', flush=True)
    #print(gen_text)
    #print(orgTxt)
    return [orgTxt, gen_text]

def pubmedGPTGetResp( length, temp, text):

    context = text
    mNewToken  = length
    #print('tokenizing', flush=True)
    input_ids = tokenizerpubgpt(context, return_tensors="pt", padding=True).input_ids.to(modelpubgpt.device)
    if len(input_ids[0])>1024:
        return
    #gen_tokens = modelpubgpt.generate(input_ids, do_sample=True,temperature=temp, max_time=30.0, max_new_tokens=mNewToken)
    gen_tokens = modelpubgpt.generate(input_ids, do_sample=True,temperature=temp, max_time=30.0, max_new_tokens=mNewToken, pad_token_id=28895)
    #print('generated text', flush=True)
    gen_text = tokenizerpubgpt.batch_decode(gen_tokens[:, input_ids.shape[1]:])
    orgTxt = tokenizerpubgpt.batch_decode(input_ids)
    #print(gen_text)
    #print(orgTxt)
    return [orgTxt, gen_text]

            

def aiThread(whichAI, aiInput, completionLength,temp):
    #print('ai thread being run!', whichAI, aiInput, completionLength,temp)
    global runningAIs
    if whichAI == 'gal':
        text = galAiGetResp(completionLength,temp,  aiInput)


    if whichAI == 'pubmedGPT':
        text = pubmedGPTGetResp(completionLength,temp,  aiInput)
    runningAIs-=1
    if not text:
    
        return

    attachAIResp2MsgEntry(text)
    
    #call aiTHreadLauncher upon finishing up
    aiTheadLauncher()
    return

def aiTheadLauncher():
    global runningAIs
    #if nothing in backlog, return

    try:
        if len(backlog) == 0:
            return
        while runningAIs < 3:
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
                    if len(item['text'])> 0:
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
    except:
        print('invalid json detail')
##############################################################################################################

##################################
def attachToken2MsgEntry(res):
    text = res[1]
    result = res[0]

    text2tokenreq[text]['response'] = result
    serverws.send(json.dumps(text2tokenreq[text], ensure_ascii=True))

def galAiGetTokenOnly(text):
 
    print('tokenizing', flush=True)
    input_ids = tokenizerfb(text, return_tensors="pt", padding=True).input_ids.to('cuda')
 
    return [len(input_ids[0]), text]

def pubmedGPTGetTokenOnly(text):

    input_ids = tokenizerpubgpt(text, return_tensors="pt", padding=True).input_ids.to('cuda')
    
    return [len(input_ids[0]), text]

def aiThreadTokenOnly(whichAI, aiInput):
    #print('ai thread being run!', whichAI, aiInput, completionLength,temp)
    global runningAIsTokenOnly
    runningAIsTokenOnly+=1
    if whichAI == 'gal':
        res = galAiGetTokenOnly( aiInput)


    if whichAI == 'pubmedGPT':
        res = pubmedGPTGetTokenOnly(aiInput)

    attachToken2MsgEntry(res)
    runningAIsTokenOnly-=1
    #call aiTHreadLauncher upon finishing up
    aiTheadLauncherTokenOnly()
    return

def aiTheadLauncherTokenOnly():
    global runningAIsTokenOnly
    global backlogTokenOnly

    try:
        if len(backlogTokenOnly) == 0:
            return

        for item in backlogTokenOnly:
            if runningAIsTokenOnly > 2:
                return
            if item['ai'] == 'gal':
                _thread.start_new_thread(aiThreadTokenOnly, ('gal', item['text']))
            if item['ai'] == 'pubmedGPT':
                _thread.start_new_thread(aiThreadTokenOnly, ('pubmedGPT', item['text']))
        backlogTokenOnly = []
    except:
        print('invalid json detail')


##################################


def on_message(ws, message):
    try:
        global backlog
        global backlogTokenOnly
        rx = json.loads(message)
        
        if rx['text']=='':
            return

        # trial token doesnt go through generation like the other actions
        if rx['action'] == 'trialToken':
            text2tokenreq[rx['text']]=rx
            for item in backlogTokenOnly:
                if item['token'] == rx['token']:
                    backlogTokenOnly.remove(item)
            backlogTokenOnly.append(rx)
            aiTheadLauncherTokenOnly()
            return
        # generation actions
        text2req[rx['text']]=rx
        for item in backlog:
            if item['token'] == rx['token']:
                backlog.remove(item)
        backlog.append(rx)
        aiTheadLauncher()
    except:
        print('invalid json')

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


    


