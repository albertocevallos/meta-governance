// SPDX-License-Identifier: MIT

pragma solidity 0.8.12;

import { SafeMath } from "@openzeppelin/contracts/utils/math/SafeMath.sol";
import { IERC20 } from "@openzeppelin/contracts/interfaces/IERC20.sol";

/**
 * @title MetaGovernance
 * @author Alberto Cevallos
 *
 * Contract for weighted quadratic voting in token holder governance.
 *
 */
contract MetaGovernance {

    using SafeMath for uint256;

    /* ============ Enums ============ */
    /* ============ Constants ============= */
    /* ============ State Variables ============ */

    address public owner;
    address public token;
    string public name;
    string public symbol;
    address[] public tokens;
    uint256[] public multiples;
    bool[] public isLp;

    /* ============ Events ============ */
    /* ============ Modifiers ============ */
    modifier onlyOwner() {
         require(msg.sender == owner);
         _;
    }

    /* ============ Constructor ============ */
    constructor(
        address _owner,
        address _token,
        string memory _name,
        string memory _symbol,
        address[] memory _tokens,
        uint256[] memory _multiples,
        bool[] memory _isLp


    ) {
        owner = _owner;
        token = _token;
        name = _name;
        symbol = _symbol;
        tokens = _tokens;
        multiples = _multiples;
        isLp = _isLp;

    }

    /* ============ External Functions ============ */

    /**
     * Calculates a voter's balance given their multiple holdings.
     *
     * @param _voter        Address of the voter who's balance is being calculated
     *
     * @return sum          Returns voter's adjusted balanced given balanced and multiples.
     */
    function balanceOf(address _voter) external view returns (uint256) {
        uint256 sum = 0;
        for (uint i = 0; i < tokens.length; i++) {
            uint256 realBalance = IERC20(tokens[i]).balanceOf(_voter);
            sum = sum.add(realBalance.mul(multiples[i]));
        }
        return sum;
    }

    /* ============ Internal Functions ============ */

    function _getBalancesFromLp(address _voter, address _lpToken) internal view returns (uint256) {
        uint256 tokensInLp = IERC20(token).balanceOf(_lpToken);
        uint256 lpSupply = IERC20(_lpToken).totalSupply();
        uint256 lpBalanceOfUser = IERC20(_lpToken).balanceOf(_voter);
        return lpBalanceOfUser.mul(tokensInLp).div(lpSupply);
    }
}
    