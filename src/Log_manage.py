import os

class Log_manage:
    def __init__(self):
        self.log_list=list()
        self.abs_path=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.log_folder=os.path.join(self.abs_path,'data','log')
        self.path_dict:dict[str,str]={
            'present_log_folder':'',
            'stock':'',
            'acquisition_folder':'',
            'arsenal_pool_folder':'',
            'character_pool_folder':'',
        }

    def get_all_log(self):
        return [entry for entry in os.listdir(self.log_folder)]
    
    def set_present_log_folder(self,log_name:str):
        self.path_dict['present_log_folder']=os.path.join(self.log_folder,log_name)
        self.path_dict['stock']=os.path.join(self.log_folder,log_name,'stock')
        self.path_dict['acquisition_folder']=os.path.join(self.log_folder,log_name,'acquisition_center')
        self.path_dict['arsenal_pool_folder']=os.path.join(self.log_folder,log_name,'pools','arsenal')
        self.path_dict['character_pool_folder']=os.path.join(self.log_folder,log_name,'pools','character')
        self.path_dict['record']=os.path.join(self.log_folder,'record')