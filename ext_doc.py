#!/usr/bin/env python3
# Duplicate, Similar, Search, Top Fn add => 50% + 50% ProgBar

from tkinter import *
from tkinter import filedialog, ttk
import sys, glob, os, re
import tarfile, subprocess
import imghdr, shutil
from pathlib import Path
import collections, PIL
from PIL import Image
from itertools import islice
from hashlib import md5
import imagehash, webbrowser

root = Tk()

# Main Frame
frame = Frame(root, height=800, width=700, bd=3, relief=RIDGE)
frame.grid()

# Sub Frames
frame1 = Frame(frame, height=50, width=500, bd=3, relief=GROOVE)
frame1.grid(row=0, column=0, columnspan=2, sticky=NW)

frame2 = Frame(frame, height=300, width=100, bd=3, relief=GROOVE)
frame2.grid(row=1, column=0, rowspan=2, sticky=N)

frame3 = Frame(frame, height=300, width=400, bd=3, relief=GROOVE)
frame3.grid(row=1, column=1, sticky=N)

# Auxillary Functions
def fullpath():
    if var2.get():
        for root,dir,fname in os.walk(en.get()):
            for file in fname:
                yield (os.path.join(root, file))
    else:
        for file in os.listdir(en.get()):
            if os.path.isfile(os.path.join(en.get(), file)):
                yield (os.path.join(en.get(), file))

def filesize(file):
    size = os.path.getsize(file)
    sizeinmb = size/1000000
    sizeflt = "{:.2f}".format(sizeinmb)
    return sizeflt

def lb(text):
    listbox.insert(END, text)
    listbox.yview(END)

def validate():
    if os.path.exists(en.get()):
        return True
    else:
        lb("Error: Incorrect or No Path Entered")
        return False

def browse():
    try:
        dir = filedialog.askdirectory(parent=frame, initialdir='/data/.folder/', title='Please select a directory')
    except:
        dir = filedialog.askdirectory(parent=frame, initialdir=os.getcwd(), title='Please select a directory')
    en.delete(0,END)
    en.insert(0,dir)
    try:
        count_lb()
    except:
        pass

def write():
    if var.get():
        return True
    else:
        #lb("Error: Write Access not enabled")
        return False

def ls():
    if validate():
        lb("File List:")
        for file in fullpath():
            name = os.path.relpath(file, en.get())
            lb(" - "+name)
    lb("")

def count():
    if validate():
        global leng
        x = []
        for file in fullpath():
            x.append(file)
        leng = len(x)
        
def count_lb():
    count()
    lb("Count: "+str(leng))
    lb("")

# Main Functions
def correct():
    if validate():
        bar['value'] = 1
        p,c,d = 1,0,0
        count()
        frame.config(cursor="watch")
        frame.update()
        for file in fullpath():
            bar['value'] = int(p/leng*100)
            root.update_idletasks()
            p += 1
            # find the correct extension
            ftype = imghdr.what(file)
            ext = os.path.splitext(file)[1][1:]
            # find files with the (incorrect) extension to rename
            if ext:
                if ftype != ext:
                    if ftype != None:
                        #File type is JPG or JPEG, ignore the mismatch
                        if (ftype == "jpeg") & (ext == "jpg"):
                            continue
                        # If Ftype is jpeg & Ext not JPG, rename it to jpg
                        elif (ftype == "jpeg") & (ext != "jpg"):
                            filechk = file.replace(ext,"jpg")
                            filechk2 = Path(filechk)
                            if filechk2.is_file():
                                lb("Error: "+file+": File already EXISTS, not overwritting: "+str(filechk2))
                            else:
                                # rename the file
                                lb("Rename file: "+file+" from: "+ext+(" => ")+"jpg")
                                if write():
                                    shutil.move(file, file.replace(ext,"jpg"))
                                    c += 1
                        else:
                            filechk = file.replace(ext,ftype)
                            filechk2 = Path(filechk)
                            if filechk2.is_file():
                                lb("Error: "+file+": File already EXISTS, not overwritting: "+str(filechk2))
                            else:
                                # rename the file
                                lb("Rename file: "+file+" from: "+ext+(" => ")+ftype)
                                if write():
                                    shutil.move(file, file.replace(ext,ftype))
                                    c += 1
                    else:
                        #if ext == "png":
                        #    filechk = file.replace(ext,"jpg")
                        #    filechk2 = Path(filechk)
                        #    if filechk2.is_file():
                        #        lb("Error: "+file+": File already EXISTS, not overwritting: "+filechk2)
                        #    else:
                        #        lb(file+": File type not determined for PNG, Renaming to: => "+file.replace(ext,"jpg"))
                        #        if write():
                        #            shutil.move(file, file.replace(ext,"jpg"))
                        #            c += 1
                        #else:
                            # Could not determine file type by imghdr, try File
                            cmd = "/usr/bin/file '%s'" %file
                            proc = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE).communicate()[0].split(b':')[1]
                            extn = (proc.split()[0]).decode("utf-8")
                            #lb(file+ " ===> "+ extn)
                            if (extn == "HTML") & (ext != "html"):
                                filechk = file.replace(ext,"html")
                                filechk2 = Path(filechk)
                                if filechk2.is_file():
                                    lb("Error: "+file+": File already EXISTS, not overwritting: "+str(filechk2))
                                else:
                                    # rename the file
                                    lb("Rename file: "+file+" from: "+ext+(" => ")+"html")
                                    if write():
                                        shutil.move(file, file.replace(ext,"html"))
                                        c += 1
                            elif (extn == "HTML") & (ext == "html"):
                                continue
                            elif (extn == "JPEG") & (ext == "jpg"):
                                continue
                            elif (extn == "JPEG") & (ext != "jpg"):
                                filechk = file.replace(ext,"jpg")
                                filechk2 = Path(filechk)
                                if filechk2.is_file():
                                    lb("Error: "+file+": File already EXISTS, not overwritting: "+str(filechk2))
                                else:
                                    # rename the file
                                    lb("Rename file: "+file+" from: "+ext+(" => ")+"jpg")
                                    if write():
                                        shutil.move(file, file.replace(ext,"jpg"))
                                        c += 1
                            elif (extn == "ISO") & (ext == "mp4"):
                                continue
                            elif (extn == "RIFF") & (ext == "avi"):
                                continue                                
                            else:
                                lb("Unknown File: "+file+" Format: "+extn)
                                d += 1
                else:
                    # Correct Extension
                    continue
            else:
                # Extensionless: Could not determine file type by imghdr, try File
                if ftype == None:
                    cmd = "/usr/bin/file '%s'" %file
                    proc = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE).communicate()[0].split(b':')[1]
                    extn = (proc.split()[0]).decode("utf-8")
                    #lb(file+ " ===> "+ extn)
                    if extn == "HTML":
                        newname = file +".html"
                        filechk = Path(newname)
                        if filechk.is_file():
                            lb("Error: "+file+": File already EXISTS, not overwritting: "+str(filechk))
                        else:
                            # rename the file
                            lb("Extensionless: "+file+" : has no ext, Appending: .html")
                            if write():
                                shutil.move(file, newname)
                                c += 1
                    elif extn == "JPEG":
                        newname = file +".jpg"
                        filechk = Path(newname)
                        if filechk.is_file():
                            lb("Error: "+file+": File already EXISTS, not overwritting: "+str(filechk))
                        else:
                            # rename the file
                            lb("Extensionless: "+file+" : has no ext, Appending: .jpg")
                            if write():
                                shutil.move(file, newname)
                                c += 1
                    #elif extn == "ISO":
                    #    continue
                    #elif extn == "RIFF":
                    #    continue                                
                    else:
                        lb("Unknown Extensionless File: "+file+" Format: "+extn)
                        d += 1

                elif ftype == "jpeg":
                    newname = file +".jpg"
                    filechk = Path(newname)
                    if filechk.is_file():
                        lb("Error: "+file+": File already EXISTS, not overwriting: "+str(filechk))
                    else:
                        lb(file+": has no ext, Appending: jpg")
                        if write():
                            shutil.move(file, newname)
                            c += 1
                else:
                    newname = file +"."+ ftype
                    filechk = Path(newname)
                    if filechk.is_file():
                        lb("Error: "+file+": File already EXISTS, not overwriting: "+str(filechk))
                    else:
                        lb(file+": has no ext, Appending: "+ftype)
                        if write():
                            shutil.move(file, newname)
                            c += 1
                                
                #lb("Error: "+file+": No Extension detected, Run Missing Extensions function.")
        frame.config(cursor="")
        lb("Info: Total Files: "+ str(leng) +" Processed Files: "+ str(c))
        lb("")

def webpconv():
    if validate():
        bar['value'] = 1
        p = 1
        count()
        frame.config(cursor="watch")
        frame.update()
        c = 0
        for file in fullpath():
            bar['value'] = int(p/leng*100)
            root.update_idletasks()
            p += 1
            name, ext = os.path.splitext(file)
            if ext == ".webp":
                fnpng = name + ".jpg"
                fpath = Path(fnpng)
                if fpath.is_file():
                    lb("Error: "+file+"("+filesize(file)+"MB)"+": File already EXISTS, not overwritting: "+fnpng+"("+filesize(fnpng)+"MB)")
                else:
                    try:
                        if write():
                            im = Image.open(file).convert("RGB")
                            im.save(fnpng, "jpeg")
                            c += 1
                            if fpath.is_file():
                                lb(file+"("+filesize(file)+"MB)"+" deleted and Converted file saved as: "+fnpng+"("+filesize(fnpng)+"MB)")
                                os.remove(file)
                            else:
                                lb("Error: "+file+": Conversion to JPG failed")
                        else:
                            lb("Info: "+file+"("+filesize(file)+"MB)"+" be deleted and Converted file be saved as: "+name+".jpg")
                    except OSError as e:
                        lb("Error: "+file+": Exception occured: "+str(e))
                        pass
                    except:
                        lb("Error: Exception error occured when processing: "+file)
                        pass
            else:
                #File is not Webp, Skipping
                continue
        frame.config(cursor="")
        lb("Info: Total Files: "+ str(leng) +" Processed Files: "+ str(c))
        lb("")

def colonrep():
    if validate():
        bar['value'] = 1
        p = 1
        count()
        frame.config(cursor="watch")
        frame.update()
        c = 0
        for file in fullpath():
            bar['value'] = int(p/leng*100)
            root.update_idletasks()
            p += 1
            if re.search(r':', file):
                filechk = file.replace(":","_")
                filechk2 = Path(filechk)
                if filechk2.is_file():
                    lb("Error: "+file+": File already EXISTS, not overwriting: "+filechk2)
                else:
                    # rename the file
                    if write():
                        shutil.move(file, file.replace(":","_"))
                        lb("Renamed file: "+file+(" => ")+file.replace(":","_"))
                        c += 1
                    else:
                        lb("Info: Renamed file: "+file+(" will be saved as: ")+file.replace(":","_"))
            else:
                continue
                #lb("Error: Colon not found in file: "+file.split('/')[-1])
        frame.config(cursor="")
        lb("Info: Total Files: "+ str(leng) +" Processed Files: "+ str(c))
        lb("")

def duplicate():
    if validate():
        frame.config(cursor="watch")
        frame.update()
        bar['value'] = 1
        p = 1
        count()
        x,y = [],[]
        d = 0
        for file in fullpath():
            bar['value'] = int(p/leng*100)
            root.update_idletasks()
            p += 1
            afile = open(file, 'rb')
            hasher = md5()
            buf = afile.read(65536)
            while len(buf) > 0:
                hasher.update(buf)
                buf = afile.read(65536)
            afile.close()
            hash = hasher.hexdigest()
            y.append(hash)
            x.append(file)
        a = 1
        b = [item for item, count in collections.Counter(y).items() if count > 1]
        for i in range(len(b)):
            lb("Duplicate Set: "+ str(a))
            a += 1
            c = 0
            for j in range(len(y)):
                if b[i] == y[j]:
                    if c == 0:
                        lb("Original File: "+ x[j])
                        c += 1
                    else:
                        if write():
                            os.remove(x[j])
                            lb("Deleted duplicate file: "+ x[j])
                            d += 1
                        else:
                            lb("Info: "+x[j]+" WILL BE deleted")
        frame.config(cursor="")
        lb("Info: Total Files: "+ str(leng) +" Deleted Files: "+ str(d))
        lb("")

def similar():
    if validate():
        bar['value'] = 1
        p = 1
        count()
        frame.config(cursor="watch")
        frame.update()
        x,y,z,a = [],[],[],1
        for file in fullpath():
            bar['value'] = int(p/leng*100)
            root.update_idletasks()
            p += 1
            try:
                hash = imagehash.whash(Image.open(file))
                x.append(file)
                y.append(hash)
            except OSError:
                pass
        c = [item for item, count in collections.Counter(y).items() if count > 1]
        for i in range(len(c)):
            for j in range(i+1, len(c)):
                    if abs(c[i] - c[j]) < 8:
                        z.append(c[i])
        for i in range(len(z)):
            try:
                c.remove(z[i])
            except:
                pass
        for i in range(len(c)):
            lb("Duplicate set:"+ str(a))
            a += 1
            for j in range(len(y)):
                if c[i]-y[j] < 8:
                    #print(x[j], " Factor:", c[i]-y[j])
                    lb("Dupes: "+ x[j] + " Factor: "+str(c[i]-y[j]))
        frame.config(cursor="")
        lb("Info: Total Files: "+ str(leng)+" Duplicate Sets: "+ str(a-1))
        lb("")

def search():
    if validate():
        frame.config(cursor="watch")
        frame.update()
        bar['value'] = 1
        p = 1
        count()
        currdir = os.getcwd()
        img = filedialog.askopenfilename(parent=frame, initialdir=currdir, title='Please select an image')
        try:
            hash1 = imagehash.whash(PIL.Image.open(img))
        except AttributeError:
            lb("Info: Operation cancelled by user")
            return
        except OSError:
            lb("Info: Corrupt image selected: "+img)
            return
        lb("Searching Image: "+img)
        x,y = [],[]
        c = 0
        for file in fullpath():
            bar['value'] = int(p/leng*100)
            root.update_idletasks()
            p += 1
            try:
                hash = imagehash.whash(PIL.Image.open(file))
            except OSError:
                lb("Error: Unsupported File" + file)
                continue
            x.append(file)
            y.append(hash)
        for i in range(len(x)):
            if not (img == x[i]):
                if y[i]-hash1 < 8:
                    lb(x[i]+" Factor: "+str(y[i]-hash1))
                    c += 1
        frame.config(cursor="")
        lb("Info: Total Files: "+ str(leng)+" Duplicate Sets: "+ str(c))
        lb("")

def hugepng():
    if validate():
        frame.config(cursor="watch")
        frame.update()
        bar['value'] = 1
        p,c,d = 1,0,0
        count()
        x = {}
        for file in fullpath():
            bar['value'] = int(p/leng*100)
            root.update_idletasks()
            p += 1
            filesz = os.path.getsize(file)
            name, ext = os.path.splitext(file)
            # search huge PNG Files
            if ((ext == ".png")|(ext == ".PNG")) & (filesz > 1000000):
                d += 1
                fnpng = name + ".jpg"
                fpath = Path(fnpng)
                if fpath.is_file():
                    lb("Error: "+file+"("+filesize(file)+"MB)"+ ": File already EXISTS, not overwritting: "+ fnpng+ "("+filesize(fnpng)+"MB)" )
                else:
                    try:
                        if write():
                            im = Image.open(file).convert("RGB")
                            im.save(fnpng, "jpeg")
                            if fpath.is_file():
                                lb(file+"("+filesize(file)+"MB)"+ " deleted and Converted file saved as: "+ fnpng+ "("+filesize(fnpng)+"MB)")
                                os.remove(file)
                                c += 1
                            else:
                                lb("Error: "+file+": Conversion to JPG failed")
                        else:
                            lb("Info: "+file+"("+filesize(file)+"MB)"+" be deleted and Converted file be saved as: "+fnpng)
                    except OSError as e:
                        lb("Error: "+file+": Exception occured: "+str(e))
                        pass
                    except:
                        lb("Error: Exception error occured when processing: "+file)
                        pass
            else:
                #File is not Huge PNG, Skipping
                continue
        frame.config(cursor="")
        lb("Info: Total Files: "+ str(leng) + " Huge PNG Files: "+ str(d)+ " Converted Files: "+str(c))
        lb("")

# More Auxillary Functions
def backup():
    if validate():
        try:
            os.mkdir("tmp")
        except Exception:
            pass
        tar = tarfile.open(os.path.join("tmp/" + "backup.tar.gz"), "w:gz")
        wr = open(os.path.join("tmp/" + "file_list.txt"), "w")
        wr.write("List of files:\n\n")
        frame.config(cursor="watch")
        frame.update()
        bar['value'] = 1
        p = 1
        count()
        for name in fullpath():
            wr.write(name + '\n')
            tar.add(name)
            lb("File backup: "+name)
            bar['value'] = int(p/leng*100)
            root.update_idletasks()
            p += 1
        frame.config(cursor="")
        wr.close()
        tar.close()
        lb("Info: Total Files backed up: "+str(p-1))
        lb("")

def verify():
    if validate():
        try:
            lb("Initial Count: "+str(leng))
            x = []
            for file in fullpath():
                x.append(file)
            leng2 = len(x)
            lb("Final Count: "+str(leng2))
            if leng == leng2:
                lb("Info: Operation completed successfully")
            else:
                lb("Error: Operation failed, some files missing, Restore from backup !!!")
        except NameError:
            lb("Error: Count function not used before operation, cannot use this feature now")
        lb("")

def delete():
    if validate():
        try:
            shutil.rmtree("tmp")
            lb("Info: Backup Directory Deleted")
        except:
            lb("Error: Backup not found")
        lb("")

def stats():
    if validate():
        lb("Directory Stats are below:")
        x = []
        for file in fullpath():
                ext = os.path.splitext(file)[1][1:]
                x.append(ext)
        y = set(x)
        for i in y:
            lb(i+" : "+str(x.count(i)))
        lb("")

def top():
    if validate():
        bar['value'] = 1
        p = 1
        count()
        frame.config(cursor="watch")
        frame.update()
        x = {}
        for file in fullpath():
            bar['value'] = int(p/leng*100)
            root.update_idletasks()
            p += 1
            filesize = (os.path.getsize(file))
            relfile = os.path.relpath(file, en.get())
            x.update({relfile: filesize})
        # Limit iterations to 10 or less in case lesser no of files
        if (len(x) < 10):
            a = len(x)
        else:
            a = 10
        for i in range(a):
            key, value = max(x.items(), key = lambda p: p[1])
            sizeinmb = (value/1000000)
            sizeflt = "{:.2f}".format(sizeinmb)
            lb(key+" ("+sizeflt+" MB)")
            x.pop((max(x, key=x.get)))
        frame.config(cursor="")
        lb("")

def clear():
    listbox.delete(0, END)

def page():
    webbrowser.open_new(r"https://github.com/amanjosan2008/Image-Extension-Doctor")

def about():
    win1 = Toplevel()
    win1.attributes('-topmost','true')
    win1.title("About")

    frame4 = Frame(win1, height=100, width=300, bd=3, relief=GROOVE)
    frame4.grid()
    Button(frame4, text="Visit Project Page", command=page).grid(row=0, sticky=W)

# Menu Configuration
menu = Menu(frame)

item1 = Menu(menu, tearoff=0)
item1.add_command(label='Browse', command=browse)
item1.add_separator()
item1.add_command(label='Exit', command=exit)

item2 = Menu(menu, tearoff=0)
item2.add_command(label='File Count', command=count_lb)
item2.add_command(label='List Files', command=ls)
item2.add_command(label='Top 10 Files', command=top)
item2.add_separator()
item2.add_command(label='Show Stats', command=stats)
item2.add_command(label='Verify Files', command=verify)

item3 = Menu(menu, tearoff=0)
item3.add_command(label='Backup Files', command=backup)
item3.add_command(label='Delete Backup', command=delete)

item4 = Menu(menu, tearoff=0)
item4.add_command(label='Clear Logs', command=clear)
item4.add_command(label='About', command=about)

menu.add_cascade(label='File', menu=item1)
menu.add_cascade(label='Info', menu=item2)
menu.add_cascade(label='Options', menu=item3)
menu.add_cascade(label='Help', menu=item4)

root.config(menu=menu)

# Entry Widget
Button(frame1, text="Browse: ", width=12, command=browse).grid(row=0, column=0)
en = Entry(frame1, width=60)
en.grid(row=0, column=1)
en.focus_set()

# Checkbuttons
var = IntVar()
c = Checkbutton(frame1, text="Write Access", variable=var)
c.grid(row=0, column=2)

var2 = IntVar()
d = Checkbutton(frame1, text="Recursive", variable=var2)
d.grid(row=0, column=3)

# Buttons for Main Functions
Button(frame2, text="Correct Extensions", width=12, command=correct).grid(row=0)
Button(frame2, text="Webp Convert", width=12, command=webpconv).grid(row=1)
Button(frame2, text="Replace Colon", width=12, command=colonrep).grid(row=2)
Button(frame2, text="Duplicates", width=12, command=duplicate).grid(row=3)
Button(frame2, text="Similar Images", width=12, command=similar).grid(row=4)
Button(frame2, text="Image Search", width=12, command=search).grid(row=5)
Button(frame2, text="Huge PNG", width=12, command=hugepng).grid(row=6)

# Listbox & Scrollbar
scrollbar1 = Scrollbar(frame3, orient=VERTICAL)
scrollbar2 = Scrollbar(frame3, orient=HORIZONTAL)
listbox = Listbox(frame3, height=30, width=100, yscrollcommand=scrollbar1.set, xscrollcommand=scrollbar2.set)
listbox.xview_scroll(3, "pages")
listbox.yview_scroll(3, "pages")
listbox.grid(row=0, columnspan=2)
scrollbar1.config(command=listbox.yview)
scrollbar1.grid(row=0, column=2, ipady = 226)
scrollbar2.config(command=listbox.xview)
scrollbar2.grid(row=1, column=0, columnspan=2, ipadx = 386)

lb("Ready, Log Output: ")

# Progress Bar
Label(frame3, text="Progress:", width=15).grid(row=2, column=0)
bar = ttk.Progressbar(frame3, length=678)
bar.grid(row=2, column=1)

root.title("File Extension Doctor")

try:
    img = PhotoImage(file='icon.png')
    root.tk.call('wm', 'iconphoto', root._w, img)
except:
    lb("Error: icon.png file not found")

root.mainloop()


