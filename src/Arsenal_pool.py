import random
import os

class Arsenal:
    def __init__(self,**kwargs):
        self.name:str=None #type: ignore
        self.rarity:int=None #type: ignore
        self.gained:bool=False #type: ignore
        self.potential_phase:int=0 #type: ignore
        self.tokens:int=0 #type: ignore
        self.path:str=None #type: ignore
        for key,value in kwargs.items():
            if hasattr(self,key):
                setattr(self,key,value)
        abs_path=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.path=os.path.join(abs_path,'resource','arsenal',f'{self.name}.png')

    def upgrade(self):
        if self.potential_phase+self.tokens<=5:
            self.potential_phase+=self.tokens
            self.tokens=0
        else:
            self.tokens=self.potential_phase+self.tokens-5
            self.potential_phase=5

class Arsenal_pool:
    def __init__(self,arsenals:list[Arsenal]):
        self.arsenals=arsenals
        self.six_star_arsenals=[x for x in self.arsenals if x.rarity==6]
        self.five_star_arsenals=[x for x in self.arsenals if x.rarity==5]
        self.four_star_arsenals=[x for x in self.arsenals if x.rarity==4]

class Arsenal_issue:
    def __init__(self,arsenals:list[Arsenal],up_arsenal:Arsenal):
        self.arsenal_pool=Arsenal_pool(arsenals)
        self.up_arsenal=up_arsenal
        self.up_guarantee_count=0
        self.six_stars_guarantee_count=0
        self.first_up=False
        self.total_pulls=0
        self.pull_rate=0.04
        self.pull_rate_five_star=0.15
        self.pull_rate_four_star=0.85
        self.records:list[list[Arsenal]]=list()
        self.up_pull_count=0

    def check_40_guarantee(self):
        if self.six_stars_guarantee_count==40:
            return True
        else:
            return False
        
    def check_80_guarantee(self):
        if self.total_pulls==80 and self.first_up==False:
            return True
        else:
            return False
    
    def check_extra_up(self):
        if self.up_guarantee_count<=10:
            return False
        else:
            if (self.up_guarantee_count-10)%8==0:
                if((self.up_guarantee_count-10)/8)%2==1:
                    return True
                else:
                    self.give_arms_oc()
                    return False
            else:
                return False
            
    def give_arms_oc(self):
        #TODO: 完成武库赠礼（补充武库箱）的赠送
        pass
            

    def pull(self) -> Arsenal:
        self.total_pulls+=1
        self.six_stars_guarantee_count+=1
        random_number=random.random()
        if self.check_80_guarantee():
            self.first_up=True
            self.up_pull_count+=1
            self.six_stars_guarantee_count=0
            return self.up_arsenal
        if random_number<self.pull_rate or self.check_40_guarantee():
            self.six_stars_guarantee_count=0
            up_rate=random.random()
            if up_rate<0.25:
                self.up_pull_count+=1
                return self.up_arsenal
            else:
                return random.choice(self.arsenal_pool.six_star_arsenals)
        elif random_number<self.pull_rate+self.pull_rate_five_star:
            return random.choice(self.arsenal_pool.five_star_arsenals)
        else:
            return random.choice(self.arsenal_pool.four_star_arsenals)
    
    def pull_ten_times(self) -> list[Arsenal]:
        self.up_guarantee_count+=1
        pulled_arsenals=[self.pull() for _ in range(10)]
        if self.check_extra_up():
            self.up_pull_count+=1
            pulled_arsenals.append(self.up_arsenal)
        self.records.append(pulled_arsenals)
        return pulled_arsenals