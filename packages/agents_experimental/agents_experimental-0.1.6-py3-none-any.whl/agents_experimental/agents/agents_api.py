from typing import Dict, List, Optional, Any, Union, Callable
from cognite.client import CogniteClient
from ..api.base import APIBase
from .agent import Agent
from ..data_classes import AgentDefinition


class AgentsAPI(APIBase):
    """
    API client for the Agents API.
    
    Args:
        cognite_client: The CogniteClient to use for authentication and API calls.
    """
    
    _RESOURCE_PATH = "/ai/agents"
    
    def __init__(self, cognite_client: CogniteClient):
        super().__init__(cognite_client)
    
    def create(self, agent: Union[Dict[str, Any], AgentDefinition]) -> Agent:
        """
        Create or update an agent.
        
        Args:
            agent: The agent to create or update, either as a dictionary or an AgentDefinition.
            
        Returns:
            Agent: The created or updated agent.
        """
        if isinstance(agent, AgentDefinition):
            agent_dict = agent.to_dict()
        else:
            agent_dict = agent
            
        request = {
            "items": [agent_dict]
        }
        response = self._post("", json=request)
        return Agent(self._cognite_client, response["items"][0])
    
    def list(self, limit: int = 25) -> List[Agent]:
        """
        List agents.
        
        Args:
            limit: Maximum number of agents to return.
            
        Returns:
            List[Agent]: The list of agents.
        """
        params = {"limit": limit}
        response = self._get("", params=params)
        return [Agent(self._cognite_client, item) for item in response["items"]]
    
    def retrieve(self, id: str) -> Agent:
        """
        Retrieve an agent by ID.
        
        Args:
            id: The external ID of the agent.
            
        Returns:
            Agent: The retrieved agent.
        """
        request = {
            "items": [{"externalId": id}],
            "ignoreUnknownIds": False
        }
        response = self._post("/byids", json=request)
        if not response["items"]:
            raise ValueError(f"Agent with ID {id} not found")
        return Agent(self._cognite_client, response["items"][0])
    
    def delete(self, id: str) -> None:
        """
        Delete an agent.
        
        Args:
            id: The external ID of the agent to delete.
        """
        request = {
            "items": [{"externalId": id}],
            "ignoreUnknownIds": False
        }
        self._post("/delete", json=request) 