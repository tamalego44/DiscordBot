if [ -z $1 ]; then
    echo "Run, Restart, Kill"

elif [ $1 == "run" ]; then
    nohup python bot.py &

elif [ $1 == "kill" ]; then
    ps aux | grep "python bot.py" | awk '{print $2}' | xargs kill -9 &>/dev/null

elif [ $1 == "restart" ]; then
    ps aux | grep "python bot.py" | awk '{print $2}' | xargs kill -9 &>/dev/null
    nohup python bot.py &

else
    echo "Run, Restart, Kill"
fi