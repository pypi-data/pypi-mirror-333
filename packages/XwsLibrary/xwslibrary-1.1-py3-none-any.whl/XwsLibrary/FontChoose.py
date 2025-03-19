from tkinter import *
from tkinter import ttk
from tkinter import messagebox as msgbox
from tkinter import font

def FontChoose():
	def Updata_TestLabel():
		try:
			NewFont_Font = FontCombo_Font.get()
			NewFont_Size = FontCombo_Size.get()
			NewFont = font.Font(
				family=NewFont_Font,
				size=int(NewFont_Size),
				weight="bold" if BoldVar.get() else "normal"
			)
		except Exception as e:
			msgbox.showerror('错误',f'错误！{e}')
			exit()
		FontLabel_Test.config(font=NewFont)
	def ApplyNewFont():
		global OutputFont
		try:
			NewFont_Font = FontCombo_Font.get()
			NewFont_Size = FontCombo_Size.get()
			NewFont = font.Font(
				family=NewFont_Font,
				size=int(NewFont_Size),
				weight="bold" if BoldVar.get() else "normal"
			)
		except Exception as e:
			
			msgbox.showerror('错误',f'错误！{e}')
			exit()
		FontLabel_Test.config(font=NewFont)
		FontWindow.after(100,FontWindow.destroy)
		OutputFont = NewFont_Font,NewFont_Size
	FontWindow = Tk()
	FontWindow.title('选择一个字体...')
	FontWindow.geometry('300x150')

	FontWindow.resizable(False,False)
	FontLabel_Font = Label(FontWindow,text='字体:')
	FontLabel_Font.place(x=0,y=0)
	FontLabel_Size = Label(FontWindow,text='字号:')
	FontLabel_Size.place(x=0,y=22)

	FontCombo_Font = ttk.Combobox(FontWindow,width='18')
	FontCombo_Font.place(x=40,y=0)
	FontCombo_Size = ttk.Combobox(FontWindow,width='8')
	FontCombo_Size.place(x=40,y=22)
	Font_Families = sorted(font.families())
	FontCombo_Font.config(values=Font_Families)
	FontCombo_Size.config(values=[8,9,10,11,12,14,16,18,20,22,24])

	BoldVar = BooleanVar()
	FontCheck_Bold = Checkbutton(FontWindow,text='加粗？',variable=BoldVar)
	FontCheck_Bold.place(x=200,y=22)

	FontLabel_Test = Label(FontWindow,text='测试文本 ABCabc 123')
	FontLabel_Test.place(x=0,y=80)

	FontButton_Exp = ttk.Button(FontWindow,text='测试',command=Updata_TestLabel,width=10)
	FontButton_Exp.place(x=0,y=50)
	FontButton_App = ttk.Button(FontWindow,text='应用',command=ApplyNewFont,width=10)
	FontButton_App.place(x=80,y=50)

	FontWindow.mainloop()
	return OutputFont

if __name__ == '__main__':
	a = FontChoose()
	print(a)