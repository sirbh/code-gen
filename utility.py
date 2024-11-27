import os
import json
from json_tricks import loads
import subprocess
import platform


def save_server_code(directory_name, json_data):
    # Ensure the directory name is within the current working directory
    directory_path = os.path.join(os.getcwd(), directory_name)

    
    # Create the directory if it does not exist
    if not os.path.exists(directory_path):
        os.makedirs(directory_path)
    
    # Load JSON data
    data = json_data


    # Iterate through the dictionary
    for relative_path, content in data.items():
        # Construct the absolute file path within the created directory
        file_path = os.path.join(directory_path, relative_path)

        # Create the directory if it does not exist
        directory = os.path.dirname(file_path)
        if not os.path.exists(directory):
            os.makedirs(directory)

        # Write the content to the file
        with open(file_path, 'w') as file:
            file.write(content)

    print(f"Files created successfully in {directory_path}.")

def directory_to_json(dir_path):
    json_data = {}

    for root, _, files in os.walk(dir_path):
        for file_name in files:
            if file_name == "package-lock.json":
                continue    
            file_path = os.path.join(root, file_name)
            # Calculate relative path from dir_path
            rel_path = os.path.relpath(file_path, dir_path)
            
            with open(file_path, 'r', encoding='utf-8') as f:
                file_content = f.read()
                json_data[rel_path] = file_content
    
    return json_data

def append_to_file(file_path, text):
    directory_path = os.path.join(os.getcwd(), file_path)
    try:
        # Open the file in append mode, which creates the file if it does not exist
        with open(directory_path, 'a') as file:
            # Write the text to the file
            file.write(text + '\n')
        print(f"Successfully appended to {directory_path}")
    except Exception as e:
        print(f"An error occurred while appending to the file: {e}")


def is_docker_running():
    try:
        # Check if Docker is installed by running the `docker --version` command
        subprocess.run(['docker', '--version'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
        
        # Check if Docker daemon is running by running `docker info`
        result = subprocess.run(['docker', 'info'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
        
        # If no exception is raised, Docker is installed and running
        return True
    except subprocess.CalledProcessError as e:
        # Docker is either not installed or not running
        print(f"Docker error: {e}")
        return False
    except FileNotFoundError:
        # Docker CLI is not found in PATH
        print("Docker is not installed.")
        return False



def run_command(command):
    """
    Runs a given terminal command and returns the output, error, and return code.
    
    Parameters:
    command (str): The terminal command to run.
    
    Returns:
    tuple: A tuple containing the output, error, and return code of the command.
    """
    directory_name="express-server"
    directory_path = os.path.join(os.getcwd(), directory_name)
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True, cwd=directory_path)
        return result.stdout, result.stderr, result.returncode
    except subprocess.CalledProcessError as e:
        return e.stdout, e.stderr, e.returncode

def append_json_to_file(json_object):
    # Check if the file exists
    directory_name="logs.json"
    directory_path = os.path.join(os.getcwd(), directory_name)
    file_exists = os.path.isfile(directory_path)

    # Open the file in append mode, create it if it doesn't exist
    with open(directory_path, 'a') as file:
        # Convert the JSON object to a string
        json_str = json.dumps(json_object)
        
        # Write the JSON string to the file followed by a newline
        file.write(json_str + '\n')







# print(json_data.items())

# json_data = {
#   "controllers/index.js": "const { PrismaClient } = require('@prisma/client');\nconst prisma = new PrismaClient();\n\nconst getFlavors = async (req, res) => {\n  try {\n    const flavors = await prisma.flavor.findMany();\n    res.json(flavors);\n  } catch (error) {\n    res.status(500).json({ error: 'Failed to fetch flavors' });\n  }\n};\n\nconst getFlavorById = async (req, res) => {\n  const { flavorId } = req.params;\n  try {\n    const flavor = await prisma.flavor.findUnique({ where: { id: flavorId } });\n    if (!flavor) {\n      return res.status(404).json({ message: 'Flavor not found' });\n    }\n    res.json(flavor);\n  } catch (error) {\n    res.status(500).json({ error: 'Failed to fetch flavor' });\n  }\n};\n\nconst createOrder = async (req, res) => {\n  const { customerId, items } = req.body;\n  try {\n    const order = await prisma.order.create({\n      data: {\n        customerId,\n        items: { create: items }\n      },\n      include: { items: true }\n    });\n    res.status(201).json(order);\n  } catch (error) {\n    res.status(500).json({ error: 'Failed to create order' });\n  }\n};\n\nconst getOrderById = async (req, res) => {\n  const { orderId } = req.params;\n  try {\n    const order = await prisma.order.findUnique({\n      where: { id: orderId },\n      include: { items: true }\n    });\n    if (!order) {\n      return res.status(404).json({ message: 'Order not found' });\n    }\n    res.json(order);\n  } catch (error) {\n    res.status(500).json({ error: 'Failed to fetch order' });\n  }\n};\n\nconst getCustomerById = async (req, res) => {\n  const { customerId } = req.params;\n  try {\n    const customer = await prisma.customer.findUnique({ where: { id: customerId } });\n    if (!customer) {\n      return res.status(404).json({ message: 'Customer not found' });\n    }\n    res.json(customer);\n  } catch (error) {\n    res.status(500).json({ error: 'Failed to fetch customer' });\n  }\n};\n\nmodule.exports = { getFlavors, getFlavorById, createOrder, getOrderById, getCustomerById };",
#   "routes/index.js": "const express = require('express');\nconst router = express.Router();\nconst { getFlavors, getFlavorById, createOrder, getOrderById, getCustomerById } = require('../controllers');\n\nrouter.get('/flavors', getFlavors);\nrouter.get('/flavors/:flavorId', getFlavorById);\nrouter.post('/orders', createOrder);\nrouter.get('/orders/:orderId', getOrderById);\nrouter.get('/customers/:customerId', getCustomerById);\n\nmodule.exports = router;",
#   "prisma/schema.prisma": "generator client {\n  provider = \"prisma-client-js\"\n}\n\ndatasource db {\n  provider = \"postgresql\"\n  url      = env(\"DATABASE_URL\")\n}\n\nmodel Flavor {\n  id          String  @id @default(cuid())\n  name        String\n  description String?\n}\n\nmodel Order {\n  id         String       @id @default(cuid())\n  customerId String\n  items      OrderItem[]\n  total      Float\n}\n\nmodel OrderItem {\n  id       String @id @default(cuid())\n  orderId  String\n  flavorId String\n  quantity Int\n  order    Order   @relation(fields: [orderId], references: [id])\n  flavor   Flavor  @relation(fields: [flavorId], references: [id])\n}\n\nmodel Customer {\n  id    String @id @default(cuid())\n  name  String\n  email String @unique\n  orders Order[]\n}",
#   "docker/Dockerfile": "FROM node:16-alpine\n\nWORKDIR /app\n\nCOPY package*.json ./\n\nRUN npm install\n\nCOPY . .\n\nEXPOSE 3000\n\nCMD [\"node\", \"server.js\"]",
#   "docker/docker-compose.yml": "version: '3.8'\nservices:\n  db:\n    image: postgres:13\n    environment:\n      POSTGRES_USER: postgres\n      POSTGRES_PASSWORD: postgres\n      POSTGRES_DB: icecreamshop\n    ports:\n      - \"5432:5432\"\n  app:\n    build: .\n    ports:\n      - \"3000:3000\"\n    environment:\n      DATABASE_URL: postgres://postgres:postgres@db:5432/icecreamshop\n    depends_on:\n      - db",
#   ".env": "DATABASE_URL=postgres://postgres:postgres@db:5432/icecreamshop",
#   "server.js": "const express = require('express');\nconst app = express();\nconst routes = require('./routes');\n\napp.use(express.json());\napp.use('/api', routes);\n\nconst PORT = process.env.PORT || 3000;\napp.listen(PORT, () => {\n  console.log(`Server is running on port ${PORT}`);\n});",
#   "package.json": "{\n  \"name\": \"icecream-shop-api\",\n  \"version\": \"1.0.0\",\n  \"description\": \"API for managing an ice cream shop\",\n  \"main\": \"server.js\",\n  \"scripts\": {\n    \"start\": \"node server.js\",\n    \"dev\": \"nodemon server.js\",\n    \"prisma:generate\": \"prisma generate\",\n    \"test\": \"jest\"\n  },\n  \"dependencies\": {\n    \"@prisma/client\": \"^3.0.0\",\n    \"express\": \"^4.17.1\"\n  },\n  \"devDependencies\": {\n    \"nodemon\": \"^2.0.7\",\n    \"prisma\": \"^3.0.0\",\n    \"jest\": \"^27.0.6\",\n    \"supertest\": \"^6.1.6\"\n  }\n}",
#   "test/flavors.test.js": "const request = require('supertest');\nconst express = require('express');\nconst routes = require('../routes');\nconst app = express();\napp.use(express.json());\napp.use('/api', routes);\n\ndescribe('GET /api/flavors', () => {\n  it('should return a list of flavors', async () => {\n    const res = await request(app).get('/api/flavors');\n    expect(res.statusCode).toEqual(200);\n    expect(res.body).toBeInstanceOf(Array);\n  });\n});\n\ndescribe('GET /api/flavors/:flavorId', () => {\n  it('should return a flavor by ID', async () => {\n    const flavorId = 'existing-flavor-id';\n    const res = await request(app).get(`/api/flavors/${flavorId}`);\n    expect(res.statusCode).toEqual(200);\n    expect(res.body).toHaveProperty('id');\n  });\n\n  it('should return 404 if flavor not found', async () => {\n    const flavorId = 'non-existing-flavor-id';\n    const res = await request(app).get(`/api/flavors/${flavorId}`);\n    expect(res.statusCode).toEqual(404);\n  });\n});",
#   "test/orders.test.js": "const request = require('supertest');\nconst express = require('express');\nconst routes = require('../routes');\nconst app = express();\napp.use(express.json());\napp.use('/api', routes);\n\ndescribe('POST /api/orders', () => {\n  it('should create a new order', async () => {\n    const newOrder = {\n      customerId: 'existing-customer-id',\n      items: [\n        { flavorId: 'flavor-id-1', quantity: 2 },\n        { flavorId: 'flavor-id-2', quantity: 1 }\n      ]\n    };\n    const res = await request(app).post('/api/orders').send(newOrder);\n    expect(res.statusCode).toEqual(201);\n    expect(res.body).toHaveProperty('id');\n  });\n});\n\ndescribe('GET /api/orders/:orderId', () => {\n  it('should return an order by ID', async () => {\n    const orderId = 'existing-order-id';\n    const res = await request(app).get(`/api/orders/${orderId}`);\n    expect(res.statusCode).toEqual(200);\n    expect(res.body).toHaveProperty('id');\n  });\n\n  it('should return 404 if order not found', async () => {\n    const orderId = 'non-existing-order-id';\n    const res = await request(app).get(`/api/orders/${orderId}`);\n    expect(res.statusCode).toEqual(404);\n  });\n});",
#   "test/customers.test.js": "const request = require('supertest');\nconst express = require('express');\nconst routes = require('../routes');\nconst app = express();\napp.use(express.json());\napp.use('/api', routes);\n\ndescribe('GET /api/customers/:customerId', () => {\n  it('should return a customer by ID', async () => {\n    const customerId = 'existing-customer-id';\n    const res = await request(app).get(`/api/customers/${customerId}`);\n    expect(res.statusCode).toEqual(200);\n    expect(res.body).toHaveProperty('id');\n  });\n\n  it('should return 404 if customer not found', async () => {\n    const customerId = 'non-existing-customer-id';\n    const res = await request(app).get(`/api/customers/${customerId}`);\n    expect(res.statusCode).toEqual(404);\n  });\n});"
# }









# save_server_code("express-server", json_data)

print(directory_to_json("express-server"))


