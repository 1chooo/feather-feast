# -*- coding: utf-8 -*-
'''
Create Date: 2023/07/26
Author: @1chooo(Hugo ChunHo Lin)
Version: v0.0.2
'''

import os

def check_dir(file_path) -> None:

    if not os.path.isdir(file_path):
        os.mkdir(file_path, mode=0o777)
        print(file_path, 'has been created successfully.')

    return None

def get_output_path(file_path, current_date, id, type) -> str:

    output_path = file_path + current_date + '_' + id + type

    return output_path


def getDomainUrl(SERVER_DOMAIN_URL) -> str:

    SERVER_DOMAIN_URL = str(input('Please input your current server domain: '))

    return SERVER_DOMAIN_URL


def getImageDomainUrl(IMAGE_SERVER_DOMAIN_URL) -> str:

    IMAGE_SERVER_DOMAIN_URL = str(input('Please input your current IMAGE server domain: '))

    return IMAGE_SERVER_DOMAIN_URL