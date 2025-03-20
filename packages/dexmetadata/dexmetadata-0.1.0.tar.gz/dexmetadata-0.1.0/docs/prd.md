## Deployless Metadata Fetcher for DEX Pools

This document outlines the requirements and approach for creating a Python script to fetch metadata for decentralized exchange (DEX) pools, such as token addresses, names, symbols, and decimals.  The script will be designed to be efficient and work across different blockchains and DEX types (like Uniswap V2, Uniswap V3, Aerodrome) using a single blockchain request.

### Goal

Create a Python script that, given a list of DEX pool addresses, retrieves the following metadata for each pool:

1. **Token 0 Address:** Address of the first token in the pair.
2. **Token 1 Address:** Address of the second token in the pair.
3. **Token 0 Decimals:** Decimal precision of Token 0.
4. **Token 1 Decimals:** Decimal precision of Token 1.
5. **Token 0 Name:** Name of Token 0.
6. **Token 1 Name:** Name of Token 1.
7. **Token 0 Symbol:** Symbol of Token 0.
8. **Token 1 Symbol:** Symbol of Token 1.

### Approach: Deployless Multicall

To maximize efficiency and compatibility across different blockchains (some of which might not have a deployed 'multicall' contract), we will utilize a "deployless" contract call technique.

**Concept of Deployless Contract Calls:**

Instead of calling a *deployed* smart contract, we will create a special smart contract whose logic is executed directly within the blockchain's read-only call operation (`eth_call`).  This is achieved by providing the compiled bytecode of a contract directly within the `eth_call` data.  The constructor of this temporary contract will contain the logic to fetch the desired metadata. The result of the constructor's execution will be returned as the output of the `eth_call`.

This approach allows us to perform multiple contract interactions (like fetching metadata from different tokens and pool factories) within a single blockchain request, significantly reducing the number of calls needed.

**Solidity Contract Logic (Conceptual):**

We will conceptually design a simple Solidity contract that, in its constructor, performs the following steps for each input pool address:

1. **Determine DEX Type**:  Based on the input pool address (or potentially an associated factory address), identify if it's a Uniswap V2, Uniswap V3, Aerodrome, or another DEX type.  For simplicity in the initial version, let's assume all input addresses are from a DEX where we can get token0 and token1 using a common pattern. For example, for Uniswap V2-like pools directly calling `token0()` and `token1()` on the pool contract.
2. **Fetch Token Addresses**:  For each pool address, call the `token0()` and `token1()` functions on the pool contract to get the addresses of the two tokens in the pair.
3. **Fetch Token Metadata**: For each token address obtained in the previous step, call the ERC20 functions:

   - `decimals()` to get the decimal precision.
   - `name()` to get the token name.
   - `symbol()` to get the token symbol.
4. **Structure and Return Data**: Organize the fetched metadata for each pool into a structured format (like a list of dictionaries) and return it as the output of the constructor.  The constructor will use assembly to directly return this encoded data.

**Python Script Outline:**

The Python script will perform the following steps:

1. **Setup Web3.py:**

   - Import necessary libraries from `web3.py`.
   - Initialize a Web3 provider to connect to the desired blockchain (e.g., using an RPC URL).
2. **Solidity Bytecode Generation (Pre-computation - not part of runtime script initially):**

   - Write a simple Solidity contract as described conceptually above. You do *not* need to output this solidity code as part of this task, just the *concept* is explained here for context.
   - Compile this Solidity contract to obtain its bytecode. This bytecode will be hardcoded or loaded into the Python script. For now, a placeholder bytecode can be used, and the actual Solidity contract and compilation will be a later step.
3. **Input Data Encoding:**

   - Create a function to encode the input pool addresses into a format suitable for passing as constructor arguments to the deployless contract.  This will likely involve ABI encoding of an array of addresses.
4. **`eth_call` Execution:**

   - Construct the `data` parameter for the `eth_call` function. This data will consist of:
       - The pre-computed bytecode of our deployless contract.
       - The ABI-encoded input data (pool addresses).
   - Use `web3.eth.call` to execute the deployless contract call.
5. **Output Data Decoding:**

   - Create a function to decode the output data returned by the `eth_call`.  This data will be ABI-encoded and needs to be parsed back into Python data structures (likely a list of dictionaries, where each dictionary represents the metadata for a pool).
6. **Main Function:**

   - Define a main function that:
       - Takes a list of pool addresses as input.
       - Encodes the input addresses.
       - Executes the `eth_call` using the deployless bytecode and encoded input data.
       - Decodes the returned data.
       - Prints or returns the metadata in a user-friendly format.

**Example Python Function Signature:**

```

from typing import List, Dict

def fetch_pool_metadata(pool_addresses: List[str]) -> List[Dict[str, str]]:

    """

    Fetches metadata for a list of DEX pool addresses using deployless multicall.

    Args:

        pool_addresses: A list of pool contract addresses (as strings).

    Returns:

        A list of dictionaries, where each dictionary contains metadata for a pool.

        Example:

        [

            {

                "pool_address": "0x...",

                "token0_address": "0x...",

                "token1_address": "0x...",

                "token0_decimals": "18",

                "token1_decimals": "6",

                "token0_name": "Token A",

                "token1_name": "Token B",

                "token0_symbol": "TKA",

                "token1_symbol": "TKB",

            },

            ...

        ]

    """

    # ... implementation details ...

    pass

# Example usage

pool_addresses_input = [

    "0x...",  # Pool address 1

    "0x...",  # Pool address 2

    # ... more pool addresses

]

pool_metadata_list = fetch_pool_metadata(pool_addresses_input)

for metadata in pool_metadata_list:

    print(f"Pool Address: {metadata['pool_address']}")

    print(f"  Token 0: {metadata['token0_symbol']} ({metadata['token0_address']}), Decimals: {metadata['token0_decimals']}, Name: {metadata['token0_name']}")

    print(f"  Token 1: {metadata['token1_symbol']} ({metadata['token1_address']}), Decimals: {metadata['token1_decimals']}, Name: {metadata['token1_name']}")

    print("-" * 30)

```

**Extensibility:**

To support more DEX types (beyond Uniswap V2-like), the Solidity contract would need to be modified to include logic for detecting the DEX type and using the appropriate methods to fetch token addresses and possibly handle different patterns for getting tokens or factory contracts. This might involve:

- Checking contract code or using heuristics to identify DEX type.
- Using different factory contracts or function calls based on DEX type to get token addresses.

For now, focusing on Uniswap V2-like pool structure is a good starting point for a functional script, and extensibility can be considered in later iterations.

**Next Steps for Development:**

1. **Implement the Solidity Logic Conceptually Described above**: (This is a separate task for a Solidity developer, but conceptually understood for Python script development).
2. **Obtain the Bytecode** of the compiled Solidity contract (Placeholder can be used initially for Python script development).
3. **Implement the Python script** based on the outline, starting with encoding input addresses, performing `eth_call` with placeholder bytecode, and then decoding (initially, decoding can be stubbed).
4. **Test** with a few Uniswap V2 pool addresses on base network
5. **Refine and Extend** the script to handle more DEX types and error conditions as needed.