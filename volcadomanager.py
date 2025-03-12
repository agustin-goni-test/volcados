import requests
from pydantic import ValidationError
from resultvolcado import ResultadoVolcado, ResultFuncion
from registrosvolcado import RepresentativeRegister, BankAccountRegister, BankAccountConfigurationRegister, Register, BranchRegister
from registrosvolcado import TicketRegister

class VolcadoManager:
    BASE_URL = "https://apidev.mcdesaqa.cl/central/af/ayc/registry/commerce/v1/register"
    TICKET_URL = "https://apidev.mcdesaqa.cl/central/af/ayc/registry/commerce/v1/ticket"
    PING_ENDPOINT = "ping"
    
    REPRESENTATIVE_ENDPOINT = "representative"
    BANK_ACCOUNT_ENDPOINT = "bankAccount"
    BANK_ACCOUNT_CONFIGURATION_ENDPOINT = "bankAccount/configuration"
    COMMERCE_ENDPOINT = ""
    BRANCH_ENDPOINT = "branch"
    TICKET_ENDPOINT = ""

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

   
    # Método para volcar el comercio central
    def volcadoComercio(self, register: Register, result: ResultadoVolcado):
        """Sends a request to register a commerce."""
        print("Iniciando volcado comercio...")

        commerce_id=""
        entry=""
        agreement_id=""

        # Convert the Register object to JSON data
        json_data = register.to_json()
        print("JSON Data:", json_data)
        print("\n")

        # Use the COMMERCE_ENDPOINT for the URL
        url = f"{self.BASE_URL}/{self.COMMERCE_ENDPOINT}"

        # Consume the service
        try:
            # Convert the Register object to a dictionary (you can adjust this based on your Register class method)
            payload = register.dict()
            response = requests.post(url, json=payload, headers=self.headers)

            if response.status_code == 200:
                data = response.json()
                data_section = data.get('data', {})  # Default to empty dict if 'data' is missing
                commerce_id = data_section.get('commerce_id', 'Unknown')
                entry = data_section.get('entry', 'Unknown')
                agreement_id = data_section.get('agreement_id', 'Unknown')
                print("Volcado comercio exitoso:", data)
                print(f"\nParámetros de salida: commerce_id = {commerce_id} - entry = {entry} - agreement_id = {agreement_id}\n")

                # Agregar los parámetros correspondientes al resultado
                result.ComercioCentral.commerce_id = commerce_id
                result.ComercioCentral.entry = entry
                result.ComercioCentral.agreement_id = agreement_id

                # Retornar condición de éxito
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

    
    def volcadoTicket(self, register: TicketRegister, result: ResultadoVolcado):
        print("Iniciando volcado de ticket...")

        # Convert the Register object to JSON data
        json_data = register.to_json()
        print("JSON Data:", json_data)
        print("\n")

        date = ""
        time = ""

        # Use the TICKET_ENDPOINT for the URL
        url = f"{self.TICKET_URL}/{self.TICKET_ENDPOINT}"

        # Consume the service
        try:
            # Convert the Register object to a dictionary (you can adjust this based on your Register class method)
            payload = register.dict()
            response = requests.post(url, json=payload, headers=self.headers)

            if response.status_code == 200:
                data = response.json()
                data_section = data.get('data', {})  # Default to empty dict if 'data' is missing
                date = data_section.get('date', 'Unknown')
                time = data_section.get('time', 'Unknown')
                date_and_time = date + " " + time
                print("Volcado ticket exitoso:", data)
                print(f"\nParámetros de salida: ComercioTicketDateAndTime = {date_and_time}\n")

                # Guardar parámetro de resultado
                result.ComercioCentral.ComercioTicketDateAndTime = date_and_time
                
                # Retornar condicion de éxito
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


    def volcadoSucursal(self, register: BranchRegister, result: ResultadoVolcado):

        print("\nEntrando al volcado de sucursal...")

        # Convert the input to JSON
        json_data = register.to_json()

        # Define the URL
        url = f"{self.BASE_URL}/{self.BRANCH_ENDPOINT}"

        # Consume the service
        # Convert the Branch object to a dictionary (you can adjust this based on your Register class method)
        try:
            payload = register.dict()
            response = requests.post(url, json=payload, headers=self.headers)

            if response.status_code == 200:
                data = response.json()
                data_section = data.get('data', {})  # Default to empty dict if 'data' is missing
                branch_id = data_section.get('branch_id', 'Unknown')
                local_code = data_section.get('local_code', 'Unknown')
                entity_id = data_section.get('entity_id', 'Unknown')
                print("Volcado de sucursal exitoso", data)
                print(f"\nParámetros de salida: branch_id = {branch_id} - local_code={local_code} - entity_id={entity_id}\n")

                result.Sucursales[0].branch_id = branch_id
                result.Sucursales[0].local_code = local_code
                result.Sucursales[0].entity_id = entity_id
            
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
            payload = representative.dict()
            response = requests.post(url, json=payload, headers=self.headers)

            if response.status_code == 200:
                data = response.json()
                data_section = data.get('data', {})
                print("Volcado de representante legal exitoso:")
                print(data)
                result.success = True
                result.source = "Volcado representante legal"
                result.message = data_section.get('response_message', 'Unknown')
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

    
    def volcadoCuentaBancaria(self):
        # Create bank account
        bank_account = BankAccountRegister(
            commerceRut="15202083-K",
            holderRut="15202083-K",
            holderName="Pepe",
            accountTypeCode=2,
            bankAccount=45362345,
            user="AYC",
            bankCode=28,
            holderMail="pepe@gmail.com",
            serviceId=4,
            paymentType="PAGO EN CUENTA BANCARIA"
        )

        # Define URL for this endpoint
        url = f"{self.BASE_URL}/{self.BANK_ACCOUNT_ENDPOINT}"

        # Convert to JSON (ensuring correct alias format)
        json_data = bank_account.to_json()
        print("JSON Output:", json_data)

        try:
            # Convert to dictionary with alias-aware dumping
            payload = bank_account.dict()

            # Send POST request
            response = requests.post(url, json=payload, headers=self.headers)

            # Check if response is OK (HTTP 200)
            if response.status_code == 200:
                response_data = response.json()  # Convert response to JSON

                # Extract and print the accountId
                account_id = response_data.get("data", {}).get("accountId")
                
                if account_id is not None:
                    print(f"Bank Account Created! Account ID: {account_id}")
                    print(f'\nVolcado de cuenta bancaria ==> CHECK, accountID = {account_id}\n')
                else:
                    print("Error: 'accountId' not found in response.")

            else:
                print(f"API request failed with status code {response.status_code}: {response.text}")

        except requests.exceptions.RequestException as e:
            print(f"An error occurred: {str(e)}")


    def volcadoConfiguracionCuentaBancaria(self):
        # Create configuration
        bank_account_configuration = BankAccountConfigurationRegister(
            accountId=86844,
            commerceRut="15202083-K",
            financedRut="15202083-K",
            localCode=203744,
            user="AYC",
            serviceId=4,
            paymentType="CUENTA_BANCARIA"
        )

        # Define URL for this endpoint
        url = f"{self.BASE_URL}/{self.BANK_ACCOUNT_CONFIGURATION_ENDPOINT}"

        # Convert to JSON (ensuring correct alias format)
        json_data = bank_account_configuration.to_json()
        print("JSON Output:", json_data)

        try:
            # Convert to dictionary with alias-aware dumping
            payload = bank_account_configuration.dict()

            # Send POST request
            response = requests.post(url, json=payload, headers=self.headers)

            # Check if response is OK (HTTP 200)
            if response.status_code == 200:
                response_data = response.json()  # Convert response to JSON                
                print("Bank Account Created!")
                print(response_data)
                print("\nVolcado de cuenta bancaria ==> CHECK\n")

            else:
                print(f"API request failed with status code {response.status_code}: {response.text}")

        except requests.exceptions.RequestException as e:
            print(f"An error occurred: {str(e)}")


