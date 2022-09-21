from neuralintents import GenericAssistant

def train():
    assistant = GenericAssistant('intents.json', model_name="skynix_app_control")
    assistant.train_model()
    assistant.save_model()
    
train()
