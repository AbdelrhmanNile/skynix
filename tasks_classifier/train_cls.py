from neuralintents import GenericAssistant

def train_tasks_cls():
    assistant = GenericAssistant('tasks_intents.json', model_name="skynix_tasks_cls")
    assistant.train_model()
    assistant.save_model()
    
train_tasks_cls()