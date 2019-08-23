import pandas as pd 
import numpy as np
import sys
sys.path.extend(['..','.'])
from decimal import Decimal

"""
def skip_frames(file_ptr,frame_no):
  atoms=int(file_ptr.readline().strip())
  curr_frame_no=int(file_ptr.readline().strip().split()[2])
  if curr_frame_no==frame_no:
    return (atoms,curr_frame_no)
  elif curr_frame_no<frame_no:
    #skip ahead
    for i in range(atoms):
      line=file_ptr.readline()
    return skip_frames(file_ptr,frame_no)
  elif curr_frame_no>frame_no:
    file_ptr.seek(0)
    return skip_frames(file_ptr,frame_no)
"""
def skip_frames(file_ptr,frame_no):
  atoms=int(file_ptr.readline().strip())
  curr_frame_no=int(file_ptr.readline().strip().split()[2])
  if curr_frame_no==frame_no:
    return (atoms,curr_frame_no)
  elif curr_frame_no<frame_no:
    #skip ahead
    for f in range(curr_frame_no,frame_no):
      assert f==curr_frame_no,'check skip frame'
      for i in range(atoms):
        file_ptr.readline()
      atoms=int(file_ptr.readline().strip())
      curr_frame_no=int(file_ptr.readline().strip().split()[2])
    return (atoms,curr_frame_no)
  elif curr_frame_no>frame_no:
    file_ptr.seek(0)
    return skip_frames(file_ptr,frame_no)


def identify_file_type(file_ptr):
  return file_ptr.name.strip().split('.')[-1].lower()

def read_file(file_ptr,frames=False,column_list=['element','x','y','z'],start_frame_no=0,end_frame_no=100):
  file_type=identify_file_type(file_ptr)
  if file_type=='xyz':
    if frames:
      return read_file_xyz_with_frames(file_ptr,column_list=column_list, 
					start_frame_no=start_frame_no,end_frame_no=end_frame_no)
    else:
      return read_file_xyz_without_frames(file_ptr,column_list)
  elif file_type=='mol':
    if frames:
      return read_file_mol_with_frames(file_ptr,column_list=column_list,
                                        start_frame_no=start_frame_no,end_frame_no=end_frame_no)
    else:
      return read_file_mol_without_frames(file_ptr,column_list)
    
  else:
    print('cannot read .'+file_type+' files yet\n functionality will be added in future')

def read_file_xyz_without_frames(file_ptr,column_list=['element','x','y','z']):
  atoms=int(file_ptr.readline())
  print(atoms)
  file_ptr.readline()
  
  cords=pd.DataFrame(index=range(atoms),columns=column_list)
  for i,_ in enumerate(range(atoms)):
    line=file_ptr.readline()
    cords.iloc[i]=line.strip().split()
  return cords

def read_file_xyz_with_frames(file_ptr,column_list=['element','x','y','z'],start_frame_no=0,end_frame_no=100):
  if start_frame_no>config.MAX_FRAME_NO:
    print('start_frame_no={} is higher than MAX_FRAME_NO={}'.format(start_frame_no,config.MAX_FRAME_NO))
    return

  if end_frame_no>config.MAX_FRAME_NO:
    print('end_frame_no={} is higher than MAX_FRAME_NO={}'.format(end_frame_no,config.MAX_FRAME_NO))
    print('running till last frame')

  data=[]
  curr_frame_no=start_frame_no
  for f in range(start_frame_no,end_frame_no+1):
    atoms,curr_frame_no=skip_frames(file_ptr,f)
    assert f==curr_frame_no,'check read_file function'
    for _ in range(atoms):
      line=file_ptr.readline().strip().split()
      line.append(curr_frame_no)    
      data.append(line)
  cords=pd.DataFrame(data,columns=column_list+['frame'])
  cords[column_list[1:]]=cords[column_list[1:]].applymap(np.float64)
  return (cords,curr_frame_no)

def read_file_mol_without_frames(file_ptr,column_list=['element','x','y','z','connectivity']):
  file_ptr.readline()
  file_ptr.readline()
  file_ptr.readline()

  info=file_ptr.readline()
  info=info.strip().split()
  atoms=int(info[0])
  bonds=int(info[1])

  print('atoms={} bonds={}'.format(atoms,bonds))

  cords=pd.DataFrame(index=range(atoms),columns=column_list)

  for i,_ in enumerate(range(atoms)):
    line=file_ptr.readline()
    line=line.strip().split()
    xyz=list(map(float,line[:3]))
    xyz.insert(0,line[3])
    xyz.append([])
    cords.iloc[i]=xyz

  #add bonds
  return cords


def read_file_mol_with_frames(file_ptr):
  pass

if __name__=='__main__':
  #import sys
  #sys.path.extend(['..','.'])
  file=open('/home/vanka/siddharth/mol_data/Acetamide3d.mol','r')
  cords=read_file(file,column_list=['element','x','y','z','connectivity'])
  print(cords)
