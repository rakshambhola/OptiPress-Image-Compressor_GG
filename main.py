info="""===========================================================================
Image Compressor Tool
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
try:
    import time
    from PIL import Image,ImageOps
    from tqdm import tqdm
    import os
    import shutil
    import tkinter as tk
    from tkinter import filedialog, messagebox
except Exception as e:
    print("Error:",e)
    print("Please report this error to the developer: GitHub: https://github.com/rakshambhola")
    input("press enter to exit:")
    exit()
print("Import Finished")

# === CONFIGURATION ===
JPEG_QUALITY = 100         # 1–95 (higher = better quality, larger file)
PNG_COMPRESS_LEVEL = 9     # 0–9 (higher = smaller file, slower)
counter=[0,0,0] #compressed,copied,error
log1,log2,log3=[],[],[]

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

def compress_image(input_path, output_path):
    global JPEG_QUALITY, PNG_COMPRESS_LEVEL, counter, log1, log2, log3
    
    try:
        # Record original timestamps
        original_stat = os.stat(input_path)

        img = Image.open(input_path)
        img = ImageOps.exif_transpose(img)  # Fix orientation
        format_ext = os.path.splitext(input_path)[1].lower()
        icc_profile = img.info.get('icc_profile')
        exif_data = img.info.get('exif', b'')

        # Save compressed version in temporary path first
        temp_output = output_path + ".tmp"

        # --- Handle different formats ---
        if img.mode in ("RGBA", "LA") and format_ext in (".png", ".webp"):
            save_params = {
                "format": "PNG" if format_ext == ".png" else "WEBP",
                "optimize": True,
            }
            if format_ext == ".png":
                save_params["compress_level"] = PNG_COMPRESS_LEVEL
            if format_ext == ".webp":
                save_params["lossless"] = True

            # Preserve ICC profile if available
            if icc_profile:
                save_params["icc_profile"] = icc_profile

            img.save(temp_output, **save_params)

        elif format_ext in (".jpg", ".jpeg"):
            img = img.convert("RGB")
            save_params = {
                "format": "JPEG",
                "quality": JPEG_QUALITY,
                "optimize": True,
                "progressive": True
            }
            if icc_profile:
                save_params["icc_profile"] = icc_profile
            if exif_data:
                save_params["exif"] = exif_data        
            img.save(temp_output, **save_params)        
        else:
            img = img.convert("RGB")
            save_params = {
                "format": "JPEG",
                "quality": JPEG_QUALITY,
                "optimize": True
            }
            if icc_profile:
                save_params["icc_profile"] = icc_profile
            img.save(temp_output, **save_params)

        # --- Compare sizes ---
        original_size = os.path.getsize(input_path)
        compressed_size = os.path.getsize(temp_output)

        #if False:
        if compressed_size >= original_size:        
            # Compression ineffective → copy original instead
            shutil.copy2(input_path, output_path)
            os.remove(temp_output)
            #print(f"⚖️ Copied original: {output_path}")
            log2.append(f"⚖️ Copied original: {output_path}")
            counter[1]+=1
        else:
            # Keep compressed version
            shutil.move(temp_output, output_path)
            #print(f"✅ Compressed: {output_path}")
            log1.append(f"✅ Compressed: {output_path}")
            counter[0]+=1

        # --- Restore timestamps ---
        os.utime(output_path, (original_stat.st_atime, original_stat.st_mtime))

    except Exception as e:
        #print(f"❌ Error compressing {input_path}: {e}")
        log3.append(f"❌ Error compressing {input_path}: {e}")
        counter[2]+=1

def compress(input_path,output_path,ext):
    global counter
    # Compress JPG/JPEG/PNG
    if ext in ["jpg", "jpeg", "png", "webp", "bmp", "tiff"]:
        compress_image(input_path, output_path)
    # Copy any other formats
    else:
        shutil.copy2(input_path, output_path)
        #print(f"Copied {ext}: {output_path}")
        log2.append(f"Copied {ext}: {output_path}")
        counter[1]+=1        
try: import base64; qwerty = base64.b64decode("CgpFYXN0ZXIgRWdnOkdH").decode("utf-8")
except Exception: qwerty=''
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
    #for root, dirs, files in os.walk(input_folder):
    total = sum(len(dirs) for _, dirs, _ in os.walk(input_folder))
    for root, dirs, files in tqdm(os.walk(input_folder), total=total, desc="Compressing Directory", unit="dir"):
        relative_path = os.path.relpath(root, input_folder)
        target_dir = os.path.join(output_folder, relative_path)
        os.makedirs(target_dir, exist_ok=True)
        #for file in files:
        for file in tqdm(files, desc="Compressing images", unit="img"):
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
    #for src_path in image_paths:
    for src_path in tqdm(image_paths, desc="Compressing images", unit="img"):
        filename = os.path.basename(src_path)
        dest_path = os.path.join(dest_folder, filename)

        # Handle duplicate file names
        base, ext = os.path.splitext(filename)
        counter = 1
        while os.path.exists(dest_path):
            dest_path = os.path.join(dest_folder, f"{base} ({counter}){ext}")
            counter += 1
        ext = ext.lower().split('.')[-1]
        compress(src_path,dest_path,ext)

def input_choice():
    print("\nThis is a image compression tool")
    print("\t1: Choose specific images to compress")
    print("\t2: Select a folder of images to compress")
    print("\t3: Exit")
    a=input("Enter your choice (1,2,3):")
    if a.lower().strip() not in ['1','2','3','exit']:
        print("Invalid choice try again!!")
        return input_choice()
    else:
        if a.lower()=='exit' or a=='3':
            return 0
        else:
            return int(a)

def i_c_7():
    print("\nChoose your custom compression level (Higher = better quality, larger file):")
    a=input("Enter your choice (0-100):")
    if a.lower().strip()=='exit':
        return None
    try:
        if int(a) >=0 and int(a) <=100:
            return int(a)
        else:
            print("Invalid choice try again!!")
            return i_c_7()                   
    except Exception:
        print("Invalid choice try again!!")
        return i_c_7()        

def input_choice_2():
    print("\nChoose compression level:")
    print("\t1: Lossless 100\n\t2: Very Low 90\n\t3: Low 80\n\t4: Medium 70\n\t5: High 60\n\t6: Very High 50\n\t7: Custom (100-1)")
    a=input("Enter your choice (1-7):")
    if a.lower().strip() not in ['1','2','3','4','5','6','7','exit']:
        print("Invalid choice try again!!")
        return input_choice_2()
    else:
        if a.lower()=='exit':
            return None
        else:
            match int(a):
                case 1:
                    return (100)
                case 2:
                    return (90)
                case 3:
                    return (80)
                case 4:
                    return (70)
                case 5:
                    return (60)
                case 6:
                    return (50)
                case 7:
                    return i_c_7()

def save_logs():
    global log1, log2, log3
    log=[]
    log.append(info)
    log.extend(log1)
    log.append('\n\n\n\n\n\n')
    log.extend(log2)
    log.append('\n\n\n\n\n\n')
    log.extend(log3)
    root = tk.Tk()
    root.withdraw()
    confirm = messagebox.askyesno("Save Logs", "Do you want to save the logs?")
    if not confirm:
        return

    file_path = filedialog.asksaveasfilename(
        title="Save Logs As",
        defaultextension=".txt",
        initialfile="Log.txt",
        filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
    )

    if not file_path:
        print("Logs Save cancelled.")
        return

    try:
        with open(file_path, "w", encoding="utf-8") as f:
            for item in log:
                f.write(str(item).rstrip("\r\n") + "\n")
        print(f"Logs successfully saved to: {file_path}")
        messagebox.showinfo("Success", f"Logs successfully saved to:\n{file_path}")
    except Exception as e:
        print("Error saving log file:", e)
        messagebox.showerror("Error", f"Error saving log file:\n{e}")
    finally:
        root.destroy()             
    
def main():
    global JPEG_QUALITY
    a=input_choice()
    if a:
        if a==1:
            input_files= select_file("Select one or more images",("Image Files", "*.jpg *.jpeg *.png *.webp *.bmp *.tiff"))
            JPEG_QUALITY=input_choice_2()
            if type(None) == type(JPEG_QUALITY):
                return qwerty
            output_folder = select_folder("Select destination folder")
            print('\n\n')
            start_time = time.time()
            process_images_2(input_files, output_folder)
        else:
            input_folder = select_folder("Select source folder")
            JPEG_QUALITY=input_choice_2()
            if type(None) == type(JPEG_QUALITY):
                return qwerty
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
        text = f"Compressed={counter[0]},Copied={counter[1]} in {time_taken:.2f} seconds\nSkipped Corrupted files={counter[2]}"
        messagebox.showinfo("Message", text)
        root.destroy()
        save_logs()
    return qwerty

if __name__ == "__main__":
    try:
        main()
        #print(main())
        exit()
    except Exception as e:
        print("\n\nError:",e)
        print("Please report this error to the developer: GitHub: https://github.com/rakshambhola")
        input("press enter to exit:")
        exit()

