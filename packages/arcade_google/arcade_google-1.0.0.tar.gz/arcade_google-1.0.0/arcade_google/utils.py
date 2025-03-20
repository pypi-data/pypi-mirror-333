import logging
import re
from base64 import urlsafe_b64decode, urlsafe_b64encode
from datetime import datetime, timedelta
from email.message import EmailMessage
from email.mime.text import MIMEText
from enum import Enum
from typing import Any, Optional, Union, cast
from zoneinfo import ZoneInfo

from arcade.sdk import ToolContext
from bs4 import BeautifulSoup
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import Resource, build

from arcade_google.constants import DEFAULT_SEARCH_CONTACTS_LIMIT
from arcade_google.exceptions import GmailToolError, GoogleServiceError
from arcade_google.models import Corpora, Day, GmailAction, GmailReplyToWhom, OrderBy, TimeSlot

## Set up basic configuration for logging to the console with DEBUG level and a specific format.
logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)

logger = logging.getLogger(__name__)


def parse_datetime(datetime_str: str, time_zone: str) -> datetime:
    """
    Parse a datetime string in ISO 8601 format and ensure it is timezone-aware.

    Args:
        datetime_str (str): The datetime string to parse. Expected format: 'YYYY-MM-DDTHH:MM:SS'.
        time_zone (str): The timezone to apply if the datetime string is naive.

    Returns:
        datetime: A timezone-aware datetime object.

    Raises:
        ValueError: If the datetime string is not in the correct format.
    """
    try:
        dt = datetime.fromisoformat(datetime_str)
        if dt.tzinfo is None:
            dt = dt.replace(tzinfo=ZoneInfo(time_zone))
    except ValueError as e:
        raise ValueError(
            f"Invalid datetime format: '{datetime_str}'. "
            "Expected ISO 8601 format, e.g., '2024-12-31T15:30:00'."
        ) from e
    return dt


class DateRange(Enum):
    TODAY = "today"
    YESTERDAY = "yesterday"
    LAST_7_DAYS = "last_7_days"
    LAST_30_DAYS = "last_30_days"
    THIS_MONTH = "this_month"
    LAST_MONTH = "last_month"
    THIS_YEAR = "this_year"

    def to_date_query(self) -> str:
        today = datetime.now()
        result = "after:"
        comparison_date = today

        if self == DateRange.YESTERDAY:
            comparison_date = today - timedelta(days=1)
        elif self == DateRange.LAST_7_DAYS:
            comparison_date = today - timedelta(days=7)
        elif self == DateRange.LAST_30_DAYS:
            comparison_date = today - timedelta(days=30)
        elif self == DateRange.THIS_MONTH:
            comparison_date = today.replace(day=1)
        elif self == DateRange.LAST_MONTH:
            comparison_date = (today.replace(day=1) - timedelta(days=1)).replace(day=1)
        elif self == DateRange.THIS_YEAR:
            comparison_date = today.replace(month=1, day=1)
        elif self == DateRange.LAST_MONTH:
            comparison_date = (today.replace(month=1, day=1) - timedelta(days=1)).replace(
                month=1, day=1
            )

        return result + comparison_date.strftime("%Y/%m/%d")


def build_email_message(
    recipient: str,
    subject: str,
    body: str,
    cc: Optional[list[str]] = None,
    bcc: Optional[list[str]] = None,
    replying_to: Optional[dict[str, Any]] = None,
    action: GmailAction = GmailAction.SEND,
) -> dict[str, Any]:
    if replying_to:
        body = build_reply_body(body, replying_to)

    message: Union[EmailMessage, MIMEText]

    if action == GmailAction.SEND:
        message = EmailMessage()
        message.set_content(body)
    elif action == GmailAction.DRAFT:
        message = MIMEText(body)

    message["To"] = recipient
    message["Subject"] = subject

    if cc:
        message["Cc"] = ",".join(cc)
    if bcc:
        message["Bcc"] = ",".join(bcc)
    if replying_to:
        message["In-Reply-To"] = replying_to["header_message_id"]
        message["References"] = f"{replying_to['header_message_id']}, {replying_to['references']}"

    encoded_message = urlsafe_b64encode(message.as_bytes()).decode()

    data = {"raw": encoded_message}

    if replying_to:
        data["threadId"] = replying_to["thread_id"]

    return data


def build_reply_body(body: str, replying_to: dict[str, Any]) -> str:
    attribution = f"On {replying_to['date']}, {replying_to['from']} wrote:"
    lines = replying_to["plain_text_body"].split("\n")
    quoted_plain = "\n".join([f"> {line}" for line in lines])
    return f"{body}\n\n{attribution}\n\n{quoted_plain}"


def build_reply_recipients(
    replying_to: dict[str, Any], current_user_email_address: str, reply_to_whom: GmailReplyToWhom
) -> str:
    if reply_to_whom == GmailReplyToWhom.ONLY_THE_SENDER:
        recipients = [replying_to["from"]]
    elif reply_to_whom == GmailReplyToWhom.EVERY_RECIPIENT:
        recipients = [replying_to["from"], *replying_to["to"].split(",")]
    else:
        raise ValueError(f"Unsupported reply_to_whom value: {reply_to_whom}")

    recipients = [
        email_address.strip()
        for email_address in recipients
        if email_address.strip().lower() != current_user_email_address.lower().strip()
    ]

    return ", ".join(recipients)


def parse_plain_text_email(email_data: dict[str, Any]) -> dict[str, Any]:
    """
    Parse email data and extract relevant information.
    Only returns the plain text body.

    Args:
        email_data (Dict[str, Any]): Raw email data from Gmail API.

    Returns:
        Optional[Dict[str, str]]: Parsed email details or None if parsing fails.
    """
    payload = email_data.get("payload", {})
    headers = {d["name"].lower(): d["value"] for d in payload.get("headers", [])}

    body_data = _get_email_plain_text_body(payload)

    email_details = {
        "id": email_data.get("id", ""),
        "thread_id": email_data.get("threadId", ""),
        "label_ids": email_data.get("labelIds", []),
        "history_id": email_data.get("historyId", ""),
        "snippet": email_data.get("snippet", ""),
        "to": headers.get("to", ""),
        "cc": headers.get("cc", ""),
        "from": headers.get("from", ""),
        "reply_to": headers.get("reply-to", ""),
        "in_reply_to": headers.get("in-reply-to", ""),
        "references": headers.get("references", ""),
        "header_message_id": headers.get("message-id", ""),
        "date": headers.get("date", ""),
        "subject": headers.get("subject", ""),
        "body": body_data or "",
    }

    return email_details


def parse_multipart_email(email_data: dict[str, Any]) -> dict[str, Any]:
    """
    Parse email data and extract relevant information.
    Returns the plain text and HTML body along with the images.

    Args:
        email_data (Dict[str, Any]): Raw email data from Gmail API.

    Returns:
        Optional[Dict[str, Any]]: Parsed email details or None if parsing fails.
    """

    payload = email_data.get("payload", {})
    headers = {d["name"].lower(): d["value"] for d in payload.get("headers", [])}

    # Extract different parts of the email
    plain_text_body = _get_email_plain_text_body(payload)
    html_body = _get_email_html_body(payload)

    email_details = {
        "id": email_data.get("id", ""),
        "thread_id": email_data.get("threadId", ""),
        "label_ids": email_data.get("labelIds", []),
        "history_id": email_data.get("historyId", ""),
        "snippet": email_data.get("snippet", ""),
        "to": headers.get("to", ""),
        "cc": headers.get("cc", ""),
        "from": headers.get("from", ""),
        "reply_to": headers.get("reply-to", ""),
        "in_reply_to": headers.get("in-reply-to", ""),
        "references": headers.get("references", ""),
        "header_message_id": headers.get("message-id", ""),
        "date": headers.get("date", ""),
        "subject": headers.get("subject", ""),
        "plain_text_body": plain_text_body or _clean_email_body(html_body),
        "html_body": html_body or "",
    }

    return email_details


def parse_draft_email(draft_email_data: dict[str, Any]) -> dict[str, str]:
    """
    Parse draft email data and extract relevant information.

    Args:
        draft_email_data (Dict[str, Any]): Raw draft email data from Gmail API.

    Returns:
        Optional[Dict[str, str]]: Parsed draft email details or None if parsing fails.
    """
    message = draft_email_data.get("message", {})
    payload = message.get("payload", {})
    headers = {d["name"].lower(): d["value"] for d in payload.get("headers", [])}

    body_data = _get_email_plain_text_body(payload)

    return {
        "id": draft_email_data.get("id", ""),
        "thread_id": draft_email_data.get("threadId", ""),
        "from": headers.get("from", ""),
        "date": headers.get("internaldate", ""),
        "subject": headers.get("subject", ""),
        "body": _clean_email_body(body_data) if body_data else "",
    }


def get_draft_url(draft_id: str) -> str:
    return f"https://mail.google.com/mail/u/0/#drafts/{draft_id}"


def get_sent_email_url(sent_email_id: str) -> str:
    return f"https://mail.google.com/mail/u/0/#sent/{sent_email_id}"


def get_email_details(service: Any, messages: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """
    Retrieves full message data for each message ID in the given list and extracts email details.

    :param service: Authenticated Gmail API service instance.
    :param messages: A list of dictionaries, each representing a message with an 'id' key.
    :return: A list of dictionaries, each containing parsed email details.
    """

    emails = []
    for msg in messages:
        try:
            # Fetch the full message data from Gmail using the message ID
            email_data = service.users().messages().get(userId="me", id=msg["id"]).execute()
            # Parse the raw email data into a structured form
            email_details = parse_plain_text_email(email_data)
            # Only add the details if parsing was successful
            if email_details:
                emails.append(email_details)
        except Exception as e:
            # Log any errors encountered while trying to fetch or parse a message
            raise GmailToolError(
                message=f"Error reading email {msg['id']}.", developer_message=str(e)
            )
    return emails


def get_email_in_trash_url(email_id: str) -> str:
    return f"https://mail.google.com/mail/u/0/#trash/{email_id}"


def _build_gmail_service(context: ToolContext) -> Any:
    """
    Private helper function to build and return the Gmail service client.

    Args:
        context (ToolContext): The context containing authorization details.

    Returns:
        googleapiclient.discovery.Resource: An authorized Gmail API service instance.
    """
    try:
        credentials = Credentials(
            context.authorization.token
            if context.authorization and context.authorization.token
            else ""
        )
    except Exception as e:
        raise GoogleServiceError(message="Failed to build Gmail service.", developer_message=str(e))

    return build("gmail", "v1", credentials=credentials)


def _extract_plain_body(parts: list) -> Optional[str]:
    """
    Recursively extract the email body from parts, handling both plain text and HTML.

    Args:
        parts (List[Dict[str, Any]]): List of email parts.

    Returns:
        Optional[str]: Decoded and cleaned email body or None if not found.
    """
    for part in parts:
        mime_type = part.get("mimeType")

        if mime_type == "text/plain" and "data" in part.get("body", {}):
            return urlsafe_b64decode(part["body"]["data"]).decode()

        elif mime_type.startswith("multipart/"):
            subparts = part.get("parts", [])
            body = _extract_plain_body(subparts)
            if body:
                return body

    return _extract_html_body(parts)


def _extract_html_body(parts: list) -> Optional[str]:
    """
    Recursively extract the email body from parts, handling only HTML.

    Args:
        parts (List[Dict[str, Any]]): List of email parts.

    Returns:
        Optional[str]: Decoded and cleaned email body or None if not found.
    """
    for part in parts:
        mime_type = part.get("mimeType")

        if mime_type == "text/html" and "data" in part.get("body", {}):
            html_content = urlsafe_b64decode(part["body"]["data"]).decode()
            return html_content

        elif mime_type.startswith("multipart/"):
            subparts = part.get("parts", [])
            body = _extract_html_body(subparts)
            if body:
                return body

    return None


def _get_email_images(payload: dict[str, Any]) -> Optional[list[str]]:
    """
    Extract the email images from an email payload.

    Args:
        payload (Dict[str, Any]): Email payload data.

    Returns:
        Optional[List[str]]: List of decoded image contents or None if none found.
    """
    images = []
    for part in payload.get("parts", []):
        mime_type = part.get("mimeType")

        if mime_type.startswith("image/") and "data" in part.get("body", {}):
            image_content = part["body"]["data"]
            images.append(image_content)

        elif mime_type.startswith("multipart/"):
            subparts = part.get("parts", [])
            subimages = _get_email_images(subparts)
            if subimages:
                images.extend(subimages)

    if images:
        return images

    return None


def _get_email_plain_text_body(payload: dict[str, Any]) -> Optional[str]:
    """
    Extract email body from payload, handling 'multipart/alternative' parts.

    Args:
        payload (Dict[str, Any]): Email payload data.

    Returns:
        Optional[str]: Decoded email body or None if not found.
    """
    # Direct body extraction
    if "body" in payload and payload["body"].get("data"):
        return _clean_email_body(urlsafe_b64decode(payload["body"]["data"]).decode())

    # Handle multipart and alternative parts
    return _clean_email_body(_extract_plain_body(payload.get("parts", [])))


def _get_email_html_body(payload: dict[str, Any]) -> Optional[str]:
    """
    Extract email html body from payload, handling 'multipart/alternative' parts.

    Args:
        payload (Dict[str, Any]): Email payload data.

    Returns:
        Optional[str]: Decoded email body or None if not found.
    """
    # Direct body extraction
    if "body" in payload and payload["body"].get("data"):
        return urlsafe_b64decode(payload["body"]["data"]).decode()

    # Handle multipart and alternative parts
    return _extract_html_body(payload.get("parts", []))


def _clean_email_body(body: Optional[str]) -> str:
    """
    Remove HTML tags and clean up email body text while preserving most content.

    Args:
        body (str): The raw email body text.

    Returns:
        str: Cleaned email body text.
    """
    if not body:
        return ""

    try:
        # Remove HTML tags using BeautifulSoup
        soup = BeautifulSoup(body, "html.parser")
        text = soup.get_text(separator=" ")

        # Clean up the text
        cleaned_text = _clean_text(text)

        return cleaned_text.strip()
    except Exception:
        logger.exception("Error cleaning email body")
        return body


def _clean_text(text: str) -> str:
    """
    Clean up the text while preserving most content.

    Args:
        text (str): The input text.

    Returns:
        str: Cleaned text.
    """
    # Replace multiple newlines with a single newline
    text = re.sub(r"\n+", "\n", text)

    # Replace multiple spaces with a single space
    text = re.sub(r"\s+", " ", text)

    # Remove leading/trailing whitespace from each line
    text = "\n".join(line.strip() for line in text.split("\n"))

    return text


def _update_datetime(day: Day | None, time: TimeSlot | None, time_zone: str) -> dict | None:
    """
    Update the datetime for a Google Calendar event.

    Args:
        day (Day | None): The day of the event.
        time (TimeSlot | None): The time of the event.
        time_zone (str): The time zone of the event.

    Returns:
        dict | None: The updated datetime for the event.
    """
    if day and time:
        dt = datetime.combine(day.to_date(time_zone), time.to_time())
        return {"dateTime": dt.isoformat(), "timeZone": time_zone}
    return None


def build_gmail_query_string(
    sender: str | None = None,
    recipient: str | None = None,
    subject: str | None = None,
    body: str | None = None,
    date_range: DateRange | None = None,
    label: str | None = None,
) -> str:
    """Helper function to build a query string
    for Gmail list_emails_by_header and search_threads tools.
    """
    query = []
    if sender:
        query.append(f"from:{sender}")
    if recipient:
        query.append(f"to:{recipient}")
    if subject:
        query.append(f"subject:{subject}")
    if body:
        query.append(body)
    if date_range:
        query.append(date_range.to_date_query())
    if label:
        query.append(f"label:{label}")
    return " ".join(query)


def get_label_ids(service: Any, label_names: list[str]) -> dict[str, str]:
    """
    Retrieve label IDs for given label names.
    Returns a dictionary mapping label names to their IDs.

    Args:
        service: Authenticated Gmail API service instance.
        label_names: List of label names to retrieve IDs for.

    Returns:
        A dictionary mapping found label names to their corresponding IDs.
    """
    try:
        # Fetch all existing labels from Gmail
        labels = service.users().labels().list(userId="me").execute().get("labels", [])
    except Exception as e:
        raise GmailToolError(message="Failed to list labels.", developer_message=str(e)) from e

    # Create a mapping from label names to their IDs
    label_id_map = {label["name"]: label["id"] for label in labels}

    found_labels = {}
    for name in label_names:
        label_id = label_id_map.get(name)
        if label_id:
            found_labels[name] = label_id
        else:
            logger.warning(f"Label '{name}' does not exist")

    return found_labels


def fetch_messages(service: Any, query_string: str, limit: int) -> list[dict[str, Any]]:
    """
    Helper function to fetch messages from Gmail API for the list_emails_by_header tool.
    """
    response = (
        service.users()
        .messages()
        .list(userId="me", q=query_string, maxResults=limit or 100)
        .execute()
    )
    return response.get("messages", [])  # type: ignore[no-any-return]


def remove_none_values(params: dict) -> dict:
    """
    Remove None values from a dictionary.
    :param params: The dictionary to clean
    :return: A new dictionary with None values removed
    """
    return {k: v for k, v in params.items() if v is not None}


# Drive utils
def build_drive_service(auth_token: Optional[str]) -> Resource:  # type: ignore[no-any-unimported]
    """
    Build a Drive service object.
    """
    auth_token = auth_token or ""
    return build("drive", "v3", credentials=Credentials(auth_token))


def build_files_list_query(
    mime_type: str,
    document_contains: Optional[list[str]] = None,
    document_not_contains: Optional[list[str]] = None,
) -> str:
    query = [f"(mimeType = '{mime_type}' and trashed = false)"]

    if isinstance(document_contains, str):
        document_contains = [document_contains]

    if isinstance(document_not_contains, str):
        document_not_contains = [document_not_contains]

    if document_contains:
        for keyword in document_contains:
            name_contains = keyword.replace("'", "\\'")
            full_text_contains = keyword.replace("'", "\\'")
            keyword_query = (
                f"(name contains '{name_contains}' or fullText contains '{full_text_contains}')"
            )
            query.append(keyword_query)

    if document_not_contains:
        for keyword in document_not_contains:
            name_not_contains = keyword.replace("'", "\\'")
            full_text_not_contains = keyword.replace("'", "\\'")
            keyword_query = (
                f"(name not contains '{name_not_contains}' and "
                f"fullText not contains '{full_text_not_contains}')"
            )
            query.append(keyword_query)

    return " and ".join(query)


def build_files_list_params(
    mime_type: str,
    page_size: int,
    order_by: list[OrderBy],
    pagination_token: Optional[str],
    include_shared_drives: bool,
    search_only_in_shared_drive_id: Optional[str],
    include_organization_domain_documents: bool,
    document_contains: Optional[list[str]] = None,
    document_not_contains: Optional[list[str]] = None,
) -> dict[str, Any]:
    query = build_files_list_query(
        mime_type=mime_type,
        document_contains=document_contains,
        document_not_contains=document_not_contains,
    )

    params = {
        "q": query,
        "pageSize": page_size,
        "orderBy": ",".join([item.value for item in order_by]),
        "pageToken": pagination_token,
    }

    if (
        include_shared_drives
        or search_only_in_shared_drive_id
        or include_organization_domain_documents
    ):
        params["includeItemsFromAllDrives"] = "true"
        params["supportsAllDrives"] = "true"

    if search_only_in_shared_drive_id:
        params["driveId"] = search_only_in_shared_drive_id
        params["corpora"] = Corpora.DRIVE.value

    if include_organization_domain_documents:
        params["corpora"] = Corpora.DOMAIN.value

    params = remove_none_values(params)

    return params


def build_file_tree_request_params(
    order_by: Optional[list[OrderBy]],
    page_token: Optional[str],
    limit: Optional[int],
    include_shared_drives: bool,
    restrict_to_shared_drive_id: Optional[str],
    include_organization_domain_documents: bool,
) -> dict[str, Any]:
    if order_by is None:
        order_by = [OrderBy.MODIFIED_TIME_DESC]
    elif isinstance(order_by, OrderBy):
        order_by = [order_by]

    params = {
        "q": "trashed = false",
        "corpora": Corpora.USER.value,
        "pageToken": page_token,
        "fields": (
            "files(id, name, parents, mimeType, driveId, size, createdTime, modifiedTime, owners)"
        ),
        "orderBy": ",".join([item.value for item in order_by]),
    }

    if limit:
        params["pageSize"] = str(limit)

    if (
        include_shared_drives
        or restrict_to_shared_drive_id
        or include_organization_domain_documents
    ):
        params["includeItemsFromAllDrives"] = "true"
        params["supportsAllDrives"] = "true"

    if restrict_to_shared_drive_id:
        params["driveId"] = restrict_to_shared_drive_id
        params["corpora"] = Corpora.DRIVE.value

    if include_organization_domain_documents:
        params["corpora"] = Corpora.DOMAIN.value

    return params


def build_file_tree(files: dict[str, Any]) -> dict[str, Any]:
    file_tree: dict[str, Any] = {}

    for file in files.values():
        owners = file.get("owners", [])
        if owners:
            owners = [
                {"name": owner.get("displayName", ""), "email": owner.get("emailAddress", "")}
                for owner in owners
            ]
            file["owners"] = owners

        if "size" in file:
            file["size"] = {"value": int(file["size"]), "unit": "bytes"}

        # Although "parents" is a list, a file can only have one parent
        try:
            parent_id = file["parents"][0]
            del file["parents"]
        except (KeyError, IndexError):
            parent_id = None

        # Determine the file's Drive ID
        if "driveId" in file:
            drive_id = file["driveId"]
            del file["driveId"]
        # If a shared drive id is not present, the file is in "My Drive"
        else:
            drive_id = "My Drive"

        if drive_id not in file_tree:
            file_tree[drive_id] = []

        # Root files will have the Drive's id as the parent. If the parent id is not in the files
        # list, the file must be at drive's root
        if parent_id not in files:
            file_tree[drive_id].append(file)

        # Associate the file with its parent
        else:
            if "children" not in files[parent_id]:
                files[parent_id]["children"] = []
            files[parent_id]["children"].append(file)

    return file_tree


# Docs utils
def build_docs_service(auth_token: Optional[str]) -> Resource:  # type: ignore[no-any-unimported]
    """
    Build a Drive service object.
    """
    auth_token = auth_token or ""
    return build("docs", "v1", credentials=Credentials(auth_token))


# Contacts utils
def build_people_service(auth_token: Optional[str]) -> Resource:  # type: ignore[no-any-unimported]
    """
    Build a People service object.
    """
    auth_token = auth_token or ""
    return build("people", "v1", credentials=Credentials(auth_token))


def search_contacts(service: Any, query: str, limit: Optional[int]) -> list[dict[str, Any]]:
    """
    Search the user's contacts in Google Contacts.
    """
    response = (
        service.people()
        .searchContacts(
            query=query,
            pageSize=limit or DEFAULT_SEARCH_CONTACTS_LIMIT,
            readMask=",".join([
                "names",
                "nicknames",
                "emailAddresses",
                "phoneNumbers",
                "addresses",
                "organizations",
                "biographies",
                "urls",
                "userDefined",
            ]),
        )
        .execute()
    )

    return cast(list[dict[str, Any]], response.get("results", []))
