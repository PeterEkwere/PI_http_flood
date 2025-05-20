// Save this as derive_keys.js
const StellarSdk = require('@stellar/stellar-sdk');
const bip39 = require('bip39');
const { derivePath } = require('@hawkingnetwork/ed25519-hd-key-rn');

async function getPrivateKeyFromPassphrase(passphrase) {
  const seed = await bip39.mnemonicToSeed(passphrase);
  const derivedSeed = derivePath("m/44'/314159'/0'", seed);
  const keypair = StellarSdk.Keypair.fromRawEd25519Seed(derivedSeed.key);
  
  return {
    publicKey: keypair.publicKey(),
    secretKey: keypair.secret()
  };
}

// Take passphrase from command line arguments
async function main() {
  // Check if passphrase is provided
  if (process.argv.length < 3) {
    console.error("Please provide a passphrase as an argument");
    process.exit(1);
  }

  const passphrase = process.argv[2];

  try {
    const keys = await getPrivateKeyFromPassphrase(passphrase);
    // Output as JSON for easy parsing in Python
    console.log(JSON.stringify(keys));
  } catch (error) {
    console.error("Error:", error.message);
    process.exit(1);
  }
}

main();
