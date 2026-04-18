import os
import pandas as pd
from src.Character_pool import Character
from src.Arsenal_pool import Arsenal
from src.Build_pool import build_pool

class Stock:
    def __init__(self,origeometry:int=0,oroberyl:int=0,chartered_permit:int=0,spectral_permit:int=0,basic_permit:int=0,\
                 arsenal_ticket:int=0,bond_quota:int=0,aic_quota:int=0,endpoint_quota:int=0):
        self.origeometry=origeometry
        self.oroberyl=oroberyl
        self.chartered_permit=chartered_permit
        self.spectral_permit=spectral_permit
        self.basic_permit=basic_permit
        self.arsenal_ticket=arsenal_ticket
        self.bond_quota=bond_quota
        self.aic_quota=aic_quota
        self.endpoint_quota=endpoint_quota
        self.all_character:dict[str,Character]=None #type:ignore
        self.all_arsenal:dict[str,Arsenal]=None #type:ignore
        self.special_item_stock:dict={}
        self.spectral_permit_stock:dict={}
        self.free_pull_used=[]

    def add_stock(self,**kwargs):
        for key,value in kwargs.items():
            if key=='insufficient':
                raise ValueError('资源不足')
            if hasattr(self,key):
                if (getattr(self,key)+value)<0:
                    raise ValueError('资源不足')
        for key,value in kwargs.items():
            if key=='insufficient':
                raise ValueError('资源不足')
            if hasattr(self,key):
                if (getattr(self,key)+value)<0:
                    raise ValueError('资源不足')
                else:
                    setattr(self,key,getattr(self,key)+value)
            else:
                self.special_item_stock[key]+=value 
    
    def set_stock_from_log(self,folder:str):
        reader=pd.read_csv(os.path.join(folder,'stock','stock.csv')).to_dict(orient='records') #type:ignore
        for row in reader:self.set_stock(**row) #type:ignore

        reader=pd.read_csv(os.path.join(folder,'stock','special_item.csv')).to_dict(orient='records') #type:ignore
        for row in reader:
            self.special_item_stock[row['name']]=row['count']

        reader=pd.read_csv(os.path.join(folder,'stock','spectral_permit.csv')).to_dict(orient='records') #type:ignore
        for row in reader:
            self.spectral_permit_stock[row['name']]=row

        with open(os.path.join(folder,'stock','free_pull_used.txt'),'r',encoding='utf-8') as f:
            reader=f.readline()
            self.free_pull_used=reader.split(',')
            
        self.all_character=build_pool(os.path.join(folder,'pools','character','default.csv'),'character').get_dict()
        self.all_arsenal=build_pool(os.path.join(folder,'pools','arsenal','default.csv'),'arsenal').get_dict()

    def save_stock_to_log(self,folder:str):
        stock_dict={}
        for key,value in vars(self).items():
            if not (key=='all_character' or key=='all_arsenal' or key=='special_stock'):
                stock_dict[key]=value
        columns=['origeometry','oroberyl','chartered_permit','spectral_permit','basic_permit',\
                 'arsenal_ticket','bond_quota','aic_quota','endpoint_quota']
        stock_data=pd.DataFrame([stock_dict],columns=columns)
        stock_data.to_csv(os.path.join(folder,'stock','stock.csv'),index=False)

        spectral_list=[]
        for key,value in self.spectral_permit_stock.items():
            spectral_list.append({'name':key,'stock':value['stock'],'gained':value['gained'],'limit':value['limit']})
        spectral_data=pd.DataFrame(spectral_list,columns=['name','stock','gained','limit'])
        spectral_data.to_csv(os.path.join(folder,'stock','spectral_permit.csv'),index=False)
        
        special_list=[]
        for key,value in self.special_item_stock.items():
            special_list.append({'name':key,'count':value})
        special_data=pd.DataFrame(special_list,columns=['name','count'])
        special_data.to_csv(os.path.join(folder,'stock','special_item.csv'),index=False)

        character_columns=['name','rarity','gained','potential_phase','tokens','state','path']
        arsenal_columns=['name','rarity','gained','potential_phase','tokens','type','state','path']
        character_data=pd.DataFrame([vars(value) for _,value in self.all_character.items()],columns=character_columns)
        arsenal_data=pd.DataFrame([vars(value) for _,value in self.all_arsenal.items()],columns=arsenal_columns)
        character_data.to_csv(os.path.join(folder,'pools','character','default.csv'),index=False)
        arsenal_data.to_csv(os.path.join(folder,'pools','arsenal','default.csv'),index=False)

        with open(os.path.join(folder,'stock','free_pull_used.txt'),'w',encoding='utf-8') as f:
            text=','.join(self.free_pull_used)
            f.write(text)

    def set_stock(self,**kwargs):
        for key,value in kwargs.items():
            if hasattr(self,key):
                setattr(self,key,value)
            else:
                raise AttributeError("there is no attribute {key}")

    def calculate_pull(self,resource_spent:dict[str,int]={}) -> dict[str,int]:
        if resource_spent=={}:
            resource_needed:dict[str,int]=\
            {
                'spectral_permit':0,
                'chartered_permit':0,
                'oroberyl':0,
                'origeometry':0
            }
        else: resource_needed=resource_spent
        if self.spectral_permit+resource_needed['spectral_permit']>0:
            return {'spectral_permit':-1}
        elif self.chartered_permit+resource_needed['chartered_permit']>0:
            return {'chartered_permit':-1}
        elif self.oroberyl+resource_needed['oroberyl']>=500:
            return {'oroberyl':-500}
        else:
            oroberyl_needed=500-(self.oroberyl+resource_needed['oroberyl'])
            origeometry_needed=(oroberyl_needed+75-1)//75
            if self.origeometry+resource_needed['origeometry']>=origeometry_needed:
                return_oroberyl=origeometry_needed*75-oroberyl_needed
                return {'oroberyl':return_oroberyl+self.oroberyl, 'origeometry':-origeometry_needed}
            else:
                return {'insufficient':0}
            
    def calculate_basic_pull(self,resource_spent:dict[str,int]={}) -> dict[str,int]:
        if resource_spent=={}:
            resource_needed:dict[str,int]=\
            {
                'basic_permit':0,
                'chartered_permit':0,
                'oroberyl':0,
                'origeometry':0
            }
        else: resource_needed=resource_spent
        if self.basic_permit+resource_needed['basic_permit']>0:
            return {'basic_permit':-1}
        elif self.chartered_permit+resource_needed['chartered_permit']>0:
            return {'chartered_permit':-1}
        elif self.oroberyl+resource_needed['oroberyl']>=500:
            return {'oroberyl':-500}
        else:
            oroberyl_needed=500-(self.oroberyl+resource_needed['oroberyl'])
            origeometry_needed=(oroberyl_needed+75-1)//75
            if self.origeometry+resource_needed['origeometry']>=origeometry_needed:
                return_oroberyl=origeometry_needed*75-oroberyl_needed
                return {'oroberyl':return_oroberyl+self.oroberyl, 'origeometry':-origeometry_needed}
            else:
                return {'insufficient':0}
    
    def calculate_ten_pulls(self) -> dict[str, int]:
        resource_needed:dict[str,int]=\
            {
                'basic_permit':0,
                'spectral_permit':0,
                'chartered_permit':0,
                'oroberyl':0,
                'origeometry':0
            }
        for _ in range(10):
            pull_once=self.calculate_pull(resource_needed)
            for name,number in pull_once.items():
                if name=='insufficient':
                    return {'insufficient':0}
                else:
                    resource_needed[name]+=number
        return resource_needed
    
    def calculate_basic_ten_pulls(self) -> dict[str, int]:
        resource_needed:dict[str,int]=\
            {
                'basic_permit':0,
                'chartered_permit':0,
                'oroberyl':0,
                'origeometry':0
            }
        for _ in range(10):
            pull_once=self.calculate_basic_pull(resource_needed)
            for name,number in pull_once.items():
                if name=='insufficient':
                    return {'insufficient':0}
                else:
                    resource_needed[name]+=number
        return resource_needed
    
    def calculate_arsenal_pull(self) -> dict[str, int]:
        if self.arsenal_ticket>=1980:
            return {'arsenal_ticket':-1980}
        elif self.arsenal_ticket+self.origeometry*25>=1980:
            ticket_needed=1980-self.arsenal_ticket
            origeometry_needed=(ticket_needed+25-1)//25
            return_ticket=origeometry_needed*25+self.arsenal_ticket-1980
            return {'arsenal_ticket':return_ticket-self.arsenal_ticket,'origeometry':-origeometry_needed}
        else:
            return {'insufficient':0}

    def calculate_arsenal_ticket(self,characters:list[Character]):
        ticket_changed=0
        for character in characters:
            if character.rarity==6:
                ticket_changed+=2000
            elif character.rarity==5:
                ticket_changed+=200
            elif character.rarity==4:
                ticket_changed+=20
        return ticket_changed
    
    def calculate_bond_quota(self,box,type):
        quota_change=0
        if type=='character':
            for x in box:
                self.all_character[x.name].gained=True
                if self.all_character[x.name].rarity==6:
                    quota_change+=50
                elif self.all_character[x.name].rarity==5:
                    quota_change+=10
        elif type=='arsenal':
            for x in box:
                self.all_arsenal[x.name].gained=True
                if self.all_arsenal[x.name].rarity==6:
                    quota_change+=50
                elif self.all_arsenal[x.name].rarity==5:
                    quota_change+=10
        self.bond_quota+=quota_change
        return quota_change
    
    def token_quota_exchange(self):
        for character in self.all_character.values():
            if character.gained==True and (character.tokens+character.potential_phase>5):
                exchange_number=character.tokens+character.potential_phase-5
                character.tokens-=exchange_number
                if character.rarity==6:
                    self.endpoint_quota+=exchange_number*10
                elif character.rarity==5:
                    self.aic_quota+=exchange_number*20
                elif character.rarity==4:
                    self.aic_quota+=exchange_number*5
    
    def character_potential_upgrade(self,name:str):
        self.all_character[name].upgrade()

    def deal_with_character_pull(self,characters:list[Character]):
        for character in characters:
            if self.all_character[character.name].gained:
                self.all_character[character.name].tokens+=1
            else:
                self.all_character[character.name].gained=True

    def deal_with_arsenal_pull(self,arsenals:list[Arsenal]):
        for arsenal in arsenals:
            if self.all_arsenal[arsenal.name].gained:
                self.all_arsenal[arsenal.name].tokens+=1
            else:
                self.all_arsenal[arsenal.name].gained=True
