from pydantic import BaseModel, Field, EmailStr, conint, constr, field_validator
from typing import Optional
from inputvolcados import VolcadoComercio
from datetime import date, datetime
import json
from entidadesvolcado import ComercioCentral, CuentaBancaria, RepresentanteLegal, Terminal, Sucursal


# Clases para manejar los parámetros de ingreso de todas las llamadas de BD
# En volcado-comercio estás clases se llaman "Register". Acá estoy usando esa convención.
# En task-volcado son "Request", pero el contenido de cada una es el mismo

# Todas estas clases tiene dos métodos:
#   * from_volcado_comercio(), que obtiene el request de la información de origina ("BD vertical")
#   * from_entidades(), que obtiene el volcado desde las entidades de negocio (nueva versión)

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
    
    @classmethod
    def from_entidades(cls, entidad: RepresentanteLegal):

        return cls(
            commerceRut=entidad.commerceRut,
            legalRepresentativeRut=entidad.legalRepresentativeRut,
            email=entidad.email,
            name=entidad.name,
            lastName=entidad.lastName,
            motherLastName=entidad.motherLastName,
            mobilePhoneNumber=entidad.mobilePhoneNumber,
            sign="true" if entidad.sign else "false",
            isThird="true" if entidad.isThird else "false",
            isSignAllowed="true" if entidad.isSignAllowed else "false",
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
    
    @classmethod
    def from_entidades(cls, entidad: CuentaBancaria):

        return cls(
            commerceRut=entidad.commerceRut,
            holderRut=entidad.holderRut,
            holderName=entidad.holderName,
            accountTypeCode=entidad.accountTypeCode,
            bankAccount=entidad.bankAccount,
            bankCode=entidad.bankCode,
            holderMail=entidad.holderMail,
            user="AYC",
            serviceId=4,
            paymentType="PAGO EN CUENTA BANCARIA"
        )
    

# Ésta al final no la estoy usando!!!!!
# La hice de nuevo más abajo
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
    
    @classmethod
    def from_entidades(cls, entidades: ComercioCentral):

        return cls(
            commerceRut=entidades.commerceRut,
            name=entidades.name,
            lastName=entidades.lastName,
            mothersLastName=entidades.mothersLastName,
            businessName=entidades.businessName,
            fanName=entidades.fanName,
            businessLine=str(entidades.businessLine),
            address=entidades.address,
            addressNumber=entidades.addressNumber,
            cityId=entidades.cityId,
            regionId=entidades.regionId,
            townOrVillage=entidades.townOrVillage,
            mobilePhoneNumber=entidades.mobilePhoneNumber,
            email=entidades.email,
            sellerCode=entidades.sellerCode,
            emailPayment=entidades.emailPayment
        )



# Clase para manejar la estructura del volcado de sucursal
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
    
    @classmethod
    def from_entidades(cls, entidad: Sucursal):
        return cls(
            commerceRut=entidad.commerceRut,
            name=entidad.name,
            businessName=entidad.businessName,
            fanName=entidad.fanName,
            address=entidad.address,
            addressNumber=entidad.addressNumber,
            cityId=entidad.cityId,
            regionId=entidad.regionId,
            townOrVillage=entidad.townOrVillage,
            mobilePhoneNumber=entidad.mobilePhoneNumber,
            email=entidad.email,
            idMcc=entidad.idMcc,
            webSite=entidad.webSite,
            commerceId=0 # diferido
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
    
    @classmethod
    def from_entidades(cls, entidad: Sucursal):

        return cls(
            branchId=0,
            serviceId=4,
            commerceRut=entidad.commerceRut,
            mantisaBill=entidad.mantisaBill,
            dvBill=entidad.dvBill,
            paymentType="PAGO EN CUENTA BANCARIA",
            bankAccount=entidad.bankAccount,
            mantisaHolder=entidad.mantisaHolder,
            logicBalanceId=0
        )


# Clase para manejar el volcado de los payment types
# Contiene una lista "en duro" de los tipos de pagos a usar
# Esta lista podría venir como argumento, tal como en el volcado actual
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
    
    @classmethod
    def from_entidades(cls, entidad: Sucursal):

        return cls(
            commerceRut=entidad.commerceRut,
            serviceBranchId=0, # difer¡do
            description="",
            branchCode=0, # diferido
            branchEntityId=0 # diferido
        )


# Clase para manejar el volcado del contrato
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
    
    @classmethod
    def from_entidades(cls, entidad: ComercioCentral):

        return cls(
            commerceRut=entidad.commerceRut
        )
    

# Clase para manejar el volcado del merchant discount
class MerchantDiscountRegister(BaseModel):
    branchCode: int = Field(..., ge=0)
    idMcc: int = Field(..., ge=0)
    branchServiceId: int = Field(..., ge=0)
    serviceId: int = Field(..., ge=0)
    integrationType: str

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
            integrationType="PRESENCIAL"
        )
    
    @classmethod
    def from_entidades(cls, entidad: Sucursal):

        return cls(
            branchCode=0, # diferido
            idMcc=entidad.idMcc,
            branchServiceId=0, # diferido
            serviceId=4,
            integrationType="PRESENCIAL"
        )


# Clase para manejar el volcado de terminal
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
            additionalInfo=None, # Para e-commerce se toma "webSite"
            serviceId=4,
            sellerRut="5-1"
        )
    
    @classmethod
    def from_entidades(cls, entidad: Terminal):
        return cls(
            commerceRut=entidad.commerceRut,
            branchCode=entidad.branchCode,
            contractId=entidad.contractId,
            technology=entidad.technology,
            ussdNumber=entidad.ussdNumber,
            user=entidad.user,
            obs=entidad.obs,
            additionalInfo=entidad.additionalInfo,
            serviceId=entidad.serviceId,
            sellerRut=entidad.sellerRut
        )


# Clase para manejar el volcado de configuración de cuenta bancaria
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
    
    @classmethod
    def from_entidades(cls, entidad: CuentaBancaria):
        
        return cls(
            accountId=0, # diferido
            financedRut=entidad.holderRut,
            commerceRut=entidad.commerceRut,
            localCode=0, # diferido
            user="AYC",
            serviceId=4,
            paymentType="CUENTA_BANCARIA"            
        )


# Clase para manejar el volcado de CC en sucursal    
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
    
    @classmethod
    def from_entidades(cls, entidad: Sucursal):

        return cls(
            commerceRut=entidad.commerceRut,
            branchCode=0, # diferido
            user="AYC",
            serviceId=4
        )

# Clase para manejar el volcado de CC en terminal
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
    
    @classmethod
    def from_entidades(cls, entidad: Terminal):

        return cls(
            commerceRut=entidad.commerceRut,
            branchCode=entidad.branchCode, # diferido
            user=entidad.user,
            serviceId=entidad.serviceId,
            terminalNumber=entidad.terminalNumber # diferido
        )


# Clase para volcar el comercio en ISWITCH
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
    
    @classmethod
    def from_entidades(cls, entidad: ComercioCentral):

        return cls(
            commerceRut=entidad.commerceRut
        )


# Clase para volcar la sucursal en ISWITCH
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
    
    @classmethod
    def from_entidades(cls, entidad: Sucursal):

        return cls(
            commerceRut=entidad.commerceRut,
            localCode = 0 # diferido
        )


# Clase para volcar el terminal en ISWITCH
class IswitchTerminalRegister(BaseModel):
    commerceRut: str = Field(..., pattern=RUT_PATTERN)
    terminalNumber: str
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
            terminalNumber="0", # diferido
            user="AYC"
        )
    
    @classmethod
    def from_entidades(cls, entidad: Terminal):

        return cls(
            commerceRut=entidad.commerceRut,
            terminalNumber=entidad.terminalNumber, # diferido
            user=entidad.user
        )
    

# Clase para volcar el comercio en la réplica PCI
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
    
    @classmethod
    def from_entidades(cls, entidad: Sucursal):

        return cls(
            commerceRut=entidad.commerceRut,
            branchCode=0 #diferido
        )


# Clase para volcar el comercio en el SWITCH
class CommerceSwitchRegister(BaseModel):
    branchCode: int = Field(..., ge=0)
    # emitTicket: str
    # changeDebit: str
    # changeCredit: str
    # changePrepaid: str
    # perquisiteDebit: str
    # perquisiteCredit: str
    # perquisitePrepaid: str

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
            # emitTicket="",
            # changeCredit="",
            # changeDebit="",
            # changePrepaid="",
            # perquisiteDebit="",
            # perquisiteCredit="",
            # perquisitePrepaid=""
        )
    
    @classmethod
    def from_entidades(cls, entidad: Sucursal):

        return cls(
            branchCode=0, #diferido
        )


# Clase para volcar el ticket de afiliación
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
            task="VALIDACION_AUTOAFILIACION",
            email=comercio.commerce_mail
        )
    
    @classmethod
    def from_entidades(cls, entidad: Sucursal):

        return cls(
            commerceRut=entidad.commerceRut,
            user="autoafiliacion", # Validar valor
            obs="pos",
            business="MULTICAJA",
            task="VALIDACION_AUTOAFILIACION",
            email=entidad.email
        )


# Clase para volcar en Monitor Plus
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
    contractDate: int # Validar si esto no causa problemas en el servicio de Monitor
    merchantType: int = Field(..., ge=0)
    cashBack: str = Field(..., min_length=1, max_length=1)
    gratuity: str = Field(..., min_length=1, max_length=1)
    admissionDate: int # Validar si esto no causa problemas en el servicio de Monitor
    posAmount: int
    commerceContactName: str
    commerceContactPosition: str
    commerceContactPhone: str
    commerceRepresentativeLegalName: str
    commerceRepresentativeLegalrut: str = Field(..., pattern=RUT_PATTERN)
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

        fecha_actual = datetime.now()
        fecha_epoch = int(fecha_actual.timestamp() * 1000)

        return cls(
            commerceRut=comercio.commerce_rut,
            user="AYC",
            branchCode=0, # diferido
            fantasyName=comercio.fantasy_name,
            businessName="Nombre", # Lógica de PN o PJ
            address=comercio.direction,
            phone=comercio.commerce_contact[0]["contactPhone"],
            commune=comercio.cityId,
            email=comercio.commerce_contact[0]["contactMail"],
            commerceType="C",
            contractDate=fecha_epoch,
            merchantType=sucursal.mcc,
            cashBack="C",
            gratuity="C",
            admissionDate=fecha_epoch,
            posAmount=0,
            commerceContactName=comercio.commerce_contact[0]["names"],
            commerceContactPosition="REPRESENTANTE",
            commerceContactPhone=comercio.commerce_contact[0]["contactPhone"],
            commerceRepresentativeLegalName=comercio.legal_representatives[0]["names"],
            commerceRepresentativeLegalrut=comercio.legal_representatives[0]["legalRepresentativeRUT"],
            commerceRepresentativeLegalPhone=comercio.legal_representatives[0]["legalRepresentativePhone"]
        )


    @classmethod
    def from_entidades(cls, entidad: Sucursal):

        fecha_actual = datetime.now()
        fecha_epoch = int(fecha_actual.timestamp() * 1000)

        return cls(
            commerceRut=entidad.commerceRut,
            user="AYC",
            branchCode=0, # diferido
            fantasyName=entidad.fanName,
            businessName="Nombre", # Lógica de PN o PJ
            address=entidad.address,
            phone=entidad.mobilePhoneNumber,
            commune=str(entidad.cityId),
            email=entidad.email,
            commerceType="C",
            contractDate=fecha_epoch,
            merchantType=entidad.idMcc,
            cashBack="C",
            gratuity="C",
            admissionDate=fecha_epoch,
            posAmount=0,
            commerceContactName=entidad.commerceContactName,
            commerceContactPosition="REPRESENTANTE",
            commerceContactPhone=entidad.mobilePhoneNumber,
            commerceRepresentativeLegalName=entidad.commerceRepresentativeLegalName,
            commerceRepresentativeLegalrut=entidad.commerceRepresentativeLegalRut,
            commerceRepresentativeLegalPhone=entidad.commecerRepresentativeLegalPhone
        )

# Clase para volcar el ticket de RedPos
class RedPosRegister(BaseModel):
    commerceRut: str = Field(..., pattern=RUT_PATTERN)
    remark: str
    user: str
    terminalNumber: str

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
            user="AYC",
            # Este dato remark fue tomado de un caso puntual, sólo para poder probar
            remark="-SIM: MOVISTAR -MODELO: POSANDROIDMOVIL -CANAL: AUTOAFILIACION. CANAL_ORIGEN: AUTOAFILIACION_POS",
            terminalNumber="0" # Así es como llega hoy, no hay dato diferido
        )
    
    @classmethod
    def from_entidades(cls, entidad: Terminal):

        return cls(
            commerceRut=entidad.commerceRut,
            user=entidad.user,
            # Este dato remark fue tomado de un caso puntual, sólo para poder probar
            remark="-SIM: MOVISTAR -MODELO: POSANDROIDMOVIL -CANAL: AUTOAFILIACION. CANAL_ORIGEN: AUTOAFILIACION_POS",
            terminalNumber=entidad.terminalNumber # Así es como llega hoy, no hay dato diferido
        )