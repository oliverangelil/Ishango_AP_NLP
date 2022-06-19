from neo4j import GraphDatabase
from collections import Counter
import itertools
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

    def getEntity(self):
        query = "MATCH (n) RETURN labels(n)"
        if self.driver is not None:
            with self.driver.session() as session:
                result = session.run(query)
                nodeLabels = Counter([dict(ii)['labels(n)'][0] for ii in result])
        else: print("No connected to Neo4j")
        return dict(nodeLabels)
    
    def getRelations(self):
        query = "MATCH p=()-[r]-() RETURN TYPE(r)"
        if self.driver is not None:
            with self.driver.session() as session:
                result = session.run(query)
                relations = Counter([dict(i)['TYPE(r)'] for i in result])
        else: pass
        return dict(relations)
    
    def getProperties(self):
        query = "MATCH (n) RETURN KEYS(n)"
        if self.driver is not None:
            with self.driver.session() as session:
                result = session.run(query)
                props_keys = Counter(list(itertools.chain(*[dict(i)['KEYS(n)'] for i in result])))
        else: pass
        return dict(props_keys)


# flatten_list = list(itertools.chain(*original_list))


uri = os.environ.get('DB_URI')
user = os.environ.get('DB_USER')
password = os.environ.get('DB_PASS')

neoConn = Neo4jConnect(uri, user, password)

r = neoConn.getProperties()

print(r)


neoConn.closeConnection()