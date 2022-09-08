from neuralintents import GenericAssistant


def train_main_cls():
    assistant = GenericAssistant('main_intents.json', model_name="skynix_main_cls")
    assistant.train_model()
    assistant.save_model()
    
def train_tasks_cls():
    assistant = GenericAssistant('tasks_intents.json', model_name="skynix_tasks_cls")
    assistant.train_model()
    assistant.save_model()
    
train_tasks_cls()