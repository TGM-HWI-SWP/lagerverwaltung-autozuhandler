class FilterService:
    def __init__(self, car_service, part_service, customer_service, customer_lookup_fn):
        self.car_service = car_service
        self.part_service = part_service
        self.customer_service = customer_service
        self.customer_lookup_fn = customer_lookup_fn

    def filter_cars(self, search_term, brand_filter, status_filter):
        filtered = self.car_service.list_all()
        term = str(search_term).strip().lower()

        if term:
            filtered = [
                car for car in filtered
                if term in car.id.lower()
                or term in car.brand.lower()
                or term in car.model.lower()
                or term in car.fuel.lower()
                or term in car.color.lower()
                or term in car.status.lower()
                or term in self.customer_lookup_fn(car.customer_id).lower()
            ]

        if brand_filter != "Alle":
            filtered = [car for car in filtered if car.brand == brand_filter]

        if status_filter != "Alle":
            filtered = [car for car in filtered if car.status == status_filter]

        return filtered

    def filter_parts(self, search_term, category_filter, status_filter):
        filtered = self.part_service.list_all()
        term = str(search_term).strip().lower()

        if term:
            filtered = [
                part for part in filtered
                if term in part.id.lower()
                or term in part.name.lower()
                or term in part.category.lower()
                or term in part.brand.lower()
                or term in part.status.lower()
            ]

        if category_filter != "Alle":
            filtered = [part for part in filtered if part.category == category_filter]

        if status_filter != "Alle":
            filtered = [part for part in filtered if part.status == status_filter]

        return filtered

    def filter_customers(self, search_term):
        filtered = self.customer_service.list_all()
        term = str(search_term).strip().lower()

        if term:
            filtered = [
                customer for customer in filtered
                if term in customer.id.lower()
                or term in customer.name.lower()
                or term in customer.phone.lower()
                or term in customer.email.lower()
                or term in customer.address.lower()
            ]

        return filtered