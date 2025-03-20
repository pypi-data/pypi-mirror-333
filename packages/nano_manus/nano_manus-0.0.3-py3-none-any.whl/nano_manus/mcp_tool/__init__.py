import os
import json
from ..env import CONFIG, CONSOLE
from .official import MCPOfficial
from .pool import MCPPool


TOOLS = MCPPool()

if os.getenv("BRAVE_API_KEY"):
    TOOLS.add_mcp_client(
        "search_web",
        MCPOfficial.from_docker(
            "mcp/brave-search",
            volume_mounts=[
                "-e",
                f"BRAVE_API_KEY={os.getenv('BRAVE_API_KEY')}",
            ],
        ),
    )
else:
    CONSOLE.print(
        "[red][Warning] BRAVE_API_KEY is not set, search_web tool will not be available[/red]"
    )

if os.getenv("JINA_API_KEY"):
    TOOLS.add_mcp_client(
        "read_webpage",
        MCPOfficial.from_smithery(
            "jina-ai-mcp-server",
            suffix_args=[
                "--config",
                json.dumps(
                    {
                        "jinaApiKey": os.getenv("JINA_API_KEY"),
                    }
                ),
            ],
        ),
    )
else:
    CONSOLE.print(
        "[red][Warning] JINA_API_KEY is not set, jina tool will not be available[/red]"
    )
# if os.getenv("OPENROUTER_API_KEY"):
#     TOOLS.add_mcp_client(
#         "browser",
#         MCPOfficial.from_smithery(
#             "@Deploya-labs/mcp-browser-use",
#             suffix_args=[
#                 "--config",
#                 json.dumps(
#                     {
#                         "OPENROUTER_API_KEY": os.getenv("OPENROUTER_API_KEY"),
#                     }
#                 ),
#             ],
#         ),
#     )
# else:
#     CONSOLE.print(
#         "[red][Warning] OPENROUTER_API_KEY is not set, broswer tool will not be available[/red]"
#     )

TOOLS.add_mcp_client(
    "terminal",
    MCPOfficial.from_smithery(
        "@wonderwhy-er/desktop-commander",
        suffix_args=[
            "--config",
            "{}",
        ],
    ),
)
