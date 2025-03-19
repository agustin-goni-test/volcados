import json
from typing import List

class Mensaje:
    def __init__(self, source: str, message: str):
        self.source = source
        self.message = message
    
    def to_dict(self):
        return {"source": self.source, "message": self.message}

class AdditionalMessages:
    def __init__(self, volcados=None):
        self.Volcados = volcados if volcados else []
    
    def to_dict(self):
        return {"Volcados": [v.to_dict() for v in self.Volcados]}

class Errors:
    def __init__(self, errors=None):
        self.Errors = errors if errors else []
    
    def to_dict(self):
        return {"Errors": [e.to_dict() for e in self.Errors]}

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
        self.Errors = Errors()
    
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
            "Errors": self.Errors.to_dict()
        }

class CuentaBancaria:
    def __init__(self, accountId=0, wasSuccessful=False, responseMessage=""):
        self.accountId = accountId
        self.wasSuccessful = wasSuccessful
        self.responseMessage = responseMessage
        self.AdditionalMessages = AdditionalMessages()
        self.Errors = Errors()
    
    def to_dict(self):
        return {
            "accountId": self.accountId,
            "wasSuccessful": self.wasSuccessful,
            "responseMessage": self.responseMessage,
            "AdditionalMessages": self.AdditionalMessages.to_dict(),
            "Errors": self.Errors.to_dict()
        }

class RepresentanteLegal:
    def __init__(self, wasSuccessful=False, responseMessage=""):
        self.wasSuccessful = wasSuccessful
        self.responseMessage = responseMessage
        self.AdditionalMessages = AdditionalMessages()
        self.Errors = Errors()
    
    def to_dict(self):
        return {
            "wasSuccessful": self.wasSuccessful,
            "responseMessage": self.responseMessage,
            "AdditionalMessages": self.AdditionalMessages.to_dict(),
            "Errors": self.Errors.to_dict()
        }

class Terminal:
    def __init__(self, terminal=0, collector="", billing_price="0.00", wasSuccessful=False, responseMessage=""):
        self.terminal = terminal
        self.collector = collector
        self.billing_price = billing_price
        self.wasSuccessful = wasSuccessful
        self.responseMessage = responseMessage
        self.AdditionalMessages = AdditionalMessages()
        self.Errors = Errors()
    
    def to_dict(self):
        return {
            "terminal": self.terminal,
            "collector": self.collector,
            "billing_price": self.billing_price,
            "wasSuccessful": self.wasSuccessful,
            "responseMessage": self.responseMessage,
            "AdditionalMessages": self.AdditionalMessages.to_dict(),
            "Errors": self.Errors.to_dict()
        }
    
    def to_json(self):
        return json.dumps(self.to_dict(), indent=4)

class Sucursal:
    def __init__(self, branch_id=0, entity_id=0, local_code=0, wasSuccessful=False, responseMessage="", num_terminals=0):
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
        self.Errors = Errors()
        self.Terminals = []  # Ensure the list starts empty
        if num_terminals > 0:
            for _ in range(num_terminals):
                self.add_terminal()
    
    def add_terminal(self, terminal=None):
        self.Terminals.append(terminal if terminal else Terminal())
    
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
            "Errors": self.Errors.to_dict(),
            "Terminals": [t.to_dict() for t in self.Terminals]
        }
    
    def to_json(self):
        return json.dumps(self.to_dict(), indent=4)
    
class ResultadoVolcado:
    def __init__(self, num_sucursales=0, num_terminals_per_sucursal=0, num_cuentas_bancarias=0, num_representantes_legales=0):
        self.ComercioCentral = ComercioCentral()
        self.CuentaBancaria = [CuentaBancaria() for _ in range(num_cuentas_bancarias)]
        self.RepresentanteLegal = [RepresentanteLegal() for _ in range(num_representantes_legales)]
        self.Sucursales = [Sucursal() for _ in range(num_sucursales)]
        for sucursal in self.Sucursales:
            for _ in range(num_terminals_per_sucursal):
                sucursal.add_terminal()
    
    def add_sucursal(self, sucursal=None):
        self.Sucursales.append(sucursal if sucursal else Sucursal())
    
    def add_cuenta_bancaria(self, cuenta=None):
        self.CuentaBancaria.append(cuenta if cuenta else CuentaBancaria())
    
    def add_representante_legal(self, representante=None):
        self.RepresentanteLegal.append(representante if representante else RepresentanteLegal())

    def add_terminal_to_sucursal(self, local_code, terminal=None):
        for sucursal in self.Sucursales:
            if sucursal.local_code == local_code:
                sucursal.add_terminal(terminal if terminal else Terminal())
                return True  # Terminal added successfully
        return False  # No matching sucursal found
    
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

####################################################################################
# Clasea para manejar resultados de volcados según necesidades especiales
####################################################################################


class ResultFuncion:
    def __init__(self, success: bool = False, source: str = "", message: str = ""):
        self.success = success
        self.source = source
        self.message = message

    def __repr__(self):
        return f"{self.__class__.__name__}(success={self.success}, source='{self.source}', message='{self.message}')"

class CommerceResult(ResultFuncion):
    def __init__(self, commerce_id: int = 0, entry: int = 0, agreement_id: int = 0, **kwargs):
        super().__init__(**kwargs)  # Pass common attributes to the base class
        self.commerce_id = commerce_id
        self.entry = entry
        self.agreement_id = agreement_id

class TicketResult(ResultFuncion):
    def __init__(self, date: str = "", time: str = "", **kwargs):
        super().__init__(**kwargs)  # Pass common attributes to the base class
        self.date = date
        self.time = time

class ServiceResult(ResultFuncion):
    def __init__(self, service_branch_id: str = "0", **kwargs):
        super().__init__(**kwargs)  # Pass common attributes to the base class
        self.service_branch_id = service_branch_id

class PaymentTypeResult(ResultFuncion):
    def __init__(self, payment_type_id: list[str] = None, **kwargs):
        super().__init__(**kwargs)  # Pass common attributes to the base class
        self.payment_type_id = payment_type_id if payment_type_id is not None else []

class TerminalResult(ResultFuncion):
    def __init__(self, terminal: int = 0, collector: str = "", billing_price = "", **kwargs):
        super().__init__(**kwargs)  # Pass common attributes to the base class
        self.terminal = terminal
        self.collector = collector
        self.billing_price = billing_price

class BranchResult(ResultFuncion):
    def __init__(self, branch_id: int = 0, entity_id: int = 0, local_code: int = 0, **kwargs):
        super().__init__(**kwargs)  # Pass common attributes to the base class
        self.branch_id = branch_id
        self.entity_id = entity_id
        self.local_code = local_code

class ContratoResult(ResultFuncion):
    def __init__(self, date: str = "", time: str = "", **kwargs):
        super().__init__(**kwargs)  # Pass common attributes to the base class
        self.date = date
        self.time = time

class BankAccountResult(ResultFuncion):
    def __init__(self, account_id: int = 0, **kwargs):
        super().__init__(**kwargs)  # Pass common attributes to the base class
        self.account_id = account_id

class IswitchBranchResult(ResultFuncion):
    def __init__(self, branchIswId: str = "", **kwargs):
        super().__init__(**kwargs)  # Pass common attributes to the base class
        self.branchIswId = branchIswId

class MonitorResult(ResultFuncion):
    def __init__(self, date: str = "", time: str = "", **kwargs):
        super().__init__(**kwargs)  # Pass common attributes to the base class
        self.date = date
        self.time = time

class RedPosResult(ResultFuncion):
    def __init__(self, ticket: str = "", **kwargs):
        super().__init__(**kwargs)  # Pass common attributes to the base class
        self.ticket = ticket