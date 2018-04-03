from math import *
from copy import deepcopy

AVG_EARTH_RADIUS = 6371

def haversineDistance(P, Q):
	# Menghitung jarak antar 2 titik koordinat di permukaan bumi
	# Referensi kode dari https://pypi.python.org/pypi/haversine
	# convert titik dari desimal ke radian
	P1 = deepcopy(P)
	P2 = deepcopy(Q)
	P1[0], P1[1], P2[0], P2[1] = map(radians, (P1[0], P1[1], P2[0], P2[1]))
	# haversine process
	y = P2[0] - P1[0]
	x = P2[1] - P1[1]
	a = sin(y * 0.5) ** 2 + cos(P1[0]) * cos(P2[0]) * sin(x * 0.5) ** 2
	result = 2 * AVG_EARTH_RADIUS * asin(sqrt(a))
	return result

def readFile(filename):
	# Membaca sekaligus parsing dari file input untuk membaca koordinat setiap titik dan hubungan antar titik
	fin = open(filename,'r')
	n = int(fin.readline())
	Points = []
	PointName = []
	for i in range (0,n):
		line = fin.readline().split()
		PointName.append(line[0])
		Point = [float(line[1]), float(line[2])]
		Points.append(Point)
	Adjs = []
	for i in range (0,n):
		line = fin.readline().split()
		Adjs.append(line[1:len(line)])
	return Points, PointName, Adjs

def makeAdjMatrix(Points,PointName,Adjs):
	# Membuat Matriks ketetanggan dengan bobotnya adalah jarak
	AdjMat = []
	N = len(Points)
	for i in range(0,N):
		AdjArr = []
		for j in range(0,N):
			if (PointName[j] in Adjs[i]):
				AdjArr.append(haversineDistance(Points[i],Points[j]))
			else:
				AdjArr.append(-999)
		AdjMat.append(AdjArr)
	return AdjMat

def makeHeurMatrix(Points):
	# Membuat Matriks heuristik
	HeurMat = []
	N = len(Points)
	for i in range(0,N):
		HeurArr = []
		for j in range(0,N):
			if (i != j):
				HeurArr.append(haversineDistance(Points[i],Points[j]))
			else:
				HeurArr.append(-999)
		HeurMat.append(HeurArr)
	return HeurMat

Points, PointName, Adjs = readFile("itb.txt")
AdjMat = makeAdjMatrix(Points,PointName,Adjs)
HeurMat = makeHeurMatrix(Points)