from tkinter import *
from tkinter import messagebox as mb
import os

class XwUniversalError(Exception):
	def __init__(self,message):
		self.message = message
	def __str__(self):
		return f'OH!NO!AN ERROR!{self.message}'

def Input(title,message,passw=0,tip='*'):#pss = 0,noPass;pass = 1,pass]
	global get
	inputBox = Tk()
	inputBox.geometry('200x100')
	inputBox.title(title)
	inputBox.resizable(False,False)
	if passw == 0:#noPass
		label = Label(inputBox,text=message,font=('微软雅黑',17))
		label.place(x=0,y=0)
		def getInput():
			global get
			get = text.get()
			inputBox.after(100,inputBox.destroy())
		text = Entry(inputBox,width=28,font=('微软雅黑',12))
		text.place(x=0,y=30)
		okButton = Button(inputBox,text='确认',width=15,command=getInput)
		okButton.place(x=0,y=70)
		canButton = Button(inputBox,text='取消',width=11,command=quit)
		canButton.place(x=114,y=70)
		inputBox.mainloop()
		return get
	if passw == 1:#Pass
		label = Label(inputBox,text=message,font=('微软雅黑',17))
		label.place(x=0,y=0)
		def getInput():
			global get
			get = text.get()
			inputBox.after(100,inputBox.destroy())
		text = Entry(inputBox,width=28,font=('微软雅黑',12),show=tip)
		text.place(x=0,y=30)
		okButton = Button(inputBox,text='确认',width=15,command=getInput)
		okButton.place(x=0,y=70)
		canButton = Button(inputBox,text='取消',width=11,command=quit)
		canButton.place(x=114,y=70)
		inputBox.mainloop()
		return get
	else:
		inputBox.destroy()
		raise XwUniversalError(f'Unknown Parameter [passw]:{passw}')
q = Input(title='a',message='aaa',passw=0)
print(q)