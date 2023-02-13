from transformers import AutoTokenizer, AutoModelForCausalLM, OPTForCausalLM, AutoModelForSeq2SeqLM

checkpoint = "bigscience/mt0-xl"

tokenizer = AutoTokenizer.from_pretrained(checkpoint)
model = AutoModelForSeq2SeqLM.from_pretrained(checkpoint, torch_dtype="auto", device_map="auto")

inputs = tokenizer.encode('"knowledge_panel": { "type": "English theoretical physicist", "title": "Stephen Hawking", "description": "Stephen William Hawking CH CBE FRS FRSA was an English theoretical physicist, cosmologist, and author who, at the time of his death, was director of research at the Centre for Theoretical Cosmology at the University of Cambridge.", "url": "https://en.m.wikipedia.org/wiki/Stephen_Hawking", "metadata": [ { "title": "Born", "value": "January 8, 1944, Oxford, United Kingdom" }, { "title": "Died", "value": "March 14, 2018, Cambridge, United Kingdom" }, { "title": "Spouse", "value": "Jane Hawking (m. 1965–1995)" }, { "title": "Children", "value": "Lucy Hawking, Robert Hawking, Timothy Hawking" }, { "title": "Grandchild", "value": "William Smith" } ], "books": [ { "title": "A Brief History of Time", "year": "1988" }, { "title": "The Theory of Everything", "year": "2002" }, { "title": "Brief Answers to the Big Questions", "year": "2018" }, // ... ], "tv_shows_and_movies": [ { "title": "The Big Bang Theory", "year": "2007 – 2019" }, { "title": "Hawking", "year": "2013" }, { "title": "Pope Francis: A Man of His Word", "year": "2018" },  ], "ratings": [], "available_on": [], "images": [ { "url": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSxAnWUfynMEzPWZ6HW_dgPBrTofkvL0HxJhA&s", "source": "https://www.youtube.com/watch?v=uAs_QMIzGMY" }, { "url": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSjge7YZaQDXprEsagPMmyKDeO75vpm4EHbsA&s", "source": "https://revistagalileu.globo.com/Ciencia/Espaco/noticia/2018/03/stephen-hawking-morre-aos-76-anos-conheca-seu-legado.html" }, { "url": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSAWF8OW59cueqlC1QECwrr5Eds5vrAPIQBsA&s", "source": "https://www.tecmundo.com.br/ciencia/235370-stephen-hawking-veja-5-livros-conhecer-obra-cientista.htm" }, // ... ], "songs": [], "demonstration": null, "lyrics": null }\n According to the above information, what are the 3 tv shows and movies about Hawking?', return_tensors="pt").to("cuda:0")
outputs = model.generate(inputs)
print(tokenizer.decode(outputs[0]))
