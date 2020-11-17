'''
Author: hymmnos_snow
Last-Edited: 2020-11-16
For Yukihana Lamy
Happy Birth Day
'''


import pull_SuperChat as PSC

import tkinter as tk
import tkinter.filedialog
import tkinter.messagebox
import _thread


class GUI:
    def __init__(self):
        # main window
        main_window = tk.Tk()
        icon2 = tk.PhotoImage(file='./resouce/icon2.png')
        main_window.iconphoto(True, icon2)
        main_window.title("Super-chat Recorder")
        main_window.geometry("330x180")
        # logo frame
        logo_frame = tk.Frame(main_window)
        logo = tk.PhotoImage(file='./resouce/mogumogu.png')
        logo_label = tk.Label(logo_frame, image=logo)
        logo_label.pack(side=tk.LEFT)
        logo_frame.pack()
        # url frame
        url_frame = tk.Frame(main_window, height=5, width=35)
        url_label = tk.Label(url_frame, text="URL:")
        url_label.pack(side=tk.LEFT)
        self.url_entry = tk.Entry(url_frame, width=27)
        self.url_entry.pack(side=tk.RIGHT)
        url_frame.pack()
        # save frame
        save_frame = tk.Frame(main_window, height=5, width=35)
        save_label = tk.Label(save_frame, text="Save as.. :")
        save_label.pack(side=tk.LEFT)
        self.save_entry = tk.Entry(save_frame, width=28)
        self.save_entry.insert(0, "./save.xls")
        self.save_entry.pack(side=tk.LEFT)
        save_img = tk.PhotoImage(file='./resouce/folder.png')
        save_btn = tk.Button(save_frame, image=save_img, command=self.save_directory)
        save_btn.pack(side=tk.RIGHT)
        save_frame.pack()
        # start frame
        start_btn = tk.Button(main_window, text="Start", command=self.startRecord)
        start_btn.pack(side=tk.TOP)
        # process frame
        self.status = 0
        self.process_frame = tk.Frame(main_window)
        self.process_label2 = tk.Label(self.process_frame, text="0%")
        self.process_img1 = tk.PhotoImage(file='./resouce/1.png')
        self.process_img2 = tk.PhotoImage(file='./resouce/2.png')
        self.yorokorami = tk.PhotoImage(file='./resouce/yorokorami.png')
        self.okorami = tk.PhotoImage(file='./resouce/okorami.png')
        self.process_label1 = tk.Label(self.process_frame, image=self.process_img1)
        self.process_frame.pack(side=tk.BOTTOM)
        # loop
        main_window.mainloop()

    def save_directory(self):  # get save directory
        files = [('Excel File', '*.xls'),
                 ('All Files', '*.*')]
        file = tkinter.filedialog.asksaveasfilename(filetypes=files, defaultextension=files)
        self.save_entry.delete(0, 'end')
        self.save_entry.insert(0, file)

    def startRecord(self):  # start fetching the super chats in a new thread
        _thread.start_new_thread(PSC.start, (self.url_entry.get(), self.save_entry.get(), self))
        self.process_label1.pack(side=tk.LEFT)
        self.process_label2.pack(side=tk.RIGHT)
        self.status = 1

    def process(self, percentage): # update the process image
        if self.status == 1:
            self.process_label1.config(image=self.process_img2)
            self.status = 2
        else:
            self.process_label1.config(image=self.process_img1)
            self.status = 1
        if percentage <100:
            self.process_label2.config(text=str(percentage) + "%")
        else:
            self.process_label1.config(image=self.yorokorami)
            self.process_label2.pack_forget()

    def error(self):
        self.process_label1.config(image=self.okorami)
        tk.messagebox.showinfo('ERROR', 'Please Input a Valid URL.\nチャットのリプレイを利用可能のURLを入れてください。')


GUI()
