#!/bin/bash

ps aux | grep "python bot.py" | awk '{print $2}' | xargs kill -9 &>/dev/null

nohup python bot.py &


