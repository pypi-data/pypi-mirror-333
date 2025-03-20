from jsonrpcserver import method
from pydantic import BaseModel

from inspect_tool_support._remote_tools._bash_session.controller import (
    BashSessionController,
)
from inspect_tool_support._remote_tools._bash_session.tool_types import (
    BashCommandResult,
    BashParams,
    BashRestartResult,
    CommandParams,
    NewSessionResult,
    RestartParams,
)
from inspect_tool_support._util._json_rpc_helpers import (
    with_validated_rpc_method_params,
)

controller = BashSessionController()


@method
async def bash_session_new_session(**params: object) -> object:
    return await with_validated_rpc_method_params(
        BaseModel, _bash_new_session, **params
    )


@method
async def bash_session(**params: object) -> object:
    return await with_validated_rpc_method_params(BashParams, _bash_session, **params)


async def _bash_new_session(_: BaseModel) -> NewSessionResult:
    return NewSessionResult(session_name=await controller.new_session())


async def _bash_session(params: BashParams) -> BashCommandResult | BashRestartResult:
    match params.root:
        case CommandParams(session_name=session_name, command=command):
            return await controller.execute_command(session_name, command)
        case RestartParams(session_name=session_name):
            return await controller.restart(session_name)
