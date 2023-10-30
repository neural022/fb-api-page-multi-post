# -*- coding: utf-8 -*-
import json

class Config():
    def __init__(self, file_path):
        self.file_path = file_path

    def load_config(self):
        with open(self.file_path, encoding='utf-8') as f:
            data = json.load(f)
            return data

    def save_config(self, data):
        with open(self.file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f)
                
if __name__ == '__main__':
    config = Config("../config/config.json")

    data = config.load_config()
    print(type(data), data)

    data['api_version'] = '18.0'
    config.save_config(data)

    data = config.load_config()
    print(type(data), data)
