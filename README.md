# Raspberry Pi Swear Jar

It's a really simple programme written in Python that lets you tap an NFC card onto an NFC hat (this one - https://www.waveshare.com/wiki/PN532_NFC_HAT) and logs a swear under your ID.

It also publishes the results for Today, This Month, and All Time to a display (this one - https://www.waveshare.com/wiki/2inch_LCD_Module)

And that's it!

# Setup

Assuming the hardware and interface is all set up correctly (see above links) then open up `users.json` and add the details of each user. `uid` is the NFC card / fob / device identifier. 

Once done, executing `python3 run.py` should just work.
