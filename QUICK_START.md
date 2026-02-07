# Quick Start Guide

## ⚠️ Building from Mac?

**PyInstaller can only build for the OS it's running on.**

You have two options:
1. **Use GitHub Actions** (push to GitHub, download built .exe from Actions tab)
2. **Build on Windows** (VM, physical PC, or the Ruby computer itself)

See `BUILD_INSTRUCTIONS.md` for details.

## Building the EXE on Windows

1. **Install PyInstaller**:
   ```bash
   pip install pyinstaller
   ```

2. **Build the executable**:
   ```bash
   pyinstaller build_exe.spec
   ```

3. **Find your EXE**:
   - Look in the `dist` folder
   - File will be named: `GKTW_Laser_Tool.exe`

## Building with GitHub Actions (from any OS)

1. **Push to GitHub**:
   ```bash
   git push
   ```

2. **Download EXE**:
   - Go to GitHub → Actions tab
   - Find latest build
   - Download from Artifacts section

## Running Without Building

For development/testing, you can run without building an EXE:

```bash
python run_server.py
```

Or use the batch file (Windows):
```bash
START_APP.bat
```

## What to Copy to the Laser Computer

After building, copy to the Ruby computer:
1. `GKTW_Laser_Tool.exe` (from the dist folder)
2. That's it! Everything is bundled.

## First-Time Setup on Laser Computer

1. Run `GKTW_Laser_Tool.exe`
2. Browser opens automatically
3. Click "Admin" in navigation
4. Configure:
   - Personal Access Token (from Trotec Ruby)
   - Ruby IP Address (usually `localhost` if on same computer)
   - Default Material Profile (select from dropdown)

## Daily Use

1. Double-click `GKTW_Laser_Tool.exe`
2. Create/customize laser files
3. Send to laser queue
4. Press START on laser machine

## Need More Details?

- **Building**: See `BUILD_INSTRUCTIONS.md`
- **User Guide**: See `USER_GUIDE.md`
- **Troubleshooting**: Check console window for errors
