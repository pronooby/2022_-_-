import  os,sys,shutil,glob
from PIL import Image


def getBinaryData(filename):
    binaryValues = [] #저장할 바이트값
    file = open(filename, "rb")
    data = file.read(1)  #바이트단위로 읽어들임
    while data !=b"":   #바이트 객체가 존재할때까지 반복
        try:
            binaryValues.append(ord(data))  
        except TypeError:
            pass
        data = file.read(1)  


    return binaryValues

def createGreyScaleImageSpecificWith(dataSet,outputfilename,width=0):

	if (width == 0): # 따로 지정하지 않았을때
		size = len(dataSet)   # 입력된 바이너리 파일 문자의 개수

		if (size < 10240) :
			width = 32
		elif (10240 <= size <= 10240*3 ):
			width = 64
		elif (10240*3 <= size <= 10240*6 ):
			width = 128
		elif (10240*6 <= size <= 10240*10 ):
			width = 256
		elif (10240*10 <= size <= 10240*20 ):
			width = 384
		elif (10240*20 <= size <= 10240*50 ):
			width = 512
		elif (10240*50 <= size <= 10240*100 ):
			width = 768
		else :
			width = 1024

	height = int(size/width)+1   #소수가 되어 짤릴 수 있으므로 +패딩

	image = Image.new('L', (width,height))  # 이미지 생성 함수 "L은 흑백"

	image.putdata(dataSet) # 바이너리로 이미지 생성

	imagename = outputfilename+".png"
	image.save(imagename) #이미지 저장

def filecheck():

    path = os.path.dirname(os.path.abspath(__file__))
    p=[]
    for file in os.listdir():

        if os.path.isfile(file):
            p.append(os.path.abspath(file))
        if os.path.isdir(file):
            pass
    return p

if __name__=="__main__":
    p=filecheck()
    folder_name = str(input())
    current_path = os.getcwd()  # 현재 경로 가지고오기
    os.mkdir(current_path + "/" + folder_name)  # 현재 경로 + 폴더명 입력

    for i in p:
        file_full_path=i
        path=os.path.dirname(file_full_path) #경로의 형태는 'C;/~폴더명'
        base_name=os.path.splitext(os.path.basename(file_full_path))[0] #파일명(확장자 제거된)
        outputFilename=os.path.join(path,base_name) #지정경로/파일명

        binaryData=getBinaryData(file_full_path)  #파일을 바이너리데이터로
        createGreyScaleImageSpecificWith(binaryData, outputFilename) #바이너리 크기, 작성될 파일의 이름

    imagefiles = glob.iglob(os.path.join(os.path.dirname(os.path.abspath(__file__)), "*.png"))
    for j in imagefiles:
        if os.path.isfile(j):
            shutil.move(j, folder_name)   #폴더에 이미지 저장

#수정. 실행하면 파일명을 입력하고 대기
