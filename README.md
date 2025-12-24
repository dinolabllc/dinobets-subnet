<div align="center">

# **Dinobets - Decentralized Casino**
[![Discord Chat](https://img.shields.io/discord/308323056592486420.svg)](https://discord.gg/bittensor)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT) 

---

[Discord](https://discord.gg/bittensor) • [Network](https://taostats.io/) • [Research](https://bittensor.com/whitepaper)
</div>

---

- [Introduction](#Introduction)
- [Roadmap](#Roadmap)
- [Installation](#Installation)
- [Miners](#Miners)
- [Validators](#Validators)
- [Scoring](#Scoring)
- [Disclaimer](#Disclaimer)
- [License](#License)

---
## Introduction

Dinobets is a decentralized, provably fair casino platform that empowers operators to launch and manage their own casino games without developing the whole casino platform or games and marketing efforts. The platform is built on the Dinobets Bittensor subnet, where operators participate as miners to earn rewards. Dinobets offers a suite of on-chain casino games that operators can easily deploy. By joining the Dinobets subnet as a miner and configuring a game pool, operators gain access to automated, fair, and transparent casino infrastructure. Operators generate hashes for their games and all hashes are verified by our platform and validators in historical.

---
## Roadmap

**Phase I** - *Live on Mainnet*
- Original games - Crash
- Operator games - Limbo
- PvP games - Bullet Spin
- Available tokens - TAO, USDT, ETH, BNB, TRON
- Lottery with Jackpot

**Phase II** - *4 months*
- Original games - Roulette
- Operator games - Coinflip, Mines, Dice
- PvP games - RPS (rock & paper & scissors)
- Available tokens - BTC, Solana, USDC, XRP, LTC, DOGE

**Phase III**- *4 months*
- Three original slot games
- Three operator slot games
- Three pvp games
- Affiliate slot providers

*Ongoing: As a VIP service, we accept and develop custom new game types based on operator requirements.*

---
## Installation

For first-time miners, please follow the [Bittensor document](https://docs.learnbittensor.org/miners/) to register a hotkey.

Please avoid using the root account, and make sure Python3 is available as command `python` under a regular user account. Ubuntu 22.04 is the only officially supported OS, although many other OSes can also work with minimum tweaks, including macOS.

```bash
sudo apt update
sudo apt install npm -y
sudo npm install pm2 -g
```

```bash
git clone https://github.com/dinolabllc/dinobets-subnet

cd dinobets-subnet
python -m venv .venv
source .venv/bin/activate

pip install -e .
```

---
## Miners

Miners can create a game pool and configure the required parameters with selecting game type in the Dinobets Operator Dashboard.

Current available operator game types:
`Limbo`

After depositing into the game pool, operators must configure the following:

- **House Edge**
must be greater than 0.005, which includes the Dinobets service fee.

- **Max Profit**
is the maximum payout a user can win in a single round.\
`Max profit >= Pool Amount / 100000`\
Recommended to be less than `Pool Amount / 1000`


```bash
source .venv/bin/activate

pm2 start ./neurons/miner.py \
    --name dinobets-miner -- \
    --wallet.name {coldkey} \
    --wallet.hotkey {hotkey} \
    --netuid {netuid}
```

---
## Validators

```bash
source .venv/bin/activate

pm2 start ./neurons/validator.py \
    --name dinobets-validator -- \
    --wallet.name {coldkey} \
    --wallet.hotkey {hotkey} \
    --netuid {netuid}
```

---
## Scoring

Operator performance and ranking are determined using the following scoring model:

- **P** = Pool amount
- **M** = Max profit
- **H** = House edge
- **C** = Number of unique users who play the operator's game
- **G** = Daily percentage change of game-playing users
- **W** = Total wager amount
- **D** = Number of days the game has been running

```math
\begin{aligned}
Score = {\frac{\sqrt{M*P}}{H}} + \ln{C}*(1+0.5*G)*{\frac{W}{D}}
\end{aligned}
```

*We are on the testnet netuid 427.*

---
## Disclaimer

Casino games with good house edge and enough pool are profitable in the long term, but operators may still experience short‑term losses.

Dinobets is not responsible for any losses due to operator misconfiguration or poor risk management.

Operators must:

- Carefully set all parameters
- Manage their pool responsibly
- Understand the inherent risks of hosting casino games

For support, technical guidance, or community discussions, please refer to the Dinobets documentation and community channels.

---

## License

This repository is licensed under the MIT License.
```text
# The MIT License (MIT)
# Copyright © 2025 Dinolabs LLC

# Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated
# documentation files (the “Software”), to deal in the Software without restriction, including without limitation
# the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software,
# and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all copies or substantial portions of
# the Software.

# THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO
# THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL
# THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION
# OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
# DEALINGS IN THE SOFTWARE.
```
