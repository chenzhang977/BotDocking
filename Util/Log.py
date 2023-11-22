import datetime 

def log(text: str):
    if not text:
        return
        
    now = datetime.datetime.now()
    text = text.replace('\n', ' ')
    print(now.strftime("%Y-%m-%d %H:%M:%S"), text)