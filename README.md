# 🖼️ GIF Generator Web App

This is a Flask-based web app that allows users to upload multiple images, generate a custom-named animated GIF, preview it, and download it instantly.

## 📁 Demo Folders

The project comes with three demo folders in `web_app/static/uploads/`:
- `team/` – Team member images
- `chicklet/` – Chicklet meme frames
- `nyan/` – Nyan cat animation frames

Use these to test GIF generation easily.

---

## 🚀 Features

- Upload multiple images (JPG/PNG)
- Automatic resizing to match the first frame
- Custom name input for generated GIF
- Preview generated GIF before download
- Downloadable final GIF
- Clean and responsive UI

---

## 🛠️ Tech Stack

- **Backend**: Python, Flask
- **Frontend**: HTML, TailwindCSS (optional), JavaScript
- **Image Processing**: Pillow, imageio

---

## 📦 Project Structure

```
GIF_Creator/
├── create_gif.py
├── chickelt/
├── nyan/
├── team/
├── web_gif_generator/
│   ├── static/
│   │   ├── gifs/
│   │   ├── uploads/
│   │   │   ├── team/
│   │   │   ├── chicklet/
│   │   │   └── nyan/
|   ├── templates/
|   |    ├── index.html
|   ├── app.py
```

---

## 🧑‍💻 Local Setup

### 1. Clone the Repo

```bash
git clone https://github.com/your-username/Gif_Creator.git
cd Gif_Cretor
cd web_gif_generator
```

### 2. Create a Virtual Environment

```bash
python -m venv venv
# Activate (Windows)
venv\Scripts\activate
# Activate (macOS/Linux)
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install flask pillow imageio
```

### 4. Run the App

```bash
python app.py
```

Visit [http://localhost:5000](http://localhost:5000) in your browser.

---
Right now choose images is not working
But Choose Folder with images is working so use that

also for instead of web gif genartor

run 

python create_gif.py

to create gif locally

---

## 📥 Usage Guide

1. Upload 2 or more images
2. Enter a name for the GIF (e.g., `funny_dance`)
3. Click **Generate GIF**
4. Preview and download your final animated GIF

---

## ✅ To-Do / Enhancements

- Drag & drop image support
- GIF speed customization
- Ability to reorder frames
- Support for folders/ZIP uploads

---

> Built with 💚 by Rajvardhan Deshmukh using Flask and Open Source tools.
