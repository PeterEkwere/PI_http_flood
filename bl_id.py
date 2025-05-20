from stellar_sdk import Server, exceptions

def get_claimable_balances(public_key, horizon_url="https://api.mainnet.minepi.com"):
    """Fetch claimable balances for a given public key"""
    server = Server(horizon_url)
    try:
        balances = (
            server.claimable_balances()
            .for_claimant(public_key)
            .limit(1)
            .order(desc=True)
            .call()
        )
        if balances['_embedded']['records']:
            balance = balances['_embedded']['records'][0]
            return balance['id'], balance['amount']
        return None, None
    except exceptions.BadRequestError as e:
        print(f"Error fetching balances: {e}")
        return None, None

# Usage example:
if __name__ == "__main__":
    balance_id, amount = get_claimable_balances("GAKO7CYILCVH4JA3MMU3LVIJVYGEJSNIIDOMTQKTXJ45STYMAXR4HI4T")
    print(f"balance id is {balance_id}, amount is  {amount}")
