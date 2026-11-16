from src.models import Apartment
from src.manager import Manager
from src.models import Parameters
from src.models import ApartmentSettlement
from src.models import TenantSettlement


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

def test_get_apartment_costs_invalid_month():
    parameters = Parameters()
    manager = Manager(parameters)

    try:
        manager.get_apartment_costs("apart-polanka", 2025, 13)
        assert False
    except ValueError:
        pass



def test_create_apartment_settlement():
    manager = Manager(Parameters())

    settlement = manager.create_apartment_settlement("apart-polanka", 2025, 1)

    assert isinstance(settlement, ApartmentSettlement)
    assert settlement.apartment == "apart-polanka"
    assert settlement.year == 2025
    assert settlement.month == 1
    assert settlement.total_bills_pln == 910.0

    assert settlement.total_rent_pln == 0.0 #ile zaplacil
    assert settlement.total_due_pln == 910.0 #ile wisi hajsu

    #mieszkanie nie ma rachunków.
    empty_settlement = manager.create_apartment_settlement("apart-polanka", 2030, 1)

    assert isinstance(empty_settlement, ApartmentSettlement)
    assert empty_settlement.apartment == "apart-polanka"
    assert empty_settlement.year == 2030
    assert empty_settlement.month == 1
    assert empty_settlement.total_bills_pln == 0.0
    assert empty_settlement.total_due_pln == 0.0

#Piszemy test -> Test nie przechodzi -> Piszemy metodę -> Test przechodzi


def test_create_tenant_settlements():
    manager = Manager(Parameters()) #Tworzymy Managera

    # Trzech najemców
    apartment_settlement = manager.create_apartment_settlement("apart-polanka", 2025, 1)
    settlements = manager.create_tenant_settlements(apartment_settlement) #zwraca listę trzech rozliczeń

    assert len(settlements) == 3
    assert all(isinstance(s, TenantSettlement) for s in settlements)
    #Czy wszystkie trzy rozliczenia mają odpowiedni typ
    for settlement in settlements:
        assert settlement.apartment_settlement == "apart-polanka"
        #Czy rozliczenie dotyczy właściwego mieszkania
        assert settlement.year == 2025
        assert settlement.month == 1
        assert abs(settlement.bills_pln - 910.0 / 3) < 0.001

    # Jeden najemca
    manager.tenants = {"tenant-1": manager.tenants["tenant-1"]}
    #Zastąp słownik najemców nowym słownikiem, który zawiera tylko tenant-1, czyli Jana Nowaka
    settlements = manager.create_tenant_settlements(apartment_settlement)
    #teraz jest tylko jeden najemca
    assert len(settlements) == 1 #Czy powstało jedno rozliczenie
    assert settlements[0].tenant == "tenant-1" #Czy jest to tenant-1
    assert settlements[0].bills_pln == 910.0 #Czy jedyny najemca otrzymał całe 910 zł rachunków

    # Brak najemców
    manager.tenants = {} #pusty słownik najemców
    settlements = manager.create_tenant_settlements(apartment_settlement) #próbujemy utworzyć rozliczenia

    assert len(settlements) == 0 #czy lista wynikowa jest pusta


#Przypadek 1: jan, adam, ewa (303,33)
#Przypadek 2: jan (910)
#przypadek 3: - []