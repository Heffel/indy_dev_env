# **Health Institute Demonstration - Alice Patient - Immunization Center**  

### This is a demonstration script for Aries agents aimed at observing the issuance and validation of verifiable credentials within the Hyperledger stack, as well as the interaction of agents with the Indy blockchain.  

### The agents: Health Institute (healthInst), Alice Patient (alice), and Immunization Center (ImmuCent) are adaptations of the Faber, Alice, and ACME agents provided by aca-py.org. For more information, check https://aca-py.org/latest/aca-py.org/  

### ACA-Py supports Aries Interop Profile (AIP) 2.0, offering key protocols for issuing, verifying, and storing verifiable credentials (VCs) in the Hyperledger AnonCreds format, covering Zero-Knowledge Proof (ZKP) operations used by Aries/AnonCreds implementations in agents.  

---

## **Health Institute**  

Credential issuer: It will issue credentials to Alice containing information that will determine her eligibility for a vaccination campaign.  

- **Option "1g"**: Alice is over 18 and has a special condition (represented by status **1**).  
- **Option "1b"**: Alice is under 18 and does not have the condition (represented by **0**).  

The Health Institute agent also has a method to validate credentials issued by it.  

---

## **Alice Patient**  

A patient candidate for a vaccination campaign. Alice requests a verifiable credential from the Health Institute containing proof of her health condition and age. This credential will be presented to the Immunization Center as a requirement for an experimental vaccination campaign.  

---

## **Immunization Center**  

Verifier/Credential Issuer: The Immunization Center will request a verifiable presentation from Alice, where she will present the credential issued by the Health Institute containing proof of her age and condition. The Immunization Center can also issue a new credential confirming her approval for the campaign.  

---

## **SETUP**  

The proposed demonstration requires completing the steps in the [README.md](https://github.com/Heffel/indy_dev_env/blob/master/README.md) file.  

If you have not completed them yet, stop here, visit [README.md](https://github.com/Heffel/indy_dev_env/blob/master/README.md), and return after following the listed steps.  

### **Copying the Demo Files to the Lab Folder**  

As described in the [README.md](https://github.com/Heffel/indy_dev_env/blob/master/README.md) file, the virtual machine has a **lab** directory mapped to a level above the project directory. This **lab** directory enables interaction between the host machine (e.g., IDEs) and files visible within the virtual machine.  

We will copy the provided files to the **lab** directory and execute them from there.  

You can do this in two ways:  

#### **Option 1a - Copy the "docker_demo" folder using the host machine's file manager:**  

1. Locate the project directory using your file manager.  
2. Inside the project directory, find the **docker_demo** folder.  
3. Copy the **docker_demo** folder to the level above the project folder.  

**Example:**  
If the project folder is saved in:  
`C:/media/user/projects/indy_dev_env/`  
Copy the **docker_demo** folder to:  
`C:/media/user/projects/`  

![image](https://github.com/user-attachments/assets/e089b029-e958-4dc3-97f1-8e7d27839374)


#### **Option 1b - Copy the "docker_demo" folder using the virtual machine's command line:**  

1. Ensure you are in the **/home/vagrant** directory by typing:  

```bash  
cd ~ 
```  

2. Run the following command:  

```bash  
cp -r ../../lab/indy_dev_env/docker_demo/ ../../lab/docker_demo 
```  

**Important:**  
The **docker_demo** folder must be copied to the **lab** folder. Running the agents from their original location (inside the Git repository folder) may cause startup issues.  

---

## **Obtaining LEDGER_URL**  

The Aries agents provided by aca-py are designed to run on **localhost** and will attempt to connect to the **von-network** blockchain at `localhost:9000`.  

However, since we are running them on a virtual machine, the blockchain **will not be listening on localhost:9000**. Instead, we need to determine the correct IP address to observe transactions on the **von-network**.  

1. **Ensure the von-network is running** in the virtual machine. Instructions for this are available in the [README.md](https://github.com/Heffel/indy_dev_env/blob/master/README.md).  
2. **Obtain the correct IP address** of the von-network using the instructions in [README.md](https://github.com/Heffel/indy_dev_env/blob/master/README.md).  
3. **Example:** Let's assume the von-network is running at `192.168.178.172:9000`.  

---

## **STARTING THE AGENTS**  

### **1. Open a command-line terminal in the project's main folder (where the **Vagrantfile** is located).**  
### **2. Access the virtual machine using:**  

```bash 
vagrant ssh 
```   

### **3. Verify that the **von-network** nodes and **PostgreSQL** containers are running using:**  

```bash   
sudo docker ps 
```   

This should list the running containers:  

```bash 
CONTAINER ID   IMAGE              COMMAND                  CREATED        STATUS        PORTS                                                           NAMES 
b52d061ec5db   von-network-base   "./scripts/start_nod…"   24 hours ago   Up 24 hours   0.0.0.0:9707-9708->9707-9708/tcp, :::9707-9708->9707-9708/tcp   von-node4-1 
212f7587dde3   von-network-base   "./scripts/start_nod…"   24 hours ago   Up 24 hours   0.0.0.0:9701-9702->9701-9702/tcp, :::9701-9702->9701-9702/tcp   von-node1-1 
07f02a4e8827   von-network-base   "./scripts/start_nod…"   24 hours ago   Up 24 hours   0.0.0.0:9705-9706->9705-9706/tcp, :::9705-9706->9705-9706/tcp   von-node3-1 
3261605956b9   von-network-base   "bash -c 'sleep 10 &…"   24 hours ago   Up 24 hours   0.0.0.0:9000->8000/tcp, :::9000->8000/tcp                       von-webserver-1 
b1591e3c60e2   von-network-base   "./scripts/start_nod…"   24 hours ago   Up 24 hours   0.0.0.0:9703-9704->9703-9704/tcp, :::9703-9704->9703-9704/tcp   von-node2-1 
2ff0aac77b96   postgres           "docker-entrypoint.s…"   24 hours ago   Up 24 hours   0.0.0.0:5432->5432/tcp, :::5432->5432/tcp                       some-postgres 
```   

### **4. Navigate to the **lab/runners** directory:**  

```bash   
cd ../../lab/docker_demo/demo  
```   

### **5. Start the **Alice** agent by running:**

```bash   
sudo ./run_demo alice 
```   

Once the command is executed, the **run_demo** script will build the Docker container hosting the Alice agent. This step may take a few minutes.  

### **6. Open the **von-network** interface in a web browser and go to **Ledger State > Domain**.**  

Since Alice is a **holder** agent, she does not interact with the blockchain directly. She will wait for communication from the **Health Institute** and **Immunization Center**, which will register their credential schemas on the blockchain.  

### **7. In the terminal, verify that Alice has obtained the **genesis file** from the ledger and is running:**  

```bash   
#9 Input invitation details 
Invite details:            
```   


### **08 - Starting the Health Institute Agent**  

Repeat steps **01, 02, and 04**. Once inside the **demo** folder, run the Health Institute agent using the command:  

```bash   
sudo ./run_demo faber
```   

Notice that **"faber"** is the name of the **faber.py** file inherited from the original ACA-Py demo. When checking the code, you will see that it corresponds to the **Health Institute** agent.  

### **09 - Credential Schema Registration**  

During initialization, the **Health Institute** agent will display the credential schema it registers on the blockchain. It should look like this:  

```bash   
#3/4 Create a new schema/cred def on the ledger
Schema:
  {
    "sent": {
      "schema_id": "6jMNVK6f3WCY31ZL9ZXn5F:2:health schema:83.72.27",
      "schema": {
        "ver": "1.0",
        "id": "6jMNVK6f3WCY31ZL9ZXn5F:2:health schema:83.72.27",
        "name": "health schema",
        "version": "83.72.27",
        "attrNames": [
          "name",
          "date",
          "timestamp",
          "birthdate_dateint",
          "condition"
        ],
        "seqNo": 20
      }
    },
    "schema_id": "6jMNVK6f3WCY31ZL9ZXn5F:2:health schema:83.72.27",
    "schema": {
      "ver": "1.0",
      "id": "6jMNVK6f3WCY31ZL9ZXn5F:2:health schema:83.72.27",
      "name": "health schema",
      "version": "83.72.27",
      "attrNames": [
        "name",
        "date",
        "timestamp",
        "birthdate_dateint",
        "condition"
      ],
      "seqNo": 20
    }
  }
  
Schema ID: 6jMNVK6f3WCY31ZL9ZXn5F:2:health schema:83.72.27
Cred def ID: 6jMNVK6f3WCY31ZL9ZXn5F:3:CL:20:healthInstitute.agent.health_schema
```   

### **10 - Viewing the Schema in the Blockchain**  

Open **von-network** in your web browser, scroll to the bottom right section **"Ledger State"**, and click on the **"Domain"** link.  

Unlike Alice Patient, the Health Institute agent generates **entries on the blockchain**, as it has the ability to issue verifiable credentials.  

Check the following fields:  

- **Message wrapper**  
- **Metadata**  
- **Transaction** (This field will contain the alias `"healthInstitute.agent"`).  

### **11 - Expand the **"raw data"** field to examine the schema structure.**  

---

### **12 - Verifying the Agent’s Status**  

Return to the terminal and verify that the **Health Institute** agent is running and has generated connection data. The output should look like the following example:  

![image](https://github.com/user-attachments/assets/b2f7edc3-1f9e-4c61-9238-13da3d2bcc2c)  

---

### **⚠️ Important:**  

Do **not** copy the connection data shown here. Instead, use the connection details generated in your terminal.  

```bash   
Invitation Data: 
{"@type": "https://didcomm.org/out-of-band/1.1/invitation", "@id": "d7036e77-455d-4c37-b6a1-8852dfac8640", "handshake_protocols": ["https://didcomm.org/didexchange/1.0"], "services": [{"id": "#inline", "type": "did-communication", "recipientKeys": ["did:key:z6MkegshLyXJRnyYTCirvPR81J725UBNpJUN9sNZGjpdDY8d"], "serviceEndpoint": "http://localhost:8020"}], "label": "healthInstitute.agent"}
```   

### **13 - Extract the Connection Data**  

Use only the part after `"Data:"`.  

```bash   
{"@type": "https://didcomm.org/out-of-band/1.1/invitation", "@id": "d7036e77-455d-4c37-b6a1-8852dfac8640", "handshake_protocols": ["https://didcomm.org/didexchange/1.0"], "services": [{"id": "#inline", "type": "did-communication", "recipientKeys": ["did:key:z6MkegshLyXJRnyYTCirvPR81J725UBNpJUN9sNZGjpdDY8d"], "serviceEndpoint": "http://localhost:8020"}], "label": "healthInstitute.agent"}
```  

Paste this into the terminal of the **Alice Patient** agent and press **ENTER** to establish a session between the two agents, enabling their operational menus.  

---

### **14 - Alice’s Agent Menu**  

After connecting, Alice’s terminal should display:  

```bash   
Alice      | Connected 
Alice      | Check for endorser role ... 
Connect duration: 0.35s 
    (3) Send Message 
    (4) Input New Invitation
    (5) Display All Credentials 
    (X) Exit?                                                                                                                                                                                                                               

[3/4/X]                          
```   

---

### **15 - Health Institute’s Agent Menu**  

The **Health Institute** agent’s menu should look like this:  

```bash   
HealthInstitute | Check for endorser role ...
    (1g) Issue Good Credential
    (1b) Issue Bad Credential
    (1a) Set Credential Type (indy)
    (2) Send Proof Request
    (2a) Send *Connectionless* Proof Request (requires a Mobile client)
    (3) Send Message
    (4) Create New Invitation
    (T) Toggle tracing on credential/proof exchange
    (X) Exit?                                                                                                                                                                                                     
[1/2/3/4/T/X]                              
```   

---

### **16 - Testing Communication Between Agents**  

To verify agent communication, we can send messages from **Alice to Health Institute** (or vice versa).  

In this example, we will send a message from **Alice to Health Institute**.  

1. Select **option 3** in Alice’s menu.  
2. Enter the message: `"Hello from Alice"`.  
3. Press **ENTER** to send the message.  

```bash  
Alice      | Connected 
Alice      | Check for endorser role ... 
Connect duration: 0.27s 
    (3) Send Message 
    (4) Input New Invitation
    (5) Display All Credentials
    (X) Exit?                                                                                                                                                                                                                                  
[3/4/X] 3                                                                                                                                                                                                                                      
Enter message: Hello from Alice                                                                                                                                                                                                               
Alice      | Received message: healthInstitute.agent received your message 
```   

---

### ** Checking Message Reception in Health Institute**  

In **Health Institute’s terminal**, you should see the received message:  

```bash  
HealthInstitute      | Connected 
HealthInstitute      | Check for endorser role ... 
HealthInstitute      | Received message: Hello from Alice 

    (1g) Issue Good Credential
    (1b) Issue Bad Credential
    (1a) Set Credential Type (indy)
    (2) Send Proof Request
    (2a) Send *Connectionless* Proof Request (requires a Mobile client)
    (3) Send Message
    (4) Create New Invitation
    (T) Toggle tracing on credential/proof exchange
    (X) Exit?                                                                                                                                                                                                                                                 

[1/2/3/4/T/X]                                      
```   


### **17 - Issuing a Credential to Alice**  

In **Health Institute**, we will issue a credential to Alice containing proof that she is **over 18 years old** and has a **special condition**.  

- In the **Health Institute** agent, select **option 1g**.  
- Observe the process in **Health Institute**:  

```bash  
#13 Issue good credential offer to X
HealthInstitute | Credential: state = offer-sent, cred_ex_id = 1cb8b5b6-7904-4fa1-884f-666681216997
HealthInstitute | Credential: state = request-received, cred_ex_id = 1cb8b5b6-7904-4fa1-884f-666681216997

#17 Issue credential to X
HealthInstitute | Credential: state = credential-issued, cred_ex_id = 1cb8b5b6-7904-4fa1-884f-666681216997
HealthInstitute | Credential: state = done, cred_ex_id = 1cb8b5b6-7904-4fa1-884f-666681216997
```   

---

### **18 - Checking Credential Reception in Alice**  

In **Alice’s** terminal, observe that the agent has received a credential:  

```bash  
Alice      | Credential: state = offer-received, cred_ex_id = add9926a-440e-4a9b-a974-777d2a6e73f7

#15 After receiving credential offer, send credential request
Alice      | Credential: state = request-sent, cred_ex_id = add9926a-440e-4a9b-a974-777d2a6e73f7
Alice      | Credential: state = credential-received, cred_ex_id = add9926a-440e-4a9b-a974-777d2a6e73f7

#18.1 Stored credential 2cb8fa7d-fcd9-4c79-a398-cfe080ac696e in wallet
Alice      | Credential: state = done, cred_ex_id = a216a6ee-49de-4197-be9a-39f48b28d0c0
Credential details:
  {
    "referent": "2cb8fa7d-fcd9-4c79-a398-cfe080ac696e",
    "schema_id": "6jMNVK6f3WCY31ZL9ZXn5F:2:health schema:83.72.27",
    "cred_def_id": "6jMNVK6f3WCY31ZL9ZXn5F:3:CL:20:healthInstitute.agent.health_schema",
    "rev_reg_id": null,
    "cred_rev_id": null,
    "attrs": {
      "birthdate_dateint": "20001108",
      "date": "2018-05-28",
      "timestamp": "1731078818",
      "condition": "1",
      "name": "Alice Smith"
    }
  }
  
Alice      | credential_id 2cb8fa7d-fcd9-4c79-a398-cfe080ac696e
Alice      | cred_def_id 6jMNVK6f3WCY31ZL9ZXn5F:3:CL:20:healthInstitute.agent.health_schema
Alice      | schema_id 6jMNVK6f3WCY31ZL9ZXn5F:2:health schema:83.72.27
```   

Alice’s **date of birth (2000/11/08)** makes her **over 18 years old**, and the **condition "1"** qualifies her for the **vaccination campaign** at the **Immunization Center**.  

---

### **19 - Verifying the Stored Credential in Alice**  

Check the newly stored credential in **Alice’s** agent.  

- Select **option 5** in **Alice’s menu** to list all credentials.  
- The output should look like this:  

```bash
All credentials: {'results': [{'referent': '2cb8fa7d-fcd9-4c79-a398-cfe080ac696e', 'schema_id': '6jMNVK6f3WCY31ZL9ZXn5F:2:health schema:83.72.27', 'cred_def_id': '6jMNVK6f3WCY31ZL9ZXn5F:3:CL:20:healthInstitute.agent.health_schema', 'rev_reg_id': None, 'cred_rev_id': None, 'attrs': {'date': '2018-05-28', 'birthdate_dateint': '20001108', 'name': 'Alice Smith', 'timestamp': '1731078818', 'condition': '1'}}]}
```  

---

### **20 - Official Credential Verification at Immunization Center**  

Even though Alice can verify her own credential, we will **officially request** credential verification using the **Immunization Center** agent.  

- If you want to perform an additional verification before proceeding, use **option 2** in **Health Institute**.  
- This option requests proof of the same attributes required by the **Immunization Center**.  

If verification is successful, **Health Institute's terminal** will display:  

```bash
#20 Request proof of health from patient
Generated proof request web request: {'connection_id': '07c9cb3a-e144-4476-b04c-ded0d6c074c2', 'presentation_request': {'indy': {'name': 'Proof of Health', 'version': '1.0', 'requested_attributes': {'0_name_uuid': {'name': 'name', 'restrictions': [{'schema_name': 'health schema'}]}, '0_date_uuid': {'name': 'date', 'restrictions': [{'schema_name': 'health schema'}]}}, 'requested_predicates': {'0_birthdate_dateint_GE_uuid': {'name': 'birthdate_dateint', 'p_type': '<=', 'p_value': 20061121, 'restrictions': [{'schema_name': 'health schema'}]}, '0_condition_GE_uuid': {'name': 'condition', 'p_type': '>=', 'p_value': 1, 'restrictions': [{'schema_name': 'health schema'}]}}}}, 'by_format': {'indy': {'name': 'Proof of Health', 'version': '1.0', 'requested_attributes': {'0_name_uuid': {'name': 'name', 'restrictions': [{'schema_name': 'health schema'}]}, '0_date_uuid': {'name': 'date', 'restrictions': [{'schema_name': 'health schema'}]}}, 'requested_predicates': {'0_birthdate_dateint_GE_uuid': {'name': 'birthdate_dateint', 'p_type': '<=', 'p_value': 20061121, 'restrictions': [{'schema_name': 'health schema'}]}, '0_condition_GE_uuid': {'name': 'condition', 'p_type': '>=', 'p_value': 1, 'restrictions': [{'schema_name': 'health schema'}]}}}}}
HealthInstitute | Presentation: state = request-sent, pres_ex_id = be1f4ec0-b8a5-47c9-b109-74f1b25523fe
HealthInstitute | Presentation: state = presentation-received, pres_ex_id = be1f4ec0-b8a5-47c9-b109-74f1b25523fe

#28 Check if proof is valid
HealthInstitute | Presentation: state = done, pres_ex_id = be1f4ec0-b8a5-47c9-b109-74f1b25523fe
HealthInstitute | Proof = true
```  

A **TRUE** value confirms that the expected conditions were successfully validated.  

In **Alice’s terminal**, the verification process appears as follows:  

```bash
Alice      | Presentation: state = request-received, pres_ex_id = 520e2068-5f8f-4af2-8a69-1fda389f3305

#24 Query for credentials in the wallet that satisfy the proof request
Presentation: state = request-received, pres_ex_id = 520e2068-5f8f-4af2-8a69-1fda389f3305

#25 Generate the indy proof

#26 Send the proof to X: {"indy": {"requested_predicates": {"0_birthdate_dateint_GE_uuid": {"cred_id": "d84ca4ac-2f24-41ea-89bf-72cbed23be3c"}, "0_condition_GE_uuid": {"cred_id": "d84ca4ac-2f24-41ea-89bf-72cbed23be3c"}}, "requested_attributes": {"0_name_uuid": {"cred_id": "d84ca4ac-2f24-41ea-89bf-72cbed23be3c", "revealed": false}, "0_date_uuid": {"cred_id": "d84ca4ac-2f24-41ea-89bf-72cbed23be3c", "revealed": true}}, "self_attested_attributes": {}}}
Alice      | Presentation: state = presentation-sent, pres_ex_id = 520e2068-5f8f-4af2-8a69-1fda389f3305
Presentation: state = presentation-sent, pres_ex_id = 520e2068-5f8f-4af2-8a69-1fda389f3305
Alice      | Presentation: state = done, pres_ex_id = 520e2068-5f8f-4af2-8a69-1fda389f3305
Presentation: state = done, pres_ex_id = 520e2068-5f8f-4af2-8a69-1fda389f3305
```

### **21 - In Alice, select option 4 to prepare the agent for a future connection with the Immunization Office agent.**  

### **22 - To start the Immunization Center agent, repeat steps 01, 02, and 04. Once in the runners folder, execute the Immunization Center agent using the command:**  

```bash   
sudo ./run_demo acme
```   

Note that **"acme"** is the name of the **acme.py** file inherited from the original ACA-Py demo. When checking the code, you will see that it corresponds to the **Immunization Center** agent.  

### **23 - During initialization, the Immunization Center agent will display credential schemas that it will register on the blockchain. It should look like this:**   
```bash   
#3/4 Create a new schema/cred def on the ledger
Schema:
  {
    "sent": {
      "schema_id": "4BNtF7ULEegATHDPq5qF2F:2:immunization id schema:47.13.59",
      "schema": {
        "ver": "1.0",
        "id": "4BNtF7ULEegATHDPq5qF2F:2:immunization id schema:47.13.59",
        "name": "immunization id schema",
        "version": "47.13.59",
        "attrNames": [
          "date",
          "position",
          "patient_id",
          "name"
        ],
        "seqNo": 24
      }
    },
    "schema_id": "4BNtF7ULEegATHDPq5qF2F:2:immunization id schema:47.13.59",
    "schema": {
      "ver": "1.0",
      "id": "4BNtF7ULEegATHDPq5qF2F:2:immunization id schema:47.13.59",
      "name": "immunization id schema",
      "version": "47.13.59",
      "attrNames": [
        "date",
        "position",
        "patient_id",
        "name"
      ],
      "seqNo": 24
    }
  }
  
Schema ID: 4BNtF7ULEegATHDPq5qF2F:2:immunization id schema:47.13.59
Cred def ID: 4BNtF7ULEegATHDPq5qF2F:3:CL:24:immunization.agent.immunization_id_schema
Publish schema/cred def duration: 9.23s
Schema:
  {
    "sent": {
      "schema_id": "4BNtF7ULEegATHDPq5qF2F:2:immunization id schema:16.22.94",
      "schema": {
        "ver": "1.0",
        "id": "4BNtF7ULEegATHDPq5qF2F:2:immunization id schema:16.22.94",
        "name": "immunization id schema",
        "version": "16.22.94",
        "attrNames": [
          "name",
          "patient_id",
          "date",
          "position"
        ],
        "seqNo": 26
      }
    },
    "schema_id": "4BNtF7ULEegATHDPq5qF2F:2:immunization id schema:16.22.94",
    "schema": {
      "ver": "1.0",
      "id": "4BNtF7ULEegATHDPq5qF2F:2:immunization id schema:16.22.94",
      "name": "immunization id schema",
      "version": "16.22.94",
      "attrNames": [
        "name",
        "patient_id",
        "date",
        "position"
      ],
      "seqNo": 26
    }
  }

Schema ID: 4BNtF7ULEegATHDPq5qF2F:2:immunization id schema:16.22.94
Cred def ID: 4BNtF7ULEegATHDPq5qF2F:3:CL:26:immunization.agent.immunization_id_schema
Publish schema and cred def duration: 6.49s

```   

### **24 - Access the von-network in your browser and locate the "Ledger State" section in the bottom right corner. Click on the "Domain" link.**  

Note that, just like the **Health Institute**, the **Immunization Center** has generated entries on the blockchain since it is an agent capable of issuing verifiable credentials.  

Check the following fields:  

- **Message wrapper**  
- **Metadata**  
- **Transaction** (The Transaction field will contain the attribute `"Alias: immunization.agent"`).  

Expand the **"raw data"** field to inspect the schema structure.  

---

### **25 - To establish communication between Alice and Immunization Center, select option 4 in Alice to input a new connection invitation.**  

### **26 - In Immunization Center, just like with Health Institute, copy the connection details and provide them in Alice. Alice will display the invitation response data.**  

---

### **27 - The Immunization Center agent's menu should look like this:**  
```bash   
Immunization | Connected
immunization.agent handle_connections completed completed
    (1) Issue Credential
    (2) Send Proof Request
    (3) Send Message
    (4) Create New Invitation
    (X) Exit?                                                                                                                                                                                                     
[1/2/3/X]                       
```   

In the proposed scenario, the Immunization Center will request a presentation from Alice, where she must provide a credential proving her age and special condition, which was previously issued by the Health Institute.

Once the request is made, Alice will automatically respond with the appropriate credential, which will then be validated.  

Next, the **Immunization Center** operator will issue a second **verifiable credential** to Alice using **option 1**, confirming her approval for the campaign.  

We can observe this second credential in the **Immunization Center** agent's code:  
```python   
                agent.cred_attrs[cred_def_id] = {
                    "patient_id": "IMMUN0009",
                    "name": "Alice Smith",
                    "date": datetime.date.today().strftime("%Y-%m-%d"),
                    "position": "APPROVED"
                }
                cred_preview = {
                    "@type": CRED_PREVIEW_TYPE,
                    "attributes": [
                        {"name": n, "value": v}
                        for (n, v) in agent.cred_attrs[cred_def_id].items()
                    ],
                }
                offer_request = {
                    "connection_id": agent.connection_id,
                    "comment": f"Offer on cred def id {cred_def_id}",
                    "credential_preview": cred_preview,
                    "filter": {"indy": {"cred_def_id": cred_def_id}},
                }
                await agent.admin_POST(
                    "/issue-credential-2.0/send-offer", offer_request
                )
```   

### **28 - In Immunization Center, select option 2 to request a presentation from Alice. The terminal in Immunization Center should display something like this:**

```bash   
#20 Request proof of health
Proof request sent: {
    "connection_id": "8336d778-965e-4ffd-8cd9-6a506204c827",
    "presentation_request": {
        "indy": {
            "name": "Proof of Health",
            "version": "1.0",
            "nonce": "211500893938358422591916050572689060843",
            "requested_attributes": {
                "0_name_uuid": {
                    "name": "name",
                    "restrictions": [
                        {
                            "schema_name": "health schema"
                        }
                    ]
                },
                "0_date_uuid": {
                    "name": "date",
                    "restrictions": [
                        {
                            "schema_name": "health schema"
                        }
                    ]
                }
            },
            "requested_predicates": {
                "0_birthdate_dateint_GE_uuid": {
                    "name": "birthdate_dateint",
                    "p_type": "<=",
                    "p_value": 20061121,
                    "restrictions": [
                        {
                            "schema_name": "health schema"
                        }
                    ]
                },
                "0_condition_GE_uuid": {
                    "name": "condition",
                    "p_type": ">=",
                    "p_value": 1,
                    "restrictions": [
                        {
                            "schema_name": "health schema"
                        }
                    ]
                }
            }
        }
    }
}
Immunization | Presentation: state = request-sent, pres_ex_id = c038962c-75e0-4d23-8de0-49a3149398ca
Immunization | Presentation: state = presentation-received, pres_ex_id = c038962c-75e0-4d23-8de0-49a3149398ca

#27 Process the proof provided by X

#28 Check if proof is valid
Immunization | Presentation: state = done, pres_ex_id = c038962c-75e0-4d23-8de0-49a3149398ca
Immunization | Proof =  true

#28.1 Received proof of health, check claims
Immunization | name: (attribute not revealed)
Immunization | date: 2018-05-28
Immunization | schema_id: 2tYgwKYx4TweHGaNJQ3Bjm:2:health schema:12.10.84
Immunization | cred_def_id 2tYgwKYx4TweHGaNJQ3Bjm:3:CL:18:healthInstitute.agent.health_schema
```

### **29 - Alice will respond with the credential issued by Health Institute:**  

```bash   
Alice      | Presentation: state = request-received, pres_ex_id = 9e07c488-485a-4cc8-920a-b6d1ed412147

#24 Query for credentials in the wallet that satisfy the proof request
Presentation: state = request-received, pres_ex_id = 9e07c488-485a-4cc8-920a-b6d1ed412147

#25 Generate the indy proof

#26 Send the proof to X: {"indy": {"requested_predicates": {"0_birthdate_dateint_GE_uuid": {"cred_id": "d84ca4ac-2f24-41ea-89bf-72cbed23be3c"}, "0_condition_GE_uuid": {"cred_id": "d84ca4ac-2f24-41ea-89bf-72cbed23be3c"}}, "requested_attributes": {"0_name_uuid": {"cred_id": "d84ca4ac-2f24-41ea-89bf-72cbed23be3c", "revealed": false}, "0_date_uuid": {"cred_id": "d84ca4ac-2f24-41ea-89bf-72cbed23be3c", "revealed": true}}, "self_attested_attributes": {}}}
Alice      | Presentation: state = presentation-sent, pres_ex_id = 9e07c488-485a-4cc8-920a-b6d1ed412147
Presentation: state = presentation-sent, pres_ex_id = 9e07c488-485a-4cc8-920a-b6d1ed412147
Alice      | Presentation: state = done, pres_ex_id = 9e07c488-485a-4cc8-920a-b6d1ed412147
Presentation: state = done, pres_ex_id = 9e07c488-485a-4cc8-920a-b6d1ed412147
```

### **30 - After verification, the Immunization Center operator can generate a new credential for Alice by selecting option 1.**
```bash
#13 Issue credential offer to X
Immunization | Credential: state = offer-sent, cred_ex_id = 58c9da46-85a1-44f6-ad4d-a0ebb4f35148
Immunization | Credential: state = request-received, cred_ex_id = 58c9da46-85a1-44f6-ad4d-a0ebb4f35148
Immunization | Credential: state = credential-issued, cred_ex_id = 58c9da46-85a1-44f6-ad4d-a0ebb4f35148
Immunization | Credential: state = done, cred_ex_id = 58c9da46-85a1-44f6-ad4d-a0ebb4f35148
``` 

### **31 - After the verification and issuance of the new credential, check in Alice's agent that it has been received:** 
```bash
Alice      | Credential: state = offer-received, cred_ex_id = d8b1a370-093c-48bb-8bfe-096849d8e1af

#15 After receiving credential offer, send credential request
Alice      | Credential: state = request-sent, cred_ex_id = d8b1a370-093c-48bb-8bfe-096849d8e1af
Alice      | Credential: state = credential-received, cred_ex_id = d8b1a370-093c-48bb-8bfe-096849d8e1af

#18.1 Stored credential 48cbd62d-e1e8-4401-891c-aad3106dd6ac in wallet
Alice      | Credential: state = done, cred_ex_id = d8b1a370-093c-48bb-8bfe-096849d8e1af
Credential details:
  {
    "referent": "48cbd62d-e1e8-4401-891c-aad3106dd6ac",
    "schema_id": "MBcUP9jtziBNBZNvhQS53G:2:immunization id schema:31.66.25",
    "cred_def_id": "MBcUP9jtziBNBZNvhQS53G:3:CL:24:immunization.agent.immunization_id_schema",
    "rev_reg_id": null,
    "cred_rev_id": null,
    "attrs": {
      "position": "APPROVED",
      "date": "2024-11-21",
      "name": "Alice Smith",
      "patient_id": "IMMUNI0009"
    }
  }
  
Alice      | credential_id 48cbd62d-e1e8-4401-891c-aad3106dd6ac
Alice      | cred_def_id MBcUP9jtziBNBZNvhQS53G:3:CL:24:immunization.agent.immunization_id_schema
Alice      | schema_id MBcUP9jtziBNBZNvhQS53G:2:immunization id schema:31.66.25
``` 

Now, option 5 will list two credentials, which should look like the following:  

```bash
All credentials: {'results': [{'referent': '74429c6c-93ad-457a-b8fc-89ec5e07ece5', 'schema_id': 'VeBrp2W8QMaiCeqsVzxpwS:2:health schema:39.2.95', 'cred_def_id': 'VeBrp2W8QMaiCeqsVzxpwS:3:CL:36:healthInstitute.agent.health_schema', 'rev_reg_id': None, 'cred_rev_id': None, 'attrs': {'timestamp': '1731083813', 'date': '2018-05-28', 'condition': '1', 'name': 'Alice Smith', 'birthdate_dateint': '20001108'}}, {'referent': '65134589-ed80-4343-ad53-ed9ac82774cd', 'schema_id': 'BAjHxoChwzMvdogdRyrvaf:2:immunization id schema:98.76.68', 'cred_def_id': 'BAjHxoChwzMvdogdRyrvaf:3:CL:42:immunization.agent.immunization_id_schema', 'rev_reg_id': None, 'cred_rev_id': None, 'attrs': {'position': 'APPROVED', 'date': '2024-11-08', 'patient_id': 'IMMUNI0009', 'name': 'Alice Smith'}}]}

```
* To test the scenario where Alice does not pass the verification:
1. Stop the **Alice** agent using option **"X"** and restart it.  
2. Establish a new connection with the **Health Institute** and issue a credential where **Alice does not qualify** for the vaccination campaign by selecting **option "1b"**.  
3. In Alice’s terminal, you will see:  

```bash
#18.1 Stored credential d8de13c4-411d-42bf-a7ea-1b3236c9e2b0 in wallet
Credential details:
  {
    "referent": "d8de13c4-411d-42bf-a7ea-1b3236c9e2b0",
    "schema_id": "2tYgwKYx4TweHGaNJQ3Bjm:2:health schema:12.10.84",
    "cred_def_id": "2tYgwKYx4TweHGaNJQ3Bjm:3:CL:18:healthInstitute.agent.health_schema",
    "rev_reg_id": null,
    "cred_rev_id": null,
    "attrs": {
      "condition": "0",
      "timestamp": "1732161948",
      "date": "2018-05-28",
      "birthdate_dateint": "20141121",
      "name": "Alice Smith"
    }
  }
```
Alice's **date of birth (2014/11/21)** makes her **under 18 years old**, and the **condition "0"** disqualifies her from the **Immunization Center’s vaccination campaign**.  

When requesting credential verification through the **Immunization Center** agent, Alice’s agent will log an error stack, ultimately confirming that the received identity does **not meet the expected predicate**.  

```bash
File "/home/aries/aries_cloudagent/protocols/present_proof/v2_0/routes.py", line 1229, in present_proof_send_presentation
Alice      |     await report_problem(
Alice      |   File "/home/aries/aries_cloudagent/protocols/present_proof/v2_0/__init__.py", line 57, in report_problem
Alice      |     raise http_error_class(reason=err.roll_up) from err
Alice      | aiohttp.web_exceptions.HTTPBadRequest: Error creating presentation. Invalid state: Predicate is not satisfied.
```

The **Immunization Center** agent will record that the proof **was abandoned**.  


```bash
Immunization | Presentation: state = request-sent, pres_ex_id = 245fb7ed-0879-40ee-b1c6-9b50a7464cc1
Immunization | Presentation: state = abandoned, pres_ex_id = 245fb7ed-0879-40ee-b1c6-9b50a7464cc1
```
### **All agents provide an API that can be accessed via the web browser on the host machine.**  

In this demonstration, the default ports are:  
- **8021** for **Health Institute**  
- **8031** for **Alice**  
- **8051** for **Bob**  
- **8041** for **Immunization Center**  

If you assigned different ports to the agents, the API will be available on **port +1**.  

**Example:** If **Alice** is listening on **8050**, the API will be available on **8051**.  

For this example, the **localhost URL** is:  
**http://192.168.178.172**  

http://192.168.178.172:8021/api/doc - HEALTH INSTITUTE

http://192.168.178.172:8031/api/doc - ALICE

http://192.168.178.172:8041/api/doc - IMMUNIZATION CENTER

![image](https://github.com/user-attachments/assets/04834245-62ea-4e60-bdc9-dddccfd7fdfa)


### **Let's look at an example of how we can query Alice's stored credentials:**  

1. Access **http://192.168.178.172:8031/api/doc**  
2. Locate the option: **"GET /credentials"**  
3. Fill in the fields for:  
   - The **number of credentials**  
   - The **search index**  
   - Leave **WQL** in the third field  

![image](https://github.com/user-attachments/assets/342d155b-7cf6-42ba-8e04-e7a952b3baa0)

3 - Clik on "EXECUTE"

4 - Scroll down and check the credentials in the response body.


![image](https://github.com/user-attachments/assets/b07d92b4-234c-478b-a092-048e27bc83dc)


### **More information on how to use the API can be found in the links above its options.**
![image](https://github.com/user-attachments/assets/cdb89631-aeab-4722-b81e-3620d0a10223)






