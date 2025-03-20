 # fewsats-mcp

 This package was created using `uv`, a fast Python package installer and resolver.

 ## Project Setup

 To recreate this project, follow these steps:

 ```bash
 # Initialize the project
 uv init fewsats-mcp
 cd fewsats-mcp

 # Create and activate a virtual environment
 uv venv
 source .venv/bin/activate

 # Add dependencies
 uv add "mcp[cli]" fewsats

 # Create main server file
 mv main.py fewsats-mcp-server.py

 # Run the server
 uv run fewsats-mcp-server.py



                                               Development

To work on this project:

 1 Activate the virtual environment:

    source .venv/bin/activate

 2 Make changes to the fewsats-mcp-server.py file.
 3 Run the server:

    uv run fewsats-mcp-server.py



                                                   TODO

 • [ ] Add tests
 • [ ] Configure CI/CD
 • [ ] Publish the package
