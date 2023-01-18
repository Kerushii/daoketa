from transformers import AutoTokenizer, AutoModelForCausalLM
import json
import sys
import threading
# text = some text source with a potential unicode problem

from copy import deepcopy


print('py init', flush=True)
max_memory_mapping = {0: "24GB", 1: "24GB"}
tokenizerfb = AutoTokenizer.from_pretrained("facebook/galactica-6.7b")
modelfb = AutoModelForCausalLM.from_pretrained("facebook/galactica-6.7b", device_map="auto",  max_memory=max_memory_mapping)

tokenizerpubgpt = AutoTokenizer.from_pretrained("stanford-crfm/pubmedgpt",  device_map="auto",  max_memory=max_memory_mapping)
modelpubgpt = AutoModelForCausalLM.from_pretrained("stanford-crfm/pubmedgpt").to('cuda')
print('py ready', flush=True)



msg = {}
aiRunning = [False, False]

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
    print('tokenizing', flush=True)
    input_ids = tokenizerpubgpt(context, return_tensors="pt").input_ids.to('cuda')
    print('done tokenizing', flush=True)
    gen_tokens = modelpubgpt.generate(input_ids, do_sample=True,temperature=temp, max_time=30.0, max_new_tokens=mNewToken,)
    print('generated text', flush=True)
    gen_text = tokenizerpubgpt.batch_decode(gen_tokens)
    print('decoding', flush=True)
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

def tAI(whichAI, pubMedInput, galAIInput, completionLength, processedMsg, threadActive):
    global aiRunning


    if whichAI == 'gal':
        text = galAiGetResp(completionLength,temp,  galAIInput)


    if whichAI == 'pubmedGPT':
        text = pubmedGPTGetResp(completionLength,temp,  pubMedInput)

    attachAIResp2MsgEntry(text, processedMsg)
    aiRunning[threadActive]=False
    #print('ai running'+str(aiRunning))
    return

#aiThread = threading.Thread(target = tAI, args = ())
while True:
    rx = input()
    try:
        print('received '+rx, flush=True)
        rx = json.loads(rx)
        msgEntry = rx['userNameAction']
        if rx['text'] == '':
            continue
        msg[msgEntry]= {'aiType':rx['aiType'],'temp':rx['temp'], 'text':rx['text'], 'completionLength':rx['completionLength']}
    except:
        print('invalid json from server, skipping to the next request', flush=True)
        pass

    
    
    for threadActive in aiRunning:
        if aiRunning[threadActive]:
            continue
        processedMsg = {}
        aiRunning[threadActive] = True

        completionLength = 50
        inputPool={'gal':0,'pubmedGPT':0}
        pubMedInput = []
        galAIInput = []
        for entry in msg:
            completionLength = int(msg[entry]['completionLength'])
            temp = float(msg[entry]['temp'])
            if msg[entry]['aiType'] == 'gal':
                inputPool['gal']+=1
                galAIInput.append(msg[entry]['text'])
            if msg[entry]['aiType'] == 'pubmedGPT':
                inputPool['pubmedGPT']+=1
                pubMedInput.append(msg[entry]['text'])
        maxBacklogAI = max(inputPool, key=inputPool.get)

        if inputPool[maxBacklogAI] == 0:
            continue
        tempMsgQ = deepcopy(msg)
        for header in tempMsgQ:
            if msg[header]['aiType']==maxBacklogAI:
                del msg[header]
                processedMsg[header]=tempMsgQ[header]
        aiThread = threading.Thread(target = tAI, args = (maxBacklogAI,pubMedInput,galAIInput, completionLength, processedMsg, threadActive))
        aiThread.start()


    


