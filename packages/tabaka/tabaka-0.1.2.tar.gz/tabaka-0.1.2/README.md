

## Usage 


### MCP Server (stdio)

```
uv run tabaka-mcp/tabaka.py run --mode stdio
```

### MCP Server (sse)

```
uv run tabaka-mcp/tabaka.py run --mode=sse
```

### Using as Library

```python

if __name__ == "__main__":
    container_name_prefix = "tabaka-sandbox-test-"
    sandbox = Tabaka(
        config=TabakaConfig(allowed_languages=["python", "go"])
    )  

    result = sandbox.execute_code(
        """import time\nprint("Hello, World!")\nprint("Hello, World!")\nprint(5*9*44+4)""",
        language_id="python",
        timeout=5,
    )
    print(result)



    result = sandbox.execute_code(
        """
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

print(np.random.randint(1, 100))
print(np.__version__)
print(pd.__version__)
    """,
        language_id="python",
        timeout=10,
        required_packages=["pandas", "numpy", "matplotlib"],
    )
    print("\nResult:\n", result)

    # Cleanup the sandbox
    sandbox.cleanup()
```