import os
import pandas as pd

abs_path = os.path.dirname(os.path.abspath(__file__))
default_acquisition_center_path=os.path.join(abs_path,'acquisition_center','default.txt')

class Product:
    def __init__(self,**kwargs):
        self.name:str=kwargs.get('name') #type: ignore
        self.type:str=kwargs.get('type') #type: ignore
        self.cost_type:str=kwargs.get('cost_type') #type: ignore
        self.cost:int=kwargs.get('cost') #type: ignore
        self.gained:int=kwargs.get('gained') #type: ignore
        self.limit:int=kwargs.get('limit') #type: ignore
        self.path:str=kwargs.get('path') #type: ignore
        self.content_in_text:str=kwargs.get('content_in_text') #type: ignore
        temp_dict:dict=kwargs.get('content')#type: ignore
        self.content:dict[str, int]=dict()
        for key,value in temp_dict.items():
            self.content[key]=value

class Acquisition_center:
    def __init__(self):
        self.cost_count=0
        self.products:dict[str,Product]=dict()

    def set_acquisition_center_from_log(self,folder_path:str):
        reader=pd.read_csv(os.path.join(folder_path,'default.csv')) #type:ignore
        reader['content']=reader['content'].apply(eval)
        reader=reader.to_dict(orient='records')
        for product in reader:
            self.products[product['name']]=Product(**product) #type:ignore

    def save_acquisition_center_to_log(self,folder_path:str):
        product_list=[]
        for _,value in self.products.items():
            product_list.append(vars(value))
        columns=['name','type','cost','gained','limit','content','content_in_text','path']
        data=pd.DataFrame(product_list,columns=columns)
        data.to_csv(os.path.join(folder_path,'default.csv'))

    def purchase(self,product_name:str) -> dict[str, int]:
        if product_name in self.products and self.products[product_name].gained < self.products[product_name].limit:
            if self.products[product_name].cost_type=='rmb':
                self.cost_count+=self.products[product_name].cost
                self.products[product_name].gained+=1
                return self.products[product_name].content
            else:
                temp=self.products[product_name].content
                temp[self.products[product_name].cost_type]=-self.products[product_name].cost
                self.products[product_name].gained+=1
                return temp
        else:
            if product_name not in self.products:
                raise ValueError(f"there is no product named {product_name}")
            elif self.products[product_name].gained >= self.products[product_name].limit:
                raise ValueError(f"the gain of product {product_name} has reached its limit")
            else:
                raise ValueError("unknown error")