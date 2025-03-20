#!/usr/bin/env python
import argparse
import sys
import streamlit.web.cli as stcli
import os

def main():
    parser = argparse.ArgumentParser(description="Melvin - Tecton Copilot")
    parser.add_argument("--port", type=int, default=3000, help="Port to run the server on")
    parser.add_argument("--host", type=str, default="localhost", help="Host to run the server on")
    parser.add_argument("--no-browser", action="store_true", help="Don't open browser automatically")
    
    args = parser.parse_args()
    
    # Get the absolute path to the UI file
    ui_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "ui.py")
    
    # Prepare Streamlit arguments
    sys.argv = [
        "streamlit", "run", 
        ui_path,
        "--server.port", str(args.port),
        "--server.address", args.host,
        "--browser.gatherUsageStats", "false",
        "--theme.base", "light"
    ]
    
    if args.no_browser:
        sys.argv.extend(["--server.headless", "true"])
    
    # Run Streamlit
    sys.exit(stcli.main())

if __name__ == "__main__":
    main()
