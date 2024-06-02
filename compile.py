import PyInstaller.__main__

PyInstaller.__main__.run([
    'LivoScore.py',
    '--onefile',
    '--windowed',
    '--clean',
    '-i=livoscore.ico',
    '-n=LivoScore',
    '--version-file=file_version_info.txt',
    '--osx-bundle-identifier=com.ak.volley.livoscore',
    '--debug=imports',
    '--add-data=Utils:Utils'
    '--hidden-import=_ssl',
    '--target-architecture=x86_64',
    '--hidden-import=requests,time,json,os,threading,PySimpleGUI,sseclient,flask,ssl,bs4,datetime,obsws_python,platform,lxml,_ssl',
])