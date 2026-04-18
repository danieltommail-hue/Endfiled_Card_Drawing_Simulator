from src.Arsenal_pool import Arsenal
from src.Character_pool import Character
import pandas as pd
import os

abs_path=os.path.dirname(os.path.abspath(__file__))
standard_path=os.path.join(os.path.dirname(abs_path),'data','standard')

class build_pool:
    def __init__(self,file_path:str,pool_type:str):
        self.pool_list=list()
        self.pool_dict={}
        self.file_path=file_path
        self.pool_type=pool_type
        self.up_name=None
        self.build()
    
    def build(self):
        reader=pd.read_csv(self.file_path).to_dict(orient='records')
        if self.pool_type=='character':
            for simple_dict in reader:
                if simple_dict.get('state')=='normal':
                    new_character=Character(**simple_dict) #type:ignore
                    self.pool_list.append(new_character)
                    self.pool_dict[simple_dict.get('name')]=new_character
                elif simple_dict.get('state')=='up':
                    self.up_name=Character(**simple_dict) #type:ignore
        elif self.pool_type=='arsenal':
            for simple_dict in reader:
                if simple_dict.get('state')=='normal':
                    new_character=Arsenal(**simple_dict) #type:ignore
                    self.pool_list.append(new_character)
                    self.pool_dict[simple_dict.get('name')]=new_character
                elif simple_dict.get('state')=='up':
                    self.up_name=Arsenal(**simple_dict) #type:ignore

        '''
        with open(self.file_path, 'r', encoding='utf-8') as f:
            reader=csv.DictReader(f)
            if self.pool_type=='character':
                for row in reader:
                    if row.get('state')=='normal':
                        new_character=Character(**row)
                        self.pool_list.append(new_character)
                        self.pool_dict[row.get('name')]=new_character
                    elif row.get('state')=='up':
                        self.up_name=Character(**row)
            elif self.pool_type=='arsenal':
                for row in reader:
                    if row.get('state')=='normal':
                        new_arsenal=Arsenal(**row)
                        self.pool_list.append(new_arsenal)
                        self.pool_dict[row.get('name')]=new_arsenal
                    elif row.get('state')=='up':
                        self.up_name=Arsenal(**row)
'''
    def get_list(self):
        return self.pool_list
    
    def get_dict(self):
        return self.pool_dict

default_character_pool=build_pool(os.path.join(standard_path,'pools','character','default.csv'),'character')
default_arsenal_pool=build_pool(os.path.join(standard_path,'pools','arsenal','default.csv'),'arsenal')