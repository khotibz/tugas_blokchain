import hashlib
import json
import time


class Block:

  def __init__(self, index, data, previous_hash):
    self.index = index
    self.timestamp = time.time()
    self.data = data
    self.previous_hash = previous_hash
    self.hash = self.calculate_hash()

  def calculate_hash(self):
    payload = {
        "index": self.index,
        "timestamp": self.timestamp,
        "data": self.data,
        "previous_hash": self.previous_hash,
    }
    raw = json.dumps(payload, sort_keys=True).encode()
    return hashlib.sha256(raw).hexdigest()


class Blockchain:

  def __init__(self):
    self.chain = [self.create_genesis_block()]

  def create_genesis_block(self):
    # TODO: buat genesis block
    return Block(0, "Genesis Block - Transaksi Pertama", "0")

  def latest_block(self):
    return self.chain[-1]

  def add_block(self, data):
    # TODO: buat block baru dengan previous_hash dari latest block
    prev_block = self.latest_block()
    new_block = Block(prev_block.index + 1, data, prev_block.hash)
    self.chain.append(new_block)

  def is_valid(self):
    # TODO: cek hash block dan previous_hash link untuk seluruh chain
    for i in range(1, len(self.chain)):
      current_block = self.chain[i]
      previous_block = self.chain[i - 1]

      # 1. Validasi apakah hash blok saat ini valid (sesuai dengan isinya)
      if current_block.hash != current_block.calculate_hash():
        return False

      # 2. Validasi apakah previous_hash cocok dengan hash blok sebelumnya
      if current_block.previous_hash != previous_block.hash:
        return False

    # Validasi genesis block
    if (
        len(self.chain) > 0
        and self.chain[0].hash != self.chain[0].calculate_hash()
    ):
      return False

    return True


# ==========================================
# SKENARIO PENGUJIAN WAJIB
# ==========================================
if __name__ == "__main__":
  print("--- INISIALISASI BLOCKCHAIN ---")
  my_blockchain = Blockchain()

  # Skenario 1: Chain baru hanya memiliki genesis block
  print(
      f"\nSkenario 1 - Chain baru hanya memiliki genesis block: Valid ="
      f" {my_blockchain.is_valid()}"
  )

  # Skenario 2: Tambah minimal 3 block dengan transaksi berbeda
  print("\nSkenario 2 - Menambahkan 3 blok transaksi baru...")
  my_blockchain.add_block({"sender": "Ahmad", "receiver": "Budi", "amount": 50})
  my_blockchain.add_block({"sender": "Budi", "receiver": "Cika", "amount": 20})
  my_blockchain.add_block({"sender": "Cika", "receiver": "Doni", "amount": 100})
  print(f"Status Chain setelah penambahan 3 blok: Valid = {my_blockchain.is_valid()}")

  # Skenario 5: Cetak index, hash, dan previous_hash setiap block
  print("\nSkenario 5 - Rincian Keterkaitan Blok dalam Chain:")
  for block in my_blockchain.chain:
    print(f"Index        : {block.index}")
    print(f"Data         : {block.data}")
    print(f"Previous Hash: {block.previous_hash}")
    print(f"Hash         : {block.hash}")
    print("-" * 50)

  # Skenario 3: Ubah data pada block tengah tanpa menghitung ulang chain (Tampering Data)
  print(
      "\nSkenario 3 - Mengubah data pada blok tengah (Blok index 1) secara"
      " ilegal..."
  )
  my_blockchain.chain[1].data = {
      "sender": "Ahmad",
      "receiver": "Hacker",
      "amount": 9999,
  }
  print(
      "Status Chain setelah Data Tampering (tanpa re-calculate): Valid ="
      f" {my_blockchain.is_valid()}"
  )

  # Skenario 4: Ubah previous_hash pada block (Tampering Link)
  print(
      "\nSkenario 4 - Mengembalikan data blok 1, lalu merusak previous_hash"
      " pada blok 2..."
  )
  # Reset data blok 1
  my_blockchain.chain[1].data = {
      "sender": "Ahmad",
      "receiver": "Budi",
      "amount": 50,
  }
  # Rusak previous_hash di blok 2
  my_blockchain.chain[2].previous_hash = "fake_previous_hash_string"
  print(
      "Status Chain setelah Previous Hash Tampering: Valid ="
      f" {my_blockchain.is_valid()}"
  )