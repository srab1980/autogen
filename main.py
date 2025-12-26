#!/usr/bin/env python3
"""
AutoGen Studio Application
This is the entry point for running AutoGen Studio.
"""

if __name__ == "__main__":
    import sys
    import os
    import subprocess
    
    # Get port from environment or use default
    port = os.environ.get('PORT', '8081')
    host = os.environ.get('HOST', '0.0.0.0')
    
    # Run autogenstudio UI using subprocess for safety
    subprocess.run(['autogenstudio', 'ui', '--host', host, '--port', port])
