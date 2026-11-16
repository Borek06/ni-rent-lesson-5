from src.models import Apartment
from src.manager import Manager
from src.models import Parameters


def test_load_data():
    parameters = Parameters()
    manager = Manager(parameters)
    assert isinstance(manager.apartments, dict)
    assert isinstance(manager.tenants, dict)
    assert isinstance(manager.transfers, list)
    assert isinstance(manager.bills, list)

    for apartment_key, apartment in manager.apartments.items():
        assert isinstance(apartment, Apartment)
        assert apartment.key == apartment_key

def test_tenants_in_manager():
    parameters = Parameters()
    manager = Manager(parameters)
    assert len(manager.tenants) > 0
    names = [tenant.name for tenant in manager.tenants.values()]
    for tenant in ['Jan Nowak', 'Adam Kowalski', 'Ewa Adamska']:
        assert tenant in names

def test_if_tenants_have_valid_apartment_keys():
    parameters = Parameters()
    manager = Manager(parameters)
    assert manager.check_tenants_apartment_keys() == True

    manager.tenants['tenant-1'].apartment = 'invalid-key'
    assert manager.check_tenants_apartment_keys() == False

def test_get_apartment_costs(): #test z trzema asercjami
    parameters = Parameters()
    manager = Manager(parameters)

    # (Czy) takie mieszkanie nie istnieje
    assert manager.get_apartment_costs("nieistniejace", 2025, 1) is None

    # (Czy) jeśli mieszkanie istnieje, ale nie ma rachunków za wskazany okres, powinna zwrócić 0.0
    assert manager.get_apartment_costs("apart-polanka", 2030, 1) == 0.0

    # (Czy) jeśli są rachunki za styczeń 2025, powinna zwrócić sumę 910 zł
    assert manager.get_apartment_costs("apart-polanka", 2025, 1) == 910.0