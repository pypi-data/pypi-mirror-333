import logging
import random

from simpleCan.util import dataStructure as ds, can_func, dbcReader
from simpleCan.util.task import SendMessageTask, RecvMessageTask
from simpleCan.util.messageList import MessageList

__all__ = ['SimpleCan']

__author__ = 'Jiajie Liu'


class SimpleCan:

    def __init__(self, dbcPath=None):
        # create a list to store all messages sending to DDU
        self.tasklist = []
        self.messageList = MessageList()
        if dbcPath is not None:
            self.dbcReader = dbcReader.DBCReader(dbcPath=dbcPath)
        can_func.setup()

    def env_run(self, duration=360):
        self.messageList.clearMessageList()
        self.messageList.load_default_messageList()
        messageList = self.messageList.get_messageList()
        self.clearTaskList()
        for i in range(len(messageList)):
            self.tasklist.append(SendMessageTask(message_id=messageList[i].id,
                                                 data=messageList[i].data,
                                                 period=messageList[i].period,
                                                 duration=duration))
        for task in self.tasklist:
            task.task_run()
    def sendMessage(self, message_id, data, period, duration=30):
        task = SendMessageTask(message_id=message_id,
                               data=data,
                               period=period,
                               duration=duration)
        self.tasklist.append(task)
        task.task_run()

    def modifyMessage(self, message_id, data):
        try:
            for task in self.tasklist:
                if task.get_messageID() == message_id:
                    logging.critical(task.get_messageID())
                    task.task_modifyData(newData=data)

        except Exception as e:
            logging.error(e)

    def stopMessage(self, message_id):
        try:
            for task in self.tasklist:
                if task.get_messageID() == message_id:
                    task.task_stop()
        except Exception as e:
            logging.error(e)

    def recvTargetMessage(self, messageId, offset=0, duration=10) -> ds.ReceivedCanMessage:
        return RecvMessageTask.recvTargetMessage(message_id=messageId, offset=offset, duration=duration)

    def recvMessage(self)->ds.ReceivedCanMessage:
        return RecvMessageTask.recvMessage()

    def clearTaskList(self):
        self.tasklist = []

    def endAllTasks(self):
        for task in self.tasklist:
            task.task_stop()

    def __del__(self):
        self.endAllTasks()
        can_func.teardown()


    ## DBC related functionalities

    def updateDBC(self, dbcPath):
        self.dbcReader = dbcReader.DBCReader(dbcPath=dbcPath)

    def sendAllMessagesFromDBC(self, duration=30):
        canTxMessageList = self.dbcReader.getcanTxMessageList()
        for canMessage in canTxMessageList:
            self.sendMessage(message_id=canMessage.id, period=canMessage.period, data=canMessage.data,
                             duration=duration)

    def sendAllMessagesFromDBCrdValue(self, period_minimum=10, period_maximum=1000, duration=30):
        canTxMessageList = self.dbcReader.getcanTxMessageList()
        for canMessage in canTxMessageList:
            self.sendMessage(message_id=canMessage.id, period=random.randint(period_minimum, period_maximum) / 1000,
                             data=[random.randint(0, 255), random.randint(0, 255), random.randint(0, 255),
                                   random.randint(0, 255), random.randint(0, 255), random.randint(0, 255),
                                   random.randint(0, 255),
                                   random.randint(0, 255)], duration=duration)

    def sendMessageDBC(self, messageName, duration=30, **kwargs):
        canMessage = self.dbcReader.generateCanMessage(message=messageName, duration=duration, **kwargs)
        self.sendMessage(message_id=canMessage.id, data=canMessage.data, period=canMessage.period, duration=duration)
    def recvTargetMessageDBC(self, messageName, offset = 0, duration = 10)-> ds.ReceivedCanMessageDecode:
        try:
            messageId = self.dbcReader.getMessageIdByName(messageName)
            recvMessage = self.recvTargetMessage(messageId = messageId, offset = offset, duration = duration)
            return self.dbcReader.decodeCanMessage(message_id=recvMessage.getMessageID(), data=recvMessage.data)
        except Exception as e:
            logging.error(e)

    def recvMessageDBC(self)->ds.ReceivedCanMessageDecode:
        try:
            recvMessage = self.recvMessage()
            return self.dbcReader.decodeCanMessage(message_id=recvMessage.getMessageID(), data=recvMessage.data)
        except Exception as e:
            logging.error(e)


