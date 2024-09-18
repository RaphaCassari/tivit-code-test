from neo4j import GraphDatabase


class Neo4jService:
    def __init__(self, uri, user, password):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))

    def close(self):
        self.driver.close()

    def save_user_data(self, user_data):
        with self.driver.session() as session:
            session.run(
                """
                MERGE (u:User {name: $name, email: $email})
                WITH u
                UNWIND $purchases AS purchase
                MERGE (p:Purchase {id: purchase.id, item: purchase.item, price: purchase.price})
                MERGE (u)-[:PURCHASED]->(p)
                """,
                name=user_data["name"], email=user_data["email"], purchases=user_data["purchases"]
            )

    def save_admin_data(self, admin_data):
        with self.driver.session() as session:
            session.run(
                """
                MERGE (a:Admin {name: $name, email: $email})
                WITH a
                UNWIND $reports AS report
                MERGE (r:Report {id: report.id, title: report.title, status: report.status})
                MERGE (a)-[:GENERATED]->(r)
                """,
                name=admin_data["name"], email=admin_data["email"], reports=admin_data["reports"]
            )

    def get_recommendations(self, name):
        with self.driver.session() as session:
            result = session.run(
                """
                MATCH (u:User {name: $name})-[:PURCHASED]->(p:Purchase)
                RETURN p.item as recommended_item, p.price as price
                LIMIT 3
                """, name=name
            )
            return [{"item": record["recommended_item"], "price": record["price"]} for record in result]
