import os
import shutil
from datetime import datetime
from src.Stock import Stock
from src.Character_pool import Headhunting,Basic_Headhunting
from src.Arsenal_pool import Arsenal_issue
from src.Build_pool import build_pool
from src.Acquisition_center import Acquisition_center
from src.Log_manage import Log_manage
from src.Record import Record

class Environment:
    def __init__(self):
        self.stock=Stock()
        self.headhunting:Headhunting=None #type: ignore
        self.arsenal_issue:Arsenal_issue=None #type: ignore
        self.acquisition_center:Acquisition_center=Acquisition_center()
        self.record:Record=Record()
        self.path_dict:dict[str, str]={}
        self.log_manage=Log_manage()

    def get_time(self):
        return datetime.now().strftime("%Y_%m_%d_%H_%M_%S_%f")

    def get_standard_path(self,name:str,name_type:str):
        standard_path=os.path.join(self.log_manage.abs_path,'data','standard')
        return os.path.join(standard_path,name_type,f'{name}.csv')
    
    def get_log_path(self,name:str,name_type:str='',log_name:str='',csv_bool=False):
        if csv_bool:
            if log_name=='':
                log_path=self.log_manage.path_dict['present_log_folder']
            else:
                log_path=os.path.join(self.log_manage.abs_path,'data','log',log_name)
            return os.path.join(log_path,name_type,f'{name}.csv')
        else:
            if log_name=='':
                log_path=self.log_manage.path_dict['present_log_folder']
            else:
                log_path=os.path.join(self.log_manage.abs_path,'data','log',log_name)
            return os.path.join(log_path,name_type,name)

    def create_new_log(self):
        log_name=datetime.now().strftime("%Y_%m_%d_%H_%M_%S")
        standard_path=os.path.join(self.log_manage.abs_path,'data','standard')
        new_log_path=os.path.join(self.log_manage.log_folder,log_name)
        os.makedirs(new_log_path,exist_ok=True)
        for root,dirs,files in os.walk(standard_path):
            rel_path=os.path.relpath(root,standard_path)
            new_root_path=os.path.join(new_log_path,rel_path)
            os.makedirs(new_root_path,exist_ok=True)
            for file in files:
                standard_file=os.path.join(root,file)
                new_log_file=os.path.join(new_root_path,file)
                shutil.copy(standard_file,new_log_file)
        os.makedirs(os.path.join(new_log_path,'record'),exist_ok=True)
        self.set_environment_from_log(log_name=log_name)

    def set_environment_from_log(self,log_name:str):
        self.log_manage.set_present_log_folder(log_name)
        self.record.set_record_from_log(self.get_log_path('record'))
        self.acquisition_center.set_acquisition_center_from_log(self.get_log_path('acquisition_center'))
        self.stock.set_stock_from_log(self.get_log_path(''))
        
    def save_log(self):
        log_name=datetime.now().strftime("%Y_%m_%d_%H_%M_%S")
        self.record.save_record_to_log(self.get_log_path('record'))
        self.acquisition_center.save_acquisition_center_to_log(self.get_log_path('acquisition_center'))
        self.stock.save_stock_to_log(self.get_log_path(''))
        new_name=self.get_log_path('',log_name=log_name)
        os.rename(self.get_log_path(''),new_name)
        self.log_manage.set_present_log_folder(new_name)

    def set_headhunting(self,up_name:str):
        if self.headhunting and self.headhunting.up_character.name!='basic':
            self.stock.spectral_permit_stock[self.headhunting.up_character.name]['stock']=self.stock.spectral_permit
            self.stock.spectral_permit_stock[self.headhunting.up_character.name]['gained']=\
                self.acquisition_center.products['卡池寻访凭证'].gained
            self.stock.spectral_permit_stock[self.headhunting.up_character.name]['limit']=\
                self.acquisition_center.products['卡池寻访凭证'].limit
        pool=build_pool(self.get_standard_path(up_name,'pools\\character'),'character')
        if up_name=='basic':
            self.headhunting=Basic_Headhunting(pool.get_list()) #type:ignore
        elif up_name=='start':
            self.headhunting=Basic_Headhunting(pool.get_list(),True) #type:ignore
        else:
            self.headhunting=Headhunting(pool.get_list(),pool.up_name) #type:ignore
            self.stock.spectral_permit=self.stock.spectral_permit_stock[up_name]['stock']
            self.acquisition_center.products['卡池寻访凭证'].limit=\
                self.stock.spectral_permit_stock[up_name]['limit']
            self.acquisition_center.products['卡池寻访凭证'].gained=\
                self.stock.spectral_permit_stock[up_name]['gained']

    def set_arsenal_issue(self,up_name:str):
        pool=build_pool(self.get_standard_path(up_name,'pools/arsenal'),'arsenal')
        self.arsenal_issue=Arsenal_issue(pool.get_list(),pool.up_name) #type:ignore

    def pull_one_character(self):
        if self.headhunting.up_character.name=='basic':
            self.stock.add_stock(**self.stock.calculate_basic_pull())
        else:
            self.stock.add_stock(**self.stock.calculate_pull())
        pulled_character=self.headhunting.pull_once()
        self.record.add_record('character',self.headhunting.up_character.name,\
                               pulled_character,self.get_time())
        self.stock.deal_with_character_pull(pulled_character)
        self.stock.calculate_bond_quota(pulled_character,'character')
        arsenal_change=self.stock.calculate_arsenal_ticket(pulled_character)
        self.stock.add_stock(**{'arsenal_ticket':arsenal_change})
        return pulled_character

    def pull_ten_characters(self):
        if (not self.headhunting.up_character.name=='basic') and (self.headhunting.up_character.name not in self.stock.free_pull_used)\
        and self.headhunting.total_pulls>=30:
            self.stock.free_pull_used.append(self.headhunting.up_character.name)
            pulled_characters=self.headhunting.free_pull_ten_times()
        else:
            if self.headhunting.up_character.name=='basic':
                self.stock.add_stock(**self.stock.calculate_basic_ten_pulls())
            else:
                self.stock.add_stock(**self.stock.calculate_pull())
            pulled_characters=self.headhunting.pull_ten_times()
        self.record.add_record('character',self.headhunting.up_character.name,\
                               pulled_characters,self.get_time())
        self.stock.deal_with_character_pull(pulled_characters)
        self.stock.calculate_bond_quota(pulled_characters,'character')
        arsenal_change=self.stock.calculate_arsenal_ticket(pulled_characters)
        self.stock.add_stock(**{'arsenal_ticket':arsenal_change})
        return pulled_characters
    
    def pull_arsenal(self):
        self.stock.add_stock(**self.stock.calculate_arsenal_pull())
        pulled_arsenal=self.arsenal_issue.pull_ten_times()
        self.record.add_record('arsenal',self.arsenal_issue.up_arsenal.name,\
                               pulled_arsenal,self.get_time())
        self.stock.deal_with_arsenal_pull(pulled_arsenal)
        self.stock.calculate_bond_quota(pulled_arsenal,'arsenal')
        return pulled_arsenal

    def acquisition_purchase(self,name:str):
        if name=='spectral_permit':
            self.stock.spectral_permit_stock[self.headhunting.up_character.name]['gained']+=1
        product=self.acquisition_center.purchase(name)
        self.stock.add_stock(**product)