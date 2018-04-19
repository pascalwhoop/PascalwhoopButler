
#!/bin/bash
python -m unittest
PID=-1
inotifywait -rm --exclude "tensorboard\/|log\/|\.idea\/|py~|__pycache__|venv\/|swp|git\/" -e close_write ./ | while read change; do
    if [$PID -gt 0]
    then
	    kill $PID
    fi
    echo "change detected"
    #python main.py &
    python main.py
    #not working with the PID remembering
    PID=$! 
done
