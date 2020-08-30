from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Mappings
from rest_framework.renderers import JSONRenderer
import json

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics import pairwise_kernels
from numpy import max,argmax,mean

import re
def ngrams(string, n=1):
    string = re.sub(r'[,-./]|\sBD',r'', string)
    ngrams = zip(*[string[i:] for i in range(n)])
    return [''.join(ngram) for ngram in ngrams]

def dataInsertionCode():
    a=["BATCH_REF", "TXN_REF", "BUYER", "SUPPLIER", "INV_REF", "PO_REF", "INV_DATE", "INV_AMT", "INV_CCY", "MAT_DATE", "PAY_DATE", "TENOR", "NET_AMT", "GROSS_AMT", "DISC_AMT", "ADJUST_AMT", "ADJUST_REASON_CODE", "PAY_TERM", "STATUS", "NOTE"]
    b=["batchNum", "txnNum", "buyer", "supplier", "invNum", "poNum", "invDt", "invAmt", "invCcy", "matDt", "payDueDt", "tenor", "netAmt", "grossAmt", "discAmt", "adjustAmt", "adjustReason", "payTerm", "status", "notes"]
    c=["BatchNumber", "TransactionNumber", "Buyer", "Supplier", "InvoiceNumber", "PONumber", "InvoiceDate", "InvoiceAmount", "InvoiceCurrency", "MaturityDate", "PaymentDate", "Tenor", "NetAmt", "GrossAmt", "DiscountAmt", "AdjustmAmt", "AdjustReasonCode", "PayTerm", "Status", "Notes"]
    dl=[ "Batch #", "Transaction #", "Buyer Name", "Supplier Name", "Inv #", "PO #", 
    "Invoice Date", "Invoice Amount", "Invoice Currency", "Maturity Date", "Payment Date", "Tenor", "Net Amount", "Gross Amount", "Discount Amount", "Adjustment Amount", "Adjustment Reason Code", "Payment Term", "Status", "Notes"]
    t=[ "batchReference", "transactionReference", "buyerName", "supplierName", 
    "invoiceReference", "poReference", "invoiceDate", "invoiceAmount", "invoiceCurrency", 
    "maturityDate", "paymentDate", "tenor", "netAmount", "grossAmount", "discountAmount", 
    "adjustmentAmount", "adjustmentReasonCode", "paymentTerm", "status", "notes"]
    mappings=Mappings()
    for i in range(len(t)):
        setattr(mappings, t[i],json.dumps( [a[i].lower(),b[i].lower(),c[i].lower(),t[i].lower(),dl[i].lower()] ))
        print(getattr(mappings,t[i]))
    mappings.save()


t=[ "batchReference", "transactionReference", "buyerName", "supplierName", 
"invoiceReference", "poReference", "invoiceDate", "invoiceAmount", "invoiceCurrency", 
"maturityDate", "paymentDate", "tenor", "netAmount", "grossAmount", "discountAmount", 
"adjustmentAmount", "adjustmentReasonCode", "paymentTerm", "status", "notes"]


jsonDec = json.decoder.JSONDecoder()
vec = CountVectorizer(analyzer=ngrams)

# Create your views here.
  
class TrainFormatMatch(APIView):
    renderer_classes = [JSONRenderer]
    def post(self, request):
        try:
            data=json.loads(request.body)
            #data insertion code
            #dataInsertionCode()
            k=[]
            s=[]
            mappings=Mappings.objects.get(id=1)
            for i in range(len(t)):
                target=jsonDec.decode(getattr(mappings,t[i]))
                print(target)
                vec.fit(target)
                l=[]
                for j in data["source"]["formatFields"]:
                    c=pairwise_kernels(vec.transform([j.lower()]),vec.transform(target),metric='cosine')
                    l.append(round(max(c),3))
                n=argmax(l)
                print(l)
                if n not in k:
                    s.append(round(max(l),3)*100)
                    k.append(n)
                else:
                    z=l[n+1:]
                    s.append(round(max(z),3)*100)
                    k.append(argmax(z)+len(l[0:n+1]))
            print(k)
            
            """
            for i in range(len(t)):
                target=jsonDec.decode(getattr(mappings,t[i]))
                value=data["source"]["formatFields"][i]
                if value not in target:
                    target.append(value.lower())
                setattr(mappings, t[i],json.dumps( target ))
                print(getattr(mappings,t[i]))
            mappings.save()
            """
            
            return Response({
                "sourceformatName":data["source"]["formatName"],
                "targetformatName":data["target"]["formatName"],
                "overallConfidence":mean(s),
                 "mappings": [
                    {"sourceField" : data["source"]["formatFields"][k[0]],"targetField" : "batchReference","confidence" : s[0]},
                    {"sourceField" : data["source"]["formatFields"][k[1]],"targetField" : "transactionReference", "confidence" : s[1]},
                    {"sourceField" : data["source"]["formatFields"][k[2]],"targetField" : "buyerName", "confidence" : s[2]},
                    {"sourceField" : data["source"]["formatFields"][k[3]],"targetField" : "supplierName", "confidence" : s[3]},
                    {"sourceField" : data["source"]["formatFields"][k[4]],"targetField" : "invoiceReference", "confidence" : s[4]},
                    {"sourceField" : data["source"]["formatFields"][k[5]],"targetField" : "poReference", "confidence" : s[5]},
                    {"sourceField" : data["source"]["formatFields"][k[6]],"targetField" : "invoiceDate", "confidence" : s[6]},
                    {"sourceField" : data["source"]["formatFields"][k[7]],"targetField" : "invoiceAmount", "confidence" : s[7]},
                    {"sourceField" : data["source"]["formatFields"][k[8]],"targetField" : "invoiceCurrency", "confidence" : s[8]},
                    {"sourceField" : data["source"]["formatFields"][k[9]],"targetField" : "maturityDate", "confidence" : s[9]},
                    {"sourceField" : data["source"]["formatFields"][k[10]],"targetField" : "paymentDate", "confidence" : s[10]},
                    {"sourceField" : data["source"]["formatFields"][k[11]],"targetField" : "tenor", "confidence" : s[11]},
                    {"sourceField" : data["source"]["formatFields"][k[12]],"targetField" : "netAmount", "confidence" : s[12]},
                    {"sourceField" : data["source"]["formatFields"][k[13]],"targetField" : "grossAmount", "confidence" : s[13]},
                    {"sourceField" : data["source"]["formatFields"][k[14]],"targetField" : "discountAmount", "confidence" : s[14]},
                    {"sourceField" : data["source"]["formatFields"][k[15]],"targetField" : "adjustmentAmount", "confidence" : s[15]},
                    {"sourceField" : data["source"]["formatFields"][k[16]],"targetField" : "adjustmentReasonCode", "confidence" : s[16]},
                    {"sourceField" : data["source"]["formatFields"][k[17]],"targetField" : "paymentTerm", "confidence" : s[17]},
                    {"sourceField" : data["source"]["formatFields"][k[18]],"targetField" : "status", "confidence" : s[18]},
                    {"sourceField" : data["source"]["formatFields"][k[19]],"targetField" : "notes", "confidence" : s[19]},
                ]
            })
        except Exception as ex:
            print(ex)

class TrainFormatLearn(APIView):
    renderer_classes = [JSONRenderer]
    def post(self, request):
        try:
            data=json.loads(request.body)

            mappings=Mappings.objects.get(id=1)

            for i in data["mappings"]:
                target=jsonDec.decode(getattr(mappings,i["targetField"]))
                target.append(i["sourceField"].lower())
                setattr(mappings, i["targetField"],json.dumps( target ))
                print(getattr(mappings,i["targetField"]))
            mappings.save()
            
            
            return Response({
                "sourceformatName": data["source"]["formatName"],
                "targetformatName": data["target"]["formatName"],
                "Message" : "Learned the mappings"
            })
        except Exception as ex:
            print(ex)

class FormatMatch(APIView):
    renderer_classes = [JSONRenderer]
    def post(self, request):
        try:
            data=json.loads(request.body)
            #data insertion code
            #dataInsertionCode()
            k=[]
            s=[]
            mappings=Mappings.objects.get(id=1)
            for i in range(len(t)):
                target=jsonDec.decode(getattr(mappings,t[i]))
                print(target)
                vec.fit(target)
                l=[]
                for j in data["source"]["formatFields"]:
                    c=pairwise_kernels(vec.transform([j.lower()]),vec.transform(target),metric='cosine')
                    l.append(round(max(c),3))
                n=argmax(l)
                print(l)
                if n not in k:
                    s.append(round(max(l),3)*100)
                    k.append(n)
                else:
                    z=l[n+1:]
                    s.append(round(max(z),3)*100)
                    k.append(argmax(z)+len(l[0:n+1]))
            print(k)
            
            
            return Response({
                "sourceformatName":data["source"]["formatName"],
                "targetformatName":data["target"]["formatName"],
                "overallConfidence":mean(s),
                 "mappings": [
                    {"sourceField" : data["source"]["formatFields"][k[0]],"targetField" : "batchReference","confidence" : s[0]},
                    {"sourceField" : data["source"]["formatFields"][k[1]],"targetField" : "transactionReference", "confidence" : s[1]},
                    {"sourceField" : data["source"]["formatFields"][k[2]],"targetField" : "buyerName", "confidence" : s[2]},
                    {"sourceField" : data["source"]["formatFields"][k[3]],"targetField" : "supplierName", "confidence" : s[3]},
                    {"sourceField" : data["source"]["formatFields"][k[4]],"targetField" : "invoiceReference", "confidence" : s[4]},
                    {"sourceField" : data["source"]["formatFields"][k[5]],"targetField" : "poReference", "confidence" : s[5]},
                    {"sourceField" : data["source"]["formatFields"][k[6]],"targetField" : "invoiceDate", "confidence" : s[6]},
                    {"sourceField" : data["source"]["formatFields"][k[7]],"targetField" : "invoiceAmount", "confidence" : s[7]},
                    {"sourceField" : data["source"]["formatFields"][k[8]],"targetField" : "invoiceCurrency", "confidence" : s[8]},
                    {"sourceField" : data["source"]["formatFields"][k[9]],"targetField" : "maturityDate", "confidence" : s[9]},
                    {"sourceField" : data["source"]["formatFields"][k[10]],"targetField" : "paymentDate", "confidence" : s[10]},
                    {"sourceField" : data["source"]["formatFields"][k[11]],"targetField" : "tenor", "confidence" : s[11]},
                    {"sourceField" : data["source"]["formatFields"][k[12]],"targetField" : "netAmount", "confidence" : s[12]},
                    {"sourceField" : data["source"]["formatFields"][k[13]],"targetField" : "grossAmount", "confidence" : s[13]},
                    {"sourceField" : data["source"]["formatFields"][k[14]],"targetField" : "discountAmount", "confidence" : s[14]},
                    {"sourceField" : data["source"]["formatFields"][k[15]],"targetField" : "adjustmentAmount", "confidence" : s[15]},
                    {"sourceField" : data["source"]["formatFields"][k[16]],"targetField" : "adjustmentReasonCode", "confidence" : s[16]},
                    {"sourceField" : data["source"]["formatFields"][k[17]],"targetField" : "paymentTerm", "confidence" : s[17]},
                    {"sourceField" : data["source"]["formatFields"][k[18]],"targetField" : "status", "confidence" : s[18]},
                    {"sourceField" : data["source"]["formatFields"][k[19]],"targetField" : "notes", "confidence" : s[19]},
                ]
            })
        except Exception as ex:
            print(ex)