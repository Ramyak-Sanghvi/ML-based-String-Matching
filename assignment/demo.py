a=["BATCH_REF", "TXN_REF", "BUYER", "SUPPLIER", "INV_REF", "PO_REF", "INV_DATE", "INV_AMT", "INV_CCY", "MAT_DATE", "PAY_DATE", "TENOR", "NET_AMT", "GROSS_AMT", "DISC_AMT", "ADJUST_AMT", "ADJUST_REASON_CODE", "PAY_TERM", "STATUS", "NOTE"]
b=["batchNum", "txnNum", "buyer", "supplier", "invNum", "poNum", "invDt", "invAmt", "invCcy", "matDt", "payDueDt", "tenor", "netAmt", "grossAmt", "discAmt", "adjustAmt", "adjustReason", "payTerm", "status", "notes"]
c=["BatchNumber", "TransactionNumber", "Buyer", "Supplier", "InvoiceNumber", "PONumber", "InvoiceDate", "InvoiceAmount", "InvoiceCurrency", "MaturityDate", "PaymentDate", "Tenor", "NetAmt", "GrossAmt", "DiscountAmt", "AdjustmAmt", "AdjustReasonCode", "PayTerm", "Status", "Notes"]
dl=[ "Batch #", "Transaction #", "Buyer Name", "Supplier Name", "Inv #", "PO #", 
"Invoice Date", "Invoice Amount", "Invoice Currency", "Maturity Date", "Payment Date", "Tenor", "Net Amount", "Gross Amount", "Discount Amount", "Adjustment Amount", "Adjustment Reason Code", "Payment Term", "Status", "Notes"]
t=[ "batchReference", "transactionReference", "buyerName", "supplierName", 
"invoiceReference", "poReference", "invoiceDate", "invoiceAmount", "invoiceCurrency", 
"maturityDate", "paymentDate", "tenor", "netAmount", "grossAmount", "discountAmount", 
"adjustmentAmount", "adjustmentReasonCode", "paymentTerm", "status", "notes"]

d={}
for i in range(len(t)):
    d[t[i]]= [a[i].lower(),b[i].lower(),c[i].lower(),t[i].lower(),dl[i].lower()]

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics import pairwise_kernels
from numpy import max,argmax

import re
def ngrams(string, n=1):
    string = re.sub(r'[,-./]|\sBD',r'', string)
    ngrams = zip(*[string[i:] for i in range(n)])
    return [''.join(ngram) for ngram in ngrams]

vec = CountVectorizer(analyzer=ngrams)

k=[]
for i in d:
    vec.fit(d[i])
    l=[]
    print(i)
    for j in dl:
        c=pairwise_kernels(vec.transform([j.lower()]),
                    vec.transform(d[i]),
                    metric='cosine')
        l.append(round(max(c),3))
    print(l)
    k.append(argmax(l))
print(k)
