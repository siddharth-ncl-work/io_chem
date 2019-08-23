import pandas as pd 
import numpy as np
import sys
sys.path.extend(['..','.'])
from decimal import Decimal

import read_file_mol_md

def fileType(file):
  if type(file)==str:
    file.strip().split('.')[-1].lower()
  else:
    return file_ptr.name.strip().split('.')[-1].lower()

def readFile(file_path):
  pass

def readFileMd(file,info='cords',start_frame_no,end_frame_no=None):
  file_type=fileType(file)
  if file_type=='xyz':
    pass
  elif file_type=='.mol':
    if info=='cords':
      df=read_file_mol_md.getCords(file,start_frame_no,end_frame_no)
      return df
    elif info=='bonds':
      df=read_file_mol_md.getBonds(file,start_frame_no,end_frame_no)
      return df


#if __name__=='__main__':
  #import sys
  #sys.path.extend(['..','.'])
  #file=open('/home/vanka/siddharth/mol_data/Acetamide3d.mol','r')
  #cords=read_file(file,column_list=['element','x','y','z','connectivity'])
  #print(cords)
