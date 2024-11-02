import pytest

from meal_max.models.battle_model import BattleModel
from meal_max.models.kitchen_model import Meal

@pytest.fixture()
def battle_model():
    """Fixture to provide a new instance of PlaylistModel for each test."""
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

def test_clear_playlist_empty_playlist(battle_model, caplog):
    """Test clearing the entire playlist when it's empty."""
    playlist_model.clear_playlist()
    assert len(playlist_model.playlist) == 0, "Playlist should be empty after clearing"
    assert "Clearing an empty playlist" in caplog.text, "Expected warning message when clearing an empty playlist"
