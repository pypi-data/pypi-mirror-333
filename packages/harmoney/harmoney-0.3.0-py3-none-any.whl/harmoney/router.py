import asyncio
import base64
from threading import Thread
from typing import List
from uvicorn import Config, Server
import fastapi
from uvicorn.config import LOG_LEVELS
import pickle as pkl
import uuid
from ._callSpec import  _ClientPacket, _CallPacket

__all__ = ["startRouter"]

class _Router:
    def __init__(self, pollingDelay=0.5) -> None:
        self.router = fastapi.APIRouter()
        self.router.add_api_websocket_route("/reg", self.registerRunner)
        self.router.add_api_websocket_route("/cliReq/{count}", self.multiClientRequest)
        self.taskQueue = asyncio.Queue()
        self.runnerCount=0
        self.returnDict = {}
        self.doneDict = {}
        self.pollingDelay = pollingDelay

    async def registerRunner(self,  wsConnection: fastapi.WebSocket):
        """
        Method which queries an available task and sends the data to the attached runner.
        """
        await wsConnection.accept()
        await wsConnection.send_text(str(self.runnerCount))
        methods=await wsConnection.receive()
        methods = pkl.loads(base64.b64decode(methods["text"]))
        print(f"Runner Connected with ID: {self.runnerCount}, Methods: {methods['methods']}")
        runnerID=self.runnerCount
        self.runnerCount+=1
        runnerCounter = 0
        while True:
            reqID, data  = await self.taskQueue.get()
            runnerCounter+=1
            print(f"Runr {runnerID} Counter: {runnerCounter}")
            await wsConnection.send_bytes(pkl.dumps(data))
            retValue = await wsConnection.receive()
            self.returnDict[reqID] = pkl.loads(base64.b64decode(retValue["bytes"]))

    async def clientRequest(self, data:_ClientPacket):
        """
        Method to handle single request, adds the task to queue and awaits for result.
        To be deprecated for better task handling.
        """
        reqID = uuid.uuid4().hex
        callPacket = data
        await self.taskQueue.put((reqID, callPacket))
        while reqID not in self.returnDict:
            await asyncio.sleep(self.pollingDelay)
        returnValue = self.returnDict[reqID]
        self.returnDict.pop(reqID)
        return returnValue

    async def multiClientRequest(self, wsConn:fastapi.WebSocket, count:int):
        """
        Method accepts a task list and adds them to the queue.
        Returns the results to client.
        """
        await wsConn.accept()
        softLimit=50
        await wsConn.send_text(str(count))
        reqID = uuid.uuid4().hex
        self.returnDict[reqID] = [0]*count
        self.doneDict[reqID] = [0]*count
        print(f"Received {count} tasks")
        taskBytes = await wsConn.receive_bytes()
        taskPackets = pkl.loads(taskBytes)
        softLimitItr = 0
        for task in range(len(taskPackets)):
            while (task > (softLimitItr+softLimit)) and not self.doneDict[reqID][softLimitItr]==1:
                await asyncio.sleep(1)
            if self.doneDict[reqID][softLimitItr]==1:
                softLimitItr+=1
            t=Thread(target=self._worker, args=(reqID, task, taskPackets[task]))
            t.daemon=True
            t.start()
        while not all(self.doneDict[reqID]):
            await asyncio.sleep(1)
        await wsConn.send_bytes(pkl.dumps(self.returnDict[reqID]))
        self.returnDict.pop(reqID)

    def _worker(self, id, idx, data:_ClientPacket):
        """
        Thread worker to handle one task.
        To be depricated for better task handling.
        """
        retVal = asyncio.run(self.clientRequest(data))
        self.returnDict[id][idx]=retVal
        self.doneDict[id][idx]=1
        return

def startRouter(host, port, pollingDelay=0.1, logLevel=3):
    """
    Main function to start the router system.
    """
    br = _Router(pollingDelay=pollingDelay)
    app = fastapi.FastAPI()
    app.include_router(br.router)
    level = list(LOG_LEVELS.keys())[logLevel]
    serverConf = Config(app = app, host=host,  port=port, log_level=LOG_LEVELS[level], ws_ping_interval=10, ws_ping_timeout=None, ws_max_size=1024*1024*1024)
    server = Server(config=serverConf)
    server.run()
