get_app = """Extract Application name from the following sentences.

sentence: run brave
application name: brave

sentence: <command>
application name:"""

question_answering_hint = """You are a chatbot and you have been asked the following QUESTION, give a correct responsive ANSWER to the QUESTION based on HINT.

QUESTION:
<question>

HINT:
<hint>

ANSWER:
"""

intent = """I want to start coding tomorrow because it seems to be so fun!
Intent: start coding
###
Show me the last pictures you have please.
Intent: show pictures
###
Search all these files as fast as possible.
Intent: search files
###
<text>
Intent:"""

chat = """the following is a chat log between USER and SKYNIX. SKYNIX is a smart chatbot that knows a lot about Linux and is ready to help you with Linux related questions. SKYNIX answers questions with thorough, academic responses, and offers follow-up questions or suggestions to spur curiosity. SKYNIX maintains a cool, friendly tone.


<block>
SKYNIX:"""

wikipedia = """Read the following conversation and recommend a single relevant Wikipedia article title.

CONVERSATION:
USER: that is interesting.
SKYNIX: yes it really is.
USER: i want to learn more about Linux, can you teach me?
Single most relevant Wikipedia article title: Linux

CONVERSATION:
<block>


Single most relevant Wikipedia article title: """

followup_question = """Given the following conversation and the selected topic (<topic>) write a follow-up question to ask.


<block>


One follow-up question to ask about <topic>:"""

answer_question = """Use the following passage to give a detailed answer to the question. If the answer is not present in the passage, just write "NOT PRESENT".


QUESTION:
<question>


PASSAGE:
<passage>


DETAILED ANSWER or "NOT PRESENT":
"""

merge = """Merge the following answers into a single coherent paragraph. The question asked was: <question>


VARIOUS ANSWERS:
<answers>


MERGED PARAGRAPH:"""

tutor = """The following is a chat log between SKYNIX and USER. SKYNIX is an academic tutor who uses the HINT to provide robust answers to the USER. SKYNIX encourages curiosity and uses compassionate listening. SKYNIX answers questions with thorough, academic responses, and offers follow-up questions or suggestions to spur curiosity. SKYNIX maintains a cool, professional tone.

<block>
HINT: <hint>
SKYNIX:"""

code = """
given the follwoing PROMPT generate CODE.

PROMPT:
a python3 function named wow to print "hello world"

CODE:
def wow():
    print("hello, world")
###

PROMPT:
<prompt>

CODE:"""

indent_python = """indent the follwoing PYTHON CODE:

PYTHON CODE:
def hello():
print("hello world")

INDENTED PYTHON CODE:
def hello():
    print("hello world")
###

PYTHON CODE:
<code>

INDENTED PYTHON CODE:
"""

linux_task = """
Write a LINUX COMMAND to do the following TASK. If the command is not possible, write "not possible"

TASK:
<task>

LINUX COMMAND:
"""

linux_command = """answer the following QUESTION with the right bash LINUX COMMAND.

QUESTION:
what is the linux command for installing a package on ubuntu?

LINUX COMMAND:
sudo apt install package_name
###

QUESTION:
<question>

LINUX COMMAND:
"""

qa_linux_command_hint = """answer the following QUESTION with the right bash LINUX COMMAND based on HINT.

QUESTION:
what is the linux command for installing vlc on ubuntu?

HINT:
apt install vlc

ANSWER:
to install vlc on ubuntu use the following command: "apt install vlc"
###

QUESTION:
<question>

HINT:
<hint>

ANSWER:
"""

convo_linux_command = """
read the follwoing CONVERSATION and answer with the right bash LINUX COMMAND.

CONVERSATION:
USER: do you know how to use linux?
SKYNIX: yes i do, i can show you how to install a package with apt
USER: what will be the command for that?

LINUX COMMAND:
sudo apt install <package_name>
###

CONVERSATION:
<block>

LINUX COMMAND:
"""

song_name = """extract the SONG NAME from the following SENTENCE.

TEXT:
i want to listen to stairway to heaven.
SONG NAME:
stairway to heaven

TEXT:
<text>
SONG NAME:
"""

pclassification = """classify the following SENTENCE into one of the following CATEGORIES.
SENTENCE:
<sentence>

CATEGORIES:
<categories>

CATEGORY:
"""

task_response = """you have been assigned the following TASK, give a correct ANSWER to the TASK based on HINT.

TASK:
<task>

ANSWER HINT:
<hint>

ANSWER:
"""