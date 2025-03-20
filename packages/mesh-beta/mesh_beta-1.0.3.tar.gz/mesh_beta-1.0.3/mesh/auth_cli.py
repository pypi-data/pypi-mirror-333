#!/usr/bin/env python3
"""
Mesh Authentication CLI

This script provides a command-line interface for authenticating with Mesh.
It can be used directly or as a post-install script.
"""

import os
import sys
import argparse
import logging
import socket
from . import auth

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("mesh.auth_cli")

def find_available_port(start_port=45678, end_port=45700):
    """Find an available port in the given range"""
    for port in range(start_port, end_port):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            try:
                s.bind(('localhost', port))
                return port
            except socket.error:
                continue
    return None

def main():
    """Run the authentication flow"""
    parser = argparse.ArgumentParser(description="Authenticate with Mesh")
    parser.add_argument("--force", action="store_true", help="Force a new login even if already authenticated")
    parser.add_argument("--headless", action="store_true", help="Use device code flow instead of browser")
    parser.add_argument("--port", type=int, help="Specify a port for the callback server")
    parser.add_argument("--auto", action="store_true", help="Run in automatic mode (for installation)")
    args = parser.parse_args()
    
    print("Starting Mesh authentication...")
    
    # Always use device code flow by default
    try:
        print("Attempting device code authentication...")
        token_data = auth.authenticate_device_flow()
        if token_data:
            print("Authentication successful using device code flow!")
            return 0
        print("Device code authentication failed.")
        return 1
    except Exception as e:
        print(f"Device code authentication error: {e}")
        return 1

if __name__ == "__main__":
    sys.exit(main()) 