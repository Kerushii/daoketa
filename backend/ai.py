from transformers import AutoTokenizer, AutoModelForCausalLM
import json
import sys
import threading


print('py init', flush=True)
max_memory_mapping = {0: "24GB", 1: "24GB"}
tokenizerfb = AutoTokenizer.from_pretrained("facebook/galactica-6.7b")
modelfb = AutoModelForCausalLM.from_pretrained("facebook/galactica-6.7b", device_map="auto",  max_memory=max_memory_mapping)

tokenizerpubgpt = AutoTokenizer.from_pretrained("stanford-crfm/pubmedgpt")
modelpubgpt = AutoModelForCausalLM.from_pretrained("stanford-crfm/pubmedgpt").to('cuda')
print('py ready', flush=True)



msg = None
aiRunning = False
ai2Running = False


def galAiGetResp( length, temp, text):
    global msg
    msg = None
        
    context = text
    mNewToken  = length
    input_ids = tokenizerfb(context, return_tensors="pt").input_ids.to('cuda')
    gen_tokens = modelfb.generate(input_ids, do_sample=True, temperature=temp, max_new_tokens=mNewToken,)
    gen_text = tokenizerfb.batch_decode(gen_tokens)[0]
    return gen_text

def pubmedGPTGetResp( length, temp, text):
    global msg
    msg = None
        
    context = text
    mNewToken  = length
    input_ids = tokenizerpubgpt(context, return_tensors="pt").input_ids.to('cuda')
    gen_tokens = modelpubgpt.generate(input_ids, do_sample=True, temperature=temp, max_new_tokens=mNewToken,)
    gen_text = tokenizerpubgpt.batch_decode(gen_tokens)[0]
    return gen_text
    

def tAI():
    global aiRunning
    print('py ai thread initing')
    #while msg:
    if msg['action'] == 'assist' and msg['aiType'] == 'gal':
        if msg['text'] == '':
            return
        text = galAiGetResp(int(msg['completionLength']), float(msg['temp']),  msg['text'])
        print('fdgerguhyGTYGVTFYTYGRtfgycyrtfGYVYTGYTvGTVYGUBYU'+text, flush=True)
    print('py ai thread exitings')
    aiRunning = False
    return

#aiThread = threading.Thread(target = tAI, args = ())
while True:
    
    msg = input() #multi user scenerio: while the ai thread is working, accumulate 1 msg for each user. the msg list will be destroyed once the ai runs
    print('py '+str(msg))

    #covert msg from json to dict
    msg = json.loads(msg)
    
    if not aiRunning:
        aiRunning = True
        aiThread = threading.Thread(target = tAI, args = ())
        aiThread.start()
        continue

    if not ai2Running:
        ai2Running = True
        ai2Thread = threading.Thread(target = tAI, args = ())
        ai2Thread.start()

    


