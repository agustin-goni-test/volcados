from inputvolcados import Comercio, Sucursal, VolcadoComercio
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

def get_sucursal_from_volcado(volcado: VolcadoComercio):
    comercio = volcado.comercio
    sucursal = volcado.sucursales[0]
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
        commerceRepresentativeLegalName=representante.get("names", ""),
        commerceRepresentativeLegalRut=representante.get("legalRepresentativeRut", "")
    )


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


def get_representante_from_volcado(volcado: VolcadoComercio):
    comercio = volcado.comercio
    representante = comercio.legal_representatives[0]

    return RepresentanteLegal(
        commerceRut=comercio.commerce_rut,
        legalRepresentativeRut=representante.get("legalRepresentativeRut", ""),
        email=comercio.commerce_mail,
        name=representante.get("names", ""),
        lastName=representante.get("lastName", ""),
        motherLastName=representante.get("secondLastName", ""),        
        mobilePhoneNumber=representante.get("legalRepresentativePhone", ""),
        sign=True,
        isThird=False,
        isSignAllowed=False
    )

def get_terminal_from_volcado(volcado: VolcadoComercio):
    comercio = volcado.comercio
    sucursal = volcado.sucursales[0]
    terminal = sucursal

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
        sellerRut=str(comercio.executive_rut)
    )





# Este código lee un archivo Excel con la información de un comercio y generar los
# request para hacer el volcado según el camino tradicional (sin multiplicidad).
# Estamos mostrando cada request en pantalla

if __name__ == "__main__":
    
    AUTH_TOKEN = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJhcHAiOiJtcy1jZW50cmFsLWFmLWF5Yy1yZWdpc3Ryby1jb21lcmNpbyIsImlzcyI6ImFmLWF5Yy1yZWdpc3Ryby1jb21lcmNpby1jZW50cmFsIn0.gxrgQE6Oae1-gw3Gaif0j3e-uY2sMjR2IWPwRS-5mL0"
    
    file_path = "InfoComercio.xlsx"
    volcado = VolcadoComercio.from_excel(file_path)

    # Variable para activar información de debug
    # DEBUG = False
    DEBUG = False
    
    # info_deb = input("Agegar información de DEBUG? (s/n) ")
    # if info_deb == "S" or info_deb == "s":
    #     DEBUG = True
    #     print("\nModo DEBUG activado.")
    #     print(DEBUG)
    #     input("Presione ENTER: ")
    #     print("\n")
    # else:
    #     print("\nModo DEBUG desactivado")
    #     input("Presione ENTER: ")
    #     print("\n")
    
    # if DEBUG:
    #     print(volcado.to_json())

    manager = VolcadoManager(AUTH_TOKEN, volcado)

    entidades = EntidadesVolcado()
    result = ResultadoVolcado()

    ###########################################################################
    #
    # En esta sección estamos creando el objeto de las entidades de volcado
    #
    # Análogo a lo que ocurrirá en verticales con el consumer volcado
    #
    ############################################################################
    

    print("\n")
    comercio_central = get_comercio_central_from_volcado(volcado)
    cuenta = get_cuenta_from_volcado(volcado)
    representante = get_representante_from_volcado(volcado)
    sucursal = get_sucursal_from_volcado(volcado)
    terminal = get_terminal_from_volcado(volcado)

    sucursal.add_terminal(terminal)

    entidades.comercioCentral = comercio_central
    entidades.add_cuenta_bancaria(cuenta)
    entidades.add_representante_legal(representante)
    entidades.add_sucursal(sucursal)

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

    proceso = ProcesoVolcado(manager, result)
    proceso.procesarComercio(entidades)

    # Este código lee un archivo Excel con la información de un comercio y generar los
    # request para hacer el volcado según el camino tradicional (sin multiplicidad).
    # Estamos mostrando cada request en pantalla

    # region

    # Preparando request para VolcadoComercio:
    # comercio_register = Register.from_volcado_comercio(volcado)
    # print("Request para volcado comercio. ")
    # if DEBUG:
    #     print(comercio_register.to_json())
    #     print ("\n")

    # # Preparando request para Volcado Sucursal
    # branch_register = BranchRegister.from_volcado_comercio(volcado)
    # print("Request para volcado sucursal. ")
    # if DEBUG:
    #     print(branch_register.to_json())
    #     print("\n")

    # # Preparando request para Volcado Servicio Sucursal
    # branch_service_register = ServiceRegister.from_volcado_comercio(volcado)
    # print("Request para volcado servicio sucursal. ")
    # if DEBUG:
    #     print(branch_service_register.to_json())
    #     print("\n")

    # # Preparando volcado para Representante Legal
    # representante_register = RepresentativeRegister.from_volcado_comercio(volcado)
    # print("Request para volcado de representante legal. ")
    # if DEBUG:
    #     print(representante_register.to_json())
    #     print("\n")

    # # Preparando volcado de cuenta bancaria
    # cuenta_register = BankAccountRegister.from_volcado_comercio(volcado)
    # print("Request para volcado de cuenta bancaria. ")
    # if DEBUG:
    #     print(cuenta_register.to_json())
    #     print("\n")

    # payment_type_register = PaymentTypeRegister.from_volcado_comercio(volcado)
    # print("Request para volcado de payment type. ")
    # if DEBUG:
    #     print(payment_type_register.to_json())
    #     print("\n")

    # contract_register = ContractRegister.from_volcado_comercio(volcado)
    # print("Request para volcado de contrato. ")
    # if DEBUG:
    #     print(contract_register.to_json())
    #     print("\n")

    # merchant_register = MerchantDiscountRegister.from_volcado_comercio(volcado)
    # print("Request para volcado de merchant discount. ")
    # if DEBUG:
    #     print(merchant_register.to_json())
    #     print("\n")

    # terminal_register = TerminalRegister.from_volcado_comercio(volcado)
    # print("Request para volcado de terminal. ")
    # if DEBUG:
    #     print(terminal_register.to_json())
    #     print("\n")

    # bank_account_register = BankAccountRegister.from_volcado_comercio(volcado)
    # print("Request para creación de cuenta bancaria. ")
    # if DEBUG:
    #     print(bank_account_register.to_json())
    #     print("\n")

    # bank_config_register = BankAccConfigRegister.from_volcado_comercio(volcado)
    # print("Request para volcado de configuración de cuenta bancaria. ")
    # if DEBUG:
    #     print(bank_config_register.to_json())
    #     print("\n")

    # branch_cc_register = BranchCCRegister.from_volcado_comercio(volcado)
    # print("Request para volcado Branch CC. ")
    # if DEBUG:
    #     print(branch_cc_register.to_json())
    #     print("\n")

    # terminal_cc_register = TerminalCCRegister.from_volcado_comercio(volcado)
    # print("Request para terminal CC. ")
    # if DEBUG:
    #     print(terminal_cc_register.to_json())
    #     print("\n")

    # iswitch_commerce_register = IswitchCommerceRegister.from_volcado_comercio(volcado)
    # print("Request para volcado de comercio en Iswitch. ")
    # if DEBUG:
    #     print(iswitch_commerce_register.to_json())
    #     print("\n")

    # iswitch_branch_register = IswitchBranchRegister.from_volcado_comercio(volcado)
    # print("Request para volcado de sucursal en Iswitch. ")
    # if DEBUG:
    #     print(iswitch_branch_register.to_json())
    #     print("\n")

    # iswitch_terminal_register = IswitchTerminalRegister.from_volcado_comercio(volcado)
    # print("Request para volcado de terminal en Iswitch. ")
    # if DEBUG:
    #     print(iswitch_terminal_register.to_json())
    #     print("\n")

    # commerce_pci_register = CommercePciRegister.from_volcado_comercio(volcado)
    # print("Request para volcado de comercio en réplica PCI. ")
    # if DEBUG:
    #     print(commerce_pci_register.to_json())
    #     print("\n")

    # commerce_switch_register = CommerceSwitchRegister.from_volcado_comercio(volcado)
    # print("Request para volcado de comercio en switch. ")
    # if DEBUG:
    #     print(commerce_switch_register.to_json())
    #     print("\n")

    # ticket_register = TicketRegister.from_volcado_comercio(volcado)
    # print("Request para volcado para ticket de comercio. ")
    # if DEBUG:
    #     print(ticket_register.to_json())
    #     print("\n")

    # monitor_register = MonitorRegister.from_volcado_comercio(volcado)
    # print("Request para volcado en Monitor Plus. ")
    # if DEBUG:
    #     print(monitor_register.to_json())
    #     print("\n")

    # red_pos_register = RedPosRegister.from_volcado_comercio(volcado)
    # print("Request para volcado de ticket en RedPos. ")
    # if DEBUG:
    #     print(red_pos_register.to_json())
    #     print("\n")


    # Este flujo de acá permitirá poder analizar pasos de volcado uno por uno, para evitar
    # reintentar volcados ya ejecutados durante el período de pruebas

    # print ("Comenzando volcado...")
    # print("los pasos serán los siguientes:")

    # step_list = '''    1. VolcadoComercio
    # 2. VolcadoTicket
    # 3. VolcadoSucursal
    # 4. VolcadoRepresentante
    # 5. VolcadoServicio
    # 6. VolcadoTipoPago
    # 7. VolcadoMerchant
    # 8. VolcadoTerminal
    # 9. VolcadoContrato
    # 10. VolcadoCuentaBancaria
    # 11. VolcadoConfiguraciónCuenta
    # 12. VolcadoCCSucursal
    # 13. VolcadoCCTerminal
    # 14. VolcadoIswitchComercio
    # 15. VolcadoIswitchSucursal
    # 16. VolcadoIswitchTerminal
    # 17. VolcadoPci
    # 18. VolcadoSwitch
    # 19. VolcadoMonitor
    # 20. VolcadoRedPos
    # '''

    # print(step_list)

    # # Selección del paso del que empezaremos a trabajar el volcado
    # seleccion_usuario = input("Ingrese el paso desde el cuál empezar (por defecto 1): ")
    # seleccion = int(seleccion_usuario) if seleccion_usuario else 1

    # print(f'El paso seleccionado es el {seleccion} \n')

    # # Marcar el tiempo de inicio para medir desempeño
    # start_time = time.time()

    # # Variable para descontar timeout de Monitor Plus
    # elapsed_monitor = 0.0

    # # Generación de objeto de resultado
    # result = ResultadoVolcado()
    # if DEBUG:
    #     print("Objeto resultado creado...")    
    #     print(result)
    #     print("\n")

    # endregion
    
    
    # region

    # Comenzando el volcado como tal
    # Partimos por revisar si el servicio está contestando

    # if manager.isResponding():

    #     # Indicador de errores en proceso
    #     FOUND_ERRORS = False

    #     print("Servicio contestando en forma correcta...")

    #     # Si empezamos en el paso 1
    #     if seleccion <= 1 and not FOUND_ERRORS:

    #         comercio_result = CommerceResult()
    #         exito = manager.volcadoComercio(comercio_register, comercio_result)
    #         if exito:
    #             print("Volcado de comercio correcto, resultado hasta el momento:")

    #             # Agregar el mensaje a los volcados
    #             result.ComercioCentral.AdditionalMessages.Volcados.append(Mensaje(comercio_result.source,
    #                                                                               comercio_result.message))
                
    #             # Agregar valores de salida
    #             result.ComercioCentral.commerce_id = comercio_result.commerce_id
    #             result.ComercioCentral.agreement_id = comercio_result.agreement_id
    #             result.ComercioCentral.entry = comercio_result.entry

    #             if DEBUG:
    #                 print(result)
    #                 input("\nPresione ENTER para continuar...")

    #         else:
    #             print("Hubo un problema con el volcado de comercio")

    #             # Agregar el mensaje a los errores
    #             result.ComercioCentral.Errors.Errors.append(Mensaje(comercio_result.source,
    #                                                                 comercio_result.message))
    #             print(result)
    #             FOUND_ERRORS = True

    #         # Dejar espacio para la legibilidad de la respuesta
    #         print("\n\n")


    #     # Si empezamos en el paso 2
    #     if seleccion <= 2 and not FOUND_ERRORS:

    #         ticket_result = TicketResult()
    #         exito = manager.volcadoTicket(ticket_register, ticket_result)
            
    #         # Si retornó True
    #         if exito:
    #             print("Volcado de ticket correcto, resultado hasta el momento:")
                
    #             # Agregar valores de respuesta
    #             result.ComercioCentral.AdditionalMessages.Volcados.append(Mensaje(ticket_result.source,
    #                                                                      ticket_result.message))
                
    #             # Guardar parámetro de salida
    #             result.ComercioCentral.ComercioTicketDateAndTime = (ticket_result.date + " " + ticket_result.time) if ticket_result.date and ticket_result.time else ""
                
    #             if DEBUG:
    #                 print(result)
    #                 input("\nPresione ENTER para continuar..")

    #         # Si retornó False
    #         else:
    #             print("Hubo un problema con el volcado de ticket")

    #             # Agregar mensaje de error
    #             result.ComercioCentral.Errors.Errors.append(Mensaje(ticket_result.source,
    #                                                                 ticket_result.message))
                
    #             print(result)
    #             FOUND_ERRORS = True
            
    #         # Dejar espacio para la legibilidad de la respuesta
    #         print("\n\n")


    #     # Si empezamos en el paso 3
    #     if seleccion <= 3 and not FOUND_ERRORS:
            
    #         # Usar parámetro diferidos
    #         branch_register.commerceId = result.ComercioCentral.commerce_id
            
    #         # Generar objeto de resultado y llamar a la función de volcado
    #         branch_result = BranchResult()
    #         exito = manager.volcadoSucursal(branch_register, branch_result)
    #         if exito:
    #             print("Volcado de sucursal correcto, resultado hasta el momento:")

    #             # Agregar valores de respuesta
    #             result.Sucursales[0].AdditionalMessages.Volcados.append(Mensaje(branch_result.source,
    #                                                                    branch_result.message))
                
    #             # Agregar parámetros de salida
    #             result.Sucursales[0].branch_id = branch_result.branch_id
    #             result.Sucursales[0].entity_id = branch_result.entity_id
    #             result.Sucursales[0].local_code = branch_result.local_code

    #             if DEBUG:
    #                 print(result)
    #                 input("\nPresione ENTER para continuar..")

    #         else:
    #             print("Hubo un problema con el volcado de sucursal")

    #             # Agregar a los mensajes de error
    #             result.Sucursales[0].Errors.Errors.append(Mensaje(branch_result.source, branch_result.message))
    #             print(result)

    #             FOUND_ERRORS = True

    #         # Dejar espacio para la legibilidad de la respuesta
    #         print("\n\n")


    #     # Si empezamos en el paso 4
    #     if seleccion <= 4 and not FOUND_ERRORS:
    #         representante_register.commerceId = result.ComercioCentral.commerce_id
    #         representante_result = ResultFuncion()
    #         exito = manager.volcadoRepresentanteLegal(representante_register, representante_result)

    #         # Si retornó True
    #         if exito:
    #             print("Volcado de representante correcto: resultado hasta el momento:")
            
    #             # Agregar el mensaje a los volcados
    #             result.RepresentanteLegal[0].AdditionalMessages.Volcados.append(Mensaje(representante_result.source,
    #                                                                      representante_result.message))
                
    #             # Guardar información del representante
    #             result.RepresentanteLegal[0].wasSuccessful = True
    #             result.RepresentanteLegal[0].responseMessage = "Representante legal creado"
                
    #             # Imprimir el objeto resultado si está en DEBUG 
    #             if DEBUG:
    #                 print(result)
    #                 input("\nPresione cualquier tecla para continuar..")

    #         # Si retornó False                
    #         else:
    #             print("Hubo un problema con el volcado de representante")

    #             #Agregar el mensaje a los errores y detener
    #             result.RepresentanteLegal[0].Errors.Errors.append(Mensaje(representante_result.source,
    #                                                                      representante_result.message))
    #             print(result)
    #             FOUND_ERRORS = True

    #         # Dejar espacio para la legibilidad de la respuesta
    #         print("\n\n")


    #     # Paso 5: Servicio sucursal
    #     if seleccion <= 5 and not FOUND_ERRORS:

    #         # Asignar valor diferido
    #         branch_service_register.branchId = result.Sucursales[0].branch_id

    #         service_branch_result = ServiceResult()
    #         exito = manager.volcadoServicioSucursal(branch_service_register, service_branch_result)

    #         # Si retornó True
    #         if exito:
    #             print("Volcado de servicio sucursal correcto: resultado hasta el momento:")
            
    #             # Agregar el mensaje a los volcados
    #             result.Sucursales[0].AdditionalMessages.Volcados.append(Mensaje(service_branch_result.source,
    #                                                                      service_branch_result.message))
                
    #             # Guardar parámetros de salida
    #             result.Sucursales[0].service_branch_id = service_branch_result.service_branch_id
                
    #             # Imprimir el objeto resultado    
    #             if DEBUG:
    #                 print(result)
    #                 input("\nPresione cualquier tecla para continuar..")

    #         # Si retornó False                
    #         else:
    #             print("Hubo un problema con el volcado de servicio de sucursal")

    #             #Agregar el mensaje a los errores y detener
    #             result.Sucursales[0].Errors.Errors.append(Mensaje(service_branch_result.source,
    #                                                                      service_branch_result.message))
    #             print(result)
    #             FOUND_ERRORS = True

    #         # Dejar espacio para la legibilidad de la respuesta
    #         print("\n\n")    
        

    #     # Paso 6: Payment types
    #     if seleccion <= 6 and not FOUND_ERRORS:
            
    #         # Agregar valores diferidos
    #         payment_type_register.branchCode = result.Sucursales[0].branch_id
    #         payment_type_register.serviceBranchId = result.Sucursales[0].service_branch_id
    #         payment_type_register.branchEntityId = result.Sucursales[0].entity_id
            
    #         # Creación de objeto resultado y llamada al servicio del manager de volcados
    #         payment_type_result = PaymentTypeResult()
    #         exito = manager.volcadoPaymentType(payment_type_register, payment_type_result)

    #         # Si retornó True
    #         if exito:
    #             print("Volcado de payment type correcto: resultado hasta el momento:")
            
    #             # Agregar el mensaje a los volcados
    #             result.Sucursales[0].AdditionalMessages.Volcados.append(Mensaje(payment_type_result.source,
    #                                                                      payment_type_result.message))
    #             print("Resultado recuperado:")
    #             print(payment_type_result.payment_type_id)                                                        
    #             result.Sucursales[0].paymentTypeIds = payment_type_result.payment_type_id

    #             # Imprimir el objeto resultado si está en DEBUG    
    #             if DEBUG:
    #                 print(result)
    #                 input("\nPresione cualquier tecla para continuar..")

    #         # Si retornó False                
    #         else:
    #             print("Hubo un problema con el volcado de payment type")

    #             #Agregar el mensaje a los errores y detener
    #             result.Sucursales[0].Errors.Errors.append(Mensaje(payment_type_result.source,
    #                                                                      payment_type_result.message))
    #             print(result)
    #             FOUND_ERRORS = True

    #         # Dejar espacio para la legibilidad de la respuesta
    #         print("\n\n")


    #     # Paso 7: Merchant discount
    #     if seleccion <= 7 and not FOUND_ERRORS:
            
    #         # Agregar los valores diferidos
    #         merchant_register.branchCode = result.Sucursales[0].local_code
    #         merchant_register.branchServiceId = result.Sucursales[0].service_branch_id
            
    #         # Crear objeto de resultado y llamar a volcado a través del manager
    #         merchant_result = ResultFuncion()
    #         exito = manager.volcadoMerchantDiscount(merchant_register, merchant_result)

    #         # Si retornó True
    #         if exito:
    #             print("Volcado de merchant discount correcto: resultado hasta el momento:")
            
    #             # Agregar el mensaje a los volcados
    #             result.Sucursales[0].AdditionalMessages.Volcados.append(Mensaje(merchant_result.source,
    #                                                                      merchant_result.message))
                
    #             # Imprimir el objeto resultado si está en DEBUG   
    #             if DEBUG:
    #                 print(result)
    #                 input("\nPresione ENTER para continuar..")

    #         # Si retornó False                
    #         else:
    #             print("Hubo un problema con el volcado de merchant discount")

    #             #Agregar el mensaje a los errores y detener
    #             result.Sucursales[0].Errors.Errors.append(Mensaje(merchant_result.source,
    #                                                                      merchant_result.message))
    #             print(result)
    #             FOUND_ERRORS = True

    #         # Dejar espacio para la legibilidad de la respuesta
    #         print("\n\n")
    

    #     # Paso 8: Terminal
    #     if seleccion <= 8 and not FOUND_ERRORS:
    #         # Agregar los valores diferidos al request
    #         terminal_register.branchCode = result.Sucursales[0].local_code
    #         terminal_register.contractId = str(result.ComercioCentral.agreement_id)
            
    #         # Crear el objeto de resultado y llamar al volcado a través del manager
    #         terminal_result = TerminalResult()
    #         exito = manager.volcadoTerminal(terminal_register, terminal_result)

    #         # Si retornó True
    #         if exito:
    #             print("Volcado de terminal: resultado hasta el momento:")

    #             # Capturar datos del resultado
    #             result.Sucursales[0].Terminals[0].terminal = terminal_result.terminal
    #             result.Sucursales[0].Terminals[0].collector = terminal_result.collector
    #             result.Sucursales[0].Terminals[0].billing_price = terminal_result.billing_price
            
    #             # Agregar el mensaje a los volcados
    #             result.Sucursales[0].Terminals[0].AdditionalMessages.Volcados.append(Mensaje(terminal_result.source,
    #                                                                      terminal_result.message))
                
    #             # Imprimir el objeto resultado si está en DEBUG    
    #             if DEBUG:
    #                 print(result)
    #                 input("\nPresione ENTER para continuar..")

    #         # Si retornó False                
    #         else:
    #             print("Hubo un problema con el volcado de terminal")

    #             #Agregar el mensaje a los errores y detener
    #             result.Sucursales[0].Terminals[0].Errors.Errors.append(Mensaje(terminal_result.source,
    #                                                                      terminal_result.message))
    #             print(result)
    #             FOUND_ERRORS = True

    #         # Dejar espacio para la legibilidad de la respuesta
    #         print("\n\n")


    #     # Paso 9: Contrato
    #     if seleccion <= 9 and not FOUND_ERRORS:
            
    #         # Crear el objeto de resultado y llamar al volcado a través del manager
    #         contract_result = ContratoResult()
    #         exito = manager.volcadoContrato(contract_register, contract_result)

    #         # Si retornó True
    #         if exito:
    #             print("Volcado de contrato correcto: resultado hasta el momento:")

    #             # Capturar datos del resultado
    #             result.ComercioCentral.ContratoDateAndTime = (contract_result.date + " " + contract_result.time) if contract_result.date and contract_result.time else ""
            
    #             # Agregar el mensaje a los volcados
    #             result.ComercioCentral.AdditionalMessages.Volcados.append(Mensaje(contract_result.source,
    #                                                                      contract_result.message))
                
    #             # Imprimir el objeto resultado si está en DEBUG    
    #             if DEBUG:
    #                 print(result)
    #                 input("\nPresione ENTER para continuar..")

    #         # Si retornó False                
    #         else:
    #             print("Hubo un problema con el volcado de contrato")

    #             #Agregar el mensaje a los errores y detener
    #             result.ComercioCentral.Errors.Errors.append(Mensaje(contract_result.source,
    #                                                                      contract_result.message))
    #             print(result)
    #             FOUND_ERRORS = True

    #         # Dejar espacio para la legibilidad de la respuesta
    #         print("\n\n")
        

    #     # Paso 10: Cuenta Bancaria
    #     if seleccion <= 10 and not FOUND_ERRORS:

    #         bank_account_result = BankAccountResult()
    #         exito = manager.volcadoCuentaBancaria(bank_account_register, bank_account_result)

    #         # Si retornó True
    #         if exito:
    #             print("Volcado de cocuenta bancaria: resultado hasta el momento:")

    #             # Capturar datos del resultado
    #             result.CuentaBancaria[0].accountId = bank_account_result.account_id
            
    #             # Agregar el mensaje a los volcados
    #             result.CuentaBancaria[0].AdditionalMessages.Volcados.append(Mensaje(bank_account_result.source,
    #                                                                      bank_account_result.message))
                
    #             # Imprimir el objeto resultado    
    #             if DEBUG:
    #                 print(result)
    #                 input("\nPresione ENTER para continuar..")

    #         # Si retornó False                
    #         else:
    #             print("Hubo un problema con el volcado de la cuenta bancaria")

    #             #Agregar el mensaje a los errores y detener
    #             result.CuentaBancaria[0].Errors.Errors.append(Mensaje(bank_account_result.source,
    #                                                                      bank_account_result.message))
    #             print(result)
    #             FOUND_ERRORS = True

    #         # Dejar espacio para la legibilidad de la respuesta
    #         print("\n\n")
        

    #     # Paso 11: Configuración de cuenta bancaria
    #     if seleccion <= 11 and not FOUND_ERRORS:

    #         # Datos diferidos
    #         bank_config_register.accountId = result.CuentaBancaria[0].accountId
    #         bank_config_register.localCode = result.Sucursales[0].local_code

    #         bank_config_result = ResultFuncion()
    #         exito = manager.volcadoConfiguracionCuentaBancaria(bank_config_register, bank_config_result)

    #         # Si retornó True
    #         if exito:
    #             print("Volcado de configuración de cuenta bancaria: resultado hasta el momento:")
                
    #             # Agregar el mensaje a los volcados
    #             # Dado que la cuenta debe asociarse con la sucursal, ponemos a que sucursal quedó asociada
    #             # Esta va a ser necesario para múltiples sucursales
    #             mensaje_config_cuenta = bank_config_result.message + " para sucursal " + bank_config_register.localCode
    #             result.CuentaBancaria[0].AdditionalMessages.Volcados.append(Mensaje(bank_config_result.source,
    #                                                                      mensaje_config_cuenta))
                
    #             # Imprimir el objeto resultado    
    #             if DEBUG:
    #                 print(result)
    #                 input("\nPresione ENTER para continuar..")

    #         # Si retornó False                
    #         else:
    #             print("Hubo un problema con el volcado de configuración de cuenta bancaria")

    #             #Agregar el mensaje a los errores y detener
    #             result.CuentaBancaria[0].Errors.Errors.append(Mensaje(bank_config_result.source,
    #                                                                      bank_config_result.message))
    #             print(result)
    #             FOUND_ERRORS = True
            
    #         # Dejar espacio para la legibilidad de la respuesta
    #         print("\n\n")

        
    #     # Paso 12: Condiciones comerciales de sucursal
    #     if seleccion <= 12 and not FOUND_ERRORS:

    #         # Datos diferidos
    #         branch_cc_register.branchCode = result.Sucursales[0].local_code

    #         branch_cc_result = ResultFuncion()
    #         exito = manager.volcadoBranchCC(branch_cc_register, branch_cc_result)

    #         # Si retornó True
    #         if exito:
    #             print("Volcado condiciones comerciales de sucursal: resultado hasta el momento:")
            
    #             # Agregar el mensaje a los volcados
    #             result.Sucursales[0].AdditionalMessages.Volcados.append(Mensaje(branch_cc_result.source,
    #                                                                      branch_cc_result.message))
                
    #             # Imprimir el objeto resultado si está en DEBUG   
    #             if DEBUG:
    #                 print(result)
    #                 input("\nPresione ENTER para continuar..")

    #         # Si retornó False                
    #         else:
    #             print("Hubo un problema con el volcado de condiciones comerciales de sucursal")

    #             #Agregar el mensaje a los errores y detener
    #             result.Sucursales[0].Errors.Errors.append(Mensaje(branch_cc_result.source,
    #                                                                      branch_cc_result.message))
    #             print(result)
    #             FOUND_ERRORS = True

    #         # Dejar espacio para la legibilidad de la respuesta
    #         print("\n\n")
        

    #     # Paso 13: Condiciones comerciales de terminal
    #     if seleccion <= 13 and not FOUND_ERRORS:

    #         # Datos diferidos
    #         terminal_cc_register.terminalNumber = result.Sucursales[0].Terminals[0].terminal
    #         terminal_cc_register.branchCode = result.Sucursales[0].local_code

    #         # Crear objeto de resultado y llamar a volcado a través del manager
    #         terminal_cc_result = ResultFuncion()
    #         exito = manager.volcadoTerminalCC(terminal_cc_register, terminal_cc_result)

    #         # Si retornó True
    #         if exito:
    #             print(f"Volcado de condiciones comerciales del terminal {terminal_cc_register.terminalNumber}: resultado hasta el momento:")
            
    #             # Agregar el mensaje a los volcados
    #             result.Sucursales[0].Terminals[0].AdditionalMessages.Volcados.append(Mensaje(terminal_cc_result.source,
    #                                                                      terminal_cc_result.message))
                
    #             # Imprimir el objeto resultado    
    #             if DEBUG:
    #                 print(result)
    #                 input("\nPresione ENTER para continuar..")

    #         # Si retornó False                
    #         else:
    #             print(f"Hubo un problema con el volcado de condiciones comerciales del terminal {terminal_cc_register.terminalNumber}")

    #             #Agregar el mensaje a los errores y detener
    #             result.Sucursales[0].Terminals[0].Errors.Errors.append(Mensaje(terminal_cc_result.source,
    #                                                                      terminal_cc_result.message))
    #             print(result)
    #             FOUND_ERRORS = True

    #         # Dejar espacio para la legibilidad de la respuesta
    #         print("\n\n")
        

    #     # Paso 14: Volcado de comercio en ISWITCH
    #     if seleccion <= 14 and not FOUND_ERRORS:

    #         # Crear objeto de resultado y llamar al volcado a través del manager
    #         iswitch_commerce_result = ResultFuncion()
    #         exito = manager.volcadoIswitchComercio(iswitch_commerce_register, iswitch_commerce_result)

    #         # Si retornó True
    #         if exito:
    #             print("Volcado de comercio en ISWITCH correcto: resultado hasta el momento:")
            
    #             # Agregar el mensaje a los volcados
    #             result.ComercioCentral.AdditionalMessages.Volcados.append(Mensaje(iswitch_commerce_result.source,
    #                                                                      iswitch_commerce_result.message))
                
    #             # Imprimir el objeto resultado    
    #             if DEBUG:
    #                 print(result)
    #                 input("\nPresione ENTER para continuar..")

    #         # Si retornó False                
    #         else:
    #             print("Hubo un problema con el volcado de comercio en ISWITCH")

    #             #Agregar el mensaje a los errores y detener
    #             result.ComercioCentral.Errors.Errors.append(Mensaje(iswitch_commerce_result.source,
    #                                                                      iswitch_commerce_result.message))
    #             print(result)
    #             FOUND_ERRORS = True

    #         # Dejar espacio para la legibilidad de la respuesta
    #         print("\n\n")

        
    #     # Paso 15: Volcado de sucursal en ISWITCH
    #     if seleccion <= 15 and not FOUND_ERRORS:

    #         iswitch_branch_register.localCode = result.Sucursales[0].local_code

    #         iswitch_branch_result = IswitchBranchResult()
    #         exito = manager.volcadoIswitchBranch(iswitch_branch_register, iswitch_branch_result)

    #         # Si retornó True
    #         if exito:
    #             print(f"Volcado de comercio en ISWITCH con sucursal {iswitch_branch_register.localCode} correcto: resultado hasta el momento:")
            
    #             # Agregar el mensaje a los volcados
    #             result.Sucursales[0].AdditionalMessages.Volcados.append(Mensaje(iswitch_branch_result.source,
    #                                                                      iswitch_branch_result.message))
                
                
    #             # Capturar el resultado (en realidad, en este servicio no viene el dato)
    #             result.Sucursales[0].branchIswId = iswitch_branch_result.branchIswId
                
    #             # Imprimir el objeto resultado    
    #             if DEBUG:
    #                 print(result)
    #                 input("\nPresione ENTER para continuar..")

    #         # Si retornó False                
    #         else:
    #             print(f"Hubo un problema con el volcado de comercio en ISWITCH con sucursal {iswitch_branch_register.localCode}")

    #             #Agregar el mensaje a los errores y detener
    #             result.Sucursales[0].Errors.Errors.append(Mensaje(iswitch_branch_result.source,
    #                                                                      iswitch_branch_result.message))
    #             print(result)
    #             FOUND_ERRORS = True

    #         # Dejar espacio para la legibilidad de la respuesta
    #         print("\n\n")

        
    #     # Paso 16: Volcado de terminal en ISWITCH
    #     if seleccion <= 16 and not FOUND_ERRORS:

    #         # Dato diferido
    #         iswitch_terminal_register.terminalNumber = str(result.Sucursales[0].Terminals[0].terminal)

    #         iswitch_terminal_result = IswitchBranchResult()
    #         exito = manager.volcadoIswitchTerminal(iswitch_terminal_register, iswitch_terminal_result)

    #         # Si retornó True
    #         if exito:
    #             print(f"Volcado de terminal {iswitch_terminal_register.terminalNumber} en ISWITCH correcto: resultado hasta el momento:")
            
    #             # Agregar el mensaje a los volcados
    #             result.Sucursales[0].Terminals[0].AdditionalMessages.Volcados.append(Mensaje(iswitch_terminal_result.source,
    #                                                                      iswitch_terminal_result.message))
                
    #             # Imprimir el objeto resultado    
    #             if DEBUG:
    #                 print(result)
    #                 input("\nPresione ENTER para continuar..")

    #         # Si retornó False                
    #         else:
    #             print(f"Hubo un problema con el volcado de terminal {iswitch_terminal_register.terminalNumber} en ISWITCH")

    #             #Agregar el mensaje a los errores y detener
    #             result.Sucursales[0].Terminals[0].Errors.Errors.append(Mensaje(iswitch_terminal_result.source,
    #                                                                      iswitch_terminal_result.message))
    #             print(result)
    #             FOUND_ERRORS = True

    #         # Dejar espacio para la legibilidad de la respuesta
    #         print("\n\n")
        

    #     # Paso 17: Volcado de comercio en réplica PCI
    #     if seleccion <= 17 and not FOUND_ERRORS:

    #         # Dato diferido
    #         commerce_pci_register.branchCode = result.Sucursales[0].local_code

    #         commerce_pci_result = ResultFuncion()
    #         exito = manager.volcadoCommercePci(commerce_pci_register, commerce_pci_result)

    #         # Si retornó True
    #         if exito:
    #             print(f"Volcado de comercio en réplica PCI para sucursal {commerce_pci_register.branchCode} correcto: resultado hasta el momento:")
            
    #             # Agregar el mensaje a los volcados
    #             result.Sucursales[0].AdditionalMessages.Volcados.append(Mensaje(commerce_pci_result.source,
    #                                                                      commerce_pci_result.message))
                
    #             # Imprimir el objeto resultado    
    #             if DEBUG:
    #                 print(result)
    #                 input("\nPresione ENTER para continuar..")

    #         # Si retornó False                
    #         else:
    #             print(f"Hubo un problema con el volcado de comercio en réplica PCI para sucursal {commerce_pci_register.branchCode}")

    #             #Agregar el mensaje a los errores y detener
    #             result.Sucursales[0].Errors.Errors.append(Mensaje(commerce_pci_result.source,
    #                                                                      commerce_pci_result.message))
    #             print(result)
    #             FOUND_ERRORS = True

    #         # Dejar espacio para la legibilidad de la respuesta
    #         print("\n\n")


    #     # Paso 18: Volcado de comercio en Switch
    #     if seleccion <= 18 and not FOUND_ERRORS:

    #         # Dato diferido
    #         commerce_switch_register.branchCode = result.Sucursales[0].local_code

    #         commerce_switch_result = ResultFuncion()
    #         exito = manager.volcadoCommerceSwitch(commerce_switch_register, commerce_switch_result)

    #         # Si retornó True
    #         if exito:
    #             print(f"Volcado de comercio en switch, sucursal {commerce_switch_register.branchCode}: resultado hasta el momento:")
            
    #             # Agregar el mensaje a los volcados
    #             result.Sucursales[0].AdditionalMessages.Volcados.append(Mensaje(commerce_switch_result.source,
    #                                                                      commerce_switch_result.message))
                
    #             # Imprimir el objeto resultado    
    #             if DEBUG:
    #                 print(result)
    #                 input("\nPresione ENTER para continuar..")

    #         # Si retornó False                
    #         else:
    #             print(f"Hubo un problema con el volcado de comercio en switch, sucursal {commerce_switch_register.branchCode}")

    #             #Agregar el mensaje a los errores y detener
    #             result.Sucursales[0].Errors.Errors.append(Mensaje(commerce_switch_result.source,
    #                                                                      commerce_switch_result.message))
    #             print(result)
    #             FOUND_ERRORS = True

    #         # Dejar espacio para la legibilidad de la respuesta
    #         print("\n\n")


    #     # Paso 19: Volcado de comercio en Monitor Plus (problemas de timeout)
    #     if seleccion <= 19 and not FOUND_ERRORS:

    #         # Dato diferido
    #         monitor_register.branchCode = result.Sucursales[0].local_code

    #         monitor_result = MonitorResult()
    #         start_monitor = time.time() 
    #         exito = manager.volcadoMonitorPlus(monitor_register, monitor_result)

    #         # Si retornó True
    #         if exito:
    #             end_monitor = time.time()
    #             elapsed_monitor = end_monitor - start_monitor
    #             print("Volcado de comercio en Monitor Plus: resultado hasta el momento:")
            
    #             # Agregar el mensaje a los volcados
    #             result.Sucursales[0].AdditionalMessages.Volcados.append(Mensaje(monitor_result.source,
    #                                                                      monitor_result.message))
                
    #             # Agregar hora y fecha de ejemplo, dado que el servicio tiene timeout
    #             result.Sucursales[0].MonitorPlusDateAndTime = '14/03/2025 15:00'
                
    #             # Imprimir el objeto resultado    
    #             if DEBUG:
    #                 print(result)
    #                 input("\nPresione ENTER para continuar..")

    #         # Si retornó False                
    #         else:
    #             print("Hubo un problema con el volcado de comercio en Monitor Plus")

    #             #Agregar el mensaje a los errores y detener
    #             result.Sucursales[0].Errors.Errors.append(Mensaje(monitor_result.source,
    #                                                                      monitor_result.message))
    #             print(result)
    #             FOUND_ERRORS = True

    #         # Dejar espacio para la legibilidad de la respuesta
    #         print("\n\n")

        
    #     # Paso 20: Volcado de ticket en RedPos
    #     if seleccion <= 20 and not FOUND_ERRORS:

    #         # Dato de terminal diferido
    #         red_pos_register.terminalNumber = str(result.Sucursales[0].Terminals[0].terminal)

    #         red_pos_result = RedPosResult()
    #         exito = manager.volcadoRedPos(red_pos_register, red_pos_result)

    #         # Si retornó True
    #         if exito:
    #             print("Volcado de ticket en RedPos correcto: resultado hasta el momento:")
    #             print(f"Número de ticket: {red_pos_result.ticket} ")
            
    #             # Agregar el mensaje a los volcados
    #             result.Sucursales[0].Terminals[0].AdditionalMessages.Volcados.append(Mensaje(red_pos_result.source,
    #                                                                      red_pos_result.message))
                
    #             # Actualmente no es posible guardar el valor del ticket en el objeto resultado

    #             # Imprimir el objeto resultado    
    #             if DEBUG:
    #                 print(result)
    #                 input("\nPresione ENTER para continuar..")

    #         # Si retornó False                
    #         else:
    #             print("Hubo un problema con el volcado de ticket en RedPos")

    #             #Agregar el mensaje a los errores y detener
    #             result.Sucursales[0].Terminals[0].Errors.Errors.append(Mensaje(red_pos_result.source,
    #                                                                      red_pos_result.message))
    #             print(result)
    #             FOUND_ERRORS = True

    #         # Dejar espacio para la legibilidad de la respuesta
    #         print("\n\n")


    #     # Medir el tiempo de cierre y el total
    #     finish_time = time.time()
    #     elapsed_time = finish_time - start_time
    #     adjusted_time = elapsed_time - elapsed_monitor
        
    #     # Resultados
    #     print(result)
    #     print("Proceso de volcado concluido correctamente!")
    #     print(f"Tiempo total transcurrido: {elapsed_time} segundos")
    #     print(f'Tiempo transcurrido descontando la espera por Monitor Plus: {adjusted_time}')

    # endregion




