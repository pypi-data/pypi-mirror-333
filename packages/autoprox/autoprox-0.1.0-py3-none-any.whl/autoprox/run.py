import uvicorn
import argparse
import sys
from typing import List, Optional

def main(args: Optional[List[str]] = None) -> int:
    """
    Run the Autonomi Network Proxy server.
    
    Args:
        args: Command line arguments (if None, sys.argv[1:] will be used)
        
    Returns:
        Exit code (0 for success)
    """
    parser = argparse.ArgumentParser(
        description="Autonomi Network HTTP Proxy Server"
    )
    parser.add_argument(
        "--host", 
        default="localhost", 
        help="Host to bind the server to (default: localhost)"
    )
    parser.add_argument(
        "--port", 
        type=int, 
        default=17017, 
        help="Port to bind the server to (default: 17017)"
    )
    parser.add_argument(
        "--reload",
        action="store_true",
        help="Enable auto-reload (for development)"
    )
    
    parsed_args = parser.parse_args(args)
    
    print(f"Starting Autonomi Network Proxy on {parsed_args.host}:{parsed_args.port}")
    print("API documentation will be available at: http://{}:{}/v0/docs".format(
        parsed_args.host, parsed_args.port
    ))
    
    uvicorn.run(
        "autoprox.main:app",
        host=parsed_args.host,
        port=parsed_args.port,
        reload=parsed_args.reload
    )
    
    return 0

if __name__ == "__main__":
    sys.exit(main()) 