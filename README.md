<div align="center">

<img src="./icon.png" alt="OptiPress Logo" width="120" height="120" />

# OptiPress

### *File Compressor*

[![Release](https://img.shields.io/badge/Release-0.7.1-blue?style=for-the-badge&logo=github)](https://github.com/rakshambhola/OptiPress-Image-Compressor_GG/releases)
[![Python](https://img.shields.io/badge/Python-3.12.7-green?style=for-the-badge&logo=python)](https://www.python.org/)

<p align="center">
  <a href="#assets">Assets</a> •
  <a href="#overview">Overview</a> •
  <a href="#features">Features</a> •
  <a href="#requirements">Requirements</a> •
  <a href="#roadmap">Roadmap</a> •
</p>

</div>

---

# OptiPress-Image Compressor
### 🔹 Simple • Fast • Lossless
**OptiPress** - A lightweight yet powerful image compression tool that intelligently reduces image size without sacrificing quality. It preserves metadata, handles transparency, and maintains your original folder structure automatically.

---
## Assets

* Latest Release: [OptiPress-Image-Compressor-v.0.7.1_GG.zip](https://github.com/rakshambhola/OptiPress-Image-Compressor_GG/releases/download/v.0.7.1_GG/OptiPress-Image-Compressor-v.0.7.1_GG.zip)
* Release: [OptiPress-Image-Compressor-v.0.5.1_GG.zip](https://github.com/rakshambhola/OptiPress-Image-Compressor-v.0.5.1_GG/releases/download/v.0.5.1_GG/OptiPress-Image-Compressor-v.0.5.1_GG.zip)

---

## Overview
This tool allows you to:

* Compress individual image files or entire folders.
* Maintain original **quality, timestamps, and metadata**.
* Automatically handle **duplicate file/folder names**.
* Preserve **transparent PNGs** safely.
* Preserves your folder and subfolder structure across all file formats.
* Supports ".jpg", ".jpeg", ".png", ".webp", ".bmp", ".tiff" formats.

---

## Features

| Feature                          | Description                                                                |
| -------------------------------- | -------------------------------------------------------------------------- |
| 🗂️ Folder & File Selection      | Choose one or more images, or a whole folder of images at once.            |
| 🔄 Folder Structure Preservation | Keeps your folder and sub-folder hierarchy exactly the same in output.     |
| ⚡ Lossless Compression           | Reduces file size while preserving image quality and EXIF/ICC metadata.    |
| 🕓 Timestamp Preservation        | Maintains original creation and modification dates.                        |
| 🧊 Transparency Handling         | Detects transparent PNGs and safely copies them without quality loss.      |
| 🧠 Auto Duplicate Handling       | Automatically renames files or folders if same names exist in destination. |
| 📊 Final Report                  | Shows total compressed/copied images and total time taken.                 |

---

## 🧩 Requirements

**Python Version:** 3.7 or higher
**Required Libraries:**

* `Pillow`
* `tqdm`
* `tkinter` *(included with Python)*
* `shutil` *(standard library)*
* `os` *(standard library)*

Install required libraries:
```
pip install Pillow tqdm
```
**or**
```bash
pip install -r requirements.txt
```

---

## 🧰 Built and tested with these versions:

```
Python - 3.12.7
pillow - 11.3.0
tqdm - 4.66.4
```

---

## Roadmap

### Phase 1: Core Features ✅
- [x] Folder & File Selection
- [x] Folder Structure Preservation
- [x] Lossless Compression
- [x] Timestamp Preservation
- [x] Transparency Handling
- [x] Auto Duplicate Handling
- [x] Report system as a pop-up

### Phase 2: Enhancements 🚧
- [x] Progress Bar
- [x] Additional Image formats
- [x] Save Logs
- [ ] Support for Video Files
- [ ] Compress to Defined Size
- [ ] CLI to basic GUI Application
- [ ] Support for more different file types
- [ ] Push notifications

### Phase 3: Scale & Polish 📋
- [ ] Basic to Modern GUI
- [ ] Analytics dashboard
- [ ] Web App
- [ ] Mobile App
- [ ] AI-powered image enhancement

---

## 💬 Notes

* The tool never deletes or overwrites your original files.

---

## 🧑‍💻 Author

**👤 Raksham Bhola**
🔗 GitHub: [rakshambhola](https://github.com/rakshambhola)

---

## 📜 License

This project is open-source and available under the **MIT License**.

---

<div align="center">

**Star ⭐ this repo if you find it useful!**

[⬆ Back to Top](#OptiPress)

</div>
