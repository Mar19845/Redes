import getpass
from networkx.algorithms.shortest_paths.generic import shortest_path
import yaml
import networkx as nx
import asyncio
import logging
from datetime import datetime
import slixmpp
import networkx as nx
import random
import sys



if sys.platform == 'win32' and sys.version_info >= (3, 8):
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())


class Client(slixmpp.ClientXMPP):
    def __init__(self, jid, password, algorithm, nodo, nodes, users, graph):
        super().__init__(jid, password)
        self.received = set()
        self.initialize(jid, password, algorithm, nodo, nodes, users, graph)
        
        self.schedule(name="echo", callback=self.echo, seconds=10, repeat=True)
        self.schedule(name="update", callback=self.update_graph, seconds=10, repeat=True)
        
        
        
        self.connected_event = asyncio.Event()
        self.presences_received = asyncio.Event()

        self.add_event_handler('session_start', self.start)
        self.add_event_handler('message', self.recived_message)
        
        
        self.register_plugin('xep_0030') # Service Discovery
        self.register_plugin('xep_0045') # Multi-User Chat
        self.register_plugin('xep_0199') # Ping
        
    async def start(self, event):
        self.send_presence() 
        await self.get_roster()
        self.connected_event.set() 
         
    def initialize(self, jid, password, algoritmo, nodo, nodes, users, graph):
        self.algoritmo = algoritmo
        self.users = users
        self.graph = graph
        self.nodo = nodo
        self.nodes = nodes
        self.jid = jid
        self.password = password
    
    async def recived_message(self, msg):
        if msg['type'] in ('normal', 'chat'):
            await self.send_msg(msg['body'])
            
    def echo(self):
        for i in self.nodes:
            msg = "echo-" + str(self.jid) + "-" + str(self.users[i]) + "--"+ str(datetime.timestamp(datetime.now())) +"-" + str(i) + "-"
            self.send_message(mto=self.users[i],mbody=msg,mtype='chat')
    def update_graph(self):
        if self.algoritmo == '2':
            for i in self.nodes:
                self.graph.nodes[i]["neighbors"] = self.graph.neighbors(i)
            
            #update graph
            neigh = nx.graph.get_node_attributes(self.graph,'neighbors')

        elif self.algoritmo == '3':
            # Updating states table
            for x in self.graph.nodes().data():
                if x[0] in self.nodes:
                    dataneighbors= x
            for x in self.graph.edges.data('weight'):
                if x[1] in self.nodes and x[0]==self.nodo:
                    dataedges = x
            StrNodes = str(dataneighbors) + "|" + str(dataedges)
            for i in self.nodes:
                update_msg = "2-" + str(self.jid) + "-" + str(self.users[i]) + "-" + str(self.graph.number_of_nodes()) + "--" + str(self.nodo) + "-" + StrNodes
                self.send_message(mto=self.users[i],mbody=update_msg,mtype='chat')
    
    
    
    #part of the logic            
    async def send_msg(self, msg):
        message = msg.split('-')
        
        if message[0] == 'msg':
            pass
        elif message[0] == 'echo':
            # get the distance between nodes
            if message[6] == '':
                now = datetime.now()
                timestamp = datetime.timestamp(now)
                msg = msg + str(timestamp)
                self.send_message(mto=message[1],mbody=msg,mtype='chat')
            else:
                difference = float(message[6]) - float(message[4])
                self.graph.nodes[message[5]]['weight'] = difference