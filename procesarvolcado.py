from entidadesvolcado import EntidadesVolcado, ComercioCentral, Sucursal, Terminal, RepresentanteLegal, CuentaBancaria
from volcadomanager import VolcadoManager
from resultvolcado import ResultadoVolcado, BankAccountResult
from registrosvolcado import Register, ContractRegister, IswitchCommerceRegister, BankAccountRegister, BankAccConfigRegister
from resultvolcado import CommerceResult, ContratoResult, ResultFuncion, Mensaje
import resultvolcado as res
import registrosvolcado as registros

class ProcesoVolcado:
    def __init__(self, manager: VolcadoManager, result: ResultadoVolcado):
        self.manager = manager
        self.result = result

    
    # Método para el volcado del comercio central
    # Procesa la parte relacionada a la entidad ComercioCentral
    def procesarComercioCentral(self, comercio: ComercioCentral):
        print("Procesando comercio central...\n")
        
        # Parámetro DEBUG para arrojar en pantalla más información de los volcados
        DEBUG = True

        # Parámetro para "saltarse" el volcado de comercio en caso de estar probando
        TEST_COMERCIO_FIJO = False
        volcado_sin_error = True

        #####################################
        # Generar requests
        #####################################        

        # Request volcado comercio
        request_comercio = Register.from_entidades(comercio)
        
        # Request contrato
        request_contrato = ContractRegister.from_entidades(comercio)

        # Request comercio Iswitch
        request_iswitch_commerce = IswitchCommerceRegister.from_entidades(comercio)

        if DEBUG:
            print(request_comercio.to_json())
            print("\n")
            print(request_contrato.to_json())
            print(request_iswitch_commerce.to_json())
            input("Presione ENTER...")

        #######################################################################
        # Parte 1: Volcado comercio. Punto de entrada de todo
        # Este volcado NO se puede ejecutar más de una vez,
        # dado que arroja un error de que el comercio ya existe en BO.
        # En caso de tener que probar, varias veces, hay que hacerlo con un
        # volcado comercio que ya existe, usando sus propiedades "en duro"
        #######################################################################

        if not TEST_COMERCIO_FIJO:
            result_comercio = CommerceResult()
            exito_comercio = self.manager.volcadoComercio(request_comercio, result_comercio)
            if exito_comercio:
                print("Volcado de comercio OK.")
                self.result.ComercioCentral.AdditionalMessages.Volcados.append(Mensaje(result_comercio.source,
                                                                                    result_comercio.message))
                self.result.ComercioCentral.agreement_id = result_comercio.agreement_id
                self.result.ComercioCentral.commerce_id = result_comercio.commerce_id
                self.result.ComercioCentral.entry = result_comercio.entry
                if DEBUG:
                    input("ENTER para continuar...")
            else:
                print("Error en el volcado de comercio")
                volcado_sin_error = False
                if DEBUG:
                    input("ENTER para continuar...")
        
        else:
            print("Saltándose el volcado de comercio para no duplicar...")
            input("ENTER...")
            self.result.ComercioCentral.agreement_id = 542472
            self.result.ComercioCentral.commerce_id = 1324064
            self.result.ComercioCentral.entry = 189
            self.result.ComercioCentral.AdditionalMessages.Volcados.append(Mensaje("Volcado ficticio",
                                                                                   "Para evitar error por comercio duplicado"))


        #######################################################################
        # Parte 2: Volcado de contrato
        #######################################################################
        
        # Ejecutar volcado de contrato
        if volcado_sin_error:
            result_contrato = ContratoResult()
            exito_contrato = self.manager.volcadoContrato(request_contrato, result_contrato)
            if exito_contrato:
                print("Volcado contrato OK")
                self.result.ComercioCentral.AdditionalMessages.Volcados.append(Mensaje(result_contrato.source,
                                                                                       result_contrato.message))
                if DEBUG:
                    input("ENTER para continuar...")
            else:
                print("Error en volcado contrato")
                volcado_sin_error = False
                if DEBUG:
                    input("ENTER para continuar...")

        #######################################################################
        # Parte 3: Volcado de comercio en ISWITCH
        #######################################################################

        # Ejecutar volcado de comercio en Iswitch
        if volcado_sin_error:
            result_comercio_iswitch = ResultFuncion()
            exito_iswitch = self.manager.volcadoIswitchComercio(request_iswitch_commerce, result_comercio_iswitch)
            if exito_iswitch:
                print("Volcado comercio Iswitch OK")
                self.result.ComercioCentral.AdditionalMessages.Volcados.append(Mensaje(result_comercio_iswitch.source,
                                                                                       result_comercio_iswitch.message))
                if DEBUG:
                    input("ENTER para continuar...")
            else:
                print("Error en volcado comercio Iswitch")
                volcado_sin_error = False
                if DEBUG:
                    input("ENTER para continuar...")

            if volcado_sin_error:
                print("Volcado de toda la entidad comercio central quedó OK")
                self.result.ComercioCentral.wasSuccessful = True
                print(self.result.to_json())
                if DEBUG:
                    input("ENTER...")



    # Método para el volcado del sucursal
    # Procesa la parte relacionada a la entidad Sucursal
    # Debido a las dependencias entre los volcados, el procesamiento de terminales
    # debe quedar dentro de este método, en dos partes
    def procesarSucursal(self, sucursal: Sucursal):
        print("Procesando sucursal...\n")

        # Parámetro para información adicional
        DEBUG = False

        # Debe ser verdadero en todo el proceso, o de lo contrario no continúa
        volcados_sin_errores = True

        # Objeto de resultado para guardar mensajes
        mensajes_sucursal = res.Sucursal()

        # Crear requests de sucursales
        request_sucursal = registros.BranchRegister.from_entidades(sucursal)
        request_servicio_sucursal = registros.ServiceRegister.from_entidades(sucursal)
        request_payment_type = registros.PaymentTypeRegister.from_entidades(sucursal)
        request_merchant_discount = registros.MerchantDiscountRegister.from_entidades(sucursal)
        request_branch_cc = registros.BranchCCRegister.from_entidades(sucursal)
        request_iswitch_branch = registros.IswitchBranchRegister.from_entidades(sucursal)
        request_commerce_pci = registros.CommercePciRegister.from_entidades(sucursal)
        request_monitor = registros.MonitorRegister.from_entidades(sucursal)
        request_switch = registros.CommerceSwitchRegister.from_entidades(sucursal)

        if DEBUG:
            print(request_sucursal.to_json())
            print("\n")
            print(request_servicio_sucursal.to_json())
            print("\n")
            print(request_payment_type.to_json())
            print("\n")
            print(request_merchant_discount.to_json())
            print("\n")
            print(request_branch_cc.to_json())
            print("\n")
            print(request_iswitch_branch.to_json())
            print("\n")
            print(request_commerce_pci.to_json())
            print("\n")
            print(request_monitor.to_json())
            print("\n")
            print(request_switch.to_json())
            print("\n")

            input ("ENTER para comenzar el volcado...")
            print("\n")

        #######################################################################
        # Parte 1: Volcado sucursal
        #######################################################################

        request_sucursal.commerceId = self.result.ComercioCentral.commerce_id

        result_sucursal = res.BranchResult()

        exito_sucursal = self.manager.volcadoSucursal(request_sucursal, result_sucursal)

        if exito_sucursal:
            print(f"\nVolcado sucursal exitoso para sucursal {result_sucursal.local_code}")
            mensajes_sucursal.AdditionalMessages.Volcados.append(Mensaje(result_sucursal.source, result_sucursal.message))
            mensajes_sucursal.branch_id = result_sucursal.branch_id
            mensajes_sucursal.entity_id = result_sucursal.entity_id
            mensajes_sucursal.local_code = result_sucursal.local_code
            if DEBUG:
                input("ENTER")

        else:
            print("\nHubo un error en el volcado de sucursal")
            mensajes_sucursal.Errors.Errors.append(Mensaje(result_sucursal.source, result_sucursal.message))
            volcados_sin_errores = False
            if DEBUG:
                input("ENTER")


        #######################################################################
        # Parte 2: Volcado servicio sucursal
        #######################################################################

        # Usamos este parámetro para identificar la sucursal
        id_local = result_sucursal.local_code

        if volcados_sin_errores:
            request_servicio_sucursal.branchId = int(result_sucursal.branch_id)

            result_servicio_sucursal = res.ServiceResult()

            exito_servicio_sucursal = self.manager.volcadoServicioSucursal(request_servicio_sucursal, result_servicio_sucursal)
            
            if exito_servicio_sucursal:
                print(f"\nVolcado de servicio de sucursal exitoso para sucursal {id_local}")
                mensajes_sucursal.AdditionalMessages.Volcados.append(Mensaje(result_servicio_sucursal.source,
                                                                            result_servicio_sucursal.message))
                mensajes_sucursal.service_branch_id = result_servicio_sucursal.service_branch_id
                if DEBUG:
                    input("ENTER")

            else:
                print("\nHubo un error en el volcado de servicio de sucursal")
                volcados_sin_errores = False
                mensajes_sucursal.Errors.Errors.append(Mensaje(result_servicio_sucursal.source,
                                                            result_servicio_sucursal.message))
                if DEBUG:
                    input("ENTER")


        #######################################################################
        # Parte 3: Volcado payment type
        #######################################################################

        if volcados_sin_errores:
            request_payment_type.serviceBranchId = int(result_servicio_sucursal.service_branch_id)
            request_payment_type.branchCode = int(result_sucursal.branch_id)
            request_payment_type.branchEntityId = int(result_sucursal.entity_id)

            result_payment_type = res.PaymentTypeResult()

            exito_payment_type = self.manager.volcadoPaymentType(request_payment_type, result_payment_type)

            if exito_payment_type:
                print(f"\nVolcado de payment type exitoso para sucursal {id_local}")
                mensajes_sucursal.AdditionalMessages.Volcados.append(Mensaje(result_payment_type.source,
                                                                            result_payment_type.message))
                mensajes_sucursal.paymentTypeIds = result_payment_type.payment_type_id
                if DEBUG:
                    input("ENTER")
            else:
                print("\nHubo un error en el volcado de payment type")
                volcados_sin_errores = False
                mensajes_sucursal.Errors.Errors.append(Mensaje(result_payment_type.source,
                                                            result_payment_type.message))
                if DEBUG:
                    input("ENTER")


        #######################################################################
        # Parte 4: Volcado merchant discount
        #######################################################################

        if volcados_sin_errores:
            request_merchant_discount.branchCode = int(result_sucursal.local_code)
            request_merchant_discount.branchServiceId = int(result_servicio_sucursal.service_branch_id)

            result_merchant_discount = res.ResultFuncion()

            exito_merchant_discount = self.manager.volcadoMerchantDiscount(request_merchant_discount,
                                                                        result_merchant_discount)

            if exito_merchant_discount:
                print(f"\nVolcado de merchant discount exitoso para sucursal {id_local}")
                mensajes_sucursal.AdditionalMessages.Volcados.append(Mensaje(result_merchant_discount.source,
                                                                            result_merchant_discount.message))
                if DEBUG:
                    input("ENTER")

            else:
                print("Hubo un error en el volcado de merchant discount")
                volcados_sin_errores = False
                mensajes_sucursal.Errors.Errors.append(Mensaje(result_merchant_discount.source,
                                                            result_merchant_discount.message))
                if DEBUG:
                    input("ENTER")

        #######################################################################
        # Interludio: Acá es necesario hacer una pausa en los volcados de 
        # sucursal para hacer el volcado inicial de los terminales.
        # De lo contrario, el volcado de las condiciones comerciales de la sucursal
        # va a fallar.
        #######################################################################
        
        print(f"\nagreement_id: {self.result.ComercioCentral.agreement_id}")
        input("ENTER...")

        # Obtener el agreement_id del ComercioCentral
        contractId = self.result.ComercioCentral.agreement_id

        # Obtener el branchCode del resultado del volcado de la sucursal
        branchCode = result_sucursal.local_code

        # Iterar por todos los terminales que vienen en la entrada
        for input_terminal in sucursal.Terminales:

            # Generar el objeto de resultado para el terminal actual
            mensajes_terminal = res.Terminal()

            # terminal = sucursal.Terminales[0]
            self.procesarTerminal(input_terminal, mensajes_terminal, branchCode, contractId)
            mensajes_sucursal.add_terminal(mensajes_terminal)

        print(mensajes_sucursal.to_json())
        input("ENTER...")


        #######################################################################
        # Parte 5: Volcado de condiciones comerciales de sucursal
        #######################################################################

        if volcados_sin_errores:
            request_branch_cc.branchCode = int(result_sucursal.local_code)
            
            result_branch_cc = res.ResultFuncion()

            exito_branch_cc = self.manager.volcadoBranchCC(request_branch_cc, result_branch_cc)

            if exito_branch_cc:
                print (f"\nVolcado de condiciones comerciales de sucursal exitoso para sucursal {id_local}")
                mensajes_sucursal.AdditionalMessages.Volcados.append(Mensaje(result_branch_cc.source,
                                                                            result_branch_cc.message))
                if DEBUG:
                    input("ENTER")

            else:
                print("\nHubo un error en el volcado de las condiciones comerciales de la sucursal")
                volcados_sin_errores = False
                mensajes_sucursal.Errors.Errors.append(Mensaje(result_branch_cc.source,
                                                            result_branch_cc.message))
                if DEBUG:
                    input("ENTER")


        #######################################################################
        # Parte 6: Volcado sucursal en ISWITCH
        #######################################################################

        if volcados_sin_errores:
            request_iswitch_branch.localCode = int(result_sucursal.local_code)

            result_iswitch_branch = res.IswitchBranchResult()

            exito_iswitch_branch = self.manager.volcadoIswitchBranch(request_iswitch_branch, result_iswitch_branch)

            if exito_iswitch_branch:
                print(f"\nVolcado de sucursal en ISWITCH fue exitoso para sucursal {id_local}")
                mensajes_sucursal.AdditionalMessages.Volcados.append(Mensaje(result_iswitch_branch.source,
                                                                            result_iswitch_branch.message))
                mensajes_sucursal.branchIswId = result_iswitch_branch.branchIswId
                if DEBUG:
                    input("ENTER")

            else:
                print("\nHubo un problema con el volcado de sucursal en ISWITCH")
                volcados_sin_errores = False
                mensajes_sucursal.Errors.Errors.append(Mensaje(result_iswitch_branch.source,
                                                            result_iswitch_branch.message))
                if DEBUG:
                    input("ENTER")
                                                           

        #######################################################################
        # Parte 7: Volcado en réplica PCI
        #######################################################################

        if volcados_sin_errores:
            request_commerce_pci.branchCode = int(result_sucursal.local_code)

            result_commerce_pci = ResultFuncion()

            exito_commerce_pci = self.manager.volcadoCommercePci(request_commerce_pci, result_commerce_pci)

            if exito_commerce_pci:
                print(f"\nVolcado en réplica PCI exitoso para sucursal {id_local}")
                mensajes_sucursal.AdditionalMessages.Volcados.append(Mensaje(result_commerce_pci.source,
                                                                            result_commerce_pci.message))
                if DEBUG:
                    input("ENTER")
                
            else:
                print("Hubo un problema con el volcado de réplica PCI")
                volcados_sin_errores = False
                mensajes_sucursal.Errors.Errors.append(Mensaje(result_commerce_pci.source,
                                                            result_commerce_pci.message))
                if DEBUG:
                    input("ENTER")

        
        #######################################################################
        # Parte 8: Volcado en Monitor Plus
        #######################################################################

        if volcados_sin_errores:
            request_monitor.branchCode = int(result_sucursal.local_code)

            result_monitor = res.MonitorResult()

            exito_monitor = self.manager.volcadoMonitorPlus(request_monitor, result_monitor)

            if exito_monitor:
                print(f"\nVolcado de Monitor Plus exitoso para sucursal {id_local}")
                mensajes_sucursal.AdditionalMessages.Volcados.append(Mensaje(result_monitor.source,
                                                                            result_monitor.message))
                date_and_time = result_monitor.date + " " + result_monitor.time
                mensajes_sucursal.MonitorPlusDateAndTime = date_and_time
                if DEBUG:
                    input("ENTER")
                
            else:
                print("\nHubo un problema con el volcado de Monitor Plus")
                volcados_sin_errores = False
                mensajes_sucursal.Errors.Errors.append(Mensaje(result_monitor.source,
                                                            result_monitor.message))
                if DEBUG:
                    input("ENTER")


        #######################################################################
        # Parte 9: Volcado en switch
        #######################################################################

        if volcados_sin_errores:
            request_switch.branchCode = int(result_sucursal.local_code)

            result_switch = res.ResultFuncion()

            exito_switch = self.manager.volcadoCommerceSwitch(request_switch, result_switch)

            if exito_switch:
                print(f"\nVolcado en SWITCH exitoso para sucursal {id_local}")
                mensajes_sucursal.AdditionalMessages.Volcados.append(Mensaje(result_switch.source,
                                                                            result_switch.message))
                if DEBUG:
                    input("ENTER")
                
            else:
                print("\nHubo un error en el volcado en SWITCH")
                volcados_sin_errores = False
                mensajes_sucursal.Errors.Errors.append(Mensaje(result_switch.source,
                                                            result_switch.message))
                if DEBUG:
                    input("ENTER")

        # Acá llegamos una vez terminado el volcado, independiente de si resultó exitoso o no.
        # En el proceso, tuvimos que agregar los mensajes de éxito o fracaso.
        # Ahora capturamos el estado general del proceso y guardamos en su resultado.
        # Luego, el resultado lo agregamos al resultado general.
        if volcados_sin_errores:
            mensajes_sucursal.wasSuccessful = True
            mensajes_sucursal.responseMessage = "Todos los elementos de las sucursal volcados con éxito"
        else:
            mensajes_sucursal.wasSuccessful = False
            mensajes_sucursal.responseMessage = "Hubo algún problema en el proceso de volcado de la sucursal"
        
        self.result.add_sucursal(mensajes_sucursal)

        
        # Una vez terminado el volcado de sucursal, es necesario hacer los adicionales
        # de los volcados de terminal, de manera de dejar todo listo
        # Debe iterarse sobre todos los terminales
        for index, input_terminal in enumerate(sucursal.Terminales):

            # Pasamos el objeto de resultado de terminal que ya habíamos creado antes
            # y que es parte del objeto de resultados de sucursal
            # mensajes_terminal = mensajes_sucursal.Terminals[0]
            if index < len(mensajes_sucursal.Terminals):
                mensajes_terminal = mensajes_sucursal.Terminals[index]
                self.procesarAdicionalesTerminal(input_terminal, mensajes_terminal, int(branchCode))
            else:
                print("La cantidad de elementos no coincide...")
                input("ENTER..")

        print(mensajes_sucursal.to_json())
        input("ENTER...")



    # Método para el volcado del terminal básico
    # Procesa la parte relacionada a la entidad Terminal
    # Sólo considera la creación del terminal, no el resto de sus partes
    # Esto es necesario porque las CC de la sucursal requieren que al menos un terminal exista
    def procesarTerminal(self, terminal: Terminal, mensajes_terminal: res.Terminal, branchCode: int, contractId: str):
        print("Procesando terminal...\n")
        print(f"Valores recibidos: branchCode = {branchCode}, contractId = {contractId}  ")

        DEBUG = False
        volcados_sin_errores = True

        # Objeto de resultado para guardar mensajes
        # mensajes_terminal = res.Terminal()

        # Crear requests de terminales
        request_terminal = registros.TerminalRegister.from_entidades(terminal)
        # request_terminal_cc = registros.TerminalCCRegister.from_entidades(terminal)
        # request_terminal_iswitch = registros.IswitchTerminalRegister.from_entidades(terminal)
        # request_red_pos = registros.RedPosRegister.from_entidades(terminal)

        if DEBUG:
            print(request_terminal.to_json())
            print("\n")
            input("ENTER...")
        
        #######################################################################
        # Parte 1: Volcado terminal
        #######################################################################
        
        result_terminal = res.TerminalResult()
        
        # Valores diferidos, por ahora implementados sólo para pruebas

        request_terminal.branchCode = int(branchCode)  # De sucursal
        request_terminal.contractId = str(contractId)  # De comercio central

        if DEBUG:
            print("\nRequest completo con parámetros diferidos")
            print(request_terminal.to_json())
            print("\n")
            input("ENTER...")
            

        exito_terminal = self.manager.volcadoTerminal(request_terminal, result_terminal)
        if exito_terminal:
            id_terminal = result_terminal.terminal
            print(f"Volcado de terminal exitoso con id de terminal {id_terminal}")
            mensajes_terminal.AdditionalMessages.Volcados.append(Mensaje(result_terminal.source, result_terminal.message))
            mensajes_terminal.terminal = id_terminal
            if DEBUG:
                input("ENTER para continuar...")

        else:
            print("Error en el volcado de terminal")
            mensajes_terminal.Errors.Errors.append(Mensaje(result_terminal.source, result_terminal.message))
            volcados_sin_errores = False
            if DEBUG:
                input("ENTER para continuar...")

        if volcados_sin_errores:
            mensajes_terminal.responseMessage = f"Volcado PARCIAL del terminal {id_terminal} listo"
        else:
            mensajes_terminal.responseMessage = "Falló el volcado de terminal"
            mensajes_terminal.wasSuccessful = False

        
    # Método para el volcado del resto de las características del terminal
    # Procesa la parte relacionada a la entidad Terminal
    # Genera condiciones comerciales, ISWITCH y ticket RedPOS
    def procesarAdicionalesTerminal(self, terminal: Terminal, mensajes_terminal: res.Terminal, branchCode: int):

        DEBUG = False
        volcados_sin_errores = True
        
        # Crear requests para volcados adicionales
        request_terminal_cc = registros.TerminalCCRegister.from_entidades(terminal)
        request_terminal_iswitch = registros.IswitchTerminalRegister.from_entidades(terminal)
        request_red_pos = registros.RedPosRegister.from_entidades(terminal)
        
        if DEBUG:
            print("\nMostrando requests de adicionales de terminal:")
            print(request_terminal_cc.to_json())
            print("\n")
            input("ENTER...")
            print(request_terminal_iswitch.to_json())
            print("\n")
            input("ENTER...")
            print(request_red_pos.to_json())
            print("\n")
            input("ENTER...")

        #######################################################################
        # (continuación) Parte 2: Volcado condiciones comerciales de terminal
        #######################################################################

        id_terminal = mensajes_terminal.terminal
        request_terminal_cc.terminalNumber = id_terminal
        
        # Número de sucursal, que por el momento es de prueba
        request_terminal_cc.branchCode = branchCode

        result_terminal_cc = res.ResultFuncion()
        exito_terminal_cc = self.manager.volcadoTerminalCC(request_terminal_cc, result_terminal_cc)

        if exito_terminal_cc:
            print(F"Volcado de condiciones comerciales de terminal exitosas para terminal {id_terminal}")
            mensajes_terminal.AdditionalMessages.Volcados.append(Mensaje(result_terminal_cc.source, result_terminal_cc.message))
            if DEBUG:
                input("ENTER para continuar...")

        else:
            print("Hubo un error en el volcado de las condiciones comerciales del terminal")
            mensajes_terminal.Errors.Errors.append(Mensaje(result_terminal_cc.source, result_terminal_cc.message))
            volcados_sin_errores = False
            if DEBUG:
                input("ENTER para continuar...")

        #######################################################################
        # Parte 3: Volcado de terminal en ISWITCH
        #######################################################################

        if volcados_sin_errores:
            request_terminal_iswitch.terminalNumber = str(id_terminal)
            
            result_terminal_iswitch = res.ResultFuncion()
            
            exito_terminal_iswitch = self.manager.volcadoIswitchTerminal(request_terminal_iswitch, result_terminal_iswitch)

            if exito_terminal_iswitch:
                print(f"Volcado de terminal en ISWITCH exitoso para terminal {id_terminal}")
                mensajes_terminal.AdditionalMessages.Volcados.append(Mensaje(result_terminal_iswitch.source, result_terminal_iswitch.message))
                if DEBUG:
                    input("ENTER para continuar...")
            else:
                print(f"Hubo un error en el volcado de terminal ISWITCH para terminal {id_terminal}")
                mensajes_terminal.Errors.Errors.append(Mensaje(result_terminal_iswitch.source, result_terminal_iswitch.message))
                volcados_sin_errores = False
                if DEBUG:
                    input("ENTER para continuar...")

        #######################################################################
        # Parte 4: Volcado de ticket RedPos
        #######################################################################

        if volcados_sin_errores:

            request_red_pos.terminalNumber = str(id_terminal)

            result_red_pos = res.RedPosResult()
            
            exito_red_pos = self.manager.volcadoRedPos(request_red_pos, result_red_pos)

            if exito_red_pos:
                print(f"Volcado de ticket RedPos exitoso para terminal {id_terminal}")
                mensajes_terminal.AdditionalMessages.Volcados.append(Mensaje(result_red_pos.source, result_red_pos.message))
                if DEBUG:
                    input("ENTER para continuar...")
            else:
                print(f"Hubo un error en el volcado de ticket RedPos para terminal {id_terminal}")
                mensajes_terminal.Errors.Errors.append(Mensaje(result_red_pos.source, result_red_pos.message))
                volcados_sin_errores = False
                if DEBUG:
                    input("ENTER para continuar...")

        # Acá llegamos una vez terminado el volcado, independiente de si resultó exitoso o no.
        # En el proceso, tuvimos que agregar los mensajes de éxito o fracaso.
        # Ahora capturamos el estado general del proceso y guardamos en su resultado.
        # Luego, el resultado lo agregamos al resultado general.
        if volcados_sin_errores:
            # Todo resultó bien
            mensajes_terminal.wasSuccessful = True
            mensajes_terminal.responseMessage= "Volcado que crea el terminal fue exitoso"
        else:
            mensajes_terminal.wasSuccessful = False
            mensajes_terminal.responseMessage = "Hubo un error en la creación del terminal"
        
        # mensaje_sucursal = res.Sucursal()
        # mensaje_sucursal.add_terminal(mensajes_terminal)
        # self.result.add_sucursal(mensaje_sucursal)
        
 

    # Método para el volcado de cuenta bancaria
    # Procesa la parte relacionada a la entidad CuentaBancaria
    # Considerar que, dado que en este flujo tendremos una sola cuenta,
    # ésta debe asociarse a todas las sucursales que se volcaron.
    # Por eso recibe como argumento una lista de terminales.
    def procesarCuentaBancaria(self, cuenta: CuentaBancaria, sucursales: list[int]):
        print("Procesando cuenta bancaria...\n")
        DEBUG = False
        volcado_sin_error = True

        # Crear objeto de resultado concerniente a la cuenta bancaria para mostrar
        mensajes_cuenta = res.CuentaBancaria()

        # Generar requests
        print(cuenta.to_json())

        # Request para cuenta bancaria
        request_bank_account = BankAccountRegister.from_entidades(cuenta)

        # Request para configuración de cuenta
        request_bank_acc_config = BankAccConfigRegister.from_entidades(cuenta)

        if DEBUG:
            print(request_bank_account.to_json())
            print("\n")
            print(request_bank_acc_config.to_json())
            input("Presione ENTER...")

        # Ejecutar volcado de cuenta bancaria
        result_bank_account = BankAccountResult()
        exito_account = self.manager.volcadoCuentaBancaria(request_bank_account, result_bank_account)
        if exito_account:
            print("\nVolcado de cuenta bancaria correcto:")
            # Guardar el mensaje de éxito en la entidad
            # Lo guardamos en un objeto de resultado cuenta bancaria que agregaremos al objeto de resultado general
            mensajes_cuenta.AdditionalMessages.Volcados.append(Mensaje(result_bank_account.source,
                                                                       result_bank_account.message))
            # Guardar el número de cuenta
            # Lo guardamos en primera instancia en el objeto de mensajes de cuenta bancaria
            # Este objeto se va a agregar al resultado final
            mensajes_cuenta.accountId = result_bank_account.account_id
            if DEBUG:
                input("ENTER para continuar...")
        else:
            # Registrar error de volcado
            # Registrar en objeto de resultado de cuenta para después agregar al resultado general
            mensajes_cuenta.Errors.Errors.append(Mensaje(result_bank_account.source,
                                                         result_bank_account.message))
            print("\nError en el volcado de cuenta bancaria")
            volcado_sin_error = False
            if DEBUG:
                input("ENTER para continuar...")

        # Ejecutar volcado de configuración de cuenta
        # Este volcado debe asociar la cuenta a cada una de las sucursales que corresponde.
        # Probablemente la mejor forma de mandar esa información es directo desde la entidad
        if volcado_sin_error:
            result_congif_cuenta = ResultFuncion()

            for sucursal in sucursales:
                # Parámetro diferido de número de cuenta
                request_bank_acc_config.accountId = mensajes_cuenta.accountId
                # Parámetro diferido de sucursal, iterado según la lista
                request_bank_acc_config.localCode = sucursal                

                exito_config = self.manager.volcadoConfiguracionCuentaBancaria(request_bank_acc_config, result_congif_cuenta)

                mensaje_con_sucursal = f"{result_congif_cuenta.message} para sucursal {sucursal}"

                if exito_config:
                    print("\nvolcado de configuracion de cuenta bancaria OK.")
                    # Guardar el mensaje de éxito
                    mensajes_cuenta.AdditionalMessages.Volcados.append(Mensaje(result_congif_cuenta.source, mensaje_con_sucursal))
                    # Si está en DEBUG, detener
                    if DEBUG:
                        input("ENTER para continuar...")
                else:
                    print("\nError en volcado de confiuración de cuenta bancaria")
                    volcado_sin_error = False
                    # Guardar el mensaje de fracaso
                    mensajes_cuenta.Errors.Errors.append(Mensaje(result_congif_cuenta.source, mensaje_con_sucursal))
                    # Si está en DEBUG, detener
                    if DEBUG:
                        input("ENTER para continuar...")


        # Acá llegamos una vez terminado el volcado, independiente de si resultó exitoso o no.
        # En el proceso, tuvimos que agregar los mensajes de éxito o fracaso.
        # Ahora capturamos el estado general del proceso y guardamos en su resultado.
        # Luego, el resultado lo agregamos al resultado general.
        if volcado_sin_error:
            # Todo resultó bien
            mensajes_cuenta.wasSuccessful = True
            mensajes_cuenta.responseMessage= "Volcado de todos los componentes del temrinal fue exitoso"
        else:
            mensajes_cuenta.wasSuccessful = False
            mensajes_cuenta.responseMessage = "Hubo un error en alguna parte de los volcados del terminal"

        self.result.add_cuenta_bancaria(mensajes_cuenta)
        

    def procesarRepresentanteLegal(self, representante: RepresentanteLegal):
        print("Procesando representante legal...\n")

        DEBUG = False
        volcados_sin_error = True
        
        # Crea request para representante legal
        request_rep_legal = registros.RepresentativeRegister.from_entidades(representante)

        # Asignar el id de comercio
        if DEBUG:
            request_rep_legal.commerceId = 1324064
        else:
            request_rep_legal.commerceId = self.result.ComercioCentral.commerce_id

        # Si está en DEBUG, mostrar la información creada
        if DEBUG:
            print("\n")
            print(request_rep_legal.to_json())
            input("ENTER...")

        # Crear objeto de mensajes de volcado (resultado)
        mensajes_rep = res.RepresentanteLegal()

        # Crear objeto de resultado y hacer el volcado del representante
        result_rep_legal = ResultFuncion()
        exito_representante = self.manager.volcadoRepresentanteLegal(request_rep_legal, result_rep_legal)
        
        if exito_representante:
            print("\nVolcado de representante exitoso:")
            # Guardar el resultado del volcado
            mensajes_rep.AdditionalMessages.Volcados.append(Mensaje(result_rep_legal.source, result_rep_legal.message))
            
            # Si está en DEBUG, detener
            if DEBUG:
                input("ENTER para continuar...")

        else:
            print("\nError en el volcado de representante legal")
            # Guardar el error
            mensajes_rep.Errors.Errors.append(Mensaje(result_rep_legal.source, result_rep_legal.message))
            volcados_sin_error = False
                                              
            # Si está en DEBUG, detener
            if DEBUG:
                input("ENTER para continuar...")

        if volcados_sin_error:
            mensajes_rep.wasSuccessful = True
            mensajes_rep.responseMessage = "Volcado de representante legal exitoso"
        else:
            mensajes_rep.wasSuccessful = False
            mensajes_rep.responseMessage = "Hubo un error en el volcado de representante legal"
        self.result.add_representante_legal(mensajes_rep)


    
    # Método de procesamiento general
    # Es un análogo a una "capa de servicios"
    def procesarComercio(self, entidades: EntidadesVolcado):
        
        # Volcado los datos del comercio central
        self.procesarComercioCentral(entidades.comercioCentral)

        # Iterar por sucursales
        for sucursal in entidades.get_sucursales():

            # Volcar sucursal
            self.procesarSucursal(sucursal)

        
        # Obtener la lista de las sucursales efectivamente creadas para la asociación de la cuenta
        for cuenta in entidades.get_cuentas_bancarias():

            sucursales = []

            # Debe recibir una lista de sucursales
            for resultado_sucursal in self.result.Sucursales:
                sucursales.append(resultado_sucursal.local_code)
                
            print(f"\nLista de sucursales para cuenta bancaria: {sucursales}")

            # Volcar cuenta bancaria
            self.procesarCuentaBancaria(cuenta, sucursales)

        # print(self.result.to_json())
        
        for representante in entidades.get_representantes_legales():

            # Volcar representante legal
            self.procesarRepresentanteLegal(representante)
        
        print(self.result.to_json())





        
