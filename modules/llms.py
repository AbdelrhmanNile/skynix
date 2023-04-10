import poe

class LLMS:
    
    def __init__(self, poe_token):
        self.poe_client = poe.Client(poe_token)
        
    def chatgpt(self, text, clear_history = True):
        for chunk in self.poe_client.send_message("chinchilla", text, with_chat_break = clear_history):
            pass
        return chunk["text"]
    
    def claude(self, text, clear_history = True):
        for chunk in self.poe_client.send_message("a2", text, with_chat_break = clear_history):
            pass
        return chunk["text"]
    
    def instruct_claude(self, text, clear_history = True):
        for chunk in self.poe_client.send_message("instructclaude", text, with_chat_break = clear_history):
            pass
        return chunk["text"]
    
    def skynix(self, text, clear_history = False):
        for chunk in self.poe_client.send_message("skynix", text, with_chat_break = clear_history):
            pass
        return chunk["text"]
    
    