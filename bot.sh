DIR_PATH=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )

if [ -z $1 ]; then
    echo "Run, Restart, Kill"

elif [ $1 == "run" ]; then
    nohup python $DIR_PATH/bot.py &

elif [ $1 == "kill" ]; then
    ps -aux | grep -i "python $DIR_PATH/bot.py" | awk '{print $2}' | xargs kill -9 &>/dev/null

elif [ $1 == "restart" ]; then
    ps -aux | grep -i "python $DIR_PATH/bot.py" | awk '{print $2}' | xargs kill -9 &>/dev/null
    nohup python $DIR_PATH/bot.py &

else
    echo "Run, Restart, Kill"
fi
