import os
import sys
import logging
import inspect
import importlib.util
import importlib
from flask import Flask, jsonify, request
from flask_cors import CORS

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler('node_api.log')
    ]
)

logger = logging.getLogger(__name__)

# Add the nodes directory to the Python path
nodes_dir = "/Users/tajnoah/Desktop/langmvp/act_workflow/act/nodes"
parent_dir = os.path.dirname(nodes_dir)
act_dir = os.path.dirname(parent_dir)

# Add all necessary directories to Python path
sys.path.append(nodes_dir)
sys.path.append(parent_dir)
sys.path.append(act_dir)

# Set up module structure for relative imports
act_module = type('MockActModule', (), {})
sys.modules['act'] = act_module

# Create nodes module
nodes_module = type('MockNodesModule', (), {})
sys.modules['act.nodes'] = nodes_module

# Create a mock NodeResource class
class MockNodeResource:
    def __init__(self, *args, **kwargs):
        pass
    
    def __getattr__(self, name):
        return self

# Import base_node and add MockNodeResource if needed
try:
    import base_node
    if not hasattr(base_node, 'NodeResource'):
        setattr(base_node, 'NodeResource', MockNodeResource)
        logger.info("Added mock NodeResource to base_node")
        
    # Add base_node to act.nodes for relative imports
    sys.modules['act.nodes.base_node'] = base_node
except Exception as e:
    logger.error(f"Error importing base_node: {str(e)}")
    # Create a mock base_node module with minimal functionality
    base_node = type('MockBaseNode', (), {})
    setattr(base_node, 'NodeResource', MockNodeResource)
    sys.modules['base_node'] = base_node
    sys.modules['act.nodes.base_node'] = base_node

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Dictionary to store node classes and instances
nodes = {}
node_registry = {}

def make_serializable(obj):
    """Convert objects to JSON serializable format."""
    if hasattr(obj, '__dict__'):
        return {k: make_serializable(v) for k, v in obj.__dict__.items() 
                if not k.startswith('_')}
    elif isinstance(obj, dict):
        return {k: make_serializable(v) for k, v in obj.items()}
    elif isinstance(obj, (list, tuple)):
        return [make_serializable(item) for item in obj]
    elif hasattr(obj, 'value') and not callable(obj.value):
        return obj.value
    else:
        # Try to convert to string or return as is if primitive type
        try:
            return str(obj) if not isinstance(obj, (int, float, bool, str, type(None))) else obj
        except:
            return str(type(obj))

def load_node_modules():
    """Dynamically load all Node classes from the nodes directory."""
    # Try to import the NodeRegistry from base_node
    try:
        if hasattr(base_node, 'NodeRegistry'):
            global node_registry
            node_registry = base_node.NodeRegistry
            logger.info("Successfully imported NodeRegistry")
    except Exception as e:
        logger.error(f"Error importing NodeRegistry: {str(e)}")
    
    # Get all node files
    node_files = [f for f in os.listdir(nodes_dir) if f.endswith('Node.py') and f != 'base_node.py']
    
    for file in node_files:
        try:
            # Get the module name without .py extension
            module_name = file[:-3]  
            
            # Create the full module name for relative imports
            full_module_name = f"act.nodes.{module_name}"
            
            # Load the module
            spec = importlib.util.spec_from_file_location(full_module_name, os.path.join(nodes_dir, file))
            module = importlib.util.module_from_spec(spec)
            
            # Register in sys.modules for relative imports
            sys.modules[full_module_name] = module
            sys.modules[module_name] = module  # Also register as a top-level module
            
            # Execute the module with error handling
            try:
                spec.loader.exec_module(module)
                logger.info(f"Successfully loaded module {full_module_name}")
            except Exception as e:
                logger.error(f"Error executing module {full_module_name}: {str(e)}")
                continue
            
            # Find node class in module
            for name, obj in inspect.getmembers(module):
                # Look for classes that have "Node" in their name and aren't base classes
                if (inspect.isclass(obj) and "Node" in name and 
                    name != "BaseNode" and name != "NodeRegistry"):
                    
                    # Get node_type from class name
                    node_type = name.lower().replace('node', '')
                    
                    # Try to instantiate the node with error handling
                    try:
                        node_instance = obj()
                        # Check if the class has get_schema method
                        if hasattr(node_instance, 'get_schema'):
                            # Store the node class and instance
                            nodes[node_type] = {
                                'class': obj,
                                'instance': node_instance,
                                'name': name,
                                'module': full_module_name
                            }
                            logger.info(f"Successfully instantiated node: {name}")
                        else:
                            nodes[node_type] = {
                                'class': obj,
                                'instance': node_instance,
                                'name': name,
                                'module': full_module_name,
                                'warning': 'No get_schema method found'
                            }
                            logger.warning(f"Node {name} has no get_schema method")
                    except Exception as e:
                        # Register the class even if instantiation fails
                        nodes[node_type] = {
                            'class': obj,
                            'instance': None,
                            'name': name,
                            'module': full_module_name,
                            'error': str(e)
                        }
                        logger.error(f"Error instantiating {name}: {str(e)}")
        
        except Exception as e:
            logger.error(f"Error loading module from file {file}: {str(e)}")
    
    # If NodeRegistry is available, try to get registered nodes from there
    if node_registry and hasattr(node_registry, 'get_nodes'):
        try:
            registry_nodes = node_registry.get_nodes()
            for node_type, node_class in registry_nodes.items():
                if node_type not in nodes:
                    try:
                        # Try to instantiate node from registry
                        node_instance = node_class()
                        nodes[node_type] = {
                            'class': node_class,
                            'instance': node_instance,
                            'name': node_class.__name__,
                            'from_registry': True
                        }
                        logger.info(f"Added and instantiated node from registry: {node_class.__name__}")
                    except Exception as e:
                        nodes[node_type] = {
                            'class': node_class,
                            'instance': None,
                            'name': node_class.__name__,
                            'from_registry': True,
                            'error': str(e)
                        }
                        logger.error(f"Error instantiating registry node {node_class.__name__}: {str(e)}")
        except Exception as e:
            logger.error(f"Error getting nodes from registry: {str(e)}")
    
    logger.info(f"Loaded {len(nodes)} node types")

@app.route('/api/nodes', methods=['GET'])
def get_all_nodes():
    """Return a list of all available nodes."""
    result = {}
    for node_type, node_data in nodes.items():
        try:
            # If we have an instance with get_schema, use it
            if node_data.get('instance') and hasattr(node_data['instance'], 'get_schema'):
                try:
                    schema = node_data['instance'].get_schema()
                    result[node_type] = {
                        'node_type': schema.node_type if hasattr(schema, 'node_type') else node_type,
                        'version': schema.version if hasattr(schema, 'version') else "unknown",
                        'description': schema.description if hasattr(schema, 'description') else "No description available",
                        'class_name': node_data['name'],
                        'status': 'active'
                    }
                except Exception as e:
                    result[node_type] = {
                        'node_type': node_type,
                        'class_name': node_data['name'],
                        'schema_error': str(e),
                        'status': 'error_schema'
                    }
            else:
                # If no instance or no get_schema, provide basic info
                result[node_type] = {
                    'node_type': node_type,
                    'class_name': node_data['name'],
                    'error': node_data.get('error', "Unknown error"),
                    'status': 'unavailable'
                }
                if 'module' in node_data:
                    result[node_type]['module'] = node_data['module']
                if 'from_registry' in node_data:
                    result[node_type]['from_registry'] = node_data['from_registry']
        except Exception as e:
            result[node_type] = {
                'node_type': node_type,
                'class_name': node_data.get('name', 'Unknown'),
                'error': str(e),
                'status': 'error'
            }
    
    return jsonify(result)

@app.route('/api/nodes/<node_type>', methods=['GET'])
def get_node_schema(node_type):
    """Return the complete schema for a specific node type."""
    if node_type not in nodes:
        return jsonify({'error': f'Node type {node_type} not found'}), 404
    
    node_data = nodes[node_type]
    
    # If instance is not available, try to instantiate it now
    if not node_data.get('instance'):
        try:
            node_data['instance'] = node_data['class']()
            logger.info(f"Instantiated {node_data['name']} on-demand")
        except Exception as e:
            return jsonify({
                'error': f"Could not instantiate {node_data['name']}: {str(e)}",
                'class_name': node_data['name'],
                'node_type': node_type
            }), 500
    
    try:
        schema = node_data['instance'].get_schema()
        # Convert schema to dict for JSON serialization
        schema_dict = make_serializable(schema)
        return jsonify(schema_dict)
    except Exception as e:
        return jsonify({
            'error': str(e),
            'class_name': node_data['name'],
            'node_type': node_type
        }), 500

@app.route('/api/nodes/<node_type>/operations', methods=['GET'])
def get_node_operations(node_type):
    """Return all available operations for a specific node type."""
    if node_type not in nodes:
        return jsonify({'error': f'Node type {node_type} not found'}), 404
    
    node_data = nodes[node_type]
    
    # If instance is not available, try to instantiate it now
    if not node_data.get('instance'):
        try:
            node_data['instance'] = node_data['class']()
            logger.info(f"Instantiated {node_data['name']} on-demand")
        except Exception as e:
            return jsonify({
                'error': f"Could not instantiate {node_data['name']}: {str(e)}",
                'class_name': node_data['name'],
                'node_type': node_type
            }), 500
    
    node_instance = node_data['instance']
    operations = []
    
    try:
        # Method 1: Check for OpenAI-style operation parameters
        if hasattr(node_instance, '_operation_parameters'):
            operations = list(node_instance._operation_parameters.keys())
        
        # Method 2: Look for operation methods
        if not operations:
            for name, method in inspect.getmembers(node_instance, inspect.ismethod):
                if name.startswith('_operation_'):
                    operations.append(name[11:])  # Remove '_operation_' prefix
        
        # Method 3: Check schema for operation enum
        if not operations:
            schema = node_instance.get_schema()
            for param in schema.parameters:
                if param.name == 'operation' and hasattr(param, 'enum'):
                    operations = param.enum
        
        # Method 4: Check for an Operation class in the module
        if not operations:
            module = inspect.getmodule(node_instance.__class__)
            for name, obj in inspect.getmembers(module):
                if name.endswith('Operation') and inspect.isclass(obj):
                    # Extract operations from class attributes
                    for attr_name, attr_value in inspect.getmembers(obj):
                        if not attr_name.startswith('_') and isinstance(attr_value, str):
                            operations.append(attr_value)
        
        # Add details if available
        operation_details = {}
        for op in operations:
            operation_details[op] = {
                'name': op,
                'description': f"Execute {op} operation",
                'endpoint': f"/api/nodes/{node_type}/operations/{op}"
            }
            
        return jsonify({
            'node_type': node_type,
            'operations_count': len(operations),
            'operations': operation_details
        })
    except Exception as e:
        logger.error(f"Error getting operations for {node_type}: {str(e)}")
        return jsonify({
            'error': str(e),
            'class_name': node_data['name'],
            'node_type': node_type
        }), 500

@app.route('/api/nodes/<node_type>/operations/<operation>', methods=['GET'])
def get_operation_parameters(node_type, operation):
    """Return the parameters required for a specific operation."""
    if node_type not in nodes:
        return jsonify({'error': f'Node type {node_type} not found'}), 404
    
    node_data = nodes[node_type]
    
    # If instance is not available, try to instantiate it now
    if not node_data.get('instance'):
        try:
            node_data['instance'] = node_data['class']()
            logger.info(f"Instantiated {node_data['name']} on-demand")
        except Exception as e:
            return jsonify({
                'error': f"Could not instantiate {node_data['name']}: {str(e)}",
                'class_name': node_data['name'],
                'node_type': node_type
            }), 500
    
    node_instance = node_data['instance']
    
    try:
        # Method 1: Use get_operation_parameters if available
        if hasattr(node_instance, 'get_operation_parameters'):
            params = node_instance.get_operation_parameters(operation)
            return jsonify({
                'node_type': node_type,
                'operation': operation,
                'parameters': params
            })
        
        # Method 2: Check _operation_parameters dictionary
        if hasattr(node_instance, '_operation_parameters'):
            param_names = node_instance._operation_parameters.get(operation.lower(), [])
            schema = node_instance.get_schema()
            all_params = schema.parameters
            
            # Filter parameters based on operation
            filtered_params = []
            for param in all_params:
                if param.name in param_names:
                    filtered_params.append(make_serializable(param))
            
            return jsonify({
                'node_type': node_type,
                'operation': operation,
                'parameters': filtered_params
            })
        
        # Method 3: For other nodes (fallback)
        schema = node_instance.get_schema()
        # Convert all parameters to serializable format
        all_params = [make_serializable(param) for param in schema.parameters]
        
        # As a fallback, return all parameters with a note
        return jsonify({
            'node_type': node_type,
            'operation': operation,
            'note': 'Operation-specific parameter filtering not available, showing all parameters',
            'parameters': all_params
        })
    except Exception as e:
        logger.error(f"Error getting parameters for {node_type}/{operation}: {str(e)}")
        return jsonify({
            'error': str(e),
            'node_type': node_type,
            'operation': operation
        }), 500

@app.route('/api/execute/<node_type>', methods=['POST'])
def execute_node(node_type):
    """Execute a node with given parameters."""
    if node_type not in nodes:
        return jsonify({'error': f'Node type {node_type} not found'}), 404
    
    node_data = nodes[node_type]
    
    # If instance is not available, try to instantiate it now
    if not node_data.get('instance'):
        try:
            node_data['instance'] = node_data['class']()
            logger.info(f"Instantiated {node_data['name']} on-demand")
        except Exception as e:
            return jsonify({
                'error': f"Could not instantiate {node_data['name']}: {str(e)}",
                'class_name': node_data['name'],
                'node_type': node_type
            }), 500
    
    try:
        node_instance = node_data['instance']
        node_params = request.json
        
        # Check if the execute method is sync or async
        if inspect.iscoroutinefunction(node_instance.execute):
            # For async nodes, you'll need to run this in an event loop
            import asyncio
            result = asyncio.run(node_instance.execute(node_params))
        else:
            # For sync nodes
            result = node_instance.execute(node_params)
            
        return jsonify(result)
    except Exception as e:
        logger.error(f"Error executing {node_type}: {str(e)}")
        return jsonify({
            'error': str(e),
            'node_type': node_type
        }), 500

@app.route('/api/docs', methods=['GET'])
def get_api_docs():
    """Return API documentation in OpenAPI format."""
    swagger_doc = {
        "openapi": "3.0.0",
        "info": {
            "title": "Node API",
            "description": "API for interacting with workflow nodes",
            "version": "1.0.0"
        },
        "servers": [
            {
                "url": "/api",
                "description": "Node API Server"
            }
        ],
        "paths": {
            "/nodes": {
                "get": {
                    "summary": "Get all nodes",
                    "description": "Returns a list of all available nodes",
                    "responses": {
                        "200": {
                            "description": "Successful response",
                            "content": {
                                "application/json": {
                                    "schema": {
                                        "type": "object"
                                    }
                                }
                            }
                        }
                    }
                }
            },
            "/nodes/{node_type}": {
                "get": {
                    "summary": "Get node schema",
                    "description": "Returns the schema for a specific node type",
                    "parameters": [
                        {
                            "name": "node_type",
                            "in": "path",
                            "required": True,
                            "schema": {
                                "type": "string"
                            }
                        }
                    ],
                    "responses": {
                        "200": {
                            "description": "Successful response",
                            "content": {
                                "application/json": {
                                    "schema": {
                                        "type": "object"
                                    }
                                }
                            }
                        }
                    }
                }
            },
            "/nodes/{node_type}/operations": {
                "get": {
                    "summary": "Get node operations",
                    "description": "Returns all operations for a node type",
                    "parameters": [
                        {
                            "name": "node_type",
                            "in": "path",
                            "required": True,
                            "schema": {
                                "type": "string"
                            }
                        }
                    ],
                    "responses": {
                        "200": {
                            "description": "Successful response"
                        }
                    }
                }
            },
            "/nodes/{node_type}/operations/{operation}": {
                "get": {
                    "summary": "Get operation parameters",
                    "description": "Returns parameters for a specific operation",
                    "parameters": [
                        {
                            "name": "node_type",
                            "in": "path",
                            "required": True,
                            "schema": {
                                "type": "string"
                            }
                        },
                        {
                            "name": "operation",
                            "in": "path",
                            "required": True,
                            "schema": {
                                "type": "string"
                            }
                        }
                    ],
                    "responses": {
                        "200": {
                            "description": "Successful response"
                        }
                    }
                }
            },
            "/execute/{node_type}": {
                "post": {
                    "summary": "Execute node",
                    "description": "Execute a node with the provided parameters",
                    "parameters": [
                        {
                            "name": "node_type",
                            "in": "path",
                            "required": True,
                            "schema": {
                                "type": "string"
                            }
                        }
                    ],
                    "requestBody": {
                        "description": "Node parameters",
                        "required": True,
                        "content": {
                            "application/json": {
                                "schema": {
                                    "type": "object"
                                }
                            }
                        }
                    },
                    "responses": {
                        "200": {
                            "description": "Successful response"
                        }
                    }
                }
            }
        }
    }
    
    return jsonify(swagger_doc)

@app.route('/', methods=['GET'])
def index():
    """Return a simple welcome page with links to API docs."""
    return """
    <html>
        <head>
            <title>Node API Server</title>
            <style>
                body { font-family: Arial, sans-serif; line-height: 1.6; padding: 20px; max-width: 800px; margin: 0 auto; }
                h1 { color: #333; }
                a { color: #0066cc; text-decoration: none; }
                a:hover { text-decoration: underline; }
                .endpoint { background: #f4f4f4; padding: 10px; border-radius: 5px; margin-bottom: 10px; }
                code { background: #e0e0e0; padding: 2px 4px; border-radius: 3px; }
            </style>
        </head>
        <body>
            <h1>Node API Server</h1>
            <p>Welcome to the Node API Server. Use the following endpoints to interact with the API:</p>
            
            <div class="endpoint">
                <h3>API Documentation</h3>
                <p><a href="/api/docs">/api/docs</a></p>
            </div>
            
            <div class="endpoint">
                <h3>List All Nodes</h3>
                <p><a href="/api/nodes">/api/nodes</a></p>
            </div>
            
            <p>For specific node operations, use the following pattern:</p>
            <code>/api/nodes/{node_type}</code><br>
            <code>/api/nodes/{node_type}/operations</code><br>
            <code>/api/nodes/{node_type}/operations/{operation}</code>
        </body>
    </html>
    """

# Load all node modules when the app starts
load_node_modules()

if __name__ == '__main__':
    app.run(debug=True, port=5088)