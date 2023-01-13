from transformers import AutoTokenizer, AutoModelForCausalLM
import json


print('py init')
max_memory_mapping = {0: "24GB", 1: "24GB"}
tokenizerfb = AutoTokenizer.from_pretrained("facebook/galactica-6.7b")
modelfb = AutoModelForCausalLM.from_pretrained("facebook/galactica-6.7b", device_map="auto",  max_memory=max_memory_mapping)

tokenizerpubgpt = AutoTokenizer.from_pretrained("stanford-crfm/pubmedgpt")
modelpubgpt = AutoModelForCausalLM.from_pretrained("stanford-crfm/pubmedgpt").to('cuda')
print('py ready')

def galAiGetResp(length, temp, text):
    context = text
    
    mNewToken  = length
    input_ids = tokenizerfb(context, return_tensors="pt").input_ids.to('cuda')
    gen_tokens = modelfb.generate(input_ids, do_sample=True, temperature=temp, max_new_tokens=mNewToken,)
    gen_text = tokenizerfb.batch_decode(gen_tokens)[0]
    return gen_text

def pubmedGPTGetResp(length, temp, text):
    context = text
    
    mNewToken  = length
    input_ids = tokenizerpubgpt(context, return_tensors="pt").input_ids.to('cuda')
    gen_tokens = modelpubgpt.generate(input_ids, do_sample=True, temperature=temp, max_new_tokens=mNewToken,)
    gen_text = tokenizerpubgpt.batch_decode(gen_tokens)[0]
    return gen_text


while True:
    
    msg = input()
    
    #covert msg from json to dict
    print('py 1'+msg)
    msg = json.loads(msg)
    print('py 2'+str(msg))
    if msg['action'] == 'assist' and msg['aiType'] == 'gal':
        if msg['text'] == '':
            continue
        text = galAiGetResp(int(msg['completionLength']), float(msg['temp']),  msg['text'])
        print('fdgerguhyGTYGVTFYTYGRtfgycyrtfGYVYTGYTvGTVYGUBYU'+text)




