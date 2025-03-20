import inspect
import json
import uuid
from typing import Dict, List, Optional, Any, Union, Callable
from cognite.client import CogniteClient
from ..data_classes import AgentMessage, ToolCall, Attachment


class AgentSession:
    """
    Represents a chat session with an agent.
    
    Args:
        cognite_client: The CogniteClient to use for authentication and API calls.
        agent_id: The external ID of the agent.
        client_tools: Optional list of tool functions to make available to the agent.
        run_python: Whether to automatically execute client-side tool calls.
    """
    
    def __init__(
        self, 
        cognite_client: CogniteClient, 
        agent_id: str, 
        client_tools: Optional[List[Callable]] = None, 
        run_python: bool = False
    ):
        self._cognite_client = cognite_client
        self._agent_id = agent_id
        self._client_tools = client_tools or []
        self._run_python = run_python
        self._cursor = None
        self._messages = []
        self._tool_map = {tool.__name__: tool for tool in self._client_tools}
    
    def chat(self, message: str) -> AgentMessage:
        """
        Send a message to the agent and get a response.
        
        Args:
            message: The message to send.
            
        Returns:
            AgentMessage: The agent's response, including message text, tool calls, reasoning, and attachments.
        """
        # Create a unique message ID
        message_id = str(uuid.uuid4())
        
        # Create the user message
        user_message = {
            "id": message_id,
            "content": {
                "type": "text",
                "text": message
            },
            "role": "user"
        }
        
        # Add the new message to our history
        self._messages.append(user_message)
        
        # Prepare the request with all messages in the conversation history
        request = {
            "agentId": self._agent_id,
            "messages": self._messages  # Send all messages, not just the current one
        }
        
        # Add cursor if we have one (for continuing the conversation)
        if self._cursor:
            request["cursor"] = self._cursor
        
        # Add custom tools if provided
        if self._client_tools:
            request["customClientTools"] = self._prepare_custom_tools()
        
        # Make the API call
        url = f"/api/v1/projects/{self._cognite_client.config.project}/ai/agents/chat"
        response = self._cognite_client.post(
            url, 
            json=request, 
            headers={"cdf-version": "20240101-alpha"}
        )
        
        # Extract the JSON content from the response
        response_json = response.json()
        
        # Store the cursor for the next request
        self._cursor = response_json.get("cursor")
        
        # Process the response
        agent_message = None
        if "messages" in response_json and response_json["messages"]:
            # Get the last message from the agent
            agent_response = next((msg for msg in reversed(response_json["messages"]) 
                                if msg.get("role") == "agent"), None)
            if agent_response:
                # Create the AgentMessage object from the response
                agent_message = AgentMessage.from_dict(agent_response)
                
                # Add the agent's response to our message history
                self._messages.append(agent_response)
                
                # Handle tool calls if run_python is enabled
                if self._run_python and agent_message.tool_calls:
                    self._execute_tool_calls(agent_message.tool_calls)
        
        # Include attachments from the top-level response if they exist
        if agent_message and "attachments" in response_json:
            for attachment_data in response_json.get("attachments", []):
                attachment = Attachment.from_dict(attachment_data)
                if attachment not in agent_message.attachments:
                    agent_message.attachments.append(attachment)
        
        return agent_message
    
    def _execute_tool_calls(self, tool_calls: List[ToolCall]) -> None:
        """
        Execute client-side tool calls.
        
        Args:
            tool_calls: The tool calls to execute.
        """
        for tool_call in tool_calls:
            if tool_call.name in self._tool_map:
                tool_func = self._tool_map[tool_call.name]
                try:
                    result = tool_func(**tool_call.arguments)
                    # Here we could send the result back to the agent in a follow-up message
                    # For now, we'll just print the result
                    print(f"Tool call result for {tool_call.name}: {result}")
                except Exception as e:
                    print(f"Error executing tool {tool_call.name}: {str(e)}")
    
    def _prepare_custom_tools(self) -> List[Dict[str, Any]]:
        """
        Prepare the custom tools for the API request.
        
        Returns:
            List[Dict[str, Any]]: The prepared tools.
        """
        prepared_tools = []
        
        for tool in self._client_tools:
            # Get the function signature and docstring
            signature = inspect.signature(tool)
            docstring = inspect.getdoc(tool) or ""
            
            # Prepare the tool definition
            tool_def = {
                "name": tool.__name__,
                "description": docstring,
                "parameters": {
                    "type": "object",
                    "properties": {},
                    "required": []
                }
            }
            
            # Add parameters
            for param_name, param in signature.parameters.items():
                # Skip self parameter for methods
                if param_name == "self":
                    continue
                
                # Get parameter type annotation if available
                param_type = "string"  # Default type
                if param.annotation != inspect.Parameter.empty:
                    if param.annotation == str:
                        param_type = "string"
                    elif param.annotation == int:
                        param_type = "integer"
                    elif param.annotation == float:
                        param_type = "number"
                    elif param.annotation == bool:
                        param_type = "boolean"
                
                # Add parameter to the tool definition
                tool_def["parameters"]["properties"][param_name] = {
                    "type": param_type,
                    "description": f"Parameter {param_name}"
                }
                
                # Add to required parameters if it doesn't have a default value
                if param.default == inspect.Parameter.empty:
                    tool_def["parameters"]["required"].append(param_name)
            
            prepared_tools.append(tool_def)
        
        return prepared_tools 