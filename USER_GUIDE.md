# GKTW Laser Tool - User Guide

## For Volunteers

### Starting the Application

1. **Double-click** `GKTW_Laser_Tool.exe`
2. A black window (console) will appear - **DO NOT CLOSE THIS WINDOW**
3. On first run, it will:
   - Set up the database
   - Create an admin user (username: `admin`, password: `Volunteer710`)
   - Load any SVG templates from the `svgs` folder
4. Your web browser will automatically open to the application
5. If the browser doesn't open, manually go to: http://127.0.0.1:8000

### Creating Laser Files

1. Click **"New File"** or select a template from the home page
2. Fill in the customization fields (guest name, text lines, etc.)
3. Preview the design in real-time as you type
4. Click **"Finished Customizing"** when done

### Sending to Laser

1. Click **"Customized Files"** in the navigation bar
2. Find the file you want to cut
3. Click **"Send to Laser"**
4. The file will upload to the Trotec Ruby software
5. Go to the laser machine and press **START**

### Troubleshooting

**Q: Browser doesn't open automatically?**
- Manually open a browser and go to: http://127.0.0.1:8000

**Q: Can't send files to laser?**
- Check that the Ruby software is running on the laser computer
- Ask an admin to verify the configuration in Admin → Settings

**Q: Application won't start?**
- Make sure no other copy is already running
- Try restarting your computer
- Contact an admin

### Stopping the Application

When you're done:
1. Close the browser tabs
2. Go to the black console window
3. Press **CTRL+C** or close the window

---

## For Administrators

### Initial Setup

1. **Run the application** for the first time
2. Click **"Admin"** in the navigation bar
3. Configure the following:

#### Personal Access Token (PAT)
- Open Trotec Ruby software
- Generate a Personal Access Token
- Copy and paste it into the PAT field

#### Ruby IP Address
- Find the IP address of the computer running Trotec Ruby
- Usually something like: `192.168.1.100` or `localhost` if on the same computer
- Enter it in the IP Address field

#### Default Material Profile
- After entering PAT and IP, refresh the page
- A dropdown will appear with available material profiles
- Select the default material (e.g., "Acrylic 3mm", "Birch Plywood")
- All files will use this material setting when sent to the laser

### Managing Templates

#### Default Admin Login
- **Username**: `admin`
- **Password**: `Volunteer710`
- **URL**: http://127.0.0.1:8000/admin/

#### Automatic Template Loading

Place SVG files in the `svgs` folder next to the .exe:
```
GKTW_Laser_Tool.exe
svgs/
  ├── badge.svg
  ├── keychain.svg
  └── name_tag.svg
```

Templates use Django template syntax:
- `{{ data.0 }}` - First customization field
- `{{ data.1 }}` - Second customization field
- `{{ data.2 }}` - Third customization field
- And so on...

On startup, the application will:
1. Scan the `svgs` folder
2. Detect how many fields each template needs (by counting `{{ data.X }}` tags)
3. Automatically create TemplateFile entries
4. Skip templates that already exist

#### Manual Template Management

You can also add templates manually:
1. Go to: http://127.0.0.1:8000/admin/
2. Login with admin credentials
3. Click "Template files"
4. Add new entries manually

### Data Storage

- **Database**: `db.sqlite3` (in the same folder as the .exe)
- **Uploaded Files**: `media` folder
- **Session Data**: Stored in database, cleared when server restarts

### Backing Up

To backup your data:
1. Stop the application
2. Copy `db.sqlite3` and the `media` folder
3. Store safely

To restore:
1. Stop the application
2. Replace `db.sqlite3` and `media` folder with backup copies
3. Restart the application

### Updates

When installing a new version:
1. Stop the old version
2. Replace the .exe file
3. Keep the `db.sqlite3` and `media` folder from the old version
4. Start the new version

### Network Access (Optional)

To allow access from other computers on the network:

1. Edit the startup script to bind to `0.0.0.0` instead of `127.0.0.1`
2. Add firewall rule to allow port 8000
3. Users can access via: `http://[YOUR_COMPUTER_IP]:8000`

**Note**: Only do this on a trusted network.

### Support

For technical issues:
- Check the console window for error messages
- Check `BUILD_INSTRUCTIONS.md` for troubleshooting
- Contact the developer with error details
