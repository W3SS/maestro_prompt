from typing import List
from utcp import Tool
from src.application.tools import MaestroTools
from src.application.tool_schema import DesignAlbumInput, CreateBatchInput, StartBatchInput

def get_utcp_tools() -> List[Tool]:
    """
    Get UTCP compliant tools.
    These can be consumed by any UTCP client or agent.
    """
    
    tools = [
        Tool.from_function(
            func=MaestroTools.design_album,
            name="design_album",
            description="Design a concept album using AI.",
            args_model=DesignAlbumInput
        ),
        Tool.from_function(
            func=MaestroTools.create_batch,
            name="create_batch",
            description="Create a new Suno generation batch.",
            args_model=CreateBatchInput
        ),
        Tool.from_function(
            func=MaestroTools.start_batch,
            name="start_batch",
            description="Start processing a batch.",
            args_model=StartBatchInput
        )
    ]
    return tools
