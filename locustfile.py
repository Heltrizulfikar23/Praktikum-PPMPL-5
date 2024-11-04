from locust import HttpUser, TaskSet, task, between
import random
import json

# Data contoh untuk pengujian
test_data = {
    "name": "Test Item",
    "description": "This is a sample item for testing"
}

class APITaskSet(TaskSet):
    wait_time = between(1, 5)  # waktu tunggu antar tugas

    @task(1)
    def add_item(self):
        # POST request untuk menambahkan item baru
        response = self.client.post("/items", json=test_data)
        if response.status_code == 201:
            # Simpan ID item yang baru dibuat
            item_id = response.json().get("id")
            if item_id:
                self.item_id = item_id

    @task(2)
    def fetch_all_items(self):
        # GET request untuk mengambil semua item
        self.client.get("/items")

    @task(3)
    def fetch_item_by_id(self):
        # GET request untuk mengambil satu item berdasarkan ID
        if hasattr(self, 'item_id'):
            self.client.get(f"/items/{self.item_id}")

    @task(4)
    def modify_item(self):
        # PUT request untuk mengubah item
        if hasattr(self, 'item_id'):
            new_data = {
                "name": "Modified Test Item",
                "description": "This item has been modified for testing purposes"
            }
            self.client.put(f"/items/{self.item_id}", json=new_data)

    @task(5)
    def remove_item(self):
        # DELETE request untuk menghapus item
        if hasattr(self, 'item_id'):
            self.client.delete(f"/items/{self.item_id}")
            del self.item_id  # hapus ID untuk menghindari penghapusan berulang

# Kelas utama untuk user yang melakukan pengujian
class LoadTestUser(HttpUser):
    tasks = [APITaskSet]
    wait_time = between(1, 3)
