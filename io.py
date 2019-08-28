import pandas as pd 
import numpy as np
import sys
#sys.path.extend(['..','.','../..'])
from decimal import Decimal

from . import read_file_mol_md
from . import read_file_xyz

def fileType(file):
  if type(file)==str:
    file.strip().split('.')[-1].lower()
  else:
    return file.name.strip().split('.')[-1].lower()

def readFile(file_path,file_type=None,info='cords'):
  if file_type==None:
    file_type=fileType(file_path)
  if file_type=='xyz':
    if info=='cords':
      df=read_file_xyz.getCords(file_path)
      return df
    elif info=='atoms':
      pass

def readFileMd(file,start_frame_no=0,end_frame_no=None,info='cords',file_type=None):
  if file_type==None:
    file_type=fileType(file)
  if file_type=='xyz':
    pass
  elif file_type=='mol':
    if info=='atoms':
      atoms=read_file_mol_md.totalAtoms(file)
      return atoms
    elif info=='cords':
      df=read_file_mol_md.getCords(file,start_frame_no,end_frame_no=end_frame_no)
      return df
    elif info=='bonds':
      df=read_file_mol_md.getBonds(file,start_frame_no,end_frame_no=end_frame_no)
      return df
  elif file_type=='opt':
    pass
  else:
    print('file type is not yet implemented')

#file=open('/home/vanka/siddharth/mol_data/Acetamide3d.mol','r')
if __name__=='__main__':
  file_path='/home/vanka/siddharth/shailaja_project/Na_cluster_for_center_of_mass'
  df=readFile(file_path,file_type='xyz')
  print(df)
