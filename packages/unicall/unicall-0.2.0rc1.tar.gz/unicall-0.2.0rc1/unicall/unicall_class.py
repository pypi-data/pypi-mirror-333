import logging
import typing as t

import imy.async_utils

from . import base_transport, data_models, errors

_logger = logging.getLogger(__name__)


class Unicall:
    """
    Base class for all RPC interfaces.

    Unicall is a base class for all interfaces that you want to expose to the
    outside world. It acts as a registry of functions that can be called either
    by you (@remote), or by a remote client (@local).
    """

    # Maps function names of all @local functions to function objects. The name
    # (key) is the name as would be seen by a remote client. The function object
    # contains already parsed metadata about the function. The callable is the
    # actual method to call.
    #
    # This value must be separate for each class. Thus, it is never actually
    # initialized here, but rather by `__init_subclass__`.
    _local_methods_: dict[str, tuple[data_models.FunctionMetadata, t.Callable]]

    # Maps function names of all @remote functions to function objects. The name
    # (key) is the name as would be seen by a remote client.
    _remote_methods_: dict[str, data_models.FunctionMetadata]

    def __init__(
        self,
        *,
        transport: base_transport.Transport,
    ) -> None:
        self._transport = transport

    def __init_subclass__(cls) -> None:
        # Initialize per-class attributes. These mustn't be inherited, but
        # rather be local to each class.
        cls._local_methods_ = {}
        cls._remote_methods_ = {}

        # Find all methods annotated with @local and register them
        for member in vars(cls).values():
            # Local method?
            try:
                function_meta = member._unicall_local_
            except AttributeError:
                pass
            else:
                assert callable(member), member
                cls._local_methods_[function_meta.name] = (function_meta, member)

            # Remote method?
            try:
                function_meta = member._unicall_remote_
            except AttributeError:
                pass
            else:
                assert callable(member), member
                cls._remote_methods_[function_meta.name] = function_meta

    async def _handle_single_request(
        self,
        python_function,
        arguments: list[t.Any],
        success_callback: t.Callable[[t.Any], t.Awaitable[None]],
        error_callback: t.Callable[[Exception], t.Awaitable[None]],
    ) -> None:
        """
        Processes a single request to run a local function, responding as
        needed.
        """

        # Call the function
        try:
            result = await python_function(self, *arguments)
        except Exception as error:
            await error_callback(error)
            return

        # Woo-hoo!
        await success_callback(result)

    async def serve(self) -> None:
        """
        Starts the RPC server.

        This method makes the server start listen for incoming requests and
        handles them. The function will never return - cancel it using `asyncio`
        mechanisms if you need it to stop early.
        """

        async with imy.async_utils.TaskGroup() as tasks:
            while True:
                # Requests can fail. Don't die if that happens
                try:
                    # Get a request
                    (
                        function_meta,
                        python_function,
                        arguments,
                        success_callback,
                        error_callback,
                    ) = await self._transport.listen_for_request(self)

                    # Handle the request. Do that in a separate task so that
                    # multiple requests can be handled in parallel.
                    tasks.create_task(
                        self._handle_single_request(
                            python_function,
                            arguments,
                            success_callback,
                            error_callback,
                        ),
                        name=f"Request handler for function `{function_meta.name}`",
                    )

                # Log errors but don't give up
                except errors.RpcError:
                    _logger.exception("Error in RPC request:")
