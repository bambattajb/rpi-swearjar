import sys
sys.path.append("..")
from lib import LCD_2inch
from PIL import Image,ImageDraw,ImageFont

class Screen:
	def __init__(self):
		self.disp = LCD_2inch.LCD_2inch()
		self.disp.Init()

	def clear(self):
		self.disp.clear()

	def draw(self, text):
		try:
			canvas = Image.new("RGB", (self.disp.height, self.disp.width), "WHITE")
			draw = ImageDraw.Draw(canvas)
			font = ImageFont.truetype("./Font/Font02.ttf",25)
			draw.text((5, 5), text, fill = "BLACK", font=font)
			self.disp.ShowImage(canvas)
		except IOError as e:
			print(e)
		except KeyboardInterrupt:
    			self.disp.module_exit()
    			print("quit:")
    			exit()