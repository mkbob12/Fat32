import binascii 
import os, sys, pickle
import argparse, sys 

parser = argparse.ArgumentParser()


def big_endian_to_little_endian(big_endian_data):
     # 빅엔디안 바이너리 데이터의 바이트 순서를 반대로 변경하여 리틀엔디안으로 변환
    num_bytes = len(big_endian_data)
    little_endian_data = b''.join([big_endian_data[num_bytes - i - 1:num_bytes - i] for i in range(num_bytes)])

    return little_endian_data


def bytes_to_int(byte_data):
    # 바이트 문자열을 정수로 변환
    integer_value = int.from_bytes(byte_data, byteorder='big', signed=False)
    return integer_value

def int_to_bytes(integer_value):
    # 정수를 바이트 문자열로 변환
    byte_data = integer_value.to_bytes((integer_value.bit_length() + 7) // 8, byteorder='big', signed=False)
    return byte_data
        


def main(file_path, argv):
    
    with open(file_path, 'rb') as file:
  
        # 지정한 offset만큼 파일 포인터를 이동시킨다.  
        file.seek(14)
        
        # 데이터를 읽기 
        data = file.read()
    
        # FArea 영역 
        FArea = data[0:2]
        FArea = big_endian_to_little_endian(FArea)
                
        # 바이트 문자열을 정수로 변환 
        FArea_int = bytes_to_int(FArea)
        FArea_int = FArea_int * 512 
        
        FArea = int_to_bytes(FArea_int)
        FArea_hex= binascii.hexlify(FArea).decode('utf-8')
        print("File System FArea", FArea_hex)
       
        # 지정한 offset만큼 파일 포인터를 이동시킨다.  
        file.seek(FArea_int)
        
        # 데이터를 읽기 
        data = file.read()
        print("Media_type", data[0:4])
        print("Partition_type", data[4:8])
        
        start = int(argv[1])
        start = int_to_bytes(start * 4)
        start = bytes_to_int(start)
        file.seek(FArea_int + start)
        data = file.read()
        
        
        print(f"{int(argv[1])}" , "시작")
        while(True):

            data = data[0:4]
           
            if (data == b'\xff\xff\xff\x0f') :
                print( "->EOF")
                break

           
            data =  big_endian_to_little_endian(data)
            Data_int= bytes_to_int(data)
            
            # data 출력 
            print("->", Data_int, end="")
            
            Data_int = int_to_bytes(Data_int * 4)
            Data_int= bytes_to_int(Data_int)
            file.seek(FArea_int + Data_int)
            data = file.read()
           
    
if __name__ == "__main__":
    
    file_path = './fat32.dd'
    argv = sys.argv
    main(file_path,argv)