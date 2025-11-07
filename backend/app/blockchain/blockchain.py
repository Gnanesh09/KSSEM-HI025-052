# app/blockchain/blockchain.py
"""
Python Blockchain Implementation for GreenChain
"""
import hashlib
import json
from datetime import datetime
from typing import List, Dict
import pickle
import os

class Block:
    """Single block in blockchain"""
    
    def __init__(self, index: int, transactions: List[Dict], 
                 previous_hash: str, timestamp: str = None):
        self.index = index
        self.timestamp = timestamp or datetime.now().isoformat()
        self.transactions = transactions
        self.previous_hash = previous_hash
        self.nonce = 0
        self.hash = self.calculate_hash()
    
    def calculate_hash(self) -> str:
        """Generate SHA-256 hash"""
        block_string = json.dumps({
            "index": self.index,
            "timestamp": self.timestamp,
            "transactions": self.transactions,
            "previous_hash": self.previous_hash,
            "nonce": self.nonce
        }, sort_keys=True)
        
        return hashlib.sha256(block_string.encode()).hexdigest()
    
    def mine_block(self, difficulty: int = 2):
        """Proof of Work"""
        target = "0" * difficulty
        
        while self.hash[:difficulty] != target:
            self.nonce += 1
            self.hash = self.calculate_hash()
        
        print(f"⛏️  Block #{self.index} mined: {self.hash[:16]}...")
    
    def to_dict(self) -> Dict:
        return {
            "index": self.index,
            "timestamp": self.timestamp,
            "transactions": self.transactions,
            "previous_hash": self.previous_hash,
            "hash": self.hash,
            "nonce": self.nonce
        }


class GreenChainBlockchain:
    """Main blockchain"""
    
    def __init__(self):
        self.chain: List[Block] = []
        self.pending_transactions: List[Dict] = []
        self.difficulty = 2
        
        # Load or create
        if not self.load_from_disk():
            self.create_genesis_block()
    
    def create_genesis_block(self):
        """First block"""
        genesis = Block(0, [{
            "type": "genesis",
            "message": "GreenChain Initialized",
            "timestamp": datetime.now().isoformat()
        }], "0" * 64)
        
        self.chain.append(genesis)
        print("🎉 Genesis block created")
    
    def get_latest_block(self) -> Block:
        return self.chain[-1]
    
    def add_transaction(self, transaction: Dict) -> str:
        """Add transaction to pending pool"""
        tx_id = hashlib.sha256(
            json.dumps(transaction, sort_keys=True).encode()
        ).hexdigest()
        
        transaction['tx_id'] = tx_id
        transaction['timestamp'] = datetime.now().isoformat()
        
        self.pending_transactions.append(transaction)
        return tx_id
    
    def mine_pending_transactions(self):
        """Create new block"""
        if not self.pending_transactions:
            return None
        
        new_block = Block(
            len(self.chain),
            self.pending_transactions.copy(),
            self.get_latest_block().hash
        )
        
        new_block.mine_block(self.difficulty)
        self.chain.append(new_block)
        
        self.pending_transactions = []
        self.save_to_disk()
        
        return new_block
    
    def is_chain_valid(self) -> tuple[bool, str]:
        """Verify blockchain integrity"""
        for i in range(1, len(self.chain)):
            current = self.chain[i]
            previous = self.chain[i - 1]
            
            if current.hash != current.calculate_hash():
                return False, f"Block #{i} tampered"
            
            if current.previous_hash != previous.hash:
                return False, f"Block #{i} chain broken"
        
        return True, "Blockchain valid ✓"
    
    def get_stats(self) -> Dict:
        """Blockchain statistics"""
        total_tx = sum(len(b.transactions) for b in self.chain)
        
        return {
            "total_blocks": len(self.chain),
            "total_transactions": total_tx,
            "latest_hash": self.get_latest_block().hash,
            "is_valid": self.is_chain_valid()[0],
            "pending": len(self.pending_transactions)
        }
    
    def save_to_disk(self, filename: str = "blockchain_data.pkl"):
        """Save blockchain"""
        with open(filename, 'wb') as f:
            pickle.dump(self.chain, f)
    
    def load_from_disk(self, filename: str = "blockchain_data.pkl") -> bool:
        """Load blockchain"""
        if os.path.exists(filename):
            with open(filename, 'rb') as f:
                self.chain = pickle.load(f)
            print(f"📂 Blockchain loaded ({len(self.chain)} blocks)")
            return True
        return False


# Global blockchain instance
blockchain = GreenChainBlockchain()


def record_insurance_claim(claim_data: Dict) -> str:
    """
    Record insurance claim on blockchain
    """
    transaction = {
        "type": "insurance_claim",
        "claim_id": claim_data['claim_id'],
        "field_id": claim_data['field_id'],
        "damage_type": claim_data['damage_type'],
        "pre_ndvi": claim_data['pre_ndvi'],
        "post_ndvi": claim_data['post_ndvi'],
        "damage_percent": claim_data['damage_percent'],
        "status": claim_data['status'],
        "payout": claim_data['payout']
    }
    
    tx_id = blockchain.add_transaction(transaction)
    block = blockchain.mine_pending_transactions()
    
    return tx_id, block.index if block else 0
