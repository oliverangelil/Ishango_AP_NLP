from neo4j import GraphDatabase
from collections import Counter
import itertools


class Neo4jConnect:
    def __init__(self, uri, user, password):
        self.db_uri = uri
        self.db_user = user
        self.db_pass = password

        self.driver = None

        try:
            self.driver = GraphDatabase.driver(
                self.db_uri, auth=(self.db_user, self.db_pass))
        except Exception as err:
            print("Failed to connect to Database: ", err)

    def __closeConnection__(self):
        if self.driver is None:
            pass
        else:
            self.driver.close()

    def __getEntity__(self):
        query = "MATCH (n) RETURN labels(n)"
        if self.driver is not None:
            with self.driver.session() as session:
                result = session.run(query)
                node_results = [dict(ii)['labels(n)'][0] for ii in result]
                nodeLabels = Counter(node_results)
        else:
            print("No connected to Neo4j")
        return dict(nodeLabels)

    def __getRelations__(self):
        query = "MATCH p=()-[r]-() RETURN TYPE(r)"
        if self.driver is not None:
            with self.driver.session() as session:
                result = session.run(query)
                relations = Counter([dict(i)['TYPE(r)'] for i in result])
        else:
            pass
        return dict(relations)

    def __getProperties__(self):
        query = "MATCH (n) RETURN KEYS(n)"
        if self.driver is not None:
            with self.driver.session() as session:
                result = session.run(query)
                props_results = [dict(i)['KEYS(n)'] for i in result]
                props_keys = Counter(list(itertools.chain(*props_results)))
        else:
            pass
        return dict(props_keys)
