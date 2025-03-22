import socket, datetime, json, threading, markdown

response_header = (
    "HTTP/1.1 {state} OK\r\n"
    "Content-Type: text/html; charset=utf-8\r\n"
    "Connection: close\r\n"
    "Date: {date}\r\n"
    "Server: {server}\r\n\r\n"
)

global_settings = {}


def http_response(client_socket, response):
    client_socket.sendall(response.encode("utf-8"))
    client_socket.close()


def generate_response(request_map, global_settings):
    response = response_header

    try:
        with open(
            f"{global_settings["page_path"]}{request_map['path']}",
            "r",
            encoding="utf-8",
        ) as html_file:
            context = html_file.readlines()
            for line in context:
                line = line.lstrip().strip()
                response += line
    except FileNotFoundError:
        print(f"找不到 page{request_map['path']}")
        return response.format(
            state="404", date=datetime.datetime.now(), server=global_settings["server"]
        )
    # except KeyError:
    #     print("KeyError")
    #     return response.format(
    #         state="404", date=datetime.datetime.now(), server=global_settings["server"]
    #     )
    md_label_left = response.find("<markdown>")
    md_label_right = response.find("</markdown>")
    if md_label_left != -1 and md_label_right != -1:
        md_file_name = response[md_label_left + len("<markdown>") : md_label_right]
        with open(
            f"{global_settings['markdown_path']}/{md_file_name}.md",
            "r",
            encoding="utf-8",
        ) as md_file:
            md_context = md_file.read()
        md_html = markdown.markdown(md_context)
        response = response.replace(
            response[md_label_left : md_label_right + len("</markdown>")], md_html
        )

    return response.format(
        state="200", date=datetime.datetime.now(), server=global_settings["server"]
    )


def get_request_header(client_socket):
    request = b""
    request_map = {}
    while True:
        part = client_socket.recv(1024)
        if len(part) == 0:
            break
        request += part
        if len(part) < 1024:
            break
    request = request.decode("utf-8")
    request_data = list(filter(None, request.split("\r\n")))
    if len(request_data) == 0:
        exit()
    request_line = request_data[0].split(" ")
    request_map["method"] = request_line[0]
    request_map["path"] = request_line[1]
    request_map["version"] = request_line[2]
    for line in request_data[1:]:
        line = line.split(": ")
        request_map[line[0]] = line[1]
    if request_map["path"] == "/":
        request_map["path"] = "/index.html"
    else:
        request_map["path"] += ".html"
    return request_map


def sent_response(client_socket, client_address, global_settings):
    request_map = get_request_header(client_socket)
    response = generate_response(request_map, global_settings)
    http_response(client_socket, response)


def main():
    try:
        with open("settings.json", "r", encoding="utf-8") as settings_file:
            global_settings = json.load(settings_file)
    except FileNotFoundError:
        print("找不到 settings.json")
        exit()
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((global_settings["host"], global_settings["port"]))
    server_socket.listen(1024)
    print(f"服务器启动成功，监听 http://{global_settings['host']}:{global_settings['port']}")

    while True:
        client_socket, client_address = server_socket.accept()
        print(f"连接 {client_address}")
        threading.Thread(
            target=sent_response, args=(client_socket, client_address, global_settings)
        ).start()


if __name__ == "__main__":
    main()
