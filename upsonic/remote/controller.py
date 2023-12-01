#!/usr/bin/python3
# -*- coding: utf-8 -*-

import json
import ast



class Upsonic_Remote:
    def _log(self, message):
        self.console.log(message)

    def __enter__(self):
        return self  # pragma: no cover

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass  # pragma: no cover

    def __init__(self, database_name, api_url, password=None, enable_hashing:bool=False, verify=True, locking=False, client_id=None):
        import requests
        from requests.auth import HTTPBasicAuth


        self.force_compress = False
        self.force_encrypt = False
        self.locking = locking
        self.enable_hashing = enable_hashing

        self.client_id = client_id

        self.verify = verify

        from upsonic import console

        self.console = console


        self.requests = requests
        self.HTTPBasicAuth = HTTPBasicAuth


        self.database_name = database_name
        self._log(
            f"[{self.database_name[:5]}*] [bold white]Upsonic Cloud[bold white] initializing...",
        )
        
        if self.client_id is not None:
            self._log(f"[{self.database_name[:5]}*] [bold white]Client ID[bold white]: {self.client_id}")
        from upsonic import encrypt, decrypt
        self.encrypt = encrypt
        self.decrypt = decrypt


        self.api_url = api_url
        self.password = password

        try:
            self.informations = self._informations()
        except TypeError:
            self.informations = None

        self._log(
            f"[{self.database_name[:5]}*] [bold green]Upsonic Cloud[bold green] active",
        )
        self._log("---------------------------------------------")

    def _informations(self):
        return self._send_request("GET", "/informations", make_json=True)

    def debug(self, message):
        data = {"message": message}
        return self._send_request("POST", "/controller/debug", data)

    def info(self, message):
        data = {"message": message}
        return self._send_request("POST", "/controller/info", data)

    def warning(self, message):
        data = {"message": message}
        return self._send_request("POST", "/controller/warning", data)

    def error(self, message):
        data = {"message": message}
        return self._send_request("POST", "/controller/error", data)

    def exception(self, message):
        data = {"message": message}
        return self._send_request("POST", "/controller/exception", data)

    def _send_request(self, method, endpoint, data=None, make_json=False):
        try:
            response = self.requests.request(
                method,
                self.api_url + endpoint,
                data=data,
                auth=self.HTTPBasicAuth("", self.password),
                verify=self.verify
            )
            try:
                response.raise_for_status()
                return response.text if not make_json else json.loads(response.text)
            except self.requests.exceptions.RequestException as e:  # pragma: no cover
                print(f"Error on '{self.api_url + endpoint}': ", response.text)
                return None  # pragma: no cover
        except self.requests.exceptions.ConnectionError:
            print("Error: Remote is down")
            return None


    def _lock_control(self, key, locking_operation=False):
        result = self.get(key+"_lock")
        if result is not None:
            if result == self.client_id and not locking_operation:
                return False
            return True
        return False
  

    def lock_control(self, key):
        if self.locking:
            return self._lock_control(key)
        else:
            return False

    def lock_key(self, key):
        if self._lock_control(key, locking_operation=True):
            self.console.log(f"[bold red] '{key}' is already locked")
            return False

        if self.set(key+"_lock", self.client_id, locking_operation=True) == "Data set successfully":
            self.console.log(f"[bold green] '{key}' is locked")
            return True
        else:
            return False

    def unlock_key(self, key):
        result = self._lock_control(key, locking_operation=True)
        if not result:
            self.console.log(f"[bold red] '{key}' is already unlocked")
            return False
        
        if self._lock_control(key):
            self.console.log(f"[bold red] '{key}' is locked by another client")
            return False

    

        if self.delete(key+"_lock") == "Data deleted successfully":
            self.console.log(f"[bold green] '{key}' is unlocked")
            return True
        else:         
            return False

    def set(self, key, value, encryption_key="a", compress=None, cache_policy=0, locking_operation=False):
        if not locking_operation:
            if self.lock_control(key):
                self.console.log(f"[bold red] '{key}' is locked")
                return None


        compress = True if self.force_compress else compress
        encryption_key = (
            self.force_encrypt if self.force_encrypt != False else encryption_key
        )

        if encryption_key is not None:

            value = self.encrypt(encryption_key, value)

        data = {
            "database_name": self.database_name,
            "key": key,
            "value": value,
            "compress": compress,
            "cache_policy": cache_policy,
        }
        return self._send_request("POST", "/controller/set", data)

    def get(self, key, encryption_key="a"):
        encryption_key = (
            self.force_encrypt if self.force_encrypt != False else encryption_key
        )

        data = {"database_name": self.database_name, "key": key}
        response = self._send_request("POST", "/controller/get", data)

        if response is not None:
            if not response == "null\n":
                # Decrypt the received value
                if encryption_key is not None:
                    try:
                        response = self.decrypt(encryption_key, response)
                    except:
                        pass                    
                return response
            else:
                return None

    def active(self, value=None, encryption_key="a", compress=None):
        def decorate(value):
            key = value.__name__
            self.set(key, value, encryption_key=encryption_key, compress=compress)

        if value == None:
            return decorate
        else:
            decorate(value)
            return value

    def get_all(self, encryption_key="a"):
        encryption_key = (
            self.force_encrypt if self.force_encrypt != False else encryption_key
        )

        data = {"database_name": self.database_name}
        datas = self._send_request("POST", "/controller/get_all", data)

        datas = json.loads(datas)

        for each in datas:
            if encryption_key is not None:
                try:
                    datas[each] = self.decrypt(encryption_key, datas[each])
                except:
                    pass


        return datas

    def delete(self, key):
        data = {"database_name": self.database_name, "key": key}
        return self._send_request("POST", "/controller/delete", data)

    def database_list(self):
        return ast.literal_eval(self._send_request("GET", "/database/list"))


    def database_rename(self, database_name, new_database_name):
        data = {"database_name": database_name, "new_database_name": new_database_name}
        return self._send_request("POST", "/database/rename", data)


    def database_pop(self, database_name):
        data = {"database_name": database_name}
        return self._send_request("POST", "/database/pop", data)

    def database_pop_all(self):
        return self._send_request("GET", "/database/pop_all")

    def database_delete(self, database_name):
        data = {"database_name": database_name}
        return self._send_request("POST", "/database/delete", data)

    def database_delete_all(self):
        return self._send_request("GET", "/database/delete_all")
