
'''
    TODO: remove these functions from map_utils.py and update client's imports
'''
import os
import sys
import time
import datetime
import base64
import asyncio
from functools import reduce
import json
from pymonad.promise import Promise
from pymonad.either import Left, Right
from pyrsistent import PMap

from urllib.parse import unquote
from semantic_api.common.src.common_types import SchemaId


def typeName(elem):
    return type(elem).__name__

def err(msg):
    sys.stderr.write(msg + '\n')

def sort_by_instance(item):
    return len(item['@type']) + len(item['name'])

def redMsg(msg): 
    sys.stdout.write("\033[91m {}\033[00m" .format(msg) + '\n')
def greenMsg(msg): 
    sys.stdout.write("\033[92m {}\033[00m" .format(msg) + '\n')

def msg(msg):
    sys.stdout.write(msg + '\n')

def err(msg):
    sys.stdout.write(redMsg(msg) + '\n')


def urlEncode(name):
    noSlashOrColonOrPound = name.replace('/', '%2F').replace(':','%3A').replace('#','%23').replace('+', '%2B')

    return noSlashOrColonOrPound

def plusEncode(name):
    encoded = name.replace('+', '%2B')
    return encoded

def plusSeparatedPath(path):
    # remove first / and replace rest with + for terminus use
    plussedPath = path.replace('/','', 1).replace('/', '+')
    return plussedPath

def urlDecode(name):
    return unquote(name)

def to_json_ld_type(obj):
    obj['@type'] = obj.pop('type')
    return obj



def refForPath(type, path, lexicalField):
    # path is name in the format a/b/c
    # nb assumes no @id existence
    # preconditions:  path is not url encoded
    # non-invariance: terminus' lexical id generation is subject to change, the following may break
    # nb: sensitive to lexical id generation fields, assumes only name (path) and potentially an UsdSpecifier enum (as the lexicalField)
    # terminus' uses the char '+' to seperate lexical fields and these shal not be encoded

    schemaPrefix = 'terminusdb:///schema#'
    lexicalField = schemaPrefix+'UsdSpecifier/'+lexicalField if lexicalField != None and lexicalField.find('Specifier') > -1 else lexicalField
    ref = path
   # ref.replace('/', '%2F')
    ref = urlEncode(type+'_'+ref)
    if lexicalField is not None:
        if isinstance(lexicalField, list):
          ref = [ ref+'+'+urlEncode(element) for element in lexicalField]
        elif not isinstance(lexicalField, str):
          ref = ref+'+'+urlEncode(str(lexicalField))
        else:
          ref = ref+'+'+urlEncode(lexicalField)

    ref = ref+'_URI'
    
    # terminus will url encode the ref
    return { "@ref": ref }

    #return { "@ref": plusEncode(ref) }

def defineSchemaId( name: str, version: str, instance:str, dbIp: str) -> SchemaId:
   schemaDef: SchemaId =  dict(schemaName= name, schemaVersion= version, instanceName= instance, dbUri= dbIp)
   return schemaDef

def getDbId(schema: SchemaId) -> str:
    msg('schema '+json.dumps(schema, indent=6))
    return schema.get('schemaName')+'-'+schema.get('schemaVersion')+'-'+schema.get('instanceName') if schema is not None else None

#def out_either_func(e_func, err_msg):
#    return e_func.either(lambda e: f'Error: {err_msg}: {e}', lambda x: x())

def out_either(eith, err_msg):
    return eith.either(lambda e: f'Error: {err_msg}: {e}', lambda x: x)


async def reject_promised(args):
     return await Promise(lambda resolve, reject: reject(args))

async def resolve_promised(x):
     return await Promise(lambda resolve, reject: resolve(x))

async def resolve_either(args):
     return  await Promise(lambda resolve, reject: resolve(Right(args)))

async def reject_either(args):
     return  await Promise(lambda resolve, reject: resolve(Left(args)))
     
async def chain_out(args):
     #piped_either = await args
     piped_either = await args
     return piped_either.either(lambda e: f'Error: out_promised_either : {e}', lambda x: x['doc'])

def circular_index(current, size):
    return (current + 1) % size





def instance_count(typeMap: PMap):
   count = 0
   types = typeMap.keys()
   for type in types:
       instanceMap: PMap = typeMap.get(type) 
       if instanceMap is not None:
          count = len(instanceMap.keys())
   #greenMsg('instance_count '+str(count))
   return count

def custom_encoder(x):
    if isinstance(x, datetime.datetime):
        return x.isoformat()
    elif isinstance(x, bytes):
        return base64.b64encode(x).decode()
    else:
        raise TypeError

'''
deprecated following

class batchScheduler:
    def __init__(self, max_count):
        
            period units: seconds
            batch size vs batch frequency is not fully known for db
            working assumption is that frequency is the independent parameter
            targeting 1 Hz, optimal range 1/2 to 5Hz
        
        self.max_count = max_count
        self.window_start = time.time()

        
    def batch_is_ready(self, count):
       
        now = time.time()
        elapsed = now - self.window_start
        over_count = count >= self.max_count 
        
        if  over_count:
            greenMsg(f'batch is ready: elapsed: {elapsed} count: {count}  over_count: {over_count}')
            self.window_start = now
            return True
        else:
            #msg(f'batch is not ready: elapsed: {elapsed} count: {count}  over_count: {over_count}')
            return False

'''
