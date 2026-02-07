# Building GKTW Laser Tool as EXE

This guide will help you create a standalone Windows executable (.exe) for the GKTW Laser Tool.

## Important: Cross-Platform Building

**PyInstaller can only build executables for the platform it's running on.** This means:
- Building on **Windows** → Creates `.exe` for Windows ✅
- Building on **Mac** → Creates Mac app, NOT `.exe` ❌
- Building on **Linux** → Creates Linux binary, NOT `.exe` ❌

### Your Options:

1. **Build on Windows machine/VM** (Section 1 below) - Most reliable
2. **Use GitHub Actions** (Section 2 below) - Automated cloud build
3. **Build on the Ruby computer** - If it has Python installed

## Section 1: Building on Windows

### Prerequisites

1. **Windows PC or VM**
2. **Python 3.8 or higher** installed
3. **All dependencies** installed (see requirements.txt)
4. **PyInstaller** - Install with: `pip install pyinstaller`

### Build Steps

#### 1. Install Build Dependencies

```bash
pip install pyinstaller
pip install -r requirements.txt
```

#### 2. Test the Application First

Before building, make sure the application runs correctly:

```bash
python run_server.py
```

This should:
- Start the Django server
- Open your browser to http://127.0.0.1:8000
- Work without errors

Press CTRL+C to stop when done testing.

#### 3. Build the Executable

Run PyInstaller with the provided spec file:

```bash
pyinstaller build_exe.spec
```

This will:
- Create a `dist` folder
- Generate `GKTW_Laser_Tool.exe` inside the dist folder
- Bundle all dependencies, templates, and static files

The build process may take a few minutes.

#### 4. Test the Executable

Navigate to the dist folder and run:

```bash
cd dist
GKTW_Laser_Tool.exe
```

The application should start and open in your browser.

---

## Section 2: Building with GitHub Actions (Cloud)

If you don't have access to a Windows machine, use GitHub Actions to build automatically in the cloud.

### Setup (One-time)

1. **Push your code to GitHub**:
   ```bash
   git add .
   git commit -m "Add build workflow"
   git push
   ```

2. **The workflow will run automatically** on every push to main branch

### Download the Built EXE

1. Go to your GitHub repository
2. Click **"Actions"** tab
3. Click on the latest workflow run
4. Scroll down to **"Artifacts"**
5. Download **"GKTW-Laser-Tool-Windows"**
6. Extract the zip file to get `GKTW_Laser_Tool.exe`

### Manual Build Trigger

You can also trigger a build manually:
1. Go to **Actions** tab
2. Click **"Build Windows EXE"** workflow
3. Click **"Run workflow"** button
4. Wait for completion (~5-10 minutes)
5. Download from Artifacts section

### Benefits of GitHub Actions:
- ✅ No Windows machine needed
- ✅ Consistent build environment
- ✅ Automatic builds on every push
- ✅ Free for public repositories
- ✅ Build history and artifacts retained

---

## Distribution

### What to Package

After building, you'll have a `dist` folder containing:
- `GKTW_Laser_Tool.exe` - The main executable (large file, ~100-200MB)

### Important Notes

1. **Database**: The application will create a `db.sqlite3` file in the same directory as the .exe when first run
2. **File Uploads**: Uploaded template files will be stored in a `media` folder
3. **Settings**: Session data is stored in the database

### Creating a Distribution Package

To distribute to the Ruby computer:

1. Copy the entire `dist` folder (or just the .exe if using --onefile)
2. Include a README with:
   - How to run: "Double-click GKTW_Laser_Tool.exe"
   - How to access: "Browser will open automatically to http://127.0.0.1:8000"
   - How to stop: "Press CTRL+C in the console window or close the window"

## Troubleshooting

### "No module named X" errors

If you get import errors, add the missing module to the `hiddenimports` list in `build_exe.spec`:

```python
hiddenimports=[
    'django',
    'requests',
    'missing_module_name',  # Add here
]
```

Then rebuild: `pyinstaller build_exe.spec`

### Templates or static files not found

Make sure the files are being collected in the spec file. Check the `template_files` and `static_files` collection logic.

### Antivirus Warnings

PyInstaller executables sometimes trigger antivirus warnings. This is normal. You may need to:
- Add an exception in your antivirus software
- Sign the executable with a code signing certificate (for production use)

## Advanced Options

### Smaller Executable

The current spec uses `--onefile` mode (everything in one .exe). If you prefer smaller size but multiple files:

1. Change the spec file to remove the --onefile bundling
2. This will create a folder with the .exe and supporting files

### Custom Icon

To add a custom icon:

1. Get a `.ico` file (Windows icon format)
2. In `build_exe.spec`, change:
   ```python
   icon=None,  # Replace with: icon='path/to/icon.ico'
   ```

### Hide Console Window

If you don't want the console window to show:

In `build_exe.spec`, change:
```python
console=True,  # Change to: console=False
```

Note: This makes debugging harder, so test thoroughly first.

## Production Recommendations

For production use on the Ruby computer:

1. **Test thoroughly** on a similar Windows machine first
2. **Include admin guide** for configuring PAT, IP, and import profile
3. **Create desktop shortcut** for easy access
4. **Set up auto-start** if the laser computer boots daily
5. **Keep source code** for future updates
6. **Version the EXE** in the filename (e.g., GKTW_Laser_Tool_v1.0.exe)
