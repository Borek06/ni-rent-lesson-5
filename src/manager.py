from src.models import Apartment, Bill, Parameters, Tenant, Transfer


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

    def get_apartment_costs(self, apartment_key: str, year: int, month: int):
        if apartment_key not in self.apartments: #brak mieszkania w mieszkaniach
            return None #mieszkanie nie istnieje

        total = 0.0 #suma

        for bill in self.bills: #przegladamy rachunki. bill = 0, 1, ...
            if (bill.apartment == apartment_key #
                    and bill.settlement_year == year
                    and bill.settlement_month == month):
                total += bill.amount_pln

        return total

#self - wczytaj