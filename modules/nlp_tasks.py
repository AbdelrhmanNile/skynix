import spacy
pclassification = """classify the following SENTENCE into one of the following CATEGORIES.
SENTENCE:
<sentence>

CATEGORIES:
<categories>

CATEGORY:
"""
class NLPTasks:
    def __init__(self):
        try:
            self.en_core_web_lg = spacy.load("en_core_web_lg")
        except OSError:
            spacy.cli.download("en_core_web_lg")
            self.en_core_web_lg = spacy.load("en_core_web_lg")
            
    
    def entities_extraction(self, text):
        tokens = self.en_core_web_lg(text)
        entities = [(ent.text, ent.label_) for ent in tokens.ents]
        res = []
        for entity in entities:
            res.append({"text": entity[0], "type": entity[1]})
        return res
    
    def embeddings(self, text):
        tokens = self.en_core_web_lg(text)
        return tokens.vector
    
    def classification(self, model, text, classes):
        
        return model(pclassification.replace("<sentence>", text).replace("<categories>", str(classes)))
        
        

#test = NLPTasks()
#print(test.embeddings('hey'))