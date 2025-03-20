from typing import Dict, List, Optional, Any, Union, Callable
import json
from cognite.client import CogniteClient
from .session import AgentSession
from ..data_classes import AgentDefinition


class Agent:
    """
    Represents an agent in the Cognite AI platform.
    
    Args:
        cognite_client: The CogniteClient to use for authentication and API calls.
        data: The agent data.
    """
    
    def __init__(self, cognite_client: CogniteClient, data: Dict[str, Any]):
        self._cognite_client = cognite_client
        self._data = data
    
    @property
    def id(self) -> str:
        """
        Get the external ID of the agent.
        
        Returns:
            str: The external ID.
        """
        return self._data["externalId"]
    
    @property
    def name(self) -> str:
        """
        Get the name of the agent.
        
        Returns:
            str: The name.
        """
        return self._data["name"]
    
    @property
    def description(self) -> Optional[str]:
        """
        Get the description of the agent.
        
        Returns:
            Optional[str]: The description, or None if not set.
        """
        return self._data.get("description")
    
    @property
    def tools(self) -> List[Dict[str, Any]]:
        """
        Get the tools available to the agent.
        
        Returns:
            List[Dict[str, Any]]: The tools.
        """
        return self._data.get("tools", [])
    
    @property
    def model(self) -> Optional[str]:
        """
        Get the model used by the agent.
        
        Returns:
            Optional[str]: The model name, or None if not set.
        """
        return self._data.get("model")
    
    def __str__(self) -> str:
        """
        Get a string representation of the agent.
        
        Returns:
            str: A JSON string representation of the agent data.
        """
        return json.dumps(self._data, indent=2)
    
    def __repr__(self) -> str:
        """
        Get a concise representation of the agent for debugging.
        
        Returns:
            str: A concise representation of the agent.
        """
        tool_names = [tool.get("name", f"Tool_{i}") for i, tool in enumerate(self.tools)]
        return f"Agent(id='{self.id}', name='{self.name}', tools={tool_names})"
    
    def start_session(self, client_tools: Optional[List[Callable]] = None, run_python: bool = False) -> AgentSession:
        """
        Start a chat session with the agent.
        
        Args:
            client_tools: Optional list of tool functions to make available to the agent.
            run_python: Whether to automatically execute client-side tool calls.
            
        Returns:
            AgentSession: The chat session.
        """
        return AgentSession(self._cognite_client, self.id, client_tools, run_python)
    
    def to_dict(self) -> Dict[str, Any]:
        """
        Convert the agent to a dictionary.
        
        Returns:
            Dict[str, Any]: The agent as a dictionary.
        """
        return self._data.copy()
    
    @classmethod
    def from_definition(cls, cognite_client: CogniteClient, definition: AgentDefinition) -> "Agent":
        """
        Create an Agent from an AgentDefinition.
        
        Args:
            cognite_client: The CogniteClient to use for authentication and API calls.
            definition: The agent definition.
            
        Returns:
            Agent: The created agent.
        """
        return cls(cognite_client, definition.to_dict()) 