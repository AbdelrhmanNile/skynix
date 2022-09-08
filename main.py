import os
from freenlpc import FreeNlpc
from ForeFront import ForeFrontApi
from dotenv import load_dotenv
from microservices.weather import get_weather
import prompts
import pyautogui
from neuralintents import GenericAssistant
import wikipedia
import numpy as np

load_dotenv(".env")

class SkyNix:
    def __init__(self):
        self.version = "0.0.1"
        self.name = "SKYNIX"
        
        self.core_functions = FreeNlpc([os.getenv("nlpc1"), os.getenv("nlpc2")])
        self.gptj = ForeFrontApi(os.getenv("forefront_key"), os.getenv("skynix_gptj"))
        
        self.main_intents = {"chat": self.chat,
                            "tasks": self._get_intent}
        
        self.tasks = {"weather": self.get_weather,
                      "get_name": self.get_name,
                      "run_app": self.run_app,
                      "chat": self.chat}
        
        self.main_cls = GenericAssistant('main_intents.json', model_name="skynix_main_cls", intent_methods=self.main_intents)
        self.main_cls.load_model()
        
        self.tasks_cls = GenericAssistant('tasks_intents.json', model_name="skynix_tasks_cls", intent_methods=self.tasks)
        self.tasks_cls.load_model()
        
        self.conversation = ["The following is a conversation between USER and SKYNIX. SKYNIX is a smart chatbot."]
        
    def _inference(self, text: str):
        user_input = f"USER: {text}"
        self.conversation.append({"message": user_input,
                                  "embeddings": self.core_functions.embeddings([user_input])})
        self.conversation.append(f"{self.name}:")
        response = self.main_cls.request(text)
        skynix_response = f"SKYNIX: {response}"
        self.conversation[-1] = {"message": skynix_response,
                                 "embeddings": self.core_functions.embeddings([skynix_response])}
        return response
    
    def chat(self, text: str):
        convo_str = self._convo_to_str()
        while True:
            response = self.gptj.generate(convo_str, length=30, temperature=0.6, stop_sequences=["USER:", "SKYNIX:"])
            print(f"RAW RESPONSE: {response}")
            if response == "" or response == " ":
                continue
            else:
                break
        return self._clean_text(response)
    
    def tutor(self, text: str):
        pass
        
    def _get_intent(self, text: str):
        response = self.tasks_cls.request(text)
        return response
    
    
    def _convo_to_str(self, for_summary=False):
        convo_str = ""
        for i in self.conversation:
            try:
                convo_str = convo_str + i["message"] + "\n"
            except:
                if for_summary == True:
                    continue
                else:
                    convo_str = convo_str + i + "\n"
        return convo_str
      
    def _wake_word(self):
        pass
    
    def similarity(v1, v2):
        return np.dot(v1, v2)
    
    def _search_index(self, recent, all_lines, count=10):
        if len(all_lines) <= count:
            return list()
        scores = list()
        for i in all_lines:
            if recent['vector'] == i['vector']:
                continue
            score = similarity(recent['vector'], i['vector'])
            #print(score)
            scores.append({'line': i['line'], 'score': score})
        ordered = sorted(scores, key=lambda d: d['score'], reverse=True)
        try:
            ordered = ordered[0:count]
            return [i['line'] for i in ordered]
        except:
            return [i['line'] for i in ordered]
    
    def _clean_text(self, text: str):
        clean_text = text.strip().splitlines()[0]
        return clean_text
    
    
    def get_weather(self, text: str):
        entities = self.core_functions.entities_extraction(text)['entities']
        for entity in entities:
            if entity['type'] == "GPE":
                city = entity['text']
        temp = str(int(get_weather(city))) + " celsius."
        response = self.gptj.generate(prompts.question_answering_hint.replace("<question>", text).replace("<hint>", temp), length=20, stop_sequences=["QUESTION:","ANSWER:"])
        return self._clean_text(response)
    
    def run_app(self, text: str):
        app_name = self.gptj.generate(prompts.get_app.replace("<command>", text), length=20, stop_sequences=["\n","###"])
        pyautogui.hotkey("win", "b")
        return f"running {app_name}"
    
    def get_name(self, text: str):
        return "my name is " + self.name.lower()
        
        
skynix = SkyNix()
while True:
    text = input("USER: ")
    response = skynix._inference(text)
    print(response)
    print("####################")
    print(skynix._convo_to_str())