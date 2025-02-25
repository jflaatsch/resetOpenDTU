#!/bin/bash

TIMESTAMP=$(TZ=GMT date +"start: %F; %T, %Z")
echo $TIMESTAMP

# export DISPLAY=":0"
PYTHON_FOLDER="~/resetOpenDTU"

source ${PYTHON_FOLDER}/.venv/bin/activate
python ${PYTHON_FOLDER}/main.py R,1

if [[ $? -eq 0 ]] then 
    echo "OpenDTU reset successfully..." 
    TIMESTAMP=$(TZ=GMT date +"end  : %F; %T, %Z")
    echo $TIMESTAMP 
    echo 
    exit 0 
else 
    echo "OpenDTU reset failed..."
    TIMESTAMP=$(TZ=GMT date +"end  : %F; %T, %Z")
    echo $TIMESTAMP
    exit 1
fi

