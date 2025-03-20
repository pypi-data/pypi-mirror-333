# Deployless Metadata Fetcher - Implementation Learnings

This document captures key insights from our successful implementation of deployless contract execution for fetching DEX pool metadata.

## What is Deployless Execution?

Deployless execution is a technique that allows executing contract code without deploying it to the blockchain. It works by:

1. Compiling a Solidity contract into bytecode
2. Sending the bytecode as the `data` parameter in an `eth_call` to the blockchain
3. Receiving the result of the constructor's execution, which contains the data we want

This approach is powerful because it allows executing complex logic in a single RPC call without requiring any deployed contracts.

## Key Requirements for Successful Deployless Execution

1. **Omit the 'to' Field in eth_call**
   
   The most critical requirement is to omit the 'to' field in the eth_call request:
   ```json
   {
     "data": "<bytecode>",
     "gas": 30000000
   }
   ```
   Including a 'to' address (even 0x0) causes the RPC to treat it as a regular contract call rather than a deployless execution.

2. **Return Assembly Pattern**
   
   For returning complex data from the constructor, this assembly pattern works reliably:
   ```solidity
   assembly {
       return(add(encodedData, 32), mload(encodedData))
   }
   ```
   
   Where `encodedData` is the ABI-encoded data we want to return.

3. **Correct ABI Type Definition**
   
   For our pool metadata structure, the correct ABI type definition is:
   ```
   (address,(address,string,string,uint8),(address,string,string,uint8))[]
   ```
   
   This represents an array of tuples containing:
   - Pool address
   - Token0 metadata (address, name, symbol, decimals)
   - Token1 metadata (address, name, symbol, decimals)

## Implementation Strategy

Our working implementation follows this strategy:

1. **Contract Structure**
   - Define structs for `TokenMetadata` and `PoolMetadata`
   - Implement a constructor that takes pool addresses as input 
   - Fetch token addresses and metadata for each pool
   - Return the structured data using assembly

2. **Token Metadata Fetching**
   - Use try/catch to handle ERC20 interface calls
   - Provide fallback values for non-standard tokens
   - Keep gas usage minimal by avoiding complex operations

3. **Python Integration**
   - Encode pool addresses as constructor arguments
   - Perform the eth_call without a 'to' address
   - Decode the returned data using the correct ABI type
   - Format the result into a user-friendly structure

## Asyncio Implementation

We've significantly improved performance by implementing an asynchronous processing approach:

1. **Connection Pooling**
   - Reuse Web3 provider instances to avoid connection overhead
   - Implement a global semaphore to limit concurrent connections

2. **Concurrent Batch Processing**
   - Process multiple batches in parallel with asyncio.gather()
   - Control concurrency with a configurable semaphore
   - Demonstrated up to 80% performance improvement in stress tests

3. **Backwards Compatibility**
   - Maintained the original sync interface with transparent async implementation
   - Added new async-specific parameters for fine-tuning performance

Example performance comparison from stress test with batch_size=2:
```
Sequential execution time: 15.27 seconds
Parallel execution time: 3.18 seconds
Improvement: 79.2%
```

Performance improvement varies based on test parameters:
- With small batch_size (2-5), concurrent processing shows 75-80% improvement
- With larger batch_size (20-30), improvement is around 45-50%
- This difference occurs because larger batches already provide significant optimization, so adding concurrency has less relative impact

Our optimization script identified batch_size=20 with 2 concurrent batches as optimal for Ankr's Base RPC, showing a 45.7% improvement over sequential execution with the same batch size. This balanced approach maximizes throughput while minimizing RPC errors.

## Challenges and Solutions

1. **RPC Compatibility**
   
   While our implementation works across Base, Arbitrum, and Optimism, not all RPC providers support deployless execution. Some may block it for security reasons.
   
   Solution: Test your implementation with your specific RPC provider.

2. **Bytecode Stability**
   
   Once you have working bytecode, be very careful with recompilation. Small changes in the Solidity code can result in different bytecode that might not work.
   
   Solution: Save known working bytecode and use it directly rather than recompiling.

3. **Gas Limitations**
   
   Complex operations in deployless execution can hit gas limits or cause stack underflow errors.
   
   Solution: Keep the contract logic simple and focused on the data you need.

4. **Rate Limiting**
   
   RPC providers impose rate limits that can cause failures when making many parallel requests:
   - Ankr provides ~1800 requests/minute guaranteed (more possible depending on load)
   - Other providers have similar limits, often ranging from 100-2000 requests/minute
   
   Solutions:
   - Use connection pooling to reduce connection overhead
   - Implement configurable concurrency limits (`max_concurrent_batches`)
   - Balance batch size and concurrency to stay within rate limits
   - Add retry logic with exponential backoff for occasional rate limit errors
   
   Our optimization script calculates theoretical requests per minute based on measured response times to help identify settings that might approach rate limits.

## DEX Support

The current implementation supports Uniswap V2-style pools that have `token0()` and `token1()` functions. To support other DEX types:

1. Identify the interface pattern for the specific DEX
2. Add conditional logic to handle different pool types
3. Test extensively with different pool contracts

## Final Implementation

Our successful implementation:
- Fetches real token metadata (addresses, names, symbols, decimals) for multiple pools in a single call
- Works across multiple EVM-compatible chains
- Handles errors gracefully with fallback values
- Uses minimal gas by focusing only on the necessary operations
- Leverages asyncio for parallel processing and significant performance improvements
- Provides both synchronous and asynchronous APIs for flexibility

This approach is significantly more efficient than making multiple separate calls for each pool and token, especially when working with many pools at once.