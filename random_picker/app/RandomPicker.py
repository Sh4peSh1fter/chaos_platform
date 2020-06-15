import requests
import random
import json
from flask import Flask, request
import os

class Picker:
    def __init__(self, pick_interval = 300, group_pick = "all", db_host = "52.255.160.180", queue_size = 1):
        self.pick_interval = pick_interval
        self.group_pick = group_pick
        self.__db_host = db_host
        self.__queue_size = queue_size
        self.servers_queue = []

    # This function add server to queue of servers that have been injected recently.
    def add_server_to_queue(self, new_server):
        if self.servers_queue.length() == self.__queue_size:
            self.servers_queue.pop(0)
            self.servers_queue.append(new_server)
        else:
            self.servers_queue.append(new_server)

    def set_interval(self, new_interval):
        self.pick_interval = new_interval

    def set_group(self, new_group):
        self.group_pick = new_group

    def show_data(self):
        return json.dumps({"Interval": self.pick_interval, "Group to pick": self.group_pick}, indent=2)

    def get_fault(self, server):
        response = requests.get("{0}/fault".format(self.__db_host))
        filtered_fault_list = []
        # Check if request succeeded
        if "200" in str(response):
            all_faults = json.loads(response.content.decode("utf-8"))["result"]
            for fault in all_faults:
                for server_group in server["groups"]:
                    if fault["active"]:
                        if server_group in fault["targets"]:
                            filtered_fault_list.append(fault)
                            break

        return random.choice(filtered_fault_list)

    # This function gets a name of group of servers and query for the servers in the group and choose server that dose not
    # exists at the list
    def get_server(self, new_group = "all"):
        response = requests.get("{0}/server".format(self.__db_host))
        single_server = None
        # Check if request succeeded
        if "200" in str(response):
            server_list = json.loads(response.content.decode("utf-8"))["result"]
            # Check if the servers have to be filtered by group
            if self.group_pick != new_group:
                filter_groups = lambda server: server if new_group in server["groups"] else None
                filtered_server_list = list(map(filter_groups, server_list))
                server_list = list(filter(None, filtered_server_list))

            if len(server_list) != 0:
                single_server = random.choice(server_list)
                while single_server in self.servers_queue:
                    single_server = random.choice(server_list)

                self.add_server_to_queue(single_server)

        return single_server


















'''



class Picker:
    def __init__(self, db_host = "52.255.160.180"):
        self.pick_interval = 300
        self.group_pick = "all"
        self.__db_host = db_host

    def set_interval(self, new_interval):
        self.pick_interval = new_interval

    def set_group(self, new_group):
        self.group_pick = new_group

    def show_data(self):
        return json.dumps({"Interval": self.pick_interval, "Group to pick": self.group_pick}, indent=2)

    def get_fault(self, server):
        response = requests.get("{0}/fault".format(self.__db_host))
        filtered_fault_list = []
        # Check if request succeeded
        if "200" in str(response):
            all_faults = json.loads(response.content.decode("utf-8"))["result"]
            for fault in all_faults:
                for server_group in server["groups"]:
                    if fault["active"]:
                        if server_group in fault["targets"]:
                            filtered_fault_list.append(fault)
                            break

        return random.choice(filtered_fault_list)

    def get_server(self, new_group = "all"):
        response = requests.get("{0}/server".format(self.__db_host))
        single_server = None
        # Check if request succeeded
        if "200" in str(response):
            server_list = json.loads(response.content.decode("utf-8"))["result"]
            # Check if the servers have to be filtered by group
            if self.group_pick != new_group:
                filter_groups = lambda server: server if new_group in server["groups"] else None
                filtered_server_list = list(map(filter_groups, server_list))
                server_list = list(filter(None, filtered_server_list))

            if len(server_list) != 0:
                single_server = random.choice(server_list)

        return single_server


'''