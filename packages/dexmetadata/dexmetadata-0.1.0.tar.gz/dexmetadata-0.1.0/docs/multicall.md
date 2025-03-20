<file_map>
├── metadata_fetcher
│   ├── docs
│   │   ├── current_task.md
│   │   ├── deployless.md
│   │   ├── learnings.md
│   │   ├── multicall_optimizations.md
│   │   ├── optimizations.md
│   │   └── prd.md
│   ├── examples
│   │   └── fetch.py
│   ├── src
│   │   └── dexmetadata
│   │       ├── .cache
│   │       │   └── PoolMetadataFetcher.json
│   │       ├── contracts
│   │       │   ├── PoolMetadataFetcher.f38dbc81.bin
│   │       │   └── PoolMetadataFetcher.sol
│   │       ├── __init__.py
│   │       ├── bytecode.py
│   │       ├── decoder.py
│   │       ├── fetcher.py
│   │       └── py.typed
│   ├── tests
│   │   ├── __init__.py
│   │   ├── conftest.py
│   │   ├── test_bytecode.py
│   │   └── test_decoder.py
│   ├── .env.template
│   ├── CLAUDE.md
│   ├── pyproject.toml
│   ├── README.md
│   └── uv.lock

├── cryo-main
│   ├── .github
│   │   ├── ISSUE_TEMPLATE
│   │   │   ├── bug_report.md
│   │   │   ├── feature_request.md
│   │   │   └── question.md
│   │   ├── workflows
│   │   │   ├── build_and_test.yml
│   │   │   └── python_release.yml
│   │   └── PULL_REQUEST_TEMPLATE.md
│   ├── book
│   │   ├── additional_reading
│   │   │   └── additional_reading.md
│   │   ├── basic_usage
│   │   │   ├── basic_usage.md
│   │   │   ├── data_acquisition.md
│   │   │   ├── data_formatting.md
│   │   │   ├── data_querying.md
│   │   │   └── data_selection.md
│   │   ├── contributing
│   │   │   ├── adding_a_dataset.md
│   │   │   ├── contributing.md
│   │   │   └── repository_layout.md
│   │   ├── cookbook
│   │   │   ├── cookbook.md
│   │   │   ├── reorgs.md
│   │   │   └── uniswap.md
│   │   ├── cryo_python
│   │   │   ├── example_usage.md
│   │   │   ├── installation.md
│   │   │   ├── overview.md
│   │   │   ├── reference.md
│   │   │   └── speed.md
│   │   ├── datasets
│   │   │   ├── address_appearances.md
│   │   │   ├── balance_diffs.md
│   │   │   ├── balance_reads.md
│   │   │   ├── balances.md
│   │   │   ├── blocks.md
│   │   │   ├── code_diffs.md
│   │   │   ├── code_reads.md
│   │   │   ├── codes.md
│   │   │   ├── contracts.md
│   │   │   ├── dataset_guide.md
│   │   │   ├── dataset_reference.md
│   │   │   ├── erc20_balances.md
│   │   │   ├── erc20_metadata.md
│   │   │   ├── erc20_supplies.md
│   │   │   ├── erc20_transfers.md
│   │   │   ├── erc721_metadata.md
│   │   │   ├── erc721_transfers.md
│   │   │   ├── eth_calls.md
│   │   │   ├── four_byte_counts.md
│   │   │   ├── geth_balance_diffs.md
│   │   │   ├── geth_calls.md
│   │   │   ├── geth_code_diffs.md
│   │   │   ├── geth_nonce_diffs.md
│   │   │   ├── geth_opcodes.md
│   │   │   ├── geth_storage_diffs.md
│   │   │   ├── javascript_traces.md
│   │   │   ├── logs.md
│   │   │   ├── native_transfers.md
│   │   │   ├── nonce_diffs.md
│   │   │   ├── nonce_reads.md
│   │   │   ├── nonces.md
│   │   │   ├── slot_diffs.md
│   │   │   ├── slot_reads.md
│   │   │   ├── slots.md
│   │   │   ├── storage_reads.md
│   │   │   ├── trace_calls.md
│   │   │   ├── traces.md
│   │   │   ├── transactions.md
│   │   │   └── vm_traces.md
│   │   ├── intro
│   │   │   ├── concepts.md
│   │   │   ├── data_sources.md
│   │   │   ├── example_usage.md
│   │   │   ├── installation.md
│   │   │   ├── interfaces.md
│   │   │   ├── intro.md
│   │   │   └── quickstart.md
│   │   ├── reference
│   │   │   ├── interfaces
│   │   │   │   ├── cli.md
│   │   │   │   ├── interfaces.md
│   │   │   │   ├── python.md
│   │   │   │   └── rust.md
│   │   │   └── reference.md
│   │   ├── cryo_python.md
│   │   ├── quickstart.md
│   │   └── SUMMARY.md
│   ├── crates
│   │   ├── cli
│   │   │   ├── src
│   │   │   │   ├── parse
│   │   │   │   │   ├── args.rs
│   │   │   │   │   ├── blocks.rs
│   │   │   │   │   ├── execution.rs
│   │   │   │   │   ├── file_output.rs
│   │   │   │   │   ├── mod.rs
│   │   │   │   │   ├── parse_utils.rs
│   │   │   │   │   ├── partitions.rs
│   │   │   │   │   ├── query.rs
│   │   │   │   │   ├── schemas.rs
│   │   │   │   │   ├── source.rs
│   │   │   │   │   └── timestamps.rs
│   │   │   │   ├── args.rs
│   │   │   │   ├── lib.rs
│   │   │   │   ├── main.rs
│   │   │   │   ├── remember.rs
│   │   │   │   └── run.rs
│   │   │   ├── tests
│   │   │   │   └── tests.rs
│   │   │   └── Cargo.toml
│   │   ├── freeze
│   │   │   ├── src
│   │   │   │   ├── datasets
│   │   │   │   │   ├── address_appearances.rs
│   │   │   │   │   ├── balance_diffs.rs
│   │   │   │   │   ├── balance_reads.rs
│   │   │   │   │   ├── balances.rs
│   │   │   │   │   ├── blocks.rs
│   │   │   │   │   ├── code_diffs.rs
│   │   │   │   │   ├── code_reads.rs
│   │   │   │   │   ├── codes.rs
│   │   │   │   │   ├── contracts.rs
│   │   │   │   │   ├── erc20_approvals.rs
│   │   │   │   │   ├── erc20_balances.rs
│   │   │   │   │   ├── erc20_metadata.rs
│   │   │   │   │   ├── erc20_supplies.rs
│   │   │   │   │   ├── erc20_transfers.rs
│   │   │   │   │   ├── erc721_metadata.rs
│   │   │   │   │   ├── erc721_transfers.rs
│   │   │   │   │   ├── eth_calls.rs
│   │   │   │   │   ├── four_byte_counts.rs
│   │   │   │   │   ├── geth_balance_diffs.rs
│   │   │   │   │   ├── geth_calls.rs
│   │   │   │   │   ├── geth_code_diffs.rs
│   │   │   │   │   ├── geth_nonce_diffs.rs
│   │   │   │   │   ├── geth_opcodes.rs
│   │   │   │   │   ├── geth_storage_diffs.rs
│   │   │   │   │   ├── javascript_traces.rs
│   │   │   │   │   ├── logs.rs
│   │   │   │   │   ├── mod.rs
│   │   │   │   │   ├── native_transfers.rs
│   │   │   │   │   ├── nonce_diffs.rs
│   │   │   │   │   ├── nonce_reads.rs
│   │   │   │   │   ├── nonces.rs
│   │   │   │   │   ├── slots.rs
│   │   │   │   │   ├── storage_diffs.rs
│   │   │   │   │   ├── storage_reads.rs
│   │   │   │   │   ├── trace_calls.rs
│   │   │   │   │   ├── traces.rs
│   │   │   │   │   ├── transactions.rs
│   │   │   │   │   └── vm_traces.rs
│   │   │   │   ├── multi_datasets
│   │   │   │   │   ├── blocks_and_transactions.rs
│   │   │   │   │   ├── call_trace_derivatives.rs
│   │   │   │   │   ├── geth_state_diffs.rs
│   │   │   │   │   ├── mod.rs
│   │   │   │   │   ├── state_diffs.rs
│   │   │   │   │   └── state_reads.rs
│   │   │   │   ├── types
│   │   │   │   │   ├── chunks
│   │   │   │   │   │   ├── binary_chunk.rs
│   │   │   │   │   │   ├── chunk_ops.rs
│   │   │   │   │   │   ├── chunk.rs
│   │   │   │   │   │   ├── mod.rs
│   │   │   │   │   │   ├── number_chunk.rs
│   │   │   │   │   │   └── subchunks.rs
│   │   │   │   │   ├── collection
│   │   │   │   │   │   ├── collect_by_block.rs
│   │   │   │   │   │   ├── collect_by_transaction.rs
│   │   │   │   │   │   ├── collect_generic.rs
│   │   │   │   │   │   └── mod.rs
│   │   │   │   │   ├── dataframes
│   │   │   │   │   │   ├── creation.rs
│   │   │   │   │   │   ├── export.rs
│   │   │   │   │   │   ├── mod.rs
│   │   │   │   │   │   ├── read.rs
│   │   │   │   │   │   ├── sort.rs
│   │   │   │   │   │   └── u256s.rs
│   │   │   │   │   ├── datatypes
│   │   │   │   │   │   ├── datatype_macros.rs
│   │   │   │   │   │   ├── meta.rs
│   │   │   │   │   │   ├── mod.rs
│   │   │   │   │   │   ├── multi.rs
│   │   │   │   │   │   └── scalar.rs
│   │   │   │   │   ├── decoders
│   │   │   │   │   │   ├── log_decoder.rs
│   │   │   │   │   │   └── mod.rs
│   │   │   │   │   ├── columns.rs
│   │   │   │   │   ├── conversions.rs
│   │   │   │   │   ├── errors.rs
│   │   │   │   │   ├── execution.rs
│   │   │   │   │   ├── files.rs
│   │   │   │   │   ├── mod.rs
│   │   │   │   │   ├── partitions.rs
│   │   │   │   │   ├── queries.rs
│   │   │   │   │   ├── reports.rs
│   │   │   │   │   ├── rpc_params.rs
│   │   │   │   │   ├── schemas.rs
│   │   │   │   │   ├── signatures.rs
│   │   │   │   │   ├── sources.rs
│   │   │   │   │   └── summaries.rs
│   │   │   │   ├── collect.rs
│   │   │   │   ├── freeze.rs
│   │   │   │   └── lib.rs
│   │   │   ├── build.rs
│   │   │   └── Cargo.toml
│   │   ├── python
│   │   │   ├── .github
│   │   │   │   └── workflows
│   │   │   │       └── CI.yml
│   │   │   ├── python
│   │   │   │   ├── cryo
│   │   │   │   │   ├── __init__.py
│   │   │   │   │   ├── _args.py
│   │   │   │   │   ├── _collect.py
│   │   │   │   │   ├── _freeze.py
│   │   │   │   │   ├── _spec.py
│   │   │   │   │   └── py.typed
│   │   │   │   └── cryo_test
│   │   │   │       ├── cryo_test
│   │   │   │       │   ├── cli
│   │   │   │       │   │   ├── __init__.py
│   │   │   │       │   │   ├── cli_classes.py
│   │   │   │       │   │   ├── cli_run.py
│   │   │   │       │   │   ├── cli_summary.py
│   │   │   │       │   │   └── cli_utils.py
│   │   │   │       │   ├── commands
│   │   │   │       │   │   ├── __init__.py
│   │   │   │       │   │   ├── command_generation.py
│   │   │   │       │   │   ├── command_parsing.py
│   │   │   │       │   │   └── command_types.py
│   │   │   │       │   ├── files
│   │   │   │       │   │   ├── __init__.py
│   │   │   │       │   │   ├── file_io.py
│   │   │   │       │   │   └── file_paths.py
│   │   │   │       │   ├── __init__.py
│   │   │   │       │   ├── __main__.py
│   │   │   │       │   ├── comparison.py
│   │   │   │       │   ├── defaults.py
│   │   │   │       │   ├── polars_utils.py
│   │   │   │       │   └── scripts.py
│   │   │   │       ├── examples
│   │   │   │       │   └── ethers_vs_alloy
│   │   │   │       │       ├── build_cryo
│   │   │   │       │       └── compare_alloy_to_ethers
│   │   │   │       ├── pyproject.toml
│   │   │   │       └── README.md
│   │   │   ├── python_tests
│   │   │   │   ├── test_chunks.py
│   │   │   │   ├── test_columns.py
│   │   │   │   ├── test_datatypes.py
│   │   │   │   └── test_output_formats.py
│   │   │   ├── rust
│   │   │   │   ├── collect_adapter.rs
│   │   │   │   ├── freeze_adapter.rs
│   │   │   │   └── lib.rs
│   │   │   ├── build.rs
│   │   │   ├── Cargo.toml
│   │   │   ├── pyproject.toml
│   │   │   └── README.md
│   │   └── to_df
│   │       ├── src
│   │       │   └── lib.rs
│   │       └── Cargo.toml
│   ├── examples
│   │   ├── all.sh
│   │   ├── erc20_balances.sh
│   │   └── uniswap.sh
│   ├── book.toml
│   ├── Cargo.lock
│   ├── Cargo.toml
│   ├── CONTRIBUTING.md
│   ├── LICENSE-APACHE
│   ├── LICENSE-MIT
│   ├── README.md
│   └── rustfmt.toml

├── multicall.py-master
│   ├── .github
│   │   └── workflows
│   │       └── black.yaml
│   ├── examples
│   │   ├── daistats.py
│   │   └── mcd_exporter.py
│   ├── multicall
│   │   ├── __init__.py
│   │   ├── call.py
│   │   ├── constants.py
│   │   ├── exceptions.py
│   │   ├── loggers.py
│   │   ├── multicall.py
│   │   ├── signature.py
│   │   └── utils.py
│   ├── tests
│   │   ├── __init__.py
│   │   ├── conftest.py
│   │   ├── test_call.py
│   │   ├── test_multicall.py
│   │   ├── test_signature.py
│   │   └── test_utils.py
│   ├── license
│   ├── poetry.lock
│   ├── pyproject.toml
│   └── readme.md

</file_map>

<file_contents>
File: .github/workflows/black.yaml
```yaml
name: Black Formatter

on:
  pull_request:
    branches:
      - master

jobs:
  format:
    runs-on: ubuntu-latest

    steps:
    - name: Checkout code
      uses: actions/checkout@v3
      with:
        ref: ${{ github.head_ref }}  # Check out the PR branch

    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.12'

    - name: Install Black
      run: pip install black

    - name: Run Black
      run: black .

    - name: Check for changes
      id: changes
      run: |
        if [[ -n $(git status --porcelain) ]]; then
          echo "changes_detected=true" >> $GITHUB_ENV
        else
          echo "changes_detected=false" >> $GITHUB_ENV
        fi

    - name: Commit changes
      if: env.changes_detected == 'true'
      run: |
        git config --local user.name "github-actions[bot]"
        git config --local user.email "github-actions[bot]@users.noreply.github.com"
        git add .
        git commit -m "chore: \`black .\`"
        git push
```

File: examples/daistats.py
```py
from decimal import Decimal
from web3.datastructures import AttributeDict
from multicall import Call, Multicall


MCD_VAT = "0x35d1b3f3d7966a1dfe207aa4514c12a259a0492b"
MCD_VOW = "0xa950524441892a31ebddf91d3ceefa04bf454466"
MCD_DAI = "0x6b175474e89094c44da98b954eedeac495271d0f"
UNISWAP_EXCHANGE = "0x2a1530C4C41db0B0b2bB646CB5Eb1A67b7158667"
SAI = "0x89d24a6b4ccb1b6faa2625fe562bdd9a23260359"
MCD_JOIN_SAI = "0xad37fd42185ba63009177058208dd1be4b136e6b"
MCD_GOV = "0x9f8f72aa9304c8b593d555f12ef6589cc3a579a2"
GEM_PIT = "0x69076e44a9C70a67D5b79d95795Aba299083c275"
ETH = "0xc02aaa39b223fe8d0a0e5c4f27ead9083c756cc2"
MCD_JOIN_ETH_A = "0x2f0b23f53734252bda2277357e97e1517d6b042a"
BAT = "0x0d8775f648430679a709e98d2b0cb6250d2887ef"
MCD_JOIN_BAT_A = "0x3d0b1912b66114d4096f48a8cee3a56c231772ca"
MCD_POT = "0x197e90f9fad81970ba7976f33cbd77088e5d7cf7"
CDP_MANAGER = "0x5ef30b9986345249bc32d8928b7ee64de9435e39"
MCD_JUG = "0x19c0976f590d67707e62397c87829d896dc0f1f1"
MCD_FLIP_ETH_A = "0xd8a04f5412223f513dc55f839574430f5ec15531"
MCD_FLIP_BAT_A = "0xaa745404d55f88c108a28c86abe7b5a1e7817c07"
MCD_SPOT = "0x65c79fcb50ca1594b025960e539ed7a9a6d434a3"
CHAI = "0x06AF07097C9Eeb7fD685c692751D5C66dB49c215"


def from_wad(value):
    return Decimal(value) / 10**18


def from_ray(value):
    return Decimal(value) / 10**27


def from_rad(value):
    return Decimal(value) / 10**45


def from_ilk(values):
    return {
        "Art": from_wad(values[0]),
        "rate": from_ray(values[1]),
        "spot": from_ray(values[2]),
        "line": from_rad(values[3]),
        "dust": from_rad(values[4]),
    }


def from_jug(values):
    return {
        "duty": from_ray(values[0]),
        "rho": values[1],
    }


def from_spot(values):
    return {
        "pip": values[0],
        "mat": from_ray(values[1]),
    }


def calc_fee(rate):
    return rate ** (60 * 60 * 24 * 365) * 100 - 100


def get_fee(base, jug):
    return calc_fee(base + jug["duty"])


multi = Multicall(
    [
        Call(MCD_VAT, ["Line()(uint256)"], [["Line", from_rad]]),
        Call(MCD_VAT, ["debt()(uint256)"], [["debt", from_rad]]),
        Call(MCD_VAT, ["vice()(uint256)"], [["vice", from_rad]]),
        Call(MCD_VAT, ["dai(address)(uint256)", MCD_VOW], [["vow_dai", from_rad]]),
        Call(MCD_VAT, ["sin(address)(uint256)", MCD_VOW], [["vow_sin", from_rad]]),
        Call(
            MCD_VAT,
            ["ilks(bytes32)((uint256,uint256,uint256,uint256,uint256))", b"ETH-A"],
            [["eth_ilk", from_ilk]],
        ),
        Call(
            MCD_VAT,
            ["ilks(bytes32)((uint256,uint256,uint256,uint256,uint256))", b"BAT-A"],
            [["bat_ilk", from_ilk]],
        ),
        Call(
            MCD_VAT,
            ["ilks(bytes32)((uint256,uint256,uint256,uint256,uint256))", b"SAI"],
            [["sai_ilk", from_ilk]],
        ),
        Call(MCD_VOW, ["hump()(uint256)"], [["surplus_buffer", from_rad]]),
        Call(MCD_VOW, ["sump()(uint256)"], [["debt_size", from_rad]]),
        Call(MCD_VOW, ["Ash()(uint256)"], [["ash", from_rad]]),
        Call(MCD_VOW, ["Sin()(uint256)"], [["sin", from_rad]]),
        Call(MCD_DAI, ["totalSupply()(uint256)"], [["dai_supply", from_wad]]),
        Call(
            MCD_DAI,
            ["balanceOf(address)(uint256)", UNISWAP_EXCHANGE],
            [["uniswap_dai", from_wad]],
        ),
        Call(SAI, ["totalSupply()(uint256)"], [["sai_supply", from_wad]]),
        Call(
            SAI,
            ["balanceOf(address)(uint256)", MCD_JOIN_SAI],
            [["sai_locked", from_wad]],
        ),
        Call(MCD_GOV, ["balanceOf(address)(uint256)", GEM_PIT], [["gem_pit", from_wad]]),
        Call(
            ETH,
            ["balanceOf(address)(uint256)", MCD_JOIN_ETH_A],
            [["eth_locked", from_wad]],
        ),
        Call(BAT, ["totalSupply()(uint256)"], [["bat_supply", from_wad]]),
        Call(
            BAT,
            ["balanceOf(address)(uint256)", MCD_JOIN_BAT_A],
            [["bat_locked", from_wad]],
        ),
        Call(MCD_POT, ["Pie()(uint256)"], [["savings_pie", from_wad]]),
        Call(MCD_POT, ["chi()(uint256)"], [["pie_chi", from_ray]]),
        Call(MCD_POT, ["rho()(uint256)"], [["pot_drip", None]]),
        Call(MCD_POT, ["dsr()(uint256)"], [["dsr", from_ray]]),
        Call(CDP_MANAGER, ["cdpi()(uint256)"], [["cdps", None]]),
        Call(MCD_JUG, ["base()(uint256)"], [["base", from_ray]]),
        Call(
            MCD_JUG,
            ["ilks(bytes32)((uint256,uint256))", b"ETH-A"],
            [["eth_jug", from_jug]],
        ),
        Call(
            MCD_JUG,
            ["ilks(bytes32)((uint256,uint256))", b"BAT-A"],
            [["bat_jug", from_jug]],
        ),
        Call(
            MCD_JUG,
            ["ilks(bytes32)((uint256,uint256))", b"SAI"],
            [["sai_jug", from_jug]],
        ),
        Call(MCD_FLIP_ETH_A, ["kicks()(uint256)"], [["eth_kicks", None]]),
        Call(MCD_FLIP_BAT_A, ["kicks()(uint256)"], [["bat_kicks", None]]),
        Call(
            MCD_SPOT,
            ["ilks(bytes32)((address,uint256))", b"ETH-A"],
            [["eth_mat", from_spot]],
        ),
        Call(
            MCD_SPOT,
            ["ilks(bytes32)((address,uint256))", b"BAT-A"],
            [["bat_mat", from_spot]],
        ),
        Call(CHAI, ["totalSupply()(uint256)"], [["chai_supply", from_wad]]),
        Call(MCD_GOV, ["totalSupply()(uint256)"], [["mkr_supply", from_wad]]),
    ]
)


def fetch_data():
    data = multi()
    data["eth_fee"] = get_fee(data["base"], data["eth_jug"])
    data["bat_fee"] = get_fee(data["base"], data["bat_jug"])
    data["sai_fee"] = get_fee(data["base"], data["sai_jug"])
    data["pot_fee"] = calc_fee(data["dsr"])
    data["savings_dai"] = data["savings_pie"] * data["pie_chi"]
    data["eth_price"] = data["eth_mat"]["mat"] * data["eth_ilk"]["spot"]
    data["bat_price"] = data["bat_mat"]["mat"] * data["bat_ilk"]["spot"]
    data["sys_locked"] = (
        data["eth_price"] * data["eth_locked"]
        + data["bat_price"] * data["bat_locked"]
        + data["sai_locked"]
    )
    data["sys_surplus"] = data["vow_dai"] - data["vow_sin"]
    data["sys_debt"] = data["vow_sin"] - data["sin"] - data["ash"]
    return data


def main():
    data = fetch_data()
    data = AttributeDict.recursive(data)
    print("The Fundamental Equation of Dai")
    print(
        f"{data.eth_ilk.Art * data.eth_ilk.rate:,.0f} + {data.bat_ilk.Art * data.bat_ilk.rate:,.0f} + {data.sai_ilk.Art:,.0f} + {data.vice:,.0f} = {data.debt:,.0f}"
    )
    print("(Dai from ETH + Dai from BAT + Dai from Sai + System Debt) = Total Dai")
    print()
    print(f"Total Dai: {data.debt:,.0f}")
    print(f"Total Sai: {data.sai_supply:,.0f}")
    print(f"Dai + Sai: {data.debt + data.sai_supply:,.0f}")
    print(f"Total Chai: {data.chai_supply:,.0f}")
    print()
    print(
        f"Dai from ETH: {data.eth_ilk.Art * data.eth_ilk.rate:,.0f} ({data.eth_ilk.Art * data.eth_ilk.rate / data.debt:.2%})"
    )
    print(
        f"Dai from BAT: {data.bat_ilk.Art * data.bat_ilk.rate:,.0f} ({data.bat_ilk.Art * data.bat_ilk.rate / data.debt:.2%})"
    )
    print(
        f"Dai from SAI: {data.sai_ilk.Art * data.sai_ilk.rate:,.0f} ({data.sai_ilk.Art * data.sai_ilk.rate / data.debt:.2%})"
    )
    print()
    print(f"ETH Locked: {data.eth_locked:,.0f}")  # eth_supply missing
    print(
        f"ETH Ceiling: {data.eth_ilk.line:,.0f} Dai ({data.eth_ilk.Art * data.eth_ilk.rate / data.eth_ilk.line:.2%} util.)"
    )
    print(f"ETH Stability Fee: {data.eth_fee:.2f}%")
    print()
    print(f"BAT Locked: {data.bat_locked:,.0f} ({data.bat_locked / data.bat_supply:.2%} supply)")
    print(
        f"BAT Ceiling: {data.bat_ilk.line:,.0f} Dai ({data.bat_ilk.Art * data.bat_ilk.rate / data.bat_ilk.line:.2%} util.)"
    )
    print(f"BAT Stability Fee: {data.bat_fee:.2f}%")
    print()
    print(f"Dai (ERC20) Supply: {data.dai_supply:,.0f} ({data.dai_supply / data.debt:.2%})")
    print(f"Dai in DSR: {data.savings_dai:,.0f} ({data.savings_dai / data.debt:.2%})")
    print(f"Pie in DSR: {data.savings_pie:,.0f}")
    print(f"Dai Savings Rate: {data.pot_fee:.2f}%")
    print()
    print(f"ETH Price: ${data.eth_price:,.2f}")
    print(f"BAT Price: ${data.bat_price:,.4f}")
    print(f"Collat. Ratio: {data.sys_locked / data.debt:,.2%}")
    print(f"Total Locked: ${data.sys_locked:,.0f}")
    print()
    print(f"System Surplus: {data.sys_surplus:,.0f} Dai")
    print(f"Surplus Buffer: {data.surplus_buffer:,.0f}")
    print()
    print(f"Debt available to heal: {data.sys_debt:,.0f} Dai")
    print(f"Debt Buffer: {data.debt_size:,.0f}")
    print()
    print(f"Vaults Opened: {data.cdps:,d}")
    print()
    print(f"ETH Vault Auctions: {data.eth_kicks:,d}")
    print(f"BAT Vault Auctions: {data.bat_kicks:,d}")
    print()
    print(f"MKR Supply: {data.mkr_supply:,.2f}")
    print(f"MKR in Burner: {data.gem_pit:,.2f}")
    print()
    print(f"Dai in Uniswap: {data.uniswap_dai:,.0f}")


if __name__ == "__main__":
    main()

```

File: examples/mcd_exporter.py
```py
import time
from functools import partial
from decimal import Decimal
from multicall import Call, Multicall
from prometheus_client import start_http_server, Gauge


MCD_VAT = "0x35d1b3f3d7966a1dfe207aa4514c12a259a0492b"
MCD_VOW = "0xa950524441892a31ebddf91d3ceefa04bf454466"
MCD_DAI = "0x6b175474e89094c44da98b954eedeac495271d0f"
UNISWAP_EXCHANGE = "0x2a1530C4C41db0B0b2bB646CB5Eb1A67b7158667"
SAI = "0x89d24a6b4ccb1b6faa2625fe562bdd9a23260359"
MCD_JOIN_SAI = "0xad37fd42185ba63009177058208dd1be4b136e6b"
MCD_GOV = "0x9f8f72aa9304c8b593d555f12ef6589cc3a579a2"
GEM_PIT = "0x69076e44a9C70a67D5b79d95795Aba299083c275"
ETH = "0xc02aaa39b223fe8d0a0e5c4f27ead9083c756cc2"
MCD_JOIN_ETH_A = "0x2f0b23f53734252bda2277357e97e1517d6b042a"
BAT = "0x0d8775f648430679a709e98d2b0cb6250d2887ef"
MCD_JOIN_BAT_A = "0x3d0b1912b66114d4096f48a8cee3a56c231772ca"
USDC = "0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48"
MCD_JOIN_USDC_A = "0xA191e578a6736167326d05c119CE0c90849E84B7"
MCD_POT = "0x197e90f9fad81970ba7976f33cbd77088e5d7cf7"
CDP_MANAGER = "0x5ef30b9986345249bc32d8928b7ee64de9435e39"
MCD_JUG = "0x19c0976f590d67707e62397c87829d896dc0f1f1"
MCD_FLIP_ETH_A = "0xd8a04f5412223f513dc55f839574430f5ec15531"
MCD_FLIP_BAT_A = "0xaa745404d55f88c108a28c86abe7b5a1e7817c07"
MCD_FLIP_USDC_A = "0xE6ed1d09a19Bd335f051d78D5d22dF3bfF2c28B1"
MCD_SPOT = "0x65c79fcb50ca1594b025960e539ed7a9a6d434a3"
CHAI = "0x06AF07097C9Eeb7fD685c692751D5C66dB49c215"
MCD_FLAP = "0xdfE0fb1bE2a52CDBf8FB962D5701d7fd0902db9f"
MCD_FLOP = "0x4D95A049d5B0b7d32058cd3F2163015747522e99"

mcd = Gauge("mcd", "multi-collateral dai", ["param"])

ilks = ["eth", "bat", "sai", "usdc"]
params = [
    "Line",
    "debt",
    "vice",
    "base",
    "cdps",
    "sys_locked",
    "sys_surplus",
    "sys_debt",
    "vow_dai",
    "vow_sin",
    "surplus_buffer",
    "debt_size",
    "ash",
    "sin",
    "dai_supply",
    "chai_supply",
    "mkr_supply",
    "uniswap_dai",
    "gem_pit",
    "savings_pie",
    "pie_chi",
    "pot_drip",
    "dsr",
    "pot_fee",
    "savings_dai",
    "flop_kicks",
    "flap_kicks",
]


def from_wad(value):
    return Decimal(value) / 10**18


def from_ray(value):
    return Decimal(value) / 10**27


def from_rad(value):
    return Decimal(value) / 10**45


def from_wei(value, decimals=18):
    return Decimal(value) / 10**decimals


from_wad = partial(from_wei, decimals=18)
from_ray = partial(from_wei, decimals=27)
from_rad = partial(from_wei, decimals=45)


def from_ilk(values):
    return {
        "Art": from_wad(values[0]),
        "rate": from_ray(values[1]),
        "spot": from_ray(values[2]),
        "line": from_rad(values[3]),
        "dust": from_rad(values[4]),
    }


def from_jug(values):
    return {
        "duty": from_ray(values[0]),
        "rho": values[1],
    }


def from_spot(values):
    return {
        "pip": values[0],
        "mat": from_ray(values[1]),
    }


def calc_fee(rate):
    return rate ** (60 * 60 * 24 * 365) * 100 - 100


def get_fee(base, jug):
    return calc_fee(base + jug["duty"])


multi = Multicall(
    [
        Call(MCD_VAT, ["Line()(uint256)"], [["Line", from_rad]]),
        Call(MCD_VAT, ["debt()(uint256)"], [["debt", from_rad]]),
        Call(MCD_VAT, ["vice()(uint256)"], [["vice", from_rad]]),
        Call(MCD_VAT, ["dai(address)(uint256)", MCD_VOW], [["vow_dai", from_rad]]),
        Call(MCD_VAT, ["sin(address)(uint256)", MCD_VOW], [["vow_sin", from_rad]]),
        Call(
            MCD_VAT,
            ["ilks(bytes32)((uint256,uint256,uint256,uint256,uint256))", b"ETH-A"],
            [["eth_ilk", from_ilk]],
        ),
        Call(
            MCD_VAT,
            ["ilks(bytes32)((uint256,uint256,uint256,uint256,uint256))", b"BAT-A"],
            [["bat_ilk", from_ilk]],
        ),
        Call(
            MCD_VAT,
            ["ilks(bytes32)((uint256,uint256,uint256,uint256,uint256))", b"SAI"],
            [["sai_ilk", from_ilk]],
        ),
        Call(
            MCD_VAT,
            ["ilks(bytes32)((uint256,uint256,uint256,uint256,uint256))", b"USDC-A"],
            [["usdc_ilk", from_ilk]],
        ),
        Call(MCD_VOW, ["hump()(uint256)"], [["surplus_buffer", from_rad]]),
        Call(MCD_VOW, ["sump()(uint256)"], [["debt_size", from_rad]]),
        Call(MCD_VOW, ["Ash()(uint256)"], [["ash", from_rad]]),
        Call(MCD_VOW, ["Sin()(uint256)"], [["sin", from_rad]]),
        Call(MCD_DAI, ["totalSupply()(uint256)"], [["dai_supply", from_wad]]),
        Call(
            MCD_DAI,
            ["balanceOf(address)(uint256)", UNISWAP_EXCHANGE],
            [["uniswap_dai", from_wad]],
        ),
        Call(SAI, ["totalSupply()(uint256)"], [["sai_supply", from_wad]]),
        Call(
            SAI,
            ["balanceOf(address)(uint256)", MCD_JOIN_SAI],
            [["sai_locked", from_wad]],
        ),
        Call(MCD_GOV, ["balanceOf(address)(uint256)", GEM_PIT], [["gem_pit", from_wad]]),
        Call(
            ETH,
            ["balanceOf(address)(uint256)", MCD_JOIN_ETH_A],
            [["eth_locked", from_wad]],
        ),
        Call(BAT, ["totalSupply()(uint256)"], [["bat_supply", from_wad]]),
        Call(
            BAT,
            ["balanceOf(address)(uint256)", MCD_JOIN_BAT_A],
            [["bat_locked", from_wad]],
        ),
        Call(
            USDC,
            ["totalSupply()(uint256)"],
            [["usdc_supply", partial(from_wei, decimals=6)]],
        ),
        Call(
            USDC,
            ["balanceOf(address)(uint256)", MCD_JOIN_USDC_A],
            [["usdc_locked", partial(from_wei, decimals=6)]],
        ),
        Call(MCD_POT, ["Pie()(uint256)"], [["savings_pie", from_wad]]),
        Call(MCD_POT, ["chi()(uint256)"], [["pie_chi", from_ray]]),
        Call(MCD_POT, ["rho()(uint256)"], [["pot_drip", None]]),
        Call(MCD_POT, ["dsr()(uint256)"], [["dsr", from_ray]]),
        Call(CDP_MANAGER, ["cdpi()(uint256)"], [["cdps", None]]),
        Call(MCD_JUG, ["base()(uint256)"], [["base", from_ray]]),
        Call(
            MCD_JUG,
            ["ilks(bytes32)((uint256,uint256))", b"ETH-A"],
            [["eth_jug", from_jug]],
        ),
        Call(
            MCD_JUG,
            ["ilks(bytes32)((uint256,uint256))", b"BAT-A"],
            [["bat_jug", from_jug]],
        ),
        Call(
            MCD_JUG,
            ["ilks(bytes32)((uint256,uint256))", b"SAI"],
            [["sai_jug", from_jug]],
        ),
        Call(
            MCD_JUG,
            ["ilks(bytes32)((uint256,uint256))", b"USDC-A"],
            [["usdc_jug", from_jug]],
        ),
        Call(MCD_FLIP_ETH_A, ["kicks()(uint256)"], [["eth_kicks", None]]),
        Call(MCD_FLIP_BAT_A, ["kicks()(uint256)"], [["bat_kicks", None]]),
        Call(MCD_FLIP_USDC_A, ["kicks()(uint256)"], [["usdc_kicks", None]]),
        Call(
            MCD_SPOT,
            ["ilks(bytes32)((address,uint256))", b"ETH-A"],
            [["eth_mat", from_spot]],
        ),
        Call(
            MCD_SPOT,
            ["ilks(bytes32)((address,uint256))", b"BAT-A"],
            [["bat_mat", from_spot]],
        ),
        Call(
            MCD_SPOT,
            ["ilks(bytes32)((address,uint256))", b"USDC-A"],
            [["usdc_mat", from_spot]],
        ),
        Call(CHAI, ["totalSupply()(uint256)"], [["chai_supply", from_wad]]),
        Call(MCD_GOV, ["totalSupply()(uint256)"], [["mkr_supply", from_wad]]),
        Call(MCD_FLOP, ["kicks()(uint256)"], [["flop_kicks", None]]),
        Call(MCD_FLAP, ["kicks()(uint256)"], [["flap_kicks", None]]),
    ]
)


def fetch_data():
    data = multi()
    data["eth_fee"] = get_fee(data["base"], data["eth_jug"])
    data["bat_fee"] = get_fee(data["base"], data["bat_jug"])
    data["sai_fee"] = get_fee(data["base"], data["sai_jug"])
    data["usdc_fee"] = get_fee(data["base"], data["usdc_jug"])
    data["pot_fee"] = calc_fee(data["dsr"])
    data["savings_dai"] = data["savings_pie"] * data["pie_chi"]
    data["eth_price"] = data["eth_mat"]["mat"] * data["eth_ilk"]["spot"]
    data["bat_price"] = data["bat_mat"]["mat"] * data["bat_ilk"]["spot"]
    data["usdc_price"] = data["usdc_mat"]["mat"] * data["usdc_ilk"]["spot"]
    data["sys_locked"] = (
        data["eth_price"] * data["eth_locked"]
        + data["bat_price"] * data["bat_locked"]
        + data["usdc_price"] * data["usdc_locked"]
        + data["sai_locked"]
    )
    data["sys_surplus"] = data["vow_dai"] - data["vow_sin"]
    data["sys_debt"] = data["vow_sin"] - data["sin"] - data["ash"]
    return data


def update():
    data = fetch_data()
    for param in params:
        mcd.labels(param).set(data[param])
    for ilk in ilks:
        for param in ["supply", "locked", "price", "kicks", "fee"]:
            key = f"{ilk}_{param}"
            if key not in data:
                continue
            mcd.labels(key).set(data[key])
        for param in ["Art", "rate", "spot", "line", "dust"]:
            mcd.labels(f"{ilk}_{param}").set(data[f"{ilk}_ilk"][param])
        for param in ["duty", "rho"]:
            mcd.labels(f"{ilk}_{param}").set(data[f"{ilk}_jug"][param])


def loop():
    start_http_server(8000)
    while True:
        update()
        time.sleep(15)


if __name__ == "__main__":
    loop()

```

File: multicall/__init__.py
```py
from multicall.signature import Signature
from multicall.call import Call
from multicall.multicall import Multicall

```

File: multicall/call.py
```py
from typing import Any, Callable, Iterable, List, Optional, Tuple, Union

import eth_retry
from cchecksum import to_checksum_address
from eth_typing import Address, ChecksumAddress, HexAddress
from eth_typing.abi import Decodable
from web3 import Web3

from multicall.constants import Network, w3
from multicall.exceptions import StateOverrideNotSupported
from multicall.loggers import setup_logger
from multicall.signature import Signature, _get_signature
from multicall.utils import (
    _get_semaphore,
    chain_id,
    get_async_w3,
    run_in_subprocess,
    state_override_supported,
)

logger = setup_logger(__name__)

AnyAddress = Union[str, Address, ChecksumAddress, HexAddress]


class Call:
    __slots__ = (
        "target",
        "returns",
        "block_id",
        "gas_limit",
        "state_override_code",
        "w3",
        "args",
        "function",
        "signature",
        "origin",
    )

    def __init__(
        self,
        target: AnyAddress,
        function: Union[
            str, Iterable[Union[str, Any]]
        ],  # 'funcName(dtype)(dtype)' or ['funcName(dtype)(dtype)', input0, input1, ...]
        returns: Optional[Iterable[Tuple[str, Callable]]] = None,
        block_id: Optional[int] = None,
        gas_limit: Optional[int] = None,
        state_override_code: Optional[str] = None,
        # This needs to be None in order to use process_pool_executor
        _w3: Web3 = None,
        origin: Optional[AnyAddress] = None,
    ) -> None:
        self.target = to_checksum_address(target)
        self.returns = returns
        self.block_id = block_id
        self.gas_limit = gas_limit
        self.state_override_code = state_override_code
        self.w3 = _w3
        self.origin = to_checksum_address(origin) if origin else None

        self.args: Optional[List[Any]]
        if isinstance(function, list):
            self.function, *self.args = function
        else:
            self.function = function
            self.args = None

        self.signature = _get_signature(self.function)

    def __repr__(self) -> str:
        return f"<Call {self.function} on {self.target[:8]}>"

    @property
    def data(self) -> bytes:
        return self.signature.encode_data(self.args)

    def decode_output(
        output: Decodable,
        signature: Signature,
        returns: Optional[Iterable[Tuple[str, Callable]]] = None,
        success: Optional[bool] = None,
    ) -> Any:

        if success is None:
            apply_handler = lambda handler, value: handler(value)
        else:
            apply_handler = lambda handler, value: handler(success, value)

        if success is None or success:
            try:
                decoded = signature.decode_data(output)
            except:
                success, decoded = False, [None] * (1 if not returns else len(returns))  # type: ignore
        else:
            decoded = [None] * (1 if not returns else len(returns))  # type: ignore

        logger.debug("returns: %s", returns)
        logger.debug("decoded: %s", decoded)

        if returns:
            return {
                name: apply_handler(handler, value) if handler else value
                for (name, handler), value in zip(returns, decoded)
            }
        else:
            return decoded if len(decoded) > 1 else decoded[0]

    @eth_retry.auto_retry
    def __call__(
        self,
        args: Optional[Any] = None,
        _w3: Optional[Web3] = None,
        *,
        block_id: Optional[int] = None,
    ) -> Any:
        _w3 = self.w3 or _w3 or w3
        args = prep_args(
            self.target,
            self.signature,
            args or self.args,
            block_id or self.block_id,
            self.origin,
            self.gas_limit,
            self.state_override_code,
        )
        return Call.decode_output(
            _w3.eth.call(*args),
            self.signature,
            self.returns,
        )

    def __await__(self) -> Any:
        return self.coroutine().__await__()

    @eth_retry.auto_retry
    async def coroutine(
        self,
        args: Optional[Any] = None,
        _w3: Optional[Web3] = None,
        *,
        block_id: Optional[int] = None,
    ) -> Any:
        _w3 = self.w3 or _w3 or w3

        if self.state_override_code and not state_override_supported(_w3):
            raise StateOverrideNotSupported(
                f"State override is not supported on {Network(chain_id(_w3)).__repr__()[1:-1]}."
            )

        async with _get_semaphore():
            output = await get_async_w3(_w3).eth.call(
                *await run_in_subprocess(
                    prep_args,
                    self.target,
                    self.signature,
                    args or self.args,
                    block_id or self.block_id,
                    self.origin,
                    self.gas_limit,
                    self.state_override_code,
                )
            )

        return await run_in_subprocess(Call.decode_output, output, self.signature, self.returns)


def prep_args(
    target: str, 
    signature: Signature, 
    args: Optional[Any], 
    block_id: Optional[int],
    origin: str,
    gas_limit: int, 
    state_override_code: str,
) -> List:

    calldata = signature.encode_data(args)

    args = [{"to": target, "data": calldata}, block_id]

    if origin:
        args[0]['from'] = origin

    if gas_limit:
        args[0]["gas"] = gas_limit

    if state_override_code:
        args.append({target: {"code": state_override_code}})

    return args

```

File: multicall/loggers.py
```py
import logging
import os


def setup_logger(name: str) -> logging.Logger:
    logger = logging.getLogger(name)
    if os.environ.get("MULTICALL_DEBUG", False):
        logger.addHandler(logging.StreamHandler())
        logger.setLevel(logging.DEBUG)
    return logger

```

File: multicall/exceptions.py
```py
class StateOverrideNotSupported(Exception):
    pass

```

File: multicall/constants.py
```py
import asyncio
import os
from enum import IntEnum
from typing import Dict

from aiohttp import ClientTimeout

# If brownie is installed and connected, we will use brownie's Web3
# Otherwise, we will use w3 from web3py.
try:
    from brownie import network, web3  # type: ignore

    if network.is_connected():
        w3 = web3
    else:
        from web3.auto import w3
except ImportError:
    from web3.auto import w3

GAS_LIMIT: int = int(os.environ.get("GAS_LIMIT", 50_000_000))

MULTICALL2_BYTECODE = "0x608060405234801561001057600080fd5b50600436106100b45760003560e01c806372425d9d1161007157806372425d9d1461013d57806386d516e814610145578063a8b0574e1461014d578063bce38bd714610162578063c3077fa914610182578063ee82ac5e14610195576100b4565b80630f28c97d146100b9578063252dba42146100d757806327e86d6e146100f8578063399542e91461010057806342cbb15c146101225780634d2301cc1461012a575b600080fd5b6100c16101a8565b6040516100ce919061083b565b60405180910390f35b6100ea6100e53660046106bb565b6101ac565b6040516100ce9291906108ba565b6100c1610340565b61011361010e3660046106f6565b610353565b6040516100ce93929190610922565b6100c161036b565b6100c161013836600461069a565b61036f565b6100c161037c565b6100c1610380565b610155610384565b6040516100ce9190610814565b6101756101703660046106f6565b610388565b6040516100ce9190610828565b6101136101903660046106bb565b610533565b6100c16101a3366004610748565b610550565b4290565b8051439060609067ffffffffffffffff8111156101d957634e487b7160e01b600052604160045260246000fd5b60405190808252806020026020018201604052801561020c57816020015b60608152602001906001900390816101f75790505b50905060005b835181101561033a5760008085838151811061023e57634e487b7160e01b600052603260045260246000fd5b6020026020010151600001516001600160a01b031686848151811061027357634e487b7160e01b600052603260045260246000fd5b60200260200101516020015160405161028c91906107f8565b6000604051808303816000865af19150503d80600081146102c9576040519150601f19603f3d011682016040523d82523d6000602084013e6102ce565b606091505b5091509150816102f95760405162461bcd60e51b81526004016102f090610885565b60405180910390fd5b8084848151811061031a57634e487b7160e01b600052603260045260246000fd5b602002602001018190525050508080610332906109c2565b915050610212565b50915091565b600061034d60014361097b565b40905090565b43804060606103628585610388565b90509250925092565b4390565b6001600160a01b03163190565b4490565b4590565b4190565b6060815167ffffffffffffffff8111156103b257634e487b7160e01b600052604160045260246000fd5b6040519080825280602002602001820160405280156103eb57816020015b6103d8610554565b8152602001906001900390816103d05790505b50905060005b825181101561052c5760008084838151811061041d57634e487b7160e01b600052603260045260246000fd5b6020026020010151600001516001600160a01b031685848151811061045257634e487b7160e01b600052603260045260246000fd5b60200260200101516020015160405161046b91906107f8565b6000604051808303816000865af19150503d80600081146104a8576040519150601f19603f3d011682016040523d82523d6000602084013e6104ad565b606091505b509150915085156104d557816104d55760405162461bcd60e51b81526004016102f090610844565b604051806040016040528083151581526020018281525084848151811061050c57634e487b7160e01b600052603260045260246000fd5b602002602001018190525050508080610524906109c2565b9150506103f1565b5092915050565b6000806060610543600185610353565b9196909550909350915050565b4090565b60408051808201909152600081526060602082015290565b80356001600160a01b038116811461058357600080fd5b919050565b600082601f830112610598578081fd5b8135602067ffffffffffffffff808311156105b5576105b56109f3565b6105c2828385020161094a565b83815282810190868401865b8681101561068c57813589016040601f198181848f030112156105ef578a8bfd5b6105f88261094a565b6106038a850161056c565b81528284013589811115610615578c8dfd5b8085019450508d603f850112610629578b8cfd5b898401358981111561063d5761063d6109f3565b61064d8b84601f8401160161094a565b92508083528e84828701011115610662578c8dfd5b808486018c85013782018a018c9052808a01919091528652505092850192908501906001016105ce565b509098975050505050505050565b6000602082840312156106ab578081fd5b6106b48261056c565b9392505050565b6000602082840312156106cc578081fd5b813567ffffffffffffffff8111156106e2578182fd5b6106ee84828501610588565b949350505050565b60008060408385031215610708578081fd5b82358015158114610717578182fd5b9150602083013567ffffffffffffffff811115610732578182fd5b61073e85828601610588565b9150509250929050565b600060208284031215610759578081fd5b5035919050565b60008282518085526020808601955080818302840101818601855b848110156107bf57858303601f19018952815180511515845284015160408585018190526107ab818601836107cc565b9a86019a945050509083019060010161077b565b5090979650505050505050565b600081518084526107e4816020860160208601610992565b601f01601f19169290920160200192915050565b6000825161080a818460208701610992565b9190910192915050565b6001600160a01b0391909116815260200190565b6000602082526106b46020830184610760565b90815260200190565b60208082526021908201527f4d756c746963616c6c32206167677265676174653a2063616c6c206661696c656040820152601960fa1b606082015260800190565b6020808252818101527f4d756c746963616c6c206167677265676174653a2063616c6c206661696c6564604082015260600190565b600060408201848352602060408185015281855180845260608601915060608382028701019350828701855b8281101561091457605f198887030184526109028683516107cc565b955092840192908401906001016108e6565b509398975050505050505050565b6000848252836020830152606060408301526109416060830184610760565b95945050505050565b604051601f8201601f1916810167ffffffffffffffff81118282101715610973576109736109f3565b604052919050565b60008282101561098d5761098d6109dd565b500390565b60005b838110156109ad578181015183820152602001610995565b838111156109bc576000848401525b50505050565b60006000198214156109d6576109d66109dd565b5060010190565b634e487b7160e01b600052601160045260246000fd5b634e487b7160e01b600052604160045260246000fdfea2646970667358221220c1152f751f29ece4d7bce5287ceafc8a153de9c2c633e3f21943a87d845bd83064736f6c63430008010033"
MULTICALL3_BYTECODE = "0x6080604052600436106100f35760003560e01c80634d2301cc1161008a578063a8b0574e11610059578063a8b0574e1461025a578063bce38bd714610275578063c3077fa914610288578063ee82ac5e1461029b57600080fd5b80634d2301cc146101ec57806372425d9d1461022157806382ad56cb1461023457806386d516e81461024757600080fd5b80633408e470116100c65780633408e47014610191578063399542e9146101a45780633e64a696146101c657806342cbb15c146101d957600080fd5b80630f28c97d146100f8578063174dea711461011a578063252dba421461013a57806327e86d6e1461015b575b600080fd5b34801561010457600080fd5b50425b6040519081526020015b60405180910390f35b61012d610128366004610a85565b6102ba565b6040516101119190610bbe565b61014d610148366004610a85565b6104ef565b604051610111929190610bd8565b34801561016757600080fd5b50437fffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff0140610107565b34801561019d57600080fd5b5046610107565b6101b76101b2366004610c60565b610690565b60405161011193929190610cba565b3480156101d257600080fd5b5048610107565b3480156101e557600080fd5b5043610107565b3480156101f857600080fd5b50610107610207366004610ce2565b73ffffffffffffffffffffffffffffffffffffffff163190565b34801561022d57600080fd5b5044610107565b61012d610242366004610a85565b6106ab565b34801561025357600080fd5b5045610107565b34801561026657600080fd5b50604051418152602001610111565b61012d610283366004610c60565b61085a565b6101b7610296366004610a85565b610a1a565b3480156102a757600080fd5b506101076102b6366004610d18565b4090565b60606000828067ffffffffffffffff8111156102d8576102d8610d31565b60405190808252806020026020018201604052801561031e57816020015b6040805180820190915260008152606060208201528152602001906001900390816102f65790505b5092503660005b8281101561047757600085828151811061034157610341610d60565b6020026020010151905087878381811061035d5761035d610d60565b905060200281019061036f9190610d8f565b6040810135958601959093506103886020850185610ce2565b73ffffffffffffffffffffffffffffffffffffffff16816103ac6060870187610dcd565b6040516103ba929190610e32565b60006040518083038185875af1925050503d80600081146103f7576040519150601f19603f3d011682016040523d82523d6000602084013e6103fc565b606091505b50602080850191909152901515808452908501351761046d577f08c379a000000000000000000000000000000000000000000000000000000000600052602060045260176024527f4d756c746963616c6c333a2063616c6c206661696c656400000000000000000060445260846000fd5b5050600101610325565b508234146104e6576040517f08c379a000000000000000000000000000000000000000000000000000000000815260206004820152601a60248201527f4d756c746963616c6c333a2076616c7565206d69736d6174636800000000000060448201526064015b60405180910390fd5b50505092915050565b436060828067ffffffffffffffff81111561050c5761050c610d31565b60405190808252806020026020018201604052801561053f57816020015b606081526020019060019003908161052a5790505b5091503660005b8281101561068657600087878381811061056257610562610d60565b90506020028101906105749190610e42565b92506105836020840184610ce2565b73ffffffffffffffffffffffffffffffffffffffff166105a66020850185610dcd565b6040516105b4929190610e32565b6000604051808303816000865af19150503d80600081146105f1576040519150601f19603f3d011682016040523d82523d6000602084013e6105f6565b606091505b5086848151811061060957610609610d60565b602090810291909101015290508061067d576040517f08c379a000000000000000000000000000000000000000000000000000000000815260206004820152601760248201527f4d756c746963616c6c333a2063616c6c206661696c656400000000000000000060448201526064016104dd565b50600101610546565b5050509250929050565b43804060606106a086868661085a565b905093509350939050565b6060818067ffffffffffffffff8111156106c7576106c7610d31565b60405190808252806020026020018201604052801561070d57816020015b6040805180820190915260008152606060208201528152602001906001900390816106e55790505b5091503660005b828110156104e657600084828151811061073057610730610d60565b6020026020010151905086868381811061074c5761074c610d60565b905060200281019061075e9190610e76565b925061076d6020840184610ce2565b73ffffffffffffffffffffffffffffffffffffffff166107906040850185610dcd565b60405161079e929190610e32565b6000604051808303816000865af19150503d80600081146107db576040519150601f19603f3d011682016040523d82523d6000602084013e6107e0565b606091505b506020808401919091529015158083529084013517610851577f08c379a000000000000000000000000000000000000000000000000000000000600052602060045260176024527f4d756c746963616c6c333a2063616c6c206661696c656400000000000000000060445260646000fd5b50600101610714565b6060818067ffffffffffffffff81111561087657610876610d31565b6040519080825280602002602001820160405280156108bc57816020015b6040805180820190915260008152606060208201528152602001906001900390816108945790505b5091503660005b82811015610a105760008482815181106108df576108df610d60565b602002602001015190508686838181106108fb576108fb610d60565b905060200281019061090d9190610e42565b925061091c6020840184610ce2565b73ffffffffffffffffffffffffffffffffffffffff1661093f6020850185610dcd565b60405161094d929190610e32565b6000604051808303816000865af19150503d806000811461098a576040519150601f19603f3d011682016040523d82523d6000602084013e61098f565b606091505b506020830152151581528715610a07578051610a07576040517f08c379a000000000000000000000000000000000000000000000000000000000815260206004820152601760248201527f4d756c746963616c6c333a2063616c6c206661696c656400000000000000000060448201526064016104dd565b506001016108c3565b5050509392505050565b6000806060610a2b60018686610690565b919790965090945092505050565b60008083601f840112610a4b57600080fd5b50813567ffffffffffffffff811115610a6357600080fd5b6020830191508360208260051b8501011115610a7e57600080fd5b9250929050565b60008060208385031215610a9857600080fd5b823567ffffffffffffffff811115610aaf57600080fd5b610abb85828601610a39565b90969095509350505050565b6000815180845260005b81811015610aed57602081850181015186830182015201610ad1565b81811115610aff576000602083870101525b50601f017fffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffe0169290920160200192915050565b600082825180855260208086019550808260051b84010181860160005b84811015610bb1578583037fffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffe001895281518051151584528401516040858501819052610b9d81860183610ac7565b9a86019a9450505090830190600101610b4f565b5090979650505050505050565b602081526000610bd16020830184610b32565b9392505050565b600060408201848352602060408185015281855180845260608601915060608160051b870101935082870160005b82811015610c52577fffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffa0888703018452610c40868351610ac7565b95509284019290840190600101610c06565b509398975050505050505050565b600080600060408486031215610c7557600080fd5b83358015158114610c8557600080fd5b9250602084013567ffffffffffffffff811115610ca157600080fd5b610cad86828701610a39565b9497909650939450505050565b838152826020820152606060408201526000610cd96060830184610b32565b95945050505050565b600060208284031215610cf457600080fd5b813573ffffffffffffffffffffffffffffffffffffffff81168114610bd157600080fd5b600060208284031215610d2a57600080fd5b5035919050565b7f4e487b7100000000000000000000000000000000000000000000000000000000600052604160045260246000fd5b7f4e487b7100000000000000000000000000000000000000000000000000000000600052603260045260246000fd5b600082357fffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff81833603018112610dc357600080fd5b9190910192915050565b60008083357fffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffe1843603018112610e0257600080fd5b83018035915067ffffffffffffffff821115610e1d57600080fd5b602001915036819003821315610a7e57600080fd5b8183823760009101908152919050565b600082357fffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffc1833603018112610dc357600080fd5b600082357fffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffa1833603018112610dc357600080fdfea2646970667358221220bb2b5c71a328032f97c676ae39a1ec2148d3e5d6f73d95e9b17910152d61f16264736f6c634300080c0033"


# ordered by chain id for easy extension
class Network(IntEnum):
    Mainnet = 1
    Ropsten = 3
    Rinkeby = 4
    Gorli = 5
    Optimism = 10
    CostonTestnet = 16
    ThundercoreTestnet = 18
    SongbirdCanaryNetwork = 19
    Cronos = 25
    RSK = 30
    RSKTestnet = 31
    Kovan = 42
    Bsc = 56
    OKC = 66
    OptimismKovan = 69
    BscTestnet = 97
    Gnosis = 100
    Velas = 106
    Thundercore = 108
    Coston2Testnet = 114
    Fuse = 122
    Heco = 128
    Polygon = 137
    Fantom = 250
    Boba = 288
    KCC = 321
    ZkSync = 324
    OptimismGorli = 420
    Astar = 592
    Metis = 1088
    Moonbeam = 1284
    Moonriver = 1285
    MoonbaseAlphaTestnet = 1287
    Milkomeda = 2001
    Kava = 2222
    FantomTestnet = 4002
    Canto = 7700
    Klaytn = 8217
    Base = 8453
    EvmosTestnet = 9000
    Evmos = 9001
    Holesky = 17000
    Arbitrum = 42161
    Celo = 42220
    Oasis = 42262
    AvalancheFuji = 43113
    Avax = 43114
    GodwokenTestnet = 71401
    Godwoken = 71402
    Mumbai = 80001
    ArbitrumRinkeby = 421611
    ArbitrumGorli = 421613
    Sepolia = 11155111
    Aurora = 1313161554
    Harmony = 1666600000
    PulseChain = 369
    PulseChainTestnet = 943
    Sei = 1329


MULTICALL_ADDRESSES: Dict[int, str] = {
    Network.Mainnet: "0xeefBa1e63905eF1D7ACbA5a8513c70307C1cE441",
    Network.Kovan: "0x2cc8688C5f75E365aaEEb4ea8D6a480405A48D2A",
    Network.Rinkeby: "0x42Ad527de7d4e9d9d011aC45B31D8551f8Fe9821",
    Network.Gorli: "0x77dCa2C955b15e9dE4dbBCf1246B4B85b651e50e",
    Network.Gnosis: "0xb5b692a88BDFc81ca69dcB1d924f59f0413A602a",
    Network.Polygon: "0x95028E5B8a734bb7E2071F96De89BABe75be9C8E",
    Network.Bsc: "0x1Ee38d535d541c55C9dae27B12edf090C608E6Fb",
    Network.Fantom: "0xb828C456600857abd4ed6C32FAcc607bD0464F4F",
    Network.Heco: "0xc9a9F768ebD123A00B52e7A0E590df2e9E998707",
    Network.Harmony: "0xFE4980f62D708c2A84D3929859Ea226340759320",
    Network.Cronos: "0x5e954f5972EC6BFc7dECd75779F10d848230345F",
    Network.Optimism: "0x187C0F98FEF80E87880Db50241D40551eDd027Bf",
    Network.OptimismKovan: "0x2DC0E2aa608532Da689e89e237dF582B783E552C",
    Network.Kava: "0x7ED7bBd8C454a1B0D9EdD939c45a81A03c20131C",
}

MULTICALL2_ADDRESSES: Dict[int, str] = {
    Network.Mainnet: "0x5ba1e12693dc8f9c48aad8770482f4739beed696",
    Network.Kovan: "0x5ba1e12693dc8f9c48aad8770482f4739beed696",
    Network.Rinkeby: "0x5ba1e12693dc8f9c48aad8770482f4739beed696",
    Network.Gorli: "0x5ba1e12693dc8f9c48aad8770482f4739beed696",
    Network.Gnosis: "0x9903f30c1469d8A2f415D4E8184C93BD26992573",
    Network.Polygon: "0xc8E51042792d7405184DfCa245F2d27B94D013b6",
    Network.Bsc: "0xfF6FD90A470Aaa0c1B8A54681746b07AcdFedc9B",
    Network.Fantom: "0xBAD2B082e2212DE4B065F636CA4e5e0717623d18",
    Network.Moonriver: "0xB44a9B6905aF7c801311e8F4E76932ee959c663C",
    Network.Arbitrum: "0x842eC2c7D803033Edf55E478F461FC547Bc54EB2",
    Network.Avax: "0xdf2122931FEb939FB8Cf4e67Ea752D1125e18858",
    Network.Heco: "0xd1F3BE686D64e1EA33fcF64980b65847aA43D79C",
    Network.Aurora: "0xe0e3887b158F7F9c80c835a61ED809389BC08d1b",
    Network.Cronos: "0x5e954f5972EC6BFc7dECd75779F10d848230345F",
    Network.Optimism: "0x2DC0E2aa608532Da689e89e237dF582B783E552C",
    Network.OptimismKovan: "0x2DC0E2aa608532Da689e89e237dF582B783E552C",
    Network.Kava: "0x45be772faE4a9F31401dfF4738E5DC7DD439aC0b",
}

# based on https://github.com/mds1/multicall#readme
MULTICALL3_ADDRESSES: Dict[int, str] = {
    Network.Mainnet: "0xcA11bde05977b3631167028862bE2a173976CA11",
    Network.Ropsten: "0xcA11bde05977b3631167028862bE2a173976CA11",
    Network.Rinkeby: "0xcA11bde05977b3631167028862bE2a173976CA11",
    Network.Gorli: "0xcA11bde05977b3631167028862bE2a173976CA11",
    Network.Optimism: "0xcA11bde05977b3631167028862bE2a173976CA11",
    Network.CostonTestnet: "0xcA11bde05977b3631167028862bE2a173976CA11",
    Network.ThundercoreTestnet: "0xcA11bde05977b3631167028862bE2a173976CA11",
    Network.SongbirdCanaryNetwork: "0xcA11bde05977b3631167028862bE2a173976CA11",
    Network.Cronos: "0xcA11bde05977b3631167028862bE2a173976CA11",
    Network.RSK: "0xcA11bde05977b3631167028862bE2a173976CA11",
    Network.RSKTestnet: "0xcA11bde05977b3631167028862bE2a173976CA11",
    Network.Kovan: "0xcA11bde05977b3631167028862bE2a173976CA11",
    Network.Bsc: "0xcA11bde05977b3631167028862bE2a173976CA11",
    Network.OKC: "0xcA11bde05977b3631167028862bE2a173976CA11",
    Network.OptimismKovan: "0xcA11bde05977b3631167028862bE2a173976CA11",
    Network.BscTestnet: "0xcA11bde05977b3631167028862bE2a173976CA11",
    Network.Gnosis: "0xcA11bde05977b3631167028862bE2a173976CA11",
    Network.Velas: "0xcA11bde05977b3631167028862bE2a173976CA11",
    Network.Thundercore: "0xcA11bde05977b3631167028862bE2a173976CA11",
    Network.Coston2Testnet: "0xcA11bde05977b3631167028862bE2a173976CA11",
    Network.Fuse: "0xcA11bde05977b3631167028862bE2a173976CA11",
    Network.Heco: "0xcA11bde05977b3631167028862bE2a173976CA11",
    Network.Polygon: "0xcA11bde05977b3631167028862bE2a173976CA11",
    Network.Fantom: "0xcA11bde05977b3631167028862bE2a173976CA11",
    Network.Boba: "0xcA11bde05977b3631167028862bE2a173976CA11",
    Network.KCC: "0xcA11bde05977b3631167028862bE2a173976CA11",
    Network.ZkSync: "0x47898B2C52C957663aE9AB46922dCec150a2272c",
    Network.OptimismGorli: "0xcA11bde05977b3631167028862bE2a173976CA11",
    Network.Astar: "0xcA11bde05977b3631167028862bE2a173976CA11",
    Network.Metis: "0xcA11bde05977b3631167028862bE2a173976CA11",
    Network.Moonbeam: "0xcA11bde05977b3631167028862bE2a173976CA11",
    Network.Moonriver: "0xcA11bde05977b3631167028862bE2a173976CA11",
    Network.MoonbaseAlphaTestnet: "0xcA11bde05977b3631167028862bE2a173976CA11",
    Network.Milkomeda: "0xcA11bde05977b3631167028862bE2a173976CA11",
    Network.FantomTestnet: "0xcA11bde05977b3631167028862bE2a173976CA11",
    Network.Canto: "0xcA11bde05977b3631167028862bE2a173976CA11",
    Network.Klaytn: "0xcA11bde05977b3631167028862bE2a173976CA11",
    Network.EvmosTestnet: "0xcA11bde05977b3631167028862bE2a173976CA11",
    Network.Evmos: "0xcA11bde05977b3631167028862bE2a173976CA11",
    Network.Arbitrum: "0xcA11bde05977b3631167028862bE2a173976CA11",
    Network.Celo: "0xcA11bde05977b3631167028862bE2a173976CA11",
    Network.Oasis: "0xcA11bde05977b3631167028862bE2a173976CA11",
    Network.AvalancheFuji: "0xcA11bde05977b3631167028862bE2a173976CA11",
    Network.Avax: "0xcA11bde05977b3631167028862bE2a173976CA11",
    Network.GodwokenTestnet: "0xcA11bde05977b3631167028862bE2a173976CA11",
    Network.Godwoken: "0xcA11bde05977b3631167028862bE2a173976CA11",
    Network.Mumbai: "0xcA11bde05977b3631167028862bE2a173976CA11",
    Network.ArbitrumRinkeby: "0xcA11bde05977b3631167028862bE2a173976CA11",
    Network.ArbitrumGorli: "0xcA11bde05977b3631167028862bE2a173976CA11",
    Network.Sepolia: "0xcA11bde05977b3631167028862bE2a173976CA11",
    Network.Aurora: "0xcA11bde05977b3631167028862bE2a173976CA11",
    Network.Harmony: "0xcA11bde05977b3631167028862bE2a173976CA11",
    Network.PulseChain: "0xcA11bde05977b3631167028862bE2a173976CA11",
    Network.PulseChainTestnet: "0xcA11bde05977b3631167028862bE2a173976CA11",
    Network.Base: "0xcA11bde05977b3631167028862bE2a173976CA11",
    Network.Holesky: "0xcA11bde05977b3631167028862bE2a173976CA11",
    Network.Sei: "0xcA11bde05977b3631167028862bE2a173976CA11",
}

# With default AsyncBaseProvider settings, some dense calls will fail
#   due to aiohttp.TimeoutError where they would otherwise succeed.
AIOHTTP_TIMEOUT = ClientTimeout(int(os.environ.get("AIOHTTP_TIMEOUT", 30)))

# Parallelism
user_choice = max(1, int(os.environ.get("MULTICALL_PROCESSES", 1)))
parallelism_capacity = max(1, os.cpu_count() - 1)
NUM_PROCESSES = min(user_choice, parallelism_capacity)

NO_STATE_OVERRIDE = [
    Network.Gnosis,
    Network.Harmony,
    Network.Moonbeam,
    Network.Moonriver,
    Network.Kovan,
    Network.Fuse,
    Network.ZkSync,
]

# NOTE: If we run too many async calls at once, we'll have memory issues.
#       Feel free to increase this with the "MULTICALL_CALL_SEMAPHORE" env var if you know what you're doing.
ASYNC_SEMAPHORE = int(os.environ.get("MULTICALL_CALL_SEMAPHORE", 1000))

```

File: multicall/utils.py
```py
import asyncio
from concurrent.futures import ProcessPoolExecutor
from functools import lru_cache
from typing import Any, Awaitable, Callable, Coroutine, Dict, Iterable

import eth_retry
from aiohttp import ClientTimeout
from web3 import AsyncHTTPProvider, Web3
from web3.eth import AsyncEth
from web3.providers.async_base import AsyncBaseProvider

from multicall.constants import (
    AIOHTTP_TIMEOUT,
    ASYNC_SEMAPHORE,
    NO_STATE_OVERRIDE,
    NUM_PROCESSES,
)

try:
    from web3 import AsyncWeb3
except ImportError:
    AsyncWeb3 = None

try:
    from web3 import WebsocketProviderV2
except ImportError:
    WebsocketProviderV2 = None


chainids: Dict[Web3, int] = {}


@eth_retry.auto_retry
def chain_id(w3: Web3) -> int:
    """
    Returns chain id for an instance of Web3. Helps save repeat calls to node.
    """
    try:
        return chainids[w3]
    except KeyError:
        chainids[w3] = w3.eth.chain_id
        return chainids[w3]


async_w3s: Dict[Web3, Web3] = {}
process_pool_executor = ProcessPoolExecutor(NUM_PROCESSES)


def get_endpoint(w3: Web3) -> str:
    provider = w3.provider
    if isinstance(provider, str):
        return provider
    if hasattr(provider, "_active_provider"):
        provider = provider._get_active_provider(False)
    return provider.endpoint_uri


def get_async_w3(w3: Web3) -> Web3:
    if w3 in async_w3s:
        return async_w3s[w3]
    if w3.eth.is_async and isinstance(w3.provider, AsyncBaseProvider):
        timeout = w3.provider._request_kwargs["timeout"]
        if isinstance(timeout, ClientTimeout):
            timeout = timeout.total

        if timeout < AIOHTTP_TIMEOUT.total:
            w3.provider._request_kwargs["timeout"] = AIOHTTP_TIMEOUT

        async_w3s[w3] = w3
        return w3

    endpoint = get_endpoint(w3)
    request_kwargs = {"timeout": AIOHTTP_TIMEOUT}
    if WebsocketProviderV2 and endpoint.startswith(("wss:", "ws:")):
        provider = WebsocketProviderV2(endpoint, request_kwargs)
    else:
        provider = AsyncHTTPProvider(endpoint, request_kwargs)

    # In older web3 versions, AsyncHTTPProvider objects come
    # with incompatible synchronous middlewares by default.
    middlewares = []
    if AsyncWeb3:
        async_w3 = AsyncWeb3(provider=provider, middlewares=middlewares)
    else:
        async_w3 = Web3(provider=provider, middlewares=middlewares)
        async_w3.eth = AsyncEth(async_w3)

    async_w3s[w3] = async_w3
    return async_w3


def get_event_loop() -> asyncio.BaseEventLoop:
    try:
        loop = asyncio.get_event_loop()
    except RuntimeError as e:  # Necessary for use with multi-threaded applications.
        if not str(e).startswith("There is no current event loop in thread"):
            raise e
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
    return loop


def await_awaitable(awaitable: Awaitable) -> Any:
    return get_event_loop().run_until_complete(awaitable)


async def run_in_subprocess(callable: Callable, *args: Any, **kwargs) -> Any:
    if NUM_PROCESSES == 1:
        return callable(*args, **kwargs)
    return await asyncio.get_event_loop().run_in_executor(
        process_pool_executor, callable, *args, **kwargs
    )


def raise_if_exception(obj: Any) -> None:
    if isinstance(obj, Exception):
        raise obj


def raise_if_exception_in(iterable: Iterable[Any]) -> None:
    for obj in iterable:
        raise_if_exception(obj)


async def gather(coroutines: Iterable[Coroutine]) -> None:
    results = await asyncio.gather(*coroutines, return_exceptions=True)
    raise_if_exception_in(results)
    return results


def state_override_supported(w3: Web3) -> bool:
    if chain_id(w3) in NO_STATE_OVERRIDE:
        return False
    return True


def _get_semaphore() -> asyncio.Semaphore:
    "Returns a `Semaphore` attached to the current event loop"
    return __get_semaphore(asyncio.get_event_loop())


@lru_cache(maxsize=1)
def __get_semaphore(loop: asyncio.BaseEventLoop) -> asyncio.Semaphore:
    'This prevents an "attached to a different loop" edge case if the event loop is changed during your script run'
    return asyncio.Semaphore(ASYNC_SEMAPHORE)

```

File: multicall/multicall.py
```py
import asyncio
from time import time
from typing import Any, Dict, List, Optional, Tuple, Union

import aiohttp
import requests
from eth_utils import to_checksum_address

from multicall.call import AnyAddress
from web3 import Web3

from multicall import Call
from multicall.constants import (
    GAS_LIMIT,
    MULTICALL2_ADDRESSES,
    MULTICALL3_ADDRESSES,
    MULTICALL3_BYTECODE,
    w3,
)
from multicall.loggers import setup_logger
from multicall.utils import (
    _get_semaphore,
    await_awaitable,
    chain_id,
    gather,
    run_in_subprocess,
    state_override_supported,
)

logger = setup_logger(__name__)

CallResponse = Tuple[Union[None, bool], bytes]


def get_args(calls: List[Call], require_success: bool = True) -> List[Union[bool, List[List[Any]]]]:
    if require_success is True:
        return [[[call.target, call.data] for call in calls]]
    return [require_success, [[call.target, call.data] for call in calls]]


def unpack_aggregate_outputs(outputs: Any) -> Tuple[CallResponse, ...]:
    return tuple((None, output) for output in outputs)


def unpack_batch_results(batch_results: List[List[CallResponse]]) -> List[CallResponse]:
    return [result for batch in batch_results for result in batch]


class Multicall:
    __slots__ = (
        "calls",
        "block_id",
        "require_success",
        "gas_limit",
        "w3",
        "chainid",
        "multicall_sig",
        "multicall_address",
        "origin"
    )

    def __init__(
        self,
        calls: List[Call],
        block_id: Optional[int] = None,
        require_success: bool = True,
        gas_limit: int = GAS_LIMIT,
        _w3: Web3 = w3,
        origin: Optional[AnyAddress] = None,
    ) -> None:
        self.calls = calls
        self.block_id = block_id
        self.require_success = require_success
        self.gas_limit = gas_limit
        self.w3 = _w3
        self.origin = to_checksum_address(origin) if origin else None
        self.chainid = chain_id(self.w3)
        if require_success is True:
            multicall_map = (
                MULTICALL3_ADDRESSES
                if self.chainid in MULTICALL3_ADDRESSES
                else MULTICALL2_ADDRESSES
            )
            self.multicall_sig = "aggregate((address,bytes)[])(uint256,bytes[])"
        else:
            multicall_map = (
                MULTICALL3_ADDRESSES
                if self.chainid in MULTICALL3_ADDRESSES
                else MULTICALL2_ADDRESSES
            )
            self.multicall_sig = (
                "tryBlockAndAggregate(bool,(address,bytes)[])(uint256,uint256,(bool,bytes)[])"
            )
        self.multicall_address = multicall_map[self.chainid]

    def __call__(self) -> Dict[str, Any]:
        start = time()
        response = await_awaitable(self)
        logger.debug("Multicall took %ss", time() - start)
        return response

    def __await__(self) -> Dict[str, Any]:
        return self.coroutine().__await__()

    async def coroutine(self) -> Dict[str, Any]:
        batches = await gather(
            [
                self.fetch_outputs(batch, id=str(i))
                for i, batch in enumerate(batcher.batch_calls(self.calls, batcher.step))
            ]
        )
        outputs = await run_in_subprocess(unpack_batch_results, batches)

        return {name: result for output in outputs for name, result in output.items()}

    async def fetch_outputs(
        self, calls: List[Call], ConnErr_retries: int = 0, id: str = ""
    ) -> List[CallResponse]:
        logger.debug("coroutine %s started", id)

        if calls is None:
            calls = self.calls

        async with _get_semaphore():
            try:
                args = await run_in_subprocess(get_args, calls, self.require_success)
                if self.require_success is True:
                    self.block_id, outputs = await self.aggregate.coroutine(args)
                    outputs = await run_in_subprocess(unpack_aggregate_outputs, outputs)
                else:
                    self.block_id, _, outputs = await self.aggregate.coroutine(args)
                outputs = await gather(
                    [
                        run_in_subprocess(
                            Call.decode_output, output, call.signature, call.returns, success
                        )
                        for call, (success, output) in zip(calls, outputs)
                    ]
                )
                logger.debug("coroutine %s finished", id)
                return outputs
            except Exception as e:
                _raise_or_proceed(e, len(calls), ConnErr_retries=ConnErr_retries)

        # Failed, we need to rebatch the calls and try again.
        batch_results = await gather(
            [
                self.fetch_outputs(chunk, ConnErr_retries + 1, f"{id}_{i}")
                for i, chunk in enumerate(await batcher.rebatch(calls))
            ]
        )

        return_val = await run_in_subprocess(unpack_batch_results, batch_results)
        logger.debug("coroutine %s finished", id)
        return return_val

    @property
    def aggregate(self) -> Call:
        if state_override_supported(self.w3):
            return Call(
                self.multicall_address,
                self.multicall_sig,
                returns=None,
                _w3=self.w3,
                block_id=self.block_id,
                origin=self.origin,
                gas_limit=self.gas_limit,
                state_override_code=MULTICALL3_BYTECODE,
            )

        # If state override is not supported, we simply skip it.
        # This will mean you're unable to access full historical data on chains without state override support.
        return Call(
            self.multicall_address,
            self.multicall_sig,
            returns=None,
            _w3=self.w3,
            origin=self.origin,
            block_id=self.block_id,
            gas_limit=self.gas_limit,
        )


class NotSoBrightBatcher:
    """
    This class helps with processing a large volume of large multicalls.
    It's not so bright, but should quickly bring the batch size down to something reasonable for your node.
    """

    __slots__ = ("step",)

    def __init__(self) -> None:
        self.step = 10000

    def batch_calls(self, calls: List[Call], step: int) -> List[List[Call]]:
        """
        Batch calls into chunks of size `self.step`.
        """
        batches = []
        start = 0
        done = len(calls) - 1
        while True:
            end = start + step
            batches.append(calls[start:end])
            if end >= done:
                return batches
            start = end

    def split_calls(self, calls: List[Call], unused: None = None) -> Tuple[List[Call], List[Call]]:
        """
        Split calls into 2 batches in case request is too large.
        We do this to help us find optimal `self.step` value.
        """
        center = len(calls) // 2
        chunk_1 = calls[:center]
        chunk_2 = calls[center:]
        return chunk_1, chunk_2

    async def rebatch(self, calls):
        # If a separate coroutine changed `step` after calls were last batched, we will use the new `step` for rebatching.
        if self.step <= len(calls) // 2:
            return await run_in_subprocess(self.batch_calls, calls, self.step)

        # Otherwise we will split calls in half.
        if self.step >= len(calls):
            new_step = round(len(calls) * 0.99) if len(calls) >= 100 else len(calls) - 1
            logger.warning(
                f"Multicall batch size reduced from {self.step} to {new_step}. The failed batch had {len(calls)} calls."
            )
            self.step = new_step
        return await run_in_subprocess(self.split_calls, calls, self.step)


batcher = NotSoBrightBatcher()


def _raise_or_proceed(e: Exception, ct_calls: int, ConnErr_retries: int) -> None:
    """Depending on the exception, either raises or ignores and allows `batcher` to rebatch."""
    if isinstance(e, aiohttp.ClientOSError):
        if "broken pipe" not in str(e).lower():
            raise e
        logger.warning(e)
    elif isinstance(e, aiohttp.ClientResponseError):
        strings = ["request entity too large", "connection reset by peer"]
        if not any([string in str(e).lower() for string in strings]):
            raise e
        logger.warning(e)
    elif isinstance(e, requests.ConnectionError):
        if (
            "('Connection aborted.', ConnectionResetError(104, 'Connection reset by peer'))"
            not in str(e)
            or ConnErr_retries > 5
        ):
            raise e
    elif isinstance(e, requests.HTTPError):
        strings = (
            "request entity too large",
            "payload too large",
            "time-out",
            "520 server error",
        )
        if not any([string in str(e).lower() for string in strings]):
            raise e
        logger.warning(e)
    elif isinstance(e, asyncio.TimeoutError):
        pass
    elif isinstance(e, ValueError):
        if "out of gas" not in str(e).lower():
            raise e
        if ct_calls == 1:
            raise e
        logger.warning(e)
    else:
        raise e

```

File: multicall/signature.py
```py
from functools import lru_cache
from typing import Any, List, Optional, Tuple

# For eth_abi versions < 2.2.0, `decode` and `encode` have not yet been added.
# As we require web3 >=5.27, we require eth_abi compatability with eth_abi v2.0.0b6 and greater.
try:
    from eth_abi import decode, encode
except ImportError:
    from eth_abi import encode_abi as encode, decode_abi as decode

from eth_typing.abi import Decodable, TypeStr
from eth_utils import function_signature_to_4byte_selector


get_4byte_selector = lru_cache(maxsize=None)(function_signature_to_4byte_selector)


def parse_signature(signature: str) -> Tuple[str, List[TypeStr], List[TypeStr]]:
    """
    Breaks 'func(address)(uint256)' into ['func', ['address'], ['uint256']]
    """
    parts: List[str] = []
    stack: List[str] = []
    start: int = 0
    for end, character in enumerate(signature):
        if character == "(":
            stack.append(character)
            if not parts:
                parts.append(signature[start:end])
                start = end
        if character == ")":
            stack.pop()
            if not stack:  # we are only interested in outermost groups
                parts.append(signature[start : end + 1])
                start = end + 1
    function = "".join(parts[:2])
    input_types = parse_typestring(parts[1])
    output_types = parse_typestring(parts[2])
    return function, input_types, output_types


def parse_typestring(typestring: str) -> Optional[List[TypeStr]]:
    if typestring == "()":
        return []
    parts = []
    part = ""
    inside_tuples = 0
    for character in typestring[1:-1]:
        if character == "(":
            inside_tuples += 1
        elif character == ")":
            inside_tuples -= 1
        elif character == "," and inside_tuples == 0:
            parts.append(part)
            part = ""
            continue
        part += character
    parts.append(part)
    return parts


@lru_cache(maxsize=None)
def _get_signature(signature: str) -> "Signature":
    return Signature(signature)


class Signature:
    __slots__ = "signature", "function", "input_types", "output_types"

    def __init__(self, signature: str) -> None:
        self.signature = signature
        self.function, self.input_types, self.output_types = parse_signature(signature)

    @property
    def fourbyte(self) -> bytes:
        return get_4byte_selector(self.function)

    def encode_data(self, args: Optional[Any] = None) -> bytes:
        return self.fourbyte + encode(self.input_types, args) if args else self.fourbyte

    def decode_data(self, output: Decodable) -> Any:
        return decode(self.output_types, output)

```

File: tests/conftest.py
```py
import os
import sys
from brownie import network

if not network.is_connected():
    network.connect(os.environ["PYTEST_NETWORK"])
sys.path.insert(0, os.path.abspath("."))

```

File: tests/test_call.py
```py
import pytest

from brownie import web3
from joblib import Parallel, delayed
from multicall import Call
from multicall.utils import await_awaitable

CHAI = "0x06AF07097C9Eeb7fD685c692751D5C66dB49c215"


def from_wei(value):
    return value / 1e18


def test_call():
    call = Call(CHAI, "name()(string)", [["name", None]])
    assert call() == {"name": "Chai"}


def test_call_with_args():
    call = Call(CHAI, "balanceOf(address)(uint256)", [["balance", from_wei]])
    assert isinstance(call([CHAI])["balance"], float)


def test_call_with_predefined_args():
    call = Call(CHAI, ["balanceOf(address)(uint256)", CHAI], [["balance", from_wei]])
    assert isinstance(call()["balance"], float)

def test_call_with_origin():
    # Simulate the top holder sending 1 wei to the contract
    call = Call(CHAI, ['transfer(address,uint256)(bool)', CHAI, 1], [['success', None]], origin='0xc9824224fC15c9c272c9c2ad730AEdEB85DCdA6f')
    assert call()['success'] == True

def test_call_async():
    call = Call(CHAI, "name()(string)", [["name", None]])
    assert await_awaitable(call) == {"name": "Chai"}


def test_call_with_args_async():
    call = Call(CHAI, "balanceOf(address)(uint256)", [["balance", from_wei]])
    assert isinstance(await_awaitable(call.coroutine([CHAI]))["balance"], float)


def test_call_with_predefined_args_async():
    call = Call(CHAI, ["balanceOf(address)(uint256)", CHAI], [["balance", from_wei]])
    assert isinstance(await_awaitable(call)["balance"], float)


def test_call_threading():
    Parallel(4, "threading")(
        delayed(Call(CHAI, "name()(string)", [["name", None]]))() for i in range(10)
    )


@pytest.mark.skip(reason="upgraded web3")
def test_call_multiprocessing():
    # NOTE can't have middlewares for multiprocessing
    web3.provider.middlewares = tuple()
    web3.middleware_onion.clear()
    # TODO figure out why multiprocessing fails if you don't call request_func here
    web3.provider.request_func(web3, web3.middleware_onion)
    Parallel(4, "multiprocessing")(
        delayed(Call(CHAI, "name()(string)", [["name", None]], _w3=web3))() for i in range(10)
    )

```

File: tests/__init__.py
```py

```

File: tests/test_multicall.py
```py
from typing import Any, Tuple
import pytest

from brownie import web3
from joblib import Parallel, delayed
from multicall import Call, Multicall
from multicall.multicall import batcher
from multicall.utils import await_awaitable

CHAI = "0x06AF07097C9Eeb7fD685c692751D5C66dB49c215"
WHOAMI = "0x66659E34096372C1aad8d459559432Ab0aa64569"
DUMMY_CALL = Call(CHAI, "totalSupply()(uint)", [["totalSupply", None]])
batcher.step = 10_000


def from_wei(val):
    return val / 1e18


def from_wei_require_success(success, val):
    assert success
    return val / 1e18


def from_ray(val):
    return val / 1e18


def from_ray_require_success(success, val):
    assert success
    return val / 1e27


def unpack_no_success(success: bool, output: Any) -> Tuple[bool, Any]:
    return (success, output)


def test_multicall():
    multi = Multicall(
        [
            Call(CHAI, "totalSupply()(uint256)", [["supply", from_wei]]),
            Call(CHAI, ["balanceOf(address)(uint256)", CHAI], [["balance", from_ray]]),
        ]
    )
    result = multi()
    print(result)
    assert isinstance(result["supply"], float)
    assert isinstance(result["balance"], float)


def test_multicall_with_origin():
    multi = Multicall([
        Call(WHOAMI, ['sender()(address)', CHAI, 1], [['sender', None]]),
        Call(WHOAMI, ['origin()(address)', CHAI, 1], [['origin', None]]),
    ], origin=CHAI)
    result = multi()
    print(result)
    assert isinstance(result['sender'], str)
    assert isinstance(result['origin'], str)

def test_multicall_no_success():
    multi = Multicall(
        [
            Call(
                CHAI,
                "transfer(address,uint256)(bool)",
                [["success", unpack_no_success]],
            ),  # lambda success, ret_flag: (success, ret_flag)
            Call(
                CHAI,
                ["balanceOf(address)(uint256)", CHAI],
                [["balance", unpack_no_success]],
            ),  # lambda success, value: (success, from_ray(value))
        ],
        require_success=False,
    )
    result = multi()
    print(result)
    assert isinstance(result["success"], tuple)
    assert isinstance(result["balance"], tuple)


def test_multicall_async():
    multi = Multicall(
        [
            Call(CHAI, "totalSupply()(uint256)", [["supply", from_wei]]),
            Call(CHAI, ["balanceOf(address)(uint256)", CHAI], [["balance", from_ray]]),
        ]
    )
    result = await_awaitable(multi)
    print(result)
    assert isinstance(result["supply"], float)
    assert isinstance(result["balance"], float)


def test_multicall_no_success_async():
    multi = Multicall(
        [
            Call(
                CHAI,
                "transfer(address,uint256)(bool)",
                [["success", unpack_no_success]],
            ),
            Call(
                CHAI,
                ["balanceOf(address)(uint256)", CHAI],
                [["balance", unpack_no_success]],
            ),
        ],
        require_success=False,
    )
    result = await_awaitable(multi)
    print(result)
    assert isinstance(result["success"], tuple)
    assert isinstance(result["balance"], tuple)


def test_batcher_batch_calls_even():
    batcher.step = 10_000
    calls = [DUMMY_CALL for i in range(30_000)]
    batches = batcher.batch_calls(calls, batcher.step)
    # NOTE batcher.step == 10_000, so with 30_000 calls you should have 3 batches
    assert len(batches) == 3
    for batch in batches:
        print(".", end="")
        assert len(batch) <= batcher.step
    assert sum(len(batch) for batch in batches) == len(calls)


def test_batcher_batch_calls_odd():
    batcher.step = 10_000
    calls = [DUMMY_CALL for i in range(29_999)]
    batches = batcher.batch_calls(calls, batcher.step)
    # NOTE batcher.step == 10_000, so with 30_000 calls you should have 3 batches
    assert len(batches) == 3
    for batch in batches:
        assert len(batch) <= batcher.step
    assert sum(len(batch) for batch in batches) == len(calls)


def test_batcher_split_calls_even():
    calls = [DUMMY_CALL for i in range(30_000)]
    split = batcher.split_calls(calls, batcher.step)
    assert len(split) == 2
    assert sum(len(batch) for batch in split) == len(calls)
    assert len(split[0]) == 15_000
    assert len(split[1]) == 15_000


def test_batcher_split_calls_odd():
    calls = [DUMMY_CALL for i in range(29_999)]
    split = batcher.split_calls(calls, batcher.step)
    assert len(split) == 2
    assert sum(len(batch) for batch in split) == len(calls)
    assert len(split[0]) == 14_999
    assert len(split[1]) == 15_000


@pytest.mark.skip(reason="long running")
def test_batcher_step_down_and_retry():
    batcher.step = 100_000
    calls = [Call(CHAI, "totalSupply()(uint)", [[f"totalSupply{i}", None]]) for i in range(100_000)]
    results = Multicall(calls)()
    assert batcher.step < 100_000
    assert len(results) == len(calls)


@pytest.mark.skip(reason="upgrade web3")
def test_multicall_threading():
    calls = [Call(CHAI, "totalSupply()(uint)", [[f"totalSupply{i}", None]]) for i in range(50_000)]
    Parallel(4, "threading")(
        delayed(Multicall(batch))() for batch in batcher.batch_calls(calls, batcher.step)
    )


@pytest.mark.skip(reason="upgraded web3")
def test_multicall_multiprocessing():
    # NOTE can't have middlewares for multiprocessing
    web3.provider.middlewares = tuple()
    web3.middleware_onion.clear()
    # TODO figure out why multiprocessing fails if you don't call request_func here
    web3.provider.request_func(web3, web3.middleware_onion)
    calls = [Call(CHAI, "totalSupply()(uint)", [[f"totalSupply{i}", None]]) for i in range(50_000)]
    Parallel(4, "multiprocessing")(
        delayed(Multicall(batch, _w3=web3))() for batch in batcher.batch_calls(calls, batcher.step)
    )

```

File: tests/test_utils.py
```py
import pytest
from brownie import web3
from multicall.utils import *
from web3.providers.async_base import AsyncBaseProvider


class UST(Exception):
    pass


oopsie = UST("oops")


def work():
    pass


async def coro():
    return


def exception_coro():
    raise oopsie


def test_chain_id():
    assert chain_id(web3) == 1


def test_await_awaitable():
    assert await_awaitable(coro()) is None


def test_raise_if_exception():
    with pytest.raises(UST):
        raise_if_exception(UST("oops"))


def test_raise_if_exception_in():
    with pytest.raises(UST):
        raise_if_exception_in(["BTC", "ETH", UST("oops")])


def test_gather():
    assert await_awaitable(gather([coro(), coro(), coro(), coro(), coro()])) == [
        None,
        None,
        None,
        None,
        None,
    ]


def test_gather_with_exception():
    with pytest.raises(UST):
        await_awaitable(gather([coro(), coro(), coro(), coro(), exception_coro()]))


def test_get_endpoint_brownie():
    assert get_endpoint(web3) == web3.provider.endpoint_uri


def test_get_endpoint_web3py():
    web3py_w3 = Web3(get_endpoint(web3))
    assert get_endpoint(web3py_w3) == web3.provider.endpoint_uri


@pytest.mark.skip(reason="no local endpoint setup")
def test_get_endpoint_web3py_auto():
    assert get_endpoint(Web3()) == "http://localhost:8545"


def test_get_async_w3_with_sync():
    w3 = get_async_w3(web3)
    assert w3.eth.is_async
    assert isinstance(w3.provider, AsyncBaseProvider)
    assert await_awaitable(w3.eth.chain_id) == 1


def test_get_async_w3_with_async():
    async_w3 = get_async_w3(web3)
    w3 = get_async_w3(async_w3)
    assert w3 == async_w3
    assert await_awaitable(w3.eth.chain_id) == 1


def test_run_in_subprocess():
    assert await_awaitable(run_in_subprocess(work)) is None


def test_get_event_loop():
    assert get_event_loop() == asyncio.get_event_loop()


def test_get_event_loop_in_thread():
    def task():
        assert get_event_loop() == asyncio.get_event_loop()

    await_awaitable(get_event_loop().run_in_executor(None, task))

```

File: tests/test_signature.py
```py
from multicall import Signature
from multicall.signature import encode

args = ((1, 2, 3), "0x" + "f" * 40, b"data")
types = ["uint256[]", "address", "bytes"]


def test_signature_parsing():
    sig = Signature("aggregate((address,bytes)[])(uint256,bytes[])")
    assert sig.function == "aggregate((address,bytes)[])"
    assert sig.input_types == ["(address,bytes)[]"]
    assert sig.output_types == ["uint256", "bytes[]"]


def test_signature_encoding():
    sig = Signature("test(uint256[],address,bytes)()")
    assert sig.encode_data(args) == sig.fourbyte + encode(types, args)


def test_signature_decoding():
    sig = Signature("test()(uint256[],address,bytes)")
    data = encode(types, args)
    assert sig.decode_data(data) == args

```

File: pyproject.toml
```toml
[tool.poetry]
name = "multicall"
version = "0.10.0"
description = "aggregate results from multiple ethereum contract calls"
authors = ["banteg"]

[tool.poetry.dependencies]
python = ">=3.8,<4"
cchecksum = ">=0.0.3,<1"
# These web3.py versions have a busted async provider and cannot be used in any multithreaded applications
web3 = ">=5.27,!=5.29.*,!=5.30.*,!=5.31.0,!=5.31.1,!=5.31.2"
eth_retry = ">=0.1.8"

[tool.poetry.group.dev.dependencies]
pytest = ">=6.2.5"
ruff = ">=0.3.5"
joblib = ">=1.2"
eth-brownie = { "version" = ">=1.19.3", "python" = ">=3.10,<4" }
vyper = { "version" = "*", "python" = "<3.11" }

[build-system]
requires = ["poetry-core"]
build-backend = "poetry.core.masonry.api"

[tool.black]
line-length = 100

```

File: readme.md
```md
# multicall.py

python interface for makerdao's [multicall](https://github.com/makerdao/multicall) and a port of [multicall.js](https://github.com/makerdao/multicall.js)

## installation

```
pip install multicall
```

## example

```python
from multicall import Call, Multicall

# assuming you are on kovan
MKR_TOKEN = '0xaaf64bfcc32d0f15873a02163e7e500671a4ffcd'
MKR_WHALE = '0xdb33dfd3d61308c33c63209845dad3e6bfb2c674'
MKR_FISH = '0x2dfcedcb401557354d0cf174876ab17bfd6f4efd'

def from_wei(value):
    return value / 1e18

multi = Multicall([
    Call(MKR_TOKEN, ['balanceOf(address)(uint256)', MKR_WHALE], [('whale', from_wei)]),
    Call(MKR_TOKEN, ['balanceOf(address)(uint256)', MKR_FISH], [('fish', from_wei)]),
    Call(MKR_TOKEN, 'totalSupply()(uint256)', [('supply', from_wei)]),
])

multi()  # {'whale': 566437.0921992733, 'fish': 7005.0, 'supply': 1000003.1220798912}

# seth-style calls
Call(MKR_TOKEN, ['balanceOf(address)(uint256)', MKR_WHALE])()
Call(MKR_TOKEN, 'balanceOf(address)(uint256)')(MKR_WHALE)
# return values processing
Call(MKR_TOKEN, 'totalSupply()(uint256)', [('supply', from_wei)])()
```

for a full example, see implementation of [daistats](https://github.com/banteg/multicall.py/blob/master/examples/daistats.py).
original [daistats.com](https://daistats.com) made by [nanexcool](https://github.com/nanexcool/daistats).

## api

### `Signature(signature)`

- `signature` is a seth-style function signature of `function_name(input,types)(output,types)`. it also supports structs which need to be broken down to basic parts, e.g. `(address,bytes)[]`.

use `encode_data(args)` with input args to get the calldata. use `decode_data(output)` with the output to decode the result.

### `Call(target, function, returns)`

- `target` is the `to` address which is supplied to `eth_call`.
- `function` can be either seth-style signature of `method(input,types)(output,types)` or a list of `[signature, *args]`.
- `returns` is a list of tuples of `(name, handler)` for return values. if `returns` argument is omitted, you get a tuple, otherwise you get a dict. to skip processing of a value, pass `None` as a handler.

use `Call(...)()` with predefined args or `Call(...)(args)` to reuse a prepared call with different args.

use `decode_output(output)` with to decode the output and process it with `returns` handlers.

### `Multicall(calls)`

- `calls` is a list of calls with prepared values.

use `Multicall(...)()` to get the result of a prepared multicall.

### Environment Variables

- GAS_LIMIT: sets overridable default gas limit for Multicall to prevent out of gas errors. Default: 50,000,000
- MULTICALL_DEBUG: if set, sets logging level for all library loggers to logging.DEBUG
- MULTICALL_PROCESSES: pass an integer > 1 to use multiprocessing for encoding args and decoding results. Default: 1, which executes all code in the main process.
- AIOHTTP_TIMEOUT: sets aiohttp timeout period in seconds for async calls to node. Default: 30

## test
```bash
export WEB3_INFURE_PROJECT_ID=<your_infura_id>
export PYTEST_NETWORK='mainnet'
poetry run python -m pytest
```
```
</file_contents>
