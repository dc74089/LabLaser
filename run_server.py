#!/usr/bin/env python
"""
Standalone launcher for GKTW Laser Tool
Runs the Django development server and opens the browser
"""
import os
import sys
import webbrowser
import threading
import time
from pathlib import Path

def setup_django():
    """Setup Django environment"""
    # Add the project directory to the Python path
    project_dir = Path(__file__).parent
    sys.path.insert(0, str(project_dir))

    # Set Django settings module
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'LabLaser.settings')

    # Setup Django
    import django
    django.setup()


def run_migrations():
    """Run database migrations on startup"""
    from django.core.management import call_command
    print("Setting up database...")
    try:
        call_command('migrate', '--noinput', verbosity=1)
        print("✓ Database migrations completed successfully")
    except Exception as e:
        print(f"✗ Migration failed: {e}")
        raise


def is_frozen():
    """Check if running from PyInstaller executable"""
    return getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS')


def create_superuser():
    """Create default superuser if it doesn't exist"""
    from django.contrib.auth import get_user_model
    User = get_user_model()

    username = 'admin'
    password = 'Volunteer710'

    if not User.objects.filter(username=username).exists():
        print(f"Creating superuser '{username}'...")
        User.objects.create_superuser(
            username=username,
            email='admin@gktw.local',
            password=password
        )
        print(f"✓ Superuser created successfully!")
    else:
        print(f"Superuser '{username}' already exists")


def load_svg_templates():
    """Scan svgs directory and create TemplateFile objects"""
    import re
    from pathlib import Path
    from django.core.files import File
    from app.models import TemplateFile

    # Find svgs directory
    if is_frozen():
        # When running from PyInstaller, look in the extracted bundle directory
        # sys._MEIPASS is the temp folder where PyInstaller extracts files
        svgs_dir = Path(sys._MEIPASS) / 'svgs'
    else:
        # When running from source
        svgs_dir = Path(__file__).parent / 'svgs'

    if not svgs_dir.exists():
        print(f"No 'svgs' directory found at {svgs_dir}")
        print("Create an 'svgs' directory and add SVG templates to auto-load them.")
        return

    print(f"Scanning for SVG templates in {svgs_dir}...")

    svg_files = list(svgs_dir.glob('*.svg'))
    if not svg_files:
        print("No SVG files found in svgs directory")
        return

    for svg_path in svg_files:
        # Check if this template already exists by name
        template_name = svg_path.stem

        if TemplateFile.objects.filter(name=template_name).exists():
            print(f"  - {template_name}: already exists, skipping")
            continue

        # Read the SVG content
        with open(svg_path, 'r', encoding='utf-8') as f:
            svg_content = f.read()

        # Count template slots by finding {{ data.X }} patterns
        # Matches {{ data.0 }}, {{ data.1 }}, etc.
        slot_pattern = r'\{\{\s*data\.\d+\s*\}\}'
        matches = re.findall(slot_pattern, svg_content)

        # Find the highest slot number
        num_slots = 0
        if matches:
            slot_numbers = []
            for match in matches:
                # Extract the number from {{ data.X }}
                num = re.search(r'data\.(\d+)', match)
                if num:
                    slot_numbers.append(int(num.group(1)))
            num_slots = max(slot_numbers) + 1 if slot_numbers else 0

        if num_slots == 0:
            print(f"  - {template_name}: no template slots found ({{ data.0 }}), skipping")
            continue

        # Create the TemplateFile
        template = TemplateFile(
            name=template_name,
            num_slots=num_slots
        )

        # Save the file
        with open(svg_path, 'rb') as f:
            template.file.save(svg_path.name, File(f), save=True)

        print(f"  ✓ {template_name}: loaded with {num_slots} slots")

    total_templates = TemplateFile.objects.count()
    print(f"Template loading complete. Total templates: {total_templates}")


def open_browser():
    """Open browser after a short delay"""
    time.sleep(2)
    webbrowser.open('http://127.0.0.1:8000')


def main():
    """Main entry point"""
    print("=" * 50)
    print("GKTW Laser Tool - Starting...")
    print("=" * 50)

    # Setup Django
    setup_django()

    # Run migrations
    run_migrations()

    # Only run these initialization tasks when running from PyInstaller
    if is_frozen():
        print("\n" + "=" * 50)
        print("Running first-time setup...")
        print("=" * 50 + "\n")

        # Create superuser
        create_superuser()

        # Load SVG templates
        load_svg_templates()

        print("\n" + "=" * 50)
        print("Setup complete!")
        print("=" * 50 + "\n")

    # Start browser in background thread
    browser_thread = threading.Thread(target=open_browser, daemon=True)
    browser_thread.start()

    # Import and run server
    from django.core.management import execute_from_command_line

    print("\nServer starting at http://127.0.0.1:8000")
    print("Press CTRL+C to stop the server\n")

    if is_frozen():
        print("Default login credentials:")
        print("  Username: admin")
        print("  Password: Volunteer710")
        print()

    try:
        execute_from_command_line(['manage.py', 'runserver', '127.0.0.1:8000', '--noreload'])
    except KeyboardInterrupt:
        print("\n\nShutting down server...")
        sys.exit(0)


if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        print("\n" + "=" * 50)
        print("ERROR OCCURRED!")
        print("=" * 50)
        print(f"\n{type(e).__name__}: {str(e)}\n")
        import traceback
        traceback.print_exc()
        print("\nPress Enter to exit...")
        input()
        sys.exit(1)
