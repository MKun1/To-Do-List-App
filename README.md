# To-Do-List-App
# 📝 PyQt5 To-Do List App

A clean, modern, and functional desktop To-Do List application built with **PyQt5** and **Qt Designer**. Easily add, delete, and manage your daily tasks with status icons, urgency markers, and favorite tagging — all in a sleek frameless UI.

---

## 🚀 Features

- ✅ Add tasks with a click
- ❌ Delete selected tasks
- ⭐ Mark tasks as Favorite
- ⏰ Mark tasks as Completed or Urgent
- 🎨 Stylish, frameless, and draggable UI
- 🖱️ Right-click context menu for task actions
- 🧭 Status icons: pending, completed, urgent, favorite
- 🧰 Built using PyQt5 + Qt Designer
- 📦 Packaged as a single `.exe` with PyInstaller

---



## 🛠️ Installation
1. Clone the repository
```bash
git clone https://github.com/yourusername/pyqt5-todo-app.git
cd pyqt5-todo-app
```

2. Create a virtual environment (optional but recommended)
```bash

python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies
```bash

pip install -r requirements.txt
requirements.txt
```


## ▶️ Running the App
```bash

python main.py
```

## 📦 Packaging into an Executable
To package the app into a standalone .exe (Windows):

```bash

pyinstaller --noconsole --onefile --icon=app.ico --add-data "images/iconsandimages;images/iconsandimages" main.py
```
The --add-data flag ensures icons are bundled correctly.

--icon adds the custom app icon.

The resulting .exe will be found in the dist/ folder.


## 💡 Notes
Make sure to use forward slashes (/) in resource paths to ensure compatibility across platforms.

When using PyInstaller, paths must be managed using a helper like resource_path() for bundled files.

## 📃 License
This project is open-source under the MIT License.

## 🙋‍♂️ Acknowledgements
Built with ❤️ using PyQt5

UI designed with Qt Designer


