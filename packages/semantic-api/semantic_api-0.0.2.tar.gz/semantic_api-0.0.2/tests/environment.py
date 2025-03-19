import asyncio
#import sys
#sys.path.append("../src")

from typing_extensions import Final
from semantic_api.api_python.src.semantic_api import semantic
#from semantic_api.api_python.src.semantic_api import semanticClient
from semantic_api.api_python.src.config import brokerIp, schemaName, schemaVersion, instanceName, dbUri, batch_size, topics
from semantic_api.common.src.utils import msg, defineSchemaId
from semantic_fera.fera_types.src.type_constructors import pathMap



def before_all(context):
  #  context.loop = asyncio.get_event_loop()
 #   context.loop.run_forever()
  try:
    context.semantic = semantic( brokerIp, defineSchemaId(schemaName, schemaVersion, instanceName, dbUri), batch_size, topics)
    context.pathMap = pathMap(context.semantic)
    context.flatMap = None
  except Exception as e:
          print(f'before_all: Exception: {e}')
   
def after_step(context, step):
    print()
 
#def after_all(context):
#    context.loop.close
    # Clean up and close the browser window after tests are done
    # context.browser.quit()