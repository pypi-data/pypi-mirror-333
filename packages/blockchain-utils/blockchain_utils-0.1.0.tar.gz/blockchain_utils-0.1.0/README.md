### Usage (cryptoaddress related stuff)
The library supports blockchains: BTC, ETH

At the moment there is the following logic:
1. [addresses.py](crypto_utils/addresses.py)
   1. Validate and normalize Ethereum addresses
   ```python
   from crypto_utils.addresses import is_eth_address, normalize_eth_address
   
   assert is_eth_address('0xdefff89752bc4ae304e5c3aa71e917ae638e47c4') # True
   assert is_eth_address('0XDEFFF89752BC4AE304E5C3AA71E917AE638E47C4') # True
   assert is_eth_address('0xDeFFf89752BC4aE304E5c3Aa71E917ae638e47C4') # True
   assert not is_eth_address('not-eth-address') # True
   
   expected = '0xDeFFf89752BC4aE304E5c3Aa71E917ae638e47C4'
   assert normalize_eth_address('0xdefff89752bc4ae304e5c3aa71e917ae638e47c4') == expected # True
   assert normalize_eth_address('0XDEFFF89752BC4AE304E5C3AA71E917AE638E47C4') == expected # True
   ```
   2. Validate bitcoin addresses
   ```python
   from crypto_utils.addresses import is_btc_address
   
   assert is_btc_address('1A1zP1eP5QGefi2DMPTfTL5SLmv7DivfNa') # True
   assert is_btc_address('3GRdnTq18LyNveWa1gQJcgp8qEnzijv5vR') # True
   assert is_btc_address('bc1qnkyhslv83yyp0q0suxw0uj3lg9drgqq9c0auzc') # True

   assert not is_btc_address('non-btc-address') # True
   assert not is_btc_address('111') # True
   assert not is_btc_address('333') # True
   assert not is_btc_address('bc1') # True
   ```
   3. Detect blockchain for the given address:
   ```python
   from crypto_utils.addresses import detect_blockchain, BTC, ETH
   
   assert detect_blockchain('1A1zP1eP5QGefi2DMPTfTL5SLmv7DivfNa') == BTC
   assert detect_blockchain('3GRdnTq18LyNveWa1gQJcgp8qEnzijv5vR') == BTC
   assert detect_blockchain('bc1qnkyhslv83yyp0q0suxw0uj3lg9drgqq9c0auzc') == BTC

   assert detect_blockchain('0xdefff89752bc4ae304e5c3aa71e917ae638e47c4') == ETH
   assert detect_blockchain('0XDEFFF89752BC4AE304E5C3AA71E917AE638E47C4') == ETH
   assert detect_blockchain('0xDeFFf89752BC4aE304E5c3Aa71E917ae638e47C4') == ETH
   
   detect_blockchain('not-blockchain-address') # UnknownBlockchain exception raised
   ```
   4. Also, there is a shortcut that combines the previous points. Function `normalize_address` accepts `address` and performs the following logic:
      1. If the address is Ethereum address, then normalize it and return it
      2. If the address is Bitcoin address, then just return it 
      3. If the address is neither Ethereum nor Bitcoin, then raise exception UnknownBlockchain
   ```python
   from crypto_utils.addresses import normalize_address
   
   expected = '0xDeFFf89752BC4aE304E5c3Aa71E917ae638e47C4'
   assert normalize_address('0xdefff89752bc4ae304e5c3aa71e917ae638e47c4') == expected
   
   expected = '1A1zP1eP5QGefi2DMPTfTL5SLmv7DivfNa'
   assert normalize_address('1A1zP1eP5QGefi2DMPTfTL5SLmv7DivfNa') == expected
   
   expected = 'not-blockchain-address'
   assert normalize_address('not-blockchain-address') == expected # UnknownBlockchain exception raised 
   ```


