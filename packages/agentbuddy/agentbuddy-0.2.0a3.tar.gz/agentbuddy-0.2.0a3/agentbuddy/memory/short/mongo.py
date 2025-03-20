class ShortMongo(ShortMemory):
    MONGO_URI = "mongodb://localhost:27017"
    MONGO_DB = "agent_db"
    MONGO_COLLECTION = "sessions"

    mongo_client = pymongo.MongoClient(MONGO_URI)
    mongo_db = mongo_client[MONGO_DB]
    mongo_collection = mongo_db[MONGO_COLLECTION]

    def load_messages(self) -> List[str]:
        session = ShortMongo.mongo_collection.find_one({"session_id": self.session_id})
        return session["messages"] if session else []

    def save_messages(self, messages: List[str]):
        ShortMongo.mongo_collection.update_one(
            {"session_id": self.session_id},
            {"$set": {"messages": messages}},
            upsert=True
        )