import pandas as pd

def getNumOfAtoms(file):
  last_pos=file.tell()
  line=file.readline()
  while 'frame' in line:
    line=file.readfile()
  line=file.readline()
  line=file.readline()
  atoms=int(line.strip().split()[0])
  file.seek(last_pos)
  return atoms

def gotoFrame(file,frame_no):
  line=file.readline()
  while line!='':
    if 'frame' in line:
      curr_frame_no=int(line.strip().split()[1])
      if curr_frame_no==frame_no:
        return (line,True)
    line=file.readline()    
  return line,False


def processLineCords(line):
  line=line.strip().split()
  line=line[:4]
  line[0]=float(line[0])
  line[1]=float(line[1])
  line[2]=float(line[2])
  return line

def processLineBonds(line):
  line=line.strip().split()
  line=line[:3]
  line=map(int,line)
  line[0]-=1
  line[1]-=1
  return line

def getCords(file,start_frame_no,end_frame_no=None):
  data={'frame':[],'atom':[],'atom_no':[],'x':[],'y':[],'z':[]}
  '''
  if end_frame_no==None:
    line,succ=gotoFrame(file,start_frame_no)
    if not succ:
      print('Could not find start frame {}'.format(start_frame_no))
      return
    curr_frame_no=int(line.strip().split()[1])
    assert curr_frame_no==start_frame_no, 'Frame number Mismatch'
    line=file.readline()
    line=file.readline()
    atoms=int(line.strip().split()[0])
    for i in range(atoms):
      line=file.readline() 
      line=processLineCords(line)     
      data['frame'].append(curr_frame_no)
      data['atom'].append(line[3])
      data['atom_no'].append(i)
      data['x'].append(line[0])
      data['y'].append(line[1])
      data['z'].append(line[2])
    df=pd.DataFrame.from_dict(data)
    return df
    '''
  if end_frame_no!=None and end_frame_no<start_frame_no:
    return pd.DataFrame.from_dict(data)
    
  if end_frame_no==None:
    end_frame_no=start_frame_no

  #if end_frame_no>=start_frame_no:
  for frame_no in range(start_frame_no,end_frame_no):
    line,succ=gotoFrame(file,frame_no)
    if not succ:
      print('Could not find the frame {}'.format(start_frame_no))
      continue
    elif succ:
      curr_frame_no=int(line.strip().split()[1])
      assert curr_frame_no==frame_no, 'Frame number Mismatch'
      line=file.readline()
      line=file.readline()
      atoms=int(line.strip().split()[0])
      for i in range(atoms):
        line=file.readline()
        line=processLine(line)
        data['frame'].append(curr_frame_no)
        data['atom'].append(line[3])
        data['atom_no'].append(i)
        data['x'].append(line[0])
        data['y'].append(line[1])
        data['z'].append(line[2])
  df=pd.DataFrame.from_dict(data)
  return df

def getBonds(file,start_frame_no,end_frame_no=None):
  data={'frame':[],'atom_0':[],'atom_1':[],'bond':[]}
  '''
  if end_frame_no==None:
    line,succ=gotoFrame(file,start_frame_no)
    if not succ:
      print('Could not find start frame {}'.format(start_frame_no))
      return
    curr_frame_no=int(line.strip().split()[1])
    assert curr_frame_no==start_frame_no, 'Frame number Mismatch'
    line=file.readline()
    line=file.readline()
    atoms=int(line.strip().split()[0])
    bonds=int(line.strip().split()[1])
    for i in range(atoms):
      file.readline()
    for i in range(bond):
      line=file.readline()
      line=processLineBonds(line)
      data['frame'].append(curr_frame_no)
      data['atom_0'].append(line[0])
      data['atom_1'].append(line[1])
      data['bond'].append(line[2])
    df=pd.DataFrame.from_dict(data)
    return df
  '''
  if end_frame_no!=None and end_frame_no<start_frame_no:
    return pd.DataFrame.from_dict(data)
  
  if end_frame_no==None:
    end_frame_no=start_frame_no
    
  #elif end_frame_no!=None and end_frame_no>=start_frame_no:
  for frame_no in range(start_frame_no,end_frame_no):
    line,succ=gotoFrame(file,frame_no)
    if not succ:
      print('Could not find the frame {}'.format(start_frame_no))
      continue
    elif succ:
      curr_frame_no=int(line.strip().split()[1])
      assert curr_frame_no==frame_no, 'Frame number Mismatch'
      line=file.readline()
      line=file.readline()
      atoms=int(line.strip().split()[0])
      bonds=int(line.strip().split()[1])
      for i in range(atoms):
        file.readline()
      for i in range(bonds):
        line=file.readline()
        line=processLineBonds(line)
        data['frame'].append(curr_frame_no)
        data['atom_0'].append(line[0])
        data['atom_1'].append(line[1])
        data['bond'].append(line[2])
  df=pd.DataFrame.from_dict(data)
  return df
    
