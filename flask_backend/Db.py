from pymongo import MongoClient, errors

def get_db():
    try:
        client = MongoClient('mongodb://localhost:27017/', serverSelectionTimeoutMS=5000)
        # Trigger a connection test
        client.server_info()
        db = client['CuisineConnect']  # Database name
        print("Connected to MongoDB successfully!")
        return db
    except errors.ServerSelectionTimeoutError as err:
        print("MongoDB connection error:", err)
        return None