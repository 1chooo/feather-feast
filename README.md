# Leftovers Bot

[![project badge](https://img.shields.io/badge/1chooo-line__leftovers__bot-informational)](https://github.com/1chooo/line-leftovers-bot)
[![Made with Python](https://img.shields.io/badge/Python=3.9-blue?logo=python&logoColor=white)](https://python.org "Go to Python homepage")
[![License](https://img.shields.io/badge/License-MIT-blue)](./LICENSE "Go to license section")

## A brief summary of the project

The primary objective of this project is to develop a Line Bot with an ordering system to address the issue of food waste. 
Our approach involves integrating the concept of "SDGs" (Sustainable Development Goals) and promoting the idea of "preserving the environment for the long term."

### Enviroment: 

#### With pip vertial environment
python request: `3.9.6`

```
pip3 install virtualenv
virtualenv venv --python=python3.9.6
source venv/bin/activate
pip install -r requirements.txt
deactivate
rm -rf venv     # remove the venv
```

#### With ngrok free server
```SHELL
brew install ngrok --cask
ngrok config add-authtoken TOKEN
python run.py
ngrok http 5002
```


### [Reference](./assets/reference.md)

### License
Released under [MIT](./LICENSE) by @1chooo.

This software can be modified and reused without restriction.
The original license must be included with any copies of this software.
If a significant portion of the source code is used, please provide a link back to this repository.