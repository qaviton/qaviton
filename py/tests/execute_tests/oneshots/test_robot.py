import pytest
from qaviton.utils.robot import keyboard, mouse


@pytest.mark.skip(reason="this should not run in regression, its a one shot")
def test_robot():
    keyboard.press_and_release('shift+s, space')

    mouse.click()
    mouse.hold()
    mouse.release()

    keyboard.write('The quick brown fox jumps over the lazy dog.')

    # Press PAGE UP then PAGE DOWN to type "foobar".
    keyboard.add_hotkey('page up, page down', lambda: keyboard.write('foobar'))

    # Blocks until you press esc.
    keyboard.wait('esc')

    # Record events until 'esc' is pressed.
    recorded = keyboard.record(until='esc')
    # Then replay back at three times the speed.
    keyboard.play(recorded, speed_factor=3)

    # Type @@ then press space to replace with abbreviation.
    keyboard.add_abbreviation('@@', 'my.long.email@example.com')
    # Block forever.
    keyboard.wait()
