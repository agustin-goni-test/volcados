import json
from typing import List, Dict, Any

# Esta clase maneja todo lo relacionados al resultado de los volcados en cada
# una de sus entidades. La idea es mantener una estructura que tenga
# las características de responseV2.json

class VolcadoItem:
    def __init__(self, source: str, message: str):
        self.source = source
        self.message = message

    def __repr__(self):
        return f"VolcadoItem(source={self.source}, message={self.message})"

class ErrorItem:
    def __init__(self, source: str, message: str):
        self.source = source
        self.message = message

    def __repr__(self):
        return f"ErrorItem(source={self.source}, message={self.message})"

class EntityBase:
    def __init__(self, data: Dict[str, Any]):
        self.was_successful = data.get("wasSuccessful", False)
        self.response_message = data.get("responseMessage", "")
        self.additional_messages = [VolcadoItem(**msg) for msg in data.get("AdditionalMessages", {}).get("Volcados", [])]
        self.errors = [ErrorItem(**err) for err in data.get("Errors", [])]

class ComercioCentral(EntityBase):
    def __init__(self, data: Dict[str, Any]):
        super().__init__(data)
        self.entry = data.get("entry")
        self.commerce_id = data.get("commerce_id")
        self.agreement_id = data.get("agreement_id")
        self.contrato_date = data.get("ContratoDateAndTime")
        self.ticket_date = data.get("ComercioTicketDateAndTime")

class Terminal(EntityBase):
    def __init__(self, data: Dict[str, Any]):
        super().__init__(data)
        self.terminal = data.get("terminal")
        self.collector = data.get("collector")
        self.billing_price = data.get("billing_price")

class Sucursal(EntityBase):
    def __init__(self, data: Dict[str, Any]):
        super().__init__(data)
        self.branch_id = data.get("branch_id")
        self.entity_id = data.get("entity_id")
        self.local_code = data.get("local_code")
        self.service_branch_id = data.get("service_branch_id")
        self.payment_type_ids = data.get("paymentTypeIds", [])
        self.branch_isw_id = data.get("branchIswId")
        self.monitor_date = data.get("MonitorPlusDateAndTime")
        self.terminals = [Terminal(term) for term in data.get("Terminals", [])]

class CuentaBancaria(EntityBase):
    def __init__(self, data: Dict[str, Any]):
        super().__init__(data)
        self.account_id = data.get("accountId")

class RepresentanteLegal(EntityBase):
    def __init__(self, data: Dict[str, Any]):
        super().__init__(data)

class ResultadoVolcado:
    def __init__(self, json_data: str):
        data = json.loads(json_data)
        self.comercio_central = ComercioCentral(data.get("ComercioCentral", {}))
        self.sucursales = [Sucursal(suc) for suc in data.get("Sucursales", [])]
        self.cuentas_bancarias = [CuentaBancaria(cb) for cb in data.get("CuentaBancaria", [])]
        self.representantes_legales = [RepresentanteLegal(rep) for rep in data.get("RepresentanteLegal", [])]

    def __repr__(self):
        return (f"ResultadoVolcado(\n  ComercioCentral={self.comercio_central},\n  Sucursales={self.sucursales},\n  CuentasBancarias={self.cuentas_bancarias},\n  RepresentantesLegales={self.representantes_legales}\n)")

# Example usage:
# json_str = '{...}'  # Your JSON string here
# resultado = ResultadoVolcado(json_str)
# print(resultado)
