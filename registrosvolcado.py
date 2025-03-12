from pydantic import BaseModel, Field, EmailStr, conint, constr, field_validator
from typing import Optional
from inputvolcados import VolcadoComercio
from datetime import date, datetime
import json

# Definir una validación para RUT
RUT_PATTERN = r"^[0-9]+-[0-9kK]{1}$"
ADDRESS_NUMBER_PATTERN = r"^[0-9]{1,6}$"

# Clase para manejar la estructura para el endpoint de representante legal
# Incluye validaciones
class RepresentativeRegister(BaseModel):
    commerceRut: str = Field(..., pattern=r"^[0-9]+-[0-9kK]{1}$")
    legalRepresentativeRut: str = Field(..., pattern=r"^[0-9]+-[0-9kK]{1}$")
    name: str
    lastName: str
    motherLastName: str
    email: EmailStr
    mobilePhoneNumber: conint(ge=0)  # Positive or zero integer
    sign: constr(pattern=r"^true$|^false$", min_length=4, max_length=5)
    isThird: constr(pattern=r"^true$|^false$", min_length=4, max_length=5)
    isSignAllowed: constr(pattern=r"^true$|^false$", min_length=4, max_length=5)
    commerceId: conint(ge=0)  # Positive or zero integer

    # Optional: You can add custom validation functions as needed
    @field_validator("commerceRut", "legalRepresentativeRut")
    def validate_rut(cls, value):
        if not value:  # Add any custom validation logic here
            raise ValueError("Invalid RUT")
        return value

    class Config:
        # Enforce strict validation of inputs
        str_strip_whitespace = True
        str_min_length = 1

    # Method to convert the instance to JSON
    def to_json(self):
        return self.json()  # Pydantic's built-in method to serialize to JSON string

    # Method to convert the class from a JSON string
    @classmethod
    def from_json(cls, json_data: str):
        return cls.parse_raw(json_data)  # Pydantic's built-in method to parse a JSON string into an instance

    @classmethod
    def from_volcado_comercio(cls, volcado: VolcadoComercio):
        comercio = volcado.comercio
        representante = comercio.legal_representatives[0]

        return cls(
            commerceRut=comercio.commerce_rut,
            legalRepresentativeRut=representante["legalRepresentativeRUT"],
            email=comercio.commerce_mail,
            name=representante["names"],
            lastName=representante["lastName"],
            motherLastName=representante["secondLastName"],
            mobilePhoneNumber=representante["legalRepresentativePhone"],
            sign="true",
            isThird="false",
            isSignAllowed="true",
            commerceId=0
        )


# Clase para manejar la estructura del endpoint de cuenta bancaria
# Incluye validaciones
class BankAccountRegister(BaseModel):
    commerceRut: str = Field(..., pattern=RUT_PATTERN)
    holderRut: str = Field(..., pattern=RUT_PATTERN)
    holderName: str
    accountTypeCode: int = Field(ge=0)  # Positive or Zero
    bankAccount: int = Field(gt=0)  # Positive
    bankCode: int = Field(gt=0)  # Positive
    holderMail: EmailStr
    user: str
    serviceId: int = Field(gt=0)  # Positive
    paymentType: str

    def to_json(self) -> str:
        """Converts the instance to a JSON string."""
        return self.model_dump_json()

    @classmethod
    def from_json(cls, json_str: str):
        """Creates an instance from a JSON string (handling field aliases)."""
        #data = json.loads(json_str)  # Convert JSON string to dictionary
        #return cls.model_validate(data)  # Use alias-aware validation
        return cls.parse_raw(json_str)  # Pydantic's built-in method to parse a JSON string into an instance
    
    @classmethod
    def from_volcado_comercio(cls, volcado: VolcadoComercio):
        comercio = volcado.comercio
        cuenta = comercio.bank_account[0]

        return cls(
            commerceRut=comercio.commerce_rut,
            holderRut=cuenta["ownerRut"],
            holderName=cuenta["fullName"],
            accountTypeCode=int(cuenta["accountType"]),
            bankAccount=int(cuenta["accountNumber"]),
            bankCode=int(cuenta["bank"]),
            holderMail=cuenta["ownerMail"],
            user="AYC",
            serviceId=4,
            paymentType="PAGO EN CUENTA BANCARIA"
        )


    

# Clase para manejar la estructura del endpoint de configuración cuenta bancaria
class BankAccountConfigurationRegister(BaseModel):
    commerceRut: str = Field(..., pattern=RUT_PATTERN)
    financedRut: str = Field(..., pattern=RUT_PATTERN)
    accountId: int = Field(ge=0)
    localCode: int = Field(ge=0)
    user: str
    serviceId: int = Field(ge=0)
    paymentType: str

    def to_json(self) -> str:
        """Converts the instance to a JSON string."""
        return self.model_dump_json()
    
    @classmethod
    def from_json(cls, json_str: str):
        return cls.parse_raw(json_str)


# Clase para manejar la estructura del registro de comercio
class Register(BaseModel):
    commerceRut: str = Field(..., pattern=RUT_PATTERN)
    name: str
    lastName: str
    mothersLastName: str
    businessName: str
    fanName: str
    businessLine: str
    address: str
    addressNumber: str = Field(..., pattern=ADDRESS_NUMBER_PATTERN, description="Must be a number between 1 and 6")
    cityId: int = Field(..., ge=0)  # Positive or Zero
    regionId: int = Field(..., ge=0)  # Positive or Zero
    townOrVillage: str
    mobilePhoneNumber: str
    email: EmailStr
    sellerCode: str
    emailPayment: EmailStr

    def to_json(self) -> str:
        """Converts the instance to a JSON string."""
        return self.model_dump_json()

    @classmethod
    def from_json(cls, json_str: str):
        """Creates an instance from a JSON string."""
        data = json.loads(json_str)  # Convert JSON string to dict
        return cls.model_validate(data)  # Validate with Pydantic

    @classmethod
    def from_volcado_comercio(cls, volcado: VolcadoComercio):
        comercio = volcado.comercio
        contacto = comercio.commerce_contact[0]

        # Lógica para definir algunos parámetros del request
        # Faltan algunas cosas, por ejemplo la definición real del nombre del comercio
        # Según si es es persona natural o jurídica
        address_parts = comercio.direction.split(',') if comercio.direction else [""]
        town_or_village = address_parts[1].strip()[:60] if len(address_parts) > 1 else ""

        return cls(
            commerceRut=comercio.commerce_rut,
            name=contacto.get("names", ""),
            lastName=contacto.get("lastName", ""),
            mothersLastName=contacto.get("secondLastName", ""),
            businessName=comercio.social_reason,
            fanName=comercio.fantasy_name,
            businessLine=str(comercio.giro),
            address=comercio.direction,
            addressNumber="0",  # Placeholder value
            cityId=comercio.comuna,
            regionId=comercio.region,
            townOrVillage=town_or_village,
            mobilePhoneNumber=str(comercio.phone),
            email=comercio.commerce_mail,
            sellerCode="5-1",
            emailPayment=comercio.commerce_mail  # Assuming same email for payments
        )


class BranchRegister(BaseModel):
    # Assuming RutConstraint checks a specific Chilean RUT pattern
    commerceRut: str = Field(..., pattern=RUT_PATTERN)
    name: str
    businessName: str
    fanName: str
    address: str
    addressNumber: str = Field(..., pattern=ADDRESS_NUMBER_PATTERN, description="Must be a number between 1 and 6")
    cityId: int = Field(..., ge=0)  # Positive or Zero
    regionId: int = Field(..., ge=0)  # Positive or Zero
    townOrVillage: str
    mobilePhoneNumber: str
    email: EmailStr
    idMcc: int = Field(..., ge=0)  # Positive or Zero
    webSite: Optional[str] = None
    commerceId: int = Field(..., ge=0)  # Positive or Zero

    # Convert the Pydantic model to a JSON string
    def to_json(self) -> str:
        return self.json()

    # Convert a JSON string to a BranchRegister instance
    @classmethod
    def from_json(cls, json_data: str) -> "BranchRegister":
        data = json.loads(json_str)  # Convert JSON string to dict
        return cls.model_validate(data)  # Validate with Pydantic
    
    @classmethod
    def from_volcado_comercio(cls, volcado: VolcadoComercio):
        comercio = volcado.comercio
        contacto = comercio.commerce_contact[0]

        address_parts = comercio.direction.split(',') if comercio.direction else [""]
        town_or_village = address_parts[1].strip()[:60] if len(address_parts) > 1 else ""

        sucursal = volcado.sucursales[0]

        return cls(
            # commerceRut=comercio.commerce_rut,
            commerceRut=comercio.commerce_rut,
            name=comercio.fantasy_name,
            businessName=comercio.social_reason,
            fanName=comercio.fantasy_name,
            address=comercio.direction, # Debiera ser de la sucursal, pero estamos usando la del comercio
            addressNumber="0",
            cityId=comercio.comuna,
            regionId=comercio.region,
            townOrVillage=town_or_village,
            mobilePhoneNumber=str(comercio.phone),
            # email=comercio.commerce_mail,
            email=comercio.commerce_mail,
            idMcc=sucursal.mcc,
            website="",
            commerceId=0 # Esto debe venir del paso anterior
        )



# Clase para manejar la estructura del registro servicio
class ServiceRegister(BaseModel):
    branchId: Optional[int] = Field(None, ge=0)  # Positive or Zero
    serviceId: Optional[int] = Field(None, ge=0)  # Positive or Zero
    commerceRut: str = Field(..., pattern=RUT_PATTERN)  # Must match RUT format
    mantisaBill: Optional[int] = None
    dvBill: Optional[str] = None
    paymentType: str
    bankAccount: str
    mantisaHolder: int = Field(..., ge=0)  # NotNull and PositiveOrZero
    logicBalanceId: int = Field(..., ge=0)  # NotNull and PositiveOrZero

    def to_json(self) -> str:
        return self.json()

    @classmethod
    def from_json(cls, json_data: str) -> "ServiceRegister":
        data = json.loads(json_data)  # Convert JSON string to dict
        return cls.model_validate(data)  # Validate with Pydantic
    
    @classmethod
    def from_volcado_comercio(cls, volcado: VolcadoComercio):
        comercio = volcado.comercio
        bank_account = comercio.bank_account[0]

        # Extract bank account (it’s a JSON string of a list)
        # bank_account_str = comercio.bank_account  

        # # Convert from JSON string to list of dicts
        # try:
        #     bank_account_list = json.loads(bank_account_str)  # Convert to list
            
        #     # Get first bank account
        #     if isinstance(bank_account_list, list) and bank_account_list:
        #         bank_account = bank_account_list[0]  # Extract first element
        #     else:
        #         raise ValueError("bank_account_list is empty or not a list")

        # except json.JSONDecodeError as e:
        #     print(f"ERROR: Failed to parse bank_account JSON: {e}")
        #     raise

        return cls(
            branchId=0,
            serviceId=4,
            commerceRut=comercio.commerce_rut,
            mantisaBill=int(bank_account["ownerRut"][:-2]),
            dvBill=bank_account["ownerRut"][-1],
            paymentType="PAGO EN CUENTA BANCARIA",
            bankAccount=bank_account["accountNumber"],
            mantisaHolder=int(bank_account["ownerRut"][:-2]),
            logicBalanceId=0
        )


class PaymentTypeRegister(BaseModel):
    serviceBranchId: int = Field(..., ge=0)  # Positive or zero integer
    commerceRut: str = Field(..., pattern=RUT_PATTERN)  # RUT format validation
    description: str = Field(..., min_length=0)  # Not blank
    branchCode: int = Field(..., ge=0)  # Positive or zero long value
    branchEntityId: int = Field(..., ge=0)  # Positive or zero long value

    # Convert from JSON (string)
    @classmethod
    def from_json(cls, json_data: str):
        return cls.parse_raw(json_data)

    # Convert to JSON (string)
    def to_json(self) -> str:
        return self.json()

    @classmethod
    def from_volcado_comercio(cls, volcado: VolcadoComercio):
        comercio = volcado.comercio

        return cls(
            commerceRut=comercio.commerce_rut,
            serviceBranchId=0, # difer¡do
            description="",
            branchCode=0, # diferido
            branchEntityId=0 # diferido
        )


class ContractRegister(BaseModel):
    commerceRut: str = Field(..., pattern=RUT_PATTERN)

    # Convert from JSON (string)
    @classmethod
    def from_json(cls, json_data: str):
        return cls.parse_raw(json_data)

    # Convert to JSON (string)
    def to_json(self) -> str:
        return self.json()
    
    @classmethod
    def from_volcado_comercio(cls, volcado: VolcadoComercio):

        return cls(
            commerceRut=volcado.comercio.commerce_rut
        )
    

class MerchantDiscountRegister(BaseModel):
    branchCode: int = Field(..., ge=0)
    idMcc: int = Field(..., ge=0)
    branchServiceId: int = Field(..., ge=0)
    serviceId: int = Field(..., ge=0)
    integrationType: int = Field(..., ge=0)

    # Convert from JSON (string)
    @classmethod
    def from_json(cls, json_data: str):
        return cls.parse_raw(json_data)

    # Convert to JSON (string)
    def to_json(self) -> str:
        return self.json()
    
    @classmethod
    def from_volcado_comercio(cls, volcado: VolcadoComercio):
        sucursal = volcado.sucursales[0]

        return cls(
            branchCode=0, # diferido
            idMcc=sucursal.mcc,
            branchServiceId=0, # diferido
            serviceId=4,
            integrationType=20 # Validar si este valor es correcto
        )


class TerminalRegister(BaseModel):
    commerceRut: str = Field(..., pattern=RUT_PATTERN)  # RUT format validation
    branchCode: Optional[int] = Field(default=None, ge=0)  # Equivalent to @PositiveOrZero
    contractId: Optional[str] = Field(default=None, min_length=1)  # Ensuring it's a string
    technology: int  # Equivalent to @NotNull
    ussdNumber: Optional[int] = Field(default=None, ge=0)  # Equivalent to @PositiveOrZero
    user: str  # Equivalent to @NotNull
    obs: str  # Equivalent to @NotNull
    additionalInfo: Optional[str] = None  # No validation needed
    serviceId: int  # Equivalent to @NotNull
    sellerRut: str = Field(..., pattern=RUT_PATTERN)

     # Convert from JSON (string)
    @classmethod
    def from_json(cls, json_data: str):
        return cls.parse_raw(json_data)

    # Convert to JSON (string)
    def to_json(self) -> str:
        return self.model_dump_json()
    
    @classmethod
    def from_volcado_comercio(cls, volcado: VolcadoComercio):
        comercio = volcado.comercio
        sucursal = volcado.sucursales[0]

        return cls(
            commerceRut=comercio.commerce_rut,
            branchCode="0", # diferido
            contractId="0", # diferido
            technology=20, # Validar que debe ser
            ussdNumber=0,
            user="AYC",
            obs="",
            additionalInfo="Sin info adicional (solo e-commerce)", # Para e-commerce se toma "webSite"
            serviceId=4,
            sellerRut="5-1"
        )


class BankAccConfigRegister(BaseModel):
    accountId: int = Field(..., ge=0)  # Positive or Zero
    financedRut: str = Field(..., pattern=RUT_PATTERN)
    commerceRut: str = Field(..., pattern=RUT_PATTERN)
    localCode: int = Field(..., ge=0)  # Positive or Zero
    user: str
    serviceId: int = Field(..., ge=0)  # Positive or Zero
    paymentType: str

    # Convert from JSON (string)
    @classmethod
    def from_json(cls, json_data: str):
        return cls.parse_raw(json_data)

    # Convert to JSON (string)
    def to_json(self) -> str:
        return self.model_dump_json()
    
    @classmethod
    def from_volcado_comercio(cls, volcado: VolcadoComercio):
        comercio = volcado.comercio

        return cls(
            accountId=0, # diferido
            financedRut=comercio.commerce_rut,
            commerceRut=comercio.commerce_rut,
            localCode=0, # diferido
            user="AYC",
            serviceId=4,
            paymentType="CUENTA_BANCARIA" # Validar si está bien con el underscore
        )


     
class BranchCCRegister(BaseModel):
    commerceRut: str = Field(..., pattern=RUT_PATTERN)
    branchCode: int = Field(..., ge=0)
    user: str
    serviceId: int = Field(..., ge=0)

     # Convert from JSON (string)
    @classmethod
    def from_json(cls, json_data: str):
        return cls.parse_raw(json_data)

    # Convert to JSON (string)
    def to_json(self) -> str:
        return self.model_dump_json()
    
    @classmethod
    def from_volcado_comercio(cls, volcado: VolcadoComercio):
        comercio = volcado.comercio

        return cls(
            commerceRut=comercio.commerce_rut,
            branchCode=0, # diferido
            user="AYC",
            serviceId=4
        )
    

class TerminalCCRegister(BaseModel):
    commerceRut: str = Field(..., pattern=RUT_PATTERN)
    branchCode: int = Field(..., ge=0)
    user: str
    serviceId: int = Field(..., ge=0)
    terminalNumber: int = Field(..., ge=0)

    # Convert from JSON (string)
    @classmethod
    def from_json(cls, json_data: str):
        return cls.parse_raw(json_data)

    # Convert to JSON (string)
    def to_json(self) -> str:
        return self.model_dump_json()

    @classmethod
    def from_volcado_comercio(cls, volcado: VolcadoComercio):
        comercio = volcado.comercio

        return cls(
            commerceRut=comercio.commerce_rut,
            branchCode=0, # diferido
            user="AYC",
            serviceId=4,
            terminalNumber=0 # diferido
        )


class IswitchCommerceRegister(BaseModel):
    commerceRut: str = Field(..., pattern=RUT_PATTERN)

    # Convert from JSON (string)
    @classmethod
    def from_json(cls, json_data: str):
        return cls.parse_raw(json_data)

    # Convert to JSON (string)
    def to_json(self) -> str:
        return self.json()
    
    @classmethod
    def from_volcado_comercio(cls, volcado: VolcadoComercio):

        return cls(
            commerceRut=volcado.comercio.commerce_rut
        )

    
class IswitchBranchRegister(BaseModel):
    commerceRut: str = Field(..., pattern=RUT_PATTERN)
    localCode: int = Field(..., ge=0) # Originalmente un string, pero cambiado a int para mantener consistencia

    # Convert from JSON (string)
    @classmethod
    def from_json(cls, json_data: str):
        return cls.parse_raw(json_data)

    # Convert to JSON (string)
    def to_json(self) -> str:
        return self.json()
    
    @classmethod
    def from_volcado_comercio(cls, volcado: VolcadoComercio):

        return cls(
            commerceRut=volcado.comercio.commerce_rut,
            localCode = 0 # diferido
        )


class IswitchTerminalRegister(BaseModel):
    commerceRut: str = Field(..., pattern=RUT_PATTERN)
    terminalNumber: int = Field(..., ge=0) # Era string, pero cambiamos a int
    user: str

    # Convert from JSON (string)
    @classmethod
    def from_json(cls, json_data: str):
        return cls.parse_raw(json_data)

    # Convert to JSON (string)
    def to_json(self) -> str:
        return self.json()
    
    @classmethod
    def from_volcado_comercio(cls, volcado: VolcadoComercio):

        return cls(
            commerceRut=volcado.comercio.commerce_rut,
            terminalNumber=0, # diferido
            user="AYC"
        )


class CommercePciRegister(BaseModel):
    commerceRut: str = Field(..., pattern=RUT_PATTERN)
    branchCode: int = Field(..., ge=0)

    # Convert from JSON (string)
    @classmethod
    def from_json(cls, json_data: str):
        return cls.parse_raw(json_data)

    # Convert to JSON (string)
    def to_json(self) -> str:
        return self.json()
    
    @classmethod
    def from_volcado_comercio(cls, volcado: VolcadoComercio):

        return cls(
            commerceRut=volcado.comercio.commerce_rut,
            branchCode=0 #diferido
        )


class CommerceSwitchRegister(BaseModel):
    branchCode: int = Field(..., ge=0)
    emitTicket: str
    changeDebit: str
    changeCredit: str
    changePrepaid: str
    perquisiteDebit: str
    perquisiteCredit: str
    perquisitePrepaid: str

    # Convert from JSON (string)
    @classmethod
    def from_json(cls, json_data: str):
        return cls.parse_raw(json_data)

    # Convert to JSON (string)
    def to_json(self) -> str:
        return self.json()
    
    @classmethod
    def from_volcado_comercio(cls, volcado: VolcadoComercio):

        return cls(
            branchCode=0, #diferido
            emitTicket="N",
            changeCredit="N",
            changeDebit="N",
            changePrepaid="N",
            perquisiteDebit="N",
            perquisiteCredit="N",
            perquisitePrepaid="N"
        )


class TicketRegister(BaseModel):
    commerceRut: str = Field(..., pattern=RUT_PATTERN)
    user: str
    obs: str
    business: str
    task: str
    email: str

    # Convert from JSON (string)
    @classmethod
    def from_json(cls, json_data: str):
        return cls.parse_raw(json_data)

    # Convert to JSON (string)
    def to_json(self) -> str:
        return self.json()
    
    @classmethod
    def from_volcado_comercio(cls, volcado: VolcadoComercio):
        comercio = volcado.comercio
        sucursal = volcado.sucursales[0]

        return cls(
            commerceRut=comercio.commerce_rut,
            user="autoafiliacion", # Validar valor
            obs=sucursal.services[0]["serviceType"],
            business="MULTICAJA",
            task="VALIDACION_AFILIACION",
            email=comercio.commerce_mail
        )


class MonitorRegister(BaseModel):
    commerceRut: str = Field(..., pattern=RUT_PATTERN)
    user: str
    branchCode: int = Field(..., ge=0)
    fantasyName: str
    businessName: str
    address: str
    phone: str
    commune: str
    email: str
    commerceType: str = Field(..., min_length=1, max_length=1)
    contractDate: datetime # Validar si esto no causa problemas en el servicio de Monitor
    merchantType: int = Field(..., ge=0)
    cashBack: str = Field(..., min_length=1, max_length=1)
    gratuity: str = Field(..., min_length=1, max_length=1)
    admissionDate: datetime # Validar si esto no causa problemas en el servicio de Monitor
    posAmount: int
    commerceContactName: str
    commerceContactPosition: str
    commerceContactPhone: str
    commerceRepresentativeLegalName: str
    commerceRepresentativeLegalRut: str = Field(..., pattern=RUT_PATTERN)
    commerceRepresentativeLegalPhone: str

    # Convert from JSON (string)
    @classmethod
    def from_json(cls, json_data: str):
        return cls.parse_raw(json_data)

    # Convert to JSON (string)
    def to_json(self) -> str:
        return self.json()
    
    @classmethod
    def from_volcado_comercio(cls, volcado: VolcadoComercio):
        comercio = volcado.comercio
        sucursal = volcado.sucursales[0]

        return cls(
            commerceRut=comercio.commerce_rut,
            user="AYC",
            branchCode=0, # diferido
            fantasyName=comercio.fantasy_name,
            businessName="Nombre", # Lógica de PN o PJ
            address=comercio.direction,
            phone=comercio.commerce_contact[0]["contactPhone"],
            commune=comercio.direction,
            email=comercio.commerce_contact[0]["contactMail"],
            commerceType="C",
            contractDate=datetime.now(),
            merchantType=sucursal.mcc,
            cashBack="C",
            gratuity="C",
            admissionDate=datetime.now(),
            posAmount=0,
            commerceContactName=comercio.commerce_contact[0]["names"],
            commerceContactPosition="REPRESENTANTE",
            commerceContactPhone=comercio.commerce_contact[0]["contactPhone"],
            commerceRepresentativeLegalName=comercio.legal_representatives[0]["names"],
            commerceRepresentativeLegalRut=comercio.legal_representatives[0]["legalRepresentativeRUT"],
            commerceRepresentativeLegalPhone=comercio.legal_representatives[0]["legalRepresentativePhone"]
        )
