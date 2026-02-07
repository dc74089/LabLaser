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
    from django.core.management import execute_from_command_line
    print("Setting up database...")
    execute_from_command_line(['manage.py', 'migrate', '--noinput'])


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

    # Start browser in background thread
    browser_thread = threading.Thread(target=open_browser, daemon=True)
    browser_thread.start()

    # Import and run server
    from django.core.management import execute_from_command_line

    print("\nServer starting at http://127.0.0.1:8000")
    print("Press CTRL+C to stop the server\n")

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
