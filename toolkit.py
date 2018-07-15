#!/usr/bin/python
# -*- coding: utf-8 -*-
# qinhuawei@outlook.com
try:
    from Tkinter import *
    from tkFileDialog import askopenfilename,askdirectory
    from ttk import Combobox
    import ttk
except:
    from tkinter import *
    from tkinter.filedialog import askopenfilename,askdirectory
    from tkinter.ttk import Combobox,style
import logging,json,re,os,threading,Queue,sys,time
from datetime import datetime,timedelta
try:
    from playsound import playsound   # pip install playsound
except:
    playsound = None
from multiprocessing import Process

class countdown_timer():
    pid = None
    def __init__(self, duration):
        self.loop_id = -1
        self.action_list = ['U', 'D']
        self.duration = duration
        self.root = Toplevel()
        self.root.title('Timer')
        self.root.attributes('-toolwindow', 1)
        self.root.wm_attributes("-topmost", 1)
        self.root.overrideredirect(True)
        self.root.resizable(width=False, height=False)
        self.root.configure(background='#000')
        self.create_label_countdown()
        self.set_label_window()
        self.root.protocol('WM_DELETE_WINDOW', self.exit_now)
        self.restart_countdown()

    def play_sound(self):
        #os.system("start C:/Windows/Media/town.mid")
        #playsound('C:/Windows/Media/town.mid', False)
        if self.pid:
            self.pid.terminate()
        self.pid = Process(target=playsound, args=('C:/Windows/Media/town.mid',))
        self.pid.start()
        #self.pid.join()

    def set_label_window(self):
        width = 130
        height = 30
        from_top = 0
        self.root.geometry('%dx%d+%s+%s' %(width,height,self.root.winfo_screenwidth()-width-100,from_top))  # <width>x<height>
        self.label_countdown.configure(background='#000')

    def exit_now(self,):
        if self.pid:
            self.pid.terminate()
        self.root.destroy()

    def create_label_countdown(self):
        self.label_countdown = Label(self.root, text='-0_%02d:%02d' %(self.duration/60,self.duration%60),font = ('consolas bold',20),bg='#000',fg = '#fff')
        self.label_countdown.pack(fill=BOTH)
        self.label_countdown.bind('<Button-1>', lambda event:self.restart_countdown())
        self.label_countdown.bind('<Button-3>', lambda event:self.exit_now())
        self.queue_label_countdown = Queue.Queue()

    def restart_countdown(self):
        if self.pid:
            self.pid.terminate()
        self.queue_label_countdown.put(1)
        time.sleep(0.2)
        with self.queue_label_countdown.mutex:
            self.queue_label_countdown.queue.clear()
        self.loop_id = (self.loop_id + 1)%10
        self.label_countdown.config(text='%s%d_%02d:%02d' %(self.action_list[self.loop_id%2],self.loop_id,self.duration/60,self.duration%60))
        self.root.attributes('-alpha', 0.5)
        self.countdown()

    def countdown(self,):
        def count_blink():
            for iii in range(self.duration-1,-1,-1):
                try:
                    self.queue_label_countdown.get(True, timeout=1)
                    return
                except:
                    try:
                        self.label_countdown.config(text='%s%d_%02d:%02d' %(self.action_list[self.loop_id%2],self.loop_id,iii/60,iii%60))
                    except:
                        pass

            self.root.geometry('%dx50+%s+%s' %(self.root.winfo_screenwidth(),0,0))
            self.root.attributes('-alpha', 1)
            self.play_sound()
            bg_colors = ['#f00','#000']
            for iii in range(3600):
                try:
                    self.queue_label_countdown.get(True, timeout=0.5)
                    break
                except:
                    tmp=iii/2
                    self.label_countdown.configure(background=bg_colors[iii%2],
                        text='%s%d_%02d:%02d' %(self.action_list[self.loop_id%2],self.loop_id,tmp/60,tmp%60))
            self.set_label_window()

        #print '------countdown------'
        self.set_label_window()
        thr = threading.Thread(target=count_blink, args=())
        thr.setDaemon(True)
        thr.start()

class popup_option_menu(Toplevel):
    chosen_file = None
    chosen_folder = None

    def __init__(self, tip_info, callback_func):
        Toplevel.__init__(self)
        self.callback_func = callback_func
        self.title(tip_info)

        lable_width = 10
        entry_width = 50

        row_id = 0
        Label(self, text="ALIAS :", anchor=E, width=lable_width).grid(row=row_id, column=0, pady=2)
        self.var_alias = StringVar()
        Entry(self, textvariable=self.var_alias).grid(row=row_id, column=1, columnspan=2, sticky=EW)

        row_id = row_id + 1
        Label(self, text='FILE/CMD :', anchor=E, width=lable_width).grid(row=row_id, column=0, pady=2)
        self.var_main_file = StringVar()
        self.entry_file = Entry(self, textvariable=self.var_main_file, width=entry_width)
        self.button_select_file  = Button(self, text="F",  command=self.cmd_btn_select_file, wraplength=180)

        self.entry_file.grid(row=row_id, column=1,  sticky=EW)
        self.button_select_file.grid(row=row_id, column=2, sticky=EW)

        row_id = row_id + 1
        Label(self, text="DIR :", anchor=E, width=lable_width).grid(row=row_id, column=0, pady=2)
        self.var_main_folder = StringVar()
        self.entry_folder = Entry(self, textvariable=self.var_main_folder, width=entry_width)
        button_folder = Button(self, text="D",  command=self.cmd_btn_select_folder, wraplength=180)
        self.chosen_folder = ''

        self.entry_folder.grid(row=row_id, column=1,  sticky=EW)
        button_folder.grid(row=row_id, column=2,  sticky=EW)

        row_id = row_id + 1
        Label(self, text="Interpreter :", anchor=E, width=lable_width).grid(row=row_id, column=0, pady=2)
        self.var_interpreter = StringVar()
        self.entry_interpreter = Entry(self, textvariable=self.var_interpreter, width=entry_width)
        button_interpreter = Button(self, text="F",  command=self.cmd_btn_select_interpreter, wraplength=180)
        self.chosen_interpreter = ''

        self.entry_interpreter.grid(row=row_id, column=1, sticky=EW)
        button_interpreter.grid(row=row_id, column=2, sticky=EW)

        row_id = row_id + 1
        Button(self, text="OK", command=self.cmd_button_yes).grid(row=row_id, column=2, sticky=EW)
        Button(self, text="Cancel",  command=self.destroy       ).grid(row=row_id, column=3, sticky=EW)

    def cmd_btn_select_interpreter(self):
        self.attributes('-topmost', 'false')
        self.chosen_interpreter = askopenfilename()
        self.attributes('-topmost', 'true')
        if self.chosen_interpreter:
            self.entry_interpreter.insert(END, self.chosen_interpreter)

    def cmd_btn_select_file(self):
        self.attributes('-topmost', 'false')
        self.chosen_file = askopenfilename()
        self.attributes('-topmost', 'true')
        if self.chosen_file:
            self.entry_file.insert(END, self.chosen_file)
            if not self.chosen_folder:
                self.entry_folder.insert(END, os.path.dirname(self.chosen_file))

    def cmd_btn_select_folder(self):
        self.attributes('-topmost', 'false')
        self.chosen_folder = askdirectory()
        self.attributes('-topmost', 'true')
        if self.chosen_folder:
            self.entry_folder.insert(END, self.chosen_folder)

    def cmd_button_yes(self):
        if not self.var_alias.get():
            return popup_text_information('Fill ALIAS ...', self)
        if not self.chosen_file:
            self.chosen_file = self.var_main_file.get()
        if not self.chosen_file:
            return popup_text_information('Need File ...', self)

        logging.info('[%s] [%s] [%s] [%s]' %(self.var_alias.get(),self.var_main_file.get(), self.var_main_folder.get(), self.var_interpreter.get()))
        self.callback_func(self.var_alias.get(),self.var_main_file.get(), self.var_main_folder.get(), self.var_interpreter.get())
        self.destroy()

def popup_text_information(text_info, anchor):
    frame_tips = Toplevel(bg="#ffff00")
    frame_tips.geometry('+%d+%d' %(anchor.winfo_rootx()+1,anchor.winfo_rooty()+1))
    frame_tips.overrideredirect(1)
    frame_tips.title("ERROR ...")
    label_info  = Label(frame_tips, text=text_info,bg="#ffff00")
    label_info.grid (row=0, column=0)
    frame_tips.after(2000, frame_tips.destroy)

class window_main(Tk):
    json_data = {}
    dict_str_var = {}
    dict_button  = {}
    dict_cbbox  = {}
    dict_checkbox_var  = {}
    dict_btn_remove  = {}
    remove_enabled = False

    def __init__(self):
        Tk.__init__(self)
        self.load_cfg_file()
        self.title('ToolKit')
        self.wm_iconbitmap( '@icon.xbm')
        self.configure(background='#eef')
        self.resizable(width=False, height=False)
        width=10
        font=("", 10, 'bold')
        btn_bg = '#ffe'
        btn_fg = '#00f'

        frame_title = Frame(self, )
        frame_title.grid(row=0)
        self.button_add =  Button(frame_title,font=font, width=width, bg=btn_bg, fg=btn_fg, text="ADD",
            command=lambda:popup_option_menu('ADD',self.callback_add_command,).grab_set())
        self.button_remove_item = Button(frame_title, font=font, width=width, bg=btn_bg, fg=btn_fg, text="REMOVE",
            command=self.show_btn_remove)
        self.button_help = Button(frame_title,font=font, width=width, bg=btn_bg, fg=btn_fg, text="HELP",
            command=lambda :os.startfile("https://github.com/qin-neo/pyToolkit") )

        self.var_entry_timer = IntVar()
        self.var_entry_timer.set(2400)
        self.button_countdown = Button(frame_title,font=font, width=width, bg=btn_bg, fg=btn_fg, text="CountDown",
            command=self.cmd_btn_countdown)
        entry_timer = Entry(frame_title, textvariable=self.var_entry_timer, width=width)

        row_id = 0
        self.button_add.grid   (row=row_id, column=0,)
        self.button_remove_item.grid      (row=row_id, column=1)
        self.button_help.grid      (row=row_id, column=2,)
        self.button_countdown.grid      (row=row_id, column=3,)
        entry_timer.grid      (row=row_id, column=4,)

        frame_table = Frame(self, )
        #frame_scrollbar = Scrollbar(frame_table, orient=VERTICAL)
        #frame_scrollbar.pack(fill=Y, side=RIGHT, expand=FALSE)
        self.frame_list = Frame(frame_table, bg="#fa3")
        self.frame_list.pack(fill=BOTH)
        frame_table.grid(row=1)
        self.update_list_frame_view()

        self.frame_tips = Toplevel(self,bd=1,bg="black")
        self.frame_tips.withdraw()
        self.frame_tips.overrideredirect(1)
        self.frame_tips.transient()
        self.label_tips=Label(self.frame_tips,bg="yellow",justify='left')
        self.label_tips.pack()
        help_info = '''  Windows ToolKit, shortcuts with parameters.
    Author: qinhuawei@outlook.com 2018-07-04
  Left-Click on Alias button: execute shortcut
  Right-Click on Alias button: open main folder
  Right-Click in text-entry: clean text-entry
  Mid-Click in text-entry: remove chosen line from history
  REMOVE button: enable "-" button to remove shortcut
  CountDown button: start a countdown timer on right corner of screen
    Left-Click on timer: reset timer
    Right-Click on timer: exit timer'''
        self.button_help.bind("<Enter>", lambda event:self.show_tips(help_info,self.button_help))
        self.button_help.bind("<Leave>", lambda event:self.frame_tips.withdraw())

    def cmd_btn_countdown(self,):
        try:
            if Toplevel.winfo_exists(self.countdown.root):
                return
        except:
            pass
        self.countdown = countdown_timer(self.var_entry_timer.get())

    def show_tips(self, info_text, anchor):
        self.frame_tips.geometry('+%d+%d' %(anchor.winfo_rootx(),(anchor.winfo_rooty()+20)))
        self.frame_tips.deiconify()
        self.label_tips.config(text=info_text)

    def show_btn_remove(self):
        if self.remove_enabled:
            self.remove_enabled = False
            for item_alias in self.json_data.keys():
                self.dict_btn_remove[item_alias].config(state=DISABLED,text="",width=0)
        else:
            self.remove_enabled = True
            for item_alias in self.json_data.keys():
                self.dict_btn_remove[item_alias].config(state=NORMAL,text="-",width=2)

    def init_item_context(self,item_alias, main_file, main_folder, interpreter):
        if not main_folder:
            try:
                main_folder = os.path.dirname(main_file)
            except:
                pass
        if not main_folder:
            main_folder = '%userprofile%'

        self.json_data[item_alias] = {}
        self.json_data[item_alias]['main'] = re.sub(r'(\s+)', r'"\1"',main_file)
        self.json_data[item_alias]['folder'] = main_folder
        self.json_data[item_alias]['interpreter'] = interpreter
        self.json_data[item_alias]['list'] = ["",]
        logging.debug('alias [%s] main_file [%s] main_folder [%s]' %(item_alias, main_file, main_folder))

    def load_default_cfg(self):
        self.init_item_context('explorer', 'explorer', '', '')
        self.json_data['explorer']['list'] = ['https://github.com/qin-neo/pyToolkit',]

    def load_cfg_file(self):
        for iii in range(30):
            file_name = (datetime.now() - timedelta(days=iii)).strftime('cfg_%Y%m%d.json')
            if os.path.isfile(file_name):
                try:
                    data_file = open(file_name, 'rb')
                    self.json_data = json.load(data_file, encoding="utf-8")
                    data_file.close()
                    return
                except:
                    logging.exception('--------- %s ----------' %file_name)
        logging.exception('json load configuration.json failed.')
        self.load_default_cfg()

    def save_cfg_file(self):
        self.cfg_file = datetime.now().strftime('cfg_%Y%m%d.json')
        data_file = open(self.cfg_file, 'w')
        try:
            json.dump(self.json_data, data_file, sort_keys = True, indent = 4, encoding='utf8')
        except:
            json.dump(self.json_data, data_file, indent = 4)
        data_file.close()

    def callback_add_command(self, item_alias, main_file, main_folder, interpreter):
        try:
            return popup_text_information('ALIAS [%s] duplicated.\nUsed by [%s]' %(item_alias, self.json_data[item_alias]['main'])).grab_set()
        except:
            logging.info('item_alias [%s] OK' %item_alias)
        self.init_item_context(item_alias, main_file, main_folder, interpreter)
        self.update_list_frame_view()
        self.save_cfg_file()

    def cmd_button_run_script(self, item_alias):
        item_dict = self.json_data[item_alias]
        is_debug = self.dict_checkbox_var[item_alias].get()
        # on win32, CMD "start" will keep new process async with GUI.
        cmd_str = 'start "%s" /D "%s"' %(item_alias, item_dict['folder'])

        if is_debug or item_dict['interpreter'].endswith('python.exe') or item_dict['interpreter'].endswith('pypy.exe'):
            cmd_str = '%s cmd /K' %cmd_str
        else:
            cmd_str = '%s /B' %cmd_str

        cmd_str = '%s %s %s' %(cmd_str, item_dict['interpreter'], item_dict['main'])

        arg_content = self.dict_str_var[item_alias].get()
        try:
            item_dict['list'].remove(arg_content)
        except:
            pass
        item_dict['list'].insert(0, arg_content)
        while len(item_dict['list']) >= 21:
            item_dict['list'].pop(-1)
        self.dict_cbbox[item_alias]['values'] = item_dict['list']

        cmd_str = '%s %s' %(cmd_str,arg_content)
        logging.info(cmd_str)

        if (item_dict['interpreter'].endswith('python.exe') or item_dict['interpreter'].endswith('pypy.exe')) and (not is_debug):
            os.system('%s ^&^& exit' %cmd_str)
        else:
            os.system(cmd_str)
        self.save_cfg_file()

    def cmd_button_select_file(self,item_alias):
        item_dict = self.json_data[item_alias]
        chosen_file = askopenfilename(initialdir = item_dict['folder'])
        if chosen_file:
            arg_content = self.dict_str_var[item_alias].get()
            self.dict_cbbox[item_alias].set('%s "%s"' %(arg_content,chosen_file))

    def cmd_button_select_folder(self,item_alias):
        item_dict = self.json_data[item_alias]
        chosen_dir = askdirectory(initialdir = item_dict['folder'])
        if chosen_dir:
            arg_content = self.dict_str_var[item_alias].get()
            self.dict_cbbox[item_alias].set('%s "%s"' %(arg_content,chosen_dir))

    def remove_by_item_alias(self, item_alias):
        self.json_data.pop(item_alias)
        self.save_cfg_file()
        self.update_list_frame_view()

    def botton2_on_dict_cbbox(self, item_alias):
        try:
            arg_content = self.dict_str_var[item_alias].get()
            self.json_data[item_alias]['list'].remove(arg_content)
            self.dict_cbbox[item_alias]['values'] = self.json_data[item_alias]['list']
        except:
            pass
        self.dict_cbbox[item_alias].set('')

    def update_list_frame_view(self):
        self.frame_list.grid_forget()
        for widget in self.frame_list.winfo_children():
            widget.destroy()

        item_alias_list = sorted(self.json_data.keys())

        bg_color = ['#efe', '#ffa']
        foreground = '#000'
        for iii in range(len(bg_color)):
            s = ttk.Style()
            color_code = bg_color[iii]
            style_name = '%s.TCombobox' %(color_code[1:])
            s.configure(style_name, foreground=foreground)
            s.configure(style_name, fieldbackground=color_code)

        cbbox_width = 100

        for iii in  range(len(item_alias_list)):
            item_alias = item_alias_list[iii]
            color_code = bg_color[iii%2]
            style_name = '%s.TCombobox' %(color_code[1:])
            font=("consolas",8, 'bold')
            button = Button(self.frame_list, text='  %s' %item_alias, width=15, font=font, bg=color_code, fg=foreground, anchor=W,
                command=lambda item_alias=item_alias:self.cmd_button_run_script(item_alias))
            button.grid     (row=iii, column=0,)
            button.bind('<Button-3>', lambda event, item_alias=item_alias:os.startfile(self.json_data[item_alias]['folder']))

            self.dict_checkbox_var[item_alias] = IntVar()
            checkbutton = Checkbutton(self.frame_list, text="D", variable=self.dict_checkbox_var[item_alias], bg=color_code,)
            checkbutton.grid (row=iii, column=1)

            try:
                self.dict_str_var[item_alias]
            except:
                self.dict_str_var[item_alias] = {}

            try:
                self.dict_cbbox[item_alias]
            except:
                self.dict_cbbox[item_alias]  = {}

            self.dict_str_var[item_alias] = StringVar()
            text_cbbox = Combobox(self.frame_list, textvariable=self.dict_str_var[item_alias],
                font=("Arial",8), width=cbbox_width, height=20, style=style_name)

            self.dict_cbbox[item_alias] = text_cbbox

            if self.json_data[item_alias]:
                text_cbbox['values'] = self.json_data[item_alias]['list']
                text_cbbox.current(0)

            text_cbbox.grid(row=iii, column=2)
            text_cbbox.bind('<Button-2>',
                lambda event, item_alias=item_alias: self.botton2_on_dict_cbbox(item_alias))
            text_cbbox.bind('<Button-3>',
                lambda event,item_alias=item_alias: self.dict_cbbox[item_alias].set(''))
            text_cbbox.bind('<Return>',
                lambda event,item_alias=item_alias: self.cmd_button_run_script(item_alias))

            btn_remove = Button(self.frame_list, bg=color_code, fg=foreground, state=DISABLED, text="", font=font,
                command=lambda item_alias=item_alias:self.remove_by_item_alias(item_alias))
            self.dict_btn_remove[item_alias] = btn_remove
            btn_remove.grid(row=iii, column=97)

            btn_file = Button(self.frame_list, bg=color_code, fg=foreground, text="F", font=font,
                command=lambda item_alias=item_alias:self.cmd_button_select_file(item_alias))
            btn_file.grid(row=iii, column=98)

            btn_dir = Button(self.frame_list, bg=color_code, fg=foreground, text="D", font=font,
                command=lambda item_alias=item_alias:self.cmd_button_select_folder(item_alias))
            btn_dir.grid(row=iii, column=99)
        self.update()
        self.geometry("+0+%d" %(self.winfo_screenheight()-self.winfo_height()-66))

if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG, datefmt='%m%d %H:%M:%S', format='%(asctime)s %(levelname)s %(filename)s:%(lineno)d %(funcName)s: %(message)s')
    handle_main = window_main()
    handle_main.mainloop()
