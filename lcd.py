import lcddriver
from time import sleep
import requests as r

CHAMBERS = 8

# Request that the Brewpi socket expects
data = {"messageType": "lcd", "message": ""}

lcd = lcddriver.lcd()

while True:
    # Cycle through all of our chambers
    for i in xrange(0, CHAMBERS):
        # Start the screen out fresh
        lcd.lcd_clear()

        try:
            # Communicated with the brewpi script. I know...crazy setup
            resp = r.post("http://localhost/chamber" + str(i) + "/socketmessage.php", data=data).json()
        except:
            resp = ['Cannot receive', 'LCD text from', 'Python script', '']
        
        for index, line in enumerate(resp):
            # Things to make the text less confusing for my particular setup.
            if "Mode" in line:
                line = "Chamber " + str(i)
            if "Fridge" in line:
                line = line.replace("Fridge", "Beer")
            if "Beer   --.-  --.-" in line:
                line = ""
            # Newlines make a weird symbol on the lcd
            if line == "\n":
                line = ""
            lcd.lcd_display_string(line.replace("&deg", ""), index+1)
        sleep(2)