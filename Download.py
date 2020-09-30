from PyQt5.QtWidgets import *
from PyQt5.uic import *
from PyQt5 import QtGui
from os import path
import youtube_dl
import humanize
import pafy
import sys
import os
import urllib.request
import fbdown
#Connect The Ui With Code

from UI import Ui_MainWindow as Main

appStyle="""
QMainWindow{    
background-color: darkgray;
}
"""
#The App
class MainApp(QMainWindow, Main):
    def __init__(self,parent=None):
        super(MainApp,self).__init__(parent)
        QMainWindow.__init__(self)
        self.setupUi(self)
        self.Handel_Ui()
        self.Handel_button()
        self.setStyleSheet(appStyle)
            
    
    #UI Sttings
    def Handel_Ui(self):
        self.setWindowTitle('Hogo Downloder')
        self.setFixedSize(781,341)

    #Any File Download progress bar
    def Handel_progress(self , blocknum , blocksize , totalsize):
        read = blocknum * blocksize
        if totalsize > 0 :
            percent = read * 100 / totalsize
            self.progressBar.setValue(percent)


    #Any File Download Save Location browse
    def Handel_Browse(self):
        save_place = QFileDialog.getSaveFileName(self ,caption="Save As" , directory="." , filter="All File (*.*)")
        x = str(save_place[0])
        self.saving_location.setText(x)


    #Clicked Button Action
    def Handel_button(self):
        self.download.clicked.connect(self.Download)
        self.browse.clicked.connect(self.Handel_Browse)
        self.download_2.clicked.connect(self.YoutubeDownload)
        self.search_video.clicked.connect(self.SearchVideo)
        self.browse_2.clicked.connect(self.SaveVideo)
        self.download_3.clicked.connect(self.Playlist_Download)
        self.browse_3.clicked.connect(self.Playlist_Save_Browse)

    #Any Download Function 
    def Download(self):
        Url = self.url.text()
        Save_location = self.saving_location.text()
        try:
            urllib.request.urlretrieve(Url,Save_location,self.Handel_progress)
            self.url.setText('')
            self.progressBar.setValue(0)
            QMessageBox.information(self,"root","Download Finished")
            return
        except Exception:
            QMessageBox.warning(self,"Warning", "Download url is not Valid")
    
    
    #Video Download Function to get video info
    def SearchVideo(self):
        video_link = self.youtube_url.text()
        video = pafy.new(video_link)
        streams = video.allstreams
        for stream in streams:
            Value = humanize.naturalsize(stream.get_filesize())
            data = "{} {} {}  {} " .format(stream.mediatype,stream.extension,stream.quality,Value)
            self.videoquality.addItem(data)
        self.video_name.setText(video.title)
    
    
    #video Download to download The Video
    def YoutubeDownload(self):
        video_link = self.youtube_url.text()
        save_loaction = self.saving_location_2.text()
        v = pafy.new(video_link)
        st = v.allstreams
        quality = self.videoquality.currentIndex()

        down = st[quality].download(filepath = save_loaction,callback=self.doww)
        QMessageBox.information(self,"Hogo Download","Download Finished")
        
    
    #video download To save video Location
    def SaveVideo(self):
        save = QFileDialog.getExistingDirectory(self,"Select Download Folder")
        self.saving_location_2.setText(save)
        self.saving_location_3.setText(save)
    
    def Playlist_Progress(self , total , received , ratio , rate , time):
        read_data = received
        if total > 0 :
            download_percentage = read_data * 100 / total
            self.progressBar_3.setValue(download_percentage)
            remaining_time = round(time/60 , 2)

            self.label_3.setText(str('{} minutes remaining'.format(remaining_time)))
            QApplication.processEvents()
    def Playlist_Download(self):
        playlist_url = self.PlaylistUrl.text()
        save_location = self.saving_location_3.text()

        if playlist_url == '' or save_location == '' :
            QMessageBox.warning(self, "Data Error", "Provide a valid Playlist URL or save location")

        else:
            playlist = pafy.get_playlist(playlist_url)
            playlist_videos = playlist['items']


        os.chdir(save_location)
        if os.path.exists(str(playlist['title'])):
            os.chdir(str(playlist['title']))

        else:
            os.mkdir(str(playlist['title']))
            os.chdir(str(playlist['title']))

        current_video_in_download = 1
        quality = self.videoquality_2.currentIndex()


        QApplication.processEvents()

        for video in playlist_videos :
            current_video = video['pafy']
            current_video_stream = current_video.videostreams
            download = current_video_stream[quality].download(callback=self.Playlist_Progress)
            QApplication.processEvents()

            current_video_in_download +=1

    def Playlist_Save_Browse(self):
        playlist_save_location = QFileDialog.getExistingDirectory(self , "Select Download Directory")
        self.saving_location_3.setText(playlist_save_location)

    def doww(self, total, recvd, ratio, rate, eta):
        k = recvd / total
        suo = k * 100
        self.progressBar_2.setValue(suo)

#run The app
def main():
    app = QApplication(sys.argv)
    window = MainApp()
    window.show()
    app.exec_()
if __name__ == '__main__':
    main()