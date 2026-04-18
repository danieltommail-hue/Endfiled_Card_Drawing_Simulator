import os
import pandas as pd

class Record:
    def __init__(self):
        self.character_record:dict[str,list[tuple[(list[tuple[(str,int)]],str,str)]]]=dict()
        self.arsenal_record:dict[str,list[tuple[(list[tuple[(str,int)]],str,str)]]]=dict()
        self.character_print_list:list=[]
        self.arsenal_print_list:list=[]

    def set_record_from_log(self,folder_path:str):
        reader=pd.read_csv(os.path.join(folder_path,'character.csv')).to_dict(orient='records') #type:ignore
        temp:list[tuple[(str,int)]]=[]
        for row in reader:
            if row['mode']=='consecutive':
                temp.append((row['name'],row['rarity']))
                if len(temp)==10:
                    self.character_record[row['pool_name']].append((temp,row['method'],row['time']))
            else:
                self.character_record[row['pool_name']].append(([(row['name'],row['rarity'])],row['method'],row['time']))
        reader=pd.read_csv(os.path.join(folder_path,'arsenal.csv')).to_dict(orient='records') #type:ignore
        temp:list[tuple[(str,int)]]=[]       
        for row in reader:
            if row['mode']=='consecutive':
                temp.append((row['name'],row['rarity']))
                if len(temp)==10:
                    self.arsenal_record[row['pool_name']].append((temp,row['mode'],row['time']))
            else:
                self.arsenal_record[row['pool_name']].append(([(row['name'],row['rarity'])],row['mode'],row['time']))

    def save_record_to_log(self,folder_path:str):
        character_write_list=[]
        for key,value in self.character_record.items():
            pool_name=key
            temp=[]
            for single_tuple in value:
                character_list,mode,time=single_tuple
                name,rarity=character_list
                temp.append({'name':name,'rarity':rarity,'pool_name':pool_name,'mode':mode,'time':time})
            character_write_list.extend(temp)
        character_write_list.sort(key=lambda x:x['time'],reverse=False)
        self.character_print_list=character_write_list
        character_write_list.sort(key=lambda x:x['time'],reverse=True)
        columns=['name','rarity','pool_name','mode','time']
        data=pd.DataFrame(character_write_list,columns=columns)
        data.to_csv(os.path.join(folder_path,'character.csv'),index=False)
        arsenal_write_list=[]
        for key,value in self.arsenal_record.items():
            pool_name=key
            temp=[]
            for single_tuple in value:
                arsenal_list,mode,time=single_tuple
                name,rarity=arsenal_list
                temp.append({'name':name,'rarity':rarity,'pool_name':pool_name,'mode':mode,'time':time})
            arsenal_write_list.extend(temp)
        arsenal_write_list.sort(key=lambda x:x['time'],reverse=False)
        self.arsenal_print_list=arsenal_write_list
        arsenal_write_list.sort(key=lambda x:x['time'],reverse=True)
        data=pd.DataFrame(arsenal_write_list,columns=columns)
        data.to_csv(os.path.join(folder_path,'arsenal.csv'),index=False)

    def add_record(self,type_name:str,up_name:str,result:list,time:str):
        if len(result)==1:
            consecutive_flag=False
        else:
            consecutive_flag=True
        if type_name=='character':
            result_list=[]
            for character in result:
                if consecutive_flag==True:
                    result_list.append(((character.name,character.rarity),'consecutive',time))
                else:
                    result_list.append(((character.name,character.rarity),'single',time))
            self.character_record.setdefault(up_name,[]).extend(result_list)
        else:
            result_list=[]
            for arsenal in result:
                if consecutive_flag==True:
                    result_list.append(((arsenal.name,arsenal.rarity),'consecutive',time))
                else:
                    result_list.append(((arsenal.name,arsenal.rarity),'single',time))
            self.arsenal_record.setdefault(up_name,[]).extend(result_list)

    #TODO:注意抽卡的原始顺序，可能会因为后续的排序出现顺序的改变