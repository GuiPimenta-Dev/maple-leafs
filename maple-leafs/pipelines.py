import mysql.connector

# useful for handling different item types with a single interface
from itemadapter import ItemAdapter


class MyKeywordPipeline:
    def process_item(self, item, spider):
        connection = mysql.connector.connect(
            host="localhost",
            port="3306",
            database="zevvybryqx",
            user="zevvybryqx",
            password="5sh333AMyP",
        )
        cursor = connection.cursor()
        query = "SELECT url FROM articles WHERE url = %s"
        cursor.execute(query, (item["url"],))
        row = cursor.fetchone()
        if row is None and (
            item["author"] is not None
            and item["date"] is not None
            and item["title"] is not None
            and item["url"] is not None
        ):
            query = "INSERT INTO articles (site,title, author, url, date, scraped_at) VALUES (%s, %s, %s, %s, %s, NOW())"
            cursor.execute(
                query,
                (
                    spider.name.replace("-", " ").title(),
                    item["title"],
                    item["author"],
                    item["url"],
                    item["date"],
                ),
            )
            connection.commit()
        cursor.close()
        connection.close()
        return item
