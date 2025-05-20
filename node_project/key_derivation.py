import json
import subprocess
import os
from nodejs import node

def get_private_key_from_passphrase(passphrase):
    """
    Generate Stellar keypair from a mnemonic passphrase using Node.js
    
    Args:
        passphrase (str): BIP39 mnemonic passphrase
        
    Returns:
        dict: Dictionary containing public_key and secret_key, or None if error
    """
    try:
        # Get the path to the JS script (in the same directory as this file)
        script_dir = os.path.dirname(os.path.abspath(__file__))
        js_script = os.path.join(script_dir, 'derive-keys.cjs')
        
        # Run the Node.js script with the passphrase as an argument
        result = node.run([js_script, passphrase], 
                          capture_output=True, 
                          text=True,
                          check=True)
        
        # Parse JSON output from the Node.js script
        keys = json.loads(result.stdout)
        
        # Return the keys in the expected format
        return {
            "public_key": keys["publicKey"],
            "secret_key": keys["secretKey"]
        }
    except subprocess.CalledProcessError as e:
        print(f"Node.js script error: {e.stderr}")
        return None
    except json.JSONDecodeError:
        print(f"Failed to parse JSON output: {result.stdout}")
        return None
    except Exception as e:
        print(f"Error: {str(e)}")
        return None

# Example usage
if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1:
        passphrase = sys.argv[1]
    else:
        # Default test passphrase
        passphrase = "type Outside kangaroo street spoil web lonely balcony dial reopen file lava phrase display law debate panel half hungry stock abuse panic public select"
        passphrase2 = "rough across coconut love abandon people uniform zoo symptom sand daring where pistol supreme donate state already frozen find coil garage canoe wedding know"
        passphrase3 = "head always wreck drum half liquid large dilemma supply fiscal debate open mass donate robot cause sort coast aim cluster episode saddle room prepare"
        passphrase4 = "chapter ready essay couple thunder boss castle refuse bicycle left all crisp satisfy level grab mom onion practice blush inhale evil torch glimpse draft"
        passphrase5 = "allow sample hand unusual glass boil coast arm crater arrest grain door cactus vital law upon ignore devote great rifle jazz tackle language wagon"
        passphrase6 = "yellow glide huge tomato purity marble mean prison rule valve smile fault empower suggest theme chef tired burden toddler regular bachelor vocal pottery mixture"
        passphrase7 = "follow impose off ceiling ticket oyster organ gauge ready clog planet lion same protect address miss blush tomorrow auto salmon improve school essence gallery"
    keys = get_private_key_from_passphrase(passphrase6)
    if keys:
        print(f"Public Key: {keys['public_key']}")
        print(f"Secret Key: {keys['secret_key']}")
    else:
        print("Failed to generate keys")
