class Product:
    def __init__(self, pid, name, price, qty):
        self.id = pid
        self.name = name
        self.price = price
        self.qty = qty

class Customer:
    def __init__(self, cid, name, contact):
        self.id = cid
        self.name = name
        self.contact = contact
        self.points = 0

class Invoice:
    def __init__(self, ino, customer):
        self.no = ino
        self.customer = customer
        self.items = []
        self.total = 0
    
    def add_item(self, product, qty):
        if qty <= product.qty:
            product.qty -= qty
            self.items.append(f"{product.name} x{qty}")
            self.total += product.price * qty
            return True
        return False

class POSSystem:
    def __init__(self):
        self.products = [
            Product(1, "Laptop", 1000, 10),
            Product(2, "Mouse", 25, 50),
            Product(3, "Keyboard", 80, 30)
        ]
        self.customers = [
            Customer(1, "John", "555-1234"),
            Customer(2, "Jane", "555-5678")
        ]
        self.invoices = []
        self.payments = []  # Payment history
    
    def show_products(self):
        print("\n=== Products ===")
        for p in self.products:
            print(f"{p.id}. {p.name} - ${p.price} (Stock: {p.qty})")
    
    def show_customers(self):
        print("\n=== Customers ===")
        for c in self.customers:
            print(f"{c.id}. {c.name} - {c.contact} (Points: {c.points})")
    
    def add_product(self):
        print("\n--- Add Product ---")
        name = input("Name: ")
        price = float(input("Price: "))
        qty = int(input("Quantity: "))
        pid = len(self.products) + 1
        self.products.append(Product(pid, name, price, qty))
        print(f"Added {name}")
    
    def add_customer(self):
        print("\n--- Add Customer ---")
        name = input("Name: ")
        contact = input("Contact: ")
        cid = len(self.customers) + 1
        self.customers.append(Customer(cid, name, contact))
        print(f"Added {name}")
    
    def create_sale(self):
        print("\n--- Create Sale ---")
        self.show_customers()
        cid = int(input("Customer ID: "))
        
        # Find customer
        customer = None
        for c in self.customers:
            if c.id == cid:
                customer = c
                break
        
        if not customer:
            print("Customer not found!")
            return
        
        # Create invoice
        invoice = Invoice(len(self.invoices) + 1, customer)
        
        # Add products
        while True:
            self.show_products()
            pid = int(input("Product ID (0 to finish): "))
            if pid == 0:
                break
            
            # Find product
            product = None
            for p in self.products:
                if p.id == pid:
                    product = p
                    break
            
            if not product:
                print("Product not found!")
                continue
            
            qty = int(input("Quantity: "))
            if invoice.add_item(product, qty):
                print(f"Added {product.name}")
            else:
                print("Not enough stock!")
        
        if invoice.items:
            self.invoices.append(invoice)
            print(f"\nInvoice #{invoice.no}")
            print(f"Customer: {customer.name}")
            print(f"Total: ${invoice.total}")
    
    def process_payment(self):
        if not self.invoices:
            print("\nNo invoices!")
            return
        
        print("\n--- Process Payment ---")
        for i, inv in enumerate(self.invoices):
            print(f"{i+1}. Invoice #{inv.no} - ${inv.total}")
        
        choice = int(input("Select invoice (1-" + str(len(self.invoices)) + "): ")) - 1
        
        if 0 <= choice < len(self.invoices):
            invoice = self.invoices[choice]
            
            # Add to payment history
            self.payments.append({
                'customer_id': invoice.customer.id,
                'invoice_no': invoice.no,
                'amount': invoice.total
            })
            
            # Add loyalty points
            invoice.customer.points += int(invoice.total / 10)
            
            print(f"\nPayment of ${invoice.total} processed!")
            print(f"{invoice.customer.name} earned {int(invoice.total/10)} points")
            
            # Remove paid invoice
            self.invoices.pop(choice)
        else:
            print("Invalid choice!")
    
    def show_payments(self):
        print("\n=== Payment History ===")
        if not self.payments:
            print("No payments yet")
            return
        
        for p in self.payments:
            print(f"Invoice #{p['invoice_no']} - Customer {p['customer_id']} - ${p['amount']}")


def main():
    pos = POSSystem()
    
    while True:
        print("\n" + "="*40)
        print("POINT OF SALE SYSTEM")
        print("="*40)
        print("1. Show Products")
        print("2. Show Customers")
        print("3. Add Product")
        print("4. Add Customer")
        print("5. Create Sale")
        print("6. Process Payment")
        print("7. Show Payment History")
        print("8. Exit")
        print("="*40)
        
        choice = input("\nEnter choice (1-8): ")
        
        if choice == "1":
            pos.show_products()
        elif choice == "2":
            pos.show_customers()
        elif choice == "3":
            pos.add_product()
        elif choice == "4":
            pos.add_customer()
        elif choice == "5":
            pos.create_sale()
        elif choice == "6":
            pos.process_payment()
        elif choice == "7":
            pos.show_payments()
        elif choice == "8":
            print("\nGoodbye!")
            break
        else:
            print("Invalid choice!")

if __name__ == "__main__":
    main()