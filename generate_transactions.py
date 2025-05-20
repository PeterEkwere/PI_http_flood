import json
import logging
from stellar_sdk import TransactionBuilder, Asset, Account, Keypair, ClaimClaimableBalance

class XDRGenerator:
    def __init__(self, horizon_url, base_kp, dest_address, withdrawal_amount):
        self.horizon_url = horizon_url
        self.base_kp = base_kp
        self.dest_address = dest_address
        self.withdrawal_amount = withdrawal_amount
        self.session = requests.Session()
        self.channel_accounts = []
        self.xdr_cache = []

    def generate_xdr_batch(self, passphrases, unlock_time):
        """Generate and cache fresh XDRs with proper sequence numbers"""
        self._load_channels(passphrases)
        self._generate_xdrs(unlock_time)
        self._save_to_json()
        return self.xdr_cache

    def _load_channels(self, passphrases):
        """Load accounts with automatic 80/20 split"""
        # Load all accounts
        loaded = [self._load_account(p) for p in passphrases]
        self.channel_accounts = [acc for acc in loaded if acc]
        
        # Split accounts: 20% deposit, 80% claim
        split_idx = int(len(self.channel_accounts) * 0.2)
        self.deposit_accounts = self.channel_accounts[:split_idx]
        self.claim_accounts = self.channel_accounts[split_idx:]

    def _generate_xdrs(self, unlock_time):
        """Generate transactions with current sequence numbers"""
        self.xdr_cache = []
        
        # Generate deposit XDRs (20%)
        for account, kp in self.deposit_accounts:
            for _ in range(5):  # 5 transactions per deposit account
                self.xdr_cache.append(
                    self._create_deposit_xdr(account, kp, unlock_time)
        
        # Generate claim XDRs (80%)
        for account, kp in self.claim_accounts:
            for _ in range(4):  # 4 transactions per claim account
                self.xdr_cache.append(
                    self._create_claim_xdr(account, kp, unlock_time))

    def _create_deposit_xdr(self, account, kp, unlock_time):
        fresh_account = self._refresh_account(account.account.account_id)
        tx = TransactionBuilder(
            source_account=fresh_account,
            network_passphrase="Pi Network",
            base_fee=100000
        ).add_time_bounds(
            min_time=0,
            max_time=int(unlock_time + 3600)
        ).append_payment_op(
            destination=self.base_kp.public_key,
            asset=Asset.native(),
            amount="0.001"
        ).build()
        tx.sign(kp)
        return tx.to_xdr()

    def _create_claim_xdr(self, account, kp, unlock_time):
        fresh_account = self._refresh_account(account.account.account_id)
        tx = TransactionBuilder(
            source_account=fresh_account,
            network_passphrase="Pi Network",
            base_fee=100000
        ).add_time_bounds(
            min_time=0,
            max_time=int(unlock_time + 300)
        ).append_operation(
            ClaimClaimableBalance(
                balance_id=self.claimable_balance_id,
                source=self.base_kp.public_key
            )
        ).append_payment_op(
            source=self.base_kp.public_key,
            destination=self.dest_address,
            asset=Asset.native(),
            amount=self.withdrawal_amount
        ).build()
        tx.sign(self.base_kp)
        tx.sign(kp)
        return tx.to_xdr()

    def _save_to_json(self):
        """Save XDRs with metadata"""
        data = {
            "generated_at": int(time.time()),
            "deposit_xdrs": self.xdr_cache[:len(self.deposit_accounts)*5],
            "claim_xdrs": self.xdr_cache[len(self.deposit_accounts)*5:]
        }
        with open("xdr_cache.json", "w") as f:
            json.dump(data, f)




gen = XDRGenerator(
    horizon_url="https://api.mainnet.minepi.com",
    base_kp=Keypair.from_secret("BASE_ACCOUNT_SECRET"),
    dest_address="DESTINATION_ADDRESS",
    withdrawal_amount="XX.XX"
)
gen.generate_xdr_batch(passphrases, int(time.time()))
