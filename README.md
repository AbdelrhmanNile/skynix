# skynix

skynix is a smart AI chatbot / Linux assistant.

# what can it do?
- casual conversation
- teach you about Linux or other topics
- write code for you in any language
- help you with Linux commands
- tell you the weather
- play music
- run programs

# dependencies
these are the dependencies you need to install manually if you don't have them already:
- python3
- python3-pip
- vlc
- xfce4-terminal

# installation
using pip:
```pip install skynix-cli```

# initialize
- run ```skynix-cli pull``` to download the latest version of skynix and configure the environment for skynix to run
- run ```skynix-cli config``` to open the config file and configure skynix

# usage
run ```skynix-cli run``` to start skynix
in the first run it will ask you about your name.
the chat histroy will be saved in conversation.pkl ```~/.local/share/skynix```

# important notes
- in order to make it run apps you need to have your keybinds in a ```sxhkdrc``` file in ```~/.config/sxhkd```
    sxhkdrc example: [here](https://gitlab.com/dwt1/dotfiles/blob/master/.config/sxhkd/sxhkdrc)

- when configuring skynix, provide more than one nlpcloud api tokens.
    create multiple accounts on [nlpcloud](https://nlpcloud.com/) and get the api tokens.
        after creating an account play with it a bit in the playground to not get banned.
            after a while of using these tokens, nlpcloud will rate-limit them with 1 request per hour, when it happens, create another account and get another token.

- DO NOT use a vanilla gpt-j model from [forefront](https://www.forefront.ai/), fine-tune one using the dataset provided in the repo.
    they give you a free 10$ credit every month.

- you can bind ```skynix-cli run``` to a function key and it will work like a toggle.

# update skynix
- every now and then you should run ```skynix-cli pull``` to pull any new updates.

- always make sure that ```skynix-cli``` is up to date by running ```pip install --upgrade skynix-cli```

# credits
SkyNix is inspired and heavily influenced by [David Shapiro's](https://github.com/daveshap) projects.