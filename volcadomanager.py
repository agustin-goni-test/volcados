import requests
from pydantic import ValidationError
from resultvolcado import ResultadoVolcado, ResultFuncion, ServiceResult, PaymentTypeResult, PaymentTypeResult, TerminalResult, BranchResult
from resultvolcado import ContratoResult, BankAccountResult, IswitchBranchResult, MonitorResult, RedPosResult, CommerceResult, TicketResult
from registrosvolcado import RepresentativeRegister, BankAccountRegister, BankAccountConfigurationRegister, Register, BranchRegister
from registrosvolcado import TicketRegister, MerchantDiscountRegister, PaymentTypeRegister, BranchCCRegister, TerminalCCRegister
from registrosvolcado import IswitchCommerceRegister, IswitchBranchRegister, IswitchTerminalRegister, CommercePciRegister
from registrosvolcado import CommerceSwitchRegister, MonitorRegister, RedPosRegister

class VolcadoManager:
    BASE_URL = "https://apidev.mcdesaqa.cl/central/af/ayc/registry/commerce/v1/register"
    TICKET_URL = "https://apidev.mcdesaqa.cl/central/af/ayc/registry/commerce/v1/ticket"
    SIGN_URL = "https://apidev.mcdesaqa.cl/central/af/ayc/registry/commerce/v1/sign"
    PING_ENDPOINT = "ping"
    
    REPRESENTATIVE_ENDPOINT = "representative"
    BANK_ACCOUNT_ENDPOINT = "bankAccount"
    BANK_ACCOUNT_CONFIGURATION_ENDPOINT = "bankAccount/configuration"
    COMMERCE_ENDPOINT = ""
    BRANCH_ENDPOINT = "branch"
    TICKET_ENDPOINT = ""
    SERVICES_ENDPOINT = "services"
    MERCHANT_ENDPOINT = "merchant"
    PAYMENT_TYPE_ENDPOINT = "paymentType"
    TERMINAL_ENDPOINT = "terminal"
    CONTRATO_ENDPOINT = ""
    BRANCH_CC_ENDPOINT = "branches/cc"
    TERMINAL_CC_ENDPOINT = "terminal/cc"
    ISWITCH_COMMERCE_ENDPOINT = "commerce/iswitch"
    ISWITCH_BRANCH_ENDPOINT = "branch/iswitch"
    ISWITCH_TERMINAL_ENDPOINT = "terminal/iswitch"
    COMMERCE_PCI_ENDPOINT = "replica/pci"
    COMMERCE_SWITCH_ENDPOINT = "commerce/switch"
    MONITOR_ENDPOINT = "monitorPlus"
    RED_POS_ENDPOINT = "terminal/ticket"

    def __init__(self, auth_token, volcado_comercio):
        self.headers = {
            "Authorization": f"Bearer {auth_token}"
        }
        self.volcado_comercio = volcado_comercio

    # Método para validar si el servicio está activo antes de volcar
    def isResponding(self):
        """Checks if the API is responding by sending a request to the ping endpoint."""
        url = f"{self.BASE_URL}/{self.PING_ENDPOINT}"
        try:
            response = requests.get(url, headers=self.headers)

            if response.status_code == 200 and response.text.lower() == "pong":
                print("Success: Received 'pong' response.")
                return True
            else:
                print(f"Unexpected response: {response.text}")
                return False

        except requests.exceptions.RequestException as e:
            print(f"An error occurred: {str(e)}")
            return False

   
    ##### VERSIÓN COMENTADA PARA LUEGO BORRAR *****

    # Método para volcar el comercio central
    # def volcadoComercio(self, register: Register, result: ResultadoVolcado):
    #     """Sends a request to register a commerce."""
    #     print("Iniciando volcado comercio...")

    #     commerce_id=""
    #     entry=""
    #     agreement_id=""

    #     # Convert the Register object to JSON data
    #     json_data = register.to_json()
    #     print("JSON Data:", json_data)
    #     print("\n")

    #     # Use the COMMERCE_ENDPOINT for the URL
    #     url = f"{self.BASE_URL}/{self.COMMERCE_ENDPOINT}"

    #     # Consume the service
    #     try:
    #         # Convert the Register object to a dictionary (you can adjust this based on your Register class method)
    #         payload = register.dict()
    #         response = requests.post(url, json=payload, headers=self.headers)

    #         if response.status_code == 200:
    #             data = response.json()
    #             data_section = data.get('data', {})  # Default to empty dict if 'data' is missing
    #             commerce_id = data_section.get('commerce_id', 'Unknown')
    #             entry = data_section.get('entry', 'Unknown')
    #             agreement_id = data_section.get('agreement_id', 'Unknown')
    #             print("Volcado comercio exitoso:", data)
    #             print(f"\nParámetros de salida: commerce_id = {commerce_id} - entry = {entry} - agreement_id = {agreement_id}\n")

    #             # Agregar los parámetros correspondientes al resultado
    #             result.ComercioCentral.commerce_id = commerce_id
    #             result.ComercioCentral.entry = entry
    #             result.ComercioCentral.agreement_id = agreement_id

    #             # Retornar condición de éxito
    #             return True

    #         else:
    #             print(f"Failed with status code {response.status_code}: {response.text}\n")
    #             return False

    #     except ValidationError as e:
    #         print("Validation error:", e.json())
    #         return False
    #     except Exception as e:
    #         print(f"An error occurred: {str(e)}")
    #         return False
    

    def volcadoComercio(self, register: Register, result: CommerceResult):
 
        # Convert the Register object to JSON data
        json_data = register.to_json()
        print("JSON Data:", json_data)

        # Use the COMMERCE_ENDPOINT for the URL
        url = f"{self.BASE_URL}/{self.COMMERCE_ENDPOINT}"

        # Consume the service
        try:
            # Convert the Register object to a dictionary (you can adjust this based on your Register class method)
            payload = register.model_dump()
            response = requests.post(url, json=payload, headers=self.headers)

            if response.status_code == 200:
                data = response.json()
                data_section = data.get('data', {})  # Default to empty dict if 'data' is missing

                # Toma los valores para el resultado
                result.source = "Volcado de comercio central"
                result.message = data_section.get('response_message', 'Unknown')

                 # Valida el código de resultado
                if data_section.get('response_code') != '0':
                    result.success = False
                    return False
                else:
                    result.success = True
                    print("Volcado de comercio central:")

                    # Capturar los datos del resultado
                    result.commerce_id = data_section.get('commerce_id', 'Unknown')
                    result.entry = data_section.get('entry', 'Unknown')
                    result.agreement_id = data_section.get('agreement_id', 'Unknown')

                    print(data)
                    return True

            else:
                print(f"Failed with status code {response.status_code}: {response.text}\n")
                return False

        except ValidationError as e:
            print("Validation error:", e.json())
            return False
        except Exception as e:
            print(f"An error occurred: {str(e)}")
            return False
    


    ##### VERSIÓN COMENTADA PARA LUEGO BORRAR *****
    
    # def volcadoTicket(self, register: TicketRegister, result: ResultadoVolcado):
    #     print("Iniciando volcado de ticket...")

    #     # Convert the Register object to JSON data
    #     json_data = register.to_json()
    #     print("JSON Data:", json_data)
    #     print("\n")

    #     date = ""
    #     time = ""

    #     # Use the TICKET_ENDPOINT for the URL
    #     url = f"{self.TICKET_URL}/{self.TICKET_ENDPOINT}"

    #     # Consume the service
    #     try:
    #         # Convert the Register object to a dictionary (you can adjust this based on your Register class method)
    #         payload = register.dict()
    #         response = requests.post(url, json=payload, headers=self.headers)

    #         if response.status_code == 200:
    #             data = response.json()
    #             data_section = data.get('data', {})  # Default to empty dict if 'data' is missing
    #             date = data_section.get('date', 'Unknown')
    #             time = data_section.get('time', 'Unknown')
    #             date_and_time = date + " " + time
    #             print("Volcado ticket exitoso:", data)
    #             print(f"\nParámetros de salida: ComercioTicketDateAndTime = {date_and_time}\n")

    #             # Guardar parámetro de resultado
    #             result.ComercioCentral.ComercioTicketDateAndTime = date_and_time
                
    #             # Retornar condicion de éxito
    #             return True

    #         else:
    #             print(f"Failed with status code {response.status_code}: {response.text}\n")
    #             return False

    #     except ValidationError as e:
    #         print("Validation error:", e.json())
    #         return False
    #     except Exception as e:
    #         print(f"An error occurred: {str(e)}")
    #         return False



    def volcadoTicket(self, register: TicketRegister, result: TicketResult):

        # Convert the Register object to JSON data
        json_data = register.to_json()
        print("JSON Data:", json_data)

        # Use the TICKET_ENDPOINT for the URL
        url = f"{self.TICKET_URL}/{self.TICKET_ENDPOINT}"

        # Consume the service
        try:
            # Convert the Register object to a dictionary (you can adjust this based on your Register class method)
            payload = register.model_dump()
            response = requests.post(url, json=payload, headers=self.headers)

            if response.status_code == 200:
                data = response.json()
                data_section = data.get('data', {})  # Default to empty dict if 'data' is missing
                
                # Toma los valores para el resultado
                result.source = "Volcado de ticket de comercio"
                result.message = data_section.get('response_message', 'Unknown')
                
                if data_section.get('response_code') != '0':
                    result.success = False
                    return False
                else:
                    result.success = True
                    print("Volcado de ticket de comercio exitoso:")
                    result.date = data_section.get('date', 'Unknown')
                    result.time = data_section.get('time', 'Unknown')
                    print(data)
                    return True

            else:
                print(f"Failed with status code {response.status_code}: {response.text}\n")
                return False

        except ValidationError as e:
            print("Validation error:", e.json())
            return False
        except Exception as e:
            print(f"An error occurred: {str(e)}")
            return False


    ##### VERSIÓN COMENTADA PARA LUEGO BORRAR *****

    # def volcadoSucursal(self, register: BranchRegister, result: ResultadoVolcado):

    #     print("\nEntrando al volcado de sucursal...")

    #     # Convert the input to JSON
    #     json_data = register.to_json()

    #     # Define the URL
    #     url = f"{self.BASE_URL}/{self.BRANCH_ENDPOINT}"

    #     # Consume the service
    #     # Convert the Branch object to a dictionary (you can adjust this based on your Register class method)
    #     try:
    #         payload = register.dict()
    #         response = requests.post(url, json=payload, headers=self.headers)

    #         if response.status_code == 200:
    #             data = response.json()
    #             data_section = data.get('data', {})  # Default to empty dict if 'data' is missing
    #             branch_id = data_section.get('branch_id', 'Unknown')
    #             local_code = data_section.get('local_code', 'Unknown')
    #             entity_id = data_section.get('entity_id', 'Unknown')
    #             print("Volcado de sucursal exitoso", data)
    #             print(f"\nParámetros de salida: branch_id = {branch_id} - local_code={local_code} - entity_id={entity_id}\n")

    #             result.Sucursales[0].branch_id = branch_id
    #             result.Sucursales[0].local_code = local_code
    #             result.Sucursales[0].entity_id = entity_id
            
    #             return True
    #         else:
    #             print(f"\nFailed with status code {response.status_code}: {response.text}\n")
    #             return False

    #     except ValidationError as e:
    #         print("Validation error:", e.json())
    #         return False
    #     except Exception as e:
    #         print(f"An error occurred: {str(e)}")
    #         return False
    



    def volcadoSucursal(self, register: BranchRegister, result: BranchResult):

        # Convert the input to JSON
        json_data = register.to_json()
        print("JSON Data:", json_data)

        # Define the URL
        url = f"{self.BASE_URL}/{self.BRANCH_ENDPOINT}"

        # Consume the service
        # Convert the Branch object to a dictionary (you can adjust this based on your Register class method)
        try:
            payload = register.model_dump()
            response = requests.post(url, json=payload, headers=self.headers)

            if response.status_code == 200:
                data = response.json()
                data_section = data.get('data', {})  # Default to empty dict if 'data' is missing

                # Toma los valores para el resultado
                result.source = "Volcado representante legal"
                result.message = data_section.get('response_message', 'Unknown')
                
                # Valida el código de resultado
                if data_section.get('response_code') != '0':
                    result.success = False
                    return False
                else:
                    result.success = True
                    print("Volcado de sucursal exitoso:")
                    
                    # Guardar parámetros de salida
                    result.branch_id = data_section.get('branch_id', 'Unknown')
                    result.entity_id = data_section.get('entity_id', 'Unknown')
                    result.local_code = data_section.get('local_code', 'Unknown')

                    print(data)
                    return True
                
            else:
                print(f"\nFailed with status code {response.status_code}: {response.text}\n")
                return False

        except ValidationError as e:
            print("Validation error:", e.json())
            return False
        except Exception as e:
            print(f"An error occurred: {str(e)}")
            return False
        
   
   
    # Método para volcar representante legal
    def volcadoRepresentanteLegal(self, register: RepresentativeRegister, result: ResultFuncion):
        """Sends a request to register a legal representative."""
        print("\nGenerando objeto de representante legal")

        json_data = register.to_json()
        print("JSON Data:", json_data)

        url = f"{self.BASE_URL}/{self.REPRESENTATIVE_ENDPOINT}"

        try:
            payload = register.model_dump()
            response = requests.post(url, json=payload, headers=self.headers)

            if response.status_code == 200:
                data = response.json()
                data_section = data.get('data', {})
                
                # Toma los valores para el resultado
                result.source = "Volcado representante legal"
                result.message = data_section.get('response_message', 'Unknown')

                # Valida el código de resultado
                if data_section.get('response_code') != '0':
                    result.success = False
                    return False
                else:
                    result.success = True
                    print("Volcado de representante legal exitoso:")
                    print(data)
                    return True
                
            else:
                print(f"Failed with status code {response.status_code}: {response.text}")
                return False

        except ValidationError as e:
            print("Validation error:", e.json())
            return False
        except Exception as e:
            print(f"An error occurred: {str(e)}")
            return False

    # Método para volcar los servicios de sucursal
    def volcadoServicioSucursal(self, register: RepresentativeRegister, result: ServiceResult):

        json_data = register.to_json()
        print("JSON Data:", json_data)

        url = f"{self.BASE_URL}/{self.SERVICES_ENDPOINT}"

        try:
            payload = register.model_dump()
            response = requests.post(url, json=payload, headers=self.headers)

            if response.status_code == 200:
                data = response.json()
                data_section = data.get('data', {})
                
                # Toma los valores para el resultado
                result.source = "Volcado servicio sucursal"
                result.message = data_section.get('response_message', 'Unknown')

                # Valida el código de resultado
                if data_section.get('response_code') != '0':
                    result.success = False
                    return False
                else:
                    result.success = True
                    print("Volcado de servicio sucursal exitoso:")
                    result.service_branch_id = data_section.get('service_branch_id')
                    print(data)
                    return True
                
            else:
                print(f"Failed with status code {response.status_code}: {response.text}")
                return False

        except ValidationError as e:
            print("Validation error:", e.json())
            return False
        except Exception as e:
            print(f"An error occurred: {str(e)}")
            return False



    def volcadoPaymentType(self, register: RepresentativeRegister, result: PaymentTypeResult):

        # Usar lista estática de payment types
        PAYMENT_TYPES = ("PREPAGO", "CREDITO", "DEBITO")
        
        # Lista para manejar las respuestas
        payment_type_ids = []

        # Condición de éxito global
        GLOBAL_PT_SUCCESS = True

        for payment_type in PAYMENT_TYPES:

            # Modificar la descripción del request para tomar el Payment Type correspondiente
            register.description = payment_type

            print(f'Llamaremos con payment type = {register.description}')
        
            json_data = register.to_json()
            print("JSON Data:", json_data)

            url = f"{self.BASE_URL}/{self.PAYMENT_TYPE_ENDPOINT}"

            try:
                payload = register.model_dump()
                response = requests.post(url, json=payload, headers=self.headers)

                if response.status_code == 200:
                    data = response.json()
                    data_section = data.get('data', {})
                    
                    # Toma los valores para el resultado
                    result.source = "Volcado Payment Type con tipo " + payment_type 
                    result.message = data_section.get('response_message', 'Unknown')

                    # Valida el código de resultado
                    if data_section.get('responseCode') != '0':
                        result.success = False
                        GLOBAL_PT_SUCCESS = False
                        print(data_section)
                        return False
                    else:
                        result.success = True
                        print("Volcado de servicio payment type exitoso:")
                        # Agregar valor del payment type id
                        payment_type_ids.append(data_section.get('paymentTypeId'))
                    
                else:
                    print(f"Failed with status code {response.status_code}: {response.text}")
                    return False

            except ValidationError as e:
                print("Validation error:", e.json())
                return False
            except Exception as e:
                print(f"An error occurred: {str(e)}")
                return False
        
        if GLOBAL_PT_SUCCESS:
            result.payment_type_id = payment_type_ids
            return True


    # Método para volcar el terminal
    def volcadoTerminal(self, register: RepresentativeRegister, result: TerminalResult):

        json_data = register.to_json()
        print("JSON Data:", json_data)

        url = f"{self.BASE_URL}/{self.TERMINAL_ENDPOINT}"

        try:
            payload = register.model_dump()
            response = requests.post(url, json=payload, headers=self.headers)

            if response.status_code == 200:
                data = response.json()
                data_section = data.get('data', {})
                
                # Toma los valores para el resultado
                result.source = "Volcado terminal"
                result.message = data_section.get('responseMessage', 'Unknown')

                # Valida el código de resultado
                if data_section.get('responseCode') != '0':
                    result.success = False
                    print(data_section)
                    return False
                else:
                    result.success = True
                    print("Volcado de servicio sucursal exitoso:")
                    result.terminal = data_section.get('terminal')
                    result.collector = data_section.get('collector')
                    result.billing_price = data_section.get('billingPrice')
                    print(data)
                    return True
                
            else:
                print(f"Failed with status code {response.status_code}: {response.text}")
                return False

        except ValidationError as e:
            print("Validation error:", e.json())
            return False
        except Exception as e:
            print(f"An error occurred: {str(e)}")
            return False


    # Método para volcar el contrato
    def volcadoContrato(self, register: RepresentativeRegister, result: ContratoResult):

        json_data = register.to_json()
        print("JSON Data:", json_data)

        url = f"{self.SIGN_URL}/{self.CONTRATO_ENDPOINT}"

        try:
            payload = register.model_dump()
            response = requests.post(url, json=payload, headers=self.headers)

            if response.status_code == 200:
                data = response.json()
                data_section = data.get('data', {})
                
                # Toma los valores para el resultado
                result.source = "Volcado contrato"
                result.message = data_section.get('response_message', 'Unknown')

                # Valida el código de resultado
                if data_section.get('response_code') != '0':
                    result.success = False
                    print(data_section)
                    return False
                else:
                    result.success = True
                    print("Volcado de contrato exitoso:")

                    # Capturar resultados
                    result.date = data_section.get('date')
                    result.time = data_section.get('time')
                    
                    print(data)
                    return True
                
            else:
                print(f"Failed with status code {response.status_code}: {response.text}")
                return False

        except ValidationError as e:
            print("Validation error:", e.json())
            return False
        except Exception as e:
            print(f"An error occurred: {str(e)}")
            return False


    # Método para volcar merchant discount
    def volcadoMerchantDiscount(self, register: MerchantDiscountRegister, result: ResultFuncion):

        json_data = register.to_json()
        print("JSON Data:", json_data)

        url = f"{self.BASE_URL}/{self.MERCHANT_ENDPOINT}"

        try:
            payload = register.model_dump()
            response = requests.post(url, json=payload, headers=self.headers)

            if response.status_code == 200:
                data = response.json()
                data_section = data.get('data', {})
                
                # Toma los valores para el resultado
                result.source = "Volcado servicio merchant discount"
                result.message = data_section.get('response_message', 'Unknown')

                # Valida el código de resultado
                if data_section.get('response_code') != '0':
                    result.success = False
                    return False
                else:
                    result.success = True
                    print("Volcado de servicio merchant discount exitoso:")
                    print(data)
                    return True
                
            else:
                print(f"Failed with status code {response.status_code}: {response.text}")
                return False

        except ValidationError as e:
            print("Validation error:", e.json())
            return False
        except Exception as e:
            print(f"An error occurred: {str(e)}")
            return False
    
    def volcadoCuentaBancaria(self, register: BankAccountRegister, result: BankAccountResult):
        
        json_data = register.to_json()
        print("JSON Data:", json_data)

        url = f"{self.BASE_URL}/{self.BANK_ACCOUNT_ENDPOINT}"

        try:
            payload = register.model_dump()
            response = requests.post(url, json=payload, headers=self.headers)

            if response.status_code == 200:
                data = response.json()
                data_section = data.get('data', {})
                
                # Toma los valores para el resultado
                result.source = "Volcado de cuenta bancaria"
                result.message = data_section.get('responseMessage', 'Unknown')

                # Valida el código de resultado
                if data_section.get('responseCode') != '0':
                    result.success = False
                    print(data_section)
                    return False
                else:
                    result.success = True
                    print("Volcado de cuenta bancaria exitosa:")

                    # Capturar resultados
                    result.account_id = data_section.get('accountId')
                    
                    print(data)
                    return True
                
            else:
                print(f"Failed with status code {response.status_code}: {response.text}")
                return False

        except ValidationError as e:
            print("Validation error:", e.json())
            return False
        except Exception as e:
            print(f"An error occurred: {str(e)}")
            return False


    def volcadoConfiguracionCuentaBancaria(self, register: BankAccountConfigurationRegister, result: ResultFuncion):

        json_data = register.to_json()
        print("JSON Data:", json_data)

        url = f"{self.BASE_URL}/{self.BANK_ACCOUNT_CONFIGURATION_ENDPOINT}"

        try:
            payload = register.model_dump()
            response = requests.post(url, json=payload, headers=self.headers)

            if response.status_code == 200:
                data = response.json()
                data_section = data.get('data', {})
                
                # Toma los valores para el resultado
                result.source = "Volcado de configuración de cuenta bancaria"
                result.message = data_section.get('responseMessage', 'Unknown')

                # Valida el código de resultado
                if data_section.get('responseCode') != '0':
                    result.success = False
                    print(data_section)
                    return False
                else:
                    result.success = True
                    print("Volcado de configuración de cuenta bancaria exitosa:")
                    print(data)
                    return True
                
            else:
                print(f"Failed with status code {response.status_code}: {response.text}")
                return False

        except ValidationError as e:
            print("Validation error:", e.json())
            return False
        except Exception as e:
            print(f"An error occurred: {str(e)}")
            return False
        

    def volcadoBranchCC(self, register: BranchCCRegister, result: ResultFuncion):

        json_data = register.to_json()
        print("JSON Data:", json_data)

        url = f"{self.BASE_URL}/{self.BRANCH_CC_ENDPOINT}"

        try:
            payload = register.model_dump()
            response = requests.post(url, json=payload, headers=self.headers)

            if response.status_code == 200:
                data = response.json()
                data_section = data.get('data', {})
                
                # Toma los valores para el resultado
                result.source = "Volcado de condiciones comerciales de sucursal"
                result.message = data_section.get('response_message', 'Unknown')

                # Valida el código de resultado
                if data_section.get('response_code') != '0':
                    result.success = False
                    print(data_section)
                    return False
                else:
                    result.success = True
                    print("Volcado de condiciones comerciales de sucursal exitoso:")
                    print(data)
                    return True
                
            else:
                print(f"Failed with status code {response.status_code}: {response.text}")
                return False

        except ValidationError as e:
            print("Validation error:", e.json())
            return False
        except Exception as e:
            print(f"An error occurred: {str(e)}")
            return False
    


    def volcadoTerminalCC(self, register: TerminalCCRegister, result: ResultFuncion):

        json_data = register.to_json()
        print("JSON Data:", json_data)

        url = f"{self.BASE_URL}/{self.TERMINAL_CC_ENDPOINT}"

        try:
            payload = register.model_dump()
            response = requests.post(url, json=payload, headers=self.headers)

            if response.status_code == 200:
                data = response.json()
                data_section = data.get('data', {})
                
                # Toma los valores para el resultado
                result.source = "Volcado de condiciones comerciales de terminal"
                result.message = data_section.get('responseMessage', 'Unknown')

                # Valida el código de resultado
                if data_section.get('responseCode') != '0':
                    result.success = False
                    print(data_section)
                    return False
                else:
                    result.success = True
                    print("Volcado de condiciones comerciales de terminal exitoso:")
                    print(data)
                    return True
                
            else:
                print(f"Failed with status code {response.status_code}: {response.text}")
                return False

        except ValidationError as e:
            print("Validation error:", e.json())
            return False
        except Exception as e:
            print(f"An error occurred: {str(e)}")
            return False
    

    def volcadoIswitchComercio(self, register: IswitchCommerceRegister, result: ResultFuncion):

        json_data = register.to_json()
        print("JSON Data:", json_data)

        url = f"{self.BASE_URL}/{self.ISWITCH_COMMERCE_ENDPOINT}"

        try:
            payload = register.model_dump()
            response = requests.post(url, json=payload, headers=self.headers)

            if response.status_code == 200:
                data = response.json()
                data_section = data.get('data', {})
                
                # Toma los valores para el resultado
                result.source = "Volcado de comercio en ISWITCH"
                result.message = data_section.get('responseMessage', 'Unknown')

                # Valida el código de resultado
                if data_section.get('responseCode') != '0':
                    result.success = False
                    print(data_section)
                    return False
                else:
                    result.success = True
                    print("Volcado de comcerio en ISWITCH exitoso:")
                    print(data)
                    return True
                
            else:
                print(f"Failed with status code {response.status_code}: {response.text}")
                return False

        except ValidationError as e:
            print("Validation error:", e.json())
            return False
        except Exception as e:
            print(f"An error occurred: {str(e)}")
            return False
        
    
    def volcadoIswitchBranch(self, register: IswitchBranchRegister, result: IswitchBranchResult):

        json_data = register.to_json()
        print("JSON Data:", json_data)

        url = f"{self.BASE_URL}/{self.ISWITCH_BRANCH_ENDPOINT}"

        try:
            payload = register.model_dump()
            response = requests.post(url, json=payload, headers=self.headers)

            if response.status_code == 200:
                data = response.json()
                data_section = data.get('data', {})
                
                # Toma los valores para el resultado
                result.source = "Volcado de sucursal en ISWITCH"
                result.message = data_section.get('responseMessage', 'Unknown')

                # Valida el código de resultado
                if data_section.get('responseCode') != '0':
                    result.success = False
                    print(data_section)
                    return False
                else:
                    result.success = True
                    result.branchIswId = data_section.get('branchIswId')
                    print("Volcado de sucursal en ISWITCH exitoso:")
                    print(data)
                    return True
                
            else:
                print(f"Failed with status code {response.status_code}: {response.text}")
                return False

        except ValidationError as e:
            print("Validation error:", e.json())
            return False
        except Exception as e:
            print(f"An error occurred: {str(e)}")
            return False
        
    
    def volcadoIswitchTerminal(self, register: IswitchTerminalRegister, result: ResultFuncion):

        json_data = register.to_json()
        print("JSON Data:", json_data)

        url = f"{self.BASE_URL}/{self.ISWITCH_TERMINAL_ENDPOINT}"

        try:
            payload = register.model_dump()
            response = requests.post(url, json=payload, headers=self.headers)

            if response.status_code == 200:
                data = response.json()
                data_section = data.get('data', {})
                
                # Toma los valores para el resultado
                result.source = "Volcado de terminal en ISWITCH"
                result.message = data_section.get('response', 'Unknown')

                # Valida el código de resultado
                if data_section.get('responseCode') != '0':
                    result.success = False
                    print(data_section)
                    return False
                else:
                    result.success = True
                    print("Volcado de terminal en ISWITCH exitoso:")
                    print(data)
                    return True
                
            else:
                print(f"Failed with status code {response.status_code}: {response.text}")
                return False

        except ValidationError as e:
            print("Validation error:", e.json())
            return False
        except Exception as e:
            print(f"An error occurred: {str(e)}")
            return False
        
    def volcadoCommercePci(self, register: CommercePciRegister, result: ResultFuncion):

        json_data = register.to_json()
        print("JSON Data:", json_data)

        url = f"{self.BASE_URL}/{self.COMMERCE_PCI_ENDPOINT}"

        try:
            payload = register.model_dump()
            response = requests.post(url, json=payload, headers=self.headers)

            if response.status_code == 200:
                data = response.json()
                data_section = data.get('data', {})
                
                # Toma los valores para el resultado
                result.source = "Volcado de comercio en réplica PCI"
                result.message = data_section.get('response', 'Unknown')

                # Valida el código de resultado
                if data_section.get('result') != 0:
                    result.success = False
                    print(data_section)
                    return False
                else:
                    result.success = True
                    print("Volcado de comercio en réplica PCI exitoso:")
                    print(data)
                    return True
                
            else:
                print(f"Failed with status code {response.status_code}: {response.text}")
                return False

        except ValidationError as e:
            print("Validation error:", e.json())
            return False
        except Exception as e:
            print(f"An error occurred: {str(e)}")
            return False
        

    def volcadoCommerceSwitch(self, register: CommerceSwitchRegister, result: ResultFuncion):

        json_data = register.to_json()
        print("JSON Data:", json_data)

        url = f"{self.BASE_URL}/{self.COMMERCE_SWITCH_ENDPOINT}"

        try:
            payload = register.model_dump()
            response = requests.post(url, json=payload, headers=self.headers)

            if response.status_code == 200:
                data = response.json()
                data_section = data.get('data', {})
                
                # Toma los valores para el resultado
                result.source = "Volcado de comercio en Switch"
                result.message = data_section.get('response_message', 'Unknown')

                # Valida el código de resultado
                if data_section.get('response_code') != '0':
                    result.success = False
                    print(data_section)
                    return False
                else:
                    result.success = True
                    print("Volcado de comercio en Switch exitoso:")
                    print(data)
                    return True
                
            else:
                print(f"Failed with status code {response.status_code}: {response.text}")
                return False

        except ValidationError as e:
            print("Validation error:", e.json())
            return False
        except Exception as e:
            print(f"An error occurred: {str(e)}")
            return False
        
    
    def volcadoMonitorPlus(self, register: MonitorRegister, result: MonitorResult):

        json_data = register.to_json()
        print("JSON Data:", json_data)

        url = f"{self.BASE_URL}/{self.MONITOR_ENDPOINT}"

        try:
            payload = register.model_dump()
            response = requests.post(url, json=payload, headers=self.headers)

            if response.status_code == 200:
                data = response.json()
                data_section = data.get('data', {})
                
                # Toma los valores para el resultado
                result.source = "Volcado de comercio en Monitor Plus"
                result.message = data_section.get('response_message', 'Unknown')

                # Valida el código de resultado
                if data_section.get('response_code') != '0':
                    result.success = False
                    print(data_section)
                    return False
                else:
                    result.success = True
                    print("Volcado de comercio en Monitor Plus exitoso:")
                    print(data)
                    return True
                
            else:
                print(f"Failed with status code {response.status_code}: {response.text}")
                return False

        except ValidationError as e:
            print("Validation error:", e.json())
            return False
        except Exception as e:
            print(f"An error occurred: {str(e)}")
            return False
        
    
    def volcadoRedPos(self, register: RedPosRegister, result: RedPosResult):

        json_data = register.to_json()
        print("JSON Data:", json_data)

        url = f"{self.BASE_URL}/{self.RED_POS_ENDPOINT}"

        try:
            payload = register.model_dump()
            response = requests.post(url, json=payload, headers=self.headers)

            if response.status_code == 200:
                data = response.json()
                data_section = data.get('data', {})
                
                # Toma los valores para el resultado
                result.source = "Volcado de ticket en RedPos"
                result.message = data_section.get('responseMessage', 'Unknown')

                # Valida el código de resultado
                if data_section.get('responseCode') != '0':
                    result.success = False
                    print(data_section)
                    return False
                else:
                    result.success = True
                    print("Volcado de comercio ticket en RedPos exitoso:")
                    result.ticket = data_section.get('ticket')
                    print(data)
                    return True
                
            else:
                print(f"Failed with status code {response.status_code}: {response.text}")
                return False

        except ValidationError as e:
            print("Validation error:", e.json())
            return False
        except Exception as e:
            print(f"An error occurred: {str(e)}")
            return False


