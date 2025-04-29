import builtins
import pytest
from unittest.mock import AsyncMock
from main import main
from pizza_plugin import PizzaPlugin

@pytest.mark.asyncio
async def test_pizza_plugin(capsys, monkeypatch):
    # Mock the Semantic Kernel and its plugin
    mock_kernel = AsyncMock()
    mock_kernel.text_completion = AsyncMock()
    mock_kernel.text_completion.side_effect = [
        "balance : Rs.144.34",
        "{'Pizza 1': {'Name': 'Bryon's Bigdamaka pizza', 'Price': 180.76}, 'Pizza 2': {'Name': 'Gramin's Small Pizza', 'Price': 129.87}, 'Pizza 3': {'Name': 'Jaorin's Special Pizza', 'Price': 239.76}}",
        "Your order for Gramin's Small Pizza has been placed successfully."
    ]
    mock_kernel.get_full_list_of_function_metadata = lambda: []

    # Mock input to simulate user interaction
    inputs = iter(["Check balance", "Get available pizzas", "Order Gramin's Small Pizza", "q"])
    monkeypatch.setattr(builtins, "input", lambda _: next(inputs))

    # Patch the Kernel and OllamaTextCompletion
    with pytest.MonkeyPatch.context() as mp:
        mp.setattr("main.Kernel", lambda: mock_kernel)

        # Call the main function
        await main()

        # Capture the output
        captured = capsys.readouterr()

        # Define the expected output
        expected_output = (
            "balance : Rs.144.34\n"
            "{'Pizza 1': {'Name': 'Bryon's Bigdamaka pizza', 'Price': 180.76}, 'Pizza 2': {'Name': 'Gramin's Small Pizza', 'Price': 129.87}, 'Pizza 3': {'Name': 'Jaorin's Special Pizza', 'Price': 239.76}}\n"
            "Your order for Gramin's Small Pizza has been placed successfully.\n"
        )

        # Assert the output matches the expected conversation
        assert captured.out.strip() == expected_output.strip()