## Copyright Pacific Digital Technology Pty
## 2025-03-11


########################################
## classes
########################################

class FuncDemo:
  version = "0.0.3"
 
  def getFiles(self):
    return 'got the files here. version {}'.format(self.version)
    ## return 'got the files here. '
  
  def getWells(self):
    return 'got the wells from here. version {}'.format(self.version)
  
       
########################################
## functions
########################################

def read_files(searchText):
   func = FuncDemo()
   return func.getFiles()

def read_wells(searchText):
   func = FuncDemo()
   return func.getWells()


########################################
## variables
########################################

files = read_files("tty")
wells = read_wells("xtr")

