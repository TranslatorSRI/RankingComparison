import requests
import argparse
import os
from datetime import datetime as dt
from logging import Logger
import json

logger = Logger('StriderGenerator')

def post(name,url,message,params=None):
    """Wrap a post in some basic error reporting""" 
    start = dt.now() 
    s = requests.session() 
    if params is None: 
        response = s.post(url,json=message) 
    else: 
        response = s.post(url,json=message,params=params) 
    end = dt.now() 
    if not response.status_code == 200: 
        print(name, 'error:',response.status_code) 
        #print(response.json()) 
        return response.json() 
    print(f'{name} returned in {end-start}s') 
    m = response.json() 
    if 'message' in m: 
        if 'results' in m['message']: 
            print(f'Num Results: {len(m["message"]["results"])}') 
    return m

def strider_dev(message,version='1.2'):
    url = f'http://strider-dev.apps.renci.org/{version}/query'
    strider_answer = post('strider-dev',url,message)
    return strider_answer

def handle_args():
    parser = argparse.ArgumentParser(description='Run queries to produce unscored results')
    parser.add_argument('--dirs', type=str, nargs='+', help='Name of directory containing query.json')
    parser.add_argument('--all',  action='store_true', help='run all queries')
    args = parser.parse_args()
    return args

def is_valid_dir(pdir):
    curr_dir = os.getcwd()
    #is pdir a directory in the current directory?
    testdir = os.path.join(curr_dir,pdir)
    if not os.path.exists(testdir):
        logger.warning(f'Path does not exist: {testdir}')
        return False
    if not os.path.isdir(testdir):
        logger.warning(f'Path is not a directory: {testdir}')
        return False
    query_path = os.path.join(testdir,'query.json')
    if not os.path.exists(query_path):
        logger.warning(f'Path does not contain query.json: {testdir}')
        return False
    return True


def check_dirs(args):
    #if all is set, just get all the dirs and don't worry about what is set in --dirs
    curr_dir = os.getcwd()
    if args.all:
        start_dirs = os.listdir(curr_dir)
    elif args.dirs is not None:
        start_dirs = args.dirs
    else:
        start_dirs = []
    dirs = list(filter( lambda x: is_valid_dir(x), start_dirs ))
    return dirs

def rundir(directory):
    with open(f'{directory}/query.json','r') as inf:
        query = json.load(inf)
    results = strider_dev(query)
    with open(f'{directory}/result.json','w') as outf:
        json.dump(results,outf,indent=4)

def run(args):
    dirs = check_dirs(args)
    for dir in dirs:
        rundir(dir)

if __name__ == '__main__':
    run(handle_args())