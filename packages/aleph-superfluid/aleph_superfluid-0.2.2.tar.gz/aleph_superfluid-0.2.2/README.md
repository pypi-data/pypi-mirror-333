<h1 align="center">Welcome to Superfluid Python SDK(Unofficial) 👋
</h1>
<div align="center">
<img  width="300" padding="0 0 10px" alt="Superfluid logo" src="https://github.com/superfluid-finance/protocol-monorepo/raw/dev/sf-logo.png" />
<p>
  <a href="#" target="_blank">
    <img alt="License: MIT" src="https://img.shields.io/badge/License-MIT-yellow.svg" />
  </a>
  <a href="https://twitter.com/Superfluid_HQ/" target="blank">
    <img alt="Twitter: Superfluid_HQ" src="https://img.shields.io/twitter/follow/Superfluid_HQ.svg?style=social" />
  </a>
</p>
</div>

### 🏠 [Homepage](https://superfluid.finance)

### ✨ [Superfluid App](https://app.superfluid.finance/)

### 📖 [Docs](https://docs.superfluid.finance)

</br>

# Introduction

superfluid.py is an application framework for interacting with the Superfluid Protocol using the Python Programming Language.

This is a friendly fork that adds support for the Base blockchain. It may be deprecated once [merged upstream](https://github.com/Godspower-Eze/superfluid.py/pull/1).

# Features

* Minimal Framework initialization (`rpc` and `chain id`)
* New Operation syntax for transactions
* Read/Create/Update/Delete Agreement Operations (Constant Flow Agreement and Instant Distribution Agreement(In development))

# Notable Used Technologies

* Python
* Web3.py

# Installation

```bash
pip install superfluid
```

# Usage

```python
from superfluid import CFA_V1
from superfluid import Web3FlowInfo

rpc: str = "YOUR PREFERRED RPC"
chain_id: int = "CHAIN ID"

######################################################
###### CONSTANT FLOW AGREEMENT OPERATIONS ###########
######################################################

cfaV1Instance = CFA_V1(rpc, chain_id)

super_token: str = "SUPER TOKEN ADDRESS"
sender: str = "SENDER ADDRESS"
receiver: str = "RECEIVER ADDRESS"
flow_rate: int = "FLOW RATE"

PRIVATE_KEY: str = "YOUR PRIVATE KEY"

flow_data: Web3FlowInfo = cfaV1Instance.get_flow(super_token, sender, receiver)

create_flow_operation = cfaV1Instance.create_flow(
    sender, receiver, super_token, flow_rate)
transaction_hash = create_flow_operation.exec(PRIVATE_KEY)

update_flow_operation = cfaV1Instance.update_flow(
    sender, receiver, super_token, flow_rate)
transaction_hash = update_flow_operation.exec(PRIVATE_KEY)

delete_flow_operation = cfaV1Instance.delete_flow(
    sender, receiver, super_token)
transaction_hash = delete_flow_operation.exec(PRIVATE_KEY)
```
