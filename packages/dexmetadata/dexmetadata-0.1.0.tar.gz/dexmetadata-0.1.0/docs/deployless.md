# https://github.com/wevm/viem/blob/c52c8ed2a2e18d1e0d433fe87990bc5539d579be/contracts/src/deployless/DeploylessCallViaBytecode.sol#L5

```
pragma solidity ^0.8.17;

// SPDX-License-Identifier: UNLICENSED

contract DeploylessCallViaBytecode {
    constructor(
        bytes memory bytecode,
        bytes memory data
    ) { 
        address to;
        assembly {
            to := create2(0, add(bytecode, 0x20), mload(bytecode), 0)
            if iszero(extcodesize(to)) {
                revert(0, 0)
            }
        }

        assembly {
            let success := call(gas(), to, 0, add(data, 0x20), mload(data), 0, 0)
            let ptr := mload(0x40)
            returndatacopy(ptr, 0, returndatasize())
            if iszero(success) {
                revert(ptr, returndatasize())
            }
            return(ptr, returndatasize())
        }
    }
}
```

Alternative implementation using factory pattern:

```
contract CounterfactualCall {
    
    error CounterfactualDeployFailed(bytes error);

    constructor(
        address smartAccount,
        address create2Factory, 
        bytes memory factoryData,
        address userOpBuilder, 
        bytes memory userOpBuilderCalldata
    ) { 
        if (address(smartAccount).code.length == 0) {
            (bool success, bytes memory ret) = create2Factory.call(factoryData);
            if (!success || address(smartAccount).code.length == 0) revert CounterfactualDeployFailed(ret);
        }

        assembly {
            let success := call(gas(), userOpBuilder, 0, add(userOpBuilderCalldata, 0x20), mload(userOpBuilderCalldata), 0, 0)
            let ptr := mload(0x40)
            returndatacopy(ptr, 0, returndatasize())
            if iszero(success) {
                revert(ptr, returndatasize())
            }
            return(ptr, returndatasize())
        }
    }
    
}
Here’s an example of calling this contract using the ethers and viem libraries:

// ethers
const nonce = await provider.call({
  data: ethers.utils.concat([
    counterfactualCallBytecode,
    (
      new ethers.utils.AbiCoder()).encode(['address','address', 'bytes', 'address','bytes'], 
      [smartAccount, userOpBuilder, getNonceCallData, factory, factoryData]
    )
  ])
})

// viem
const nonce = await client.call({
  data: encodeDeployData({
    abi: parseAbi(['constructor(address, address, bytes, address, bytes)']),
    args: [smartAccount, userOpBuilder, getNonceCalldata, factory, factoryData],
    bytecode: counterfactualCallBytecode,
  })
})

```

other example multicall contract
```
// SPDX-License-Identifier: MIT

pragma solidity 0.8.9;

contract DeploylessMulticall {
    struct Call {
        address target;
        bytes callData;
    }

    constructor(Call[] memory calls) {
        uint256 blockNumber = block.number;
        bytes[] memory returnData = new bytes[](calls.length);
        for (uint256 i = 0; i < calls.length; i++) {
            (bool success, bytes memory ret) = calls[i].target.call(calls[i].callData);
            require(success);
            returnData[i] = ret;
        }

        assembly {
            // 'Multicall.aggregate' returns (uint256, bytes[])
            // Overwrite memory to comply with the expected format
            mstore(sub(returnData, 0x40), blockNumber)
            mstore(sub(returnData, 0x20), 0x40)

            // Fix returnData index pointers
            let indexOffset := add(returnData, 0x20)
            for
                { let pointerIndex := add(returnData, 0x20) }
                lt(pointerIndex, add(returnData, mul(add(mload(returnData), 1), 0x20)))
                { pointerIndex := add(pointerIndex, 0x20) }
            {
                mstore(pointerIndex, sub(mload(pointerIndex), indexOffset))
            }
            
            return(
                sub(returnData, 0x40),
                // We assume that 'returnData' is placed at the end of memory
                // Therefore, 'sub(mload(0x40), returnData)' provides the array length
                add(sub(mload(0x40), returnData), 0x40)
            )
        }
    }
}
```

Article: Explanation of how deployless multicall works:

<article>
Deployless Multicall for historical EVM data
8 October 2021
TL;DR: source code ↗.

EVM, despite its shortcomings and occasional weirdness, is an exciting platform. Here, I’m exploring the idea of calling a contract without deploying it.

Read-only deploy
As pointed out ↗ by adietrichs, it’s possible to do any read-only computation on EVM without actually deploying a contract. Here’s how.

First, you write a contract that does some computation in its constructor. Since a constructor can’t return anything in Solidity (it returns its source code), you put the results of your computation into an immutable variable.

Second, you compile that contract to get its bytecode, and call eth_call against an EVM node with data param equals to the bytecode. A result of that call would be the contract’s source code. Since immutable variables are stored in the source code, you can access your computation result as a part of it.

Idea
Being a fan of another “invention”, Multicall contract ↗, I was curious: is it possible to merge two concepts? Could we use Multicall without deploying it?

To be fair, if all you want is to query the current blockchain state efficiently, just deploying Multicall or using an existing deployment is the way to go. Hopefully, there are deployments available on most of the existing EVM chains.

But what if you want to query the historical state? In that case, Multicall may have been not deployed yet. This is especially the case for Multicall2 on Ethereum, which was deployed only recently.

First try
Just to confirm it’s working, I first made a contract that queries a token balance. Here’s the source code:

contract ImmutableBalanceLens {
    uint256 public immutable balance;

    constructor(ERC20 token, address owner) {
        balance = token.balanceOf(owner);
    }
}
If you compile that contract and make a read-only deployment as described above, you will be able to access balance.

Now let’s try to use the same technique with Multicall.

// Will not compile
contract ImmutableMulticall {
    bytes[] public immutable returnData;

    constructor(Call[] memory calls) {
        // Multicall's logic
        // ...
    }
}
Unfortunately, this will not work. You see, immutable supports only fixed-length data (e.g. uint256, a fixed-length array of bytes8, etc). What we need to store is a multidimensional dynamic array. Oh.

Diving into Assembly
We can’t use immutable to store dynamic-length data, so the only way to make it work is to somehow make our constructor return the result. Fortunately, there’s a way to accomplish that. Enter a universe of low-level programming.

Now, I’m not an assembly expert. What I realized is that it’s really easy to shoot yourself in the foot when using low-level language. Also, Solidity abstracts a truckload of low-level interactions, including memory management, ABI encoding, EVM instructions, etc. Finally, I likely did some things the wrong way, and you should not treat this code as the way to do it.

There’s a great documentation covering the basics ↗ and available instructions ↗. I was also inspired by some low-level Solidity libraries employing inline assembly to its fullest, like BytesUtils ↗.

First, as an exercise, let’s rewrite our ImmutableBalanceLens contract to use assembly:

contract AssemblyBalanceLens {
    constructor(ERC20 token, address owner) {
        uint256 _balance = token.balanceOf(owner);

        assembly {
            mstore(0, _balance)
            return(0, 32)
        }
    }
}
As you can see, we use two low-level instructions here. mstore puts _balance at index 0 of contract’s memory, and return, well, returns the part of memory that starts at 0 and has a length of 32.

Note: in general, you should put new variables after all the previously allocated memory. We will dive a bit into that, but you can read how Solidity allocates memory here ↗.

If we eth_call this contract, we will get the same value as when using ImmutableBalanceLens. Awesome!

Now let’s adjust the Multicall contract using this method of returning arbitrary data from the constructor.

contract AssemblyMulticall {
    constructor(Call[] memory calls) {
        // Multicall's code
        // ...
        bytes[] memory returnData = new bytes[](calls.length);
        // ...

        assembly {
            return(returnData, sub(mload(0x40), returnData))
        }
    }
}
The assembly part is pretty simple here, but it requires some knowledge of Solidity and EVM internals to understand it.

First, there is bytes[] memory returnData = new bytes[](calls.length); line in the original contract, which means that the entire returnData array will be stored in memory.

Second, as per docs,

0x40 - 0x5f (32 bytes): currently allocated memory size (aka. free memory pointer)

Therefore, calling mload(0x40) will yield the total allocated memory length.

Finally, due to the structure of our contract, returnData will be placed at the bottom of the memory heap. This is not a guarantee provided by Solidity in any way, this is simply how the current version of the compiler allocates the memory. Hopefully, we operate at the bytecode level, which kinda “sticks” the current compiler version.

Taking all of the above into consideration, return(returnData, sub(mload(0x40), returnData)) returns the part of memory that starts at pointer returnData and ends at the end of memory heap, which is also the end of returnData.

Final details

Multicall sample output. Stare long enough and you'll start to see uints and arrays.
While we have a working prototype, it still requires some changes to be fully compatible with the original Multicall contract. First, pointers to array elements of returnData are incorrect. Second, we’re missing the block part of the Multicall response, which returns the block number at the time of querying. Let’s fix that:

contract AssemblyMulticall {
    constructor(Call[] memory calls) {
        // Multicall's logic
        // ...

        assembly {
            // 'Multicall.aggregate' returns (uint256, bytes[])
            // Overwrite memory to comply with the expected format
            mstore(sub(returnData, 0x40), blockNumber)
            mstore(sub(returnData, 0x20), 0x40)

            // Fix returnData index pointers
            let indexOffset := add(returnData, 0x20)
            for
                { let pointerIndex := add(returnData, 0x20) }
                lt(pointerIndex, add(returnData, mul(add(mload(returnData), 1), 0x20)))
                { pointerIndex := add(pointerIndex, 0x20) }
            {
                mstore(pointerIndex, sub(mload(pointerIndex), indexOffset))
            }

            return(
                sub(returnData, 0x40),
                // We assume that 'returnData' is placed at the end of memory
                // Therefore, 'sub(mload(0x40), returnData' provides the array length
                add(sub(mload(0x40), returnData), 0x40)
            )
        }
    }
}
The changes may seem monstrous but are pretty simple. The trickiest part is to calculate the index offset, and then to update each pointer to the bytes array elements.

Original Multicall contract provides a helper function to get ether balance of a given account. Since we can’t access that function in the original contract, we need to provide it ourselves. I was hoping to add support for that, but I couldn’t find a decent way to do it.

We’re on the finish line! The last thing to do is to add support for Multicall2, which is the same as the original all, except it adds tryAggregate method, which doesn’t throw if one of the underlying calls throw.

Unfortunately for me, in the Multicall2 contract returnData is not stored in memory as neatly as it did in the original contract. I had to switch some booleans back and forth, as well as fix some indices inside each (boolean, bytes) tuple. I also had to update array element pointers, same as in the Multicall contract. The changes were pretty basic, but having to do all that in assembly was a PITA.

Since the new contract heavily relies on assembly, I was entertaining the idea of rewriting the calling part of the contract with assembly as well. I wasn’t sure what gains it will bring and how much time it will take, so I left it for the next time.

Performance
Since the deployless version of Multicall has the overhead of creating and initializing a contract, I assumed that it will be noticeably slower than calling a deploying version. Thus I decided to calculate that impact.

I’ve measured the time it takes to fetch DAI balances for 100 randomly selected accounts. Each strategy (Multicall/Multicall2, deployed/deployless) was run 20 times. Here’s what I got:

Multicall: 17.145s
Deployless Multicall: 18.412s
Multicall2: 15.716s
Deployless Multicall2: 15.772s
Overall, it doesn’t seem there’s a significant impact on fetching speed, although I’d still use the deployed version whenever possible.


</article>