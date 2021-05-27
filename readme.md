Usage

Make sure that the backup is connected and discoverable in either network or My PC

1. 
    Change the backup path to the correct path
    
2. 
    Change the WormWatcher folder to the correct path
    
3. 
    Edit the .bat file to work properly with specific machine (problems with python, py, or whatever the default python3 installation or specific venv is)
    
    generally should be 
    "launch python" "path to backup_script.py"
    pause <---- optional if you want to see the terminal after completion of script
    
4.
    pip install: arrow, natsort
    into whatever python installation you're using
    
5.
    Create a task scheduler script to run (make sure when the WW is NOT running) to run the .bat script every day
    
6.
    run it once to make sure that it works
    
7.
    Check the next day to make sure it worked
