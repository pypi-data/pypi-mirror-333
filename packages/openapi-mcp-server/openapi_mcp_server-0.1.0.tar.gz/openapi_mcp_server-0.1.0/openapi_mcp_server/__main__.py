import os
import sys
from requests import request
import json

from typing import List, Dict, Any, Optional, Union
from pydantic import BaseModel, create_model, Field

from dotenv import load_dotenv
from openapi_mcp_server.utils import setup_logging, load_swagger_spec, extract_api_metadata
from mcp.server.fastmcp import FastMCP

"""
Entry point for the openapi_mcp_server.
The server supports dynamic parsing of the OpenAPI document and executes API calls with the appropriate request parameters.

Configuration is controlled via environment variables:
- DEBUG: Enable debug logging (optional default is False)
- OPENAPI_SPEC_PATH: Path to the OpenAPI document
- API_BASE_URL: Base URL for the API requests
- API_HEADERS: Headers to include in the API requests (optional)
- API_WHITE_LIST: White Listed operationId in list format ["operationId1", "operationId2"] (optional)
- API_BLACK_LIST: Black Listed operationId in list format ["operationId3", "operationId4"] (optional)
- HTTP_PROXY: HTTP Proxy details
- HTTPS_PROXY: HTTPS Proxy details
- NO_PROXY: No Proxy details
"""

# Load environment variables from .env if present
load_dotenv()

# Setup logging
DEBUG = os.getenv("DEBUG", "FALSE").lower() in ("true", "1", "yes")
logger = setup_logging(debug=DEBUG)

# Configure proxy settings from environment variables
http_proxy = os.getenv("HTTP_PROXY")
https_proxy = os.getenv("HTTPS_PROXY")
no_proxy = os.getenv("NO_PROXY")

# Apply proxy settings to the environment if they exist
if http_proxy:
    os.environ["HTTP_PROXY"] = http_proxy
    logger.debug(f"HTTP proxy set: {http_proxy}")
if https_proxy:
    os.environ["HTTPS_PROXY"] = https_proxy
    logger.debug(f"HTTPS proxy set: {https_proxy}")
if no_proxy:
    os.environ["NO_PROXY"] = no_proxy
    logger.debug(f"No proxy domains: {no_proxy}")

# Pydantic Model Cache
model_cache = {}
model_mapping = {}

# Updating Variables from Environment Variables
logger.debug("DEBUG: %s", DEBUG)

if not os.getenv("OPENAPI_SPEC_PATH"):
    logger.error("OPENAPI_SPEC_PATH environment variable is not set")
    sys.exit(1)
else:
    OPENAPI_SPEC_PATH = os.getenv("OPENAPI_SPEC_PATH")
    logger.debug("OPENAPI_SPEC_PATH: %s", OPENAPI_SPEC_PATH)

if not os.getenv("API_BASE_URL"):
    logger.error("API_BASE_URL environment variable is not set")
    sys.exit(1)
else:
    API_BASE_URL = os.getenv("API_BASE_URL")
    logger.debug("API_BASE_URL: %s", API_BASE_URL)

API_HEADERS = os.getenv("API_HEADERS")
logger.debug("API_HEADERS: %s", API_HEADERS)

API_WHITE_LIST = os.getenv("API_WHITE_LIST")
logger.debug("API_WHITE_LIST: %s", API_WHITE_LIST)

API_BLACK_LIST = os.getenv("API_BLACK_LIST")
logger.debug("API_BLACK_LIST: %s", API_BLACK_LIST)

# Initialize FastMCP Server
mcp = FastMCP("openapi_mcp_server")

def get_py_type(json_type):
    """Convert JSON schema types to Python/Pydantic types"""
    type_map = {
        'integer': int,
        'number': float,
        'string': Any,
        'boolean': bool,
        'array': List,
        'object': Dict[str, Any]
    }
    return type_map.get(json_type, Any)

# Helper function to get parameter type safely
def get_param_type(param):
    if 'schema' in param:
        json_type = param['schema'].get('type', 'string')
    elif 'type' in param:
        json_type = param.get('type', 'string')
    else:
        json_type = 'string'  # default to string if type info is missing
    
    return get_py_type(json_type).__name__  # Convert to Python type and get its name

def create_pydantic_model_from_json(json_obj, model_name):
    """Create a Pydantic model from a JSON object example"""
    # Check if model already exists in cache
    if model_name in model_cache:
        return model_cache[model_name]
    
    logger.debug(f"Generating Pydantic model: {model_name}")

    fields = {}
    nested_models = []
    
    for field_name, field_value in json_obj.items():
        if isinstance(field_value, dict):
            # Create nested model
            nested_model_name = f"{model_name}{field_name.capitalize()}"
            nested_model = create_pydantic_model_from_json(field_value, nested_model_name)
            fields[field_name] = (Optional[nested_model], field_value)
            nested_models.append(nested_model)
        elif isinstance(field_value, list) and field_value and isinstance(field_value[0], dict):
            # Create nested model for array items
            nested_model_name = f"{model_name}{field_name.capitalize()}Item"
            nested_model = create_pydantic_model_from_json(field_value[0], nested_model_name)
            fields[field_name] = (List[nested_model], [])
            nested_models.append(nested_model)
        else:
            # Determine type from example value
            py_type = type(field_value)
            if py_type is str:
                fields[field_name] = (Optional[str], field_value)
            elif py_type is int:
                fields[field_name] = (Optional[int], field_value)
            elif py_type is float:
                fields[field_name] = (Optional[float], field_value)
            elif py_type is bool:
                fields[field_name] = (Optional[bool], field_value)
            elif py_type is list:
                fields[field_name] = (List[str], [])
            else:
                fields[field_name] = (Any, field_value)
    
    # Create model with the fields
    model = create_model(model_name, **fields)
    model_cache[model_name] = model
    
    # Make any nested models available in global scope
    for nested_model in nested_models:
        globals()[nested_model.__name__] = nested_model
    
    # Make model available in global scope
    globals()[model_name] = model
    
    logger.debug(f"Generated Pydantic model: {model_name}")
    logger.debug(model.model_json_schema())

    return model

# Load the OpenAPI document and create tools
def create_dynamic_tools() -> str:
    """
    Load OpenAPI document and create tools for each endpoint.
    """

    logger.debug("Executing list_functions tool.")
    
    # Check if OPENAPI_SPEC_PATH is file or URL
    try:
        if os.path.exists(OPENAPI_SPEC_PATH):
            with open(OPENAPI_SPEC_PATH, "r") as file:
                openapi_spec = file.read()
        else:
            openapi_spec = request('GET',OPENAPI_SPEC_PATH).text
    except Exception as e:
        logger.error(f"Error loading OpenAPI Spec: {e}")
        return
    
    # Convert openapi_spec to json
    try:
        openapi_spec_json = json.loads(openapi_spec)
    except Exception as e:
        logger.error(f"Error parsing OpenAPI Spec: {e}")
        return
    
    # Generating OpenAPI Spec Metadata
    try:
        version = load_swagger_spec(openapi_spec_json)
        metadata = extract_api_metadata(API_WHITE_LIST, API_BLACK_LIST, openapi_spec_json, version)
    except Exception as e:
        logger.error(f"Error processing OpenAPI Spec Metadata: {e}")
        return

    # Pre-generate all request models before creating functions
    for endpoint in metadata:
        if endpoint['request_body'] is not None:
            model_name = f"{endpoint['operationId'].capitalize()}Request"
            model = create_pydantic_model_from_json(endpoint['request_body'], model_name)
            model_mapping[endpoint['operationId']] = model_name
    
    # Dynamically generate functions for each endpoint
    for endpoint in metadata:
        try:
            func_name = endpoint['operationId']
            path = endpoint['path']
            method = endpoint['method'].upper()
            
            logger.debug(f"Generating function for endpoint: {func_name} ({method} {path})")
            
            # Parameter collections
            parameters = []
            doc_parameters = []
            
            # Path parameters
            for p in endpoint['path_parameters']:
                param_name = p['name']
                param_type = get_param_type(p)
                parameters.append(f"{param_name}: {param_type}")
                
                p_description = p.get('description', '')
                doc_parameters.append(
                    f"{param_name} (path): {p_description} "
                    f"(required, {param_type})"
                )

            # Query parameters
            for q in endpoint['query_parameters']:
                param_name = q['name']
                param_type = get_param_type(q)
                required = q.get('required', False)
                enum = None
                
                # Get enum values if present in either schema or direct parameter definition
                if 'schema' in q:
                    enum = q['schema'].get('enum')
                elif 'enum' in q:
                    enum = q.get('enum')
                
                enum_str = f" [Allowed: {', '.join(enum)}]" if enum else ""
                
                parameters.append(
                    f"{param_name}: {param_type} = None" if not required 
                    else f"{param_name}: {param_type} = None"
                )

                q_description = q.get('description', '')
                doc_parameters.append(
                    f"{param_name} (query): {q_description} "
                    f"({'required' if required else 'optional'}, {param_type}){enum_str}"
                )

            # Header parameters
            for h in endpoint['header_parameters']:
                param_name = h['name']
                param_type = get_param_type(h)
                required = h.get('required', False)
                
                parameters.append(
                    f"{param_name}: {param_type} = None" if not required 
                    else f"{param_name}: {param_type} = None"
                )

                h_description = h.get('description','')

                doc_parameters.append(
                    f"{param_name} (header): {h_description} "
                    f"({'required' if required else 'optional'}, {param_type})"
                )

            # Request body - create Pydantic model if needed
            request_model = None
            if endpoint['request_body'] is not None:
                try:
                    # Get the pre-generated model name
                    model_name = model_mapping[func_name]
                    request_model = globals()[model_name]
                    
                    # Add the model as a parameter to the function
                    parameters.append(f"body: {model_name} = None")
                    doc_parameters.append(
                        f"body (body): Request body ({model_name} instance)\n"
                        f"Example structure: {json.dumps(endpoint['request_body'], indent=2)}"
                    )
                except KeyError as e:
                    logger.error(f"Error finding model for {func_name}: {str(e)}")
                    logger.debug(f"Available models: {list(model_mapping.keys())}")
                    continue
                except Exception as e:
                    logger.error(f"Unexpected error handling request body for {func_name}: {str(e)}")
                    continue

            # Generate function signature
            params_str = ', '.join(parameters)
            
            # Build docstring
            docstring = f'"""{endpoint["summary"]}\n\n{endpoint["description"]}\n\nParameters:\n'
            docstring += '\n'.join([f'- {p}' for p in doc_parameters])
            docstring += '\n"""'
            
            # Generate function code
            func_code = f'def {func_name}({params_str}):\n'
            func_code += f'    {docstring}\n'
            
            # URL construction
            func_code += f'    try:\n'
            func_code += f'        url = f"{API_BASE_URL}{path}"\n'
            func_code += f'        logger.debug(f"Base URL constructed: {{url}}")\n'
            
            for p in endpoint['path_parameters']:
                name = p['name']
                func_code += f'        url = url.replace("{{{name}}}", str({name}))\n'
            
            func_code += f'        logger.debug(f"Final URL with path parameters: {{url}}")\n'
            
            # Query parameters
            func_code += '        params = {}\n'
            for q in endpoint['query_parameters']:
                name = q['name']
                func_code += f'        if {name} is not None:\n'
                func_code += f'            params["{name}"] = {name}\n'
                func_code += f'            logger.debug(f"Added query parameter: {name}={{{name}}}")\n'
            
            # Headers
            func_code += '        headers = {"Content-Type": "application/json"}\n'
            func_code += '        # Add any custom API headers from config\n'
            func_code += '        if API_HEADERS:\n'
            func_code += '            try:\n'
            func_code += '                custom_headers = {}\n'
            func_code += '                header_pairs = API_HEADERS.split(",")\n'
            func_code += '                for pair in header_pairs:\n'
            func_code += '                    key, value = pair.split(":")\n'
            func_code += '                    custom_headers[key.strip()] = value.strip()\n'
            func_code += '                headers.update(custom_headers)\n'
            func_code += '                logger.debug(f"Added custom headers from config: {custom_headers}")\n'
            func_code += '            except json.JSONDecodeError as e:\n'
            func_code += '                logger.warning(f"Failed to parse API_HEADERS: {e}")\n'
            
            for h in endpoint['header_parameters']:
                name = h['name']
                func_code += f'        if {name} is not None:\n'
                func_code += f'            headers["{name}"] = {name}\n'
                func_code += f'            logger.debug(f"Added header: {name}={{{name}}}")\n'
            
            # Request body
            if request_model:
                # Create default model instance if needed
                func_code += f'        # Use provided body or create default\n'
                func_code += f'        if body is None:\n'
                func_code += f'            body = {model_name}(**{json.dumps(endpoint["request_body"])})\n'
                func_code += f'            logger.debug("Created default request body")\n'
                func_code += f'        # Convert Pydantic model to dict for request\n'
                func_code += f'        try:\n'
                func_code += f'            json_data = body.dict(exclude_unset=True)\n'
                func_code += f'            logger.debug(f"Request body: {{json.dumps(json_data, indent=2)}}")\n'
                func_code += f'        except AttributeError:\n'
                func_code += f'            # For Pydantic v2 compatibility\n'
                func_code += f'            json_data = body.model_dump(exclude_unset=True)\n'
                func_code += f'            logger.debug(f"Request body (v2): {{json.dumps(json_data, indent=2)}}")\n'
            else:
                func_code += '        json_data = None\n'
            
            # HTTP request
            func_code += f'        logger.info(f"Making {method} request to {{url}}")\n'
            func_code += f'        response = request("{method}", url, params=params, headers=headers, json=json_data)\n'
            func_code += f'        logger.debug(f"Response status code: {{response.status_code}}")\n'
            func_code += '        response.raise_for_status()  # Raise exception for bad status codes\n'
            func_code += '        try:\n'
            func_code += '            result = response.json()\n'
            func_code += '            logger.debug(f"Received JSON response")\n'
            func_code += '            logger.debug(result)\n'
            func_code += '            return result\n'
            func_code += '        except ValueError:\n'
            func_code += '            result = response.text\n'
            func_code += '            logger.debug(f"Received text response: {result[:100]}...")\n'
            func_code += '            return result\n'
            func_code += '    except Exception as e:\n'
            func_code += f'        error_msg = f"Error executing {func_name}: {{str(e)}}"\n'
            func_code += '        logger.error(error_msg)\n'
            func_code += '        return {"error": error_msg}\n'
            
            # Create the function in global scope
            logger.debug(f"Generated function code for {func_name}:\n{func_code}")
            try:
                exec(func_code, globals())
                logger.info(f"Successfully created function: {func_name}")
                
                # Apply decorator to the dynamically created function
                if func_name in globals():
                    globals()[func_name] = mcp.tool(name=endpoint["operationId"], description=endpoint["description"])(globals()[func_name])
                    logger.debug(f"Function {func_name} registered as tool")

            except Exception as exec_error:
                logger.error(f"Failed to create function {func_name}: {str(exec_error)}")
                logger.error(f"Function code that failed:\n{func_code}")
                
        except Exception as e:
            logger.error(f"Error generating function for endpoint: {str(e)}")
            logger.debug(f"Endpoint data: {json.dumps(endpoint, indent=2)}")
            continue

def main():
    """
    Runs the FastMCP version of the Any OpenAPI server.
    """

    try:
        # Initialize and run the server
        try:
            logger.info("Starting openapi_mcp_server")
            create_dynamic_tools()
            mcp.run(transport='stdio')
        except KeyboardInterrupt:
            try:
                sys.exit(130)
            except SystemExit:
                os._exit(130)

    except Exception as e:
        logger.error("Error in openapi_mcp_server: %s", e)
        return

if __name__ == "__main__":
    main()