# CRUD Microservice Code Generator

This AI-powered tool automates the creation of CRUD microservices, generating server code in JavaScript. It follows an **API-First development approach**, ensuring that API design serves as the foundation of application development.

---

## **API-First Approach Overview**

The **API-First approach** emphasizes defining your API before writing any code. Key steps include:

1. Creating a detailed API specification using tools like OpenAPI.
2. Using the API spec as a blueprint for development and testing.
3. Aligning all application components and external systems with the API’s structure and functionality.

This approach is particularly effective for microservices, facilitating clear communication between services and ensuring consistent integration.

---

## **Setup**

Follow these steps to set up the CRUD Microservice Code Generator:

1. **Navigate to the Frontend Repository**: 
   - Go to the `frontend` folder and run:
     ```bash
     npm install
     ```

2. **Run the Development Server**: 
   - Start the frontend development server with:
     ```bash
     npm run dev
     ```
   - Access the application at [http://localhost:5173/](http://localhost:5173/).

3. **Run the Backend Server**: 
   - Navigate to the folder containing `server.py`, then run:
     ```bash
     python server.py
     ```

4. **Ensure Both Servers Are Running**: 
   - The frontend and backend servers must be operational before using the system.

---

## **Requirements**

Make sure the following are met before proceeding:

- **Docker Installed**: Install Docker to run the generated microservice in a containerized environment.
- **Docker Running**: Ensure Docker is running, as the system relies on it to execute the server locally.

---

## **How to Use the CRUD Microservice Code Generator**

### **Step 1: Generate the OpenAPI Specification**
1. **Initiate the Process**: Start by prompting the system, e.g., "Generate OpenAPI spec for products microservice."
2. **Review the Spec**: The generated specification will appear on the left-hand side of the interface.
3. **Modify the Spec**: Update the spec as needed to suit your requirements.
4. **Save the Spec**: Command the system to save the spec to a file.  
   **Note**: The system will fail if this step is skipped.
5. **Verify File Creation**: Ensure the file `openapi_spec.yml` is created in your working directory.

---

### **Step 2: Generate the Server Code**
1. **Press the "Generate" Button**: Confirm that `openapi_spec.yml` is saved, then press "Generate" in the interface.
2. **Code Generation**: The system generates all necessary server code in a folder named `express-server`.
3. **Transition to Interaction Screen**: After code generation, you will be redirected to interact with the server.

---

### **Step 3: Interact with the Server**
1. **Run the Server Locally**: Command the system to run the server within a Docker container.
2. **Monitor Logs and Status**: Request logs and check the real-time status of services.
3. **Test the Endpoints**: Send test requests to the endpoints and observe the responses.
4. **Fix Code Issues**: If any issues arise, instruct the system to fix the code. It will make the necessary adjustments to ensure functionality.

---

## **Goal**

The system streamlines the entire development process, enabling you to:

- Generate an API specification.
- Create server code.
- Test and debug a fully functional microservice.

All tasks are performed interactively with the LLM, ensuring an efficient and seamless development workflow centered around a well-defined API.
