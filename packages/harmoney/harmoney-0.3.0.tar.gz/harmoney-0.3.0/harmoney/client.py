import asyncio
from ._callSpec import _CallPacket
import pickle as pkl
from websockets.asyncio import client as WSC

__all__ = ["Client"]

class Client:
    def __init__(self, host, port) -> None:
        self._wsURL = f"ws://{host}:{port}/cliReq/"
        self.tasks = []

    def singleCall(self, function, **kwargs):
        """
        Performs single call with the provided function and args
        """
        self.addCall(_CallPacket(procedure=function, data=kwargs))
        return self.runAllCalls()[0]

    def addCall(self, function, **kwargs):
        """
        Adds a task to call queue.
        """
        self.tasks.append((_CallPacket(procedure=function, data=kwargs)))

    async def _runAllCalls(self, callDelay=0.01):
        """
        Logic function to communicate with the router.
        """
        print(f"Total Calls: {len(self.tasks)}")
        async with WSC.connect(self._wsURL+f"{len(self.tasks)}", open_timeout=None, ping_interval=10, ping_timeout=None) as ws:
            ackCount = int(await ws.recv())
            assert ackCount == len(self.tasks), "Comms not proper..."
            await ws.send(pkl.dumps(self.tasks))
            returnData = await ws.recv()
            returnData = pkl.loads(returnData)
            self.tasks=[]
            return returnData

    def runAllCalls(self, callDelay=0.01):
        """
        User facing function to remotely execute queued tasks.
        """
        return asyncio.run(self._runAllCalls(callDelay=callDelay))
