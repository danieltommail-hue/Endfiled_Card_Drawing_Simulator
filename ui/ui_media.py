import os
from src.Character_pool import Character
from PySide6.QtCore import Qt,QUrl
from PySide6.QtGui import QMouseEvent, QPixmap
from PySide6.QtMultimedia import QMediaPlayer,QAudioOutput
from PySide6.QtMultimediaWidgets import QVideoWidget
from PySide6.QtWidgets import QWidget,QVBoxLayout,QHBoxLayout,QGraphicsView,QGraphicsScene,QGraphicsPixmapItem,QFrame

abs_path=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
resource_path=os.path.join(abs_path,'resource')

class Pull_animate(QWidget):
    def __init__(self,character_list:list[Character],pull_animate_finish,mute_bgm):
        super().__init__()
        self.character_list=character_list
        self.pull_animate_finish=pull_animate_finish
        self.mute_bgm=mute_bgm
        self.video_list:list[str]=[]
        self.current_index=0
        self.video_list.append(self.judge_path())
        self.video_list.extend(self.find_video_path())
        self.player=QMediaPlayer(self)
        self.audio_output=QAudioOutput(self)
        self.player.setAudioOutput(self.audio_output)
        self.audio_output.setVolume(1)
        self.player.setSource(QUrl.fromLocalFile(os.path.join(resource_path,'video','before_pull_animate.mp4')))
        self.video_widget=QVideoWidget(self)
        self.video_widget.setContextMenuPolicy(Qt.ContextMenuPolicy.NoContextMenu)
        layout=QVBoxLayout(self)
        layout.setContentsMargins(0,0,0,0)
        layout.addWidget(self.video_widget)
        self.player.setVideoOutput(self.video_widget)
        self.player.mediaStatusChanged.connect(self.on_media_status_changed)
        self.flag=False
        self.player.play()
        '''
        self.before_pull_widget=QGraphicsView(self)
        before_picture_path=os.path.join(resource_path,'other','before_pull_picture.png')
        scene=QGraphicsScene()
        pixmap=QPixmap(before_picture_path)
        item=QGraphicsPixmapItem(pixmap)
        if not pixmap.isNull():print('Pixmap非空')
        else:print('Pixmax空')
        scene.addItem(item)
        self.before_pull_widget.setScene(scene)
        self.before_pull_widget.show()
        self.before_pull_widget.raise_()
        '''

    def judge_path(self)->str:
        if len(self.character_list)==1:
            if self.character_list[0].rarity==6:
                return os.path.join(resource_path,'video','one_pull_six_star.mp4')
            elif self.character_list[0].rarity==5:
                return os.path.join(resource_path,'video','one_pull_five_star.mp4')
            else:
                return os.path.join(resource_path,'video','one_pull_four_star.mp4')
        else:
            for character in self.character_list:
                if character.rarity==6:
                    return os.path.join(resource_path,'video','ten_pull_six_star.mp4')
            return os.path.join(resource_path,'video','ten_pull_five_star.mp4')
        
    def find_video_path(self):
        path_list=[]
        for character in self.character_list:
            path_list.append(os.path.join(resource_path,'character_pull_out',f'{character.name}.mp4'))
        return path_list

    def on_media_status_changed(self,status):
        if status==QMediaPlayer.MediaStatus.EndOfMedia:
            self.skip()

    def mouseDoubleClickEvent(self, event: QMouseEvent) -> None:
        event.accept()
        self.player.stop()
        self.pull_animate_finish(self.character_list)

    def mousePressEvent(self, event: QMouseEvent) -> None:
        event.accept()
        if event.button()==Qt.MouseButton.LeftButton:
            if not self.flag:
                self.flag=True
                self.mute_bgm()
            else:
                self.mute_bgm(mute_bool=False)
            self.skip()

    def skip(self):
        if self.current_index<len(self.video_list):
            self.player.setSource(QUrl.fromLocalFile(self.video_list[self.current_index]))
            self.player.play()
            self.current_index+=1
        else:
            self.player.stop()
            self.pull_animate_finish(self.character_list)

class Pull_result_picture(QWidget):
    def __init__(self,character_list:list[Character],pull_result_picture_finish):
        super().__init__()
        self.character_list=character_list
        self.path_list:list[str]=\
            [os.path.join(resource_path,'character_long',f'{character.name}.jpg') for character in character_list]
        self.pull_result_picture_finish=pull_result_picture_finish
        self.graphicsView_1=QGraphicsView(self)
        self.graphicsView_1.setGeometry(0,100,81,401)
        self.graphicsView_2=QGraphicsView(self)
        self.graphicsView_2.setGeometry(80,100,81,401)
        self.graphicsView_3=QGraphicsView(self)
        self.graphicsView_3.setGeometry(160,100,81,401)
        self.graphicsView_4=QGraphicsView(self)
        self.graphicsView_4.setGeometry(240,100,81,401)
        self.graphicsView_5=QGraphicsView(self)
        self.graphicsView_5.setGeometry(320,100,81,401)
        self.graphicsView_6=QGraphicsView(self)
        self.graphicsView_6.setGeometry(400,100,81,401)
        self.graphicsView_7=QGraphicsView(self)
        self.graphicsView_7.setGeometry(480,100,81,401)
        self.graphicsView_8=QGraphicsView(self)
        self.graphicsView_8.setGeometry(560,100,81,401)
        self.graphicsView_9=QGraphicsView(self)
        self.graphicsView_9.setGeometry(640,100,81,401)
        self.graphicsView_10=QGraphicsView(self)
        self.graphicsView_10.setGeometry(720,100,81,401)
        self.view_list:list[QGraphicsView]=[getattr(self,f'graphicsView_{i}') for i in range(1,11)]
        for graphicsview in self.view_list:
            graphicsview.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
            graphicsview.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        for i,view in zip(range(10),self.view_list):
            if i<=len(self.character_list)-1:
                pixmap=QPixmap(self.path_list[i])
                if not pixmap.isNull():
                    scene=QGraphicsScene()
                    item=QGraphicsPixmapItem(pixmap)
                    scene.addItem(item)
                    view.setScene(scene)
                    view.fitInView(item,Qt.AspectRatioMode.KeepAspectRatioByExpanding)
                else:view.setScene(QGraphicsScene())
            else:
                view.setScene(QGraphicsScene())
    
    def mousePressEvent(self, event: QMouseEvent) -> None:
        if event.button()==Qt.MouseButton.LeftButton:
            self.pull_result_picture_finish()