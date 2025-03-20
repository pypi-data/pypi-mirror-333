# OpenAPI MCP Server 🎭

[![smithery badge](https://smithery.ai/badge/@rahgadda/openapi_mcp_server)](https://smithery.ai/server/@rahgadda/openapi_mcp_server)

A Model Context Protocol server that provides REST API automation.  
This server enable LLMs to interact with RestAPI's.   
It takes swagger as input.   
Support all HTTP API Call's `GET/PUT/POST/PATCH`

## Installation
- Install package
  ```bash
  pip install openapi_mcp_server
  ```
- Below is an example to test Petstore, details available [here](https://petstore.swagger.io/). Create .env in a folder as below
  ```env
  DEBUG="True"
  API_BASE_URL="https://petstore.swagger.io/v2"
  OPENAPI_SPEC_PATH="https://petstore.swagger.io/v2/swagger.json"
  API_HEADERS="Accept:application/json"
  API_WHITE_LIST="addPet,updatePet,findPetsByStatus"
  ```
- Test with mcp server using `openapi_mcp_server` from same folder.
- Update Claud Desktop configuration with below
  ```json
  {
    "mcpServers": {
      "openapi_mcp_server":{
        "command": "openapi_mcp_server",
        "env": {
            "DEBUG":"1",
            "API_BASE_URL":"https://petstore.swagger.io/v2",
            "OPENAPI_SPEC_PATH":"https://petstore.swagger.io/v2/swagger.json",
            "API_HEADERS":"Accept:application/json",
            "API_WHITE_LIST":"addPet,updatePet,findPetsByStatus"
        }
      }
    }
  }
  ```
  
## Features
- FastAPI implementation of MCP
- RESTful API endpoints
- Schema validation

## Configuration
- List of available parameters
  - `DEBUG`: Enable debug logging (optional default is False)
  - `OPENAPI_SPEC_PATH`: Path to the OpenAPI document
  - `API_BASE_URL`: Base URL for the API requests
  - `API_HEADERS`: Headers to include in the API requests (optional)
  - `API_WHITE_LIST`: White Listed operationId in list format ["operationId1", "operationId2"] (optional)
  - `API_BLACK_LIST`: Black Listed operationId in list format ["operationId3", "operationId4"] (optional)
  - `HTTP_PROXY`: HTTP Proxy details
  - `HTTPS_PROXY`: HTTPS Proxy details
  - `NO_PROXY`: No Proxy details
- Demo
  - ![Pet Store Demo](https://github.com/rahgadda/openapi_mcp_server/blob/main/images/openapi_mcp_server_petstore_example.png?raw=true)
  - ![Loan Payment Demo](https://github.com/rahgadda/openapi_mcp_server/blob/main/images/openapi_mcp_server_account_payment_example.png?raw=true)

## Contributing
Contributions are welcome. Please feel free to submit a Pull Request.

## License
This project is licensed under the terms of the MIT license.

## Star History
[![Star History Chart](https://api.star-history.com/svg?repos=rahgadda/openapi_mcp_server=Date)](https://star-history.com/#rahgadda/openapi_mcp_server&Date)