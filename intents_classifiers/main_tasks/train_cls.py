from neuralintents import GenericAssistant

def train():
    assistant = GenericAssistant('intents.json', model_name="skynix_tasks_cls")
    assistant.train_model()
    assistant.save_model()
    
train()
