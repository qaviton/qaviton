import pytest
from qaviton.utils import unique_id

####################################
# you can ignore these tests below #
####################################


@pytest.mark.skip(reason="just testing double parameters for cross-platform & data-driven testing (it's a one shot)")
@pytest.mark.parametrize('test', [0.0,1.0,2.0], ids=unique_id.id)
@pytest.mark.parametrize('data', [0,1,2,3], ids=unique_id.id)
def test_2_layered_data(test, data):
    print(test, data)


@pytest.mark.skip(reason="don't run this its a script")
def test_all_drivers_are_done():
    import psutil

    for proc in psutil.process_iter():
        try:
            if "chrome" in proc.name():
                p = psutil.Process(proc.pid)
                # if 'SYSTEM' not in p.username:
                proc.kill()
        except Exception as e:
            print(e)