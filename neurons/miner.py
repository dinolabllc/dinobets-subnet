# The MIT License (MIT)
# Copyright © 2025 DinoBets

import time
import typing
import bittensor as bt
import hash
from dinobets.protocol import DinobetsSynapse
from dinobets.base.miner import BaseMinerNeuron

class Miner(BaseMinerNeuron):
    """
    Miner class that generates server seed and server hash for provabley fairness.
    """
    def __init__(self, config=None):
        super(Miner, self).__init__(config=config)

    async def forward(
        self, synapse: DinobetsSynapse
    ) -> DinobetsSynapse:
        """
        Process incoming requests for casino game hash.
        """
        try:
            result = await self.generate_hash(synapse)    
            return result
        
        except Exception as e:
            bt.logging.error(f"Error in forward function: {e}")
            return result
    
    async def blacklist(
        self, synapse: DinobetsSynapse
    ) -> typing.Tuple[bool, str]:
        """
        Blacklist logic for incoming requests.
        """
        if synapse.dendrite is None or synapse.dendrite.hotkey is None:
            bt.logging.warning(
                "Received a request without a dendrite or hotkey."
            )
            return True, "Missing dendrite or hotkey"
        uid = self.metagraph.hotkeys.index(synapse.dendrite.hotkey)
        if (
            not self.config.blacklist.allow_non_registered
            and synapse.dendrite.hotkey not in self.metagraph.hotkeys
        ):
            # Ignore requests from un-registered entities.
            bt.logging.trace(
                f"Blacklisting un-registered hotkey {synapse.dendrite.hotkey}"
            )
            return True, "Unrecognized hotkey"

        if self.config.blacklist.force_validator_permit:
            # If the config is set to force validator permit, then we should only allow requests from validators.
            if not self.metagraph.validator_permit[uid]:
                bt.logging.warning(
                    f"Blacklisting a request from non-validator hotkey {synapse.dendrite.hotkey}"
                )
                return True, "Non-validator hotkey"

        bt.logging.trace(
            f"Not Blacklisting recognized hotkey {synapse.dendrite.hotkey}"
        )
        return False, "Hotkey recognized!"

    async def priority(self, synapse: DinobetsSynapse) -> float:
        """
        Priority function based on stake.
        """
        if synapse.dendrite is None or synapse.dendrite.hotkey is None:
            bt.logging.warning(
                "Received a request without a dendrite or hotkey."
            )
            return 0.0
        caller_uid = self.metagraph.hotkeys.index(
            synapse.dendrite.hotkey
        )
        priority = float(
            self.metagraph.S[caller_uid]
        )
        bt.logging.trace(
            f"Prioritizing {synapse.dendrite.hotkey} with value: {priority}"
        )
        return priority

    async def generate_hash(self, synapse: DinobetsSynapse) -> DinobetsSynapse:
        """
        Generate server seed and server hash...
        """
        result = hash.generate_hash(
            synapse.client_seed,     
            synapse.nonce,
            synapse.round_id,
        )

        synapse.server_hash = result['server_hash']
        synapse.server_seed = result['server_seed']
        synapse.hash = result['hash']
        return synapse

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Cleanup when exiting the context."""
        if hasattr(self, 'conn') and self.conn:
            self.conn.close()
        super().__exit__(exc_type, exc_val, exc_tb)

# This is the main function, which runs the miner.
if __name__ == "__main__":
    bt.logging.enable_info()
    with Miner() as miner:
        while True:
            bt.logging.info(f"Miner running... {time.time()}")
            time.sleep(5)
