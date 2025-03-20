import os
import sys
import webbrowser
import argparse
from django.core.management import execute_from_command_line

def main():
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "health_report.settings")

    # Parse command-line arguments for custom port
    parser = argparse.ArgumentParser()
    parser.add_argument("--port", type=str, default="8000", help="Port to run the server on")
    args = parser.parse_args()

    # Run database migrations
    execute_from_command_line(["manage.py", "migrate"])

    # Collect static files
    execute_from_command_line(["manage.py", "collectstatic", "--noinput"])

    # Start the Django development server
    execute_from_command_line(["manage.py", "runserver", f"127.0.0.1:{args.port}"])

    # Open the browser automatically
    webbrowser.open(f"http://127.0.0.1:{args.port}")

if __name__ == "__main__":
    main()
