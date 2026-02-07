# GKTW Laser Tool - User Guide

## For Volunteers

### Starting the Application

1. **Double-click** `GKTW_Laser_Tool.exe`
2. A black window (console) will appear - **DO NOT CLOSE THIS WINDOW**
3. Your web browser will automatically open to the application
4. If the browser doesn't open, manually go to: http://127.0.0.1:8000

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

Template files are Django templates that support variable substitution:
- Use `{{ data.0 }}` for the first line
- Use `{{ data.1 }}` for the second line
- And so on...

To add new templates:
1. Access the Django admin interface: http://127.0.0.1:8000/admin/
2. Login with superuser credentials
3. Add new TemplateFile entries

### Creating a Superuser

To access the Django admin:

```bash
python manage.py createsuperuser
```

Follow the prompts to create an admin account.

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
