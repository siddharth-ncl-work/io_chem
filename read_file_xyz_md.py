import pandas as pd
from tqdm import tqdm

def totalAtoms(file):
  last_pos=file.tell()
  line=file.readline()
  if 'frame' in line:
    line=file.readline()
  while 'frame' not in line: 
    prev_line=line                                    
    line=file.readline()

  atoms=int(prev_line.strip())
  file.seek(last_pos)
  return atoms

def gotoFrame(file,frame_no,frame_no_pos=1):
  line=file.readline()
  while line!='':
    if 'frame' in line:
      curr_frame_no=int(line.strip().split()[frame_no_pos])
  while 'frame' not in line:
    line=file.readline()
  line=file.readline()
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
  line[0]=line[0].strip()
  line[1]=float(line[1])
  line[2]=float(line[2])
  line[3]=float(line[3])
  return line

def getCords(file,start_frame_no,end_frame_no=None,frame_no_pos=1):
  data={'frame':[],'atom':[],'atom_no':[],'x':[],'y':[],'z':[]}
 
  atoms=totalAtoms(file)
 
  line=line[:4]
  line[0]=float(line[0])
  line[1]=float(line[1])
  line[2]=float(line[2])
  return line

def processLineBonds(line):
  line=line.strip().split()
  line=line[:3]
  line=list(map(int,line))
  line[0]-=1
  line[1]-=1
  if line[2]>1:
    line[2]=1
  return line

def getCords(file,start_frame_no,end_frame_no=None):
  data={'frame':[],'atom':[],'atom_no':[],'x':[],'y':[],'z':[]}
 
  if end_frame_no!=None and end_frame_no<start_frame_no:
    return pd.DataFrame.from_dict(data)
    
  if end_frame_no==None:
    end_frame_no=start_frame_no

  for frame_no in range(start_frame_no,end_frame_no+1):

    line,succ=gotoFrame(file,frame_no,frame_no_pos=frame_no_pos)

    line,succ=gotoFrame(file,frame_no)

    if not succ:
      print('Could not find the frame {}'.format(start_frame_no))
      continue
    elif succ:

      curr_frame_no=int(line.strip().split()[frame_no_pos])
      assert curr_frame_no==frame_no, 'Frame number Mismatch'
      curr_frame_no=int(line.strip().split()[1])
      assert curr_frame_no==frame_no, 'Frame number Mismatch'
      line=file.readline()
      line=file.readline()
      line=file.readline()
      atoms=int(line.strip().split()[0])
      for i in range(atoms):
        line=file.readline()
        line=processLineCords(line)
        data['frame'].append(curr_frame_no)
        data['atom'].append(line[0])
        data['atom_no'].append(i)
        data['x'].append(line[1])
        data['y'].append(line[2])
        data['z'].append(line[3])
  df=pd.DataFrame.from_dict(data)
  return df
        data['atom'].append(line[3])
        data['atom_no'].append(i)
        data['x'].append(line[0])
        data['y'].append(line[1])
        data['z'].append(line[2])
  df=pd.DataFrame.from_dict(data)
  return df

def getBonds(file,start_frame_no,end_frame_no=None):
  data={'frame':[],'atom0':[],'atom1':[],'bond':[]}
 
  if end_frame_no!=None and end_frame_no<start_frame_no:
    return pd.DataFrame.from_dict(data)
  
  if end_frame_no==None:
    end_frame_no=start_frame_no
    
  for frame_no in range(start_frame_no,end_frame_no+1):
    line,succ=gotoFrame(file,frame_no)
    if not succ:
      print('Could not find the frame {}'.format(start_frame_no))
      continue
    elif succ:
      curr_frame_no=int(line.strip().split()[1])
      assert curr_frame_no==frame_no, 'Frame number Mismatch'
      line=file.readline()
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
        data['atom0'].append(line[0])
        data['atom1'].append(line[1])
        data['bond'].append(line[2])
  df=pd.DataFrame.from_dict(data)
  return df
  
def getCordsAndBonds(file,start_frame_no,end_frame_no=None):
  df_cords=pd.DataFrame(columns=['frame','atom','atom_no','x','y','z'])
  df_bonds=pd.DataFrame(columns=['frame','atom0','atom1','bond'])

  if end_frame_no!=None and end_frame_no<start_frame_no:
    return (df_cords,df_bonds)

  if end_frame_no==None:
    end_frame_no=start_frame_no

  for frame_no in range(start_frame_no,end_frame_no+1):
    data_cords={'frame':[],'atom':[],'atom_no':[],'x':[],'y':[],'z':[]}
    line,succ=gotoFrame(file,frame_no)
    if not succ:
      print('Could not find the frame {}'.format(start_frame_no))
      continue
    elif succ:
      curr_frame_no=int(line.strip().split()[1])
      assert curr_frame_no==frame_no, 'Frame number Mismatch'
      line=file.readline()
      line=file.readline()
      line=file.readline()
      atoms=int(line.strip().split()[0])
      bonds=int(line.strip().split()[1])
      for i in range(atoms):
        line=file.readline()
        line=processLineCords(line)
        data_cords['frame'].append(curr_frame_no)
        data_cords['atom'].append(line[3])
        data_cords['atom_no'].append(i)
        data_cords['x'].append(line[0])
        data_cords['y'].append(line[1])
        data_cords['z'].append(line[2])
    tmp_df_cords=pd.DataFrame.from_dict(data_cords)

    
    data_bonds={'frame':[],'atom0':[],'atom1':[],'bond':[]}
    for i in range(bonds):
        line=file.readline()
        line=processLineBonds(line)
        data_bonds['frame'].append(curr_frame_no)
        data_bonds['atom0'].append(line[0])
        data_bonds['atom1'].append(line[1])
        data_bonds['bond'].append(line[2])
    tmp_df_bonds=pd.DataFrame.from_dict(data_bonds)
    
    
    df_cords=pd.concat([df_cords,tmp_df_cords],ignore_index=True)
    df_bonds=pd.concat([df_bonds,tmp_df_bonds],ignore_index=True)
  return (df_cords,df_bonds)
  
