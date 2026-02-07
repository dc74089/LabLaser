# Using GitHub Actions to Build Windows EXE

Since you're developing on Mac but need a Windows .exe, GitHub Actions provides the easiest solution - it builds your .exe automatically in the cloud on a Windows machine.

## Initial Setup

### 1. Push Your Code to GitHub

If you haven't already:

```bash
# Initialize git (if not already done)
git init

# Add all files
git add .

# Commit
git commit -m "Initial commit with build workflow"

# Add your GitHub repository as remote
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO.git

# Push to GitHub
git push -u origin main
```

### 2. Verify Workflow File Exists

Make sure this file exists in your repository:
```
.github/workflows/build-windows.yml
```

This was created automatically when I set up the build system.

## How It Works

Every time you push code to the `main` branch:
1. GitHub Actions spins up a Windows VM
2. Installs Python and dependencies
3. Runs PyInstaller to build the .exe
4. Uploads the .exe as a downloadable artifact
5. Keeps it for 30 days

## Downloading Your Built EXE

### After Automatic Build (on push):

1. Go to your repository on GitHub
2. Click the **"Actions"** tab at the top
3. You'll see a list of workflow runs
4. Click on the most recent one
5. Scroll down to the **"Artifacts"** section
6. Click **"GKTW-Laser-Tool-Windows"** to download
7. Extract the zip file to get `GKTW_Laser_Tool.exe`

### Manual Build Trigger:

You can also build on-demand without pushing code:

1. Go to **Actions** tab
2. Click **"Build Windows EXE"** in the left sidebar
3. Click **"Run workflow"** button (top right)
4. Select branch (usually `main`)
5. Click green **"Run workflow"** button
6. Wait 5-10 minutes for completion
7. Download from Artifacts as described above

## Development Workflow

### Your typical workflow:

```bash
# 1. Make changes on your Mac
# Edit files in your IDE...

# 2. Test locally (runs on Mac, but tests the logic)
python run_server.py

# 3. Commit and push when ready
git add .
git commit -m "Added new feature"
git push

# 4. Wait a few minutes for GitHub Actions to build

# 5. Download the Windows .exe from GitHub Actions

# 6. Copy .exe to Ruby computer and test
```

## Checking Build Status

### While building:
- Go to Actions tab
- You'll see a yellow dot 🟡 (building) or orange circle (in progress)
- Click to see real-time logs

### After completion:
- Green checkmark ✅ = Success! Download the artifact
- Red X ❌ = Failed. Click to see error logs

## Troubleshooting

### Build Fails?

1. Click on the failed workflow run
2. Click on the "build" job
3. Expand the failed step to see error details
4. Common issues:
   - Missing dependency in `requirements.txt`
   - Import errors (add to `hiddenimports` in `build_exe.spec`)
   - Template/static file paths wrong

### Artifact Not Available?

- Artifacts are only kept for 30 days
- If older, just run a new build

### Build Takes Too Long?

- GitHub Actions free tier has usage limits
- Builds typically take 5-10 minutes
- Limit: 2000 minutes/month (plenty for this project)

## Cost

- **Free** for public repositories
- **Free tier** for private repositories (2000 minutes/month)
- This project uses ~5-10 minutes per build
- You can do ~200-400 builds per month on free tier

## Alternative: Build Locally on Ruby Computer

If you have Python installed on the Ruby computer, you can also build there:

1. Copy your source code to the Ruby computer
2. Install Python if not installed
3. Run:
   ```bash
   pip install -r requirements.txt
   pyinstaller build_exe.spec
   ```
4. The .exe will be in the `dist` folder

This avoids GitHub Actions entirely but requires Python on the target machine.

## Best Practices

1. **Tag releases**: Use git tags for versions
   ```bash
   git tag v1.0.0
   git push --tags
   ```

2. **Keep artifacts**: Download important builds and store them

3. **Test before deploying**: Always test the .exe on Windows before giving to volunteers

4. **Document changes**: Use clear commit messages so you know what each build contains
