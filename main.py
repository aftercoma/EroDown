#!/usr/bin/python3.14

from requests import *
from re import *
from time import sleep as turu
from bs4 import BeautifulSoup as bs 
from tqdm import tqdm
from pathlib import Path
from etc import headers as hd
from temp import banner
from subprocess import *
import os, shutil

linkimg = []
linkvid = []
hothot = [
        r'https://(.*?)',
        r'data-src="(.*?)">'
        ]
class getcl:
    global dumpy
    global linkimg
    global linkvid
    def __init__(self,target):
        self.sesion = Session();self.sesion.headers.update(
                hd.head().less
                )
        self.target = target 
        self.get = self.sesion.get(self.target)        
        if self.get.status_code == 200:
            print ('sukses')
            self.scrap()
        else:
            print ('gagal memuat targt!')
            pass
    def scrap(self):
        self.bs = bs(self.get.text, 'html.parser');self.judul=self.bs.title.string 
        print(f"Target: {self.judul}")
        print ("Mencari link img dan mp4...")
        turu(3)
        for a_tag in self.bs.find_all('div', class_='media-group'):
            self.strconvert = str(a_tag)
            self.re=(findall(r'data-src="(.*?)">', self.strconvert))
            for yaya in self.re:
                linkimg.append(yaya)
        for b_tag in self.bs.find_all('div', class_='video-lg'):
            self.video_div = b_tag.find("video")
            self.sourc = self.video_div.find('source')
            self.find = self.sourc.get('src')
            self.str2convert = str(self.find)
            linkvid.append(self.str2convert)
        if len(linkimg) > 1:
            print (f"img di temukan! : [{len(linkimg)}]")
            if len(linkvid) > 1:
                print (f"vid ditemukan! : [{len(linkvid)}]")
                self._eroDown()
        else:
            print("cek internet anda!")
            exit()
    def _eroDown(self):
        print("sedang mendownload img0")
        self.folder = Path('img')
        self.folder.mkdir(parents=True,exist_ok=True)
        for i,url in enumerate(tqdm(linkimg, desc="Total img", unit="img", position=0), start=1):
            self.path = self.folder / f"{self.judul}{i}.jpg"
            with self.sesion.get(url, stream=True) as respon:
                respon.raise_for_status()
                self.total = int(respon.headers.get("Content-Length", 0))
                with open(self.path, 'wb') as img, tqdm(
                    desc=self.path.name,
                    total=self.total or None,
                    unit="B",
                    unit_scale=True,
                    unit_divisor=1024,
                    position=1,
                    leave=False,) as bar:
                    for chunk in respon.iter_content(8191):
                            if chunk:
                                img.write(chunk)
                                bar.update(len(chunk))
        print ("selesai!")
        ask = input("Lanjut untuk download video? y/N: ")
        if ask == "y":
            self._getVid()
        else:
            pass
    def _getVid(self):
        print("sedang mendownload video...")
        self.folder1 = Path("vid")
        self.folder1.mkdir(parents=True, exist_ok=True)
        for y,url in enumerate(tqdm(linkvid, desc="Total vid", unit="vid", position=0), start=1):
            self.path1 = self.folder1 / f"{self.judul}{y}.mp4"
            with self.sesion.get(url, stream=True) as respone:
                self.totale = int(respone.headers.get("Content-Length", 0))
                respone.raise_for_status()
                with open(f"{self.judul}{y}.mp4", 'wb') as mp, tqdm(
                        desc=self.path1.name,
                        total=self.totale or None,
                        unit="B",
                        unit_scale=True,
                        unit_divisor=1024,
                        position=1,
                        leave=False,
                        ) as barr:
                    for chunkk in respone.iter_content(8191):
                        if chunkk:
                            mp.write(chunkk)
                            barr.update(len(chunkk))





        


if __name__=='__main__':
    try:
        banner.menu()
        while True:
                raw = input("type anything:~> ")
                if "https" in raw:
                    try:
                        getcl(raw)
                    except KeyboardInterrupt:
                        print ("Download Stopped Bcs CTRL+C")
                        pass
                    except exceptions.HTTPError as http_err:
                        print(f"HTTP error occurred: {http_err}")
                        pass
                    except exceptions.ConnectionError as conn_err:
                        print(f"Connection error occurred: {conn_err}")
                        pass


                if "ex" in raw:
                    print ("did u mean (exit) ?")
                if "clear" in raw:
                    run(['clear'], shell=True)
                    banner.menu();print("\n")
                elif "exit" in raw:
                    exit()
                else:
                    pass
    except KeyboardInterrupt:
        print ("KeyboardInterrupt tools has ended.");exit()

