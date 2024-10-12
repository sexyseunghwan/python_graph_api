""" 
Author      : Seunghwan Shin 
Create date : 2024-07-12 
Description : Code that can perform various functions through Telegram
    
History     : 2024-07-12 Seunghwan Shin       # first creat
              2024-08-27 Seunghwan Shin       # Modified so that only integers can be represented on the x-axis of the graph.
              2024-00-00 Seunghwan Shin       # 
"""
from controller import *

if __name__ == "__main__":
    
    environment = os.getenv('ENV', 'dev')
    dotenv_file = f".env.{environment}"
    load_dotenv(dotenv_file)
    
    app.run(debug=True, port=5800)