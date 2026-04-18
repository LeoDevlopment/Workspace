import ssl
import socket
from cryptography import x509
from cryptography.hazmat.backends import default_backend
import time
import plotly.graph_objs as go


server_int = "google.com"
server_gos = "gosuslugi.ru"
server_com = "yandex.ru"


def get_certificate_info(hostname, port=443):
    context = ssl.create_default_context()
    with socket.create_connection((hostname, port)) as sock:
        with context.wrap_socket(sock, server_hostname=hostname) as ssock:
            cert_der = ssock.getpeercert(binary_form=True)
            cert = x509.load_der_x509_certificate(cert_der, default_backend())

            print(f"\n--- Сертификат {hostname} ---")
            print(f"Домен: {hostname}")
            print(f"Издатель: {cert.issuer}")
            print(f"Алгоритм подписи: {cert.signature_algorithm_oid}")
            print(f"Срок действия: {cert.not_valid_after}")


get_certificate_info(server_int)
get_certificate_info(server_gos)
get_certificate_info(server_com)


def check_tls_version(hostname):
    context = ssl.create_default_context()
    with socket.create_connection((hostname, 443)) as sock:
        with context.wrap_socket(sock, server_hostname=hostname) as ssock:
            print(f"\n--- {hostname} ---")
            print(f"TLS-версия: {ssock.version()}")
            print(f"Выбранный алгоритм: {ssock.cipher()}")


check_tls_version(server_int)
check_tls_version(server_gos)
check_tls_version(server_com)


def measure_handshake(hostname):
    timeline = []
    for _ in range(50):
        start = time.time()
        try:
            context = ssl.create_default_context()
            with socket.create_connection((hostname, 443)) as sock:
                with context.wrap_socket(sock, server_hostname=hostname):
                    handshake_time = (time.time() - start) * 1000  # мс
                    timeline.append(handshake_time)
        except Exception as e:
            print(f"Ошибка: {e}")
    return timeline


fig = go.Figure()

fig.add_trace(go.Scatter(
    y=measure_handshake(server_int),
    name="Международный сервер"
))

fig.add_trace(go.Scatter(
    y=measure_handshake(server_gos),
    name="Государственный сервер"
))

fig.add_trace(go.Scatter(
    y=measure_handshake(server_com),
    name="Коммерческий сервер"
))

fig.update_layout(
    title="Быстродействие серверов различных отраслей",
    xaxis_title="№ попытки",
    yaxis_title="Время отклика, мс"
)


def test_deprecated_tls(hostname):
    versions = {
        "TLS 1.0": ssl.PROTOCOL_TLSv1,
        "TLS 1.1": ssl.PROTOCOL_TLSv1_1,
        "TLS 1.2": ssl.PROTOCOL_TLSv1_2,
    }

    print(f"\n--- Проверка {hostname} ---")
    for name, proto in versions.items():
        try:
            context = ssl.SSLContext(proto)
            with socket.create_connection((hostname, 443)) as sock:
                with context.wrap_socket(sock, server_hostname=hostname):
                    print(f"{name}: ✅ Поддерживается")
        except:
            print(f"{name}: ❌ Не поддерживается")


test_deprecated_tls(server_int)
test_deprecated_tls(server_gos)
test_deprecated_tls(server_com)