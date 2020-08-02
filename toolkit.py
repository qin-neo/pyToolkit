#!/usr/bin/python
# -*- coding: utf-8 -*-
# qinhuawei@outlook.com

from tkinter import *
from tkinter.filedialog import askopenfilename,askdirectory
from tkinter.ttk import Combobox
import tkinter.ttk as ttk
import urllib.request
import logging,json,re,os,psutil,time,requests
from datetime import datetime,timedelta

def get_163_stock_info(stock_list, proxyDict):
    # http://api.money.126.net/data/feed/0000001,0601318,money.api?callback=_ntes_quote_callback4621339
    the_url = 'https://api.money.126.net/data/feed/0000001,1399001,1399006'
    for stock_id in stock_list:
        if stock_id.startswith('sh'):
            stock_id = f'0{stock_id[2:]}'
        elif stock_id.startswith('sz'):
            stock_id = f'1{stock_id[2:]}'
        the_url = f'{the_url},{stock_id}'
    the_url = f'{the_url},money.api?callback=_ntes_quote_callback{datetime.now().microsecond}'
    #logging.debug(the_url)

    r = requests.get(the_url,  proxies=proxyDict, verify=False, timeout=(2,3))
    stocks_info = re.search(r'_ntes_quote_callback\d+\(([^\)]+)\)', r.text).group(1)
    #logging.debug(r.text)
    stocks_json = json.loads(stocks_info)
    stock_str = ''
    for stock_id, stock_dict in stocks_json.items():
        stock_str = '%s%8.2f%6.2f%5s\n' %(stock_str, stock_dict['price'], 100.0*stock_dict['percent'], stock_dict['name'],)
    return stock_str

class show_stock_info():
    stock_json = "stock.json"
    prev_sent = 0
    prev_recv = 0
    ts = 0
    stock_info = '\n\n\n\n\n\n'

    def __init__(self, ):
        self.read_stock_json()
        self.root = Toplevel()
        #self.root.attributes('-toolwindow', 1)
        self.root.attributes('-topmost', 'true')
        self.root.overrideredirect(True)
        self.root.resizable(width=False, height=False)

        self.label_info = Label(self.root, font = ('consolas',self.config["fontsize"]),fg='#000',bg='white',text=self.stock_info)
        self.label_info.grid()
        self.root.attributes('-alpha', self.config['transparent'])
        self.root.wm_attributes("-transparentcolor", "white")
        self.label_info.bind('<Button-1>', lambda event:os.startfile(os.path.join(os.path.dirname(__file__),self.config['stock_page'])))
        self.label_info.bind('<Button-3>', lambda event:self.root.destroy())
        self.label_info.bind("<Enter>", lambda event:self.root.attributes('-alpha', self.config['transparent']+0.5))
        self.label_info.bind("<Leave>", lambda event:self.root.attributes('-alpha', self.config['transparent']))

        try:
            self.show_stock()
            self.root.geometry(f"+{self.root.winfo_screenwidth() - self.root.winfo_width()}+{self.root.winfo_screenheight() - self.root.winfo_height() - 76}")
            self.root.update()
            self.root.geometry(f"+{self.root.winfo_screenwidth() - self.root.winfo_width()}+{self.root.winfo_screenheight() - self.root.winfo_height() - 76}")
            self.root.update()
        except:
            logging.exception('-------------------------------')
            self.root.destroy()
            os.startfile(self.stock_json)

    def read_stock_json(self):
        self.config = {
            "proxy": "",    # http://127.0.0.1:1234
            "stocks": "",    # sh601166,sh601818,sz002419,sh600016
            "refresh": 3000,
            "transparent":  0.2,
            "fontsize": 10,
            "stock_page": "qq/index.html",
            "open_hour": 9,
            "close_hour": 15,
        }

        if not os.path.isfile(self.stock_json):
            with open(self.stock_json, 'w') as fd:
                json.dump(self.config, fd, indent=4)

        with open(self.stock_json) as json_file:
            self.config = json.load(json_file)
        self.stock_list = re.findall(r'(\w+)', self.config["stocks"])
        if self.config["proxy"]:
            self.proxyDict = {
                "http"  : self.config["proxy"],
                "https" : self.config["proxy"],
            }
        else:
            self.proxyDict = None

    def show_stock(self):
        ts = datetime.now()
        try:
            if self.stock_list and ts.weekday()<5 and ts.hour>=self.config['open_hour'] and ts.hour<self.config['close_hour']:
                self.stock_info = get_163_stock_info(self.stock_list, self.proxyDict)
        except:
            if self.stock_info.count('BAD') < 3:
                self.stock_info = 'BAD\n%s' %(self.stock_info)

        ts = time.time()
        net = psutil.net_io_counters()
        bytes_recv = net.bytes_recv
        bytes_sent = net.bytes_sent
        factor = 1024*(ts - self.ts)
        self.label_info.config(text='%5.1f%% %5.1f %5.1f ██\n%s' %(psutil.cpu_percent(), (bytes_sent-self.prev_sent)/factor, (bytes_recv-self.prev_recv)/factor, self.stock_info))
        #self.root.geometry("+%d+%d" %(self.root.winfo_screenwidth()-115,self.root.winfo_screenheight()-120))
        #self.root.geometry(f"+{self.root.winfo_screenwidth()-self.root.winfo_width()}+{self.root.winfo_screenheight()-self.root.winfo_height()-66}")
        self.prev_recv = bytes_recv
        self.prev_sent = bytes_sent
        self.ts = ts
        self.root.after(self.config['refresh'], self.show_stock)

class countdown_timer():
    pid = None
    after = None
    def __init__(self, duration):
        self.loop_id = -1
        self.width = 100
        self.height = 25
        self.on_top = 200
        self.action_list = ['U', 'D']
        self.duration = duration
        self.root = Toplevel()
        self.root.title('Timer')
        self.root.attributes('-toolwindow', 1)
        #self.root.wm_attributes("-topmost", 1)
        self.root.attributes('-topmost', 'true')
        self.root.overrideredirect(True)
        self.root.resizable(width=False, height=False)
        self.root.configure(background='#000')
        self.create_label_countdown()
        self.set_label_window()
        self.root.protocol('WM_DELETE_WINDOW', self.exit_now)
        self.restart_countdown()

    def set_label_window(self):
        #self.root.geometry("%dx%d+%d+%d" %(self.width,self.height,self.root.winfo_screenwidth()-self.width, self.root.winfo_screenheight()-self.on_top)) #winfo_screenheight()
        self.root.geometry("%dx%d+%d+%d" %(self.width,self.height,0, self.root.winfo_screenheight()-self.on_top)) #winfo_screenheight()
        self.label_countdown.configure(background='#000')
        self.root.attributes('-alpha', 0.3)
        self.root.attributes('-topmost', 'true')

    def exit_now(self,):
        if self.pid:
            self.pid.terminate()
        self.root.destroy()

    def create_label_countdown(self):
        self.label_countdown = Label(self.root, text='-0_%02d:%02d' %(self.duration/60,self.duration%60),font = ('consolas bold',15),bg='#000',fg = '#fff')
        self.label_countdown.pack(fill=BOTH)
        self.label_countdown.bind('<Button-1>', lambda event:self.restart_countdown())
        self.label_countdown.bind('<Button-3>', lambda event:self.exit_now())

    def restart_countdown(self):
        if self.pid:
            self.pid.terminate()
        if self.after:
            self.root.after_cancel(self.after)
        self.set_label_window()
        self.loop_id = (self.loop_id + 1)%10
        self.label_countdown.config(text='%s%d_%02d:%02d' %(self.action_list[self.loop_id%2],self.loop_id,self.duration/60,self.duration%60))
        self.clock = self.duration+1
        self.countdown()

    def countdown(self,):
        self.clock = self.clock - 1
        if self.clock > 0:
            if self.clock % 120 == 0:
                self.set_label_window()
            self.label_countdown.config(text='%s%d_%02d:%02d' %(self.action_list[self.loop_id%2],self.loop_id,self.clock/60,self.clock%60))
            self.after = self.root.after(1000, self.countdown)
            return
        if self.clock <= 0 and self.clock % 10 == 0:
            self.root.geometry('%dx%d+%d+%d' %(self.root.winfo_screenwidth(),self.height,0,self.root.winfo_screenheight()/2))
            self.root.attributes('-alpha', 1)
            self.root.attributes('-topmost', 'true')

        tmp=-1*self.clock/2
        bg_colors = ['#f00','#000']
        self.label_countdown.config(text='%s%d_%02d:%02d' %(self.action_list[self.loop_id%2],self.loop_id,tmp/60,tmp%60), background=bg_colors[self.clock%2])
        self.after = self.root.after(500, self.countdown)

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
    dict_btn_del  = {}
    frame_batch = None
    dict_batch = {}
    del_enabled = False
    color_list = ['#2E2EFE', '#F45F04']
    fontzie = 9
    font=('Courier New', fontzie)

    def __init__(self):
        Tk.__init__(self)
        self.load_cfg_file()
        self.title('ToolKit')
        self.wm_iconbitmap( '@icon.xbm')
        self.resizable(width=False, height=False)
        width=10
        btn_bg = '#ffe'
        btn_fg = '#00f'

        frame_title = Frame(self)
        frame_title.grid(row=0, column=0)
        frame_table = Frame(self)
        frame_table.grid(row=1, column=0)
        self.frame_batch_init()

        self.button_add =  Button(frame_title,font=self.font, width=width, bg=btn_bg, fg=btn_fg, text="ADD", command=lambda:popup_option_menu('ADD',self.callback_add_command,).grab_set())
        self.button_del_item = Button(frame_title, font=self.font, width=width, bg=btn_bg, fg=btn_fg, text="DEL", command=self.show_btn_del)
        self.button_help = Button(frame_title,font=self.font, width=width, bg=btn_bg, fg=btn_fg, text="HELP", command=lambda :os.startfile("https://github.com/qin-neo/pyToolkit") )
        self.button_cpu = Button(frame_title, font=self.font, width=width, bg=btn_bg, fg=btn_fg, text="CPU", command=self.btn_cmd_cpu)

        self.var_entry_timer = IntVar()
        self.var_entry_timer.set(2400)
        self.button_countdown = Button(frame_title,font=self.font, width=width, bg=btn_bg, fg=btn_fg, text="CountDown", command=self.cmd_btn_countdown)
        entry_timer = Entry(frame_title, textvariable=self.var_entry_timer, width=width)

        row_id = 0
        self.button_add.grid   (row=row_id, column=0,)
        self.button_del_item.grid      (row=row_id, column=1)
        self.button_help.grid      (row=row_id, column=2,)
        self.button_cpu.grid      (row=row_id, column=3,)
        self.button_countdown.grid      (row=row_id, column=4,)
        entry_timer.grid      (row=row_id, column=5,)

        self.frame_list = Frame(frame_table, )
        self.frame_list.pack(fill=BOTH)
        self.update_list_frame_view()

        self.frame_tips = Toplevel(self,bd=1,bg="black")
        self.frame_tips.withdraw()
        self.frame_tips.overrideredirect(1)
        self.frame_tips.transient()
        self.label_tips=Label(self.frame_tips,bg="grey",justify='left')
        self.label_tips.pack()
        help_info = '''  Windows ToolKit, shortcuts with parameters.
    Author: qinhuawei@outlook.com 2018-07-15.
  Left-Click on Alias button: execute shortcut.
  Right-Click on Alias button: open main folder.
  Right-Click in text-entry: clean text-entry, and trigger dropdown.
  Mid-Click in text-entry: remove chosen line from history.
  Double-Click in text-entry: select all and copy.
  DEL button: enable "-" button to delete shortcut.
  CountDown button: start a timer on upper right corner of screen.
    Left-Click on timer: reset timer.
    Right-Click on timer: exit timer.'''
        self.button_help.bind("<Enter>", lambda event:self.show_tips(help_info,self.button_help))
        self.button_help.bind("<Leave>", lambda event:self.frame_tips.withdraw())
        self.button_cpu.bind('<Button-3>', lambda event:os.startfile(r'.\stock.json'))

    def frame_batch_init(self):
        self.frame_batch = Frame(self, bd=1,background='blue',)
        self.frame_batch.grid(row=1, column=1, sticky="ns")
        frame_btn = Frame(self.frame_batch)
        #frame_btn.grid(row=0,sticky='W')
        frame_btn.pack(side='top', anchor='w')
        btn_close = Button(frame_btn, font=self.font, text="CLOSE", command=self.frame_batch_close)
        btn_close.grid(row=0, column=0)
        btn_clean = Button(frame_btn, font=self.font, text="CLEAN", command=self.frame_batch_clean)
        btn_clean.grid(row=0, column=1)
        btn_run = Button(frame_btn, font=self.font, text="RUN", command=self.frame_batch_run)
        btn_run.grid(row=0, column=2)
        self.frame_batch.grid_remove()
        self.batch_lables = None

    def frame_batch_close(self):
        self.frame_batch_clean()
        self.frame_batch.grid_remove()

    def frame_batch_clean(self):
        self.batch_lables.destroy()
        self.batch_lables = None

    def frame_batch_create(self, item_alias):
        self.frame_batch.grid()
        if not self.batch_lables:
            self.batch_lables = Frame(self.frame_batch, bd=1,background='blue',)
            self.batch_lables.pack()

        arg_content = self.dict_str_var[item_alias].get()
        label = Label(self.batch_lables, font=self.font, anchor="w", text='%s: %s' %(item_alias,arg_content))
        label.grid(sticky='w')
        label.bind('<Button-3>',lambda event,item_alias=item_alias: label.destroy())

    def frame_batch_run(self):
        cmd_str = ''
        for label in self.batch_lables.winfo_children():
            item_alias, arg_content = label.cget("text").split(':',1)
            item_dict = self.json_data[item_alias]
            cmd_str = '%s CD /D "%s" & %s %s %s &' %(cmd_str, item_dict['folder'], item_dict['interpreter'], item_dict['main'], arg_content)

        logging.info(cmd_str)
        os.system(cmd_str)

    def btn_cmd_cpu(self,):
        try:
            if Toplevel.winfo_exists(self.bull.root):
                self.bull.root.destroy()
                return
        except:
            pass
        self.bull = show_stock_info()

    def cmd_btn_countdown(self,):
        try:
            if Toplevel.winfo_exists(self.countdown.root):
                self.countdown.set_label_window()
                return
        except:
            pass
        self.countdown = countdown_timer(self.var_entry_timer.get())

    def show_tips(self, info_text, anchor):
        self.frame_tips.geometry('+%d+%d' %(anchor.winfo_rootx(),(anchor.winfo_rooty()+20)))
        self.frame_tips.deiconify()
        self.label_tips.config(text=info_text)

    def show_btn_del(self):
        if self.del_enabled:
            self.del_enabled = False
            for item_alias in self.json_data.keys():
                self.dict_btn_del[item_alias].grid_remove()
        else:
            self.del_enabled = True
            for item_alias in self.json_data.keys():
                self.dict_btn_del[item_alias].grid()

    def init_item_context(self,item_alias, main_file, main_folder, interpreter):
        if not main_folder:
            try:
                main_folder = os.path.dirname(main_file)
            except:
                pass
        if not main_folder:
            main_folder = '%userprofile%'
        main_folder = (main_folder.replace("/", "\\")).strip()
        self.json_data[item_alias] = {}
        self.json_data[item_alias]['list'] = []
        self.json_data[item_alias]['main'] = os.path.basename(main_file)  #(re.sub(r'(\s+)', r'"\1"',main_file)).strip()
        self.json_data[item_alias]['folder'] = main_folder
        self.json_data[item_alias]['interpreter'] = interpreter.strip()
        logging.debug('alias [%s] main_file [%s] main_folder [%s]' %(item_alias, main_file, main_folder))

    def load_default_cfg(self):
        self.init_item_context(' RUN', ' ', '', '')
        self.json_data['start']['list'] = ['https://github.com/qin-neo/pyToolkit',]

    def load_cfg_file(self):
        for iii in range(900):
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
        self.json_data[item_alias]['debug'] = is_debug

        if is_debug or item_dict['interpreter'].endswith('python') or item_dict['interpreter'].endswith('pypy'):
            cmd_str = 'start "%s" /D "%s" cmd /K ' %(item_alias, item_dict['folder'])
        else:
            #cmd_str = 'set path=%%path%%;"%s" & start "%s" /B ' %(item_dict['folder'], item_alias)
            logging.critical('~~~~~~~~~~~~~~~~')
            cmd_str = 'start "%s" /D "%s" /B ' %(item_alias, item_dict['folder'])

        cmd_str = '%s %s %s' %(cmd_str, item_dict['interpreter'], os.path.basename(item_dict['main']))

        arg_content = self.dict_str_var[item_alias].get()
        try:
            item_dict['list'].remove(arg_content)
        except:
            pass
        item_dict['list'].insert(0, arg_content)
        while len(item_dict['list']) >= 30:
            item_dict['list'].pop(-1)
        self.dict_cbbox[item_alias]['values'] = item_dict['list']

        cmd_str = '%s %s' %(cmd_str,arg_content)
        logging.info('\n'+cmd_str)

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

    def botton3_on_dict_cbbox(self, item_alias):
        self.dict_cbbox[item_alias].focus_set()
        self.dict_cbbox[item_alias].set('')
        self.dict_cbbox[item_alias].event_generate('<Down>')

    def select_all_and_copy(self,item_alias, event):
        self.frame_tips.withdraw()
        event.widget.select_range(0, END)
        event.widget.event_generate('<Control-c>')
        self.frame_tips.geometry('+%d+%d' %(self.dict_cbbox[item_alias].winfo_rootx(),(self.dict_cbbox[item_alias].winfo_rooty()+20)))
        self.frame_tips.deiconify()
        self.label_tips.config(text='copied.')
        self.frame_tips.after(500, self.frame_tips.withdraw)

    def update_list_frame_view(self):
        self.frame_list.grid_forget()
        for widget in self.frame_list.winfo_children():
            widget.destroy()

        item_alias_list = sorted(self.json_data.keys())

        font = ("Microsoft YaHei UI", self.fontzie, )
        cbbox_font = ("Courier New", self.fontzie,)
        cbbox_width = 100

        self.frame_list.option_add('*TCombobox*Listbox.font', cbbox_font)
        # *TCombobox*Listbox.selectBackground

        for color_code in self.color_list:
            style_name = f'{color_code}.TCombobox'
            s = ttk.Style()
            s.configure(style_name, foreground=color_code,)

        for iii in  range(len(item_alias_list)):
            item_alias = item_alias_list[iii]
            color_code = self.color_list[iii%2]
            style_name = f'{color_code}.TCombobox'

            button = Button(self.frame_list, text='  %s' %item_alias, width=15, font=font, fg=color_code, anchor=W,
                command=lambda item_alias=item_alias:self.cmd_button_run_script(item_alias))
            button.grid     (row=iii, column=0,)
            button.bind('<Button-3>', lambda event, item_alias=item_alias:os.startfile(self.json_data[item_alias]['folder']))

            self.dict_checkbox_var[item_alias] = IntVar()
            try:
                if self.json_data[item_alias]['debug']:
                    self.dict_checkbox_var[item_alias].set(1)
                else:
                    self.dict_checkbox_var[item_alias].set(0)
            except:
                self.dict_checkbox_var[item_alias].set(0)
            checkbutton = Checkbutton(self.frame_list, text="D", variable=self.dict_checkbox_var[item_alias], fg=color_code,)
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
                width=cbbox_width, style=style_name, font=cbbox_font,)

            self.dict_cbbox[item_alias] = text_cbbox

            if self.json_data[item_alias]:
                text_cbbox['values'] = self.json_data[item_alias]['list']
                if text_cbbox['values']:
                    text_cbbox.current(0)

            text_cbbox.grid(row=iii, column=2, sticky=NS)
            text_cbbox.bind('<Button-2>',
                lambda event, item_alias=item_alias: self.botton2_on_dict_cbbox(item_alias))
            text_cbbox.bind('<Button-3>',
                lambda event,item_alias=item_alias: self.botton3_on_dict_cbbox(item_alias))
            text_cbbox.bind('<Return>',
                lambda event,item_alias=item_alias: self.cmd_button_run_script(item_alias))

            #text_cbbox.bind('<Double-Button-1>', lambda event,item_alias=item_alias: self.select_all_and_copy(item_alias,event))
            text_cbbox.bind('<Double-Button-1>', lambda event,item_alias=item_alias: self.frame_batch_create(item_alias))

            btn_del = Button(self.frame_list, fg=color_code, text="-", font=font,
                command=lambda item_alias=item_alias:self.remove_by_item_alias(item_alias))
            self.dict_btn_del[item_alias] = btn_del
            btn_del.grid(row=iii, column=97)
            btn_del.grid_remove()

            btn_file = Button(self.frame_list, fg=color_code, text="F", font=font,
                command=lambda item_alias=item_alias:self.cmd_button_select_file(item_alias))
            btn_file.grid(row=iii, column=98)

            btn_dir = Button(self.frame_list, fg=color_code, text="D", font=font,
                command=lambda item_alias=item_alias:self.cmd_button_select_folder(item_alias))
            btn_dir.grid(row=iii, column=99)
        self.update()
        self.focus_force()
        self.geometry("+0+%d" %(self.winfo_screenheight()-self.winfo_height()-66))

if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG, datefmt='%m%d %H:%M:%S', format='%(asctime)s %(levelname)s %(filename)s:%(lineno)d %(funcName)s: %(message)s')
    logging.info('========== START NOW ===========')
    handle_main = window_main()
    handle_main.mainloop()
