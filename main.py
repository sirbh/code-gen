import utility
import commands
import testingCommands
import datetime
import servercodefixer




if __name__ == "__main__":

























    # utility.save_server_code("express-server", json_code)

    # result = commands.run_docker_compose()
    # print(result)
    # print(datetime.datetime.now().isoformat())

    # result = commands.get_services_status()
    # print(result)
    # print(datetime.datetime.now().isoformat())

    # result = commands.get_service_logs("server", cmd_time="2024-08-05T19:57:06.349947")
    # print(result)

    # result = utility.get_service_logs("postgres")
    # print(result)

#     result = commands.curl_request("""curl -X POST http://localhost:3000/api/users -H "Content-Type: application/json" -d '{"name": "John Doe", "email": "john.doe@example.com"}'
# """)
#     print(result)

    # result = testingCommands.create_user("John Doe", "jhon@doe.com")
    # print(result)

    # result = testingCommands.get_user(1)
    # print(result)

    # print(datetime.datetime.now().isoformat())

    result = commands.run_prisma_migrate("express-server","server")
    print(result)

    # servercodefixer.fix_server_code("instructions")



  













