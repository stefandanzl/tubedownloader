import requests
import m3u8
import shutil
import os
import glob
import ffmpeg
from bs4 import BeautifulSoup
import threading
import time


import tkinter  as tk 
from tkinter import *
from tkinter import filedialog as fd
# root = tk.Tk()
# #root.geometry("800x800")  # Size of the window 
# root.title("TUBE GUI")  # Adding a title



open_filename=""
save_filename=""
episodes=[]
allnone=1
downloading=0

cur_file = -1
cur_ep=-1
len_ep= -1
cur_ts=-1
len_ts=-1


def openf():
    #print("Goodbye World!\nWait, I changed my mind!")
    
    filetypes = (
        ('html files','*.html'),
        ('All files', '*.*'),
        ('csv files','*csv'),
        ('text files', '*.txt')
        )

    open_file = fd.askopenfilename(
        title='Open a file',
        initialdir='C:/Users/stefa/Downloads',
        filetypes=filetypes)
    print(open_file)
    global open_filename
    open_filename=open_file
    
    # with open(open_file) as csvfile:
    #     readCSV = csv.reader(csvfile, delimiter=";")
    # print("works!")
    openbutton.configure(text = "File Loaded",bg="green")




def savef():
    #print("Save")
    


    filetypes = (
        ('html files','*.html'),
        ('csv files','*csv'),
        ('text files', '*.txt'),
        ('All files', '*.*')
        )

    save_file= fd.asksaveasfilename(
        title='Save as file',
        initialdir='C:/',
        filetypes=filetypes,
        defaultextension='.csv')
    print(save_file)
    global save_filename
    save_filename=save_file
    savebutton.configure(text = "Savefile set",bg="green")#, command=goodbye_world,bg="red")



def loadf():
    #pass

    global episodes
    episodes = htmlparser(htmlfile=open_filename)
    


    # # n=10 # number of buttons
    # # i=2
    # for j in range(len(episodes)):
    #     #print(episodes[j,1])
    #     #episodes[j].append(0)
    #     e = Label(scrollable_frame,width=29, justify=LEFT,text=str(episodes[j][1]))#command=lambda k=j: my_fun(k)) 
    #     e.pack()
    #     e.bind("<1>", lambda event, obj=j: onClickB(event, obj))
    #     #e.grid(row=j, column=i) 
    
    
    
    buttonreload()
    print(len(episodes))


    
def startf():
    global downloading
    if not downloading:
        
        downloading = 1


        global cur_ep 
        cur_ep = 0
        global cur_ts 
        cur_ts = 0


        #playlist()
        threading.Thread(target=playlist).start()
        #t.start
        #t.terminate()
        threading.Thread(target=showprogress).start()

def allnonef():
    if not downloading:
        global episodes
        global allnone
        if allnone:
            allnone = 0
        else:
            allnone = 1
        
        for i in range(len(episodes)):
            if allnone:
                episodes[i][2] = 0

            else:
                episodes[i][2] = 1
        buttonreload()
    else:
        print("Currently DOWNLOADING!")



def showprogress():
    while downloading:
        
        progress = "file "+str(cur_file+1)+"/"+str(len_ep+1)+"   section "+str(cur_ts)+"/"+str(len_ts)
        print(progress)
        progresslabel.config(text=progress)
        time.sleep(2)


########################




def strip_end(text, suffix):
    if not text.endswith(suffix):
        return text
    return text[:len(text)-len(suffix)]


def download_file(url):
    local_filename = url.split('/')[-1]
    #NOTee the stream=True parameter
    r = requests.get(url, stream=True)
    with open(f"ts_files/{local_filename}", 'wb') as f:
        for chunk in r.iter_content(chunk_size=1024):
            if chunk:
                f.write(chunk)

    return local_filename



def htmlparser(htmlfile):
    episodelist = []
    with open(htmlfile,"r") as f:
        
        soup = BeautifulSoup(f, "html.parser")
        soup.find_all("a", class_="element")

        episodes = soup.find_all("div", class_="page-content-box page-content-box-episode")

        for each_episode in episodes:
            episode_id = each_episode.find("a")["data-id"]
            # episode_title = each_episode.find_all("div", class_="content-box-episode-title")
            episode_title = each_episode.find("div", class_="content-box-episode-title")["title"]

            
            # info_url = source_url+"/"+each_episode.h3.find("a")["href"]
            # cover_url = source_url+"/catalogue" + \
            #     each_episode.a.img["src"].replace("..", "")

            # title = each_episode.h3.find("a")["title"]
            # rating = each_episode.find("p", class_="star-rating")["class"][1]
            # # can also be written as : each_episode.h3.find("a").get("title")
            # price = each_episode.find("p", class_="price_color").text.strip().encode(
            #     "ascii", "ignore").decode("ascii")
            # availability = each_episode.find(
            #     "p", class_="instock availability").text.strip()

            # Invoke the write_to_csv function
            #write_to_csv([info_url, cover_url, title, rating, price, availability])
            # episodelist.append([info_url, cover_url, title, rating, price, availability])
            episodelist.append([episode_id,episode_title,0])
            #print([episode_id,episode_title])
        #print(episodelist)
    return episodelist


def curl(website):     
    return os.system(f'curl "{website}"')




# /html/body/div[2]/div[5]/div[3]/div[1]/div[2]/a
# document.querySelector("#main-content-container > div:nth-child(2) > a")
# //*[@id="main-content-container"]/div[2]/a
#/html/body/div[2]/div[5]/div[3]/div[1]/div[2]/a/div/div/div[1]/span





def chunklist_options(chunklisturl):
    chunklist = requests.get(chunklisturl)
    #chunklist = curl(chunklisturl) #requests.get(chunklisturl)
    print(chunklist.text)
    #input()
    variant_m3u8 = m3u8.loads(chunklist.text)
    print("Chunklist.text",chunklist.text)
    print("VARIANT",variant_m3u8.is_variant)    # in this case will be True
    if not variant_m3u8.is_variant:
        return "error"
    bandwidth_array = []
    #chunklist_chosen = "error"


    for playlist in variant_m3u8.playlists:
        playlist.uri
        print(playlist.stream_info.bandwidth)
        print(playlist.stream_info.resolution)
        
        bandwidth_array.append(playlist.stream_info.bandwidth)

    bandwidth_array.sort()

    for playlist in variant_m3u8.playlists:    
        if (playlist.stream_info.bandwidth ==bandwidth_array[0]):
            #print("test",playlist[1])
            # print(type(playlist))
            pl = str(playlist)
            a = pl.find("chunklist")
            b = pl.find("?")
            chunklist_chosen = str(playlist)[a:b]+"8"
            print("|>",chunklist_chosen)
    
    return chunklist_chosen





def download_merge(id,chunklist,title):
    m3u8_url = 'https://wowza.tugraz.at/matterhorn_engage/smil:engage-player_'+id+'_presenter.smil/'+chunklist #chunklist_w656979502_b2130322.m3u8'
    r = requests.get(m3u8_url)
    m3u8_master = m3u8.loads(r.text)
    #print(m3u8_master.data['segments'])
    m3u8_file = m3u8_url.split('/')[-1]
    global len_ts
    len_ts = len(m3u8_master.data['segments'])
    url = strip_end(m3u8_url, m3u8_file)
    url_copy = url



    if not os.path.exists('ts_files'):
        print('ts_file folder is not found, creating the folder.')
        os.makedirs('ts_files')



    global cur_ts
    


    concat_file = open("concat.txt","w")
    media_files = []

    # print statement can be deleted, they were placed prior to debugging purposes.
    for seg in m3u8_master.data['segments']:
        #print(url)
        url += seg['uri']
        #print(url)
        cur_ts += 1

        #####print(f'downloading {seg["uri"]}')
        download_file(url)  # comment out this line to download ts files.
        
        concat_file.write(f'file ts_files/{seg["uri"]}\n')
        media_files.append(f'ts_files/{seg["uri"]}')
        #print(f'testing testing{seg["uri"]}')
        url = url_copy
        #print(url)
        ###print()


        # you should comment out the rest part if you want to merge your multiple ts files to one ts file.

    cwd = os.getcwd()  # Get the current working directory (cwd)

    print("concating .ts files")


    concat_file.close()
    #outputname = "output44"

    # Check and rename outputfile mp4 if a file with same name already exists 
    num = 0
    name = title

    while os.path.isfile(name+".mp4"):
        num += 1
        name = title + " - " + "{0:0=2d}".format(num)
        print(num)


    print(name)




    try:
        ffmpeg.input('concat.txt', format='concat', safe=0).output(name+'.mp4', c='copy').run(capture_stdout=True, capture_stderr=True)
 
        #ffmpeg.run(capture_stdout=True, capture_stderr=True)
    except ffmpeg.Error as e:
        print('stdout:', e.stdout.decode('utf8'))
        print('stderr:', e.stderr.decode('utf8'))
        raise e

    for m in media_files:
        os.remove(m)

    # concat_file.close()






# curl ("https://wowza.tugraz.at/matterhorn_engage/smil:engage-player_376a62cb-a5aa-492d-9318-afb62191630e_presenter.smil/playlist.m3u8")


# episodes = htmlparser(htmlfile=f"C:\\Users\\stefa\\Downloads\\Browse - TUBE.html")



def playlist():
    
    for e in range(len(episodes)):
        global cur_file
        
        global len_ep
        
        if episodes[e][2]:
            len_ep+=1
    
    for e in range(len(episodes)):
        global cur_ep
        cur_ep = e
        global cur_ts
        cur_ts = 0
        global len_ts
        len_ts = 0

        if episodes[e][2]:
            cur_file += 1
            chunklisturl = "https://wowza.tugraz.at/matterhorn_engage/smil:engage-player_"+ episodes[e][0] +"_presenter.smil/playlist.m3u8"
            #print(chunklisturl)
            
            chosen_chunklist = chunklist_options(chunklisturl)
            if chosen_chunklist == "error":
                continue
            episodes[e].append( chosen_chunklist)    #address of chosen chunklist quality gets stored

            
            download_merge(episodes[e][0],chosen_chunklist,episodes[e][1])
    global downloading
    downloading = 0
    progresslabel.config(text="Download complete!")

    cur_ep = -1
    len_ep = -1
    cur_ts = -1
    cur_file= -1




def buttonreload():
    global episodes
    # global top_frame

    for widget in scrollable_frame.winfo_children():
        widget.destroy()

    # n=10 # number of buttons
    # i=2
    for j in range(len(episodes)):
        #print(episodes[j,1])
        #episodes[j].append(0)
                
        e = Label(scrollable_frame,width=29, justify=LEFT,text=str(episodes[j][1]))#command=lambda k=j: my_fun(k)) 
        #episodes[j].append(e)
        e.pack()
        e.bind("<1>", lambda event, obj=j: onClickB(event, obj))
        #e.grid(row=j, column=i) 

        if episodes[j][2]:
            e.config(bg="limegreen")
        else:
            e.config(bg="lightgrey")



#m3u8_url = 'https://wowza.tugraz.at/matterhorn_engage/smil:engage-player_40d35d23-5c1e-4ae0-a8f1-4bcb81b55561_presenter.smil/chunklist_w656979502_b2130322.m3u8'




root = tk.Tk()

top_frame = Frame(root, bg='cyan', width=450, height=50, pady=3)

openbutton = Button(top_frame, text="Open File", command=openf)
savebutton = Button(top_frame, text="Save File", command=savef)
loadbutton = Button(top_frame, text="Load File", command=loadf)
allnonebutton = Button(top_frame, text="Load File", command=allnonef)
startbutton = Button(top_frame, text="Start Download", command=startf)
allnonebutton = Button(top_frame, text="ALL/NONE", command=allnonef)

progresslabel = Label(top_frame,text="Open .html file")


openbutton.grid(row=0, column=0, sticky="ns")
savebutton.grid(row=0, column=1, sticky="ns")
loadbutton.grid(row=0, column=2, sticky="ns")
allnonebutton.grid(row=0, column = 3, sticky="ns")
startbutton.grid(row=0, column=3, sticky="ns")
allnonebutton.grid(row=0, column=4, sticky="ns")

progresslabel.grid(row=1,column=0,sticky="ns")

container = tk.Frame(root)
canvas = tk.Canvas(container)
scrollbar = tk.Scrollbar(container, orient="vertical", command=canvas.yview)
scrollable_frame = tk.Frame(canvas)

scrollable_frame.bind(
    "<Configure>",
    lambda e: canvas.configure(
        scrollregion=canvas.bbox("all")
    )
)

canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")

canvas.configure(yscrollcommand=scrollbar.set)


my_str = tk.StringVar()
l1 = tk.Label(container,  textvariable=my_str, width=10 )
l1.pack()
#l1.grid(row=1,column=6,columnspan=6) 

def my_fun(k):
    my_str.set("Btn No is : "+ str(k) )    
    

def onClickA(event):
    print ("you clicked on", event.widget)
    event.widget.config(bg="green")#text="Thank you!")



def onClickB(event, obj):
    global episodes
    print ("you clicked on", obj)
    print ("you clicked on", event.widget)
    print("type",type(obj))
    
    print("guggi",len(episodes))
    #global episodes
    print("epsiose",episodes[obj],"\n\n")
    
    if not downloading:
        if episodes[obj][2]:
            episodes[obj][2]=0
            event.widget.config(bg="lightgrey")
        else:
            episodes[obj][2]=1
            event.widget.config(bg="limegreen")#text="Thank you!")
        # obj.config(text="Thank you!")


            
top_frame.pack()
container.pack()
canvas.pack(side="left", fill="both", expand=True)
scrollbar.pack(side="right", fill="y")

root.mainloop()  # Keep the window open