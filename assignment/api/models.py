from django.db import models

# Create your models here.
class Mappings(models.Model):
    batchReference=models.TextField()
    transactionReference=models.TextField()
    buyerName=models.TextField()
    supplierName=models.TextField()
    invoiceReference=models.TextField()
    poReference=models.TextField()
    invoiceDate=models.TextField()
    invoiceAmount=models.TextField()
    invoiceCurrency=models.TextField()
    maturityDate=models.TextField()
    paymentDate=models.TextField()
    tenor=models.TextField()
    netAmount=models.TextField()
    grossAmount=models.TextField()
    discountAmount=models.TextField()
    adjustmentAmount=models.TextField()
    adjustmentReasonCode=models.TextField()
    paymentTerm=models.TextField()
    status=models.TextField()
    notes=models.TextField()
