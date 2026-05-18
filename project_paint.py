# import modules
import tkinter as tk
from idlelib import help_about
from idlelib.debugger_r import frametable

from PIL import Image as PILImage
from tkinter import *
from tkinter import ttk
from tkinter import filedialog
import random
import io
import numpy as np
import time

from PIL.ImageChops import offset

def start_draw(event):
    global last_x, last_y, current_stroke_ids
    last_x, last_y = event.x, event.y
    current_stroke_ids = []
    redo_stack.clear()
tkinter_colors = [
    # Basics
    "white", "black", "gray", "grey",

    # Reds & Pinks
    "red", "darkred", "crimson", "pink", "hotpink", "deeppink", "lightpink",

    # Oranges & Yellows
    "orange", "darkorange", "coral", "lightcoral", "yellow", "gold", "lightyellow",

    # Greens
    "green", "darkgreen", "forestgreen", "lime", "limegreen", "lightgreen",
    "springgreen", "seagreen", "olive",

    # Blues
    "blue", "darkblue", "mediumblue", "navy", "royalblue", "skyblue",
    "lightskyblue", "deepskyblue", "dodgerblue", "cyan", "turquoise",

    # Purples
    "purple", "violet", "magenta", "orchid", "plum", "lavender",

    # Browns & Tans
    "brown", "saddlebrown", "sienna", "chocolate", "tan", "beige", "wheat",

    # Grays (Common variations)
    "dimgray", "gray50", "darkgray", "lightgray", "gainsboro", "whitesmoke"
]

# define all functions

#       adjustment window 1 def
def change_color():
    global new_colour
    new_colour = tkinter_colors[slider_color.get()]
    print(new_colour)
    label_color.config(text=new_colour)
def change_outline():
    global outline_color
    outline_color = tkinter_colors[slider_outline.get()-1]
    print(outline_color)
    label_outline.config(text=outline_color)

#       adjustment window 2 def
def change_border():
    global border_width
    border_width = label_border.get()
    label_border.config(text=border_width)
    pass
def change_poly():
    global poly_amount
    poly_amount = label_poly.get()
    label_poly.config(text=poly_amount)
    pass
def change_rotation():
    global rotation_amount
    rotation_amount = label_rotation.get()
    label_rotation.config(text=rotation_amount)
    pass
def update_cursor(event=None,arg=None):
    global cursor_follower
    canvas.delete("preview")
    cursor_follower = canvas.create_rectangle(0, 0, 0, 0, outline="grey")
    # Ignore whatever was passed (event or string)
    # and just ask the slider what its current number is.
    try:
        thickness = slider_size.get()
    except:
        thickness = 10  # Default fallback

    radius = thickness / 2
    # We MUST get the current mouse position so the circle
    # doesn't jump to (0,0) when we move the slider.
    x = canvas.winfo_pointerx() - canvas.winfo_rootx()
    y = canvas.winfo_pointery() - canvas.winfo_rooty()
    # 3. CRITICAL SAFEGUARD: Ensure we have clean numbers
    if None in (x, y, radius):
        return  # Abort function early to prevent crashing Tkinter

    # Calculate the exact 4 bounding box points
    x1 = x - radius
    y1 = y - radius
    x2 = x + radius
    y2 = y + radius
    # Apply the NEW radius to the existing coordinates
    canvas.coords(cursor_follower,x1, y1,x2, y2)
    # 1. Handle coordinates safely
    if event is not None:
        # If triggered by a mouse movement/click
        x = canvas.winfo_pointerx() - canvas.winfo_rootx()
        y = canvas.winfo_pointery() - canvas.winfo_rooty()
    else:
        # If triggered manually at startup, park it off-screen or at (0,0)
        canvas_width = canvas.winfo_width()
        canvas_height = canvas.winfo_height()
        x = canvas_width/2
        y = canvas_height/2

    # 2. Clear old preview
    if 'cursor_follower' in globals() and cursor_follower is not None:
        canvas.delete(cursor_follower)

    # 3. Create the new shape
    tool = my_combo.get()
    radius = slider_size.get()





def follow_cursor(event):
    global cursor_follower
    radius = slider_size.get()
    x_position_of_click = event.x
    y_position_of_click = event.y
    x1 = x_position_of_click - radius
    y1 = y_position_of_click - radius
    x2 = x_position_of_click + radius
    y2 = y_position_of_click + radius

    if cursor_follower is not None:
        radius = 15
        canvas.coords(cursor_follower,event.x - radius, event.y - radius,event.x + radius, event.y + radius)
        canvas.tag_raise(cursor_follower)

def stop_draw(event):
    global current_stroke_ids, undo_stack
    if current_stroke_ids:
        # Group the line segments together as one single structural brush action
        undo_stack.append(current_stroke_ids)

def undo_action():
    global undo_stack, redo_stack
    if not undo_stack:
        print("Nothing left to undo!")
        return
    # 1. Pop the last grouped brush stroke off the undo stack
    last_stroke = undo_stack.pop()
    redo_stack.append(last_stroke)
    # 2. Hide all segments belonging to this stroke from the canvas visual layer
    for shape_id in last_stroke:
        canvas.itemconfigure(shape_id, state="hidden")

    canvas.tag_raise("preview")

def redo_action():
    global undo_stack, redo_stack
    if not redo_stack:
        print("Nothing left to redo!")
        return

    # 1. Pop the stroke off the redo stack
    restored_stroke = redo_stack.pop()
    undo_stack.append(restored_stroke)
    # 2. Restore its visibility status on the canvas grid
    for shape_id in restored_stroke:
        canvas.itemconfigure(shape_id, state="normal")
    canvas.tag_raise("preview")

def fill_canvas():
    background_rect = canvas.create_rectangle(0, 0, width, height, fill=tkinter_colors[slider_color.get()])
def clear_canvas():
    canvas.delete("all")

#           adjustment window 1 def
def update_label_color(current_value):
    text = tkinter_colors[slider_color.get()]
    label_color.config(text=text)
def update_label_size(current_value):
    label_size.config(text=current_value)

def update_label_outline(current_value):
    text = tkinter_colors[slider_outline.get()-1]
    label_outline.config(text=text)

def randomise_color():
    random_color = random.randrange(0, len(tkinter_colors))
    print(random_color)
    label_color.config(text=tkinter_colors[random_color])
    slider_color.set(random_color)
def randomise_size():
    random_size = random.randrange(0, 100)
    print(random_size)
    label_size.config(text=random_size)
    slider_size.set(random_size)
def randomise_outline():
    random_outline = random.randrange(0, len(tkinter_colors)-1)
    label_outline.config(text=random_outline)
    slider_outline.set(random_outline)
def randomise_border():
    random_border = random.randrange(0, 100)
    print(random_border)
    label_border_update.config(text=random_border)
    slider_border.set(random_border)
def randomise_poly():
    random_poly = random.randrange(0, 15)
    print(random_poly)
    label_poly_update.config(text=random_poly)
    slider_poly.set(random_poly)
def randomise_rotation():
    random_rotation = random.randrange(0, 15)
    print(random_rotation)
    label_rotation_update.config(text=random_rotation)
    slider_rotation.set(random_rotation)

def update_label_border(current_value):
    label_border_update.config(text=current_value)
def update_label_poly(current_value):
    label_poly_update.config(text=current_value)
def update_label_rotation(current_value):
    label_rotation_update.config(text=current_value)

def save_file(active_canvas,scale_factor=4):
        # 1. Capture the canvas as PostScript data inside system memory
        # Using io.BytesIO avoids clogging your hard drive with temporary .ps files
        canvas.update_idletasks()
        canvas.delete("brush_preview")
        #array of supported formats
        supported_formats = [
            ("PNG Image", "*.png"),
            ("JPEG Image", "*.jpg;*.jpeg"),
            ("BMP Bitmap", "*.bmp"),
            ("GIF Image", "*.gif"),
            ("TIFF Image", "*.tiff;*.tif"),
            ("All Supported Images", "*.png;*.jpg;*.jpeg;*.bmp;*.gif;*.tiff;*.tif"),
            ("All Files", "*.*")
        ]
        # 1. Pop up the system "Save As" window
        file_path = filedialog.asksaveasfilename(
            defaultextension=".png",
            filetypes=supported_formats,
            title="Save Canvas Version As"
        )
        # 2. If the user cancels the pop-up window, exit the function safely
        if not file_path:
            return

        w = active_canvas.winfo_width()
        h = active_canvas.winfo_height()



        target_w = w * scale_factor
        target_h = h * scale_factor
        ps_data = active_canvas.postscript(x=0,y=0,width=w,height=h,
                                           colormode='color',
                                           pagewidth=target_w, pageheight=target_h)
        ps_image = PILImage.open(io.BytesIO(ps_data.encode('utf-8')))
        #convert to RGB
        ps_image = ps_image.convert('RGB')
        # 2. Convert the Pillow Image into a NumPy Array
        # This creates an array of shape (Height, Width, 3) for RGB colors
        img_array = np.array(ps_image)
        # 3. Convert the NumPy Array back into a Pillow Image
        final_image = PILImage.fromarray(img_array)

        # 4. Save or display the final image
        final_image.save(file_path)
        print(f"Successfully reconstructed image saved as '{file_path}'")


def program_1():
    canvas.bind("Button-1",start_draw)
    canvas.bind("<B1-Motion>", draw_with_brush)
    canvas.bind("ButtonRelease-1", stop_draw)
def draw_with_brush(event):
    # find the x and y positions where the user clicked the right mouse button
    # The magic line: event.widget automatically adapts to main_canvas OR sub_canvas
    global last_x, last_y, current_stroke_ids
    canvas = event.widget
    tool = my_combo.get()
    spline_step = slider_spline_step.get()
    smooth_active = is_checked.get()
    outline_width = slider_border.get()


    rotation = 90

    x_position_of_click = event.x
    y_position_of_click = event.y

    w = canvas.winfo_width()
    h = canvas.winfo_height()

    brush_size = slider_size.get()
    size_poly = 100
    # define a circle with the mouse click at its center
    last_x = x_position_of_click - brush_size
    last_y = y_position_of_click - brush_size
    x2 = x_position_of_click + brush_size
    y2 = y_position_of_click + brush_size
    x3 = x_position_of_click / 2 - brush_size
    y3 = y_position_of_click / 2 + brush_size

    points = calculate_triangle_points(event.x, event.y, brush_size)


    colour = new_colour
    outline = outline_color
    # draw a circle while button_1 active and mouse is moving
    if tool == "Line":
        shape_id = canvas.create_line(last_x, last_y, x2, y2,
                                      fill=tkinter_colors[slider_color.get()],
                                      tags="paint",
                                      width=outline_width)
    elif tool == "Oval":
        if slider_border.get() <= 0:
            shape_id = canvas.create_oval(last_x, last_y, x2, y2,
                                          fill=tkinter_colors[slider_color.get()],
                                           tags="paint",
                                          width=0, outline="")
        else:
            shape_id = canvas.create_oval(last_x, last_y, x2, y2,
                                          fill=tkinter_colors[slider_color.get()],
                                          outline=tkinter_colors[slider_outline.get()], tags="paint",
                                          width=outline_width)
    elif tool == "Rectangle":
        if slider_border.get() <= 0:
            shape_id = canvas.create_rectangle(last_x, last_y, x2, y2,
                                               fill=tkinter_colors[slider_color.get()],
                                               outline="", tags="paint",
                                               width=0)
        else:
            shape_id = canvas.create_rectangle(last_x, last_y, x2, y2,
                                               fill=tkinter_colors[slider_color.get()],
                                               outline=tkinter_colors[slider_outline.get()], tags="paint",
                                               width=outline_width)
    elif tool == "Polygon":
        if slider_border.get() <= 0:
            shape_id = canvas.create_polygon(points,
                                             fill=tkinter_colors[slider_color.get()],
                                             outline="", tags="paint",
                                             splinesteps=spline_step, smooth=smooth_active,
                                             width=0)
        else:
            shape_id = canvas.create_polygon(points,
                                             fill=tkinter_colors[slider_color.get()],
                                             outline=tkinter_colors[slider_outline.get()], tags="paint",
                                             splinesteps=spline_step, smooth=smooth_active,
                                             width=outline_width)


    elif tool == "Arc":
        shape_id = canvas.create_arc(last_x, last_y, x2, y2,
                                     fill=tkinter_colors[slider_color.get()],
                                     outline=tkinter_colors[slider_outline.get()], tags="paint",
                                     width=outline_width)

    current_stroke_ids.append(shape_id)
    last_x, last_y = event.x, event.y


def calculate_triangle_points(cx, cy, size):
    """
    Calculates the 3 coordinate pairs (XY pairs) for an equilateral triangle
    centered precisely at a specific mouse point (cx, cy).
    """
    # Calculate height and offsets based on the target brush size
    height_triangle = size * 0.866  # Structural height of an equilateral triangle
    half_width = size / 2
    # Vertices relative to the center anchor point
    top_vertex = (cx, cy - (height_triangle / 2))
    bottom_right = (cx + half_width, cy + (height_triangle / 2))
    bottom_left = (cx - half_width, cy + (height_triangle / 2))

    # Flatten into a sequence format required by Tkinter: [x1, y1, x2, y2, x3, y3]
    return [
        top_vertex[0], top_vertex[1],
        bottom_right[0], bottom_right[1],
        bottom_left[0], bottom_left[1]
    ]


def update_preview(event=None):
    """Updates a temporary preview outline showing the brush size."""
    canvas.delete("brush_preview")
    tool = my_combo.get()
    spline_step = slider_spline_step.get()
    smooth_active = is_checked.get()

    # If the mouse isn't on the canvas (e.g. adjusted via slider), center the preview
    if event:
        cx, cy = event.x, event.y
    else:
        cx = canvas.winfo_width() / 2
        cy = canvas.winfo_height() / 2

    brush_size = slider_size.get()
    points_poly = calculate_triangle_points(cx, cy, brush_size)

    # Apply the NEW radius to the existing coordinates
    # 1. Handle coordinates safely
    if event is not None:
        # If triggered by a mouse movement/click
        x = canvas.winfo_pointerx() - canvas.winfo_rootx()
        y = canvas.winfo_pointery() - canvas.winfo_rooty()
    else:
        # If triggered manually at startup, park it off-screen or at (0,0)
        canvas_width = canvas.winfo_width()
        canvas_height = canvas.winfo_height()
        x = canvas_width / 2
        y = canvas_height / 2

    x1 = x - brush_size
    y1 = y - brush_size
    x2 = x + brush_size
    y2 = y + brush_size

    canvas.coords(cursor_follower, x1, y1, x2, y2)

    points = [x1, y1, x2, y2]


    # Draw a temporary outline preview tag
    if tool == "Polygon":
        canvas.create_polygon(
            points_poly,
            fill="",
            outline="red",
            dash=(3, 3),
            tags="brush_preview", smooth=smooth_active,splinesteps=spline_step
        )
        slider_size.configure(from_=50, to=400)

    elif tool == "Rectangle": canvas.create_rectangle(
        points,
        outline="red", tags=("brush_preview"), dash=(3, 3)
    )
    elif tool == "Oval":canvas.create_oval(
        points,
        outline="red", tags=("brush_preview"), dash=(3, 3)
    )

def program_2():
    canvas.bind("Button-1",start_draw)
    canvas.bind("<B1-Motion>", draw_with_exp)
    canvas.bind("ButtonRelease-1", stop_draw)
def program_3():
    canvas.bind("Button-1",start_draw)
    canvas.bind("<B1-Motion>", draw_with_brush)
    canvas.bind("ButtonRelease-1", stop_draw)
def program_4():
    canvas.bind("Button-1",start_draw)
    canvas.bind("<B1-Motion>", draw_with_exp)
    canvas.bind("ButtonRelease-1", stop_draw)
def program_5():
    canvas.bind("Button-1",start_draw)
    canvas.bind("<B1-Motion>", draw_with_brush)
    canvas.bind("ButtonRelease-1", stop_draw)
def draw_with_exp(event):
    active_canvas = event.widget

    global last_x, last_y, current_stroke_ids

    w = active_canvas.winfo_width()
    h = active_canvas.winfo_height()

    x_position_of_click = event.x
    y_position_of_click = event.y

    brush_size = slider_size.get()
    # define a circle with the mouse click at its center
    x1 = x_position_of_click - brush_size
    y1 = y_position_of_click - brush_size
    x2 = x1 + 100
    y2 = y1 + 100
    x3 = x1 - 100
    y3 = y1 - 100


    spline_step = slider_spline_step.get()
    smooth_active = is_checked.get()

    if my_combo.get() == "Line":
        item_id = active_canvas.create_line(w/2, h/2, x2, y1, fill=tkinter_colors[slider_color.get()])
    elif my_combo.get() == "Oval":
        item_id = active_canvas.create_oval(x1, y1, w/2, h/2, fill=tkinter_colors[slider_color.get()],
                                            outline=tkinter_colors[slider_outline.get()])
    elif my_combo.get() == "Rectangle":
        item_id = active_canvas.create_rectangle(w/4, h/4, x2, y1, fill=tkinter_colors[slider_color.get()],
                                                 outline=tkinter_colors[slider_outline.get()])
    elif my_combo.get() == "Polygon":
        item_id = active_canvas.create_polygon(x1, y2, x2, y1,x3,y3, fill=tkinter_colors[slider_color.get()],
                                               outline=tkinter_colors[slider_outline.get()],
                                               splinesteps=spline_step, smooth=smooth_active)
    elif my_combo.get() == "Arc":
        item_id = active_canvas.create_arc(x2, y2, w/2, h/2, fill=tkinter_colors[slider_color.get()],
                                           outline=tkinter_colors[slider_outline.get()])
    else:
        pass

    current_stroke_ids.append(item_id)
    last_x, last_y = event.x, event.y



def new_canvas():
        new_win = tk.Toplevel(window)
        new_win.title("New Canvas")
        new_win.config(padx=25,pady=25,relief=SUNKEN,menu=menu_bar)

        new_frame = tk.Frame(new_win, relief="ridge")
        new_frame.grid()
        sub_canvas = Canvas(new_frame, highlightthickness=10,highlightcolor="yellow",width=1000,height=1000)
        sub_canvas.grid()

        sub_canvas.bind("<B1-Motion>", draw_with_exp)


def update_coordinates(event):
    # event.x and event.y give us the mouse position relative to the canvas
    coords_text = f"X: {event.x}, Y: {event.y}"

    # Update the label widget with the new coordinate string
    label_coords.config(text=coords_text)


def to_tk_coords(x_custom, y_custom):
    """Converts center-origin coordinates to native Tkinter pixel coordinates."""
    # 1. Find the current center point of the canvas
    center_x = canvas.winfo_width() / 2
    center_y = canvas.winfo_height() / 2

    # 2. Apply the cartesian transformation math
    tk_x = center_x + x_custom
    tk_y = center_y - y_custom  # Subtracted to make positive Y go UP

    return tk_x, tk_y

def submit_size():
    width_canvas = input_box_width.get()
    height_canvas = input_box_height.get()
    canvas.config(width=width_canvas, height=height_canvas)

def canvas_size():
    def submit_size():
        width_canvas = input_box_width.get()
        height_canvas = input_box_height.get()
        canvas.config(width=width_canvas, height=height_canvas)
    dialog = tk.Toplevel(control_frame)
    dialog.title("Canvas Size")
    dialog.resizable(False, False)

    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()

    # Calculate screen midpoints
    x = (screen_width // 2) - (width // 2)
    y = (screen_height // 2) - (height // 2)

    dialog.geometry(f"{200}x{100}+{x}+{y}")

    dialog.transient(window)
    dialog.grab_set()

    tk.Label(dialog, text="Canvas Size").grid(row=0, column=0)

    label_width = tk.Label(dialog, text="width")
    label_width.grid(row=1, column=0)
    label_height = tk.Label(dialog, text="height")
    label_height.grid(row=2, column=0)
    input_box_width = tk.Entry(dialog, width=15, font=font_underline)
    input_box_width.grid(row=1, column=1)
    input_box_height = tk.Entry(dialog, width=15, font=font_underline)
    input_box_height.grid(row=2, column=1)

    submit_btn = tk.Button(dialog, text="Submit", command=submit_size, width=10)
    submit_btn.grid(row=3, column=0)
    close_btn = tk.Button(dialog, text="Close", command=dialog.destroy, width=10)
    close_btn.grid(row=3, column=1)
# 1. Global stacks to track canvas item IDs
undo_stack = []
redo_stack = []
# Variables to track line drawing coordinates
last_x, last_y = None, None
current_stroke_ids = []
cursor_follower = None

font_all = font=("Arial",10, "normal")
font_underline = font=("Arial",10, "underline")
#default values
value = 15
new_colour = "Red"
outline_color = "White"
border_width = 2
poly_amount = 6
rotation_amount = 0

# create window
window = Tk()
window.title("Project Pain")
window.config(padx=25,pady=25,relief=SUNKEN,)
window.resizable(False, False)
# menu
menu_bar = Menu(window)
file_bar = Menu(window)
colors_bar = Menu(window)
options_bar = Menu(window)
help_bar = Menu(window)

menu_bar.add_cascade(label="File", menu=file_bar)
menu_bar.add_cascade(label="Colors", menu=colors_bar)
menu_bar.add_cascade(label="Options", menu=options_bar)
menu_bar.add_cascade(label="Help", menu=help_bar)
menu_bar.add_command(label="Clear Canvas", command=clear_canvas)
menu_bar.add_command(label="Fill canvas", command=fill_canvas)
menu_bar.add_command(label="Exit", command=window.destroy)
file_bar.add_command(label="New", command=new_canvas)
file_bar.add_command(label="Undo", command=undo_action)
file_bar.add_command(label="Redo", command=redo_action)
file_bar.add_separator()
file_bar.add_command(label="Canvas size", command=canvas_size)

# create widgets
width_canvas = 1000
height_canvas = 1080

width = width_canvas
height = height_canvas

canvas = Canvas(window, width=width, height=height )
canvas.configure(highlightthickness=1,highlightcolor="grey",highlightbackground="black")

canvas.bind("<Button-1>", start_draw)
canvas.bind("<B1-Motion>", draw_with_brush)
canvas.bind("<ButtonRelease-1>", stop_draw)

control_frame = Frame(window, relief=SUNKEN, width=width, height=200)
control_frame.grid(columnspan=3, column=1, row=0)
#               first adjustment bar
#           LABELS
label2 = Label(control_frame, text="Color:", font=font_underline)
slider_color = Scale(control_frame, from_=0, to=len(tkinter_colors)-1, orient=HORIZONTAL,
           width=10, length=200,
           command=update_label_color, font=font_all)
slider_color.set(5)
label1 = Label(control_frame, text="Size:", font=font_underline)
slider_size = Scale(control_frame, from_=0, to=200, orient=HORIZONTAL,
           width=10, length=200,
           command=lambda val: [update_label_size(val),update_cursor(),update_preview()], font=font_all)
slider_size.set(15)
label3 = Label(control_frame, text="Outline:", font=font_underline)
slider_outline = Scale(control_frame, from_=0, to= len(tkinter_colors)-1, orient=HORIZONTAL,
           width=10, length=200,
           command=update_label_outline, font=font_all)
slider_outline.set(10)

label_size = Label(control_frame, width=6, padx=10, font=font_all)
label_color = Label(control_frame, width=6, padx=10, font=font_all)
label_outline = Label(control_frame, width=6, padx=10, font=font_all)

label2.grid(row=0, column=0, sticky="w")
label1.grid(row=1, column=0, sticky="w")
label3.grid(row=2, column=0, sticky="w")
label_color.grid(row=0, column=3, sticky="w", pady=15)
label_size.grid(row=1, column=3, sticky="w", pady=15)
label_outline.grid(row=2, column=3, sticky="w", pady=15)
slider_color.grid(row=0, column=1, sticky="n")
slider_size.grid(row=1, column=1, sticky="n")
slider_outline.grid(row=2, column=1, sticky="n")

button3 = Button(control_frame, text="Randomise",command=randomise_color, font=font_all)
button3.grid(row=0, column=2,sticky="w",padx=10)
button4 = Button(control_frame, text="Randomise",command=randomise_size, font=font_all)
button4.grid(row=1, column=2,sticky="w",padx=10)
button5 = Button(control_frame, text="Randomise",command=randomise_outline, font=font_all)
button5.grid(row=2, column=2,sticky="w",padx=10)

#              second adjustment bar
#                   LABELS
label_border = Label(control_frame, text="Border:",font=font_underline, padx=10)
label_poly = Label(control_frame, text="Spline step:",font=font_underline, padx=10)
label_rotation = Label(control_frame, text="Rotation:",font=font_underline, padx=10)
label_spline_step = Label(control_frame, text="Polygons",font=font_underline, padx=10, pady=15)

#           SLIDERS
slider_border = tk.Scale(control_frame, from_=0, to=15,
                         orient=HORIZONTAL, width=10, length=200,
                         command=update_label_border,font=font_all)
slider_border.set(5)

slider_poly = tk.Scale(control_frame, from_=0, to=200,
                       orient=HORIZONTAL, width=10, length=200,
                       command=update_label_poly,font=font_all)
slider_poly.set(0)

slider_rotation = tk.Scale(control_frame, from_=0, to= 360,
                           orient=HORIZONTAL, width=10, length=200,
                           command=update_label_rotation,font=font_all)
slider_rotation.set(10)
slider_spline_step = tk.Scale(control_frame, from_= 0, to=20,
                              orient=HORIZONTAL, width=10, length=200,
                              command=update_label_rotation,font=font_all)
slider_spline_step.set(5)
#           UPDATED LABEL
label_border_update = Label(control_frame,font=font_all,width=2, padx=10)
label_poly_update = Label(control_frame,font=font_all,width=2, padx=10)
label_rotation_update = Label(control_frame,font=font_all,width=2, padx=10)
label_spline_update = Label(control_frame,font=font_all,width=2, padx=10)
#       grids
label_border.grid(row=0, column=4, sticky="w", padx=5)
label_rotation.grid(row=2, column=4, sticky="w", padx=5)
label_spline_step.grid(row=3, column=4, sticky="w", padx=5)
label_poly.grid(row=1, column=4, sticky="w", padx=5)

label_border_update.grid(row=0, column=6, sticky="w")
label_rotation_update.grid(row=2, column=6, sticky="w")
label_spline_update.grid(row=3, column=6, sticky="w")
label_poly_update.grid(row=1, column=6, sticky="w")

slider_border.grid(row=0, column=5, sticky="n")
slider_rotation.grid(row=2, column=5, sticky="n")
slider_spline_step.grid(row=3, column=5, sticky="n")
slider_poly.grid(row=1, column=5, sticky="n")



#           RANDOMISE BUTTONS
button_randomise_border = Button(control_frame, text="Randomise",command=randomise_border,font=font_all)
button_randomise_border.grid(row=0, column=7,sticky="w",padx=20)
button_randomise_rotation = Button(control_frame, text="Randomise",command=randomise_rotation,font=font_all)
button_randomise_rotation.grid(row=2, column=7,sticky="w",padx=20)
button_randomise_poly = Button(control_frame, text="Randomise",command=randomise_poly,font=font_all)
button_randomise_poly.grid(row=1, column=7,sticky="w",padx=20)

button_randomise_all = Button(control_frame,text="Randomise all",font=font_all,command=lambda:[randomise_color(),randomise_size(),randomise_outline()])
button_randomise_all.grid(row=4, pady=10, column=3,sticky="w",padx=20)

#       clearr canvas
button2 = Button(control_frame, text="Clear",command=clear_canvas,font=font_all)
button2.grid(row=4, pady=10, column=1,sticky="e")

#       save canvas button
button3 = Button(window, text="Save",command=lambda: save_file(canvas),font=font_all, width=10)
button3.grid(row=0, column=0,sticky="w")
#       new canvas button
button_plugin1 = Button(control_frame, text="New canvas", command=new_canvas,font=font_all)
button_plugin1.grid(row=4, pady=10, column=2,sticky="e")
#           programs / tools
program_buttons = LabelFrame(window, text="Program Buttons",font=font_all)
program_buttons.grid(row=1, column=0, sticky="nw", padx=10, pady=10 )

button_program1 = Button(program_buttons, text="Program 1",command=program_1,font=font_all, width=10)
button_program1.grid(row=1, column=0, sticky="nw", padx=10, pady= 10)
button_program2 = Button(program_buttons, text="Program 2",command=program_2,font=font_all, width=10)
button_program2.grid(row=2, column=0, sticky="nw", padx=10, pady=10)
button_program3 = Button(program_buttons, text="Program 3",command=program_3,font=font_all, width=10)
button_program3.grid(row=3, column=0, sticky="nw", padx=10, pady=10)
button_program4 = Button(program_buttons, text="Program 4",command=program_4,font=font_all, width=10)
button_program4.grid(row=4, column=0, sticky="nw", padx=10, pady=10)
button_program5 = Button(program_buttons, text="Program 5",command=program_5,font=font_all, width=10)
button_program5.grid(row=5, column=0, sticky="nw", padx=10, pady=10)

# Pass the canvas widget instance directly into the undo/redo control commands
btn_undo = tk.Button(control_frame, text="↩️ Undo", width=10, command=lambda:undo_action(),font=font_all)
btn_undo.grid(row=4, column=7, padx=2, pady=10, sticky="s")

btn_redo = tk.Button(control_frame, text="↪️ Redo", width=10, command=lambda:redo_action(),font=font_all)
btn_redo.grid(row=4, column=8, padx=2, pady=10, sticky="s")
#create a combobox
tkinter_shapes = [
    "Line",         # Created with canvas.create_line()
    "Oval",         # Created with canvas.create_oval() (circles and ellipses)
    "Rectangle",    # Created with canvas.create_rectangle() (squares and rectangles)
    "Polygon",      # Created with canvas.create_polygon() (triangles, hexagons, custom shapes)
    "Arc",          # Created with canvas.create_arc() (pies, chords, arcs)        # Created with canvas.create_window() (to embed buttons, entries, etc.)
]

my_combo_label =Label(window, text="Shapes",font=font_underline)
my_combo_label.grid(row=0, column=0, sticky="nw")
my_combo = ttk.Combobox(window, values=tkinter_shapes, width=10,)
my_combo.set("Oval")
my_combo.grid(row=0, column=0,columnspan=2,rowspan=3, ipadx=5,padx=5, pady=25, sticky="nw")

#   spinbox
spinbox_poly = tk.Spinbox(
    control_frame,
    from_=0,
    to=150,
    increment=5,width=10,
    font=font_all,
)
spinbox_poly.grid(row=3,column=7,columnspan=2,pady=5,padx=10, sticky="w")
#       smoothbox checkbox for smooth polygon
is_checked = tk.BooleanVar()
smooth_box = tk.Checkbutton(control_frame, text="Smooth",compound="bottom",font=font_all, variable=is_checked)
smooth_box.grid(row=3,column=6, sticky="e", pady=5)

my_label = Label(control_frame, text="",font=font_all)
my_label.grid(row=4, column=4,ipadx=5)
#CURSOR FOLLOWER FOR BRUSHES


label_coords = Label(window,font=font_all, text="X: Y:")
label_coords.grid(column=0, row=2)
# place widgets into window container using the pack layout
canvas.grid(columnspan=2, column=1, row=1, rowspan = 15)

# bind widget events to functions
canvas.bind("<Button-1>",follow_cursor)
canvas.bind("<Motion>",follow_cursor)
canvas.bind("<Motion>", update_cursor,add="+")
my_combo.bind("<<ComboboxSelected>>", update_cursor)

canvas.bind("<Button-1>", start_draw)     # Left click starts a stroke
canvas.bind("<B1-Motion>", draw_with_brush)
# Dragging draws the line
canvas.bind("<ButtonRelease-1>", stop_draw) # Releasing mouse saves the stroke

# The real-time preview ring moving around
canvas.bind("<Motion>", update_cursor)
canvas.bind("<Motion>", update_coordinates,add="+")
canvas.bind("<Motion>",update_preview,add="+")


# open window
window.config(menu=menu_bar)
window.mainloop()
