// SPDX-License-Identifier: MIT
pragma solidity ^0.8.7;
 
import "@chainlink/contracts/src/v0.8/interfaces/AggregatorV3Interface.sol";
 
contract PriceConsumerV3 {
 
    AggregatorV3Interface internal priceFeed;
 
    /**
     * Network: Rinkeby
     * Aggregator: ETH/USD
     * Address: 0x8A95c7Bb4cfB368F886749C88CCB090f588E1cc4
     */
    constructor() {
        priceFeed = AggregatorV3Interface(0x7d97425df9Fc358C9d0D7D7e6dCF0178aEDCA6BA);
    }
 
    /**
     * Returns the latest price
     */
    function getLatestPrice() public view returns (int) {
        (
            uint80 roundID,
            int price,
            uint startedAt,
            uint timeStamp,
            uint80 answeredInRound
        ) = priceFeed.latestRoundData();
        return price;
    }
}