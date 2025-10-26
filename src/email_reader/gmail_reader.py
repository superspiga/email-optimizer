"""
Lettore email tramite Gmail API
"""

import os
import base64
import logging
from datetime import datetime
from typing import List, Optional

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from bs4 import BeautifulSoup

from .base_reader import BaseEmailReader
from ..models import EmailMessage, EmailThread, EmailAccount

logger = logging.getLogger(__name__)

# Scope Gmail
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']


class GmailEmailReader(BaseEmailReader):
    """Lettore email tramite Gmail API"""

    def __init__(self, account: EmailAccount):
        super().__init__(account)
        self.service = None
        self.creds = None

    def connect(self) -> bool:
        """Connessione a Gmail API"""
        try:
            creds = None
            token_path = f"credentials/token_{self.account.email}.json"

            # Carica token esistente
            if os.path.exists(token_path):
                creds = Credentials.from_authorized_user_file(token_path, SCOPES)

            # Se non ci sono credenziali valide, fai login
            if not creds or not creds.valid:
                if creds and creds.expired and creds.refresh_token:
                    creds.refresh(Request())
                else:
                    if not self.account.credentials_file:
                        logger.error("File credenziali Gmail non specificato")
                        return False

                    flow = InstalledAppFlow.from_client_secrets_file(
                        self.account.credentials_file, SCOPES
                    )
                    creds = flow.run_local_server(port=0)

                # Salva token per usi futuri
                os.makedirs("credentials", exist_ok=True)
                with open(token_path, 'w') as token:
                    token.write(creds.to_json())

            self.creds = creds
            self.service = build('gmail', 'v1', credentials=creds)
            logger.info(f"Connesso a Gmail: {self.account.email}")
            return True

        except Exception as e:
            logger.error(f"Errore connessione Gmail: {e}")
            return False

    def disconnect(self):
        """Disconnessione da Gmail"""
        self.service = None
        self.creds = None
        logger.info(f"Disconnesso da Gmail: {self.account.email}")

    def fetch_emails(
        self,
        folder: str = "INBOX",
        limit: Optional[int] = None,
        since_date: Optional[datetime] = None,
        unread_only: bool = False
    ) -> List[EmailMessage]:
        """Recupera email da Gmail"""

        if not self.service:
            raise ConnectionError("Non connesso a Gmail API")

        emails = []

        try:
            # Costruisci query
            query_parts = [f"in:{folder}"]
            if unread_only:
                query_parts.append("is:unread")
            if since_date:
                date_str = since_date.strftime("%Y/%m/%d")
                query_parts.append(f"after:{date_str}")

            query = " ".join(query_parts)

            # Recupera lista messaggi
            results = self.service.users().messages().list(
                userId='me',
                q=query,
                maxResults=limit or 100
            ).execute()

            messages = results.get('messages', [])

            # Recupera dettagli di ogni messaggio
            for msg_ref in messages:
                try:
                    msg = self.service.users().messages().get(
                        userId='me',
                        id=msg_ref['id'],
                        format='full'
                    ).execute()

                    parsed_email = self._parse_gmail_message(msg)
                    if parsed_email:
                        emails.append(parsed_email)

                except Exception as e:
                    logger.error(f"Errore recupero messaggio {msg_ref['id']}: {e}")
                    continue

        except Exception as e:
            logger.error(f"Errore fetch Gmail: {e}")

        return emails

    def _parse_gmail_message(self, msg: dict) -> Optional[EmailMessage]:
        """Parse messaggio Gmail"""
        try:
            headers = {h['name']: h['value'] for h in msg['payload']['headers']}

            # Informazioni base
            msg_id = msg['id']
            thread_id = msg.get('threadId')
            subject = headers.get('Subject', '')
            sender = headers.get('From', '')
            to = headers.get('To', '')
            cc = headers.get('Cc', '')
            date_str = headers.get('Date', '')

            # Parse sender
            sender_email, sender_name = self._parse_email_address(sender)

            # Parse recipients
            recipients = self._parse_email_addresses(to)
            cc_list = self._parse_email_addresses(cc) if cc else []

            # Parse date
            try:
                from email.utils import parsedate_to_datetime
                date = parsedate_to_datetime(date_str) if date_str else datetime.now()
            except:
                date = datetime.now()

            # Estrai body
            body, html_body = self._extract_gmail_body(msg['payload'])

            # Thread info
            in_reply_to = headers.get('In-Reply-To')
            references = headers.get('References', '').split()

            # Labels (per determinare se letto)
            labels = msg.get('labelIds', [])
            is_read = 'UNREAD' not in labels

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
                attachments=[],  # TODO: implementa estrazione allegati
                is_read=is_read
            )

        except Exception as e:
            logger.error(f"Errore parsing Gmail message: {e}")
            return None

    def _extract_gmail_body(self, payload: dict) -> tuple[str, Optional[str]]:
        """Estrai body da payload Gmail"""
        text_body = ""
        html_body = None

        def extract_parts(parts):
            nonlocal text_body, html_body

            for part in parts:
                mime_type = part.get('mimeType')
                body = part.get('body', {})
                data = body.get('data')

                if mime_type == 'text/plain' and data:
                    text_body = base64.urlsafe_b64decode(data).decode('utf-8', errors='ignore')

                elif mime_type == 'text/html' and data:
                    html_body = base64.urlsafe_b64decode(data).decode('utf-8', errors='ignore')

                # Ricorsione per parti multipart
                if 'parts' in part:
                    extract_parts(part['parts'])

        if 'parts' in payload:
            extract_parts(payload['parts'])
        else:
            # Messaggio semplice
            body = payload.get('body', {})
            data = body.get('data')
            if data:
                content = base64.urlsafe_b64decode(data).decode('utf-8', errors='ignore')
                if payload.get('mimeType') == 'text/html':
                    html_body = content
                    soup = BeautifulSoup(content, 'html.parser')
                    text_body = soup.get_text(separator='\n', strip=True)
                else:
                    text_body = content

        return text_body, html_body

    def _parse_email_address(self, address: str) -> tuple[str, Optional[str]]:
        """Parse indirizzo email"""
        if "<" in address and ">" in address:
            name = address.split("<")[0].strip().strip('"')
            email_addr = address.split("<")[1].split(">")[0].strip()
            return email_addr, name if name else None
        return address.strip(), None

    def _parse_email_addresses(self, addresses: str) -> List[str]:
        """Parse lista indirizzi"""
        if not addresses:
            return []

        email_list = []
        for addr in addresses.split(","):
            email_addr, _ = self._parse_email_address(addr.strip())
            if email_addr:
                email_list.append(email_addr)

        return email_list

    def get_thread(self, thread_id: str) -> Optional[EmailThread]:
        """Recupera thread completo"""
        if not self.service:
            return None

        try:
            thread = self.service.users().threads().get(
                userId='me',
                id=thread_id
            ).execute()

            messages = []
            for msg in thread.get('messages', []):
                parsed = self._parse_gmail_message(msg)
                if parsed:
                    messages.append(parsed)

            if not messages:
                return None

            # Crea EmailThread
            participants = set()
            for msg in messages:
                participants.add(msg.sender)
                participants.update(msg.recipients)

            return EmailThread(
                thread_id=thread_id,
                subject=messages[0].subject,
                messages=messages,
                participants=list(participants),
                start_date=messages[0].date,
                last_date=messages[-1].date,
                message_count=len(messages)
            )

        except Exception as e:
            logger.error(f"Errore recupero thread: {e}")
            return None

    def mark_as_read(self, email_id: str) -> bool:
        """Marca come letto"""
        if not self.service:
            return False

        try:
            self.service.users().messages().modify(
                userId='me',
                id=email_id,
                body={'removeLabelIds': ['UNREAD']}
            ).execute()
            return True
        except Exception as e:
            logger.error(f"Errore mark as read: {e}")
            return False
