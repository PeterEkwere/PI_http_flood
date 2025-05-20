import json
import time
import logging
from stellar_sdk import Keypair, TransactionBuilder, Asset, Account, ClaimClaimableBalance
from node_project.key_derivation import get_private_key_from_passphrase
from bl_id import get_claimable_balances
import requests


class XDRGenerator:
    def __init__(self, base_passphrase, dest_address, withdrawal_amount, horizon_url="https://api.mainnet.minepi.com"):
        # Initialize base account
        base_keys = get_private_key_from_passphrase(base_passphrase)
        if not base_keys:
            raise ValueError("Invalid base passphrase")
        self.base_kp = Keypair.from_secret(base_keys['secret_key'])
        self.balance_id, self.locked_ammount  = get_claimable_balances(base_keys['public_key'])
        self.dest_address = dest_address
        self.withdrawal_amount = withdrawal_amount
        self.horizon_url = horizon_url
        self.session = requests.Session()
        print("balance id is ", self.balance_id)
        
        # Configure session for Pi Network
        self.session.headers.update({
            "X-Client-Name": "pi-network-client",
            "Accept": "application/json",
            "Content-Type": "application/x-www-form-urlencoded"
        })

    def generate_xdr_batch(self, channel_passphrases, unlock_time):
        """Generate fresh XDR batch with proper sequence numbers"""
        # Load and split accounts
        accounts = self._load_channels(channel_passphrases)
        split_idx = int(len(accounts) * 0.2)
        deposit_accounts = accounts[:split_idx]
        claim_accounts = accounts[split_idx:]

        xdrs = []
        
        # Generate deposit XDRs (20% of accounts)
        for _ in range(5):
            for acc, kp in deposit_accounts:
                # 5 transactions per deposit account
                xdrs.append(self._create_deposit_xdr(acc, kp, unlock_time))
        
        # Generate claim XDRs (80% of accounts)
        for _ in range(10000):
            for acc, kp in claim_accounts:
                xdrs.append(self._create_claim_xdr(acc, kp, unlock_time))
        
        self._save_xdrs(xdrs)
        return xdrs

    def _load_channels(self, passphrases):
        """Load accounts with automatic sequence refresh"""
        accounts = []
        for phrase in passphrases:
            keys = get_private_key_from_passphrase(phrase)
            if not keys:
                continue
            
            kp = Keypair.from_secret(keys['secret_key'])
            try:
                # Get fresh account data
                response = self.session.get(
                    f"{self.horizon_url}/accounts/{kp.public_key}",
                    timeout=10
                )
                account_data = response.json()
                accounts.append((
                    Account(
                        account_data['id'],
                        int(account_data['sequence'])
                    ),
                    kp
                ))
            except Exception as e:
                logging.error(f"Failed to load account {kp.public_key}: {str(e)}")
        return accounts

    def _create_deposit_xdr(self, account, kp, unlock_time):
        """Generate deposit transaction XDR"""
        tx = TransactionBuilder(
            source_account=account,
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
        """Generate claim transaction XDR"""
        tx = TransactionBuilder(
            source_account=account,
            network_passphrase="Pi Network",
            base_fee=100000
        ).add_time_bounds(
            min_time=0,
            max_time=int(unlock_time + 300)
        ).append_operation(
            ClaimClaimableBalance(
                balance_id=self.balance_id,
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

    def _save_xdrs(self, xdrs):
        """Save XDRs with metadata"""
        data = {
            "generated_at": int(time.time()),
            "base_account": self.base_kp.public_key,
            "xdrs": xdrs
        }
        with open("xdr_batch.json", "w") as f:
            json.dump(data, f)

# Usage
if __name__ == "__main__":
    # Configuration
    CHANNEL_PASSPHRASES = [
                    # Channel 0
                    "acid device pear alone monster depth slice october illness method pilot doctor suggest list drip ugly remind zone lemon dinner bubble sell timber buyer"

                    # Channel 1
                    "city display auto neutral one sense impose aerobic afraid document dice rocket six pioneer usage cheese one depth gesture bargain differ gold lady leisure",

                    # Channel 2
                    "pudding sudden expect upper rely annual stumble adapt settle capable ten ball surge donate position insane notable lounge bar tunnel main bar case size",

                    # Channel 3
                    "skull comfort divert drink athlete insect wedding detect romance shell ahead suffer proud toward foil bag winner stuff expire pipe wash disagree toy gorilla",

                    # Channel 4
                    "rural photo marriage regular demand coast park glue snake labor few exact burger hungry sorry observe enemy leopard sort script test forest prevent dash",

                    # Channel 5
                    "achieve space emotion lucky raw priority earth grocery ski speed require year guard utility muscle olive broom drip include fantasy dinner reduce syrup churn",

                    # Channel 6
                    "hobby pool cycle agree patrol entry zebra pelican charge jacket tube possible erosion trade found quiz vocal kitchen duck village short despair frost wink",

                    # Channel 7
                    "permit income wonder raise mesh boy ostrich rubber blouse trumpet spawn smart alcohol clip acquire tide end desk unlock apart venue royal now lake",

                    # Channel 8
                    "stumble entry south napkin fuel expect supply resemble scheme boat acoustic grace airport tower maid record sustain way grab lava dog fame liberty very"
    ]
    
    BASE_PASSPHRASE = "doctor result uncle jealous quick cactus inherit emerge shell galaxy venue city leave amazing grit true series filter poem find world stamp energy dirt" 
    DEST_ADDRESS = "MDFNWH6ZFJVHJDLBMNOUT35X4EEKQVJAO3ZDL4NL7VQJLC4PJOQFWAAAAAAKAWXUVERSM"
    
    # Initialize generator
    generator = XDRGenerator(
        base_passphrase=BASE_PASSPHRASE,
        dest_address=DEST_ADDRESS,
        withdrawal_amount="2000"
    )
    
    # Generate XDR batch with 1 hour validity
    generator.generate_xdr_batch(
        channel_passphrases=CHANNEL_PASSPHRASES,
        unlock_time=int(time.time()) + 600
    )
