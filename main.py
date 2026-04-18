import sys,os
from src.Environment import Environment
from src.Character_pool import Character
from src.Arsenal_pool import Arsenal
from ui.ui_main_window import Ui_MainWindow
from ui.ui_acquisition_widget import Ui_Acquisition_center
from ui.ui_pool_choose import Ui_Choose_Pool
from ui.ui_records import Ui_record
from ui.ui_media import Pull_animate,Pull_result_picture
from PySide6.QtCore import Qt,QUrl,QTimer
from PySide6.QtGui import QPixmap,QColor
from PySide6.QtWidgets import QMainWindow,QApplication,QGraphicsScene,QGraphicsPixmapItem,QGraphicsView,QWidget
from PySide6.QtWidgets import QListWidget,QListWidgetItem,QMessageBox
from PySide6.QtMultimedia import QMediaPlayer,QAudioOutput



class Acquisition_center_ui(QWidget,Ui_Acquisition_center):
    def __init__(self,main_window:'MainWindow'):
        super().__init__()
        self.main_window=main_window
        self.setupUi(self)
        self.products_dict={}
        self.load_list()

        self.products_list.setSelectionMode(QListWidget.SelectionMode.SingleSelection)

        self.acquisition_purchase.clicked.connect(self.on_clicked_acquisition_purchase)
        self.products_list.itemClicked.connect(self.update_content)
        self.products_list.itemDoubleClicked.connect(self.on_clicked_acquisition_purchase)
    
    def load_list(self):
        self.products_list.clear()
        self.products_dict={}
        original_dict=self.main_window.simulation_environment.acquisition_center.products
        for name,product in original_dict.items():
            if product.gained<product.limit:
                content_text=f'{product.name}\t{product.cost} {product.cost_type}'
                self.products_dict[content_text]=name
        for content_text in self.products_dict.keys():
            item=QListWidgetItem(content_text)
            self.products_list.addItem(item)

    def on_clicked_acquisition_purchase(self):
        selected_item=self.products_list.selectedItems()
        if not len(selected_item)==0:
            for content_text in selected_item:
                name=self.products_dict[content_text.text()]
                try:
                    self.main_window.simulation_environment.acquisition_purchase(name)
                except ValueError:
                    QMessageBox.critical(self,"Attention!","资源不足")
                self.main_window.update_stock_browser()
                self.cost_count.setText(str(self.main_window.simulation_environment.acquisition_center.cost_count))
        self.load_list()

    def update_content(self):
        selected_item=self.products_list.selectedItems()
        if not len(selected_item)==0:
            self.textBrowser.clear()
            for content_text in selected_item:
                name=self.products_dict[content_text.text()]
                original_dict=self.main_window.simulation_environment.acquisition_center.products
                content_in_text=original_dict[name].content_in_text
                self.textBrowser.append(content_in_text)



class Choose_Pool_Character(QWidget,Ui_Choose_Pool):
    def __init__(self,main_window:'MainWindow'):
        super().__init__()
        self.setupUi(self)
        self.main_window=main_window
        self.load_list()

        self.pool_list.setSelectionMode(QListWidget.SelectionMode.SingleSelection)

        self.pool_list.itemDoubleClicked.connect(self.on_clicked_choose_bottom)
        self.select_bottom.clicked.connect(self.on_clicked_choose_bottom)

    def on_clicked_choose_bottom(self):
        selected_items=self.pool_list.selectedItems()
        if not len(selected_items)==0:
            self.main_window.simulation_environment.set_headhunting(selected_items[0].text())
            self.main_window.present_character_pool.setText(selected_items[0].text())
            self.close()

    def load_list(self):
        folder_path=os.path.join(os.path.dirname(os.path.abspath(__file__)),'data','standard','pools','character')
        file_list=os.listdir(folder_path)
        for single_file in file_list:
            if single_file.split('.')[0]!='default':
                item=QListWidgetItem(single_file.split('.')[0])
                self.pool_list.addItem(item)



class Choose_Pool_Arsenal(QWidget,Ui_Choose_Pool):
    def __init__(self,main_window:'MainWindow'):
        super().__init__()
        self.setupUi(self)
        self.main_window=main_window
        self.load_list()

        self.pool_list.setSelectionMode(QListWidget.SelectionMode.SingleSelection)

        self.pool_list.itemDoubleClicked.connect(self.on_clicked_choose_bottom)
        self.select_bottom.clicked.connect(self.on_clicked_choose_bottom)

    def on_clicked_choose_bottom(self):
        selected_items=self.pool_list.selectedItems()
        if not len(selected_items)==0:
            self.main_window.simulation_environment.set_arsenal_issue(selected_items[0].text())
            self.main_window.present_arsenal_pool.setText(selected_items[0].text())
            self.close()

    def load_list(self):
        folder_path=os.path.join(os.path.dirname(os.path.abspath(__file__)),'data','standard','pools','arsenal')
        file_list=os.listdir(folder_path)
        for single_file in file_list:
            single_file=single_file.split('.')[1]
        for single_file in file_list:
            if single_file.split('.')[0]!='default' and single_file.split('.')[0]!='temp':
                item=QListWidgetItem(single_file.split('.')[0])
                self.pool_list.addItem(item)



class Character_record(QWidget,Ui_record):
    def __init__(self,main_window:'MainWindow'):
        super().__init__()
        self.setupUi(self)
        self.main_window=main_window

    def load_list(self):
        self.main_window.simulation_environment.save_log()
        temp=self.main_window.simulation_environment.record.character_print_list
        if not temp==None:
            for single_record in temp:
                mode_name='单抽' if single_record['mode']=='single' else '十连'
                content=f'{single_record['name']}\t{single_record['rarity']}\t{single_record['pool_name']}\t{mode_name}\t{single_record['time']}'
                item=QListWidgetItem(content)
                if single_record['rarity']==6:
                    item.setBackground(QColor('red'))
                elif single_record['rarity']==5:
                    item.setBackground(QColor('orange'))
                else:
                    item.setBackground(QColor('purple'))
                self.record_list.addItem(item)



class Arsenal_record(QWidget,Ui_record):
    def __init__(self,main_window:'MainWindow'):
        super().__init__()
        self.setupUi(self)
        self.main_window=main_window
    
    def load_list(self):
        self.record_list.clear()
        self.main_window.simulation_environment.save_log()
        temp=self.main_window.simulation_environment.record.arsenal_print_list
        if not temp==None:
            for single_record in temp:
                mode_name='单抽' if single_record['mode']=='single' else '十连'
                content=f'{single_record['name']}\t{single_record['rarity']}\t{single_record['pool_name']}\t{mode_name}\t{single_record['time']}'
                item=QListWidgetItem(content)
                if single_record['rarity']==6:
                    item.setBackground(QColor('red'))
                elif single_record['rarity']==5:
                    item.setBackground(QColor('orange'))
                else:
                    item.setBackground(QColor('purple'))
                self.record_list.addItem(item)



class Character_gained(QWidget,Ui_record):
    def __init__(self,main_window:'MainWindow'):
        super().__init__()
        self.setupUi(self)
        self.main_window=main_window

    def load_list(self):
        self.record_list.clear()
        all_characters=self.main_window.simulation_environment.stock.all_character
        all_characters=dict(sorted(all_characters.items(),key=lambda x:x[1].rarity,reverse=True))
        for name,character in all_characters.items():
            if character.gained:
                temp=(f'{name}\t{character.rarity}星\t潜能:{character.potential_phase}\t信物:{character.tokens}')
                item=QListWidgetItem(temp)
                self.record_list.addItem(item)



class Arsenal_gained(QWidget,Ui_record):
    def __init__(self,main_window:'MainWindow'):
        super().__init__()
        self.setupUi(self)
        self.main_window=main_window

    def load_list(self):
        self.record_list.clear()
        all_arsenals=self.main_window.simulation_environment.stock.all_arsenal
        all_arsenals=dict(sorted(all_arsenals.items(),key=lambda x:x[1].rarity,reverse=True))
        for name,arsenal in all_arsenals.items():
            if arsenal.gained:
                temp=(f'{name}\t{arsenal.rarity}星\t潜能:{arsenal.potential_phase}\t信物:{arsenal.tokens}')
                item=QListWidgetItem(temp)
                self.record_list.addItem(item)



class MainWindow(QMainWindow,Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.simulation_environment=Environment()
        self.simulation_environment.create_new_log()

        self.acquisition_center=Acquisition_center_ui(self)
        self.choose_character_pool=Choose_Pool_Character(self)
        self.choose_arsenal_pool=Choose_Pool_Arsenal(self)
        self.record_character=Character_record(self)
        self.record_arsenal=Arsenal_record(self)
        self.character_gained_list=Character_gained(self)
        self.arsenal_gained_list=Arsenal_gained(self)

        self.pull_animate=None
        self.pull_result_animate=None
        self.pull_result_picture=None
        self.stackedWidget.setContextMenuPolicy(Qt.ContextMenuPolicy.NoContextMenu)

        self.bgm_player=QMediaPlayer(self)
        self.bgm_audio_output=QAudioOutput(self)
        self.bgm_player.setAudioOutput(self.bgm_audio_output)
        self.bgm_default_volume=0.2
        self.bgm_audio_output.setVolume(self.bgm_default_volume)
        bgm_path=os.path.join(os.path.dirname(os.path.abspath(__file__)),'resource','video','after_pull.mp4')
        self.bgm_player.setSource(QUrl.fromLocalFile(bgm_path))
        self.bgm_player.setLoops(-1)
        self.bgm_player.play()
        self.bgm_timer=None

        self.set_character_pool.clicked.connect(self.on_clicked_set_character_pool)
        self.set_arsenal_pool.clicked.connect(self.on_clicked_set_arsenal_pool)
        self.character_pull_one.clicked.connect(self.on_clicked_character_pull_one)
        self.character_pull_ten.clicked.connect(self.on_clicked_character_pull_ten)
        self.arsenal_pull_ten.clicked.connect(self.on_clicked_arsenal_pull_ten)
        self.enter_acquisition_center.clicked.connect(self.on_clicked_enter_acquisition_center)
        self.check_character_log.clicked.connect(self.on_clicked_check_character_log)
        self.check_arsenal_log.clicked.connect(self.on_clicked_check_arsenal_log)
        self.create_log.clicked.connect(self.on_clicked_create_log)
        self.save_log.clicked.connect(self.on_clicked_save_log)
        self.actioncheck_gained_character.triggered.connect(self.on_actioncheck_gained_character)
        self.actioncheck_gained_arsenal.triggered.connect(self.on_actioncheck_gained_arsenal)
        self.actionquick_check_character_potential_phase.triggered.connect(self.on_character_potential)
        self.actionquick_check_arsenal_potential_phase.triggered.connect(self.on_arsenal_potential)
        self.actioncheck_special_stock.triggered.connect(self.on_check_special_stock)
        self.actiontoken_aic_quota_exchange.triggered.connect(self.on_token_aic_quota_exchange)

        self.update_stock_browser()

    def on_clicked_set_character_pool(self):
        if self.choose_character_pool==None:
            self.choose_character_pool=Choose_Pool_Character(self)
        self.update_pull_result([])
        self.choose_character_pool.show()
        self.choose_character_pool.raise_()
        self.choose_character_pool.activateWindow()

    def on_clicked_set_arsenal_pool(self):
        if self.choose_arsenal_pool==None:
            self.choose_arsenal_pool=Choose_Pool_Arsenal(self)
        self.update_pull_result([])
        self.choose_arsenal_pool.show()
        self.choose_arsenal_pool.raise_()
        self.choose_arsenal_pool.activateWindow()

    def on_clicked_character_pull_one(self):
        try:
            pulled_character=self.simulation_environment.pull_one_character()
        except ValueError:
            QMessageBox.critical(self,"Attention!","资源不足")
            return
        except AttributeError:
            QMessageBox.information(self,"Attention!","请先选择角色池")
            return
        except RuntimeError:
            QMessageBox.information(self,"Attention!",f"获得一个{self.simulation_environment.headhunting.up_character.name}的信物！")
            return
        self.display_animate(pulled_character)
        self.update_stock_browser()
        self.update_pull_result(pulled_character) #type:ignore
        self.update_pull_count()
        if self.checkBox.isChecked():
            self.check_six(pulled_character) #type:ignore

    def on_clicked_character_pull_ten(self):
        try:
            pulled_characters=self.simulation_environment.pull_ten_characters()
        except ValueError:
            QMessageBox.critical(self,"Attention!","资源不足")
            return
        except AttributeError:
            QMessageBox.information(self,"Attention!","请先选择角色池")
            return
        except RuntimeError:
            QMessageBox.information(self,"Attention!",f"获得一个{self.simulation_environment.headhunting.up_character.name}的信物！")
            return
        self.display_animate(pulled_characters)
        self.update_stock_browser()
        self.update_pull_result(pulled_characters) #type:ignore
        self.update_pull_count()
        if self.checkBox.isChecked():
            self.check_six(pulled_characters) #type:ignore

    def on_clicked_arsenal_pull_ten(self):
        try:
            pulled_arsenals=self.simulation_environment.pull_arsenal()
        except ValueError:
            QMessageBox.critical(self,"Attention!","资源不足")
            return
        except AttributeError:
            QMessageBox.information(self,"Attention!","请先选择武器池")
            return
        self.update_stock_browser()
        self.update_pull_result(pulled_arsenals) #type:ignore
        self.check_six(pulled_arsenals) #type:ignore

    def on_clicked_enter_acquisition_center(self):
        if self.acquisition_center==None:
            self.acquisition_center=Acquisition_center_ui(self)
        self.acquisition_center.show()
        self.acquisition_center.raise_()
        self.acquisition_center.activateWindow()

    def on_clicked_check_character_log(self):
        if self.record_character==None:
            self.record_character=Character_record(self)
        self.record_character.load_list()
        self.record_character.show()
        self.record_character.raise_()
        self.record_character.activateWindow()

    def on_clicked_check_arsenal_log(self):
        if self.record_arsenal==None:
            self.record_arsenal=Arsenal_record(self)
        self.record_arsenal.load_list()
        self.record_arsenal.show()
        self.record_arsenal.raise_()
        self.record_arsenal.activateWindow()

    def on_clicked_create_log(self):
        self.simulation_environment.create_new_log()
        self.simulation_environment.headhunting.reset()
        self.update_pull_result([])
        self.update_pull_count()
        self.update_stock_browser()

    def on_clicked_save_log(self):
        self.simulation_environment.save_log()

    def on_actioncheck_gained_character(self):
        if self.character_gained_list==None:
            self.character_gained_list=Character_gained(self)
        self.character_gained_list.load_list()
        self.character_gained_list.show()
        self.character_gained_list.raise_()
        self.character_gained_list.activateWindow()

    def on_actioncheck_gained_arsenal(self):
        if self.arsenal_gained_list==None:
            self.arsenal_gained_list=Arsenal_gained(self)
        self.arsenal_gained_list.load_list()
        self.arsenal_gained_list.show()
        self.arsenal_gained_list.raise_()
        self.arsenal_gained_list.activateWindow()

    def on_character_potential(self):
        for _,character in self.simulation_environment.stock.all_character.items():
            character.upgrade()
        self.character_gained_list.load_list()

    def on_arsenal_potential(self):
        for _,arsenal in self.simulation_environment.stock.all_arsenal.items():
            arsenal.upgrade()
        self.arsenal_gained_list.load_list()

    def on_check_special_stock(self):
        pass

    def on_token_aic_quota_exchange(self):
        self.simulation_environment.stock.token_quota_exchange()

    def update_stock_browser(self):
        stock_dict=vars(self.simulation_environment.stock)
        for key,value in stock_dict.items():
            if hasattr(self,key):
                getattr(self,key).setText(str(int(value)))

    def update_pull_result(self,result:list[Character|Arsenal]):
        views_list:list[QGraphicsView]=[getattr(self,f'graphicsView_{i}') for i in range(1,11)]
        for i,view in zip(range(10),views_list):
            if i<=len(result)-1:
                pixmap=QPixmap(result[i].path)
                print(result[i].path)
                if not pixmap.isNull():
                    print('not NULL')
                    scene=QGraphicsScene()
                    item=QGraphicsPixmapItem(pixmap)
                    scene.addItem(item)
                    view.setScene(scene)
                    view.fitInView(item)
                else:
                    view.setScene(QGraphicsScene())
            else:
                view.setScene(QGraphicsScene())

    def update_pull_count(self):
        self.total_count.setText(str(self.simulation_environment.headhunting.total_pulls))
        self.six_star_guarantee_count.setText(str(self.simulation_environment.headhunting.rate_up_count))

    def check_six(self,result:list[Character|Arsenal]):
        flag=False
        for single_result in result:
            if single_result.rarity==6:
                flag=True
                break
        if flag:
            QMessageBox.information(self,"Congratulations!","出6星了!")
    
    '''
    def pull_animate_finish(self,character_list):
        if self.pull_animate:
            self.stackedWidget.removeWidget(self.pull_animate)
            self.pull_animate.deleteLater()
            self.pull_animate=None
        self.pull_result_animate=Pull_result_animate(character_list,self.pull_result_animate_finish)
        self.stackedWidget.addWidget(self.pull_result_animate)
        self.stackedWidget.setCurrentWidget(self.pull_result_animate)
    
    def pull_result_animate_finish(self,character_list):
        if self.pull_result_animate:
            self.stackedWidget.removeWidget(self.pull_result_animate)
            self.pull_result_animate.deleteLater()
            self.pull_result_animate=None
        self.pull_result_picture=Pull_result_picture(character_list,self.pull_result_picture_finish)
        self.stackedWidget.addWidget(self.pull_result_picture)
        self.stackedWidget.setCurrentWidget(self.pull_result_picture)

    def pull_result_picture_finish(self):
        if self.pull_result_picture:
            self.stackedWidget.removeWidget(self.pull_result_picture)
            self.pull_result_picture.deleteLater()
            self.pull_result_picture=None
        self.stackedWidget.close()
    '''

    def display_animate(self,character_list:list[Character]):
        if self.checkBox.isChecked():return
        self.animate_widget.raise_()
        self.animate_widget.setEnabled(True)
        self.main_widget.setEnabled(False)
        while self.stackedWidget.count()>0:
            temp=self.stackedWidget.widget(0)
            if temp:
                self.stackedWidget.removeWidget(temp)
                temp.deleteLater()
        self.stackedWidget.show()
        self.stackedWidget.raise_()
        self.stackedWidget.activateWindow()
        self.pull_animate=Pull_animate(character_list,self.pull_animate_finish,self.mute_bgm)
        self.stackedWidget.addWidget(self.pull_animate)
        self.stackedWidget.setCurrentWidget(self.pull_animate)
        '''
        self.pull_result_picture=Pull_result_picture(character_list,self.after_delay)
        self.stackedWidget.addWidget(self.pull_result_picture)
        self.stackedWidget.setCurrentWidget(self.pull_result_picture)
        '''
    
    def pull_animate_finish(self,character_list):
        self.pull_result_picture=Pull_result_picture(character_list,self.after_delay)
        self.stackedWidget.addWidget(self.pull_result_picture)
        self.stackedWidget.setCurrentWidget(self.pull_result_picture)

    def after_delay(self):
        self.stackedWidget.close()
        self.main_widget.setEnabled(True)
        self.main_widget.raise_()
    
    def mute_bgm(self,duration_ms=17000,mute_bool=True):
        def restore_bgm():
            self.bgm_audio_output.setVolume(self.bgm_default_volume)
            self.bgm_player=None
        if self.bgm_timer is not None and self.bgm_audio_output.volume():
            self.bgm_timer.stop()
        if mute_bool:
            self.bgm_audio_output.setVolume(0)
            self.bgm_timer=QTimer()
            self.bgm_timer.timeout.connect(restore_bgm)
            self.bgm_timer.start(duration_ms)
        else:restore_bgm()



def main():
    app=QApplication(sys.argv)
    window=MainWindow()
    window.show()
    sys.exit(app.exec())



if __name__=='__main__':
    main()