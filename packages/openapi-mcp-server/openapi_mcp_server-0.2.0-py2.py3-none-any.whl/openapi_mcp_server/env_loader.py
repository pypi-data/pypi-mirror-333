"""
Environment variable loader for the OpenAPI MCP Server.
"""
import os
import sys
from openapi_mcp_server.utils import setup_logging

# Setup logging (done once at module level)
DEBUG = os.getenv("DEBUG", "FALSE").lower() in ("true", "1", "yes")
logger = setup_logging(debug=DEBUG)

def load_env_file(env_path):
    """
    Load environment variables from a .env file.
    
    Args:
        env_path (str): Path to the .env file
    """
    if not os.path.exists(env_path):
        logger.debug(f"Error: .env file not found at: {env_path}")
        logger.debug("Using existing environment variables only.")
        return
    
    try:
        with open(env_path, 'r') as file:
            for line in file:
                line = line.strip()
                
                # Skip empty lines and comments
                if not line or line.startswith('#'):
                    continue
                
                # Parse variable assignments
                if '=' in line:
                    key, value = line.split('=', 1)
                    key = key.strip()
                    value = value.strip()
                    
                    # Remove quotes if present
                    if value.startswith('"') and value.endswith('"'):
                        value = value[1:-1]
                    elif value.startswith("'") and value.endswith("'"):
                        value = value[1:-1]
                    
                    os.environ[key] = value
        
        logger.debug(f"Environment variables loaded from {env_path}")
    
    except Exception as e:
        logger.debug(f"Error loading .env file: {str(e)}")
        sys.exit(1)
