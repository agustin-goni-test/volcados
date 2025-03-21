from inputvolcados import Comercio, Sucursal, VolcadoComercio
import inputvolcados as input_data
from registrosvolcado import RepresentativeRegister, Register, BranchRegister, ServiceRegister, BankAccountRegister
from registrosvolcado import PaymentTypeRegister, ContractRegister, MerchantDiscountRegister, TerminalRegister
from registrosvolcado import BankAccConfigRegister, BranchCCRegister, TerminalCCRegister, IswitchCommerceRegister
from registrosvolcado import IswitchBranchRegister, IswitchTerminalRegister, CommercePciRegister, CommerceSwitchRegister
from registrosvolcado import TicketRegister, MonitorRegister, RedPosRegister
from volcadomanager import VolcadoManager
from resultvolcado import ResultadoVolcado, ResultFuncion, Mensaje, ServiceResult, PaymentTypeResult, TerminalResult, TicketResult
from resultvolcado import ContratoResult, BankAccountResult, IswitchBranchResult, MonitorResult, RedPosResult, CommerceResult, BranchResult
import requests
import json
from datetime import datetime
import time
from entidadesvolcado import EntidadesVolcado, Sucursal, Terminal, RepresentanteLegal, CuentaBancaria, ComercioCentral
from procesarvolcado import ProcesoVolcado
import resultvolcado as res


##################################################################################
# Métodos auxiliares que se usan para generar las entidades a partir
# de la información que existe en el archivo Excel.
# Lo importante acá es que el archivo Excel contiene la misma información
# que la base de datos vertical. Es como hacer un SELECT en ayc_comercio (uno solo)
# por rut_comercio, y traer las sucursales (una o varias) asociadas al comercio
##################################################################################


# Obtener la entidad de comercio central a partir de la información de la base
def get_comercio_central_from_volcado(volcado: VolcadoComercio):
    comercio = volcado.comercio
    sucursal = volcado.sucursales[0]
    servicios = sucursal.services[0]
    contacto = comercio.commerce_contact[0]

    return ComercioCentral(
        commerceRut=comercio.commerce_rut,
        businessName="Nombre de comercio",  # Requiere lógica de persona natural y jurídica
        email=comercio.commerce_mail,
        emailPayment=comercio.commerce_mail,
        fanName=comercio.fantasy_name,
        name=contacto.get("names", ""),
        lastName=contacto.get("lastName", ""),
        mothersLastName=contacto.get("secondLastName", ""),
        mobilePhoneNumber=contacto.get("contactPhone", ""),
        address=comercio.direction, # requiere lógica para definir
        addressNumber="0", # Placeholder
        cityId=comercio.comuna,
        regionId=comercio.region,
        sellerCode=str(comercio.executive_rut),
        businessLine=comercio.giro,
        townOrVillage=comercio.direction,  # requiere lógica para definir
        obs=servicios.get("serviceType", "")
    )


# Obtener la entidad asociada a una sucursal a partir de la información de la base
# Debido a que vamos a necesitar usar este método en más de una sucursal, no
# basta con pasar la estrucutura de comercio completa.
# Le pasamos el comercio y la sucursal *específica* que queremos crear.
# Pueden existir formas más elegantes de hacerlo, pero fue la solución que 
# encontré para que funcionara pronto.
def get_sucursal_from_volcado(comercio: input_data.Comercio, sucursal: input_data.Sucursal):
    contacto = comercio.commerce_contact[0]
    representante = comercio.legal_representatives[0]
    terminal = sucursal.terminals[0]
    bank_account = comercio.bank_account[0]
    address_parts = comercio.direction.split(',') if comercio.direction else [""]
    town_or_village = address_parts[1].strip()[:60] if len(address_parts) > 1 else ""

    return Sucursal(
        address=comercio.direction,
        addressNumber="0",  # Placeholder
        businessName="Nombre de comercio",
        cityId=comercio.comuna,
        commerceRut=comercio.commerce_rut,
        email=comercio.commerce_mail,
        fanName=comercio.fantasy_name,
        idMcc=sucursal.mcc,
        mobilePhoneNumber=contacto.get("contactPhone", ""),
        name=comercio.fantasy_name,
        regionId=comercio.region,
        townOrVillage=town_or_village,
        webSite=terminal.get("webPage", ""),
        mantisaBill=bank_account["ownerRut"][:-2],
        dvBill=bank_account["ownerRut"][-1],
        bankAccount=bank_account["accountNumber"],
        mantisaHolder=bank_account["ownerRut"][:-2],
        integrationType="PRESENCIAL",
        user="AYC",
        emailContacto=contacto.get("contactMail", ""),
        merchantType=sucursal.mcc,
        commerceContactName=contacto.get("names", ""),
        commerceRepresentativeLegalName=representante.get("names", ""),
        commerceRepresentativeLegalRut=representante.get("legalRepresentativeRUT", ""),
        commecerRepresentativeLegalPhone=representante.get("legalRepresentativePhone")
    )


# Obtener la entidad cuenta bancaria a partir de la información del comercio
# En este caso de uso, la cuenta va a ser única. Si no lo fuera
# habría que cambiar los parámetros de entrada.
def get_cuenta_from_volcado(volcado: VolcadoComercio):
    comercio = volcado.comercio
    cuenta = comercio.bank_account[0]

    return CuentaBancaria(
        commerceRut=comercio.commerce_rut,
        holderRut=cuenta.get("ownerRut", ""),
        holderName=cuenta.get("fullName", ""),
        accountTypeCode=cuenta.get("accounType", "2"),
        bankAccount=cuenta.get("accountNumber", ""),
        bankCode=cuenta.get("bank", ""),
        holderMail=cuenta.get("ownerMail", "")
    )


# Obtener los datos para la entidad del representante legal.
# Al igual que en el caso de la cuenta, por ahora es único.
def get_representante_from_volcado(volcado: VolcadoComercio):
    comercio = volcado.comercio
    representante = comercio.legal_representatives[0]

    return RepresentanteLegal(
        commerceRut=comercio.commerce_rut,
        legalRepresentativeRut=representante.get("legalRepresentativeRUT", ""),
        email=comercio.commerce_mail,
        name=representante.get("names", ""),
        lastName=representante.get("lastName", ""),
        motherLastName=representante.get("secondLastName", ""),        
        mobilePhoneNumber=representante.get("legalRepresentativePhone", ""),
        sign=True,
        isThird=False,
        isSignAllowed=False
    )

# Obtener la información de la entidad de terminal
# Dado que son múltiples, requiere pasar el comercio y los datos de la sucursal
# Cabe señalar que en el modelo actual no hay ningún dato del terminal que realmente dependa
# de cada termninal. Basta con pasar las sucursales
def get_terminal_from_volcado(comercio: input_data.Comercio, sucursal: input_data.Sucursal):
    # comercio = volcado.comercio
    # sucursal = volcado.sucursales[0]
    # terminal = sucursal

    return Terminal(
        commerceRut=comercio.commerce_rut,
        branchCode=0,
        contractId="0",
        technology=20,
        ussdNumber=0,
        user="AYC",
        obs="",
        additionalInfo=None,
        serviceId=4,
        sellerRut=str(comercio.executive_rut),
        terminalNumber="0" # diferido
    )



# Flujo principal para generar la lógica de volcado
if __name__ == "__main__":
    
    # Token para consumir toda la capa de servicios (en dev)
    AUTH_TOKEN = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJhcHAiOiJtcy1jZW50cmFsLWFmLWF5Yy1yZWdpc3Ryby1jb21lcmNpbyIsImlzcyI6ImFmLWF5Yy1yZWdpc3Ryby1jb21lcmNpby1jZW50cmFsIn0.gxrgQE6Oae1-gw3Gaif0j3e-uY2sMjR2IWPwRS-5mL0"
    
    # Archivo Excel en el que estarán los datos del comercio
    # Requiere que existan 2 hojas:
    # Comercio, que simula la tabla ayc_comercio
    # Sucursal, que simula la tabla ayc_sucursal
    file_path = "InfoComercio.xlsx"
    volcado = VolcadoComercio.from_excel(file_path)

    # Variable para activar información de debug
    # DEBUG = False
    DEBUG = False
    
    # Esta clase manager será encargada de hacer los llamados a todos los servicios
    # Es análogo a los bots del task-volcado
    manager = VolcadoManager(AUTH_TOKEN, volcado)

    # Creamos objeto vacío de entidades para poblarr posteriormente
    entidades = EntidadesVolcado()
    
    ###################################################################################################
    # Crear resultado del volcado
    # Considerar que hubo una modificación a la forma de crear este objeto en el commit de 17/03 a las 9:30
    # Esto para agregar en forma dinámica cada cosa según se va creando
    ###################################################################################################

    # Luego de la modificación al objeto sólo se crea con valores para comercio central
    result = ResultadoVolcado()

    ###################################################################################################
    # No vamos a crear nada más respecto al objeto de resultado
    ###################################################################################################
    
    # # Crear la parte correspondiente a la sucursal
    # sucursal = res.Sucursal()

    # # Crear terminal y agregarlo a la sucursal
    # terminal = res.Terminal()
    # sucursal.add_terminal(terminal)

    # # Agregar la sucursal al resultado completo
    # result.add_sucursal(sucursal)

    # # Crear cuenta bancaria y representante legal. Agregar a result
    # cuenta = res.CuentaBancaria()
    # rep = res.RepresentanteLegal()
    # result.add_cuenta_bancaria(cuenta)
    # result.add_representante_legal(rep)


    print(result.to_json())
    input("ENTER...")

    ###########################################################################
    #
    # En esta sección estamos creando el objeto de las entidades de volcado
    #
    # Análogo a lo que ocurrirá en verticales con el consumer volcado
    #
    ############################################################################
    

    print("\n")
    
    # Crear entidad comercio central
    comercio_central = get_comercio_central_from_volcado(volcado)
    
    # Crear entidad cuenta
    cuenta = get_cuenta_from_volcado(volcado)
    
    # Crear entidad representante
    representante = get_representante_from_volcado(volcado)

    # Iterar para todas las sucursales encontradas en el archivo
    for s in volcado.sucursales:
        
        # Si la sucursal tiene terminales
        if s.terminals:
            
            # Crear entidad de sucursal para procesar, en principio sin terminales
            sucursal = get_sucursal_from_volcado(volcado.comercio, s)
            
            # Crear una lista vacía de terminales
            terminal_objects = []
            
            # Iterar por todos los terminales que estaban agregados a la sucursal en el origen
            for terminal_data in s.terminals:

                # Obtener el objeto (entidad) terminal desde el origen (verticales)
                terminal_obj = get_terminal_from_volcado(volcado.comercio, s)

                # Agregar la entidad terminal a la lista de terminales
                terminal_objects.append(terminal_obj)

            # Iterar toda la lista de entidades terminales obtenida
            for t in terminal_objects:

                # agregar cada terminal a la sucursal
                sucursal.add_terminal(t)
        
        # Agregar la sucursal a las entidades generales
        entidades.add_sucursal(sucursal)

    # Asignar la entidad comercio central creada a las entidades generales
    entidades.comercioCentral = comercio_central
    
    # agregar la cuenta bancaria
    entidades.add_cuenta_bancaria(cuenta)
    
    # Agregar representante legal
    entidades.add_representante_legal(representante)

    # Con esto las entidades del volcado ya están listas
    # Esto representa la "entrada" del proceso de volcado
    # Se genera en verticales y se transmite a centrales    
    print("Objeto de entrada para el volcado:")
    print(entidades.to_json())
    input("ENTER...")

    # Mostramos el objeto de resultado que vamos a poblar según
    # los resultados de los volcados
    print("Objecto de resultado para el volcado:")
    print(result.to_json())
    input("ENTER")

    # Información adicional de ser requerida
    if DEBUG:
        print("Objeto comercio central:")
        print(comercio_central.to_json())
        print("\n")
        input("ENTER: ")
        print("Objeto cuenta bancaria:")
        print(cuenta.to_json())
        input("ENTER: ")
        print("\nObjeto representante legal:")
        print(representante.to_json())
        input("ENTER: ")
        print("\nObjeto de sucursal:")
        print(sucursal.to_json())
        input("ENTER: ")
        print("\nObjeto de terminal:")
        print(terminal.to_json())
        input("ENTER: ")
        print("\nObjeto de entidades completo:")
        print(entidades.to_json())
        input("ENTER...")

    # Generar objeto de procesamiento de volcado
    proceso = ProcesoVolcado(manager, result)

    # Procesar el volcado completo
    proceso.procesarComercio(entidades)

    