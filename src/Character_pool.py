import random
import os

class Character:
    def __init__(self,**kwargs):
        self.name:str=None #type: ignore
        self.rarity:int=None #type: ignore
        self.gained:bool=False #type: ignore
        self.potential_phase:int=None #type: ignore
        self.tokens:int=0 #type: ignore
        self.path:str=None #type: ignore
        for key,value in kwargs.items():
            if hasattr(self,key):
                setattr(self,key,value)
        abs_path=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.path=os.path.join(abs_path,'resource','character',f'{self.name}.png')

    def upgrade(self):
        if self.potential_phase+self.tokens<=5:
            self.potential_phase+=self.tokens
            self.tokens=0
        else:
            self.tokens=self.potential_phase+self.tokens-5
            self.potential_phase=5

class Character_pool:
    def __init__(self,characters:list[Character]):
        self.characters=characters
        self.six_star_characters=[x for x in self.characters if x.rarity==6]
        self.five_star_characters=[x for x in self.characters if x.rarity==5]
        self.four_star_characters=[x for x in self.characters if x.rarity==4]

class Headhunting:
    def __init__(self,characters:list[Character],up_character:Character):
        self.characters=Character_pool(characters)
        self.up_character=up_character
        self.five_star_guarantee_count=0
        self.guarantee_count=0
        self.first_up=False
        self.rate_up_count=0
        self.total_pulls=0
        self.pull_rate=0.008
        self.pull_rate_five_star=0.08
        self.pull_rate_four_star=0.912
        self.records:list[list[Character]]=list()
        self.up_pull_count=0
        self.up_token_count=0

    def reset(self):
        self.five_star_guarantee_count=0
        self.guarantee_count=0
        self.first_up=False
        self.rate_up_count=0
        self.total_pulls=0
        self.pull_rate=0.008
        self.pull_rate_five_star=0.08
        self.pull_rate_four_star=0.912
        self.records=list()
        self.up_pull_count=0
        self.up_token_count=0

    def succeed_guarantee(self,last_rate_up_count:int):
        self.rate_up_count=last_rate_up_count

    def check_120_guarantee(self):
        if self.guarantee_count>=120 and self.first_up==False:
            return True
        else:
            return False
        
    def check_240_guarantee(self):
        if self.guarantee_count==240:
            self.guarantee_count=0
            return True
        else:
            return False
        
    def check_five_guarantee(self):
        self.five_star_guarantee_count+=1
        if self.five_star_guarantee_count>=10:
            self.five_star_guarantee_count=0
            return True
        else:
            return False
    
    def give_up_token(self):
        self.up_token_count+=1

    def pull(self) -> Character:
        self.rate_up_count+=1
        self.guarantee_count+=1
        self.total_pulls+=1
        if self.check_240_guarantee():
            self.give_up_token()
            raise RuntimeError(f'{self.up_character.name}信物加一')
        if self.check_120_guarantee():
            self.rate_up_count=0
            self.pull_rate=0.008
            self.first_up=True
            self.up_pull_count+=1
            return self.up_character
        if self.check_five_guarantee():
            return random.choice(self.characters.five_star_characters)
        if self.rate_up_count>=66:
            self.pull_rate+=0.05
        random_number=random.random()
        if random_number<self.pull_rate:
            up_rate=random.random()
            if up_rate<0.5:
                self.up_pull_count+=1
                self.rate_up_count=0
                self.pull_rate=0.008
                self.first_up=True
                return self.up_character
            else:
                self.rate_up_count=0
                self.pull_rate=0.008
                return random.choice(self.characters.six_star_characters)
        elif random_number<self.pull_rate+\
            (1-self.pull_rate)*(self.pull_rate_five_star)/(self.pull_rate_five_star+self.pull_rate_four_star):
            return random.choice(self.characters.five_star_characters)
        else:
            return random.choice(self.characters.four_star_characters)
    '''
        if random_number<self.pull_rate:
            up_rate=random.random()
            if up_rate<0.5:
                self.up_pull_count+=1
                self.rate_up_count=0
                self.pull_rate=0.008
                self.first_up=True
                print(f'{self.up_character.name} {self.up_character.rarity} {random_number} {self.pull_rate}')
                return self.up_character
            else:
                self.rate_up_count=0
                self.pull_rate=0.008
                temp=random.choice(self.characters.six_star_characters)
                print(f'{temp.name} {temp.rarity} {random_number} {self.pull_rate}')
                return temp
        elif random_number<self.pull_rate+\
            (1-self.pull_rate)*(self.pull_rate_five_star)/(self.pull_rate_five_star+self.pull_rate_four_star):
            temp=random.choice(self.characters.five_star_characters)
            print(f'{temp.name} {temp.rarity} {random_number} {self.pull_rate}')
            return temp
        else:
            temp=random.choice(self.characters.four_star_characters)
            print(f'{temp.name} {temp.rarity} {random_number} {self.pull_rate}')
            return temp
    '''
    def pull_once(self):
        pulled_character=self.pull()
        self.records.append([pulled_character])
        return [pulled_character]

    def pull_ten_times(self):
        pulled_characters=[self.pull() for _ in range(10)]
        self.records.append(pulled_characters)
        return pulled_characters

    def free_pull_ten_times(self):
        pulled_characters=[]
        for _ in range(10):
            if self.check_five_guarantee():
                pulled_characters.append(random.choice(self.characters.five_star_characters))
            random_number=random.random()
            if random_number<0.008:
                up_rate=random.random()
                if up_rate<0.5:
                    self.up_pull_count+=1
                    self.rate_up_count=0
                    pulled_characters.append(self.up_character)
                else:
                    self.rate_up_count=0
                    pulled_characters.append(random.choice(self.characters.six_star_characters))
            elif random_number<0.088:
                pulled_characters.append(random.choice(self.characters.five_star_characters))
            else:
                pulled_characters.append(random.choice(self.characters.four_star_characters))
        self.records.append(pulled_characters)
        return pulled_characters

class Basic_Headhunting(Headhunting):
    def __init__(self,characters:list[Character],start_flag=False):
        super().__init__(characters,Character())
        self.up_character=Character(**{'name':'basic'})
        self.start_flag=start_flag
    
    def check_40_guarantee(self):
        if self.guarantee_count==40 and self.start_flag==True:
            return True
        elif self.total_pulls>40 and self.start_flag==True:
            raise ValueError('Start Headhunting must not be pulled more than 40 times')
        else:
            return False

    def pull(self) -> Character:
        self.rate_up_count+=1
        self.guarantee_count+=1
        self.total_pulls+=1
        if self.rate_up_count>=66:
            self.pull_rate+=0.05
        random_number=random.random()
        if self.check_40_guarantee():
            self.guarantee_count=0
            return random.choice(self.characters.six_star_characters)
        if self.check_five_guarantee():
            return random.choice(self.characters.five_star_characters)
        if random_number<self.pull_rate:
            self.rate_up_count=0
            self.pull_rate=0.008
            return random.choice(self.characters.six_star_characters)
        elif random_number<self.pull_rate+\
            (1-self.pull_rate)*(self.pull_rate_five_star)/(self.pull_rate_five_star+self.pull_rate_four_star):
            return random.choice(self.characters.five_star_characters)
        else:
            return random.choice(self.characters.four_star_characters)
    