import asyncio
import json
import time
import re

from typing_extensions import Final
from pyrsistent import m, pmap, PMap
from pymonad.either import Either, Left, Right
from pymonad.promise import Promise
from pymonad.tools import curry
from semantic.common.utils import msg, err, redMsg, greenMsg, to_json_ld_type, resolve_either, reject_promised, reject_either,  instance_count
from semantic.common.common_types import SchemaId, PipeArg
from semantic.api.semantic_client import semanticClient


 


class semantic:

   def __init__(self, brokerIp:str, schemaId:SchemaId, batch_size,topics):

     self.loop = asyncio.get_event_loop()
   
     self.client = semanticClient(self.loop, brokerIp, schemaId, topics)
     '''
          here, circular use of typeMaps allows for future robustness to insertion failure
          (as map is cleared on insertion to buffer the next narration batch)
          requires db insertion handshake id is propogated back and to allow map to be cleared
          circular mechanism works, need handshape. Using one map in circular buffer untill then
     '''
     self.typeMap1: PMap = m()
     #self.typeMap2: PMap = m()
     self.typeMaps = [self.typeMap1]
     self.index: int = 0
     self.number_of_maps = len(self.typeMaps)

     self.query_frame: any = {}
     self.select_frame: any = {}
     self.args: PipeArg = {}

     self.db_acknowledged = True
     self.auto_insert = True
     self.batch_size = batch_size
     self.window_start = time.time()
 
    
   '''
      Narration / Insertion routines
   '''
   
   async def narrate(self, *thunks):
      '''
        preconditions: 
                      type constructors as partial functions, allowing data input from pipe, not just from constructor arguments
                      object exist (type constructor)
                      name is unique for type (type constructor)
                      object matches type (type constructor)
        invariants: 
                      instance dictionary/ordered-map organized by type and name (instance id)
        postconditions:
                      object added to self.typeMap as pmap by type of pmap by unique name
        comment:
                      no db insertion on narrate(), requires insert() to add to db
                      only typeMap and instanceMap are PMaps (of course)
                      instance thunks are plain old objects! (dict)
                      get instanceMap for type, create instanceMap for new types
      '''
      for thunk in thunks:
          self.update_map(thunk, None)
 
      self.db_acknowledged = await self.batch_controller(self.db_acknowledged, self.insert_task)



   async def insert_task(self):
      #if self.scheduler.isScheduled(instance_count(self.typeMaps[self.index])) :
       '''
            insert typeMap in db for current index
       '''
       #greenMsg('insert_task: awaiting insert response ')
       #self.db_acknowledged = False
       result = False
       acknowledge_either = await self.insert()
       acknowledge = acknowledge_either.either(lambda e: f'Error: insert_task: {e}', lambda x: x)

       if acknowledge_either.is_right() and acknowledge == True:
         # greenMsg('insert_task: acknowledge is true ')
    
          #self.last_index = self.index
          '''
            increment self.index
          '''
          #self.index = circular_index(self.index, self.number_of_maps)
          '''
                  clear incremented typeMap to allow for new use with current index
          '''
          self.clear_map()
          #self.db_acknowledged = True
          result = True
          #greenMsg(f'insert_tasks db_acknowledge is {result}')
       else:
          redMsg(f'insert_task: acknowledged false as: {acknowledge}')
          #self.db_acknowledged = False
       return result



   async def insert(self) -> bool:
    '''
      preconditions: 
                     connection to db established (i.e mqtt connection, semantic-service running, valid db running)
                     self.typeMap has been constructed
      invariants: 
                     self.typeMap is successfully inserted into db
      postconditions:
                     self.typeMap in db
                     self.typeMap cleared
                     Either boolean indicating insertion success
    '''

    insert_either: Either  = self.getFlatTypeMap()
    jsonStr: str = insert_either.either(lambda e: f'Error: getFlatTypeMap: {e}', lambda x: x)
    if insert_either.is_right():
       try: 

         response = await self.client.insert(jsonStr)
         
         if response is None :
            return Left(f'insert: response is None')
         else:
            status = response.get('doc')
            ids = status.get('ids')
            if (status.get('@type') == 'InsertStatus' and ids >= 1):
              greenMsg('insert_task:  number of successful inserts: '+str(ids))
              return Right(True)
            else:
               return Left('insert: failed insert')
       except Exception as e:
          return Left(f'insert: Exception: {e}')
    else:
          return insert_either


 

   '''
   todo: refactor so that map_constructor can be used in a chain
   requires
           type constructors return promised eithers
           instanceMap updates (requires back assignment) means that this probably should remain a member function
   
   def map_constructor(self):
    async def map_update(args):
       result: PipeArg = {}
       pipe_either: Either = await args
       obj: dict = pipe_either.either(lambda e: f'Error: select: {e}', lambda x: x())
       
       if obj.is_right():
        
        #    by type key, get or create instanceMap for type : add named object to instanceMap
        
        json_ld_object = to_json_ld_type(obj.either(lambda : {}, lambda x: x))

        msg('update_map( type '+json_ld_object['@type']+' name '+ json_ld_object['name']+')' )
        
        instanceMap: PMap = self.typeMap.get(json_ld_object['@type']) 
        if instanceMap is None: 
          instanceMap = m()
        instanceMap = instanceMap.update({json_ld_object['name']: json_ld_object})
        self.typeMap = self.typeMap.update({json_ld_object['@type']: instanceMap})
  '''

   def update_map(self, obj_thunk, *arg):
      '''
        update_map may be used in a chain, where func returning data, type-constructor-thunk, update_map
      '''
      obj = obj_thunk(arg) if arg is not None else obj_thunk()

      if obj.is_right():
        '''
            by type key, get or create instanceMap for type : add named object to instanceMap
        '''
        json_ld_object = to_json_ld_type(obj.either(lambda : {}, lambda x: x))

        #msg('update_map( type '+json_ld_object['@type']+' name '+ json_ld_object['name']+')' )
        
        instanceMap: PMap = self.typeMaps[self.index].get(json_ld_object['@type']) 
        if instanceMap is None: 
          instanceMap = m()
        instanceMap = instanceMap.update({json_ld_object['name']: json_ld_object})

        #msg(f'update_map instanceMap len {len(instanceMap)}')
        self.typeMaps[self.index] = self.typeMaps[self.index].update({json_ld_object['@type']: instanceMap})
        
  
   def remove_from_map(self, type: str, name: str):
      instanceMap: PMap = self.typeMaps[self.index].get(type) 
      if instanceMap is not None: 
        instanceMap = instanceMap.discard(name)
        self.typeMaps[self.index] = self.typeMaps[self.index].update({type: instanceMap})
      return self
   
  

   def clear_map(self):
     ''' 
        PMap does not support dict's clear() function
        self.typeMap = m() is the most direct load on the gc
        the following is more gentle, is it worse?
      '''
     types = self.typeMaps[self.index].keys()
     for t in types:
        instanceMap: PMap = self.typeMaps[self.index].get(t) 
        if instanceMap is not None: 
          instances = instanceMap.keys()
          for i in instances:
            instanceMap = instanceMap.discard(i)
            self.typeMaps[self.index] = self.typeMaps[self.index].update({type: instanceMap})
        self.typeMaps[self.index] = self.typeMaps[self.index].discard(t)
     return self
   
   


   '''
      Framing / querying | processing routines
   '''
   
   async def chain(self, args, *funcs):
     pipeline = compose(funcs)
     result = await pipeline(args)
     return result
   
   def query_constructor(self):
      
      async def query(args): 
        result: PipeArg = {}

        response_either: Either = await self.client.frame(args)

        if response_either is None :
            return reject_either(f'Error: query with frame {json.dumps(args, indent=6)}')
        elif response_either.is_left():
            return reject_promised(response_either)
        else:
            result['doc'] = response_either.either(lambda e: f'Error: query: {e}', lambda x: x)
            return resolve_either(result)
      
      return query

   def select_constructor(self, frame: any):
        '''
          pre-conditions:
                          frame is json-ld frame for local framing
                          used as with frame argument to define a function instance that is used in chain
          invariant:
                          function return by select is used in chain 
          post-conditions:
                          select returns a function with closure on frame
        '''

        async def selected_frame(args: PipeArg):
              '''
                    pre-conditions:
                                    function instantiated by select with closure on frame outside of chain
                                    used in chain
                                    self.args['doc'] is object in chain to frame
                                    self.args['doc'] is Promised Either
                    invariants:
                                    awaits self.args['doc'] from previous function
                    post-conditions:
                                    self.args['doc'] contains framed version of input
                                    self.args['doc'] is returned as a Promised Either
              '''        
              result: PipeArg = {}

              pipe_either: Either = await args
              piped: dict = pipe_either.either(lambda e: f'Error: select: {e}', lambda x: x['doc'])
              
              if pipe_either.is_left():          
                 return reject_promised(pipe_either)
              else:
                try:
                    selected = {}
                    for key in frame.keys():
                        selected[key] = piped[key]
                    result['doc'] = selected
                    return resolve_either(result) 
                except Exception as e:
                     redMsg(f'Exception in selected_frame: {e}')
                     return reject_either(f'selected_frame: exception: {e}')

            
     
        return selected_frame
   

   '''
   not currently in use
   async def frame(self, seed, *funcs):
        pipeline = compose(funcs)
        result = await pipeline(seed)
        return result
   '''

   

   '''
   primitive methods
   '''

   def getFlatTypeMap(self):
      result: Either
      flat: list = flatPMap(self.typeMaps[self.index])
      
      if flat is None:
          #msg('getFlatTypeMap: typeMap is empty')
          result = Left('typeMap is empty')
      else:
          #msg('getFlatTypeMap: '+json.dumps(flat))
          result = Right( flat )
      return result
   
   def getInsertInstance(self, type: str, name: str):   
      
      #msg('getInsertInstance( type '+type+' name '+ name+')' )
    
      instanceMap: pmap = self.typeMaps[self.index].get(type)
     
      result: Either
      if instanceMap is None:
          result = Left(f'type {type} not found in typeMap')
      else:
         object: dict = instanceMap.get(name)
         if object is None:
          result = Left(f'name {name} not found in typeMap')
         else:
          result = Right(object)
      return result
   
   def typeMapKeys(self):
      return self.typeMaps[self.index].keys()



   async def batch_controller(self, ack, task):
        '''
        async def cleanup_task():
           if count > 0:
              await task()
        '''
        count = instance_count(self.typeMaps[self.index])
        now = time.time()
        elapsed = now - self.window_start
        over_count = count >= self.batch_size 
        #redMsg(f'batch_controller : elapsed: {elapsed} count: {count} ack: {ack} auto: {self.auto_insert}')
        if over_count and  ack == True and self.auto_insert == True:
            greenMsg(f'batch_controller inserting : elapsed: {elapsed} count: {count}')
            self.window_start = now
            result = await task()
        else:
           result = ack
        return result


   def set_auto_insertion(self, setting: bool):
      self.auto_insert = setting

   def set_batch_size(self, max: int):
      self.batch_size = max

   def get_loop(self):
      return self.loop
   
   '''
    end class semantic
   '''
'''
   Primitives
'''

def compose(functions):
     async def composed_function(x):
        result = x
        for func in functions:
            greenMsg('compose: function '+func.__name__)
            result =  await func(result)
        return result
     return composed_function

   

def function_constructor(func):
    async def closure(args):
          result: PipeArg = {}
          pipe_either = await args
          piped =  pipe_either.either(lambda e: f'Error: {func.__name__}: {e}', lambda x: x['doc'])
          if pipe_either.is_left():
              return reject_promised(pipe_either)
          else:
              try:
                  result['doc'] = func(piped)
                  return resolve_either(result)
              except Exception as e:
                  return reject_either(f'Exception {func.__name__}: exception: {e}')
    return closure


def frame_constructor(frame):
  async def frame_in_doc(args):
    args['doc'] = frame
    return args['doc']
  return frame_in_doc


async def flatten(args):
        '''
          pre-conditions:
                          self.args['doc'] is object in chain to flatten
                          self.args['doc'] is Promised Either
       
          post-conditions:
                          flatten returns a Promised Either of an array of self.args['doc'] values
        '''
        result: PipeArg = {}
        pipe_either = await args
        piped =  pipe_either.either(lambda e: f'Error: flattened: {e}', lambda x: x['doc'])
        if pipe_either.is_left():
            return reject_promised(pipe_either)
        else:
            try:
                flattened: list[any] = []
                for predicate in piped.keys():
                    flattened.append(piped[predicate])
                result['doc'] = flattened
                return resolve_either(result)
                #greenMsg('flattened '+json.dumps(flattened, indent=6))
            except Exception as e:
                return reject_either(f'flatten: exception: {e}')
      
        
'''
    Utilities

'''
def pmapToDict(pm):
  '''
    convert nested PMaps to nested dicts
    stop when object is not PMap
  '''
  mapped: dict = {}
  if not isinstance(pm, PMap):
    return pm
  else:
    typeMap = pm.keys()
    for t in typeMap:
      mapped[t] = pmapToDict(pm[t])
    msg('mapped '+json.dumps(mapped, indent=6))
    return mapped

def flatPMap(pm):
  '''
    convert nested PMaps to a flat array
    stop when object is not PMap
  '''
  flat: list = []
  typeKeys = pm.keys()
  for t in typeKeys:
    instanceMap: dict = pm.get(t)
    instanceKeys = instanceMap.keys()
    for n in instanceKeys:
      #msg('flatPMap '+t+' '+n)
      obj: dict = instanceMap.get(n)
      if isinstance(obj, PMap):
        err('obj is PMap for '+t+' '+n)
      flat.append(obj)
  #msg('flat: '+json.dumps(flat))
  return flat

