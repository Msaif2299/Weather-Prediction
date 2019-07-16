import tkinter as tk
from tkinter import ttk
import matplotlib as plt
plt.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure
import datetime
import numpy as np
import pandas as pd
from MultiStationBuilder import *

INIT_DATE = "20190703" #found using date_checker.py , not automated as user may not have .csv files on hand , will be different on different systems , change before using


LARGE_FONT= ("Verdana", 12)
MEDIUM_FONT = ("Verdana", 10)
SMALL_FONT = ("Verdana",7)


class mainWindow(tk.Tk):
    def __init__(self, *args, **kwargs):
        
        tk.Tk.__init__(self, *args, **kwargs)
        self.container = ttk.Frame(self)
        self.title('Weather Prediction')
        self.minsize(700,500)#set minsize so dates dont overlap in graph
        style = ttk.Style(self)
        style.configure('TLabel', background='black', foreground='white')
        style.configure('TFrame', background='black')
        style.configure('TButton', background='green' , foreground = 'black')

        self.container.pack(side="top", fill="both", expand = True)
        
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        frame = StartPage(self.container,self)
        self.frames[StartPage] = frame
        frame.grid(row=0,column=0,sticky="nsew")
        self.show_frame(StartPage)

    def create_pageone(self ,station_number ,name):#Used to generate base date page
        frame = PageOne(self.container, self,station_number,name)
        self.frames[PageOne] = frame
        frame.grid(row=0, column=0, sticky="nsew")
        self.show_frame(PageOne)

    def create_pagetwo(self ,station_number,name,property_name,values,no_of_days ):#Used to generate base date page
        frame = PageTwo(self.container,self,station_number,name,property_name,values,no_of_days)
        self.frames[PageTwo] = frame
        frame.grid(row=0, column=0, sticky="nsew")
        self.show_frame(PageTwo)


    def show_frame(self, cont): #used to select from possible frame list

        frame = self.frames[cont]
        frame.tkraise()

        

class StartPage(ttk.Frame):

    def __init__(self, parent, controller):
        station_list = pd.read_csv(os.getcwd() + "/data/csv/selection_list.csv")
        keys = station_list['Name'].tolist()
        values = station_list['STN---'].tolist()
        station_list = dict(zip(keys,values))
        keys.sort()
        ttk.Frame.__init__(self,parent)
        label = ttk.Label(self, text=" Start Page", font=LARGE_FONT,style = 'TLabel')
        label.pack(pady=10,padx=10)
        label = ttk.Label(self, text=" Please Select A Station:", font=LARGE_FONT,style = 'TLabel')
        label.pack(pady=10,padx=10)
        station_selector = tk.StringVar(self)
        station_selector.set(keys[0]) # default value
        station_menu = tk.OptionMenu(self, station_selector, *keys)
        station_menu.config(width=30)
        station_menu.pack()
        button = tk.Button(self, text="View Predictions",
                            bg='#000000',                             
                            fg='#b7f731',                             
                            relief='raised',                             
                            height = 2,
                            width=30,
                            command=lambda: controller.create_pageone(station_list[station_selector.get()],station_selector.get()),
                            )
        button.pack(pady=20)


class PageOne(ttk.Frame):

    def __init__(self, parent, controller,station_number,name):
        ttk.Frame.__init__(self, parent)
        label = ttk.Label(self, text=f"Currently viewing data for station number {station_number} located at {name}", font=LARGE_FONT)
        label.pack(pady=10,padx=10)
        returned_predictions = get_predictions(station_number,14)
        #print(returned_predictions)
        predictions = {k: v for k, v in returned_predictions.items() if v is not None}
        data = f"Prediction For Date :{(datetime.datetime.strptime(INIT_DATE, '%Y%m%d') + datetime.timedelta(days=1)).date()}\n\n"
        for k,v in predictions.items():
            data=data+f" Prediction of  {k} : {v[0]}\n"
        label2 = ttk.Label(self, text=data, font=LARGE_FONT,justify=tk.LEFT)
        label2.pack(pady=10,padx=10)
        #print(predictions)
        keys = list(predictions.keys())

        label3 = ttk.Label(self, text="Please Select A Property To Plot:", font=LARGE_FONT,justify=tk.LEFT)
        label3.pack(pady=0,padx=10)
        property_selector = tk.StringVar(self)
        property_selector.set(keys[0]) # default value
        property_menu = tk.OptionMenu(self, property_selector, *keys )
        property_menu.config(width=20 )
        property_menu.pack(pady=10)



        button2 = tk.Button(self, text="Plot Prediction for 1 week",
                            bg='#000000',                             
                            fg='#b7f731',                             
                            height = 2,relief='raised',                             
                            width=30,
                            command=lambda: controller.create_pagetwo(station_number,name,property_selector.get(),predictions[property_selector.get()],7))
        button2.pack(pady=10)
        button2 = tk.Button(self, text="Plot Prediction for 2 weeks",
                            bg='#000000',                             
                            fg='#b7f731',                             
                            height = 2,relief='raised',                             
                            width=30,
                            command=lambda: controller.create_pagetwo(station_number,name,property_selector.get(),predictions[property_selector.get()],14))
        button2.pack(pady=10)
        button1 = tk.Button(self, text="Go Back To Start Page",
                            bg='#000000',                             
                            fg='#b7f731',                             
                            height = 2,relief='raised',                             
                            width=30,
                            command=lambda: controller.show_frame(StartPage))
        button1.pack(pady=10)


class PageTwo(ttk.Frame):

    def __init__(self, parent, controller,station_number ,name,property_name,values,no_of_days):
        ttk.Frame.__init__(self, parent)
        label = ttk.Label(self, text=f"Currently viewing {property_name} data for station number {station_number} located at {name}", font=LARGE_FONT)
        label.pack(pady=10,padx=10)
        button2 = tk.Button(self, text="Select Another Property For Same Station",
                            bg='#000000',                             
                            fg='#b7f731',                             
                            height = 2,relief='raised',                             
                            width=30,
                            command=lambda: controller.show_frame(PageOne))
        button2.pack(pady=5)

        button1 = tk.Button(self, text="Go Back To Start Page",
                            bg='#000000',                             
                            fg='#b7f731',                             
                            height = 2,relief='raised',                             
                            width=30,
                            command=lambda: controller.show_frame(StartPage))
        button1.pack(pady=5)

        cut_values = values[:no_of_days]
        new_values = [float(i) for i  in cut_values]
        step = datetime.timedelta(days=1)
        start = datetime.datetime.strptime(INIT_DATE, '%Y%m%d')
        start = start + step #because predictions start from one day after init_date
        date_list = []
        i = 0
        while(i<no_of_days):
            date_list.append(start)
            start = start + step
            i+=1

        plt.style.use("dark_background") 
        f = plt.Figure(figsize=(5,5), dpi=100)
        a = f.add_subplot(111)
        a.set_xlabel("Date",fontsize = 18)
        a.set_ylabel(property_name,fontsize=18)
        a.plot(date_list,new_values)
        canvas = FigureCanvasTkAgg(f, self)
        canvas.draw()
        canvas.get_tk_widget().pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)
        toolbar = NavigationToolbar2Tk(canvas, self)
        toolbar.update()
        canvas._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True)



app = mainWindow()
#app.title('Weather Prediction')
app.mainloop()
