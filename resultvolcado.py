import json
from typing import List

class AdditionalMessages:
    def __init__(self, volcados=None):
        self.Volcados = volcados if volcados else []
    
    def to_dict(self):
        return {"Volcados": self.Volcados}

class ComercioCentral:
    def __init__(self, entry=0, commerce_id=0, agreement_id=0, wasSuccessful=False, responseMessage=""):
        self.entry = entry
        self.commerce_id = commerce_id
        self.agreement_id = agreement_id
        self.wasSuccessful = wasSuccessful
        self.responseMessage = responseMessage
        self.ContratoDateAndTime = ""
        self.ComercioTicketDateAndTime = ""
        self.AdditionalMessages = AdditionalMessages()
        self.Errors = []
    
    def to_dict(self):
        return {
            "entry": self.entry,
            "commerce_id": self.commerce_id,
            "agreement_id": self.agreement_id,
            "wasSuccessful": self.wasSuccessful,
            "responseMessage": self.responseMessage,
            "ContratoDateAndTime": self.ContratoDateAndTime,
            "ComercioTicketDateAndTime": self.ComercioTicketDateAndTime,
            "AdditionalMessages": self.AdditionalMessages.to_dict(),
            "Errors": self.Errors
        }

class CuentaBancaria:
    def __init__(self, accountId=0, wasSuccessful=False, responseMessage=""):
        self.accountId = accountId
        self.wasSuccessful = wasSuccessful
        self.responseMessage = responseMessage
        self.AdditionalMessages = AdditionalMessages()
        self.Errors = []
    
    def to_dict(self):
        return {
            "accountId": self.accountId,
            "wasSuccessful": self.wasSuccessful,
            "responseMessage": self.responseMessage,
            "AdditionalMessages": self.AdditionalMessages.to_dict(),
            "Errors": self.Errors
        }

class RepresentanteLegal:
    def __init__(self, wasSuccessful=False, responseMessage=""):
        self.wasSuccessful = wasSuccessful
        self.responseMessage = responseMessage
        self.AdditionalMessages = AdditionalMessages()
        self.Errors = []
    
    def to_dict(self):
        return {
            "wasSuccessful": self.wasSuccessful,
            "responseMessage": self.responseMessage,
            "AdditionalMessages": self.AdditionalMessages.to_dict(),
            "Errors": self.Errors
        }

class Terminal:
    def __init__(self, terminal=0, collector="", billing_price="0.00", wasSuccessful=False, responseMessage=""):
        self.terminal = terminal
        self.collector = collector
        self.billing_price = billing_price
        self.wasSuccessful = wasSuccessful
        self.responseMessage = responseMessage
        self.AdditionalMessages = AdditionalMessages()
        self.Errors = []
    
    def to_dict(self):
        return {
            "terminal": self.terminal,
            "collector": self.collector,
            "billing_price": self.billing_price,
            "wasSuccessful": self.wasSuccessful,
            "responseMessage": self.responseMessage,
            "AdditionalMessages": self.AdditionalMessages.to_dict(),
            "Errors": self.Errors
        }

class Sucursal:
    def __init__(self, branch_id=0, entity_id=0, local_code=0, wasSuccessful=False, responseMessage="", num_terminals=1):
        self.branch_id = branch_id
        self.entity_id = entity_id
        self.local_code = local_code
        self.wasSuccessful = wasSuccessful
        self.responseMessage = responseMessage
        self.service_branch_id = 0
        self.paymentTypeIds = []
        self.branchIswId = ""
        self.MonitorPlusDateAndTime = ""
        self.AdditionalMessages = AdditionalMessages()
        self.Errors = []
        self.Terminals = [Terminal() for _ in range(num_terminals)]
    
    def to_dict(self):
        return {
            "branch_id": self.branch_id,
            "entity_id": self.entity_id,
            "local_code": self.local_code,
            "wasSuccessful": self.wasSuccessful,
            "responseMessage": self.responseMessage,
            "service_branch_id": self.service_branch_id,
            "paymentTypeIds": self.paymentTypeIds,
            "branchIswId": self.branchIswId,
            "MonitorPlusDateAndTime": self.MonitorPlusDateAndTime,
            "AdditionalMessages": self.AdditionalMessages.to_dict(),
            "Errors": self.Errors,
            "Terminals": [t.to_dict() for t in self.Terminals]
        }

class ResultadoVolcado:
    def __init__(self, num_sucursales=1, num_terminals_per_sucursal=1):
        self.ComercioCentral = ComercioCentral()
        self.CuentaBancaria = [CuentaBancaria()]
        self.RepresentanteLegal = [RepresentanteLegal()]
        self.Sucursales = [Sucursal(num_terminals=num_terminals_per_sucursal) for _ in range(num_sucursales)]
    
    def to_dict(self):
        return {
            "ComercioCentral": self.ComercioCentral.to_dict(),
            "CuentaBancaria": [cb.to_dict() for cb in self.CuentaBancaria],
            "RepresentanteLegal": [rl.to_dict() for rl in self.RepresentanteLegal],
            "Sucursales": [s.to_dict() for s in self.Sucursales]
        }
    
    def to_json(self):
        return json.dumps(self.to_dict(), indent=4, ensure_ascii=False)
    
    def __str__(self):
        return self.to_json()




class ResultFuncion:
    def __init__(self, success: bool, source: str, message: str):
        self.success = success
        self.source = source
        self.message = message

    def __repr__(self):
        return f"{self.__class__.__name__}(success={self.success}, source='{self.source}', message='{self.message}')"

class CommerceResult(BaseResult):
    def __init__(self, commerce_id: str, entry: str, agreement_id: str, **kwargs):
        super().__init__(**kwargs)  # Pass common attributes to the base class
        self.commerce_id = commerce_id
        self.entry = entry
        self.agreement_id = agreement_id

