get_app = """Extract Application name from the following sentences.

sentence: run brave
application name: brave
###
sentence: run vlc
application name: vlc
###
sentence: run firefox
application name: firefox
###
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