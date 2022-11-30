import requests
import os
from bs4 import BeautifulSoup
import sys
from datetime import datetime
import shutil
import time
import asyncio
import time
import aiohttp
from dotenv import load_dotenv



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
    #     get_domain_rating_result.append(rating_result) 

    # result_file(get_domain_rating_result,output_file_path) 

async def gather_with_concurrency(n):
        semaphore = asyncio.Semaphore(n)
        session = aiohttp.ClientSession(connector=conn)
        # session = aiohttp.ClientSession()

        # heres the logic for the generator
        async def get(url,header,get_domain_rating_result):
            # print(get_domain_rating_result)
            async with semaphore:
                async with session.get(url,headers=header) as response:
                    obj = (await response.read())
                    soup = BeautifulSoup(obj,"html.parser")
                    # ffc = open('www1.html','w')
                    # ffc.write(str(soup))
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
                    for comm in domain_rating:
                        ss = domain_name[j]
                        rating_result = ss + ' = ' + comm.strip()
                        # print(rating_result) 
                        j +=1
                        get_domain_rating_result.append(rating_result)    
        await asyncio.gather(*(get(url,header,get_domain_rating_result) for url in domain_file))
        await session.close()        




if __name__ == "__main__":
    print("scrapt is runnig")
    ScriptPath = os.path.dirname(os.path.realpath(__file__))
    
    if '/' in ScriptPath:
        PathSlash = "/"
    else:
        PathSlash = "\\" 

    load_dotenv(ScriptPath + PathSlash + 's.env')

    ########################## load env variable ###################
    user_agent = os.environ['user_agent']
    cookies = os.environ['cookies']

    ########################### Header define ########################
    header = {
        'referer': 'https://app.ahrefs.com/dashboard',
        'cookie':f'{cookies}',
        'path': '/domain-comparison',
        'user-agent': f'{user_agent}',

        'authority': 'app.ahrefs.com',

           }

    ######################### Folder Path ######################
    
    ScriptPath = os.path.dirname(os.path.realpath(__file__))
    current_time = datetime.now().strftime("%d%m%y") 

    Input_folder = ScriptPath + PathSlash + "Input"
    Output_folder = ScriptPath + PathSlash + 'Output'
    Output_file = Output_folder + PathSlash + current_time + '_output.csv'
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
    # for url in domain_file:
    #     print(url)
    #     get_domain_ratings(url,header,Output_file)


    # Initialize connection pool
    conn = aiohttp.TCPConnector(limit_per_host=100, limit=0, ttl_dns_cache=300)
    PARALLEL_REQUESTS = 10
    results = []
    # urls = [f'https://jsonplaceholder.typicode.com/todos/{i}' for i in range(4)] #array of urls

    start_time = time.time()
    get_domain_rating_result = []
    

    ######################### Concurrency apply ###################
    # asyncio.run(gather_with_concurrency())
    loop = asyncio.get_event_loop()
    loop.run_until_complete(gather_with_concurrency(PARALLEL_REQUESTS))
    conn.close()
    # print("result=",get_domain_rating_result)
    with open(Output_file,'w') as ff4:
        ff4.writelines(i1+"\n" for i1 in get_domain_rating_result)
    duration = time.time() - start_time
    print(f"Completed {len(get_domain_rating_result)}")
    print(f"finish within = {duration} seconds" )