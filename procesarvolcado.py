from entidadesvolcado import EntidadesVolcado, ComercioCentral, Sucursal, Terminal, RepresentanteLegal, CuentaBancaria
from volcadomanager import VolcadoManager
from resultvolcado import ResultadoVolcado, BankAccountResult
from registrosvolcado import Register, ContractRegister, IswitchCommerceRegister, BankAccountRegister, BankAccConfigRegister
from resultvolcado import CommerceResult, ContratoResult, ResultFuncion, Mensaje
import resultvolcado as res

class ProcesoVolcado:
    def __init__(self, manager: VolcadoManager, result: ResultadoVolcado):
        self.manager = manager
        self.result = result

    def procesarComercioCentral(self, comercio: ComercioCentral):
        print("Procesando comercio central...\n")
        DEBUG = True
        volcado_sin_error = True

        # Generar requests        

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

        # Ejecutar volcado de comercio
        if not DEBUG:
            result_comercio = CommerceResult()
            exito_comercio = self.manager.volcadoComercio(request_comercio, result_comercio)
            if exito_comercio:
                print("Volcado de comercio OK.")
                self.result.ComercioCentral.AdditionalMessages.Volcados.append(Mensaje(result_comercio.source,
                                                                                    result_comercio.message))
                self.result.ComercioCentral.agreement_id = result_comercio.agreement_id
                self.result.ComercioCentral.commerce_id = result_comercio.commerce_id
                self.result.ComercioCentral.entry = result_comercio.entry
            else:
                print("Error en el volcado de comercio")
                volcado_sin_error = False
        
        else:
            print("Saltándose el volcado de comercio para no duplicar...")
            input("ENTER...")
            self.result.ComercioCentral.agreement_id = 542472
            self.result.ComercioCentral.commerce_id = 1324064
            self.result.ComercioCentral.entry = 189
            self.result.ComercioCentral.AdditionalMessages.Volcados.append(Mensaje("Volcado ficticio",
                                                                                   "Para evitar error por comercio duplicado"))

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



    def procesarSucursal(self, sucursal: Sucursal):
        print("Procesando sucursal...\n")

    def procesarTerminal(self, terminal: Terminal):
        print("Procesando terminal...\n")

    def procesarCuentaBancaria(self, cuenta: CuentaBancaria):
        print("Procesando cuenta bancaria...\n")
        DEBUG = True
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
            print("Volcado de cuenta bancaria correcto:")
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
            print("Error en el volcado de cuenta bancaria")
            volcado_sin_error = False
            if DEBUG:
                input("ENTER para continuar...")

        # Ejecutar volcado de configuración de cuenta
        # Este volcado debe asociar la cuenta a cada una de las sucursales que corresponde.
        # Probablemente la mejor forma de mandar esa información es directo desde la entidad
        if volcado_sin_error:
            result_congif_cuenta = ResultFuncion()
            # Parámetro diferido de número de cuenta
            request_bank_acc_config.accountId = mensajes_cuenta.accountId
            # Parámetro diferido de sucursal. Para versión de DEBUG preliminar usamos uno fijo
            if DEBUG:
                request_bank_acc_config.localCode = "205495"
            exito_config = self.manager.volcadoConfiguracionCuentaBancaria(request_bank_acc_config, result_congif_cuenta)
            if exito_config:
                print("volcado de configuracion de cuenta bancaria OK.")
                # Guardar el mensaje de éxito
                mensajes_cuenta.AdditionalMessages.Volcados.append(Mensaje(result_congif_cuenta.source,
                                                                           result_congif_cuenta.message))
                # Si está en DEBUG, detener
                if DEBUG:
                    input("ENTER para continuar...")
            else:
                print("Error en volcado de confiuración de cuenta bancaria")
                volcado_sin_error = False
                # Guardar el mensaje de fracaso
                mensajes_cuenta.Errors.Errors.append(Mensaje(result_congif_cuenta.source, result_congif_cuenta.message))
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
            mensajes_cuenta.responseMessage= "Volcado de la cuenta bancaria fue exitoso"
        else:
            mensajes_cuenta.wasSuccessful = False
            mensajes_cuenta.responseMessage = "Hubo un error en alguna parte del volcado de la cuenta bancaria"

        self.result.add_cuenta_bancaria(mensajes_cuenta)
        

    def procesarRepresentanteLegal(self, representante: RepresentanteLegal):
        print("Procesando representante legal...\n")

        # Crea request para representante legal

        # Si está en DEBUG, mostrar la información creada

        # Crear objeto de resultado y hacer el volcado del representante
        exito_representante = True
        
        if exito_representante:
            pass
            # Guardar el resultado del volcado

            # Si está en DEBUG, detener

        else:
            pass
            # Guardar el error

            # Si está en DEBUG, detener


    
    def procesarComercio(self, entidades: EntidadesVolcado):
        
        # Volcado los datos del comercio central
        self.procesarComercioCentral(entidades.comercioCentral)

        # Iterar por sucursales
        for sucursal in entidades.get_sucursales():

            # Volcar sucursal
            self.procesarSucursal(sucursal)

            # Iterar por terminales
            for terminal in sucursal.get_terminales():

                # Volcar terminal
                self.procesarTerminal(terminal)
        
        for cuenta in entidades.get_cuentas_bancarias():

            # Volcar cuenta bancaria
            self.procesarCuentaBancaria(cuenta)

        print(self.result.to_json())
        
        for representante in entidades.get_representantes_legales():

            # Volcar representante legal
            self.procesarRepresentanteLegal(representante)



        
