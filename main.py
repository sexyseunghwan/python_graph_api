""" 
Author      : Seunghwan Shin 
Create date : 2024-07-12 
Description : Code that can perform various functions through Telegram
    
History     : 2024-07-12 Seunghwan Shin       # first creat
              2024-08-27 Seunghwan Shin       # Modified so that only integers can be represented on the x-axis of the graph.
              2024-11-05 Seunghwan Shin       # Create Test api
"""
from controller import *

if __name__ == "__main__":
    
    """
    Code to load ".env" file.
    """
    environment = os.getenv('ENV', 'dev')
    dotenv_file = f".env.{environment}"
    load_dotenv(dotenv_file)
    

    """
    Function to start the "Flask" server
    Route functions exist below "controller.py"
    """ 
    app.run(debug=True, port=5800)