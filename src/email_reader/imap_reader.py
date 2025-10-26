"""
Lettore email via IMAP
"""

import email
import imaplib
from email.header import decode_header
from datetime import datetime
from typing import List, Optional
import logging
from email.utils import parsedate_to_datetime

from bs4 import BeautifulSoup

from .base_reader import BaseEmailReader
from ..models import EmailMessage, EmailThread, EmailAccount

logger = logging.getLogger(__name__)


class IMAPEmailReader(BaseEmailReader):
    """Lettore email che usa protocollo IMAP"""

    def __init__(self, account: EmailAccount):
        super().__init__(account)
        self.connection: Optional[imaplib.IMAP4_SSL] = None

    def connect(self) -> bool:
        """Connessione al server IMAP"""
        try:
            if self.account.use_ssl:
                self.connection = imaplib.IMAP4_SSL(
                    self.account.host,
                    self.account.port or 993
                )
            else:
                self.connection = imaplib.IMAP4(
                    self.account.host,
                    self.account.port or 143
                )

            self.connection.login(self.account.email, self.account.password)
            logger.info(f"Connesso a {self.account.email} via IMAP")
            return True

        except Exception as e:
            logger.error(f"Errore connessione IMAP: {e}")
            return False

    def disconnect(self):
        """Disconnessione dal server"""
        if self.connection:
            try:
                self.connection.logout()
                logger.info(f"Disconnesso da {self.account.email}")
            except:
                pass
            self.connection = None

    def fetch_emails(
        self,
        folder: str = "INBOX",
        limit: Optional[int] = None,
        since_date: Optional[datetime] = None,
        unread_only: bool = False
    ) -> List[EmailMessage]:
        """Recupera email dal server IMAP"""

        if not self.connection:
            raise ConnectionError("Non connesso al server IMAP")

        emails = []

        try:
            # Seleziona cartella
            self.connection.select(folder)

            # Costruisci criteri di ricerca
            search_criteria = []
            if unread_only:
                search_criteria.append("UNSEEN")
            if since_date:
                date_str = since_date.strftime("%d-%b-%Y")
                search_criteria.append(f'SINCE {date_str}')

            search_query = " ".join(search_criteria) if search_criteria else "ALL"

            # Cerca email
            _, message_numbers = self.connection.search(None, search_query)
            msg_nums = message_numbers[0].split()

            # Limita numero di email
            if limit:
                msg_nums = msg_nums[-limit:]

            # Recupera email
            for num in msg_nums:
                try:
                    _, msg_data = self.connection.fetch(num, "(RFC822)")
                    email_body = msg_data[0][1]
                    email_message = email.message_from_bytes(email_body)

                    parsed_email = self._parse_email_message(email_message, num.decode())
                    if parsed_email:
                        emails.append(parsed_email)

                except Exception as e:
                    logger.error(f"Errore parsing email {num}: {e}")
                    continue

        except Exception as e:
            logger.error(f"Errore recupero email: {e}")

        return emails

    def _parse_email_message(self, msg: email.message.Message, msg_id: str) -> Optional[EmailMessage]:
        """Parse di un messaggio email"""
        try:
            # Decodifica subject
            subject = self._decode_header(msg.get("Subject", ""))

            # Sender
            sender = msg.get("From", "")
            sender_email, sender_name = self._parse_email_address(sender)

            # Recipients
            to = msg.get("To", "")
            recipients = self._parse_email_addresses(to)

            # CC
            cc = msg.get("Cc", "")
            cc_list = self._parse_email_addresses(cc) if cc else []

            # Date
            date_str = msg.get("Date")
            try:
                date = parsedate_to_datetime(date_str) if date_str else datetime.now()
            except:
                date = datetime.now()

            # Body
            body, html_body = self._extract_body(msg)

            # Thread info
            thread_id = msg.get("Thread-Index") or msg.get("Message-ID")
            in_reply_to = msg.get("In-Reply-To")
            references = msg.get("References", "").split()

            # Attachments
            attachments = []
            if msg.is_multipart():
                for part in msg.walk():
                    if part.get_content_disposition() == "attachment":
                        filename = part.get_filename()
                        if filename:
                            attachments.append(self._decode_header(filename))

            return EmailMessage(
                id=msg_id,
                account_name=self.account.name,
                sender=sender_email,
                sender_name=sender_name,
                recipients=recipients,
                cc=cc_list,
                subject=subject,
                body=body,
                html_body=html_body,
                date=date,
                thread_id=thread_id,
                in_reply_to=in_reply_to,
                references=references,
                attachments=attachments,
                is_read=False
            )

        except Exception as e:
            logger.error(f"Errore parsing messaggio: {e}")
            return None

    def _decode_header(self, header: str) -> str:
        """Decodifica header email"""
        if not header:
            return ""

        decoded_parts = []
        for part, encoding in decode_header(header):
            if isinstance(part, bytes):
                decoded_parts.append(part.decode(encoding or "utf-8", errors="ignore"))
            else:
                decoded_parts.append(str(part))

        return " ".join(decoded_parts)

    def _parse_email_address(self, address: str) -> tuple[str, Optional[str]]:
        """Parse indirizzo email e nome"""
        if "<" in address and ">" in address:
            name = address.split("<")[0].strip().strip('"')
            email_addr = address.split("<")[1].split(">")[0].strip()
            return email_addr, name if name else None
        return address.strip(), None

    def _parse_email_addresses(self, addresses: str) -> List[str]:
        """Parse lista di indirizzi email"""
        if not addresses:
            return []

        email_list = []
        for addr in addresses.split(","):
            email_addr, _ = self._parse_email_address(addr.strip())
            if email_addr:
                email_list.append(email_addr)

        return email_list

    def _extract_body(self, msg: email.message.Message) -> tuple[str, Optional[str]]:
        """Estrae body testuale e HTML"""
        text_body = ""
        html_body = None

        if msg.is_multipart():
            for part in msg.walk():
                content_type = part.get_content_type()
                if content_type == "text/plain":
                    try:
                        payload = part.get_payload(decode=True)
                        charset = part.get_content_charset() or "utf-8"
                        text_body = payload.decode(charset, errors="ignore")
                    except:
                        pass

                elif content_type == "text/html":
                    try:
                        payload = part.get_payload(decode=True)
                        charset = part.get_content_charset() or "utf-8"
                        html_body = payload.decode(charset, errors="ignore")
                    except:
                        pass
        else:
            try:
                payload = msg.get_payload(decode=True)
                charset = msg.get_content_charset() or "utf-8"
                content = payload.decode(charset, errors="ignore")

                if msg.get_content_type() == "text/html":
                    html_body = content
                    # Estrai testo da HTML
                    soup = BeautifulSoup(content, "html.parser")
                    text_body = soup.get_text(separator="\n", strip=True)
                else:
                    text_body = content
            except:
                pass

        return text_body, html_body

    def get_thread(self, thread_id: str) -> Optional[EmailThread]:
        """Recupera thread email (implementazione base)"""
        # Implementazione semplificata - può essere migliorata
        # cercando tutte le email con stesso thread_id o subject
        return None

    def mark_as_read(self, email_id: str) -> bool:
        """Marca email come letta"""
        if not self.connection:
            return False

        try:
            self.connection.store(email_id, '+FLAGS', '\\Seen')
            return True
        except Exception as e:
            logger.error(f"Errore marking as read: {e}")
            return False
