import pytest
import brownie
from brownie import Wei
from brownie import config


def test_constructor(vault, gov, strategy, strategist, comp, idle, token):
    assert strategy.name() == "StrategyIdleidle"+ token.symbol().upper() + "Yield"
    assert strategy.govTokens(0) == comp
    assert strategy.govTokens(1) == idle

def test_incorrect_vault(pm, guardian, gov, strategist, rewards, strategyFactory, Token):
    token = guardian.deploy(Token)
    Vault = pm(config["dependencies"][0]).Vault
    vault = guardian.deploy(Vault)
    vault.initialize(token, gov, rewards, "", "")
    with brownie.reverts("Vault want is different from Idle token underlying"):
        strategy = strategyFactory(vault)

def test_double_init(strategy, strategist):
    with brownie.reverts("Strategy already initialized"):
        strategy.init(
            strategist,
            strategist,
            [],
            strategist,
            strategist,
            strategist,
            strategist,
            strategist
        )

def test_double_init_no_proxy(strategyFactory, vault, strategist):
    strategy = strategyFactory(vault, False)
    with brownie.reverts("Strategy already initialized"):
        strategy.init(
            strategist,
            strategist,
            [],
            strategist,
            strategist,
            strategist,
            strategist,
            strategist
        )