# The MIT License (MIT)
# Copyright © 2025 Dinobets

import time, random
import numpy as np
from typing import List

import bittensor as bt

from dinobets.base.validator import BaseValidatorNeuron
from dinobets.utils.uids import get_random_uids
from dinobets.protocol import DinobetsSynapse
from dinobets.utils.score import compute_miner_scores

class Validator(BaseValidatorNeuron):
    """
    Your validator neuron class. You should use this class to define your validator's behavior. In particular, you should replace the forward function with your own logic.

    This class inherits from the BaseValidatorNeuron class, which in turn inherits from BaseNeuron. The BaseNeuron class takes care of routine tasks such as setting up wallet, subtensor, metagraph, logging directory, parsing config, etc. You can override any of the methods in BaseNeuron if you need to customize the behavior.

    This class provides reasonable default behavior for a validator such as keeping a moving average of the scores of the miners and using them to set weights at the end of each epoch. Additionally, the scores are reset for new hotkeys at the end of each epoch.
    """

    def __init__(self, config=None):
        super(Validator, self).__init__(config=config)

        bt.logging.info("load_state()")
        self.load_state()

    def reward(query: int, response: int) -> float:
        """
        Reward the miner response to the request. This method returns a reward
        value for the miner, which is used to update the miner's score.

        Returns:
        - float: The reward value for the miner.
        """
        bt.logging.info(
            f"In rewards, query val: {query}, response val: {response}, rewards val: {1.0 if response == query * 2 else 0}"
        )
        return 1.0 if response == query * 2 else 0

    def get_rewards(
        self,
        query: int,
        responses: List[float],
    ) -> np.ndarray:
        """
        Returns an array of rewards for the given query and responses.

        Args:
        - query (int): The query sent to the miner.
        - responses (List[float]): A list of responses from the miner.

        Returns:
        - np.ndarray: An array of rewards for the given query and responses.
        """
        # Get all the reward results by iteratively calling your reward() function.

        return np.array([self.reward(query, response) for response in responses])

    async def forward(self):
        """
        The forward function is called by the validator every time step.
        It is responsible for querying the network and scoring the responses.

        Args:
            self (:obj:`bittensor.neuron.Neuron`): The neuron object which contains all the necessary state for the validator.

        """
        # TODO(developer): Define how the validator selects a miner to query, how often, etc.
        # get_random_uids is an example method, but you can replace it with your own.
        miner_uids = get_random_uids(self, k=self.config.neuron.sample_size)

        # The dendrite client queries the network.
        responses = await self.dendrite(
            # Send the query to selected miner axons in the network.
            axons=[self.metagraph.axons[uid] for uid in miner_uids],
            # Construct a dummy query. This simply contains a single integer.
            synapse=DinobetsSynapse(synapse_input=self.step),
            # All responses have the deserialize function called on them before returning.
            # You are encouraged to define your own deserialization function.
            deserialize=True,
        )

        # Log the results for monitoring purposes.
        bt.logging.info(f"Received responses: {responses}")

        # TODO(developer): Define how the validator scores responses.
        # Adjust the scores based on responses from miners.
        rewards = self.get_rewards(self, query=self.step, responses=responses)

        bt.logging.info(f"Scored responses: {rewards}")
        # Update the scores based on the rewards. You may want to define your own update_scores function for custom behavior.
        self.update_scores(rewards, miner_uids)
        time.sleep(5)
        return
    
    def score(self, _):
        time.sleep(3600)
        try:
            bt.logging.info('Calculating score...')
            self.scores = compute_miner_scores(self.metagraph.n)
            bt.logging.info("Weights updated, rewards will follow automatically.")
        except Exception as e:
            bt.logging.error("Exception: ", e)


# The main function parses the configuration and runs the validator.
if __name__ == "__main__":
    bt.logging.enable_info()
    with Validator() as validator:
        validator.loop.run_until_complete = validator.score
        validator.concurrent_forward = lambda: ...
        step = 0
        while True:
            if step % 60 == 0: bt.logging.info(f"Validator running... {time.time()}")
            time.sleep(1)
            step += 1