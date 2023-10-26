import PyInstaller.__main__

PyInstaller.__main__.run([
    'LivoScore.py',
    '--onefile',
    '--windowed',
    '--clean',
    '-i=/Users/aronkahrs/Desktop/LivoScore/livoscore.ico',
    '-n=LivoScore',
    '--osx-bundle-identifier=com.ak.volley.livoscore',
    '--debug=imports',
    '--add-data=Utils:Utils'
    '--hidden-import=_ssl',
    '--hidden-import=requests,time,json,os,threading,PySimpleGUI,sseclient,flask,ssl,bs4,datetime,obsws_python,platform,lxml,_ssl',
])