import duckdb
import pandas as pd
import os


def read_product_info(sql_query:str):
    '''This function reads the product information from the CSV file and executes the provided SQL query to retrieve the relevant information.'''
    path = os.path.join(os.path.dirname(__file__), 'product_info.csv')
    product_info = pd.read_csv(path)
    return duckdb.query(sql_query).fetchall()


if __name__ == "__main__":
    query = 'SELECT "Product Name" FROM product_info ORDER BY "Actual Price" DESC LIMIT 1;'
    results = read_product_info(query)
    print(results)
    
    


