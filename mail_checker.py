import dns.resolver
import smtplib
import socket
from typing import Tuple


def get_domain(email: str) -> str:
    return email.split('@')[-1]


def check_mx_records(domain: str) -> Tuple[bool, str]:
    """
    Проверяет наличие MX-записей домена.
    Возвращает (успех, сообщение статуса)
    """
    try:
        records = dns.resolver.resolve(domain, 'MX')
        mx_record = str(records[0].exchange).rstrip('.')
        return True, mx_record
    except dns.resolver.NXDOMAIN:
        return False, 'домен отсутствует'
    except (dns.resolver.NoAnswer, dns.resolver.NoNameservers):
        return False, 'MX-записи отсутствуют или некорректны'
    except Exception:
        return False, 'ошибка при проверке MX-записей'


def smtp_handshake(mx_host: str, email: str) -> str:
    """
    Выполняет SMTP-handshake без отправки письма.
    Важно: многие почтовые серверы (Gmail, Yandex, Outlook)
    не раскрывают реальное существование ящика и всегда
    отвечают 250 на RCPT TO.
    """
    try:
        server = smtplib.SMTP(timeout=10)
        server.connect(mx_host)
        server.helo('localhost')
        server.mail('test@example.com')
        code, _ = server.rcpt(email)
        server.quit()

        if code == 250:
            return 'домен валиден'
        return 'домен валиден'
    except (smtplib.SMTPException, socket.error):
        return 'домен валиден'


def verify_email(email: str) -> str:
    domain = get_domain(email)

    mx_ok, mx_result = check_mx_records(domain)
    if not mx_ok:
        return mx_result

    return smtp_handshake(mx_result, email)


if __name__ == '__main__':
    emails = [
        'test@gmail.com',
        'nonexistent@example.com',
        'murzaev48@gmail.com',
        'd.palmo1@yandex.ru'
    ]

    for email in emails:
        print(f'{email}: {verify_email(email)}')
