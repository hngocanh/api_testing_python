from api.base_client import BaseClient

class PublicObjectAPI(BaseClient):
    ENDPOINT = "/objects"

    def get_all(self, ids=None):
        # If ids is provided, create a list of tuples for query parameters
        # Example: ids=[1, 2, 3] becomes [("id", 1), ("id", 2), ("id", 3)]
        if ids:
            params = []
            for i in ids:
                params.append(("id", i))
        else:
            params = None
        
        return self.get(self.ENDPOINT, params=params)
    
    def get_by_id(self, object_id):
        return self.get(f"{self.ENDPOINT}/{object_id}")
    
    def create(self, payload):
        return self.post(self.ENDPOINT, json=payload)
    
    def update(self, object_id, payload):
        return self.put(f"{self.ENDPOINT}/{object_id}", json=payload)
    
    def delete_object(self, object_id):
        return self.delete(f"{self.ENDPOINT}/{object_id}")
    
    def partial_update(self, object_id, payload):
        return self.patch(f"{self.ENDPOINT}/{object_id}", json=payload)