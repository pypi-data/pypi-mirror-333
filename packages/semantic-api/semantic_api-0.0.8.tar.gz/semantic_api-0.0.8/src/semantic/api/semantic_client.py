import asyncio
import threading
import json
import re
from pymonad.either import Either, Left, Right
from typing_extensions import Final

from semantic.common.utils import msg, err, greenMsg, redMsg, custom_encoder
from semantic.common.common_types import PipeArg, SemanticConfig, SchemaId

from semantic.api.config   import port, username, password, semanticConfigTopic, serviceRequestTopic, insertAcknowledgeTopic
from semantic.py_mqtt.py_mqtt import MQTTClient


class semanticClient:

  def __init__(self, loop, brokerIp: str, schemaId: SchemaId, topics):
     self.loop = loop
     self.brokerIp = brokerIp
     self.mqtt = MQTTClient( loop, brokerIp, port, username, password, topics )
     
     '''
        schmaDef state ultimately maintained on semantic server, state default is locally maintained in config.py
     '''
     self.schemaId = schemaId
  

  
  async def insert(self, doc: str):
      '''
      frame = {
        '@type': 'InsertStatus',
        'status': 'requested'
      }
      '''
  
      pipe_args: PipeArg = {
          "schema": self.schemaId,
          "topic": serviceRequestTopic,
          "doc": doc,
          "frame": None
      }

      #redMsg('insert args '+json.dumps(pipe_args, indent=6))
      result = {}
      try:
        result = await self.insert_primitive(pipe_args)
      except Exception as e:
          txt = f'semantic_client: insert : Exception: {e}'
          redMsg(txt)
          
      return result
  

  async def frame(self, frame: str):
      pipe_args: PipeArg = {
          "schema": self.schemaId,
          "topic": serviceRequestTopic,
          "doc": None,
          "frame": frame 
      }
      response = None
      try:
         response =  await self.query_primitive(pipe_args)
      except Exception as e:
          txt = f'semantic_client: frame : Exception: {e}'
          redMsg(txt)
          return Left(txt)

      if response is None:
        return Left(f'error on query forframe {json.dumps(frame, indent=6)}')
      else:
        return Right(response.get('doc'))


  async def insert_primitive(self, args: PipeArg):
      stringified= json.dumps(args)
      
      #query_result = self.mqtt.publish(args.get('topic'), stringified)
      query_result = {}
      try:
       query_result = await asyncio.wrap_future(asyncio.run_coroutine_threadsafe(self.mqtt.publish_with_response(args.get('topic'), stringified), self.loop))
      except Exception as e:
          txt = f'semantic_client: insert_primitive : Exception: {e}'
          redMsg(txt)
    

      #greenMsg('insert_primitive result: '+str(query_result))
     
      return query_result
     
  async def query_primitive(self, args: PipeArg):
      stringified= json.dumps(args)
      msg('query_primitive args: '+stringified)
      
      query_result = {}
      try:
          redMsg('awaiting call ---------------------------------------------------------------------')
          query_result = await asyncio.wrap_future(asyncio.run_coroutine_threadsafe(self.mqtt.publish_with_response(args.get('topic'), stringified), self.loop))
           #query_result = await self.mqtt.publish_with_response(args.get('topic'), stringified)
      except Exception as e:
          txt = f'semantic_client: query_primitive : Exception: {e}'
          redMsg(txt)
      
      #greenMsg('query response: '+json.dumps(query_result, indent=6))
     
      return query_result
  

  async def semantic_config(self, command: str, args: any):
      msg('semantic_config : '+command)
      body: SemanticConfig = {
          "@type": "sc:SemanticConfig",
          "dispatch": command,
          "args": args
        }
      
     
      pipe_args: PipeArg = {
          "schema": self.schemaId,
          "topic": semanticConfigTopic,
          "doc": body,
          "frame": None 
        }
      redMsg('semantic_config pipe_args: '+json.dumps(pipe_args, indent=6))
      return await self.query_primitive(pipe_args)

  
  async def getSchemaId(self):
    #msg('getSchemaId()')
    #result = self.loop.run_until_complete(self.semantic_config('getSchemaId', None))
    result = await self.semantic_config('getSchemaIdInUse', None)
    greenMsg('getSchemaId: '+json.dumps(result, indent=6))
    return result.get('doc')
  
  async def setSchemaId(self, args: SchemaId):
    #msg('setSchemaId()')
    #result = self.loop.run_until_complete(self.semantic_config('setSchemaId', args))
    result = await self.semantic_config('setCurrentSchemaId', args)
    greenMsg('setSchemaId: '+json.dumps(result, indent=6))
    return result.get('doc')


  def listDbs():
     pass
     

  def listTypeNamesForSchema():
     pass
  def listClusterNamesForSchema():
     pass
  def listSupportedSchemas():
     pass


  def createDbForSchemaId():
    pass

  def schemaQuery():
     pass

  def queryStar():
     pass
  def getSchema():
     pass

  def getSchemaInDb():
     pass
  
  



'''

  def graphSchema', (obj) => {
    typeMap.setMap({});
    const dotForSchema = graphSchema(typeMap);
    return Promise.resolve({
      doc: dotForSchema(schemaContext.getContext().schemaName, schemaContext.getContext().schemaVersion, obj.doc.args, framing, include, edgeLabel),
      topic: obj.topic,
      mqttClient: obj.mqttClient
    })}),    
  def include', (obj) => { 
    include = (obj.doc.args == 'true');
    return Promise.resolve({
      doc: include,
      topic: obj.topic,
      mqttClient: obj.mqttClient
    })}),    
  def framing', (obj) => { 
      framing = (obj.doc.args == 'true');
      return Promise.resolve({
        doc: framing,
        topic: obj.topic,
        mqttClient: obj.mqttClient
      })}),  
  def edgeLabel', (obj) => { 
        edgeLabel = (obj.doc.args == 'true');
        return Promise.resolve({
          doc: edgeLabel,
          topic: obj.topic,
          mqttClient: obj

          '''