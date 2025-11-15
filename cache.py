import os
from google.cloud import firestore
from datetime import datetime
from typing import List, Dict, Optional

# The `project` parameter is optional and represents which project the client
# will act on behalf of. If not supplied, the client falls back to the default
# project inferred from the environment.

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "massive-boulder-478310-q0-ceb05684a511.json"
collection_name="result-cache"
document="4q4FdTUqbCtOlP7R9HNx"
database_name="sisu-store"
db = firestore.Client(project="massive-boulder-478310-q0", database=database_name)


def add_data(product, vendor, url, summary, trustability, graph, expiry):
    """
    Add new record to cache
    """
    doc_ref = db.collection(collection_name).document(document)
    doc_ref.set({"Product": product, "Company": vendor, "URL": url, "Summary": summary,
                 "trustability": trustability, "Graph": graph, "Expiry": expiry})

def read_data():
    users_ref = db.collection(collection_name)
    docs = users_ref.stream()
    print("Hi")
    for doc in docs:
        print(f"{doc.id} => {doc.to_dict()}")


class ProductManager:
    
    def __init__(self, collection_name: str = "products"):
        """
        Initialize ProductManager with Firestore client
        
        Args:
            collection_name: Name of the Firestore collection
        """
        database_name="sisu-store"
        collection_name="result-cache"
        self.db = firestore.Client(project="massive-boulder-478310-q0", database=database_name)
        self.collection = self.db.collection(collection_name)
    
    def create_product(self, product: str, vendor: str, url: str, summary: str, 
                      trustability: float, graph: str, expiry: str) -> str:
        
        """
        Create a new product document
        
        Args:
            product: Product name
            vendor: Company/vendor name
            url: Product URL
            summary: Product summary
            trustability: Trustability score (float)
            graph: Graph data/information
            expiry: Expiry date/information
            
        Returns:
            Document ID of the created product
        """
        try:
            product_data = {
                "Product": product,
                "Company": vendor,
                "URL": url,
                "Summary": summary,
                "trustability": trustability,
                "Graph": graph,
                "Expiry": expiry,
                "created_at": firestore.SERVER_TIMESTAMP,
                "updated_at": firestore.SERVER_TIMESTAMP
            }
            
            doc_ref = self.collection.document()
            doc_ref.set(product_data)
            
            print(f"✅ Product created successfully with ID: {doc_ref.id}")
            return doc_ref.id
            
        except Exception as e:
            print(f"❌ Error creating product: {e}")
            raise
    
    def get_product(self, product_id: str) -> Optional[Dict]:
        """
        Get a product by its document ID
        
        Args:
            product_id: Firestore document ID
            
        Returns:
            Product data as dictionary or None if not found
        """
        try:
            doc_ref = self.collection.document(product_id)
            doc = doc_ref.get()
            
            if doc.exists:
                data = doc.to_dict()
                data['id'] = doc.id  # Include document ID in returned data
                return data
            else:
                print(f"❌ Product with ID {product_id} not found")
                return None
                
        except Exception as e:
            print(f"❌ Error getting product: {e}")
            return None
    
    def get_product_by_name(self, product_name: str) -> Optional[Dict]:
        """
        Get a product by its name
        
        Args:
            product_name: Exact product name to search for
            
        Returns:
            Product data or None if not found
        """
        try:
            query = self.collection.where("Product", "==", product_name).limit(1)
            docs = query.stream()
            
            for doc in docs:
                data = doc.to_dict()
                data['id'] = doc.id
                return data
            
            print(f"❌ Product '{product_name}' not found")
            return None
            
        except Exception as e:
            print(f"❌ Error getting product by name: {e}")
            return None
    
    def get_all_products(self) -> List[Dict]:
        """
        Get all products in the collection
        
        Returns:
            List of all products with their IDs
        """
        try:
            docs = self.collection.stream()
            products = []
            
            for doc in docs:
                data = doc.to_dict()
                data['id'] = doc.id
                products.append(data)
            
            print(f"✅ Retrieved {len(products)} products")
            return products
            
        except Exception as e:
            print(f"❌ Error getting all products: {e}")
            return []
    
    def update_product(self, product_id: str, **kwargs) -> bool:
        """
        Update specific fields of a product
        
        Args:
            product_id: Document ID of the product to update
            **kwargs: Fields to update (e.g., Product="New Name", trustability=0.8)
            
        Returns:
            True if successful, False otherwise
        """
        try:
            if not kwargs:
                print("❌ No fields provided for update")
                return False
            
            # Add updated timestamp
            update_data = {**kwargs, "updated_at": firestore.SERVER_TIMESTAMP}
            
            doc_ref = self.collection.document(product_id)
            doc_ref.update(update_data)
            
            print(f"✅ Product {product_id} updated successfully")
            return True
            
        except Exception as e:
            print(f"❌ Error updating product: {e}")
            return False
    
    def update_full_product(self, product_id: str, product: str, vendor: str, 
                           url: str, summary: str, trustability: float, 
                           graph: str, expiry: str) -> bool:
        """
        Update all fields of a product
        
        Args:
            product_id: Document ID to update
            All other parameters: Same as create_product
            
        Returns:
            True if successful, False otherwise
        """
        try:
            product_data = {
                "Product": product,
                "Company": vendor,
                "URL": url,
                "Summary": summary,
                "trustability": trustability,
                "Graph": graph,
                "Expiry": expiry,
                "updated_at": firestore.SERVER_TIMESTAMP
            }
            
            doc_ref = self.collection.document(product_id)
            doc_ref.set(product_data, merge=False)  # Replace entire document
            
            print(f"✅ Product {product_id} fully updated")
            return True
            
        except Exception as e:
            print(f"❌ Error updating full product: {e}")
            return False
    
    def delete_product(self, product_id: str) -> bool:
        """
        Delete a product by its document ID
        
        Args:
            product_id: Document ID to delete
            
        Returns:
            True if successful, False otherwise
        """
        try:
            doc_ref = self.collection.document(product_id)
            doc = doc_ref.get()
            
            if not doc.exists:
                print(f"❌ Product with ID {product_id} not found")
                return False
            
            doc_ref.delete()
            print(f"✅ Product {product_id} deleted successfully")
            return True
            
        except Exception as e:
            print(f"❌ Error deleting product: {e}")
            return False
    
    def search_products(self, field: str, value: str) -> List[Dict]:
        """
        Search products by field value
        
        Args:
            field: Field name to search (Product, Company, etc.)
            value: Value to search for
            
        Returns:
            List of matching products
        """
        try:
            query = self.collection.where(field, "==", value)
            docs = query.stream()
            
            products = []
            for doc in docs:
                data = doc.to_dict()
                data['id'] = doc.id
                products.append(data)
            
            print(f"✅ Found {len(products)} products matching {field}='{value}'")
            return products
            
        except Exception as e:
            print(f"❌ Error searching products: {e}")
            return []
    
    def get_products_by_trustability(self, min_trust: float = 0.0, 
                                   max_trust: float = 1.0) -> List[Dict]:
        """
        Get products filtered by trustability score range
        
        Args:
            min_trust: Minimum trustability score
            max_trust: Maximum trustability score
            
        Returns:
            List of products in the trustability range
        """
        try:
            query = self.collection.where("trustability", ">=", min_trust)\
                                  .where("trustability", "<=", max_trust)\
                                  .order_by("trustability", direction=firestore.Query.DESCENDING)
            
            docs = query.stream()
            products = []
            
            for doc in docs:
                data = doc.to_dict()
                data['id'] = doc.id
                products.append(data)
            
            print(f"✅ Found {len(products)} products with trustability between {min_trust} and {max_trust}")
            return products
            
        except Exception as e:
            print(f"❌ Error filtering by trustability: {e}")
            return []
    
    def get_products_by_company(self, company: str) -> List[Dict]:
        """
        Get all products from a specific company
        
        Args:
            company: Company name to filter by
            
        Returns:
            List of products from the specified company
        """
        return self.search_products("Company", company)
    
    def batch_create_products(self, products_list: List[Dict]) -> List[str]:
        """
        Create multiple products in a batch
        
        Args:
            products_list: List of product dictionaries with required fields
            
        Returns:
            List of created document IDs
        """
        try:
            batch = self.db.batch()
            doc_ids = []
            
            for product_data in products_list:
                doc_ref = self.collection.document()
                # Add timestamps
                full_data = {
                    **product_data,
                    "created_at": firestore.SERVER_TIMESTAMP,
                    "updated_at": firestore.SERVER_TIMESTAMP
                }
                batch.set(doc_ref, full_data)
                doc_ids.append(doc_ref.id)
            
            batch.commit()
            print(f"✅ Successfully created {len(doc_ids)} products in batch")
            return doc_ids
            
        except Exception as e:
            print(f"❌ Error in batch creation: {e}")
            return []


def main():
    product_manager = ProductManager()
    all_products = product_manager.get_all_products()
    for product in all_products:
        print(f"📦 {product['Product']} by {product['Company']} "
              f"(Trust: {product['Trustability']})")

if __name__ == "__main__":
    main()
