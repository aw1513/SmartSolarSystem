# SmartSolarSystem

Climate change requires actions by everyone. Renewable energy is an essential ingredient where private house owners play a crucial role. 
The integration of renewable energy into existing power grids is making slow progress. It is challenging due to its inherent production flucutuations which cause grid instabilities leading to high maintenance and operational costs. 
To accelerate and facilitate the integration of renewables it is therefore indispensible to find technical solutions to increase the stability. Our SmartSolarSystem application is one important piece to solve this puzzle through the optimisation of self-consumption. Users profit from a currency backed by renewable energy.


We combine machine learning, an optimisation algorithm and the Ethereum blockchain to create a smart home with an incentive to minimise the strain on the electrical grid. This empowers the smart home owners to optimise their self-consumption with a smart optimiser taking into account state-of-the art predictions of the solar energy production in combination with a token-based reward system. At the same time, the feed-in to the electrical grid is minimised - as a result, the SmartSolarSystem helps reduce the stress on the grid.


## Description of the system:
The SmartSolarSystem has a fully decentralised front-end and back-end with the following components:
- Based on public weather forcasts and learned features about the individual system, the machine learning component predicts an hourly solar energy production for the next day. It makes use of a random forest implemenation.
- The optimiser is an algorithm that minimises the surplus energy for the next 24h, which is equivalent to the difference between the predicted production and the self-consumption. A variety of electrical appliances are implemented, for example household devices and storage batteries. The algorithm will learn about the house owners base consumption as well as incorporate IoT information about the devices.
- The SmartMeter delivers the actual self-consumption data in kWh which determines the amount of tokens transfered as a reward. The transactions are stored in a smart contract architecture consisting of three contracts deployed on the Ethereum blockchain: the network operator as the owner of the contract can trigger the registration of a house owner, the creation  of ERC20 standard tokens as well as the transfer of tokens to the house owner.
- A front-end interface presents the information of the predictor, the optimiser, and the tokens to the house owner.
