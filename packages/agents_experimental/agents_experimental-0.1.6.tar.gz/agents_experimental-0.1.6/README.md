# Experimental agents SDK
> :warning: **Warning**: This is an untested experimental SDK. Breaking changes will happen regularly without notice. No guarantees for stability!

A Python SDK for interacting with Atlas AI agents.

## Installation

```bash
pip install agents_experimental
```

## Usage

### Authentication

First, authenticate with Cognite Data Fusion using the CogniteClient:

```python
from cognite.client import CogniteClient
from agents_experimental import AIClient

# Create a CogniteClient with your preferred authentication method
client = CogniteClient()

# Create an AIClient using the CogniteClient
ai = AIClient(client)
```

### Agents

#### List Agents

```python
# List all agents (up to the specified limit)
agents = ai.agents.list(limit=10)
for agent in agents:
    print(f"Agent: {agent.name} (ID: {agent.id})")
```

#### Create or Update an Agent

```python
from agents_experimental import AgentDefinition, DataModel, QueryDataModelTool

# Define a data model for the query tool
data_model = DataModel(
    space="cdf_idm",
    external_id="CogniteProcessIndustries",
    version="v1",
    views=["CogniteAsset", "CogniteMaintenanceOrder"]
)

# Define an agent using dataclasses
agent_def = AgentDefinition(
    external_id="my-agent",
    name="My Agent",
    description="A helpful agent",
    instructions="You are a helpful assistant that provides information about assets and maintenance orders.",
    model="gpt-4o",  # Optional: specify the model to use
    labels=["assets", "maintenance"],  # Optional: add labels for categorization
    example_questions=[  # Optional: provide example questions
        {"text": "Show me the top 5 assets by criticality"},
        {"text": "What maintenance orders are due this week?"}
    ],
    tools=[
        # QueryDataModelTool for querying data models
        QueryDataModelTool(
            name="query asset and maintenance order data",
            external_id="my-query-data-model-tool",
            data_models=[data_model],
            instructions="Use this tool to query asset and maintenance data"
        )
    ]
)

# Create or update the agent
agent = ai.agents.create(agent_def)
print(f"Created/updated agent: {agent.name} (ID: {agent.id})")
```

#### Retrieve an Agent

```python
# Retrieve an agent by ID
agent = ai.agents.retrieve(id="my-agent")
print(f"Retrieved agent: {agent.name} (ID: {agent.id})")
```

#### Delete an Agent

```python
# Delete an agent by ID
ai.agents.delete(id="my-agent")
print("Agent deleted")
```

#### Chat with an Agent

```python
# Retrieve an agent
agent = ai.agents.retrieve(id="my-agent")

# Start a chat session with the agent
session = agent.start_session()

# Chat with the agent
print("\nUser: What's the status of asset 123?")
response = session.chat(message="What's the status of asset 123?")

# Print reasoning and attachments
print(f"\nReasoning: {response.reasoning}")
print(f"\nAttachments: {response.attachments}")

# Access the agent's response message
print(f"\nAgent: {response.message}")


# Continue the conversation
print("\nUser: Are there any maintenance orders for this asset?")
response = session.chat(message="Are there any maintenance orders for this asset?")
print(f"\nAgent: {response.message}")
```

#### Chat with Client-Side Tools

> :warning: **Warning**: Not yet verified (or even tried)

```python
# Define a custom tool function
def calculate_average(values: str):
    """
    Calculate the average of a comma-separated list of numbers.
    
    Args:
        values (str): Comma-separated list of numbers
    
    Returns:
        float: The average value
    """
    numbers = [float(x.strip()) for x in values.split(",")]
    return sum(numbers) / len(numbers)

# Retrieve an agent
agent = ai.agents.retrieve(id="my-agent")

# Start a chat session with the agent and register client-side tools
session = agent.start_session(
    client_tools=[calculate_average],
    run_python=True  # Automatically execute client-side tool calls
)

# Chat with the agent
print("\nUser: Calculate the average of 10, 20, 30, 40, 50")
response = session.chat(message="Calculate the average of 10, 20, 30, 40, 50")

# Print any tool calls
if response.tool_calls:
    print(f"\nTool calls ({len(response.tool_calls)}):")
    for tool_call in response.tool_calls:
        print(f"  - {tool_call.name}: {tool_call.arguments}")

print(f"\nAgent: {response.message}")
```
