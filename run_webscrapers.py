from webscrapers import *
#from dbhelper import DBHelper


import sys
# sys.setdefaultencoding() does not exist, here!
reload(sys)  # Reload does the trick!
sys.setdefaultencoding('UTF8')

	
def addNewEvents():
  getCSDepartment()
  getCNSDepartment()
  getUT()
  getMcCombsBBA()
  getMcCombsGeneral()
  getLibrary()
  getHornsLink()


addNewEvents()
  #dbhelper.addAllEvents(events)
