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

- to make it work, sign up for [poe](https://poe.com) to access the chatbots
    - follow [skynix](https://poe.com/SkyNix) chatbot
    - follow [InstructClaude](https://poe.com/InstructClaude) chatbot

    get your token by:
    - going to [poe](https://poe.com)
    - open your browser's developer tools (also known as "inspect") and look for the value of the `p-b` cookie in the follwoing minues
        - Chromium: Devtools > Application > Cookies > poe.com
        - Firefox: Devtools > Storage > Cookies
        - Safari: Devtools > Storage > Cookies
    - copy the value of the `p-b` cookie and paste it in the config file in the `poe_token` field


- you can bind ```skynix-cli run``` to a function key and it will work like a toggle.

# update skynix
- every now and then you should run ```skynix-cli pull``` to pull any new updates.

- always make sure that ```skynix-cli``` is up to date by running ```pip install --upgrade skynix-cli```

# credits
SkyNix is inspired and heavily influenced by [David Shapiro's](https://github.com/daveshap) projects.