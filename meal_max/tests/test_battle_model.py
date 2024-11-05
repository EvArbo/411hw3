import pytest
from unittest.mock import Mock

from meal_max.models.battle_model import BattleModel
from meal_max.models.kitchen_model import Meal

@pytest.fixture()
def battle_model():
    """Fixture to provide a new instance of BattleModel for each test."""
    return BattleModel()

@pytest.fixture
def mock_update_meal_stats(mocker):
    """Mock the update_meal_stats function for testing purposes."""
    return mocker.patch("meal_max.models.kitchen_model.update_meal_stats")

@pytest.fixture
def sample_meal1():
    return Meal(id=1, meal="Meal 1", cuisine="Cuisine 1", price=10.0, difficulty="LOW")

@pytest.fixture
def sample_meal2():
    return Meal(id=2, meal="Meal 2", cuisine="Cuisine 2", price=15.0, difficulty="MED")

@pytest.fixture
def sample_battle(sample_meal1, sample_meal2):
    return [sample_meal1, sample_meal2]

##################################################
# Battle Outcome Test Cases
##################################################

def test_battle_normal_outcome(battle_model, sample_battle):
    """Test the normal outcome of a battle"""
    battle_model.combatants = (sample_battle)
    
    mocker.patch.object(battle_model, 'get_battle_score', side_effect=[50, 30])
    mocker.patch('battle_model.get_random', return_value=0.1)

    assert battle_model.battle() == "Meal 1", "Meal 1 is the expected winner"
    
    mock_update_stats.assert_any_call(1, 'win')
    mock_update_stats.assert_any_call(2, 'loss')
    
    assert len(battle_model.combatants) == 1
    assert battle_model.combatants[0] == sample_meal1, "Loser was not removed correctly."

def test_battle_random_outcome(battle_model, sample_battle):
    """Test the normal outcome of a battle"""
    battle_model.combatants = (sample_battle)
    
    mocker.patch.object(battle_model, 'get_battle_score', side_effect=[30, 32])
    mocker.patch('battle_model.get_random', return_value=0.025)

    assert battle_model.battle() == "Meal 2", "Meal 2 is the expected winner"
    
    mock_update_stats.assert_any_call(2, 'win')
    mock_update_stats.assert_any_call(1, 'loss')
    
    assert len(battle_model.combatants) == 1
    assert battle_model.combatants[0] == sample_meal2, "Loser was not removed correctly."

def test_battle_not_enough_combatants():
    """Test error when intiating battle with less than 2 combatants"""
    battle_model.combatants = [Mock()]
    with pytest.raises(ValueError, match="Two combatants must be prepped for a battle."):
        battle_model.battle()

##################################################
# Add Combatant Mangement Test Cases
##################################################

def test_add_meal_to_battle(battle_model, sample_meal1):
    """Test adding a meal to the battle."""
    battle_model.prep_combatant(sample_meal1)
    assert len(battle_model.combatants) == 1
    assert battle_model.combatants[0].meal == 'Meal 1'

def test_add_meal_to_full_battle(battle_model, sample_meal1):
    """Test error when adding a meal to a battle with 2 combatants."""
    battle_model.prep_combatant(sample_meal1)
    with pytest.raises(ValueError, match="Combatant list is full, cannot add more combatants."):
        battle_model.prep_combatant(sample_meal1)

##################################################
# Clear Combatant Mangement Test Cases
##################################################

def test_clear_battle(battle_model, sample_meal1):
    """Test clearing the battle."""
    battle_model.prep_combatant(sample_meal1)

    battle_model.clear_combatants()
    assert len(battle_model.combatants) == 0, "Battle should be empty after clearing"

def test_clear_battle_empty_battle(battle_model, caplog):
    """Test clearing the battle when it's empty."""
    battle_model.clear_combatants()
    assert len(battle_model.combatants) == 0, "Battle should be empty after clearing"
    assert "Clearing an empty battle" in caplog.text, "Expected warning message when clearing an empty battle"

##################################################
# Combatant Retrieval Test Cases
##################################################

def test_get_battlescore(battle_model, sample_meal1):
    """Test successfully retrieving the battle score."""
    score = battle_model.get_battle_score(sample_meal1)
    expected_score = (10.0 * 9) - 1
    assert score == expected_score, "The battle score retrieved must be equal to the calculated score"

def test_get_all_songs(battle_model, sample_battle):
    """Test successfully retrieving all combatants in the battle."""
    battle_model.combatants.extend(sample_battle)

    all_combatants = battle_model.get_combatants()
    assert len(all_combatants) == 2
    assert all_combatants[0].id == 1
    assert all_combatants[1].id == 2
