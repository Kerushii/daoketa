from transformers import AutoTokenizer, AutoModelForCausalLM, OPTForCausalLM, AutoModelForSeq2SeqLM

import queue
from copy import deepcopy

q = queue.Queue()

import json
import websocket
import _thread
import rel

reqPoolToken = {}
tokenLock = _thread.allocate_lock()
reqPoolGen = {}
genLock = _thread.allocate_lock()



#modelpubgpt = AutoModelForCausalLM.from_pretrained("stanford-crfm/pubmedgpt",  device_map="auto", max_memory={0: "0GB", 1: "24GB", 2:"0GB"}, ).to('cuda:1')
#modelpubgpt1 = AutoModelForCausalLM.from_pretrained("stanford-crfm/pubmedgpt",  device_map="auto", max_memory={0: "0GB", 1: "0GB", 2:"24GB"}, ).to('cuda:2')
modelpubgpt = AutoModelForCausalLM.from_pretrained("stanford-crfm/pubmedgpt",  device_map="auto", )
#modelpubgpt1 = AutoModelForCausalLM.from_pretrained("stanford-crfm/pubmedgpt",  device_map="auto", )
#instr = AutoModelForSeq2SeqLM.from_pretrained('bigscience/mt0-xl', torch_dtype="auto", device_map="auto", max_memory={0: "24GB", 1: "24GB", 2:"0GB"}, )
instr = AutoModelForSeq2SeqLM.from_pretrained('bigscience/mt0-xl', torch_dtype="auto", device_map="auto")

modelfb = AutoModelForCausalLM.from_pretrained("facebook/galactica-6.7b", device_map="auto")

print('py ready', flush=True)


def ai(model, id):
    tokenizerpubgpt = AutoTokenizer.from_pretrained("stanford-crfm/pubmedgpt", truncation_side='left', model_max_length=1024)
    tokenizerpubgpt.padding_side = 'left'
    tokenizerpubgpt.add_special_tokens({'pad_token': '[PAD]'})
    tokenizerpubgpt.pad_token_id = 1
    tokenizerfb = AutoTokenizer.from_pretrained("facebook/galactica-6.7b", use_fast=False, truncation_side='left', model_max_length=1024)
    tokenizerfb.add_special_tokens({'pad_token': '[PAD]'})
    tokenizerfb.pad_token_id = 1
    tokenizerfb.padding_side = 'left'

    tokenizerInstr = AutoTokenizer.from_pretrained('bigscience/mt0-xl')


    if model == 'gal' and id == 1:
        useModel = modelfb
        useTokenizer = tokenizerfb
  #      device = 'cuda:0'


    if model == 'gal' and id == 2:
        useModel = modelfb
        useTokenizer = tokenizerfb
 #       device = 'cuda:0'

    if model == 'instr' and id == 1:
        useModel = instr
        useTokenizer = tokenizerInstr
#        device = 'cuda:0'


    if model == 'instr' and id == 2:
        useModel = instr
        useTokenizer = tokenizerInstr
#        device = 'cuda:0'




    if model == 'pubmedGPT' and id == 1:
        useModel = modelpubgpt
        useTokenizer = tokenizerpubgpt
#        device = 'cuda:1'

    if model == 'pubmedGPT' and id == 2:
        useModel = modelpubgpt
        useTokenizer = tokenizerpubgpt
#        device = 'cuda:1'

 #   if model == 'pubmedGPT' and id == 3:
#        useModel = modelpubgpt1
 #       useTokenizer = tokenizerpubgpt
#        device = 'cuda:2'

#    if model == 'pubmedGPT' and id == 4:
 #       useModel = modelpubgpt1
 #       useTokenizer = tokenizerpubgpt
#        device = 'cuda:2'

    while True:
        genLock.acquire()
        requestPile = q.get()
        
        # if the request is for tokenization, put it back in the queue
        if requestPile[0] != 'gen':
            q.put(requestPile)
            genLock.release()
            continue
        else:
            regP = deepcopy(requestPile[1])
        # go through the request pile and get how many AIs are of model
        aiCount = 0
        
        for request in regP:
            if regP[request]['ai'] == model:
                aiCount += 1
                del reqPoolGen[request]
        genLock.release()
        # put the request back if there are requests for other AIs
        newReq = {}
        for request in regP:
            if regP[request]['ai'] != model:
                newReq[request] = regP[request]
        
        if len(newReq) > 0:
            q.put(['gen',newReq])
        if aiCount == 0:
            continue
        #print(regP)
        context = []
        tokens = []
        temperature = 0
        length = 0
        for request in regP:
            if regP[request]['ai'] != model:
                print('continueing')
                continue
            if len(regP[request]['text']) == 0:
                continue
            if len(regP[request]['text']) > 9999:
                regP[request]['text'] = regP[request]['text'][-9999:]
            # add the context to the list
            context.append(regP[request]['text'])
            # and calculate the average temperature
            if 'temp' in regP[request]:
                temperature += float(regP[request]['temp'])

            # calculate the average length
            if 'len' in regP[request]:
                length += int(regP[request]['len'])

        if len(context) == 0:
            continue

        temperature = temperature / aiCount
        length = length / aiCount
        #serverws.send(json.dumps(request, ensure_ascii=True))

        if model == 'gal':
            print(context)
            input_ids = useTokenizer(context, max_length=1024,truncation=True,return_tensors="pt", padding=True).input_ids.to(useModel.device)
#            for indiReq in input_ids:
#                if len(input_ids[indiReq])>1024:
#                    input_ids[indiReq]=input_ids[indiReq][-1024:]
            gen_tokens = useModel.generate(input_ids,  do_sample=True, temperature=temperature, top_k=50, top_p=0.95,  max_time=30.0, max_new_tokens=length)
            gen_text = useTokenizer.batch_decode(gen_tokens)

        if model == 'pubmedGPT':
            input_ids = useTokenizer(context,max_length=1024,truncation=True, return_tensors="pt", padding=True, ).input_ids.to(useModel.device)
#            for indiReq in input_ids:
#                if len(input_ids[indiReq])>1024:
#                    input_ids[indiReq]=input_ids[indiReq][-1024:]
            gen_tokens = useModel.generate(input_ids,  do_sample=True, temperature=temperature,max_time=30.0, max_new_tokens=length, pad_token_id=useTokenizer.eos_token_id)
            gen_text = useTokenizer.batch_decode(gen_tokens)
        

        if model == 'instr':
            input_ids = useTokenizer(context,max_length=1024,truncation=True, return_tensors="pt", padding=True).input_ids.to(useModel.device)
#            for indiReq in input_ids:
#                if len(input_ids[indiReq])>1024:
#                    input_ids[indiReq]=input_ids[indiReq][-1024:]
            gen_tokens = useModel.generate(input_ids,  do_sample=True, temperature=temperature,max_time=30.0, max_new_tokens=length)
            gen_text = useTokenizer.batch_decode(gen_tokens)

        for index in range(len(gen_text)):
            for req in regP:
                if context[index] in regP[req]['text']:
                    originalSubText = context[index]
                    generatedText = gen_text[index]
                    res = generatedText.replace(originalSubText, '')
                    res = res.replace('[PAD]', '')
                    regP[req]['response'] = res
                    serverws.send(json.dumps(regP[request], ensure_ascii=True))

        

def tokenizer():
    tokenizerpubgpt = AutoTokenizer.from_pretrained("stanford-crfm/pubmedgpt", truncation_side='left', model_max_length=1024)
    tokenizerpubgpt.padding_side = 'left'
    tokenizerpubgpt.add_special_tokens({'pad_token': '[PAD]'})
    tokenizerpubgpt.pad_token_id = 1
    tokenizerfb = AutoTokenizer.from_pretrained("facebook/galactica-6.7b", use_fast=False, truncation_side='left', model_max_length=1024)
    tokenizerfb.add_special_tokens({'pad_token': '[PAD]'})
    tokenizerfb.pad_token_id = 1
    tokenizerfb.padding_side = 'left'
    while True:
        tokenLock.acquire()
        requestPile = q.get()
        if requestPile[0] != 'token':
            q.put(requestPile)
            tokenLock.release()
            continue
        else:
            regP = deepcopy( requestPile[1])
        print('tokenizer:')
        print(regP)
        for request in regP:
            # remove this request from the request pool 
            
            # limit the context to 1024 tokens

            del reqPoolToken[request]
        tokenLock.release()
        for request in regP:
            print(regP)
            if len(regP[request]['text']) > 9999:
                regP[request]['text'] = regP[request]['text'][-9999:]
            if len(regP[request]['text']) == 0:
                continue
            context = regP[request]['text']
            aiType = regP[request]['ai']
            if aiType == 'gal':
                regP[request]['response'] = len(tokenizerfb(context, max_length=1024,truncation=True,return_tensors="pt", padding=True).input_ids[0])
            if aiType == 'pubmedGPT':
                regP[request]['response'] = len(tokenizerpubgpt(context, return_tensors="pt",max_length=1024,truncation=True, padding=True).input_ids[0])
            print(tokenizerfb(context, return_tensors="pt", padding=True).input_ids)
            serverws.send(json.dumps(regP[request], ensure_ascii=True))






def on_message(ws, message):

        
    rx = json.loads(message)
    clientToken = rx['token']
    #on message clear all messages in the queue
    while not q.empty():
        q.get()
    #print('recived msg')
    #print(rx)
    if rx['action'] == 'trialToken':
        #go through the req and remove all requests with the same token
        regP = deepcopy(reqPoolToken)
        for key in regP:
            if reqPoolToken[key] == clientToken:
                del reqPoolToken[key]
        # add the new request to the pool
        reqPoolToken[rx['token']] = rx
        # add the requestpool to the queue
        q.put(['token',reqPoolToken])

    if rx['action'] == 'useAI4Assist' or rx['action'] == 'useAI4Annotate':
        #go through the req and remove all requests with the same token
        regG = deepcopy(reqPoolGen)
        for key in regG:
            if reqPoolGen[key] == clientToken:
                del reqPoolGen[key]
        # add the new request to the pool
        reqPoolGen[rx['token']] = rx
        # add the requestpool to the queue
        q.put(['gen',reqPoolGen])

def on_error(ws, error):
    print(error)

def on_close(ws, close_status_code, close_msg):
    print("### closed ###")

def on_open(ws):
    print("Opened connection")




if __name__ == "__main__":
    _thread.start_new_thread(ai, ('gal', 1))
    _thread.start_new_thread(ai, ('gal', 2))

    _thread.start_new_thread(ai, ('instr', 1))
    _thread.start_new_thread(ai, ('instr', 2))
    _thread.start_new_thread(ai, ('pubmedGPT', 1))
    _thread.start_new_thread(ai, ('pubmedGPT', 2))
#    _thread.start_new_thread(ai, ('pubmedGPT', 3))
 #   _thread.start_new_thread(ai, ('pubmedGPT', 4))

    # start 32 threads for tokenizers

    for i in range(32):
        _thread.start_new_thread(tokenizer,())

    serverws = websocket.WebSocketApp("ws://127.0.0.1:8084",
                              on_open=on_open,
                              on_message=on_message,
                              on_error=on_error,
                              on_close=on_close)

    serverws.run_forever(dispatcher=rel, reconnect=5)  # Set dispatcher to automatic reconnection, 5 second reconnect delay if connection closed unexpectedly
    rel.signal(2, rel.abort)  # Keyboard Interrupt
    rel.dispatch()


