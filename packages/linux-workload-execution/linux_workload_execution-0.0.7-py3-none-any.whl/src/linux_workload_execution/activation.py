#!/usr/bin/env python3 # for running the script like ./python_file_name.py
# -*_ coding: utf-8 -*-
'''
Entry point for the API/Python Program
####################### pip install package ###########################
Python code to take lpar, ipaddress, script directory and
script command as the input .
First step is call the zhmclient to activate the lpar(@srivaishnavi
is working on correct way to activate the lpar) .
Sleep for 10 minutes
ssh to the ipaddress (Linux guest ip address)
cd to the dir(/ffdc/u/eATS_automation) on the ssh session
invoke the script command (sh makeloop.sh) on the ssh session ,
collect the output printed on the ssh session and print it

A02 system ip address: 9.56.198.155
hmc ip address: 9.56.198.101

hmc ip 9.56.198.101 (only required for zhmc) and Linux guest IP address....
SE ip 9.56.198.155 (optional),
'''

# Package Metadata
__author__ = "Girija Golla"
__credits__ = ["Girija Golla"]
__maintainer__ = "Girija Golla"
__email__ = "girija.golla@ibm.com"
__status__ = "Development"
__version__ = "0.0.1"

# import getpass
import json
import logging
import os
import paramiko
import paramiko.ssh_exception
import requests
import subprocess
import time

# Create and configure logger
logging.basicConfig(filename="log_file.log",
                    format='%(asctime)s %(message)s',
                    filemode='w')

# Creating an object
logger = logging.getLogger()

# Setting the threshold of logger to DEBUG
logger.setLevel(logging.DEBUG)


class Activation:
    '''
    LPAR activation using ZHMCCLI Library.
    '''
    def __init__(self, config_file_path):
        '''
        Constructor.
        Args: None
        Returns: None
        '''
        logging.info("***********BEGIN: Constructor***********")
        logging.info("***********reading config details started***********")
        with open(config_file_path, 'r') as file:
            config = json.load(file)
        self.cpc = config.get('cpc')
        self.lpar = config.get('lpar')
        self.hmcm_user_name = config.get('hmcm_user_name')
        self.hmcm_pwd = config.get('hmcm_pwd')
        self.hmc_host = config.get('host_name')
        self.system_host = config.get('system_host')
        self.userid = config.get('userid')
        self.user_pwd = config.get('user_pwd')
        # self.user_pwd = getpass.getpass("Enter your password: ")

        # shell script details
        self.token = config.get('script_details').get('token')
        self.script_name = config.get('script_details').get('name')
        self.script_base_url = config.get('script_details').get('url')
        self.script_exec_path = config.get('script_details').get('exec_path')
        self.script_local_path = config.get('script_details').get('local_path')
        logging.info("***********reading config details completed***********")
        logging.info("***********END: Constructor***********")

    def entry_point(self):
        # returns 0 for success, non-zero for failure
        if self.activate_lpar():
            time.sleep(60)
            # ssh to linux system and run the make_loop.sh,
            # script that is downloaded
            self.ssh_linux_system()
            # activation_obj.deactivate_lpar()
            logging.info("***********END: main***********")

    def activate_lpar(self):
        '''
        activate_lpar.
        Args: None
        Returns: None
        zhmc -n -h 9.56.198.101 -u user@ibm.com lpar activate  A02 SAK59
        '''
        logging.info("***********BEGIN: activate_lpar***********")
        activate_lpar_cmd_str = "zhmc -n -h " + self.hmc_host + \
            " -u " + self.userid + \
            " -p " + self.user_pwd + \
            " lpar activate --allow-status-exceptions --force " + \
            self.cpc + " " + self.lpar
        try:
            result_obj = subprocess.run(activate_lpar_cmd_str,
                                        shell=True,
                                        capture_output=True,
                                        text=True)
            if result_obj.stdout:
                logging.info(f"*********** {result_obj.stdout}***********")
            if result_obj.stderr:
                logging.error(f"*********** {result_obj.stderr}***********")
            return True
        except Exception as e:
            logging.error(f"Exception {e} occured")
            logging.error(f"*********** {result_obj.stderr} ***********")
        logging.info("***********END: activate_lpar***********")
        return False

    def ssh_linux_system(self):
        logging.info("***********BEGING: ssh_linux_system***********")
        ssh_client = paramiko.SSHClient()
        ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        while True:
            try:
                logging.info(f"Trying to connect @ {time.time()}")
                ssh_client.connect(
                    self.system_host,
                    port=22,
                    username=self.hmcm_user_name,
                    password=self.hmcm_pwd)
                logging.info("Connection successful")
                self.download_ssh_script()
                self.upload_ssh_script(ssh_client.open_sftp())
                stdout = ssh_client.exec_command("cd " + self.script_exec_path +\
                                                  " | timeout 120 sh ./" + self.script_name)
                logging.info(f"{stdout}")
                ssh_client.close()
                break
            except paramiko.ssh_exception.SSHException as e:
                logging.error(f"SSH error: {str(e)}")
                time.sleep(10)
                continue
        logging.info("***********END: ssh_linux_system***********")

    def download_ssh_script(self):
        '''
        download sh script file from GitHub using python code.
        Args: None
        Returns: None
        '''
        logging.info("***********BEGIN: download_ssh_script***********")
        # Set up the headers with the token
        headers = {
            'Authorization': f'token {self.token}'
        }
        file_path = self.script_local_path + self.script_name
        try:
            response = requests.get(self.script_base_url + self.script_name,
                                    headers=headers)
            # Check if the request was successful
            if response.status_code == 200:
                with open(file_path,
                          "wb") as file:
                    file.write(response.content)
            logging.info(f"File downloaded: {file_path}")
        except Exception as e:
            logging.error(f"Exception {e} occured")
        logging.info("***********END: download_ssh_script***********")

    def upload_ssh_script(self, ftp_client):
        '''
        upload sh script file to ssh connected machine using python code.
        Args: None
        Returns: None
        '''
        logging.info("***********BEGIN: upload_ssh_script***********")
        file_path = self.script_exec_path + self.script_name
        local_file_path = self.script_local_path + self.script_name
        try:
            if os.path.isfile(local_file_path):
                logging.info("file exists and uploading to host")
                ftp_client.put(local_file_path,
                               file_path)
                logging.info(f"File uploaded: {local_file_path},\
                    to {file_path}")
                logging.info("***********Uploaded successfully***********")
                ftp_client.chmod(file_path, 777)
                ftp_client.chdir(self.script_exec_path)
                ftp_client.listdir(self.script_exec_path)
        except Exception as e:
            logging.error(f"Exception {e} occured")
        logging.info("***********END: upload_ssh_script***********")

    def deactivate_lpar(self):
        '''
        deactivate_lpar.
        Args: None
        Returns: None
        zhmc -n -h 9.56.198.101 -u user@ibm.com lpar deactivate -y \
            --allow-status-exceptions --force  A02 SAK59
        '''
        logging.info("***********BEGIN: deactivate_lpar***********")
        try:
            deactivate_lpar_cmd_str = "zhmc -n -h " + self.hmc_host + \
                " -u " + self.userid + \
                " -p " + self.user_pwd + \
                " lpar deactivate -y --allow-status-exceptions --force " + \
                self.cpc + " " + self.lpar
            result = subprocess.run(deactivate_lpar_cmd_str,
                                    shell=True,
                                    capture_output=True,
                                    text=True)
            logging.info(f"*********** {result.stdout} ***********")
        except Exception as e:
            logging.error(f"Exception {e} occured")
            logging.error(f"*********** {result.stderr} ***********")
        logging.info("***********END: deactivate_lpar***********")


# if __name__ == "__main__":
#     logging.info("***********BEGIN: main***********")
#     if (len(sys.argv) == 2 and os.path.exists(sys.argv[1])):
#         logging.info("***********JSON file provided***********")
#         logging.info(sys.argv[1])
#         activation_obj = Activation(sys.argv[1])
#         activation_obj.entry_point()
#     else:
#         logging.error("***********JSON file not provided***********")
#         logging.error("***********Please provide JSON file***********")
