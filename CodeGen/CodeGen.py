# -*- coding: utf-8 -*-
import webview
import json
import os
import subprocess
import re
import socket
import sys

def get_base_path():
    if getattr(sys, 'frozen', False):
        return os.path.dirname(sys.executable)
    return os.path.dirname(os.path.abspath(__file__))

DATA_FILE = os.path.join(get_base_path(), 'data.json')

DEFAULT_DATA = {
    "companies": [
        {"name": "ADR Holdings", "code": "AR"},
        {"name": "Inland Airfreight and Logistic Division", "code": "IA"},
        {"name": "Inland Corporation", "code": "IC"},
        {"name": "Inland Corporation Project and Heavy Lift", "code": "PH"},
        {"name": "Inland Warehousing and Logistics Division", "code": "IW"},
        {"name": "SB Inland Corporation", "code": "SB"},
        {"name": "Technofreeze, Inc.", "code": "TF"}
    ],
    "units": [
        {"name": "Accounting", "code": "A1"},
        {"name": "Audit", "code": "A2"},
        {"name": "ADRH", "code": "A3"},
        {"name": "Brokerage", "code": "B1"},
        {"name": "Building Maintenance", "code": "B2"},
        {"name": "Common", "code": "C1"},
        {"name": "Container Yard", "code": "C2"},
        {"name": "Contract Logistics", "code": "C3"},
        {"name": "Forwarding", "code": "F1"},
        {"name": "Human Resources", "code": "H1"},
        {"name": "Maintenance", "code": "M1"},
        {"name": "Management Information Systems", "code": "M2"},
        {"name": "Office of the President", "code": "O1"},
        {"name": "Operations", "code": "O2"},
        {"name": "OpEx", "code": "O3"},
        {"name": "Parts Trading", "code": "P1"},
        {"name": "Procurement", "code": "P2"},
        {"name": "Safety and Security", "code": "S1"},
        {"name": "Sales and Business Development", "code": "S2"},
        {"name": "Strategic Operation and Procurement", "code": "S3"},
        {"name": "Trucking", "code": "T1"}
    ],
    "sites": [
        {"name": "Batangueno", "code": "B1"},
        {"name": "Bulacan", "code": "B2"},
        {"name": "Cagayan De Oro Garage", "code": "C1"},
        {"name": "Cagayan De Oro Nestle Factory", "code": "C2"},
        {"name": "Cagayan De Oro Office", "code": "C3"},
        {"name": "Canlubang Factory Genpacco", "code": "C3"},
        {"name": "Canlubang Factory Wyeth", "code": "C4"},
        {"name": "Cebu Garage", "code": "C5"},
        {"name": "Cebu Office", "code": "C6"},
        {"name": "Davao Office", "code": "D1"},
        {"name": "Davao Warehouse", "code": "D2"},
        {"name": "DHL", "code": "D3"},
        {"name": "Head Office", "code": "H1"},
        {"name": "Laguna", "code": "L1"},
        {"name": "Lancaster", "code": "L2"},
        {"name": "Lipa Factory", "code": "L3"},
        {"name": "Pier 18", "code": "P1"},
        {"name": "Pulo", "code": "P2"},
        {"name": "Paranaque", "code": "P3"},
        {"name": "Subic", "code": "S1"},
        {"name": "Sucat", "code": "S2"},
        {"name": "Tanauan Factory", "code": "T1"},
        {"name": "Zamboanga", "code": "Z1"}
    ]
}

class Api:
    def __init__(self):
        self.data = {}
        self.load_data()

    def load_data(self):
        if os.path.exists(DATA_FILE):
            try:
                with open(DATA_FILE, 'r', encoding='utf-8') as f:
                    self.data = json.load(f)
            except Exception:
                self.data = DEFAULT_DATA.copy()
        else:
            self.data = DEFAULT_DATA.copy()
            self.save_data()
        return self.data

    def get_data(self):
        return self.data

    def save_data(self):
        try:
            with open(DATA_FILE, 'w', encoding='utf-8') as f:
                json.dump(self.data, f, indent=4)
            return True
        except Exception:
            return False

    def add_item(self, category, name, code):
        if category in self.data:
            self.data[category].append({"name": name, "code": code})
            self.save_data()
            return True
        return False

    def delete_item(self, category, index):
        if category in self.data and 0 <= index < len(self.data[category]):
            self.data[category].pop(index)
            self.save_data()
            return True
        return False

    def get_serial_number(self):
        try:
            command = ["powershell", "-Command", "Get-CimInstance Win32_BIOS | Select-Object -ExpandProperty SerialNumber"]
            result = subprocess.check_output(command, universal_newlines=True, stderr=subprocess.DEVNULL)
            serial = result.strip()
            if serial:
                return serial
        except Exception:
            pass
        return "0000000"

    def get_hostname(self):
        try:
            return socket.gethostname().strip()
        except:
            return ""

    def generate_id(self, company_code, unit_code, site_code):
        serial = self.get_serial_number()
        cleaned = re.sub(r"\s+", "", serial)
        if len(cleaned) > 7:
            last_7 = cleaned[-7:]
        else:
            last_7 = cleaned.zfill(7)
        return f"{company_code}{unit_code}{site_code}{last_7}"

    def copy_to_clipboard(self, text):
        try:
            process = subprocess.Popen("clip", stdin=subprocess.PIPE, shell=True)
            process.communicate(input=text.encode("utf-8"))
            return True
        except Exception:
            return False

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

if __name__ == '__main__':
    api = Api()
    html_file = resource_path('index.html')
    webview.create_window('CodeGen', f'file://{html_file}', js_api=api, width=900, height=700)
    webview.start()