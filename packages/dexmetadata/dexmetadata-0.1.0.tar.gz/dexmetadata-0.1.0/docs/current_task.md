  For researching Uniswap V3 and other DEX interfaces:
  - Examine Uniswap V3 pool contracts to identify how token addresses are stored (different from V2)
  - Note that V3 uses slot0 and positions differently than V2's token0/token1 pattern
  - Research Aerodrome's fork-specific pool structure and factory patterns
  - Look at how these DEXs handle concentrated liquidity vs traditional pairs

  For modifying PoolMetadataFetcherFixed.sol:
  - Create a pluggable interface system for different DEX "adapters"
  - Consider using low-level calls with different signatures based on DEX type
  - Implement DEX detection logic at the beginning of your contract

  For conditional logic based on pool patterns:
  - Implement a factory registry approach to identify pool types by creator address
  - Consider bytecode fingerprinting to detect pool implementations
  - Use try/catch patterns for graceful fallbacks between different DEX interfaces

  This approach would maintain your deployless execution requirement while adding multi-DEX support.

<think>Let me analyze the current task and the relevant files to create a comprehensive plan for adding support for different DEX types (like Uniswap V3 and Aerodrome) to the metadata fetcher.

From `current_task.md`, I understand that we need to:
1. Research different DEX interfaces (Uniswap V3, Aerodrome, etc.)
2. Modify PoolMetadataFetcherFixed.sol to support different DEX types 
3. Implement conditional logic based on pool patterns

From the Solidity contract `PoolMetadataFetcherFixed.sol`, I see that it's currently designed to work with Uniswap V2-style pools only, relying on the `token0()` and `token1()` methods.

From `decoder.py`, I see that it's responsible for decoding the response data from the deployless contract execution.

The current implementation assumes a fixed structure for DEX pools (Uniswap V2-style), and we need to extend it to support more DEX types.</think># Plan for Multi-DEX Support Implementation

After examining the current task and codebase, I'll outline a step-by-step approach to adding support for different DEX types like Uniswap V3 and Aerodrome to our metadata fetcher.

## Current Architecture Analysis

Currently, our system:
1. Uses a deployless contract (`PoolMetadataFetcherFixed.sol`) that specifically targets Uniswap V2-style pools
2. Assumes all pools implement the same interface (token0/token1 methods)
3. Has a fixed decoder expecting the same result structure for all pools

## Implementation Plan

### Step 1: Research DEX Interfaces
Let's first understand the key differences between DEX interfaces:

#### Uniswap V2 (Current)
- Uses `token0()` and `token1()` methods to get token addresses
- Simple pair-based liquidity model

#### Uniswap V3
- Still has `token0()` and `token1()` methods but with different implementation
- Uses `slot0()` for current price and other state
- Has concentrated liquidity positions with tick ranges

#### Aerodrome/Velodrome
- Fork of Solidly with stable and volatile pairs
- May have different factory patterns and initialization

### Step 2: Contract Architecture Redesign

Let's modify `PoolMetadataFetcherFixed.sol` to support multiple DEX types:

```solidity
// High-level pseudocode for the new contract structure
contract PoolMetadataFetcherMultiDEX {
    // Same token/pool metadata structures
    
    // New enum to identify DEX types
    enum DEXType { UNKNOWN, UNISWAP_V2, UNISWAP_V3, AERODROME }
    
    constructor(address[] memory poolAddresses) {
        // Create results array
        
        for (uint i = 0; i < poolCount; i++) {
            address poolAddress = poolAddresses[i];
            
            // 1. Detect DEX type
            DEXType dexType = detectDEXType(poolAddress);
            
            // 2. Extract metadata based on DEX type
            if (dexType == DEXType.UNISWAP_V2) {
                // Use existing V2 logic
            } else if (dexType == DEXType.UNISWAP_V3) {
                // Use V3-specific logic
            } else if (dexType == DEXType.AERODROME) {
                // Use Aerodrome-specific logic
            } else {
                // Try fallback approach
            }
        }
        
        // Return results as before
    }
    
    // Detection function using bytecode patterns and factory registry
    function detectDEXType(address pool) internal view returns (DEXType) {
        // Implementation strategies:
        // 1. Try calling type-specific methods
        // 2. Check factory addresses 
        // 3. Check bytecode fingerprints
    }
}
```

### Step 3: Implement DEX Type Detection

We'll need to implement the `detectDEXType` function with several approaches:

1. **Factory Registry**:
   - Create a mapping of known factory addresses to DEX types
   - Check if the pool was created by a known factory

2. **Interface Testing**:
   - Try calling specific methods unique to each DEX type
   - For example, V3 has `fee()` method, Aerodrome has `stable()` method

3. **Bytecode Fingerprinting**:
   - Detect implementation by examining a small part of the contract bytecode
   - Use different fingerprints for different DEX types

### Step 4: Implement Pool-Specific Metadata Extraction

For each DEX type, we'll need specialized extraction logic:

1. **Uniswap V2** (existing):
   - Keep current implementation

2. **Uniswap V3**:
   - Extract token0/token1 addresses (same method names)
   - Add fee information from fee() method
   - Consider adding tick ranges or current price

3. **Aerodrome/Velodrome**:
   - Extract token0/token1
   - Add stable/volatile flag
   - Add factory information

### Step 5: Update Result Structure and Decoder

The Python decoder needs to be updated to handle the extended result format:

```python
# Extend the current result type to include DEX-specific fields
POOL_METADATA_RESULT_TYPE = (
    "(address,uint8,(address,string,string,uint8),(address,string,string,uint8),bytes)[]"
)
# Where:
# - uint8 is the DEX type enum
# - bytes is for DEX-specific extra data
```

Then update the decoder to handle the extended format:

```python
def decode_metadata_response(response_data: bytes) -> List[Dict[str, Any]]:
    """Decode extended response with DEX type information"""
    # Similar to existing code but handling the new fields
    # Convert DEX type enum to string
    # Parse DEX-specific data based on type
```

### Step 6: Update Python Client API

We'll need to update the main `fetch_pool_metadata` function to:

1. Keep the same simple interface
2. Add optional parameters for DEX-specific features
3. Handle the extended result format

```python
def fetch_pool_metadata(
    web3_provider: Web3, 
    pool_addresses: List[str],
    include_dex_info: bool = True
) -> List[Dict[str, Any]]:
    """
    Enhanced version that includes DEX type information
    and DEX-specific metadata
    """
    # Same basic implementation
    # Extended result processing for DEX-specific fields
```

### Step 7: Testing Approach

For each DEX type, we'll need test cases:

1. **Unit Tests**:
   - Test DEX type detection with mock contracts
   - Test metadata extraction for each DEX type

2. **Integration Tests**:
   - Test with real pools from different DEXs
   - Verify results match expected values

3. **Edge Cases**:
   - Test with non-standard implementations
   - Test with pools that don't match any known type

## Implementation Sequence

I recommend tackling this in the following order:

1. Start with the Solidity contract modifications for DEX detection
2. Implement Uniswap V3 support (closest to current V2)
3. Update the decoder for extended format
4. Add Aerodrome support
5. Finally, enhance the Python API

This approach allows us to make incremental progress while maintaining backward compatibility with existing code.

Would you like me to start implementing any specific part of this plan first?
