import requests
import glob
import os
from bs4 import BeautifulSoup
import json
import argparse
import tempfile
import re

class NateeScraper():
    def __init__(self, uid: str, password: str, root_url="https://2110104.nattee.net/") -> None:
        self.root_url = root_url
        self.login_url = f"{root_url}/login/login"
        self.data = {
            'utf8': '✓', # constant
            'authenticity_token': None, # get from index page
            'login': uid, # change this to your username
            'password': password, # change this to your password
            'commit': 'login', # constant
        }
        self.session = requests.Session()
        index_page= self.session.get(self.root_url)
        ruby_authenticity_token = BeautifulSoup(index_page.text, 'html.parser').find('input', attrs={'name': 'authenticity_token'})['value']
        self.data['authenticity_token'] = ruby_authenticity_token
        # -- perform login --
        response = self.session.post(self.login_url , data=self.data)
        if 'Wrong password' in response.text:
            raise ValueError("Wrong password")
        print("Login success...")

    def __get_testcases_link(self, quiz_link: str) -> str:
        return quiz_link.replace("/submissions/direct_edit_problem/", "/testcases/show_problem/")

    def __get_testcases(self, quiz_link:str):
        test_case_link = self.__get_testcases_link(quiz_link)
        response = self.session.get(test_case_link)
        soup = BeautifulSoup(response.text, 'html.parser')
        testcases = soup.find_all('textarea')
        inputs = []
        outputs = []
        for idx, cases in enumerate(testcases):
            if idx % 2 == 0:
                inputs.append(cases.text)
            else:
                outputs.append(cases.text)
        
        cases = list(zip(inputs, outputs))
        return cases

    def create_testcase(self, cpp_path: str, quiz_link: str):
        def single_test_case(id:int, input: str, output: str):
            return {
                'id': id,
                'input': input,
                'output': output
            }

        cases = self.__get_testcases(quiz_link)
        fname = os.path.basename(cpp_path)
        root_dir = os.path.dirname(cpp_path)
        cph_folder_path = os.path.join(root_dir, '.cph')
        start_with = f'.{fname}_'
        cph_file = list(glob.glob(f'{cph_folder_path}/{start_with}*'))
        if len(cph_file) == 0:
            raise ValueError(f"You must initialize CPH config file for '{cpp_path}' file first, Via CPH extension in vscode")
        cph_file = cph_file[0]
        # generate test case
        test_cases = [single_test_case(idx, case[0], case[1]) for idx, case in enumerate(cases)]
        # read as json
        data = json.load(open(cph_file, 'r'))
        data['tests'] = test_cases
        # write back
        json.dump(data, open(cph_file, 'w'), indent=4)
        print("< --- Testcases created! --- >")
        print(f"Containing {len(test_cases)} testcases")
        return None

    def path_validator(self, cpp_path: str, quiz_link: str):
        if not cpp_path.endswith('.cpp') and os.path.isfile(cpp_path):
            raise ValueError("Please provide AN 'ACTUAL' .cpp file")
        
        # Ex. https://2110104.nattee.net//submissions/direct_edit_problem/[number]
        # check if quiz_link is valid via regex
        if not re.match(f'{self.root_url}submissions/direct_edit_problem/\d+', quiz_link):
            raise ValueError("Please provide a valid quiz link")
        return None

folder_cache = f'{tempfile.gettempdir()}/.natee_scraper/'
usr_cache = f'{folder_cache}/usrcache.cedt'
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Natee Scraper')
    parser.add_argument('cpp_path', type=str, help='Your cpp file path')
    parser.add_argument('quiz_link', type=str, help='Your quiz link')
    parser.add_argument('--uid', type=str, help='Your NatteeGrader username', default=None, required=False)
    parser.add_argument('--password', type=str, help='Your NatteeGrader password', default=None, required=False)
    args = parser.parse_args()

    if not os.path.exists(folder_cache):
        os.makedirs(folder_cache, exist_ok=True)
    if args.uid is not None and args.password is not None:
        json.dump({'uid': args.uid, 'password': args.password}, open(usr_cache, 'w'), indent=4)
        print("Cached usr data at:", usr_cache)

    notice = "Please provide username and password via --uid and --password flag"
    if not os.path.exists(usr_cache):
        raise ValueError(notice)
    
    usr_cache = json.load(open(usr_cache, 'r'))
    if usr_cache['uid'] is None or usr_cache['password'] is None:
        raise ValueError(notice)
    else:
        args.uid = usr_cache['uid']
        args.password = usr_cache['password']

    scraper = NateeScraper(args.uid, args.password)
    scraper.path_validator(args.cpp_path, args.quiz_link)
    print("Path Validated...")
    print("Creating test case...")
    scraper.create_testcase(args.cpp_path, args.quiz_link)