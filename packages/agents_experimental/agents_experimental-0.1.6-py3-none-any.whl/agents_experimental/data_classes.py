from dataclasses import dataclass, field
from typing import Dict, List, Optional, Any, Union


@dataclass
class DataModel:
    """
    Represents a data model for query generation.
    """
    space: str
    external_id: str
    version: str
    views: Optional[List[str]] = None
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary representation for API calls."""
        result = {
            "space": self.space,
            "externalId": self.external_id,
            "version": self.version
        }
        if self.views:
            result["views"] = self.views
        return result


@dataclass
class Tool:
    """
    Base class for agent tools.
    """
    type: str
    name: str
    external_id: str
    description: Optional[str] = None
    configuration: Optional[Dict[str, Any]] = None
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary representation for API calls."""
        result = {
            "type": self.type,
            "name": self.name,
            "externalId": self.external_id
        }
        if self.description:
            result["description"] = self.description
        if self.configuration:
            result["configuration"] = self.configuration
        return result


class QueryDataModelTool(Tool):
    """
    Tool for querying data models using natural language.
    """
    def __init__(self, name: str, external_id: str, data_models: List[DataModel], instructions: Optional[str] = None):
        """
        Initialize a QueryDataModelTool.
        
        Args:
            name: The name of the tool.
            external_id: The external ID of the tool.
            data_models: The data models to use for query generation.
            instructions: Optional instructions for the tool.
        """
        super().__init__(
            type="queryDataModel",
            name=name,
            external_id=external_id,
            description=None  # Description is not used for QueryDataModelTool
        )
        self.data_models = data_models
        self.instructions = instructions
        self.configuration = {
            "dataModels": [model.to_dict() for model in self.data_models]
        }
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary representation for API calls."""
        # This format matches the QueryDataModelToolDTO in the OpenAPI spec
        result = {
            "type": self.type,
            "name": self.name,
            "externalId": self.external_id,
            "configuration": self.configuration
        }
        if self.instructions:
            result["instructions"] = self.instructions
        return result


@dataclass
class AgentDefinition:
    """
    Definition for creating or updating an agent.
    """
    external_id: str
    name: str
    tools: List[Tool] = field(default_factory=list)
    description: Optional[str] = None
    instructions: Optional[str] = None
    model: Optional[str] = None
    labels: Optional[List[str]] = None
    example_questions: Optional[List[Dict[str, Any]]] = None
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary representation for API calls."""
        result = {
            "externalId": self.external_id,
            "name": self.name,
            "tools": [tool.to_dict() for tool in self.tools]
        }
        if self.description:
            result["description"] = self.description
        if self.instructions:
            result["instructions"] = self.instructions
        if self.model:
            result["model"] = self.model
        if self.labels:
            result["labels"] = self.labels
        if self.example_questions:
            result["exampleQuestions"] = self.example_questions
        return result


@dataclass
class ToolCall:
    """
    Represents a tool call from an agent.
    """
    id: str
    name: str
    arguments: Dict[str, Any]
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "ToolCall":
        """Create a ToolCall from a dictionary."""
        return cls(
            id=data.get("id", ""),
            name=data.get("name", ""),
            arguments=data.get("arguments", {})
        )


@dataclass
class Reasoning:
    """
    Represents a reasoning step from an agent.
    """
    type: str
    content: Optional[str] = None
    tool_call: Optional[Dict[str, Any]] = None
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Reasoning":
        """Create a Reasoning from a dictionary."""
        return cls(
            type=data.get("type", ""),
            content=data.get("content"),
            tool_call=data.get("toolCall")
        )


@dataclass
class Attachment:
    """
    Represents an attachment in an agent message.
    """
    type: str
    instances: Optional[Dict[str, Any]] = None
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Attachment":
        """Create an Attachment from a dictionary."""
        return cls(
            type=data.get("type", ""),
            instances=data.get("instances")
        )


@dataclass
class AgentMessage:
    """
    Represents a message from an agent.
    """
    id: str
    message: str
    role: str
    tool_calls: List[ToolCall] = field(default_factory=list)
    reasoning: List[Reasoning] = field(default_factory=list)
    attachments: List[Attachment] = field(default_factory=list)
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "AgentMessage":
        """Create an AgentMessage from a dictionary."""
        content_data = data.get("content", {})
        message = content_data.get("text", "") if isinstance(content_data, dict) else ""
        
        # Process tool calls
        tool_calls = []
        if "clientToolCalls" in data:
            for tool_call_data in data.get("clientToolCalls", []):
                tool_calls.append(ToolCall.from_dict(tool_call_data))
        
        # Process reasoning
        reasoning = []
        if "reasoning" in data:
            for reasoning_data in data.get("reasoning", []):
                reasoning.append(Reasoning.from_dict(reasoning_data))
        
        # Process attachments
        attachments = []
        if "attachments" in data:
            for attachment_data in data.get("attachments", []):
                attachments.append(Attachment.from_dict(attachment_data))
        
        return cls(
            id=data.get("id", ""),
            message=message,
            role=data.get("role", ""),
            tool_calls=tool_calls,
            reasoning=reasoning,
            attachments=attachments
        ) 