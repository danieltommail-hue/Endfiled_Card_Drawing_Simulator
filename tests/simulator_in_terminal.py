from src.Environment import Environment

simulator_environment=Environment()
simulator_environment.create_new_log()

for x in range(9):
    simulator_environment.acquisition_purchase('开采一箱衍质源石')

simulator_environment.set_headhunting('汤汤')
simulator_environment.pull_one_character
for _ in range(50):
    simulator_environment.pull_ten_characters()

simulator_environment.set_headhunting('伊冯')
simulator_environment.pull_one_character()
simulator_environment.pull_ten_characters()

simulator_environment.set_arsenal_issue('落草')
for x in range(9):
    simulator_environment.pull_arsenal()
    print(x*10)

simulator_environment.save_log()