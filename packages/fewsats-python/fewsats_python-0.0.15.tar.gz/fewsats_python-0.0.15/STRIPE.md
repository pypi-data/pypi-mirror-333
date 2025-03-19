# Stripe Agent Toolkit Analysis & Design Document

## Overview
Analyzed Stripe's approach to exposing their API as tools for AI agents. Their implementation provides a framework-agnostic core with specific adapters for different frameworks in both Python and TypeScript.

## Current Architecture

### Core Components
1. **Base Tool Definitions** (`tools.py`/`tools.ts`)
   - Framework-agnostic list of dictionaries
   - Python version:
     ```python
     {
         "method": str,          # Internal method name
         "name": str,           # Human-readable name
         "description": str,    # Detailed documentation
         "args_schema": PydanticModel,  # Input validation
         "actions": dict        # Permissions system
     }
     ```
   - TypeScript version:
     ```typescript
     {
         method: string,
         description: string,
         parameters: z.object({  // Using Zod for validation
           name: z.string(),
           email: z.string().optional()
         })
     }
     ```

2. **API Wrapper** (`api.py`/`api.ts`)
   - Core class handling API interactions
   - Python uses Pydantic, TypeScript uses Zod
   - Method routing via string identifiers
   - Example:
    ```python
    class StripeAPI(BaseModel):
    """ "Wrapper for Stripe API"""
    ...
        def run(self, method: str, *args, **kwargs) -> str:
            if method == "create_customer":
                return json.dumps(create_customer(self._context, *args, **kwargs))
            elif method == "list_customers":
                return json.dumps(list_customers(self._context, *args, **kwargs))
    ...
    ```

3. **Framework Adapters**
   - Python supports:
     - LangChain (`langchain/toolkit.py`)
     - CrewAI (`crewai/toolkit.py`)
   - TypeScript supports:
     - LangChain (`langchain/toolkit.ts`)
     - Vercel AI SDK (`ai-sdk/toolkit.ts`)
   - Each adapter converts core tools to framework-specific format

### Directory Structure
```
stripe_agent_toolkit/
├── shared/          # Framework-agnostic core (TS)
│   ├── api.ts
│   ├── configuration.ts
│   └── tools.ts
├── api.py          # Core API wrapper (Python)
├── configuration.py # Config & permissions
├── schema.py       # Pydantic models
├── tools.py        # Tool definitions
├── prompts.py      # Tool documentation
└── frameworks/     # Framework-specific implementations
    ├── crewai/     # Python only
    ├── langchain/  # Both Python & TS
    └── ai-sdk/     # TypeScript only
```

## Key Design Decisions

1. **Framework Agnostic Core**
   - Tools defined in standard format
   - No dependency on specific AI frameworks
   - Clean separation between API logic and tool interfaces

2. **Type Safety**
   - Python: Pydantic models
   - TypeScript: Zod schemas
   - Runtime type checking in both

3. **Language-Specific Features**
   - TypeScript: 
     - Strict typing
     - Vercel AI SDK support
     - Built-in metering/billing functionality
   - Python:
     - CrewAI integration
     - More extensive validation via Pydantic

