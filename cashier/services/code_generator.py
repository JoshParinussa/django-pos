"Code Generator Services module"
from datetime import datetime
from cashier.models import Invoice, Purchase, Income, Expense

class CodeGenerator:
    def generate(self, user, Model):
        if Model == Invoice :
            code = 'K'
            last_invoice = Invoice.objects.filter(created_at__startswith=datetime.now().date()).order_by('-created_at').first()
        elif Model == Purchase :
            code = 'B'
            last_invoice = Purchase.objects.filter(created_at__startswith=datetime.now().date()).order_by('-created_at').first()
        elif Model == Income :
            code = 'G'
            last_invoice = Income.objects.filter(created_at__startswith=datetime.now().date()).order_by('-created_at').first()
        elif Model == Expense :
            code = 'R'
            last_invoice = Expense.objects.filter(created_at__startswith=datetime.now().date()).order_by('-created_at').first()
        today_invoice = datetime.now().strftime("%d%m%Y")
        if not last_invoice:
            count = 1
            invoice_number = code + user.username.upper()[0] + str(user.id)[:5].upper() + today_invoice + str(count)
        else:
            count = int((last_invoice.invoice)[14:]) + 1
            invoice_number = code + user.username.upper()[0] + str(user.id)[:5].upper() + today_invoice + str(count)

        return invoice_number

code_generator = CodeGenerator()