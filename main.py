info="""===========================================================================
OptiPress-Image Compressor Tool
---------------------
A simple and efficient Python script to compress JPG, JPEG, and PNG images
without losing quality. It preserves EXIF/ICC data, handles transparency,
and maintains folder structure.

Author: Raksham Bhola
GitHub: https://github.com/rakshambhola
============================================================================\n
"""
print(info)
print("Importing Librearies")

import time
from PIL import Image,ImageOps
import os
import shutil
import tkinter as tk
from tkinter import filedialog, messagebox 

print("Import Finished")
counter=[0,0]

def select_folder(titles):
    print(titles)
    root = tk.Tk()
    root.withdraw()
    folder_selected = filedialog.askdirectory(title=titles)
    root.destroy()
    if os.path.exists(folder_selected) and os.path.isdir(folder_selected):
        print("location=",folder_selected)
        return folder_selected
    else:
        print("Please select a folder It's cumpolsory.")
        return(select_folder(titles))

def select_file(titles,extention):
    print(titles)
    root = tk.Tk()
    root.withdraw()
    file_path = filedialog.askopenfilenames(
        title=titles,
        filetypes=[extention]
    )    
    root.destroy()
    if os.path.exists(file_path[0]):
        #print("location=",file_path)
        return file_path
    else:
        print("Please select a file It's cumpolsory.")
        return(select_file(titles,extention))

def has_transparency(img):
    """Check if an image has transparency (works for PNG)."""
    if img.mode in ("RGBA", "LA") or (img.mode == "P" and 'transparency' in img.info):
        return True
    return False

def compress_image(input_path, output_path, format):
    """Compress JPG, JPEG, and PNG without quality loss."""
    global counter
    try:
        # Get original timestamps
        original_stat = os.stat(input_path)
        img = Image.open(input_path)
        img = ImageOps.exif_transpose(img)
        icc_profile = img.info.get('icc_profile')
        exif_data = img.info.get('exif', b'')
        save_params = {
            "format": "JPEG" if format == "JPG" else format,
            "optimize": True
        }
        if icc_profile:
            save_params["icc_profile"] = icc_profile
        if exif_data:
            save_params["exif"] = exif_data
        # If PNG has transparency, just copy instead of compressing
        if format == "PNG" and has_transparency(img):
            shutil.copy2(input_path, output_path)
            print(f"Copied (Transparent PNG): {output_path}")
            counter[1]+=1
            return

        # Convert non-RGB modes to RGB for compression
        if img.mode in ("RGBA", "P"):
            img = img.convert("RGB")

        #img.save(output_path, format="JPEG" if format == "JPG" else format, optimize=True)
        img.save(output_path, **save_params)
        print(f"Compressed: {output_path}")
        counter[0]+=1

        # Restore original timestamps
        os.utime(output_path, (original_stat.st_atime, original_stat.st_mtime))

    except Exception as e:
        print(f"\n\nError compressing {input_path}: {e}\n\n")

def compress(input_path,output_path,ext):
    global counter
    # Compress JPG/JPEG/PNG
    if ext in ["jpg", "jpeg", "png"]:
        compress_image(input_path, output_path, format=ext.upper())
    # Copy any other formats
    else:
        shutil.copy2(input_path, output_path)
        print(f"Copied {ext}: {output_path}")
        counter[1]+=1
import base64;qwerty=base64.b64decode("CgpFYXN0ZXIgRWdnOkdH").decode("utf-8")
def process_images_1(input_folder, output_folder):    
    """Recursively process images while maintaining folder structure."""
    # Handle duplicate folder name
    folder_name = os.path.basename(input_folder.rstrip("/\\"))
    destination_folder=output_folder
    output_folder = os.path.join(destination_folder, folder_name)
    ctr_1 = 1
    while os.path.exists(output_folder):
        output_folder = os.path.join(destination_folder, f"{folder_name} ({ctr_1})")
        ctr_1 += 1
    for root, dirs, files in os.walk(input_folder):
        relative_path = os.path.relpath(root, input_folder)
        target_dir = os.path.join(output_folder, relative_path)
        os.makedirs(target_dir, exist_ok=True)
        for file in files:
            input_path = os.path.join(root, file)
            output_path = os.path.join(target_dir, file)
            # Handle duplicate file names
            base_a, ext_a = os.path.splitext(file)
            ctr=1
            while os.path.exists(output_path):
                output_path = os.path.join(target_dir, f"{base_a} ({ctr}){ext_a}")
                ctr += 1
            ext = file.lower().split('.')[-1]
            compress(input_path,output_path,ext)

def process_images_2(image_paths, dest_folder):
    for src_path in image_paths:
        filename = os.path.basename(src_path)
        dest_path = os.path.join(dest_folder, filename)

        # Handle duplicate file names
        base, ext = os.path.splitext(filename)
        counter = 1
        while os.path.exists(dest_path):
            dest_path = os.path.join(dest_folder, f"{base}_{counter}{ext}")
            counter += 1
        ext = ext.lower().split('.')[-1]
        compress(src_path,dest_path,ext)

def input_choice():
    print("\nThis is a image compression tool")
    print("\t1: Choose specific images to compress")
    print("\t2: Select a folder of images to compress")
    print("\t3: Exit")
    a=input("Enter your choice (1,2,3):")
    if a.lower() not in ['1','2','3','exit']:
        print("Invalid choice try again!!")
        return input_choice()
    else:
        if a.lower()=='exit' or a=='3':
            return 0
        else:
            return int(a)    
    
def main():
    a=input_choice()
    if a:
        if a==1:
            input_files= select_file("Select one or more images",("Image Files", "*.jpg *.jpeg *.png"))
            output_folder = select_folder("Select destination folder")
            print('\n\n')
            start_time = time.time()
            process_images_2(input_files, output_folder)
        else:
            input_folder = select_folder("Select source folder")  
            output_folder = select_folder("Select destination folder")
            print('\n\n')
            start_time = time.time()
            process_images_1(input_folder, output_folder)
        root = tk.Tk()
        root.withdraw()
        print('\n\nProgram Finished')
        end_time = time.time()
        time_taken = end_time - start_time
        print(f"Total time taken: {time_taken:.2f} seconds")
        text = f"Compressed={counter[0]},Copied={counter[1]} in {time_taken:.2f} seconds"
        messagebox.showinfo("Message", text)        
    return qwerty

if __name__ == "__main__":
    print(main())
    #exit()

