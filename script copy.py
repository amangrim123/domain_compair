import requests
import os
from bs4 import BeautifulSoup
import sys
from datetime import datetime
import shutil
import time

header = {
    # 'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36',
    'referer': 'https://app.ahrefs.com/dashboard',
    'cookie':'_pk_id.3.a4f6=adc794d471db2510.1665461489.; G_ENABLED_IDPS=google; _pk_id.1.a4f6=88dae2a9ad700a01.1665806907.; __cf_bm=SSsxV6SpG0uoQWtkN9jlIZwAUjReODnr7cnchRJVy80-1669280495-0-AdVW9K7oIV0pOfMLa552WUqGLQrlCWUV/jGgSFRm+yTKZt2jM+weHckuJE5Vlw5UZirXyiozTjEoc/EJrnxv1mU=; __cflb=0H28vHpvobBxLDNMFZkKZZyfCfB62J4DT4HYAj9Ci1A; _pk_ref.3.a4f6=%5B%22%22%2C%22%22%2C1669280501%2C%22https%3A%2F%2Fahrefs.com%2F%22%5D; _pk_ses.3.a4f6=1; BSSESSID=makeRpR%2Bfj2Jx%2Bg2H%2FO4fg5veNjnsGqUaRrgR2Lp; intercom-device-id-dic5omcp=f8d43aa0-5767-4fcf-b0fb-47e3384b8ec6; _pk_ses.1.a4f6=1; intercom-session-dic5omcp=OC9MeGZlbHNCWEgrUVNmYVNPYjVlaXN1VUtLMElhZ1luT2VnUFFWKzBaTFZxNzdqZFNYK0VUWkJWSXc3cjA4UC0tUmRTOFI2Vi9hMXh1S1BkZjFmeTVCQT09--2f116f61ae1ac8057811c67e5b922e8088f4eef1',
    'path': '/domain-comparison',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36 Edg/107.0.1418.56',

    'authority': 'app.ahrefs.com',


}

def Creat_query(Input_file_path,temp_file_path):
    domain_list = []
    file = open(Input_file_path,'r')

    for domain in file:
        domain_list.append(domain.replace("\n",''))

    domain_query = []
    for i in range(int(len(domain_list)/5)):
        star = (i*5)
        end = (i+1)*5
        ss = domain_list[star:end]
        try:
            query_url = f"https://app.ahrefs.com/domain-comparison?targets%5B%5D={ss[0]}&targets%5B%5D={ss[1]}&targets%5B%5D={ss[2]}&targets%5B%5D={ss[3]}&targets%5B%5D={ss[4]}"
            query_u = query_url.replace('"','')
            domain_query.append(query_u)
        except:
            pass    


    with open(temp_file_path,'w') as ff1:
        ff1.writelines(i+"\n" for i in domain_query)

    return print("=========== create query successfully ============")        


def result_file(do_file,ouput_file_path):
    with open(ouput_file_path,'a') as file1:
        file1.writelines(i+"\n" for i in do_file)



def get_domain_ratings(domain_url,aheader,output_file_path):
    aa = requests.get(domain_url,headers=aheader)
    soup = BeautifulSoup(aa.content,"html.parser")
    ffc = open('www1.html','w')
    ffc.write(str(soup))

    get_domain_name = soup.find(class_="bg-faded")

    # print(get_domain_name.find('td').find("input")['value'])
    get_domain_value = get_domain_name.find_all('td')

    domain_name = []

    for i in get_domain_value:
        domain_name.append(i.find('input')['value'])


    # start form here    
    get_domain_rating = soup.find(class_="table table-ahrefs table-ahrefs-domain-comparison table-ahrefs-thin").find('tbody').find('tr')
    
    domain_rating = []

    for ii in get_domain_rating.find_all(class_='text-xs-right'):
        dd = (ii.find('span').text).replace('  ','')
        domain_rating.append(dd)

    j = 0
    get_domain_rating_result = []
    for comm in domain_rating:
        ss = domain_name[j]
        rating_result = ss + ' = ' + comm.strip()
        print(rating_result) 
        j +=1
        # print(comm.strip()) 
        get_domain_rating_result.append(rating_result) 

    result_file(get_domain_rating_result,output_file_path) 
        




if __name__ == "__main__":
    print("scrapt is runnig")

    ######################### Folder Path ######################
    
    ScriptPath = os.path.dirname(os.path.realpath(__file__))
    current_time = datetime.now().strftime("%d%m%y")

    if '/' in ScriptPath:
        PathSlash = "/"
    else:
        PathSlash = "\\"  

    Input_folder = ScriptPath + PathSlash + "Input"
    Output_folder = ScriptPath + PathSlash + 'Output'
    Output_file = Output_folder + PathSlash + current_time + '_Domains_Compair.csv'
    Temp_folder = ScriptPath + PathSlash + 'Temp'
    Temp_file = Temp_folder + PathSlash + 'query.csv'


    ########################## Create Quary ####################
    print('1. -------------Create temp folder--------------- ') 
    ######################## delete old temp folder ##################
    if os.path.exists(Temp_folder):
        shutil.rmtree(Temp_folder)
    ############################# Create New Temp Folder ###############
    time.sleep(10)
    if os.path.exists(Temp_folder) != None:
        os.mkdir(Temp_folder)    
    try:
        input_file = Input_folder + PathSlash + os.listdir(Input_folder)[0]
        Creat_query(input_file,Temp_file)
    except:
        print("Opps! No found Input file. Please upload file in Input file")
        sys.exit()

    print('2. ============= Find Domains Rating =========== ')    

    domain_file = open(Temp_file,'r')
    for url in domain_file:
        print(url)
        get_domain_ratings(url,header,Output_file)


