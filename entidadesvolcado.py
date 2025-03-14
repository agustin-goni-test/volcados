from typing import List, Optional
from pydantic import BaseModel, Field
import json

# Terminal class
class Terminal(BaseModel):
    commerceRut: str = ""
    branchCode: int = 0
    contractId: str = ""
    technology: int = 0
    ussdNumber: int = 0
    user: str = ""
    obs: str = ""
    additionalInfo: Optional[str] = None
    serviceId: int = 0
    sellerRut: str = ""

    def to_json(self) -> str:
        # Convert to dictionary first
        data_dict = self.model_dump()
        # Then convert the dictionary to a valid JSON string with double quotes
        return json.dumps(data_dict, ensure_ascii=False, indent=2)

# Sucursal class
class Sucursal(BaseModel):
    address: str = ""
    addressNumber: str = ""
    businessName: str = ""
    cityId: int = 0
    commerceRut: str = ""
    email: str = ""
    fanName: str = ""
    idMcc: int = 0
    mobilePhoneNumber: str = ""
    name: str = ""
    regionId: int = 0
    townOrVillage: str = ""
    webSite: str = ""
    mantisaBill: str = ""
    dvBill: str = ""
    bankAccount: str = ""
    mantisaHolder: str = ""
    integrationType: str = ""
    user: str = ""
    emailContacto: str = ""
    merchantType: int = 0
    commerceRepresentativeLegalName: str = ""
    commerceRepresentativeLegalRut: str = ""
    Terminales: List[Terminal] = Field(default_factory=list)

    def add_terminal(self, terminal: Terminal):
        self.Terminales.append(terminal)
    
    def get_terminales(self) -> List[Terminal]:
        return self.Terminales
    
    def get_terminal_by_index(self, index: int) -> Optional[Terminal]:
        return self.Terminales[index] if 0 <= index < len(self.Terminales) else None
    
    def to_json(self) -> str:
        # Convert to dictionary first
        data_dict = self.model_dump()
        # Then convert the dictionary to a valid JSON string with double quotes
        return json.dumps(data_dict, ensure_ascii=False, indent=2)

# CuentaBancaria class
class CuentaBancaria(BaseModel):
    commerceRut: str = ""
    holderRut: str = ""
    holderName: str = ""
    accountTypeCode: str = ""
    bankAccount: str = ""
    bankCode: int = 0
    holderMail: str = ""

    def to_json(self) -> str:
        # Convert to dictionary first
        data_dict = self.model_dump()
        # Then convert the dictionary to a valid JSON string with double quotes
        return json.dumps(data_dict, ensure_ascii=False, indent=2)

# RepresentanteLegal class
class RepresentanteLegal(BaseModel):
    commerceRut: str = ""
    legalRepresentativeRut: str = ""
    email: str = ""
    name: str = ""
    lastName: str = ""
    motherLastName: str = ""
    mobilePhoneNumber: str = ""
    sign: bool = False
    isThird: bool = False
    isSignAllowed: bool = False

    def to_json(self) -> str:
        # Convert to dictionary first
        data_dict = self.model_dump()
        # Then convert the dictionary to a valid JSON string with double quotes
        return json.dumps(data_dict, ensure_ascii=False, indent=2)

# ComercioCentral class
class ComercioCentral(BaseModel):
    commerceRut: str = ""
    businessName: str = ""
    email: str = ""
    emailPayment: str = ""
    fanName: str = ""
    name: str = ""
    lastName: str = ""
    mothersLastName: str = ""
    mobilePhoneNumber: str = ""
    address: str = ""
    addressNumber: str = ""
    cityId: int = 0
    regionId: int = 0
    sellerCode: str = ""
    businessLine: int = 0
    townOrVillage: str = ""
    obs: str = ""

    def to_json(self) -> str:
        # Convert to dictionary first
        data_dict = self.model_dump()
        # Then convert the dictionary to a valid JSON string with double quotes
        return json.dumps(data_dict, ensure_ascii=False, indent=2)

# Main Onboarding Structure
class EntidadesVolcado(BaseModel):
    comercioCentral: ComercioCentral = Field(default_factory=ComercioCentral)
    Sucursales: List[Sucursal] = Field(default_factory=list)
    CuentasBancarias: List[CuentaBancaria] = Field(default_factory=list)
    RepresentantesLegales: List[RepresentanteLegal] = Field(default_factory=list)

    def add_sucursal(self, sucursal: Sucursal):
        self.Sucursales.append(sucursal)
    
    def add_cuenta_bancaria(self, cuenta: CuentaBancaria):
        self.CuentasBancarias.append(cuenta)
    
    def add_representante_legal(self, representante: RepresentanteLegal):
        self.RepresentantesLegales.append(representante)
    
    def get_sucursales(self) -> List[Sucursal]:
        return self.Sucursales
    
    def get_cuentas_bancarias(self) -> List[CuentaBancaria]:
        return self.CuentasBancarias
    
    def get_cuenta_bancaria_by_account(self, bank_account: str) -> Optional[CuentaBancaria]:
        return next((cb for cb in self.CuentasBancarias if cb.bankAccount == bank_account), None)
    
    def get_representantes_legales(self) -> List[RepresentanteLegal]:
        return self.RepresentantesLegales
    
    def get_sucursal_by_index(self, index: int) -> Optional[Sucursal]:
        return self.Sucursales[index] if 0 <= index < len(self.Sucursales) else None
    
    def to_json(self) -> str:
        # Convert to dictionary first
        data_dict = self.model_dump()
        # Then convert the dictionary to a valid JSON string with double quotes
        return json.dumps(data_dict, ensure_ascii=False, indent=2)

    @classmethod
    def from_json(cls, json_data: str):
        # return cls.parse_raw(json_data)
        return cls.model_validate(json_data)

# Example Usage
# if __name__ == "__main__":
#     onboarding = EntidadesVolcado()
    
#     # Adding a new RepresentanteLegal
#     rep_legal = RepresentanteLegal(name="Carlos", lastName="Fernández", commerceRut="12345678-9")
#     onboarding.add_representante_legal(rep_legal)
    
#     # Retrieving and using a CuentaBancaria
#     cuenta = CuentaBancaria(bankAccount="123456789", holderName="Ana Martínez")
#     onboarding.add_cuenta_bancaria(cuenta)
#     retrieved_cuenta = onboarding.get_cuenta_bancaria_by_account("123456789")
#     if retrieved_cuenta:
#         print(f"Found account for: {retrieved_cuenta.holderName}")
    
#     # Adding a Terminal to a specific Sucursal
#     sucursal = Sucursal(name="Sucursal 1", commerceRut="12345678-9")
#     onboarding.add_sucursal(sucursal)
#     terminal = Terminal(branchCode="SC001", contractId="CTR-0001")
#     sucursal.add_terminal(terminal)
    
#     # Modifying a specific Sucursal
#     retrieved_sucursal = onboarding.get_sucursal_by_index(0)
#     if retrieved_sucursal:
#         retrieved_sucursal.businessName = "Updated Sucursal Name"
    
#     print(onboarding.to_json())
