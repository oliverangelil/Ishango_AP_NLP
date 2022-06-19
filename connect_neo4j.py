from neo4j import GraphDatabase
import os

class Neo4jConnect:
    def __init__(self, uri, user, password):
        self.db_uri = uri
        self.db_user = user
        self.db_pass = password

        self.driver = None

        try:
            self.driver = GraphDatabase.driver(self.db_uri, auth=(self.db_user, self.db_pass))
        except Exception as err:
            print("Failed to connect to Database: ", err)
    
    def closeConnection(self):
        if self.driver is None: pass
        else: self.driver.close()        

