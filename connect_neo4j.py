
import os
from neo4j import GraphDatabase
from collections import Counter
import itertools


class Neo4jConnect:
    def __init__(self, uri, user, password):
        """
            uri: [neo4j, neo4j+s, bolt+s, bolt] neo4j does not support https
            user: username
            password: password
        """
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
            print("===========")
            self.driver.close()
            print("Connection closed")

    def __unpackResults__(self, items2unpack: list):
        """
            Helper fucntion:
                unpack a list of lists into list
        """
        return list(itertools.chain(*items2unpack))

    def __getCounter__(self, items2count: list):
        """
            Helper function:
                count unique items in a list and return a dictionary
        """
        return dict(Counter(items2count))

    def __getEntity__(self):
        """
            Returns a dictionary:
                key: database entity (node)
                value: number of occurence
        """
        query = "MATCH (n) RETURN labels(n)"
        if self.driver is not None:
            with self.driver.session() as session:
                result = session.run(query)
                node_results = [dict(ii)['labels(n)'][0] for ii in result]
        else:
            print("No connected to Neo4j")
        return self.__getCounter__(node_results)

    def __getRelations__(self):
        """
            return a dictionary:
                key: database relationship type
                value: number of occurence
        """
        query = "MATCH p=()-[r]-() RETURN TYPE(r)"
        if self.driver is not None:
            with self.driver.session() as session:
                result = session.run(query)
                relations = [dict(i)['TYPE(r)'] for i in result]
        else:
            pass
        return self.__getCounter__(relations)

    def __getProperties__(self):
        """
            return a dictionary:
                key: database properties key
                value: number of occurence
        """
        query = "MATCH (n) RETURN KEYS(n)"
        if self.driver is not None:
            with self.driver.session() as session:
                result = session.run(query)
                props_results = [dict(i)['KEYS(n)'] for i in result]
                props_keys = self.__unpackResults__(props_results)
        else:
            pass
        return self.__getCounter__(props_keys)

    def getArticleBody(self):
        """
            Returns a dictionary:
                key: author_name
                value: dictionary(datePublished: mainArticle)
        """
        if self.driver is not None:
            query = """
                    MATCH (n:Article)
                    RETURN n.articleBody,
                    n.articleId,n.datePublished
                    """
            with self.driver.session() as session:
                ent_props = session.run(query)
                ent_props = [dict(i) for i in ent_props]
                articles = {
                    f"{i['n.articleId']}":
                    {'date': i['n.datePublished'],
                     'mainArticle': i['n.articleBody']}
                    for i in ent_props}
        return articles
