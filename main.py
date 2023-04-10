import os
os.environ["TF_CPP_MIN_LOG_LEVEL"] = "3"
os.environ["CUDA_VISIBLE_DEVICES"] = "-1"
#from freenlpc import FreeNlpc
from modules.nlp_tasks import NLPTasks
from modules.ForeFront import ForeFrontApi
from modules.llms import LLMS
from dotenv import load_dotenv
from modules.weather import get_weather
from modules import prompts
import pyautogui
from neuralintents import GenericAssistant
import wikipedia
import numpy as np
from sxhkd_parser import *
import textwrap
import pyperclip
from rich import print
from rich.panel import Panel
from rich.syntax import Syntax
from rich.prompt import Prompt
from pafy import backend_youtube_dl
from bs4 import BeautifulSoup
import pafy, vlc, urllib, re, requests
from time import sleep
import pickle
import json
import pywinctl
from modules.skynixwm import SkynixWm
from modules.dict_history import DictHist
#from sentence_transformers import SentenceTransformer

load_dotenv(".env")

def _channel_through_skynix(func):
        def wrapper(self, text: str):
            output = func(self, text)
            return self.llms.skynix(prompts.task_response.replace("<task>", self.tasks.last_key()).replace("<hint>", output))
        return wrapper


class SkyNix:
    def __init__(self):
        self.version = "1.0.0"
        self.name = "SKYNIX"
        
        self.config = json.load(open(f"/home/{os.getlogin()}/skynix/config.json"))
        self.skynix_window = pywinctl.getActiveWindow()
        self.wm = SkynixWm()
        #nlpcloud_tokens = self.config["nlpcloud_tokens"]
        self.core_functions = NLPTasks()
        
        #forefront_token = self.config["forefront_token"]
        #gptj_url = self.config["forefront_gptj_url"]
        #codegen_url = self.config["forefront_codegen_url"]
        #self.gptj = ForeFrontApi(forefront_token, gptj_url)
        #self.codegen = ForeFrontApi(forefront_token, codegen_url)
        self.llms = LLMS(self.config["poe_token"])
        
        
        self.tasks = DictHist({"chat": self.chat,
                      "get_weather": self.get_weather,
                      "run_app": self.app_control,
                      "chat": self.chat,
                      "tutor": self.tutor,
                      "code": self.code,
                      "music": self.music,
                      "linux_command": self.linux_command})
        
        self.tasks_cls = GenericAssistant(f'/home/{os.getlogin()}/skynix/intents_classifiers/main_tasks/intents.json', model_name="skynix_tasks_cls", intent_methods=self.tasks)
        self.tasks_cls.load_model(f"/home/{os.getlogin()}/skynix/intents_classifiers/main_tasks/skynix_tasks_cls")
        self.app_control_cls = GenericAssistant(f"/home/{os.getlogin()}/skynix/intents_classifiers/app_control/intents.json", model_name="skynix_app_control")
        self.app_control_cls.load_model(f"/home/{os.getlogin()}/skynix/intents_classifiers/app_control/skynix_app_control")
        
        self._get_sxhkd_binds()
        self._load_conversation(f"/home/{os.getlogin()}/.local/share/skynix/conversation.pkl")
        self._init_vlc()
        
    def _inference(self, text: str):
        user_input = f"{self.user_name}: {text}"
        self.conversation.append({"message": user_input, "embeddings": self.core_functions.embeddings(user_input)})
        response = self.tasks_cls.request(text)
        try:
            skynix_response = f"SKYNIX: {response.code}"
        except:
            skynix_response = f"SKYNIX: {response}"
        self.conversation.append({"message": skynix_response,
                                "embeddings": self.core_functions.embeddings(skynix_response)})
        self._save_conversation()
        return response
    
    def _talk(self, text: str):
        res = self._inference(text)
        
        if self.tasks.last_key() == "code":
            print(Syntax(res, "python", theme="one-dark", line_numbers=True))
        elif self.tasks.last_key() == "linux_command":
            print(Syntax(res, "bash", theme="one-dark"))
        else:
            print(f"[blue]{res}")
    
    ##################-SKILLS-##################
    def chat(self, text: str):
        #convo_block = self._get_memories_of(self.conversation[-1], count=20)
        #response = self.gptj.generate(prompts.chat.replace("<block>", convo_block).replace("USER", self.user_name), repetition_penalty=1.05,length=100, stop_sequences=[f"{self.user_name}","SKYNIX:"])
        response = self.llms.skynix(text)
        return self._clean_text(response)
    @_channel_through_skynix
    def tutor(self, text: str):
        convo_block = self._get_memories_of(self.conversation[-1])
        topic = self.llms.instruct_claude(prompts.wikipedia.replace("<block>", convo_block).replace("USER", self.user_name))
        topic = self._clean_text(topic)
        wiki_content = self._get_wiki(topic)
        followup_question = self.llms.instruct_claude(prompts.followup_question.replace("<block>", convo_block).replace("<topic>", topic))
        followup_question = self._clean_text(followup_question)
        answer = self._answer_question(wiki_content, followup_question)
        #response = self.llms.skynix(prompts.tutor.replace("<block>", convo_block).replace("<hint>", answer).replace("USER", self.user_name))
        return answer
    @_channel_through_skynix    
    def code(self, text: str):
        code = self.llms.instruct_claude(prompts.code.replace("<prompt>", text))
        #code = self._clean_code(code)
        pyperclip.copy(code)
        syntax = Syntax(code, "python",theme="one-dark", line_numbers=True)
        return code
    @_channel_through_skynix
    def get_weather(self, text: str):
        city = None
        entities = self.core_functions.entities_extraction(text)
        for entity in entities:
            if entity['type'] == "GPE":
                city = entity['text']
        if city == None:
            return self._self_correct(text)
        
        status, temp = get_weather(city)
        temp = round(temp)
        temperature = str(temp) + " celsius."
        info = f"{status}, {temperature}"
        while True:
            response = self.llms.instruct_claude(prompts.question_answering_hint.replace("<question>", text).replace("<hint>", info))
            if str(temp) in response:
                return self._clean_text(response)
    #@_channel_through_skynix
    def app_control(self, text: str):
        app_name = self.llms.instruct_claude(prompts.get_app.replace("<command>", text))
        app_name = self._clean_text(app_name)
        task = self.app_control_cls.request(text)
        if task == "open":
            return self._open_app(app_name)
        elif task == "close":
            return self._close_app(app_name)
        elif task == "show":
            return self._show_app(app_name)
        elif task == "hide":
            return self._hide_app(app_name)
        elif task == "focus":
            return self._focus_app(app_name)
        else:
            return self._self_correct(text)
    @_channel_through_skynix            
    def music(self, text: str):
        action = self.core_functions.classification(self.llms.instruct_claude, text, ["play", "pause", "stop"])
        action = action.strip().lower()
        if action == "play":
            #convo_block = self._get_memories_of(self.conversation[-1], count=3)
            song = self.llms.instruct_claude(prompts.song_name.replace("<text>", text))
            song = song.strip()
            yt_url = self._get_yt_url(song)
            video = pafy.new(yt_url)
            name = video.title
            duration = video.duration
            best = video.getbestaudio()
            streaming_url = best.url
            media = self.vlc.media_new(streaming_url)
            media.get_mrl()
            self.vlc_player.set_media(media)
            self._vlc_play()
            print(Panel("",width=50 ,subtitle=f"[yellow]{duration}", title=f"[magenta]--[[green]{name}[magenta]]--"))
            return f"playing {name}"
        elif action == "pause":
            self._vlc_pause()
            return "paused"
        elif action == "stop":
            self._vlc_stop()
            return "stopped"
    @_channel_through_skynix    
    def linux_command(self, text: str):
        #convo_block = self._get_memories_of(self.conversation[-1])
        command = self.llms.instruct_claude(prompts.linux_command.replace("<question>", text))
        command = self._clean_code(command)
        
        #syntax = Syntax(command, "Bash", theme="one-dark")
        return command
    
    def terminal_autopilot(self, text: str):
        print("[bold red]WARNING: Experimental feature. Use at your own risk.")
        command = self.llms.instruct_claude(prompts.linux_task.replace("<task>", text))
        command = self._clean_code(command)
        pyperclip.copy(command)
        self.terminal.show()
        self.terminal.activate()
        pyautogui.hotkey("ctrl", "shift", "v")
        sleep(1.5)
        pyautogui.press("enter")
        sleep(2)
        self.skynix_window.activate()
        return "running command"
    

    ##################-UTILS-##################
    def _get_memories_of(self, qinput: dict, count=10):
        old_memories = self._search_index(qinput, self.conversation, count)
        recent_convo = [i["message"] for i in self.conversation]
        if len(self.conversation) > 30:
            recent_convo = recent_convo[-30:]
        convo_block = "\n".join(old_memories) + "\n" + "\n".join(recent_convo)
        return convo_block.strip()
    
    
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
    
    def _similarity(self, v1, v2):
        emb1 = np.squeeze(np.asarray(v1))
        emb2 = np.squeeze(np.asarray(v2))
        return np.dot(emb1, emb2)
    
    def _search_index(self, recent, all_lines, count=10):
        if len(all_lines) <= count:
            return list()
        scores = list()
        for i in all_lines:
            if np.all(recent['embeddings'] == i['embeddings']):
                continue
            score = self._similarity(recent['embeddings'], i['embeddings'])
            scores.append({'message': i['message'], 'score': score})
        ordered = sorted(scores, key=lambda d: d['score'], reverse=True)
        try:
            ordered = ordered[0:count]
            return [i['message'] for i in ordered]
        except:
            return [i['message'] for i in ordered]
    
    def _clean_text(self, text: str):
        #try:
        #    clean_text = text.strip().splitlines()[0]
        #except:
        #    clean_text = text.strip()
        return text
    
    def _get_sxhkd_binds(self):
        self.keybinds = []
        for bind_or_err in read_sxhkdrc(f'/home/{os.getlogin()}/.config/sxhkd/sxhkdrc'):
            if isinstance(bind_or_err, SXHKDParserError):
                continue
            keybind = bind_or_err
            app = keybind.command.raw[0].strip()
            keys = keybind.hotkey.raw[0].replace("super", "win")
            keys = [i.strip() for i in keys.split("+")]
            self.keybinds.append({"app": app, "keys": keys})
    
    def _get_wiki(self, query: str):
        try:
            wiki_search = wikipedia.search(query)
            wiki = wikipedia.WikipediaPage(wiki_search[0])
            return str(wiki.summary.encode(encoding='ASCII',errors='ignore').decode()).strip()
        except:
            return "Sorry I am kinda busy right now, can you ask me later?"
    
    def _answer_question(self, article, question):
        chunks = textwrap.wrap(article, 3000)
        answers = list()
        for chunk in chunks:
            answer = self.llms.instruct_claude(prompts.answer_question.replace("<passage>", chunk).replace("<question>", question))
            answers.append(answer)
        if len(answers) == 1:
            return answers[0]
        answers = ' '.join(answers)
        final_answer = self.llms.instruct_claude(prompts.merge.replace("<answers>", answers).replace("<question>", question))
        return final_answer.strip()
    
    def _hello(self):
        start = self._inference("hey")
        print(f"[blue]{start}")
    
    def _clean_code(self, code: str):
        while code[0].isspace() or code[-1].isspace():
            if code[0].isspace():
                code = code[1:]
            elif code[-1].isspace():
                code = code[:-1]
        code = code.splitlines()[0]
        return code
    
    def _get_yt_url(self, query: str):
        query_string = urllib.parse.urlencode({"search_query": query})
        formatUrl = urllib.request.urlopen("https://www.youtube.com/results?" + query_string)

        search_results = re.findall(r"watch\?v=(\S{11})", formatUrl.read().decode())
        clip = requests.get("https://www.youtube.com/watch?v=" + "{}".format(search_results[0]))
        yt_url = "https://www.youtube.com/watch?v=" + "{}".format(search_results[0])

        return yt_url
    
    def _init_vlc(self):
        self.vlc = vlc.Instance('--no-xlib -q > /dev/null 2>&1')
        self.vlc_player = self.vlc.media_player_new()
    
    def _vlc_play(self):
        self.vlc_player.play()
    def _vlc_pause(self):
        self.vlc_player.pause()
        return "paused"
    def _vlc_stop(self):
        self.vlc_player.stop()
        return "stopped"
    
    def _self_correct(self, text: str):
        method_list = [func for func in dir(self) if callable(getattr(self, func)) and not func.startswith("_")]
        correct_task = self.core_functions.classification(self.llms.instruct_claude, text, method_list)
        return self.tasks[correct_task](text)
    
    def _save_conversation(self):
        if not os.path.exists(f'/home/{os.getlogin()}/.local/share/skynix'):
            os.mkdir(f'/home/{os.getlogin()}/.local/share/skynix')
        pickle.dump(self.conversation, open(f"/home/{os.getlogin()}/.local/share/skynix/conversation.pkl", "wb"))
    
    def _load_conversation(self, path: str):
        if os.path.isfile(path):
            self.conversation = pickle.load(open(path, "rb"))
            user_name = self.conversation[0]["message"].split(":", 1)[0]
            self.user_name = user_name
        else:
            self.conversation = []
            print("[green]Welcome to SkyNix!")
            print("[yellow]I am SkyNix, your Linux assistant.")
            self.user_name = input("please enter your name: ").upper()
            os.system("clear")
            self._hello()
    
    def _open_app(self, app_name):
        if not self.wm.open(app_name):
            return f"running {app_name}"
        else:
            return "I'm sorry, I couldn't find that app"
    def _close_app(self, app_name):
        if not self.wm.close(app_name):
            return f"closed {app_name}"
        else:
            return "I'm sorry, I couldn't find that app"
    def _show_app(self, app_name):
        if not self.wm.show(app_name):
            return f"showing {app_name}"
        else:
            return "I'm sorry, I couldn't find that app"
    def _hide_app(self, app_name):
        if not self.wm.hide(app_name):
            return f"hiding {app_name}"
        else:
            return "I'm sorry, I couldn't find that app"
    def _focus_app(self, app_name):
        if not self.wm.focus(app_name):
            return f"focused {app_name}"
        else:
            return "I'm sorry, I couldn't find that app"
    
    def _launch_alacritty_terminal(self):
        self._open_app("alacritty")
        sleep(2)
        window_title = pywinctl.getAllAppsWindowsTitles()["alacritty"][0]
        self.terminal = pywinctl.getWindowsWithTitle(window_title)[0]
        self.terminal.hide()

     
if __name__ == "__main__":
    skynix = SkyNix()
    try:
        while True:
            text = Prompt.ask("[red]>>> ")
            skynix._talk(text)
    except KeyboardInterrupt:
        print("[red]Exiting SkyNix...")
        exit()
