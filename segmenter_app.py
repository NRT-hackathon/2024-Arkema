from tkinter import *
from PIL import ImageTk, Image
import numpy as np
import glob
import cv2

# done on python 3.10.11, libraries acquired using pip.

# these were acquired using a small JavaScript snippet to get the names from the excel files provided to us.
series_panels = {
    "S1307032": ["1A","1B","1C","1D","2A","2B","2C","2D","3A","3B","3C","3D","4A","4B","4C","4D","5A","5B","5C","5D","6A","6B","6C","6D","7A","7B","7C","7D","8A","8B","8C","8D","9A","9B","9C","9D","10A","10B","10C","10D","11A","11B","11C","11D","11E","13A","13B","13C","13D","15A","15B","15C"],
    "S1307033": ["1A","1B","1C","1D","2A","2B","2C","2D","3A","3B","3C","3D","4A","4B","4C","4D","5A","5B","5C","5D","6A","6B","6C","6D","7A","7B","7C","7D","8A","8B","8C","8D","9A","9B","9C","9D","10A","10B","10C","10D","11A","11B","11C","11D","11E","13A","13B","13C","13D","15A","15B","15C"],
    "S1307035": ["1A","1B","1C","1D","2A","2B","2C","2D","3A","3B","3C","3D","4A","4B","4C","4D","5A","5B","5C","5D","6A","6B","6C","6D","7A","7B","7C","7D","8A","8B","8C","8D","9A","9B","9C","9D","10A","10B","10C","10D","11A","11B","11C","11D","11E","13A","13B","13C","13D","15A","15B","15C"],
    "S1307024": ['2d1A','2d1B','2d1C','2d1D','2d2A','2d2B','2d2C','2d2D','2d3A','2d3B','2d3C','2d3D','2d4A','2d4B','2d4C','2d4D','2d5A','2d5B','2d5C','2d5D','2d6A','2d6B','2d6C','2d6D','2d7A','2d7B','2d7C','2d7D']
}

def panel_value_generator(panel_set_name: str):
    """
    Generates the names of the panels for tracking which panel is getting cut

    Keywords:
        panel_set_name [str] - the name of the set of panels to evaluate
    """
    panel_set = series_panels[panel_set_name] + ["end"] # include an end character to know when to stop
    for panel_value in panel_set:
        yield panel_value

def file_generator():
    """
    Generates the list of files for cutting images sequentially. Assumes there is a folder called panels in the same directory as this script.
    NOTE: All the new data was filed under S1307024 for easy acquisition. These samples were all from different sets, but merging them under one name made for easier separation.
    """
    # these are the 4 datasets we were given with labels, this is done manually to avoid cases where only one is useful.
    fileset0 = glob.glob(".\panels\S1307024\*\*.JPG")
    fileset1 = glob.glob(".\panels\S1307032\*\*.JPG")
    fileset2 = glob.glob(".\panels\S1307033\*\*.JPG")
    fileset3 = glob.glob(".\panels\S1307035\*\*.JPG")

    all_files = fileset0+fileset1+fileset2+fileset3+["end"] # merge all filesets together
    for file in all_files:
        yield file

# initialize variables
img = None # image to display

file_gen = None # the generator used to iterate through the image files
panel_gen = panel_value_generator("S1307024") # the generator for the panel names

current_file = None # current file looked over
current_panel = next(panel_gen) # current panel to evaluate

prev_click_locs = [] # an array that will contain the top left and bottom right pixels of an image to mark the segment

def click(event):
    """
    Save click positions in prev_click_locs
    """
    global prev_click_locs
    print("Mouse position: (%s %s)" % (event.x, event.y))
    if len(prev_click_locs)==2: # if prev_click_locs already has two elements, delete the last one and append this new one
        prev_click_locs.pop()

    prev_click_locs.append([event.x, event.y]) # append the x and y position of click to prev_click_locs
    update_image()

def preprocess_image():
    """
    Apply preprocessing to reduce size and sharpen edges for better clarity.
    """
    global current_file
    img = cv2.imread(current_file)
    size_x, size_y, _ = img.shape
    img = cv2.resize(img, (0,0), fx=.5, fy=.5)
    root.geometry(f"{size_y//2}x{size_x//2+50}")

    hls_img = cv2.cvtColor(img, cv2.COLOR_BGR2HLS_FULL)
    eq_img = cv2.equalizeHist(hls_img[:,:,1])
    hls_img[:,:,1] = eq_img
    img = cv2.cvtColor(hls_img, cv2.COLOR_HLS2RGB_FULL)
    return img

def update_image():
    """
    Updates the application each click to show the previous click location(s)
    """
    global prev_click_locs, text_label, img_label, current_file, current_panel, root
    # Create a colored version of the mask to display
    panel_set_num = current_file.split("\\")[2]
    year = current_file.split("\\")[3][7:11]
    match len(prev_click_locs):
        case 0:
           text = f"Panel: {panel_set_num} - {current_panel} - {year}"+" "*10+"Top Left:"+" "*10+"Bottom Right:"
        case 1:
            text = f"Panel: {panel_set_num} - {current_panel} - {year}"+" "*10+f"Top Left:{prev_click_locs[0]}"+" "*10+"Bottom Right:"
        case 2:
            text = f"Panel: {panel_set_num} - {current_panel} - {year}"+" "*10+f"Top Left: {prev_click_locs[0]}"+" "*10+f"Bottom Right: {prev_click_locs[1]}"

    text_label.config(text=text)
    
    pil_img = Image.fromarray(img)
    tk_img = ImageTk.PhotoImage(pil_img)  # Convert the PIL image to a format Tkinter Label can use
    img_label.config(image=tk_img)
    img_label.image = tk_img  # Keep a reference

def undo():
    """
    Undo function for clicks
    """
    global prev_click_locs
    if prev_click_locs:
        prev_click_locs.pop()  # delete previous click
        update_image()

def reset():
    """
    Resets all clicks (slightly redundant with undo, same functionality as pressing undo twice)
    """
    global prev_click_locs
    prev_click_locs = []
    update_image()

def save_image():
    """
    Saves the current panel segment under its associated name
    """
    global prev_click_locs, current_file, current_panel, panel_gen
    if len(prev_click_locs)!=2: # if there are not two clicks, then do not save
        return
    
    panel_set_num = current_file.split("\\")[2] # get the panel set number
    year = current_file.split("\\")[3][7:11] # get the year of the panel

    prev_click_locs = np.array(prev_click_locs)*2 # make into np array and multiply by two (because the image is displayed at 1/2 size to fit on monitor)

    # get click positions
    top_left = prev_click_locs[0]
    bottom_right = prev_click_locs[1]
    
    img = cv2.imread(current_file) # get the image

    # compute equalized image
    hls_img = cv2.cvtColor(img, cv2.COLOR_BGR2HLS_FULL)
    eq_img = cv2.equalizeHist(hls_img[:,:,1])
    hls_img[:,:,1] = eq_img
    save_eq_img = cv2.cvtColor(hls_img, cv2.COLOR_HLS2RGB_FULL)

    save_img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    save_eq_img = save_eq_img[top_left[1]:bottom_right[1], top_left[0]:bottom_right[0]] # build the equalized image for saving
    save_img = save_img[top_left[1]:bottom_right[1], top_left[0]:bottom_right[0]] # build the normal image for saving

    save_eq_img = Image.fromarray(save_eq_img)
    save_img = Image.fromarray(save_img)

    # save the images
    save_eq_img.save(f"./sections/equalized/{panel_set_num}-{current_panel}-{year}.JPG")
    save_img.save(f"./sections/original/{panel_set_num}-{current_panel}-{year}.JPG")

    prev_click_locs = []

    current_panel = next(panel_gen) # get next panel name
    if current_panel == "end": # if next panel name is the end of the set
        panel_gen = panel_value_generator(panel_set_num) # move to next set
        current_panel = next(panel_gen) # get next panel name from new set

    update_image()

def next_image():
    """
    Moves on to next image. Since an image can have a different number of segments, the user must manually dictate when to move to the next image to collect segments.
    """
    global file_gen, current_file, panel_gen, current_panel, root, img
    try: # try to get the next image
        current_file = next(file_gen) 
        if current_file == "end": # if at the end
            root.destroy() # destroy the window
    except: # if it is at the beginning, then no image exists
        file_gen = file_generator() # start the file generator
        current_file = next(file_gen) # set to next file

    panel_set_num = current_file.split("\\")[2]

    img = preprocess_image() # process the image
    update_image() # update to new image

def skip_image():
    """
    Skips the current panel number. If for some reason the panel number is not in the current image file, the panel number is skipped using this function.
    """
    global current_file, panel_gen, current_panel
    panel_set_num = current_file.split("\\")[2] # get panel set number
    current_panel = next(panel_gen) # get next panel name
    if current_panel == "end": # if at the end
        panel_gen = panel_value_generator(panel_set_num) # go to the next set
        current_panel = next(panel_gen) # get next panel name
    update_image()


# Setup Tkinter window
root = Tk()
root.resizable(False, False)
root.title("Image Viewer")


# Initialize label here before update_image() is called
text_label = Label(root, text="Top Left:\tBottom Left:\tBottom Right:\tTop Right:")
text_label.grid(row=1, column=0, columnspan=5)

img_label = Label(root)
img_label.grid(row=2, column=0, columnspan=5)
img_label.bind("<Button-1>", click)

next_image()  # Call next_image() after label is defined

# Buttons for undo, reset, save, next image, and skip panel name
undo_button = Button(root, text="Undo", command=undo)
undo_button.grid(row=3, column=0)

reset_button = Button(root, text="Reset", command=reset)
reset_button.grid(row=3, column=1)

save_botton = Button(root, text="Save", command=save_image)
save_botton.grid(row=3, column=2)

next_botton = Button(root, text="Next", command=next_image)
next_botton.grid(row=3, column=3)

skip_botton = Button(root, text="Skip", command=skip_image)
skip_botton.grid(row=3, column=4)

root.mainloop()

