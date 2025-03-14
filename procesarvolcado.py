from entidadesvolcado import EntidadesVolcado, ComercioCentral, Sucursal, Terminal, RepresentanteLegal, CuentaBancaria
from volcadomanager import VolcadoManager
from resultvolcado import ResultadoVolcado
from registrosvolcado import Register, ContractRegister, IswitchCommerceRegister
from resultvolcado import CommerceResult, ContratoResult, ResultFuncion, Mensaje

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

    def procesarRepresentanteLegal(self, representante: RepresentanteLegal):
        print("Procesando representante legal...\n")
    
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

        for representante in entidades.get_representantes_legales():

            # Volcar representante legal
            self.procesarRepresentanteLegal(representante)



        
