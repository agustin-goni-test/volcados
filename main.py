from inputvolcados import Comercio, Sucursal, VolcadoComercio
from registrosvolcado import RepresentativeRegister, Register, BranchRegister, ServiceRegister, BankAccountRegister
from registrosvolcado import PaymentTypeRegister, ContractRegister, MerchantDiscountRegister, TerminalRegister
from registrosvolcado import BankAccConfigRegister, BranchCCRegister, TerminalCCRegister, IswitchCommerceRegister
from registrosvolcado import IswitchBranchRegister, IswitchTerminalRegister, CommercePciRegister, CommerceSwitchRegister
from registrosvolcado import TicketRegister, MonitorRegister, RedPosRegister
from volcadomanager import VolcadoManager
from resultvolcado import ResultadoVolcado, ResultFuncion, Mensaje, ServiceResult, PaymentTypeResult, TerminalResult
from resultvolcado import ContratoResult
import requests
import json
from datetime import datetime

# Este código lee un archivo Excel con la información de un comercio y generar los
# request para hacer el volcado según el camino tradicional (sin multiplicidad).
# Estamos mostrando cada request en pantalla

if __name__ == "__main__":
    
    AUTH_TOKEN = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJhcHAiOiJtcy1jZW50cmFsLWFmLWF5Yy1yZWdpc3Ryby1jb21lcmNpbyIsImlzcyI6ImFmLWF5Yy1yZWdpc3Ryby1jb21lcmNpby1jZW50cmFsIn0.gxrgQE6Oae1-gw3Gaif0j3e-uY2sMjR2IWPwRS-5mL0"
    
    file_path = "InfoComercio.xlsx"
    volcado = VolcadoComercio.from_excel(file_path)
    print(volcado.to_json())

    manager = VolcadoManager(AUTH_TOKEN, volcado)

    # Este código lee un archivo Excel con la información de un comercio y generar los
    # request para hacer el volcado según el camino tradicional (sin multiplicidad).
    # Estamos mostrando cada request en pantalla

    # Preparando request para VolcadoComercio:
    comercio_register = Register.from_volcado_comercio(volcado)
    print("Request para volcado comercio: ")
    print(comercio_register.to_json())
    print ("\n")

    # Preparando request para Volcado Sucursal
    branch_register = BranchRegister.from_volcado_comercio(volcado)
    print("Request para volcado sucursal: ")
    print(branch_register.to_json())
    print("\n")

    # Preparando request para Volcado Servicio Sucursal
    branch_service_register = ServiceRegister.from_volcado_comercio(volcado)
    print("Request para volcado servicio sucursal: ")
    print(branch_service_register.to_json())
    print("\n")

    # Preparando volcado para Representante Legal
    representante_register = RepresentativeRegister.from_volcado_comercio(volcado)
    print("Request para volcado de representante legal: ")
    print(representante_register.to_json())
    print("\n")

    # Preparando volcado de cuenta bancaria
    cuenta_register = BankAccountRegister.from_volcado_comercio(volcado)
    print("Request para volcado de cuenta bancaria: ")
    print(cuenta_register.to_json())
    print("\n")

    payment_type_register = PaymentTypeRegister.from_volcado_comercio(volcado)
    print("Request para volcado de payment type: ")
    print(payment_type_register.to_json())
    print("\n")

    contract_register = ContractRegister.from_volcado_comercio(volcado)
    print("Request para volcado de contrato: ")
    print(contract_register.to_json())
    print("\n")

    merchant_register = MerchantDiscountRegister.from_volcado_comercio(volcado)
    print("Request para volcado de merchant discount: ")
    print(merchant_register.to_json())
    print("\n")

    terminal_register = TerminalRegister.from_volcado_comercio(volcado)
    print("Request para volcado de terminal: ")
    print(terminal_register.to_json())
    print("\n")

    bank_config_register = BankAccConfigRegister.from_volcado_comercio(volcado)
    print("Request para volcado de configuración de cuenta bancaria: ")
    print(bank_config_register.to_json())
    print("\n")

    branch_cc_register = BranchCCRegister.from_volcado_comercio(volcado)
    print("Request para volcado Branch CC: ")
    print(branch_cc_register.to_json())
    print("\n")

    terminal_cc_register = TerminalCCRegister.from_volcado_comercio(volcado)
    print("Request para terminal CC: ")
    print(terminal_cc_register.to_json())
    print("\n")

    iswitch_commerce_register = IswitchCommerceRegister.from_volcado_comercio(volcado)
    print("Request para volcado de comercio en Iswitch: ")
    print(iswitch_commerce_register.to_json())
    print("\n")

    iswitch_branch_register = IswitchBranchRegister.from_volcado_comercio(volcado)
    print("Request para volcado de sucursal en Iswitch: ")
    print(iswitch_branch_register.to_json())
    print("\n")

    iswitch_terminal_register = IswitchTerminalRegister.from_volcado_comercio(volcado)
    print("Request para volcado de terminal en Iswitch: ")
    print(iswitch_terminal_register.to_json())
    print("\n")

    commerce_pci_register = CommercePciRegister.from_volcado_comercio(volcado)
    print("Request para volcado de comercio en réplica PCI: ")
    print(commerce_pci_register.to_json())
    print("\n")

    commerce_switch_register = CommerceSwitchRegister.from_volcado_comercio(volcado)
    print("Request para volcado de comercio en switch: ")
    print(commerce_switch_register.to_json())
    print("\n")

    ticket_register = TicketRegister.from_volcado_comercio(volcado)
    print("Request para volcado para ticket de comercio: ")
    print(ticket_register.to_json())
    print("\n")

    monitor_register = MonitorRegister.from_volcado_comercio(volcado)
    print("Request para volcado en Monitor Plus: ")
    print(monitor_register.to_json())
    print("\n")

    red_pos_register = RedPosRegister.from_volcado_comercio(volcado)
    print("Request para volcado de ticket en RedPos: ")
    print(red_pos_register.to_json())
    print("\n")


    # Este flujo de acá permitirá poder analizar pasos de volcado uno por uno, para evitar
    # reintentar volcados ya ejecutados durante el período de pruebas

    print ("Comenzando volcado...")
    print("los pasos serán los siguientes:")

    step_list = '''    1. VolcadoComercio
    2. VolcadoTicket
    3. VolcadoSucursal
    4. VolcadoRepresentante
    5. VolcadoServicio
    6. VolcadoTipoPago
    7. VolcadoMerchant
    8. VolcadoTerminal
    9. VolcadoContrato
    10. VolcadoCuentaBancaria
    11. VolcadoConfiguraciónCuenta
    12. VolcadoCCSucursal
    13. VolcadoCCTerminal
    14. VolcadoIswitchComercio
    15. VolcadoIswitchSucursal
    16. VolcadoIswitchTerminal
    17. VolcadoPci
    18. VolcadoSwitch
    19. VolcadoMonitor
    20. VolcadoRedPos
    '''

    print(step_list)

    # Selección del paso del que empezaremos a trabajar el volcado
    seleccion_usuario = input("Ingrese el paso desde el cuál empezar (por defecto 1)")
    seleccion = int(seleccion_usuario) if seleccion_usuario else 1

    print(f'El paso seleccionado es el {seleccion} \n')

    # Generación de objeto de resultado
    result = ResultadoVolcado()
    print("Objeto resultado creado...")    
    print(result)
    print("\n")

    print("Modificando parámetros... \n")

    result.ComercioCentral.commerce_id = 1324062
    result.ComercioCentral.entry = 189
    result.ComercioCentral.agreement_id = 542470

    result.Sucursales[0].branch_id = 715280
    result.Sucursales[0].entity_id = 1180012
    result.Sucursales[0].local_code = 205273
    result.Sucursales[0].service_branch_id = 9595
    result.Sucursales[0].paymentTypeIds = [
            "10624",
            "10625",
            "10626"
        ]
    
    result.Sucursales[0].Terminals[0].terminal = 5082250
    result.Sucursales[0].Terminals[0].collector = "ISWITCH"
    result.Sucursales[0].Terminals[0].billing_price = "PRECIO_PROMOCION_01"
    

    print(result)


    # Comenzando el volcado como tal
    # Partimos por revisar si el servicio está contestando

    if manager.isResponding():

        # Indicador de errores en proceso
        FOUND_ERRORS = False

        print("Servicio contestando en forma correcta...")

        # Si empezamos en el paso 1
        if seleccion <= 1 and not FOUND_ERRORS:
            exito = manager.volcadoComercio(comercio_register, result)
            if exito:
                print("Volcado de comercio correcto, resultado hasta el momento:")
                print(result)
                input("\nPresione cualquier tecla para continuar...")
            else:
                print("Hubo un problema con el volcado de comercio")
                FOUND_ERRORS = True

        # Si empezamos en el paso 2
        if seleccion <= 2 and not FOUND_ERRORS:
            exito = manager.volcadoTicket(ticket_register, result)
            if exito:
                print("Volcado de ticket correcto, resultado hasta el momento:")
                print(result)
                input("\nPresione cualquier tecla para continuar..")
            else:
                print("Hubo un problema con el volcado de ticket")
                FOUND_ERRORS = True

        # Si empezamos en el paso 3
        if seleccion <= 3 and not FOUND_ERRORS:
            branch_register.commerceId = result.ComercioCentral.commerce_id
            print("Volcaremos la sucursal con este request:")
            print(branch_register.to_json())
            print("\n")
            exito = manager.volcadoSucursal(branch_register, result)
            if exito:
                print("Volcado de sucursal correcto, resultado hasta el momento:")
                print(result)
                input("\nPresione cualquier tecla para continuar..")
            else:
                print("Hubo un problema con el volcado de sucursal")
                FOUND_ERRORS = True

        # Si empezamos en el paso 4
        if seleccion <= 4 and not FOUND_ERRORS:
            representante_register.commerceId = result.ComercioCentral.commerce_id
            representante_result = ResultFuncion()
            exito = manager.volcadoRepresentanteLegal(representante_register, representante_result)

            # Si retornó True
            if exito:
                print("Volcado de representante correcto: resultado hasta el momento:")
            
                # Agregar el mensaje a los volcados
                result.ComercioCentral.AdditionalMessages.Volcados.append(Mensaje(representante_result.source,
                                                                         representante_result.message))
                
                # Imprimir el objeto resultado    
                print(result)
                input("\nPresione cualquier tecla para continuar..")

            # Si retornó False                
            else:
                print("Hubo un problema con el volcado de representante")

                #Agregar el mensaje a los errores y detener
                result.ComercioCentral.Errors.Errors.append(Mensaje(representante_result.source,
                                                                         representante_result.message))
                print(result)
                FOUND_ERRORS = True

        # Paso 5: Servicio sucursal
        if seleccion <=5 and not FOUND_ERRORS:
            branch_service_register.branchId = "715280"
            service_branch_result = ServiceResult()
            exito = manager.volcadoServicioSucursal(branch_service_register, service_branch_result)

            # Si retornó True
            if exito:
                print("Volcado de servicio sucursal correcto: resultado hasta el momento:")
            
                # Agregar el mensaje a los volcados
                result.Sucursales[0].AdditionalMessages.Volcados.append(Mensaje(service_branch_result.source,
                                                                         service_branch_result.message))
                result.Sucursales[0].service_branch_id = service_branch_result.service_branch_id
                
                # Imprimir el objeto resultado    
                print(result)
                input("\nPresione cualquier tecla para continuar..")

            # Si retornó False                
            else:
                print("Hubo un problema con el volcado de representante")

                #Agregar el mensaje a los errores y detener
                result.Sucursales[0].Errors.Errors.append(Mensaje(service_branch_result.source,
                                                                         service_branch_result.message))
                print(result)
                FOUND_ERRORS = True    
        

        # Paso 6: Payment types
        if seleccion <=6 and not FOUND_ERRORS:
            payment_type_register.branchCode = 715280
            payment_type_register.serviceBranchId = 9595
            payment_type_register.branchEntityId = 1180012
            payment_type_result = PaymentTypeResult()
            exito = manager.volcadoPaymentType(payment_type_register, payment_type_result)

            # Si retornó True
            if exito:
                print("Volcado de payment type correcto: resultado hasta el momento:")
            
                # Agregar el mensaje a los volcados
                result.Sucursales[0].AdditionalMessages.Volcados.append(Mensaje(payment_type_result.source,
                                                                         payment_type_result.message))
                print("Resultado recuperado:")
                print(payment_type_result.payment_type_id)                                                        
                result.Sucursales[0].paymentTypeIds = payment_type_result.payment_type_id

                # Imprimir el objeto resultado    
                print(result)
                input("\nPresione cualquier tecla para continuar..")

            # Si retornó False                
            else:
                print("Hubo un problema con el volcado de payment type")

                #Agregar el mensaje a los errores y detener
                result.Sucursales[0].Errors.Errors.append(Mensaje(payment_type_result.source,
                                                                         payment_type_result.message))
                print(result)
                FOUND_ERRORS = True


        # Paso 7: Merchant discount
        if seleccion <= 7 and not FOUND_ERRORS:
            merchant_register.branchCode = 715280
            merchant_register.branchServiceId = 9595
            merchant_result = ResultFuncion()
            exito = manager.volcadoMerchantDiscount(merchant_register, merchant_result)

            # Si retornó True
            if exito:
                print("Volcado de merchant discount correcto: resultado hasta el momento:")
            
                # Agregar el mensaje a los volcados
                result.Sucursales[0].AdditionalMessages.Volcados.append(Mensaje(merchant_result.source,
                                                                         merchant_result.message))
                
                # Imprimir el objeto resultado    
                print(result)
                input("\nPresione ENTER para continuar..")

            # Si retornó False                
            else:
                print("Hubo un problema con el volcado de representante")

                #Agregar el mensaje a los errores y detener
                result.Sucursales[0].Errors.Errors.append(Mensaje(merchant_result.source,
                                                                         merchant_result.message))
                print(result)
                FOUND_ERRORS = True 

        # Paso 8: Terminal
        if seleccion <= 8 and not FOUND_ERRORS:
            # Agregar los valores diferidos al request
            terminal_register.branchCode = result.Sucursales[0].local_code
            terminal_register.contractId = str(result.ComercioCentral.agreement_id)
            
            terminal_result = TerminalResult()
            exito = manager.volcadoTerminal(terminal_register, terminal_result)

            # Si retornó True
            if exito:
                print("Volcado de merchant discount correcto: resultado hasta el momento:")

                # Capturar datos del resultado
                result.Sucursales[0].Terminals[0].terminal = terminal_result.terminal
                result.Sucursales[0].Terminals[0].collector = terminal_result.collector
                result.Sucursales[0].Terminals[0].billing_price = terminal_result.billing_price
            
                # Agregar el mensaje a los volcados
                result.Sucursales[0].Terminals[0].AdditionalMessages.Volcados.append(Mensaje(terminal_result.source,
                                                                         terminal_result.message))
                
                # Imprimir el objeto resultado    
                print(result)
                input("\nPresione ENTER para continuar..")

            # Si retornó False                
            else:
                print("Hubo un problema con el volcado de representante")

                #Agregar el mensaje a los errores y detener
                result.Sucursales[0].Terminals[0].Errors.Errors.append(Mensaje(terminal_result.source,
                                                                         terminal_result.message))
                print(result)
                FOUND_ERRORS = True 
        
        # Paso 9: Contrato
        if seleccion <= 9 and not FOUND_ERRORS:
            
            contract_result = ContratoResult()
            exito = manager.volcadoContrato(contract_register, contract_result)

            # Si retornó True
            if exito:
                print("Volcado de contrato correcto: resultado hasta el momento:")

                # Capturar datos del resultado
                result.ComercioCentral.ContratoDateAndTime = (contract_result.date + " " + contract_result.time) if contract_result.date and contract_result.time else ""
            
                # Agregar el mensaje a los volcados
                result.ComercioCentral.AdditionalMessages.Volcados.append(Mensaje(contract_result.source,
                                                                         contract_result.message))
                
                # Imprimir el objeto resultado    
                print(result)
                input("\nPresione ENTER para continuar..")

            # Si retornó False                
            else:
                print("Hubo un problema con el volcado de representante")

                #Agregar el mensaje a los errores y detener
                result.ComercioCentral.Errors.Errors.append(Mensaje(contract_result.source,
                                                                         contract_result.message))
                print(result)
                FOUND_ERRORS = True 


        
        # manager.volcadoRepresentanteLegal()
        # manager.volcadoCuentaBancaria()
        # manager.volcadoConfiguracionCuentaBancaria()
        # comercio_register = Register.from_volcado_comercio(volcado)
        # manager.volcadoComercio(comercio_register)

        # Construye el objeto de volcado de sucursal y vuelca la sucursal
        # sucursal_register = BranchRegister.from_volcado_comercio(volcado)
        # print(sucursal_register.to_json())
        # branch_id, local_code = manager.volcadoSucursal(sucursal_register)

        # print("\n")
        # print(f"branch_id = {branch_id}, local_code = {local_code}")
        
        # servicio = ServiceRegister.from_volcado_comercio(volcado)
        # print("\n")
        # print(servicio.to_json())