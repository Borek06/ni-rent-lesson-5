from src.models import Apartment, Bill, Parameters, Tenant, Transfer, ApartmentSettlement, TenantSettlement
class Manager:
    def __init__(self, parameters: Parameters):
        #ustawienia zawierające ścieżki do plików JSON
        self.parameters = parameters #zapisujemy te ustawienia w obiekcie
        #pokazanie jak sie konstruuje scierzke

        self.apartments = {}
        self.tenants = {}
        self.transfers = []
        self.bills = []

        self.load_data()
        #Ta linijka wywołuje metodę load_data(), która wczytuje dane z plików

    def load_data(self):
        self.apartments = Apartment.from_json_file(self.parameters.apartments_json_path)
        self.tenants = Tenant.from_json_file(self.parameters.tenants_json_path)
        self.transfers = Transfer.from_json_file(self.parameters.transfers_json_path)
        self.bills = Bill.from_json_file(self.parameters.bills_json_path)

    def check_tenants_apartment_keys(self) -> bool:
        for tenant in self.tenants.values():
            if tenant.apartment not in self.apartments:
                return False
        return True

    # def get_apartment_costs(self, apartment_key: str, year: int, month: int):
    #     if apartment_key not in self.apartments: #brak mieszkania w mieszkaniach
    #         return None #mieszkanie nie istnieje
    #
    #     total = 0.0 #suma
    #
    #     for bill in self.bills: #przegladamy rachunki. bill = 0, 1, ...
    #         if (bill.apartment == apartment_key #
    #                 and bill.settlement_year == year
    #                 and bill.settlement_month == month):
    #             total += bill.amount_pln
    #
    #     return total

# self - wczytaj

    def get_apartment_costs(
            self, apartment_key: str, year: int | None = None, month: int | None = None): #rok i miesiac mozna pominac
        if apartment_key not in self.apartments:
            return None

        if month is not None and (month < 1 or month > 12):
            raise ValueError("Nieprawidłowy miesiąc")

        total = 0.0

        for bill in self.bills:
            if bill.apartment != apartment_key:
                continue

            if year is not None and bill.settlement_year != year:
                continue

            if month is not None and bill.settlement_month != month:
                continue

            total += bill.amount_pln

        return total

    def create_apartment_settlement(self, apartment_key: str, year: int, month: int):
        bills_total = self.get_apartment_costs(apartment_key, year, month)
        #Korzystamy z metody napisanej we wcześniejszym zadaniu, która sumuje rachunki mieszkania za dany miesiąc

        #Tworzymy gotowy obiekt rozliczenia, zawierający mieszkanie, rok, miesiąc oraz obliczone kwoty
        return ApartmentSettlement(
            apartment=apartment_key,
            year=year,
            month=month,
            total_rent_pln=0.0,
            total_bills_pln=bills_total,
            total_due_pln=bills_total
        )

    def create_tenant_settlements(self, apartment_settlement: ApartmentSettlement):
        tenants = [
            (key, tenant)    #słownik najemców
            for key, tenant in self.tenants.items() #pozwala pobierać ze słownika pary: klucz i wartość
            if tenant.apartment == apartment_settlement.apartment
        ] #odczytuje mieszkanie, którego dotyczy rozliczenie
        #Weź tylko najemców, którzy mieszkają w tym mieszkaniu

        if len(tenants) == 0:
            return [] #jeśli nikogo nie ma, zwraca pustą listę i kończy metodę

        bills_per_tenant = apartment_settlement.total_bills_pln / len(tenants)
        #kwota przypadająca na jedną osobę
        settlements = []

        for key, tenant in tenants:
            settlements.append(TenantSettlement( #settlements = [rozliczenie Jana, rozliczenie Adama, rozliczenie Ewy]
                tenant=key, #identyfikator najemcy, np. tenant-1
                apartment_settlement=apartment_settlement.apartment, #zapisujemy identyfikator mieszkania
                month=apartment_settlement.month,
                year=apartment_settlement.year,
                rent_pln=0.0,
                bills_pln=bills_per_tenant,
                total_due_pln=bills_per_tenant,
                balance_pln=0.0
            ))

        return settlements

