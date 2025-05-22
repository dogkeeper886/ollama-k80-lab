import re


def atlassian_to_markdown(text: str) -> str:
    """
    Converts Atlassian wiki-style markup to standard Markdown.
    """

    # Normalize line breaks
    text = text.replace('\\n', '\n').replace('\r\n', '\n')

    # Bold text: +*text*+ → **text**
    text = re.sub(r'\+\*(.+?)\*\+', r'**\1**', text)

    # Headings: h1. → #, h2. → ##, etc.
    text = re.sub(r'^h([1-6])\.\s+', lambda m: '#' *
                  int(m.group(1)) + ' ', text, flags=re.MULTILINE)

    # Blockquotes: > lines
    text = re.sub(r'^\s*>', '>', text, flags=re.MULTILINE)

    # Image conversion: !URL|params! → ![](URL)
    text = re.sub(r'!([^\|!]+)\|[^!]*!', r'![](\1)', text)

    # Escaped dividers to markdown horizontal rules
    text = re.sub(r'\\[-]+', '---', text)

    # Remove extra Unicode whitespace characters (e.g., non-breaking spaces)
    # note: the space before \t is a non-breaking space
    text = re.sub(r'[ \t]+', ' ', text)

    # Collapse multiple blank lines to a maximum of 2
    text = re.sub(r'\n{3,}', '\n\n', text)

    # Strip trailing spaces
    text = '\n'.join(line.rstrip() for line in text.splitlines())

    return text.strip()


def format_comments_display(comments: list) -> str:
    """
    Format a list of comments to simple markdown with display name and converted body.
    """
    output = []
    for comment in comments:
        name = comment.get("author", {}).get("displayName", "Unknown Author")
        body_raw = comment.get("body", "")
        body_md = atlassian_to_markdown(body_raw)
        output.append(f"### {name}\n\n{body_md}\n")
    return "\n---\n".join(output)


def main(jira_response: list) -> dict:
    """Formats JSON data into a Jira-style ticket string (simplified format)."""
    issue = jira_response[0]["issue"]
    jira_ticket = issue["key"]
    root_cause = atlassian_to_markdown(issue["fields"]["customfield_10205"])
    description = atlassian_to_markdown(issue["fields"]["description"])
    comments = format_comments_display(issue["fields"]["comment"]["comments"])
    summary = issue["fields"]["summary"]
    ticket = f"""
**Jira Ticket** {jira_ticket}

**Summary:*** {summary}

**Root Cause:**
{root_cause}

**Description:**

{description}

**Comment:**

{comments}
"""

    return {
        "result": ticket
    }


if __name__ == "__main__":
    sample_jira_response = [
        {
            "issue": {
                "expand": "renderedFields,names,schema,operations,editmeta,changelog,versionedRepresentations,customfield_10039.properties,customfield_10010.requestTypePractice",
                "fields": {
                    "aggregateprogress": {
                        "progress": 0,
                        "total": 0
                    },
                    "aggregatetimeestimate": None,
                    "aggregatetimeoriginalestimate": None,
                    "aggregatetimespent": None,
                    "assignee": {
                        "accountId": "712020:d33662dd-7b1d-4cbb-8905-e7c9a5cc49f6",
                        "accountType": "atlassian",
                        "active": True,
                        "avatarUrls": {
                            "16x16": "https://secure.gravatar.com/avatar/8acd7ecda9b8e9c5e20c1d791b5d8671?d=https%3A%2F%2Favatar-management--avatars.us-west-2.prod.public.atl-paas.net%2Finitials%2FWE-5.png",
                            "24x24": "https://secure.gravatar.com/avatar/8acd7ecda9b8e9c5e20c1d791b5d8671?d=https%3A%2F%2Favatar-management--avatars.us-west-2.prod.public.atl-paas.net%2Finitials%2FWE-5.png",
                            "32x32": "https://secure.gravatar.com/avatar/8acd7ecda9b8e9c5e20c1d791b5d8671?d=https%3A%2F%2Favatar-management--avatars.us-west-2.prod.public.atl-paas.net%2Finitials%2FWE-5.png",
                            "48x48": "https://secure.gravatar.com/avatar/8acd7ecda9b8e9c5e20c1d791b5d8671?d=https%3A%2F%2Favatar-management--avatars.us-west-2.prod.public.atl-paas.net%2Finitials%2FWE-5.png"
                        },
                        "displayName": "Wu, Eric",
                        "emailAddress": "eric.wu@commscope.com",
                        "self": "https://ruckus.atlassian.net/rest/api/2/user?accountId=712020%3Ad33662dd-7b1d-4cbb-8905-e7c9a5cc49f6",
                        "timeZone": "America/Los_Angeles"
                    },
                    "attachment": [
                        {
                            "author": {
                                "accountId": "712020:f85b2370-dba7-49c7-9733-7243dcd25af7",
                                "accountType": "atlassian",
                                "active": True,
                                "avatarUrls": {
                                    "16x16": "https://secure.gravatar.com/avatar/67b44b9ab907929dae90a026d9fb178e?d=https%3A%2F%2Favatar-management--avatars.us-west-2.prod.public.atl-paas.net%2Finitials%2FJP-0.png",
                                    "24x24": "https://secure.gravatar.com/avatar/67b44b9ab907929dae90a026d9fb178e?d=https%3A%2F%2Favatar-management--avatars.us-west-2.prod.public.atl-paas.net%2Finitials%2FJP-0.png",
                                    "32x32": "https://secure.gravatar.com/avatar/67b44b9ab907929dae90a026d9fb178e?d=https%3A%2F%2Favatar-management--avatars.us-west-2.prod.public.atl-paas.net%2Finitials%2FJP-0.png",
                                    "48x48": "https://secure.gravatar.com/avatar/67b44b9ab907929dae90a026d9fb178e?d=https%3A%2F%2Favatar-management--avatars.us-west-2.prod.public.atl-paas.net%2Finitials%2FJP-0.png"
                                },
                                "displayName": "Jacob, Praveen",
                                "emailAddress": "praveen.jacob@commscope.com",
                                "self": "https://ruckus.atlassian.net/rest/api/2/user?accountId=712020%3Af85b2370-dba7-49c7-9733-7243dcd25af7",
                                "timeZone": "America/Los_Angeles"
                            },
                            "content": "https://ruckus.atlassian.net/rest/api/2/attachment/content/406384",
                            "created": "2025-02-25T05:26:08.584-0800",
                            "filename": "eu.ruckus.cloud(4).har",
                            "id": "406384",
                            "mimeType": "application/octet-stream",
                            "self": "https://ruckus.atlassian.net/rest/api/2/attachment/406384",
                            "size": 864545
                        },
                        {
                            "author": {
                                "accountId": "712020:d33662dd-7b1d-4cbb-8905-e7c9a5cc49f6",
                                "accountType": "atlassian",
                                "active": True,
                                "avatarUrls": {
                                    "16x16": "https://secure.gravatar.com/avatar/8acd7ecda9b8e9c5e20c1d791b5d8671?d=https%3A%2F%2Favatar-management--avatars.us-west-2.prod.public.atl-paas.net%2Finitials%2FWE-5.png",
                                    "24x24": "https://secure.gravatar.com/avatar/8acd7ecda9b8e9c5e20c1d791b5d8671?d=https%3A%2F%2Favatar-management--avatars.us-west-2.prod.public.atl-paas.net%2Finitials%2FWE-5.png",
                                    "32x32": "https://secure.gravatar.com/avatar/8acd7ecda9b8e9c5e20c1d791b5d8671?d=https%3A%2F%2Favatar-management--avatars.us-west-2.prod.public.atl-paas.net%2Finitials%2FWE-5.png",
                                    "48x48": "https://secure.gravatar.com/avatar/8acd7ecda9b8e9c5e20c1d791b5d8671?d=https%3A%2F%2Favatar-management--avatars.us-west-2.prod.public.atl-paas.net%2Finitials%2FWE-5.png"
                                },
                                "displayName": "Wu, Eric",
                                "emailAddress": "eric.wu@commscope.com",
                                "self": "https://ruckus.atlassian.net/rest/api/2/user?accountId=712020%3Ad33662dd-7b1d-4cbb-8905-e7c9a5cc49f6",
                                "timeZone": "America/Los_Angeles"
                            },
                            "content": "https://ruckus.atlassian.net/rest/api/2/attachment/content/784574",
                            "created": "2025-03-05T10:12:05.409-0800",
                            "filename": "image-20250305-181255.png",
                            "id": "784574",
                            "mimeType": "image/png",
                            "self": "https://ruckus.atlassian.net/rest/api/2/attachment/784574",
                            "size": 21434,
                            "thumbnail": "https://ruckus.atlassian.net/rest/api/2/attachment/thumbnail/784574"
                        },
                        {
                            "author": {
                                "accountId": "712020:d33662dd-7b1d-4cbb-8905-e7c9a5cc49f6",
                                "accountType": "atlassian",
                                "active": True,
                                "avatarUrls": {
                                    "16x16": "https://secure.gravatar.com/avatar/8acd7ecda9b8e9c5e20c1d791b5d8671?d=https%3A%2F%2Favatar-management--avatars.us-west-2.prod.public.atl-paas.net%2Finitials%2FWE-5.png",
                                    "24x24": "https://secure.gravatar.com/avatar/8acd7ecda9b8e9c5e20c1d791b5d8671?d=https%3A%2F%2Favatar-management--avatars.us-west-2.prod.public.atl-paas.net%2Finitials%2FWE-5.png",
                                    "32x32": "https://secure.gravatar.com/avatar/8acd7ecda9b8e9c5e20c1d791b5d8671?d=https%3A%2F%2Favatar-management--avatars.us-west-2.prod.public.atl-paas.net%2Finitials%2FWE-5.png",
                                    "48x48": "https://secure.gravatar.com/avatar/8acd7ecda9b8e9c5e20c1d791b5d8671?d=https%3A%2F%2Favatar-management--avatars.us-west-2.prod.public.atl-paas.net%2Finitials%2FWE-5.png"
                                },
                                "displayName": "Wu, Eric",
                                "emailAddress": "eric.wu@commscope.com",
                                "self": "https://ruckus.atlassian.net/rest/api/2/user?accountId=712020%3Ad33662dd-7b1d-4cbb-8905-e7c9a5cc49f6",
                                "timeZone": "America/Los_Angeles"
                            },
                            "content": "https://ruckus.atlassian.net/rest/api/2/attachment/content/787814",
                            "created": "2025-03-10T10:17:48.441-0700",
                            "filename": "image-20250310-171841.png",
                            "id": "787814",
                            "mimeType": "image/png",
                            "self": "https://ruckus.atlassian.net/rest/api/2/attachment/787814",
                            "size": 18042,
                            "thumbnail": "https://ruckus.atlassian.net/rest/api/2/attachment/thumbnail/787814"
                        },
                        {
                            "author": {
                                "accountId": "712020:f85b2370-dba7-49c7-9733-7243dcd25af7",
                                "accountType": "atlassian",
                                "active": True,
                                "avatarUrls": {
                                    "16x16": "https://secure.gravatar.com/avatar/67b44b9ab907929dae90a026d9fb178e?d=https%3A%2F%2Favatar-management--avatars.us-west-2.prod.public.atl-paas.net%2Finitials%2FJP-0.png",
                                    "24x24": "https://secure.gravatar.com/avatar/67b44b9ab907929dae90a026d9fb178e?d=https%3A%2F%2Favatar-management--avatars.us-west-2.prod.public.atl-paas.net%2Finitials%2FJP-0.png",
                                    "32x32": "https://secure.gravatar.com/avatar/67b44b9ab907929dae90a026d9fb178e?d=https%3A%2F%2Favatar-management--avatars.us-west-2.prod.public.atl-paas.net%2Finitials%2FJP-0.png",
                                    "48x48": "https://secure.gravatar.com/avatar/67b44b9ab907929dae90a026d9fb178e?d=https%3A%2F%2Favatar-management--avatars.us-west-2.prod.public.atl-paas.net%2Finitials%2FJP-0.png"
                                },
                                "displayName": "Jacob, Praveen",
                                "emailAddress": "praveen.jacob@commscope.com",
                                "self": "https://ruckus.atlassian.net/rest/api/2/user?accountId=712020%3Af85b2370-dba7-49c7-9733-7243dcd25af7",
                                "timeZone": "America/Los_Angeles"
                            },
                            "content": "https://ruckus.atlassian.net/rest/api/2/attachment/content/822906",
                            "created": "2025-03-25T08:42:09.221-0700",
                            "filename": "image-20250325-154149.png",
                            "id": "822906",
                            "mimeType": "image/png",
                            "self": "https://ruckus.atlassian.net/rest/api/2/attachment/822906",
                            "size": 88949,
                            "thumbnail": "https://ruckus.atlassian.net/rest/api/2/attachment/thumbnail/822906"
                        },
                        {
                            "author": {
                                "accountId": "712020:d33662dd-7b1d-4cbb-8905-e7c9a5cc49f6",
                                "accountType": "atlassian",
                                "active": True,
                                "avatarUrls": {
                                    "16x16": "https://secure.gravatar.com/avatar/8acd7ecda9b8e9c5e20c1d791b5d8671?d=https%3A%2F%2Favatar-management--avatars.us-west-2.prod.public.atl-paas.net%2Finitials%2FWE-5.png",
                                    "24x24": "https://secure.gravatar.com/avatar/8acd7ecda9b8e9c5e20c1d791b5d8671?d=https%3A%2F%2Favatar-management--avatars.us-west-2.prod.public.atl-paas.net%2Finitials%2FWE-5.png",
                                    "32x32": "https://secure.gravatar.com/avatar/8acd7ecda9b8e9c5e20c1d791b5d8671?d=https%3A%2F%2Favatar-management--avatars.us-west-2.prod.public.atl-paas.net%2Finitials%2FWE-5.png",
                                    "48x48": "https://secure.gravatar.com/avatar/8acd7ecda9b8e9c5e20c1d791b5d8671?d=https%3A%2F%2Favatar-management--avatars.us-west-2.prod.public.atl-paas.net%2Finitials%2FWE-5.png"
                                },
                                "displayName": "Wu, Eric",
                                "emailAddress": "eric.wu@commscope.com",
                                "self": "https://ruckus.atlassian.net/rest/api/2/user?accountId=712020%3Ad33662dd-7b1d-4cbb-8905-e7c9a5cc49f6",
                                "timeZone": "America/Los_Angeles"
                            },
                            "content": "https://ruckus.atlassian.net/rest/api/2/attachment/content/822925",
                            "created": "2025-03-25T10:53:28.205-0700",
                            "filename": "image-20250325-175041.png",
                            "id": "822925",
                            "mimeType": "image/png",
                            "self": "https://ruckus.atlassian.net/rest/api/2/attachment/822925",
                            "size": 101221,
                            "thumbnail": "https://ruckus.atlassian.net/rest/api/2/attachment/thumbnail/822925"
                        },
                        {
                            "author": {
                                "accountId": "712020:312e8ba4-7f21-4469-a639-1a67636dcfc8",
                                "accountType": "atlassian",
                                "active": True,
                                "avatarUrls": {
                                    "16x16": "https://secure.gravatar.com/avatar/1ce2e868f1ef9aeed6740b4fc435a740?d=https%3A%2F%2Favatar-management--avatars.us-west-2.prod.public.atl-paas.net%2Finitials%2FYW-5.png",
                                    "24x24": "https://secure.gravatar.com/avatar/1ce2e868f1ef9aeed6740b4fc435a740?d=https%3A%2F%2Favatar-management--avatars.us-west-2.prod.public.atl-paas.net%2Finitials%2FYW-5.png",
                                    "32x32": "https://secure.gravatar.com/avatar/1ce2e868f1ef9aeed6740b4fc435a740?d=https%3A%2F%2Favatar-management--avatars.us-west-2.prod.public.atl-paas.net%2Finitials%2FYW-5.png",
                                    "48x48": "https://secure.gravatar.com/avatar/1ce2e868f1ef9aeed6740b4fc435a740?d=https%3A%2F%2Favatar-management--avatars.us-west-2.prod.public.atl-paas.net%2Finitials%2FYW-5.png"
                                },
                                "displayName": "Yang, William",
                                "emailAddress": "william.yang@commscope.com",
                                "self": "https://ruckus.atlassian.net/rest/api/2/user?accountId=712020%3A312e8ba4-7f21-4469-a639-1a67636dcfc8",
                                "timeZone": "America/Los_Angeles"
                            },
                            "content": "https://ruckus.atlassian.net/rest/api/2/attachment/content/824035",
                            "created": "2025-03-27T19:27:00.306-0700",
                            "filename": "image-20250328-022553.png",
                            "id": "824035",
                            "mimeType": "image/png",
                            "self": "https://ruckus.atlassian.net/rest/api/2/attachment/824035",
                            "size": 23334,
                            "thumbnail": "https://ruckus.atlassian.net/rest/api/2/attachment/thumbnail/824035"
                        },
                        {
                            "author": {
                                "accountId": "712020:d33662dd-7b1d-4cbb-8905-e7c9a5cc49f6",
                                "accountType": "atlassian",
                                "active": True,
                                "avatarUrls": {
                                    "16x16": "https://secure.gravatar.com/avatar/8acd7ecda9b8e9c5e20c1d791b5d8671?d=https%3A%2F%2Favatar-management--avatars.us-west-2.prod.public.atl-paas.net%2Finitials%2FWE-5.png",
                                    "24x24": "https://secure.gravatar.com/avatar/8acd7ecda9b8e9c5e20c1d791b5d8671?d=https%3A%2F%2Favatar-management--avatars.us-west-2.prod.public.atl-paas.net%2Finitials%2FWE-5.png",
                                    "32x32": "https://secure.gravatar.com/avatar/8acd7ecda9b8e9c5e20c1d791b5d8671?d=https%3A%2F%2Favatar-management--avatars.us-west-2.prod.public.atl-paas.net%2Finitials%2FWE-5.png",
                                    "48x48": "https://secure.gravatar.com/avatar/8acd7ecda9b8e9c5e20c1d791b5d8671?d=https%3A%2F%2Favatar-management--avatars.us-west-2.prod.public.atl-paas.net%2Finitials%2FWE-5.png"
                                },
                                "displayName": "Wu, Eric",
                                "emailAddress": "eric.wu@commscope.com",
                                "self": "https://ruckus.atlassian.net/rest/api/2/user?accountId=712020%3Ad33662dd-7b1d-4cbb-8905-e7c9a5cc49f6",
                                "timeZone": "America/Los_Angeles"
                            },
                            "content": "https://ruckus.atlassian.net/rest/api/2/attachment/content/824083",
                            "created": "2025-03-27T21:33:45.578-0700",
                            "filename": "image-20250328-041538.png",
                            "id": "824083",
                            "mimeType": "image/png",
                            "self": "https://ruckus.atlassian.net/rest/api/2/attachment/824083",
                            "size": 96881,
                            "thumbnail": "https://ruckus.atlassian.net/rest/api/2/attachment/thumbnail/824083"
                        },
                        {
                            "author": {
                                "accountId": "712020:d33662dd-7b1d-4cbb-8905-e7c9a5cc49f6",
                                "accountType": "atlassian",
                                "active": True,
                                "avatarUrls": {
                                    "16x16": "https://secure.gravatar.com/avatar/8acd7ecda9b8e9c5e20c1d791b5d8671?d=https%3A%2F%2Favatar-management--avatars.us-west-2.prod.public.atl-paas.net%2Finitials%2FWE-5.png",
                                    "24x24": "https://secure.gravatar.com/avatar/8acd7ecda9b8e9c5e20c1d791b5d8671?d=https%3A%2F%2Favatar-management--avatars.us-west-2.prod.public.atl-paas.net%2Finitials%2FWE-5.png",
                                    "32x32": "https://secure.gravatar.com/avatar/8acd7ecda9b8e9c5e20c1d791b5d8671?d=https%3A%2F%2Favatar-management--avatars.us-west-2.prod.public.atl-paas.net%2Finitials%2FWE-5.png",
                                    "48x48": "https://secure.gravatar.com/avatar/8acd7ecda9b8e9c5e20c1d791b5d8671?d=https%3A%2F%2Favatar-management--avatars.us-west-2.prod.public.atl-paas.net%2Finitials%2FWE-5.png"
                                },
                                "displayName": "Wu, Eric",
                                "emailAddress": "eric.wu@commscope.com",
                                "self": "https://ruckus.atlassian.net/rest/api/2/user?accountId=712020%3Ad33662dd-7b1d-4cbb-8905-e7c9a5cc49f6",
                                "timeZone": "America/Los_Angeles"
                            },
                            "content": "https://ruckus.atlassian.net/rest/api/2/attachment/content/824082",
                            "created": "2025-03-27T21:33:45.230-0700",
                            "filename": "image-20250328-042807.png",
                            "id": "824082",
                            "mimeType": "image/png",
                            "self": "https://ruckus.atlassian.net/rest/api/2/attachment/824082",
                            "size": 166224,
                            "thumbnail": "https://ruckus.atlassian.net/rest/api/2/attachment/thumbnail/824082"
                        },
                        {
                            "author": {
                                "accountId": "712020:d33662dd-7b1d-4cbb-8905-e7c9a5cc49f6",
                                "accountType": "atlassian",
                                "active": True,
                                "avatarUrls": {
                                    "16x16": "https://secure.gravatar.com/avatar/8acd7ecda9b8e9c5e20c1d791b5d8671?d=https%3A%2F%2Favatar-management--avatars.us-west-2.prod.public.atl-paas.net%2Finitials%2FWE-5.png",
                                    "24x24": "https://secure.gravatar.com/avatar/8acd7ecda9b8e9c5e20c1d791b5d8671?d=https%3A%2F%2Favatar-management--avatars.us-west-2.prod.public.atl-paas.net%2Finitials%2FWE-5.png",
                                    "32x32": "https://secure.gravatar.com/avatar/8acd7ecda9b8e9c5e20c1d791b5d8671?d=https%3A%2F%2Favatar-management--avatars.us-west-2.prod.public.atl-paas.net%2Finitials%2FWE-5.png",
                                    "48x48": "https://secure.gravatar.com/avatar/8acd7ecda9b8e9c5e20c1d791b5d8671?d=https%3A%2F%2Favatar-management--avatars.us-west-2.prod.public.atl-paas.net%2Finitials%2FWE-5.png"
                                },
                                "displayName": "Wu, Eric",
                                "emailAddress": "eric.wu@commscope.com",
                                "self": "https://ruckus.atlassian.net/rest/api/2/user?accountId=712020%3Ad33662dd-7b1d-4cbb-8905-e7c9a5cc49f6",
                                "timeZone": "America/Los_Angeles"
                            },
                            "content": "https://ruckus.atlassian.net/rest/api/2/attachment/content/824604",
                            "created": "2025-03-28T23:23:21.795-0700",
                            "filename": "image-20250329-062044.png",
                            "id": "824604",
                            "mimeType": "image/png",
                            "self": "https://ruckus.atlassian.net/rest/api/2/attachment/824604",
                            "size": 81028,
                            "thumbnail": "https://ruckus.atlassian.net/rest/api/2/attachment/thumbnail/824604"
                        },
                        {
                            "author": {
                                "accountId": "712020:f85b2370-dba7-49c7-9733-7243dcd25af7",
                                "accountType": "atlassian",
                                "active": True,
                                "avatarUrls": {
                                    "16x16": "https://secure.gravatar.com/avatar/67b44b9ab907929dae90a026d9fb178e?d=https%3A%2F%2Favatar-management--avatars.us-west-2.prod.public.atl-paas.net%2Finitials%2FJP-0.png",
                                    "24x24": "https://secure.gravatar.com/avatar/67b44b9ab907929dae90a026d9fb178e?d=https%3A%2F%2Favatar-management--avatars.us-west-2.prod.public.atl-paas.net%2Finitials%2FJP-0.png",
                                    "32x32": "https://secure.gravatar.com/avatar/67b44b9ab907929dae90a026d9fb178e?d=https%3A%2F%2Favatar-management--avatars.us-west-2.prod.public.atl-paas.net%2Finitials%2FJP-0.png",
                                    "48x48": "https://secure.gravatar.com/avatar/67b44b9ab907929dae90a026d9fb178e?d=https%3A%2F%2Favatar-management--avatars.us-west-2.prod.public.atl-paas.net%2Finitials%2FJP-0.png"
                                },
                                "displayName": "Jacob, Praveen",
                                "emailAddress": "praveen.jacob@commscope.com",
                                "self": "https://ruckus.atlassian.net/rest/api/2/user?accountId=712020%3Af85b2370-dba7-49c7-9733-7243dcd25af7",
                                "timeZone": "America/Los_Angeles"
                            },
                            "content": "https://ruckus.atlassian.net/rest/api/2/attachment/content/848897",
                            "created": "2025-04-07T10:58:57.852-0700",
                            "filename": "image-20250407-175339.png",
                            "id": "848897",
                            "mimeType": "image/png",
                            "self": "https://ruckus.atlassian.net/rest/api/2/attachment/848897",
                            "size": 43178,
                            "thumbnail": "https://ruckus.atlassian.net/rest/api/2/attachment/thumbnail/848897"
                        },
                        {
                            "author": {
                                "accountId": "712020:f85b2370-dba7-49c7-9733-7243dcd25af7",
                                "accountType": "atlassian",
                                "active": True,
                                "avatarUrls": {
                                    "16x16": "https://secure.gravatar.com/avatar/67b44b9ab907929dae90a026d9fb178e?d=https%3A%2F%2Favatar-management--avatars.us-west-2.prod.public.atl-paas.net%2Finitials%2FJP-0.png",
                                    "24x24": "https://secure.gravatar.com/avatar/67b44b9ab907929dae90a026d9fb178e?d=https%3A%2F%2Favatar-management--avatars.us-west-2.prod.public.atl-paas.net%2Finitials%2FJP-0.png",
                                    "32x32": "https://secure.gravatar.com/avatar/67b44b9ab907929dae90a026d9fb178e?d=https%3A%2F%2Favatar-management--avatars.us-west-2.prod.public.atl-paas.net%2Finitials%2FJP-0.png",
                                    "48x48": "https://secure.gravatar.com/avatar/67b44b9ab907929dae90a026d9fb178e?d=https%3A%2F%2Favatar-management--avatars.us-west-2.prod.public.atl-paas.net%2Finitials%2FJP-0.png"
                                },
                                "displayName": "Jacob, Praveen",
                                "emailAddress": "praveen.jacob@commscope.com",
                                "self": "https://ruckus.atlassian.net/rest/api/2/user?accountId=712020%3Af85b2370-dba7-49c7-9733-7243dcd25af7",
                                "timeZone": "America/Los_Angeles"
                            },
                            "content": "https://ruckus.atlassian.net/rest/api/2/attachment/content/848898",
                            "created": "2025-04-07T10:58:58.168-0700",
                            "filename": "image-20250407-175358.png",
                            "id": "848898",
                            "mimeType": "image/png",
                            "self": "https://ruckus.atlassian.net/rest/api/2/attachment/848898",
                            "size": 45518,
                            "thumbnail": "https://ruckus.atlassian.net/rest/api/2/attachment/thumbnail/848898"
                        },
                        {
                            "author": {
                                "accountId": "712020:f85b2370-dba7-49c7-9733-7243dcd25af7",
                                "accountType": "atlassian",
                                "active": True,
                                "avatarUrls": {
                                    "16x16": "https://secure.gravatar.com/avatar/67b44b9ab907929dae90a026d9fb178e?d=https%3A%2F%2Favatar-management--avatars.us-west-2.prod.public.atl-paas.net%2Finitials%2FJP-0.png",
                                    "24x24": "https://secure.gravatar.com/avatar/67b44b9ab907929dae90a026d9fb178e?d=https%3A%2F%2Favatar-management--avatars.us-west-2.prod.public.atl-paas.net%2Finitials%2FJP-0.png",
                                    "32x32": "https://secure.gravatar.com/avatar/67b44b9ab907929dae90a026d9fb178e?d=https%3A%2F%2Favatar-management--avatars.us-west-2.prod.public.atl-paas.net%2Finitials%2FJP-0.png",
                                    "48x48": "https://secure.gravatar.com/avatar/67b44b9ab907929dae90a026d9fb178e?d=https%3A%2F%2Favatar-management--avatars.us-west-2.prod.public.atl-paas.net%2Finitials%2FJP-0.png"
                                },
                                "displayName": "Jacob, Praveen",
                                "emailAddress": "praveen.jacob@commscope.com",
                                "self": "https://ruckus.atlassian.net/rest/api/2/user?accountId=712020%3Af85b2370-dba7-49c7-9733-7243dcd25af7",
                                "timeZone": "America/Los_Angeles"
                            },
                            "content": "https://ruckus.atlassian.net/rest/api/2/attachment/content/848900",
                            "created": "2025-04-07T10:58:58.761-0700",
                            "filename": "image-20250407-175512.png",
                            "id": "848900",
                            "mimeType": "image/png",
                            "self": "https://ruckus.atlassian.net/rest/api/2/attachment/848900",
                            "size": 43954,
                            "thumbnail": "https://ruckus.atlassian.net/rest/api/2/attachment/thumbnail/848900"
                        },
                        {
                            "author": {
                                "accountId": "712020:f85b2370-dba7-49c7-9733-7243dcd25af7",
                                "accountType": "atlassian",
                                "active": True,
                                "avatarUrls": {
                                    "16x16": "https://secure.gravatar.com/avatar/67b44b9ab907929dae90a026d9fb178e?d=https%3A%2F%2Favatar-management--avatars.us-west-2.prod.public.atl-paas.net%2Finitials%2FJP-0.png",
                                    "24x24": "https://secure.gravatar.com/avatar/67b44b9ab907929dae90a026d9fb178e?d=https%3A%2F%2Favatar-management--avatars.us-west-2.prod.public.atl-paas.net%2Finitials%2FJP-0.png",
                                    "32x32": "https://secure.gravatar.com/avatar/67b44b9ab907929dae90a026d9fb178e?d=https%3A%2F%2Favatar-management--avatars.us-west-2.prod.public.atl-paas.net%2Finitials%2FJP-0.png",
                                    "48x48": "https://secure.gravatar.com/avatar/67b44b9ab907929dae90a026d9fb178e?d=https%3A%2F%2Favatar-management--avatars.us-west-2.prod.public.atl-paas.net%2Finitials%2FJP-0.png"
                                },
                                "displayName": "Jacob, Praveen",
                                "emailAddress": "praveen.jacob@commscope.com",
                                "self": "https://ruckus.atlassian.net/rest/api/2/user?accountId=712020%3Af85b2370-dba7-49c7-9733-7243dcd25af7",
                                "timeZone": "America/Los_Angeles"
                            },
                            "content": "https://ruckus.atlassian.net/rest/api/2/attachment/content/848899",
                            "created": "2025-04-07T10:58:58.474-0700",
                            "filename": "image-20250407-175606.png",
                            "id": "848899",
                            "mimeType": "image/png",
                            "self": "https://ruckus.atlassian.net/rest/api/2/attachment/848899",
                            "size": 33611,
                            "thumbnail": "https://ruckus.atlassian.net/rest/api/2/attachment/thumbnail/848899"
                        },
                        {
                            "author": {
                                "accountId": "557058:8b59251f-4f6a-4a26-bd58-ebff9abe7972",
                                "accountType": "atlassian",
                                "active": True,
                                "avatarUrls": {
                                    "16x16": "https://avatar-management--avatars.us-west-2.prod.public.atl-paas.net/557058:8b59251f-4f6a-4a26-bd58-ebff9abe7972/a3b20eb3-6eeb-4bf6-a5c7-7747cdbea555/16",
                                    "24x24": "https://avatar-management--avatars.us-west-2.prod.public.atl-paas.net/557058:8b59251f-4f6a-4a26-bd58-ebff9abe7972/a3b20eb3-6eeb-4bf6-a5c7-7747cdbea555/24",
                                    "32x32": "https://avatar-management--avatars.us-west-2.prod.public.atl-paas.net/557058:8b59251f-4f6a-4a26-bd58-ebff9abe7972/a3b20eb3-6eeb-4bf6-a5c7-7747cdbea555/32",
                                    "48x48": "https://avatar-management--avatars.us-west-2.prod.public.atl-paas.net/557058:8b59251f-4f6a-4a26-bd58-ebff9abe7972/a3b20eb3-6eeb-4bf6-a5c7-7747cdbea555/48"
                                },
                                "displayName": "Onteddu, Rajesh",
                                "emailAddress": "rajesh.onteddu@commscope.com",
                                "self": "https://ruckus.atlassian.net/rest/api/2/user?accountId=557058%3A8b59251f-4f6a-4a26-bd58-ebff9abe7972",
                                "timeZone": "America/Los_Angeles"
                            },
                            "content": "https://ruckus.atlassian.net/rest/api/2/attachment/content/745684",
                            "created": "2025-03-01T01:21:24.883-0800",
                            "filename": "pastedImage.10.png",
                            "id": "745684",
                            "mimeType": "image/png",
                            "self": "https://ruckus.atlassian.net/rest/api/2/attachment/745684",
                            "size": 173261,
                            "thumbnail": "https://ruckus.atlassian.net/rest/api/2/attachment/thumbnail/745684"
                        },
                        {
                            "author": {
                                "accountId": "557058:8b59251f-4f6a-4a26-bd58-ebff9abe7972",
                                "accountType": "atlassian",
                                "active": True,
                                "avatarUrls": {
                                    "16x16": "https://avatar-management--avatars.us-west-2.prod.public.atl-paas.net/557058:8b59251f-4f6a-4a26-bd58-ebff9abe7972/a3b20eb3-6eeb-4bf6-a5c7-7747cdbea555/16",
                                    "24x24": "https://avatar-management--avatars.us-west-2.prod.public.atl-paas.net/557058:8b59251f-4f6a-4a26-bd58-ebff9abe7972/a3b20eb3-6eeb-4bf6-a5c7-7747cdbea555/24",
                                    "32x32": "https://avatar-management--avatars.us-west-2.prod.public.atl-paas.net/557058:8b59251f-4f6a-4a26-bd58-ebff9abe7972/a3b20eb3-6eeb-4bf6-a5c7-7747cdbea555/32",
                                    "48x48": "https://avatar-management--avatars.us-west-2.prod.public.atl-paas.net/557058:8b59251f-4f6a-4a26-bd58-ebff9abe7972/a3b20eb3-6eeb-4bf6-a5c7-7747cdbea555/48"
                                },
                                "displayName": "Onteddu, Rajesh",
                                "emailAddress": "rajesh.onteddu@commscope.com",
                                "self": "https://ruckus.atlassian.net/rest/api/2/user?accountId=557058%3A8b59251f-4f6a-4a26-bd58-ebff9abe7972",
                                "timeZone": "America/Los_Angeles"
                            },
                            "content": "https://ruckus.atlassian.net/rest/api/2/attachment/content/786079",
                            "created": "2025-03-08T09:10:43.538-0800",
                            "filename": "pastedImage.11.png",
                            "id": "786079",
                            "mimeType": "image/png",
                            "self": "https://ruckus.atlassian.net/rest/api/2/attachment/786079",
                            "size": 42835,
                            "thumbnail": "https://ruckus.atlassian.net/rest/api/2/attachment/thumbnail/786079"
                        },
                        {
                            "author": {
                                "accountId": "557058:8b59251f-4f6a-4a26-bd58-ebff9abe7972",
                                "accountType": "atlassian",
                                "active": True,
                                "avatarUrls": {
                                    "16x16": "https://avatar-management--avatars.us-west-2.prod.public.atl-paas.net/557058:8b59251f-4f6a-4a26-bd58-ebff9abe7972/a3b20eb3-6eeb-4bf6-a5c7-7747cdbea555/16",
                                    "24x24": "https://avatar-management--avatars.us-west-2.prod.public.atl-paas.net/557058:8b59251f-4f6a-4a26-bd58-ebff9abe7972/a3b20eb3-6eeb-4bf6-a5c7-7747cdbea555/24",
                                    "32x32": "https://avatar-management--avatars.us-west-2.prod.public.atl-paas.net/557058:8b59251f-4f6a-4a26-bd58-ebff9abe7972/a3b20eb3-6eeb-4bf6-a5c7-7747cdbea555/32",
                                    "48x48": "https://avatar-management--avatars.us-west-2.prod.public.atl-paas.net/557058:8b59251f-4f6a-4a26-bd58-ebff9abe7972/a3b20eb3-6eeb-4bf6-a5c7-7747cdbea555/48"
                                },
                                "displayName": "Onteddu, Rajesh",
                                "emailAddress": "rajesh.onteddu@commscope.com",
                                "self": "https://ruckus.atlassian.net/rest/api/2/user?accountId=557058%3A8b59251f-4f6a-4a26-bd58-ebff9abe7972",
                                "timeZone": "America/Los_Angeles"
                            },
                            "content": "https://ruckus.atlassian.net/rest/api/2/attachment/content/786080",
                            "created": "2025-03-08T09:10:44.420-0800",
                            "filename": "pastedImage.12.png",
                            "id": "786080",
                            "mimeType": "image/png",
                            "self": "https://ruckus.atlassian.net/rest/api/2/attachment/786080",
                            "size": 45833,
                            "thumbnail": "https://ruckus.atlassian.net/rest/api/2/attachment/thumbnail/786080"
                        },
                        {
                            "author": {
                                "accountId": "557058:8b59251f-4f6a-4a26-bd58-ebff9abe7972",
                                "accountType": "atlassian",
                                "active": True,
                                "avatarUrls": {
                                    "16x16": "https://avatar-management--avatars.us-west-2.prod.public.atl-paas.net/557058:8b59251f-4f6a-4a26-bd58-ebff9abe7972/a3b20eb3-6eeb-4bf6-a5c7-7747cdbea555/16",
                                    "24x24": "https://avatar-management--avatars.us-west-2.prod.public.atl-paas.net/557058:8b59251f-4f6a-4a26-bd58-ebff9abe7972/a3b20eb3-6eeb-4bf6-a5c7-7747cdbea555/24",
                                    "32x32": "https://avatar-management--avatars.us-west-2.prod.public.atl-paas.net/557058:8b59251f-4f6a-4a26-bd58-ebff9abe7972/a3b20eb3-6eeb-4bf6-a5c7-7747cdbea555/32",
                                    "48x48": "https://avatar-management--avatars.us-west-2.prod.public.atl-paas.net/557058:8b59251f-4f6a-4a26-bd58-ebff9abe7972/a3b20eb3-6eeb-4bf6-a5c7-7747cdbea555/48"
                                },
                                "displayName": "Onteddu, Rajesh",
                                "emailAddress": "rajesh.onteddu@commscope.com",
                                "self": "https://ruckus.atlassian.net/rest/api/2/user?accountId=557058%3A8b59251f-4f6a-4a26-bd58-ebff9abe7972",
                                "timeZone": "America/Los_Angeles"
                            },
                            "content": "https://ruckus.atlassian.net/rest/api/2/attachment/content/786081",
                            "created": "2025-03-08T09:10:45.432-0800",
                            "filename": "pastedImage.13.png",
                            "id": "786081",
                            "mimeType": "image/png",
                            "self": "https://ruckus.atlassian.net/rest/api/2/attachment/786081",
                            "size": 118412,
                            "thumbnail": "https://ruckus.atlassian.net/rest/api/2/attachment/thumbnail/786081"
                        },
                        {
                            "author": {
                                "accountId": "557058:8b59251f-4f6a-4a26-bd58-ebff9abe7972",
                                "accountType": "atlassian",
                                "active": True,
                                "avatarUrls": {
                                    "16x16": "https://avatar-management--avatars.us-west-2.prod.public.atl-paas.net/557058:8b59251f-4f6a-4a26-bd58-ebff9abe7972/a3b20eb3-6eeb-4bf6-a5c7-7747cdbea555/16",
                                    "24x24": "https://avatar-management--avatars.us-west-2.prod.public.atl-paas.net/557058:8b59251f-4f6a-4a26-bd58-ebff9abe7972/a3b20eb3-6eeb-4bf6-a5c7-7747cdbea555/24",
                                    "32x32": "https://avatar-management--avatars.us-west-2.prod.public.atl-paas.net/557058:8b59251f-4f6a-4a26-bd58-ebff9abe7972/a3b20eb3-6eeb-4bf6-a5c7-7747cdbea555/32",
                                    "48x48": "https://avatar-management--avatars.us-west-2.prod.public.atl-paas.net/557058:8b59251f-4f6a-4a26-bd58-ebff9abe7972/a3b20eb3-6eeb-4bf6-a5c7-7747cdbea555/48"
                                },
                                "displayName": "Onteddu, Rajesh",
                                "emailAddress": "rajesh.onteddu@commscope.com",
                                "self": "https://ruckus.atlassian.net/rest/api/2/user?accountId=557058%3A8b59251f-4f6a-4a26-bd58-ebff9abe7972",
                                "timeZone": "America/Los_Angeles"
                            },
                            "content": "https://ruckus.atlassian.net/rest/api/2/attachment/content/786980",
                            "created": "2025-03-08T11:13:22.878-0800",
                            "filename": "pastedImage.14.png",
                            "id": "786980",
                            "mimeType": "image/png",
                            "self": "https://ruckus.atlassian.net/rest/api/2/attachment/786980",
                            "size": 42835,
                            "thumbnail": "https://ruckus.atlassian.net/rest/api/2/attachment/thumbnail/786980"
                        },
                        {
                            "author": {
                                "accountId": "557058:8b59251f-4f6a-4a26-bd58-ebff9abe7972",
                                "accountType": "atlassian",
                                "active": True,
                                "avatarUrls": {
                                    "16x16": "https://avatar-management--avatars.us-west-2.prod.public.atl-paas.net/557058:8b59251f-4f6a-4a26-bd58-ebff9abe7972/a3b20eb3-6eeb-4bf6-a5c7-7747cdbea555/16",
                                    "24x24": "https://avatar-management--avatars.us-west-2.prod.public.atl-paas.net/557058:8b59251f-4f6a-4a26-bd58-ebff9abe7972/a3b20eb3-6eeb-4bf6-a5c7-7747cdbea555/24",
                                    "32x32": "https://avatar-management--avatars.us-west-2.prod.public.atl-paas.net/557058:8b59251f-4f6a-4a26-bd58-ebff9abe7972/a3b20eb3-6eeb-4bf6-a5c7-7747cdbea555/32",
                                    "48x48": "https://avatar-management--avatars.us-west-2.prod.public.atl-paas.net/557058:8b59251f-4f6a-4a26-bd58-ebff9abe7972/a3b20eb3-6eeb-4bf6-a5c7-7747cdbea555/48"
                                },
                                "displayName": "Onteddu, Rajesh",
                                "emailAddress": "rajesh.onteddu@commscope.com",
                                "self": "https://ruckus.atlassian.net/rest/api/2/user?accountId=557058%3A8b59251f-4f6a-4a26-bd58-ebff9abe7972",
                                "timeZone": "America/Los_Angeles"
                            },
                            "content": "https://ruckus.atlassian.net/rest/api/2/attachment/content/786981",
                            "created": "2025-03-08T11:13:23.737-0800",
                            "filename": "pastedImage.15.png",
                            "id": "786981",
                            "mimeType": "image/png",
                            "self": "https://ruckus.atlassian.net/rest/api/2/attachment/786981",
                            "size": 45833,
                            "thumbnail": "https://ruckus.atlassian.net/rest/api/2/attachment/thumbnail/786981"
                        },
                        {
                            "author": {
                                "accountId": "557058:8b59251f-4f6a-4a26-bd58-ebff9abe7972",
                                "accountType": "atlassian",
                                "active": True,
                                "avatarUrls": {
                                    "16x16": "https://avatar-management--avatars.us-west-2.prod.public.atl-paas.net/557058:8b59251f-4f6a-4a26-bd58-ebff9abe7972/a3b20eb3-6eeb-4bf6-a5c7-7747cdbea555/16",
                                    "24x24": "https://avatar-management--avatars.us-west-2.prod.public.atl-paas.net/557058:8b59251f-4f6a-4a26-bd58-ebff9abe7972/a3b20eb3-6eeb-4bf6-a5c7-7747cdbea555/24",
                                    "32x32": "https://avatar-management--avatars.us-west-2.prod.public.atl-paas.net/557058:8b59251f-4f6a-4a26-bd58-ebff9abe7972/a3b20eb3-6eeb-4bf6-a5c7-7747cdbea555/32",
                                    "48x48": "https://avatar-management--avatars.us-west-2.prod.public.atl-paas.net/557058:8b59251f-4f6a-4a26-bd58-ebff9abe7972/a3b20eb3-6eeb-4bf6-a5c7-7747cdbea555/48"
                                },
                                "displayName": "Onteddu, Rajesh",
                                "emailAddress": "rajesh.onteddu@commscope.com",
                                "self": "https://ruckus.atlassian.net/rest/api/2/user?accountId=557058%3A8b59251f-4f6a-4a26-bd58-ebff9abe7972",
                                "timeZone": "America/Los_Angeles"
                            },
                            "content": "https://ruckus.atlassian.net/rest/api/2/attachment/content/786982",
                            "created": "2025-03-08T11:13:24.754-0800",
                            "filename": "pastedImage.16.png",
                            "id": "786982",
                            "mimeType": "image/png",
                            "self": "https://ruckus.atlassian.net/rest/api/2/attachment/786982",
                            "size": 118412,
                            "thumbnail": "https://ruckus.atlassian.net/rest/api/2/attachment/thumbnail/786982"
                        },
                        {
                            "author": {
                                "accountId": "557058:8b59251f-4f6a-4a26-bd58-ebff9abe7972",
                                "accountType": "atlassian",
                                "active": True,
                                "avatarUrls": {
                                    "16x16": "https://avatar-management--avatars.us-west-2.prod.public.atl-paas.net/557058:8b59251f-4f6a-4a26-bd58-ebff9abe7972/a3b20eb3-6eeb-4bf6-a5c7-7747cdbea555/16",
                                    "24x24": "https://avatar-management--avatars.us-west-2.prod.public.atl-paas.net/557058:8b59251f-4f6a-4a26-bd58-ebff9abe7972/a3b20eb3-6eeb-4bf6-a5c7-7747cdbea555/24",
                                    "32x32": "https://avatar-management--avatars.us-west-2.prod.public.atl-paas.net/557058:8b59251f-4f6a-4a26-bd58-ebff9abe7972/a3b20eb3-6eeb-4bf6-a5c7-7747cdbea555/32",
                                    "48x48": "https://avatar-management--avatars.us-west-2.prod.public.atl-paas.net/557058:8b59251f-4f6a-4a26-bd58-ebff9abe7972/a3b20eb3-6eeb-4bf6-a5c7-7747cdbea555/48"
                                },
                                "displayName": "Onteddu, Rajesh",
                                "emailAddress": "rajesh.onteddu@commscope.com",
                                "self": "https://ruckus.atlassian.net/rest/api/2/user?accountId=557058%3A8b59251f-4f6a-4a26-bd58-ebff9abe7972",
                                "timeZone": "America/Los_Angeles"
                            },
                            "content": "https://ruckus.atlassian.net/rest/api/2/attachment/content/745676",
                            "created": "2025-03-01T01:21:16.108-0800",
                            "filename": "pastedImage.2.png",
                            "id": "745676",
                            "mimeType": "image/png",
                            "self": "https://ruckus.atlassian.net/rest/api/2/attachment/745676",
                            "size": 42835,
                            "thumbnail": "https://ruckus.atlassian.net/rest/api/2/attachment/thumbnail/745676"
                        },
                        {
                            "author": {
                                "accountId": "557058:8b59251f-4f6a-4a26-bd58-ebff9abe7972",
                                "accountType": "atlassian",
                                "active": True,
                                "avatarUrls": {
                                    "16x16": "https://avatar-management--avatars.us-west-2.prod.public.atl-paas.net/557058:8b59251f-4f6a-4a26-bd58-ebff9abe7972/a3b20eb3-6eeb-4bf6-a5c7-7747cdbea555/16",
                                    "24x24": "https://avatar-management--avatars.us-west-2.prod.public.atl-paas.net/557058:8b59251f-4f6a-4a26-bd58-ebff9abe7972/a3b20eb3-6eeb-4bf6-a5c7-7747cdbea555/24",
                                    "32x32": "https://avatar-management--avatars.us-west-2.prod.public.atl-paas.net/557058:8b59251f-4f6a-4a26-bd58-ebff9abe7972/a3b20eb3-6eeb-4bf6-a5c7-7747cdbea555/32",
                                    "48x48": "https://avatar-management--avatars.us-west-2.prod.public.atl-paas.net/557058:8b59251f-4f6a-4a26-bd58-ebff9abe7972/a3b20eb3-6eeb-4bf6-a5c7-7747cdbea555/48"
                                },
                                "displayName": "Onteddu, Rajesh",
                                "emailAddress": "rajesh.onteddu@commscope.com",
                                "self": "https://ruckus.atlassian.net/rest/api/2/user?accountId=557058%3A8b59251f-4f6a-4a26-bd58-ebff9abe7972",
                                "timeZone": "America/Los_Angeles"
                            },
                            "content": "https://ruckus.atlassian.net/rest/api/2/attachment/content/745677",
                            "created": "2025-03-01T01:21:16.916-0800",
                            "filename": "pastedImage.3.png",
                            "id": "745677",
                            "mimeType": "image/png",
                            "self": "https://ruckus.atlassian.net/rest/api/2/attachment/745677",
                            "size": 45833,
                            "thumbnail": "https://ruckus.atlassian.net/rest/api/2/attachment/thumbnail/745677"
                        },
                        {
                            "author": {
                                "accountId": "557058:8b59251f-4f6a-4a26-bd58-ebff9abe7972",
                                "accountType": "atlassian",
                                "active": True,
                                "avatarUrls": {
                                    "16x16": "https://avatar-management--avatars.us-west-2.prod.public.atl-paas.net/557058:8b59251f-4f6a-4a26-bd58-ebff9abe7972/a3b20eb3-6eeb-4bf6-a5c7-7747cdbea555/16",
                                    "24x24": "https://avatar-management--avatars.us-west-2.prod.public.atl-paas.net/557058:8b59251f-4f6a-4a26-bd58-ebff9abe7972/a3b20eb3-6eeb-4bf6-a5c7-7747cdbea555/24",
                                    "32x32": "https://avatar-management--avatars.us-west-2.prod.public.atl-paas.net/557058:8b59251f-4f6a-4a26-bd58-ebff9abe7972/a3b20eb3-6eeb-4bf6-a5c7-7747cdbea555/32",
                                    "48x48": "https://avatar-management--avatars.us-west-2.prod.public.atl-paas.net/557058:8b59251f-4f6a-4a26-bd58-ebff9abe7972/a3b20eb3-6eeb-4bf6-a5c7-7747cdbea555/48"
                                },
                                "displayName": "Onteddu, Rajesh",
                                "emailAddress": "rajesh.onteddu@commscope.com",
                                "self": "https://ruckus.atlassian.net/rest/api/2/user?accountId=557058%3A8b59251f-4f6a-4a26-bd58-ebff9abe7972",
                                "timeZone": "America/Los_Angeles"
                            },
                            "content": "https://ruckus.atlassian.net/rest/api/2/attachment/content/745678",
                            "created": "2025-03-01T01:21:17.835-0800",
                            "filename": "pastedImage.4.png",
                            "id": "745678",
                            "mimeType": "image/png",
                            "self": "https://ruckus.atlassian.net/rest/api/2/attachment/745678",
                            "size": 118412,
                            "thumbnail": "https://ruckus.atlassian.net/rest/api/2/attachment/thumbnail/745678"
                        },
                        {
                            "author": {
                                "accountId": "557058:8b59251f-4f6a-4a26-bd58-ebff9abe7972",
                                "accountType": "atlassian",
                                "active": True,
                                "avatarUrls": {
                                    "16x16": "https://avatar-management--avatars.us-west-2.prod.public.atl-paas.net/557058:8b59251f-4f6a-4a26-bd58-ebff9abe7972/a3b20eb3-6eeb-4bf6-a5c7-7747cdbea555/16",
                                    "24x24": "https://avatar-management--avatars.us-west-2.prod.public.atl-paas.net/557058:8b59251f-4f6a-4a26-bd58-ebff9abe7972/a3b20eb3-6eeb-4bf6-a5c7-7747cdbea555/24",
                                    "32x32": "https://avatar-management--avatars.us-west-2.prod.public.atl-paas.net/557058:8b59251f-4f6a-4a26-bd58-ebff9abe7972/a3b20eb3-6eeb-4bf6-a5c7-7747cdbea555/32",
                                    "48x48": "https://avatar-management--avatars.us-west-2.prod.public.atl-paas.net/557058:8b59251f-4f6a-4a26-bd58-ebff9abe7972/a3b20eb3-6eeb-4bf6-a5c7-7747cdbea555/48"
                                },
                                "displayName": "Onteddu, Rajesh",
                                "emailAddress": "rajesh.onteddu@commscope.com",
                                "self": "https://ruckus.atlassian.net/rest/api/2/user?accountId=557058%3A8b59251f-4f6a-4a26-bd58-ebff9abe7972",
                                "timeZone": "America/Los_Angeles"
                            },
                            "content": "https://ruckus.atlassian.net/rest/api/2/attachment/content/745679",
                            "created": "2025-03-01T01:21:19.782-0800",
                            "filename": "pastedImage.5.png",
                            "id": "745679",
                            "mimeType": "image/png",
                            "self": "https://ruckus.atlassian.net/rest/api/2/attachment/745679",
                            "size": 114450,
                            "thumbnail": "https://ruckus.atlassian.net/rest/api/2/attachment/thumbnail/745679"
                        },
                        {
                            "author": {
                                "accountId": "557058:8b59251f-4f6a-4a26-bd58-ebff9abe7972",
                                "accountType": "atlassian",
                                "active": True,
                                "avatarUrls": {
                                    "16x16": "https://avatar-management--avatars.us-west-2.prod.public.atl-paas.net/557058:8b59251f-4f6a-4a26-bd58-ebff9abe7972/a3b20eb3-6eeb-4bf6-a5c7-7747cdbea555/16",
                                    "24x24": "https://avatar-management--avatars.us-west-2.prod.public.atl-paas.net/557058:8b59251f-4f6a-4a26-bd58-ebff9abe7972/a3b20eb3-6eeb-4bf6-a5c7-7747cdbea555/24",
                                    "32x32": "https://avatar-management--avatars.us-west-2.prod.public.atl-paas.net/557058:8b59251f-4f6a-4a26-bd58-ebff9abe7972/a3b20eb3-6eeb-4bf6-a5c7-7747cdbea555/32",
                                    "48x48": "https://avatar-management--avatars.us-west-2.prod.public.atl-paas.net/557058:8b59251f-4f6a-4a26-bd58-ebff9abe7972/a3b20eb3-6eeb-4bf6-a5c7-7747cdbea555/48"
                                },
                                "displayName": "Onteddu, Rajesh",
                                "emailAddress": "rajesh.onteddu@commscope.com",
                                "self": "https://ruckus.atlassian.net/rest/api/2/user?accountId=557058%3A8b59251f-4f6a-4a26-bd58-ebff9abe7972",
                                "timeZone": "America/Los_Angeles"
                            },
                            "content": "https://ruckus.atlassian.net/rest/api/2/attachment/content/745680",
                            "created": "2025-03-01T01:21:20.660-0800",
                            "filename": "pastedImage.6.png",
                            "id": "745680",
                            "mimeType": "image/png",
                            "self": "https://ruckus.atlassian.net/rest/api/2/attachment/745680",
                            "size": 102307,
                            "thumbnail": "https://ruckus.atlassian.net/rest/api/2/attachment/thumbnail/745680"
                        },
                        {
                            "author": {
                                "accountId": "557058:8b59251f-4f6a-4a26-bd58-ebff9abe7972",
                                "accountType": "atlassian",
                                "active": True,
                                "avatarUrls": {
                                    "16x16": "https://avatar-management--avatars.us-west-2.prod.public.atl-paas.net/557058:8b59251f-4f6a-4a26-bd58-ebff9abe7972/a3b20eb3-6eeb-4bf6-a5c7-7747cdbea555/16",
                                    "24x24": "https://avatar-management--avatars.us-west-2.prod.public.atl-paas.net/557058:8b59251f-4f6a-4a26-bd58-ebff9abe7972/a3b20eb3-6eeb-4bf6-a5c7-7747cdbea555/24",
                                    "32x32": "https://avatar-management--avatars.us-west-2.prod.public.atl-paas.net/557058:8b59251f-4f6a-4a26-bd58-ebff9abe7972/a3b20eb3-6eeb-4bf6-a5c7-7747cdbea555/32",
                                    "48x48": "https://avatar-management--avatars.us-west-2.prod.public.atl-paas.net/557058:8b59251f-4f6a-4a26-bd58-ebff9abe7972/a3b20eb3-6eeb-4bf6-a5c7-7747cdbea555/48"
                                },
                                "displayName": "Onteddu, Rajesh",
                                "emailAddress": "rajesh.onteddu@commscope.com",
                                "self": "https://ruckus.atlassian.net/rest/api/2/user?accountId=557058%3A8b59251f-4f6a-4a26-bd58-ebff9abe7972",
                                "timeZone": "America/Los_Angeles"
                            },
                            "content": "https://ruckus.atlassian.net/rest/api/2/attachment/content/745681",
                            "created": "2025-03-01T01:21:22.232-0800",
                            "filename": "pastedImage.7.png",
                            "id": "745681",
                            "mimeType": "image/png",
                            "self": "https://ruckus.atlassian.net/rest/api/2/attachment/745681",
                            "size": 154673,
                            "thumbnail": "https://ruckus.atlassian.net/rest/api/2/attachment/thumbnail/745681"
                        },
                        {
                            "author": {
                                "accountId": "557058:8b59251f-4f6a-4a26-bd58-ebff9abe7972",
                                "accountType": "atlassian",
                                "active": True,
                                "avatarUrls": {
                                    "16x16": "https://avatar-management--avatars.us-west-2.prod.public.atl-paas.net/557058:8b59251f-4f6a-4a26-bd58-ebff9abe7972/a3b20eb3-6eeb-4bf6-a5c7-7747cdbea555/16",
                                    "24x24": "https://avatar-management--avatars.us-west-2.prod.public.atl-paas.net/557058:8b59251f-4f6a-4a26-bd58-ebff9abe7972/a3b20eb3-6eeb-4bf6-a5c7-7747cdbea555/24",
                                    "32x32": "https://avatar-management--avatars.us-west-2.prod.public.atl-paas.net/557058:8b59251f-4f6a-4a26-bd58-ebff9abe7972/a3b20eb3-6eeb-4bf6-a5c7-7747cdbea555/32",
                                    "48x48": "https://avatar-management--avatars.us-west-2.prod.public.atl-paas.net/557058:8b59251f-4f6a-4a26-bd58-ebff9abe7972/a3b20eb3-6eeb-4bf6-a5c7-7747cdbea555/48"
                                },
                                "displayName": "Onteddu, Rajesh",
                                "emailAddress": "rajesh.onteddu@commscope.com",
                                "self": "https://ruckus.atlassian.net/rest/api/2/user?accountId=557058%3A8b59251f-4f6a-4a26-bd58-ebff9abe7972",
                                "timeZone": "America/Los_Angeles"
                            },
                            "content": "https://ruckus.atlassian.net/rest/api/2/attachment/content/745682",
                            "created": "2025-03-01T01:21:23.142-0800",
                            "filename": "pastedImage.8.png",
                            "id": "745682",
                            "mimeType": "image/png",
                            "self": "https://ruckus.atlassian.net/rest/api/2/attachment/745682",
                            "size": 116703,
                            "thumbnail": "https://ruckus.atlassian.net/rest/api/2/attachment/thumbnail/745682"
                        },
                        {
                            "author": {
                                "accountId": "557058:8b59251f-4f6a-4a26-bd58-ebff9abe7972",
                                "accountType": "atlassian",
                                "active": True,
                                "avatarUrls": {
                                    "16x16": "https://avatar-management--avatars.us-west-2.prod.public.atl-paas.net/557058:8b59251f-4f6a-4a26-bd58-ebff9abe7972/a3b20eb3-6eeb-4bf6-a5c7-7747cdbea555/16",
                                    "24x24": "https://avatar-management--avatars.us-west-2.prod.public.atl-paas.net/557058:8b59251f-4f6a-4a26-bd58-ebff9abe7972/a3b20eb3-6eeb-4bf6-a5c7-7747cdbea555/24",
                                    "32x32": "https://avatar-management--avatars.us-west-2.prod.public.atl-paas.net/557058:8b59251f-4f6a-4a26-bd58-ebff9abe7972/a3b20eb3-6eeb-4bf6-a5c7-7747cdbea555/32",
                                    "48x48": "https://avatar-management--avatars.us-west-2.prod.public.atl-paas.net/557058:8b59251f-4f6a-4a26-bd58-ebff9abe7972/a3b20eb3-6eeb-4bf6-a5c7-7747cdbea555/48"
                                },
                                "displayName": "Onteddu, Rajesh",
                                "emailAddress": "rajesh.onteddu@commscope.com",
                                "self": "https://ruckus.atlassian.net/rest/api/2/user?accountId=557058%3A8b59251f-4f6a-4a26-bd58-ebff9abe7972",
                                "timeZone": "America/Los_Angeles"
                            },
                            "content": "https://ruckus.atlassian.net/rest/api/2/attachment/content/745683",
                            "created": "2025-03-01T01:21:23.972-0800",
                            "filename": "pastedImage.9.png",
                            "id": "745683",
                            "mimeType": "image/png",
                            "self": "https://ruckus.atlassian.net/rest/api/2/attachment/745683",
                            "size": 103191,
                            "thumbnail": "https://ruckus.atlassian.net/rest/api/2/attachment/thumbnail/745683"
                        },
                        {
                            "author": {
                                "accountId": "557058:8b59251f-4f6a-4a26-bd58-ebff9abe7972",
                                "accountType": "atlassian",
                                "active": True,
                                "avatarUrls": {
                                    "16x16": "https://avatar-management--avatars.us-west-2.prod.public.atl-paas.net/557058:8b59251f-4f6a-4a26-bd58-ebff9abe7972/a3b20eb3-6eeb-4bf6-a5c7-7747cdbea555/16",
                                    "24x24": "https://avatar-management--avatars.us-west-2.prod.public.atl-paas.net/557058:8b59251f-4f6a-4a26-bd58-ebff9abe7972/a3b20eb3-6eeb-4bf6-a5c7-7747cdbea555/24",
                                    "32x32": "https://avatar-management--avatars.us-west-2.prod.public.atl-paas.net/557058:8b59251f-4f6a-4a26-bd58-ebff9abe7972/a3b20eb3-6eeb-4bf6-a5c7-7747cdbea555/32",
                                    "48x48": "https://avatar-management--avatars.us-west-2.prod.public.atl-paas.net/557058:8b59251f-4f6a-4a26-bd58-ebff9abe7972/a3b20eb3-6eeb-4bf6-a5c7-7747cdbea555/48"
                                },
                                "displayName": "Onteddu, Rajesh",
                                "emailAddress": "rajesh.onteddu@commscope.com",
                                "self": "https://ruckus.atlassian.net/rest/api/2/user?accountId=557058%3A8b59251f-4f6a-4a26-bd58-ebff9abe7972",
                                "timeZone": "America/Los_Angeles"
                            },
                            "content": "https://ruckus.atlassian.net/rest/api/2/attachment/content/745675",
                            "created": "2025-03-01T01:21:15.402-0800",
                            "filename": "pastedImage.png",
                            "id": "745675",
                            "mimeType": "image/png",
                            "self": "https://ruckus.atlassian.net/rest/api/2/attachment/745675",
                            "size": 70140,
                            "thumbnail": "https://ruckus.atlassian.net/rest/api/2/attachment/thumbnail/745675"
                        },
                        {
                            "author": {
                                "accountId": "712020:f85b2370-dba7-49c7-9733-7243dcd25af7",
                                "accountType": "atlassian",
                                "active": True,
                                "avatarUrls": {
                                    "16x16": "https://secure.gravatar.com/avatar/67b44b9ab907929dae90a026d9fb178e?d=https%3A%2F%2Favatar-management--avatars.us-west-2.prod.public.atl-paas.net%2Finitials%2FJP-0.png",
                                    "24x24": "https://secure.gravatar.com/avatar/67b44b9ab907929dae90a026d9fb178e?d=https%3A%2F%2Favatar-management--avatars.us-west-2.prod.public.atl-paas.net%2Finitials%2FJP-0.png",
                                    "32x32": "https://secure.gravatar.com/avatar/67b44b9ab907929dae90a026d9fb178e?d=https%3A%2F%2Favatar-management--avatars.us-west-2.prod.public.atl-paas.net%2Finitials%2FJP-0.png",
                                    "48x48": "https://secure.gravatar.com/avatar/67b44b9ab907929dae90a026d9fb178e?d=https%3A%2F%2Favatar-management--avatars.us-west-2.prod.public.atl-paas.net%2Finitials%2FJP-0.png"
                                },
                                "displayName": "Jacob, Praveen",
                                "emailAddress": "praveen.jacob@commscope.com",
                                "self": "https://ruckus.atlassian.net/rest/api/2/user?accountId=712020%3Af85b2370-dba7-49c7-9733-7243dcd25af7",
                                "timeZone": "America/Los_Angeles"
                            },
                            "content": "https://ruckus.atlassian.net/rest/api/2/attachment/content/848901",
                            "created": "2025-04-07T10:59:46.975-0700",
                            "filename": "SupportLog_182322021244_07042025-2037.log.gz",
                            "id": "848901",
                            "mimeType": "application/x-gzip",
                            "self": "https://ruckus.atlassian.net/rest/api/2/attachment/848901",
                            "size": 190954
                        },
                        {
                            "author": {
                                "accountId": "712020:f85b2370-dba7-49c7-9733-7243dcd25af7",
                                "accountType": "atlassian",
                                "active": True,
                                "avatarUrls": {
                                    "16x16": "https://secure.gravatar.com/avatar/67b44b9ab907929dae90a026d9fb178e?d=https%3A%2F%2Favatar-management--avatars.us-west-2.prod.public.atl-paas.net%2Finitials%2FJP-0.png",
                                    "24x24": "https://secure.gravatar.com/avatar/67b44b9ab907929dae90a026d9fb178e?d=https%3A%2F%2Favatar-management--avatars.us-west-2.prod.public.atl-paas.net%2Finitials%2FJP-0.png",
                                    "32x32": "https://secure.gravatar.com/avatar/67b44b9ab907929dae90a026d9fb178e?d=https%3A%2F%2Favatar-management--avatars.us-west-2.prod.public.atl-paas.net%2Finitials%2FJP-0.png",
                                    "48x48": "https://secure.gravatar.com/avatar/67b44b9ab907929dae90a026d9fb178e?d=https%3A%2F%2Favatar-management--avatars.us-west-2.prod.public.atl-paas.net%2Finitials%2FJP-0.png"
                                },
                                "displayName": "Jacob, Praveen",
                                "emailAddress": "praveen.jacob@commscope.com",
                                "self": "https://ruckus.atlassian.net/rest/api/2/user?accountId=712020%3Af85b2370-dba7-49c7-9733-7243dcd25af7",
                                "timeZone": "America/Los_Angeles"
                            },
                            "content": "https://ruckus.atlassian.net/rest/api/2/attachment/content/848903",
                            "created": "2025-04-07T10:59:47.289-0700",
                            "filename": "SupportLog_182322021244_07042025-2305.log.gz",
                            "id": "848903",
                            "mimeType": "application/x-gzip",
                            "self": "https://ruckus.atlassian.net/rest/api/2/attachment/848903",
                            "size": 196697
                        },
                        {
                            "author": {
                                "accountId": "712020:f85b2370-dba7-49c7-9733-7243dcd25af7",
                                "accountType": "atlassian",
                                "active": True,
                                "avatarUrls": {
                                    "16x16": "https://secure.gravatar.com/avatar/67b44b9ab907929dae90a026d9fb178e?d=https%3A%2F%2Favatar-management--avatars.us-west-2.prod.public.atl-paas.net%2Finitials%2FJP-0.png",
                                    "24x24": "https://secure.gravatar.com/avatar/67b44b9ab907929dae90a026d9fb178e?d=https%3A%2F%2Favatar-management--avatars.us-west-2.prod.public.atl-paas.net%2Finitials%2FJP-0.png",
                                    "32x32": "https://secure.gravatar.com/avatar/67b44b9ab907929dae90a026d9fb178e?d=https%3A%2F%2Favatar-management--avatars.us-west-2.prod.public.atl-paas.net%2Finitials%2FJP-0.png",
                                    "48x48": "https://secure.gravatar.com/avatar/67b44b9ab907929dae90a026d9fb178e?d=https%3A%2F%2Favatar-management--avatars.us-west-2.prod.public.atl-paas.net%2Finitials%2FJP-0.png"
                                },
                                "displayName": "Jacob, Praveen",
                                "emailAddress": "praveen.jacob@commscope.com",
                                "self": "https://ruckus.atlassian.net/rest/api/2/user?accountId=712020%3Af85b2370-dba7-49c7-9733-7243dcd25af7",
                                "timeZone": "America/Los_Angeles"
                            },
                            "content": "https://ruckus.atlassian.net/rest/api/2/attachment/content/848902",
                            "created": "2025-04-07T10:59:47.111-0700",
                            "filename": "SupportLog_182322021244_07042025-2329.log.gz",
                            "id": "848902",
                            "mimeType": "application/x-gzip",
                            "self": "https://ruckus.atlassian.net/rest/api/2/attachment/848902",
                            "size": 207279
                        },
                        {
                            "author": {
                                "accountId": "712020:d33662dd-7b1d-4cbb-8905-e7c9a5cc49f6",
                                "accountType": "atlassian",
                                "active": True,
                                "avatarUrls": {
                                    "16x16": "https://secure.gravatar.com/avatar/8acd7ecda9b8e9c5e20c1d791b5d8671?d=https%3A%2F%2Favatar-management--avatars.us-west-2.prod.public.atl-paas.net%2Finitials%2FWE-5.png",
                                    "24x24": "https://secure.gravatar.com/avatar/8acd7ecda9b8e9c5e20c1d791b5d8671?d=https%3A%2F%2Favatar-management--avatars.us-west-2.prod.public.atl-paas.net%2Finitials%2FWE-5.png",
                                    "32x32": "https://secure.gravatar.com/avatar/8acd7ecda9b8e9c5e20c1d791b5d8671?d=https%3A%2F%2Favatar-management--avatars.us-west-2.prod.public.atl-paas.net%2Finitials%2FWE-5.png",
                                    "48x48": "https://secure.gravatar.com/avatar/8acd7ecda9b8e9c5e20c1d791b5d8671?d=https%3A%2F%2Favatar-management--avatars.us-west-2.prod.public.atl-paas.net%2Finitials%2FWE-5.png"
                                },
                                "displayName": "Wu, Eric",
                                "emailAddress": "eric.wu@commscope.com",
                                "self": "https://ruckus.atlassian.net/rest/api/2/user?accountId=712020%3Ad33662dd-7b1d-4cbb-8905-e7c9a5cc49f6",
                                "timeZone": "America/Los_Angeles"
                            },
                            "content": "https://ruckus.atlassian.net/rest/api/2/attachment/content/824084",
                            "created": "2025-03-27T21:33:46.003-0700",
                            "filename": "SupportLog_202339001014_27032025-2123.log",
                            "id": "824084",
                            "mimeType": "text/plain",
                            "self": "https://ruckus.atlassian.net/rest/api/2/attachment/824084",
                            "size": 3928677
                        },
                        {
                            "author": {
                                "accountId": "712020:f85b2370-dba7-49c7-9733-7243dcd25af7",
                                "accountType": "atlassian",
                                "active": True,
                                "avatarUrls": {
                                    "16x16": "https://secure.gravatar.com/avatar/67b44b9ab907929dae90a026d9fb178e?d=https%3A%2F%2Favatar-management--avatars.us-west-2.prod.public.atl-paas.net%2Finitials%2FJP-0.png",
                                    "24x24": "https://secure.gravatar.com/avatar/67b44b9ab907929dae90a026d9fb178e?d=https%3A%2F%2Favatar-management--avatars.us-west-2.prod.public.atl-paas.net%2Finitials%2FJP-0.png",
                                    "32x32": "https://secure.gravatar.com/avatar/67b44b9ab907929dae90a026d9fb178e?d=https%3A%2F%2Favatar-management--avatars.us-west-2.prod.public.atl-paas.net%2Finitials%2FJP-0.png",
                                    "48x48": "https://secure.gravatar.com/avatar/67b44b9ab907929dae90a026d9fb178e?d=https%3A%2F%2Favatar-management--avatars.us-west-2.prod.public.atl-paas.net%2Finitials%2FJP-0.png"
                                },
                                "displayName": "Jacob, Praveen",
                                "emailAddress": "praveen.jacob@commscope.com",
                                "self": "https://ruckus.atlassian.net/rest/api/2/user?accountId=712020%3Af85b2370-dba7-49c7-9733-7243dcd25af7",
                                "timeZone": "America/Los_Angeles"
                            },
                            "content": "https://ruckus.atlassian.net/rest/api/2/attachment/content/406382",
                            "created": "2025-02-25T05:26:10.411-0800",
                            "filename": "SupportLog_202339001035_13022025-1533.log",
                            "id": "406382",
                            "mimeType": "text/plain",
                            "self": "https://ruckus.atlassian.net/rest/api/2/attachment/406382",
                            "size": 4977527
                        }
                    ],
                    "comment": {
                        "comments": [
                            {
                                "author": {
                                    "accountId": "619622c7c75da8007242597b",
                                    "accountType": "atlassian",
                                    "active": True,
                                    "avatarUrls": {
                                        "16x16": "https://secure.gravatar.com/avatar/74a18c12c068ed24ef9736848d97f100?d=https%3A%2F%2Favatar-management--avatars.us-west-2.prod.public.atl-paas.net%2Finitials%2FTN-2.png",
                                        "24x24": "https://secure.gravatar.com/avatar/74a18c12c068ed24ef9736848d97f100?d=https%3A%2F%2Favatar-management--avatars.us-west-2.prod.public.atl-paas.net%2Finitials%2FTN-2.png",
                                        "32x32": "https://secure.gravatar.com/avatar/74a18c12c068ed24ef9736848d97f100?d=https%3A%2F%2Favatar-management--avatars.us-west-2.prod.public.atl-paas.net%2Finitials%2FTN-2.png",
                                        "48x48": "https://secure.gravatar.com/avatar/74a18c12c068ed24ef9736848d97f100?d=https%3A%2F%2Favatar-management--avatars.us-west-2.prod.public.atl-paas.net%2Finitials%2FTN-2.png"
                                    },
                                    "displayName": "Thakur, Navraj",
                                    "emailAddress": "navraj.thakur@commscope.com",
                                    "self": "https://ruckus.atlassian.net/rest/api/2/user?accountId=619622c7c75da8007242597b",
                                    "timeZone": "Asia/Kolkata"
                                },
                                "body": "*Scope :-*\n \nSLA Impact Radius :  As per initial analysis problem is specific to this account, hence type SUC(single user case) categorizing as low blast radius.\n \nSLA Impact Calculation : Existing production network/AP/switch functionalities remains unaffected hence Impact is Minimum .\n \nER State : Discovery phase\n \nAdditional Info: Strangely when we tried to pull up by MAC address details were displayed, however other problem like Guest Created and Guest Expires time still remains the same which is an issue.\n \n!https://ruckus.atlassian.net/rest/api/3/attachment/content/745679|height=369,width=800!\n \n!https://ruckus.atlassian.net/rest/api/3/attachment/content/745680|height=369,width=800!",
                                "created": "2025-02-25T06:48:40.693-0800",
                                "id": "1043117",
                                "jsdPublic": True,
                                "self": "https://ruckus.atlassian.net/rest/api/2/issue/317008/comment/1043117",
                                "updateAuthor": {
                                    "accountId": "557058:8b59251f-4f6a-4a26-bd58-ebff9abe7972",
                                    "accountType": "atlassian",
                                    "active": True,
                                    "avatarUrls": {
                                        "16x16": "https://avatar-management--avatars.us-west-2.prod.public.atl-paas.net/557058:8b59251f-4f6a-4a26-bd58-ebff9abe7972/a3b20eb3-6eeb-4bf6-a5c7-7747cdbea555/16",
                                        "24x24": "https://avatar-management--avatars.us-west-2.prod.public.atl-paas.net/557058:8b59251f-4f6a-4a26-bd58-ebff9abe7972/a3b20eb3-6eeb-4bf6-a5c7-7747cdbea555/24",
                                        "32x32": "https://avatar-management--avatars.us-west-2.prod.public.atl-paas.net/557058:8b59251f-4f6a-4a26-bd58-ebff9abe7972/a3b20eb3-6eeb-4bf6-a5c7-7747cdbea555/32",
                                        "48x48": "https://avatar-management--avatars.us-west-2.prod.public.atl-paas.net/557058:8b59251f-4f6a-4a26-bd58-ebff9abe7972/a3b20eb3-6eeb-4bf6-a5c7-7747cdbea555/48"
                                    },
                                    "displayName": "Onteddu, Rajesh",
                                    "emailAddress": "rajesh.onteddu@commscope.com",
                                    "self": "https://ruckus.atlassian.net/rest/api/2/user?accountId=557058%3A8b59251f-4f6a-4a26-bd58-ebff9abe7972",
                                    "timeZone": "America/Los_Angeles"
                                },
                                "updated": "2025-03-01T01:21:21.506-0800"
                            },
                            {
                                "author": {
                                    "accountId": "712020:d33662dd-7b1d-4cbb-8905-e7c9a5cc49f6",
                                    "accountType": "atlassian",
                                    "active": True,
                                    "avatarUrls": {
                                        "16x16": "https://secure.gravatar.com/avatar/8acd7ecda9b8e9c5e20c1d791b5d8671?d=https%3A%2F%2Favatar-management--avatars.us-west-2.prod.public.atl-paas.net%2Finitials%2FWE-5.png",
                                        "24x24": "https://secure.gravatar.com/avatar/8acd7ecda9b8e9c5e20c1d791b5d8671?d=https%3A%2F%2Favatar-management--avatars.us-west-2.prod.public.atl-paas.net%2Finitials%2FWE-5.png",
                                        "32x32": "https://secure.gravatar.com/avatar/8acd7ecda9b8e9c5e20c1d791b5d8671?d=https%3A%2F%2Favatar-management--avatars.us-west-2.prod.public.atl-paas.net%2Finitials%2FWE-5.png",
                                        "48x48": "https://secure.gravatar.com/avatar/8acd7ecda9b8e9c5e20c1d791b5d8671?d=https%3A%2F%2Favatar-management--avatars.us-west-2.prod.public.atl-paas.net%2Finitials%2FWE-5.png"
                                    },
                                    "displayName": "Wu, Eric",
                                    "emailAddress": "eric.wu@commscope.com",
                                    "self": "https://ruckus.atlassian.net/rest/api/2/user?accountId=712020%3Ad33662dd-7b1d-4cbb-8905-e7c9a5cc49f6",
                                    "timeZone": "America/Los_Angeles"
                                },
                                "body": "[observation]\n \nclients\n \n0. e2:b8:c8:54:6c:b8\n \nclient info is no longer available on GUI due to limited data retention.\n \nHowever, the successful client authorization was recorded on Feb 13.\n \n{color:#343741}[https://logs.int.cloud.ruckuswireless.com/s/alto-eu/goto/bb89dee48467b749ef96bee957ca7ccf]{color}\n \n!https://ruckus.atlassian.net/rest/api/3/attachment/content/745681|height=362,width=876!\n \n1. 34:7d:f6:66:f2:01\n \nauthorized method : HotSpot(Wispr)+Mac\n \nwith no guest details, and fixed timestamps on guest created/expires\n \n!https://ruckus.atlassian.net/rest/api/3/attachment/content/745682|height=311,width=553!\n \n2. aa:41:bf:da:4b:6c\n \na. Most guest details were missing.\n \nb. The guest creation and expiration timestamps are fixed to the page click timestamp.\n \n!https://ruckus.atlassian.net/rest/api/3/attachment/content/745683|height=530,width=876!\n \n!https://ruckus.atlassian.net/rest/api/3/attachment/content/745684|height=310,width=553!\n \nRequest URL:\n[https://api.eu.ruckus.cloud/guestUsers/query]\nRequest Method:\nPOST\n \n[preview]\n \ndata\n:\n[{name: \"Debbie Robinson\", id: \"0c14e455-5f24-4ce1-808a-ae86ff9975ab\",…}]\n0\n:\n\\{name: \"Debbie Robinson\", id: \"0c14e455-5f24-4ce1-808a-ae86ff9975ab\",…}\ncreationDate\n:\n\"2025-01-16T16:39:39.172Z\"\ndevicesMac\n:\n[\"ee:bc:ec:0e:ef:5b\", \"aa:41:bf:da:4b:6c\", \"76:c6:c0:b5:31:0f\"]\n0\n:\n\"ee:bc:ec:0e:ef:5b\"\n1\n:\n\"aa:41:bf:da:4b:6c\"\n2\n:\n\"76:c6:c0:b5:31:0f\"\nemailAddress\n:\n\"\"\nexpiryDate\n:\n\"2026-01-16T16:39:39.181Z\"",
                                "created": "2025-02-25T13:37:43.786-0800",
                                "id": "1043118",
                                "jsdPublic": True,
                                "self": "https://ruckus.atlassian.net/rest/api/2/issue/317008/comment/1043118",
                                "updateAuthor": {
                                    "accountId": "557058:8b59251f-4f6a-4a26-bd58-ebff9abe7972",
                                    "accountType": "atlassian",
                                    "active": True,
                                    "avatarUrls": {
                                        "16x16": "https://avatar-management--avatars.us-west-2.prod.public.atl-paas.net/557058:8b59251f-4f6a-4a26-bd58-ebff9abe7972/a3b20eb3-6eeb-4bf6-a5c7-7747cdbea555/16",
                                        "24x24": "https://avatar-management--avatars.us-west-2.prod.public.atl-paas.net/557058:8b59251f-4f6a-4a26-bd58-ebff9abe7972/a3b20eb3-6eeb-4bf6-a5c7-7747cdbea555/24",
                                        "32x32": "https://avatar-management--avatars.us-west-2.prod.public.atl-paas.net/557058:8b59251f-4f6a-4a26-bd58-ebff9abe7972/a3b20eb3-6eeb-4bf6-a5c7-7747cdbea555/32",
                                        "48x48": "https://avatar-management--avatars.us-west-2.prod.public.atl-paas.net/557058:8b59251f-4f6a-4a26-bd58-ebff9abe7972/a3b20eb3-6eeb-4bf6-a5c7-7747cdbea555/48"
                                    },
                                    "displayName": "Onteddu, Rajesh",
                                    "emailAddress": "rajesh.onteddu@commscope.com",
                                    "self": "https://ruckus.atlassian.net/rest/api/2/user?accountId=557058%3A8b59251f-4f6a-4a26-bd58-ebff9abe7972",
                                    "timeZone": "America/Los_Angeles"
                                },
                                "updated": "2025-03-01T01:21:25.721-0800"
                            },
                            {
                                "author": {
                                    "accountId": "712020:d33662dd-7b1d-4cbb-8905-e7c9a5cc49f6",
                                    "accountType": "atlassian",
                                    "active": True,
                                    "avatarUrls": {
                                        "16x16": "https://secure.gravatar.com/avatar/8acd7ecda9b8e9c5e20c1d791b5d8671?d=https%3A%2F%2Favatar-management--avatars.us-west-2.prod.public.atl-paas.net%2Finitials%2FWE-5.png",
                                        "24x24": "https://secure.gravatar.com/avatar/8acd7ecda9b8e9c5e20c1d791b5d8671?d=https%3A%2F%2Favatar-management--avatars.us-west-2.prod.public.atl-paas.net%2Finitials%2FWE-5.png",
                                        "32x32": "https://secure.gravatar.com/avatar/8acd7ecda9b8e9c5e20c1d791b5d8671?d=https%3A%2F%2Favatar-management--avatars.us-west-2.prod.public.atl-paas.net%2Finitials%2FWE-5.png",
                                        "48x48": "https://secure.gravatar.com/avatar/8acd7ecda9b8e9c5e20c1d791b5d8671?d=https%3A%2F%2Favatar-management--avatars.us-west-2.prod.public.atl-paas.net%2Finitials%2FWE-5.png"
                                    },
                                    "displayName": "Wu, Eric",
                                    "emailAddress": "eric.wu@commscope.com",
                                    "self": "https://ruckus.atlassian.net/rest/api/2/user?accountId=712020%3Ad33662dd-7b1d-4cbb-8905-e7c9a5cc49f6",
                                    "timeZone": "America/Los_Angeles"
                                },
                                "body": "ACX-79018 has been raised for further investigation",
                                "created": "2025-02-25T21:41:30.709-0800",
                                "id": "1043119",
                                "jsdPublic": True,
                                "self": "https://ruckus.atlassian.net/rest/api/2/issue/317008/comment/1043119",
                                "updateAuthor": {
                                    "accountId": "557058:8b59251f-4f6a-4a26-bd58-ebff9abe7972",
                                    "accountType": "atlassian",
                                    "active": True,
                                    "avatarUrls": {
                                        "16x16": "https://avatar-management--avatars.us-west-2.prod.public.atl-paas.net/557058:8b59251f-4f6a-4a26-bd58-ebff9abe7972/a3b20eb3-6eeb-4bf6-a5c7-7747cdbea555/16",
                                        "24x24": "https://avatar-management--avatars.us-west-2.prod.public.atl-paas.net/557058:8b59251f-4f6a-4a26-bd58-ebff9abe7972/a3b20eb3-6eeb-4bf6-a5c7-7747cdbea555/24",
                                        "32x32": "https://avatar-management--avatars.us-west-2.prod.public.atl-paas.net/557058:8b59251f-4f6a-4a26-bd58-ebff9abe7972/a3b20eb3-6eeb-4bf6-a5c7-7747cdbea555/32",
                                        "48x48": "https://avatar-management--avatars.us-west-2.prod.public.atl-paas.net/557058:8b59251f-4f6a-4a26-bd58-ebff9abe7972/a3b20eb3-6eeb-4bf6-a5c7-7747cdbea555/48"
                                    },
                                    "displayName": "Onteddu, Rajesh",
                                    "emailAddress": "rajesh.onteddu@commscope.com",
                                    "self": "https://ruckus.atlassian.net/rest/api/2/user?accountId=557058%3A8b59251f-4f6a-4a26-bd58-ebff9abe7972",
                                    "timeZone": "America/Los_Angeles"
                                },
                                "updated": "2025-03-01T01:21:26.072-0800"
                            },
                            {
                                "author": {
                                    "accountId": "712020:d33662dd-7b1d-4cbb-8905-e7c9a5cc49f6",
                                    "accountType": "atlassian",
                                    "active": True,
                                    "avatarUrls": {
                                        "16x16": "https://secure.gravatar.com/avatar/8acd7ecda9b8e9c5e20c1d791b5d8671?d=https%3A%2F%2Favatar-management--avatars.us-west-2.prod.public.atl-paas.net%2Finitials%2FWE-5.png",
                                        "24x24": "https://secure.gravatar.com/avatar/8acd7ecda9b8e9c5e20c1d791b5d8671?d=https%3A%2F%2Favatar-management--avatars.us-west-2.prod.public.atl-paas.net%2Finitials%2FWE-5.png",
                                        "32x32": "https://secure.gravatar.com/avatar/8acd7ecda9b8e9c5e20c1d791b5d8671?d=https%3A%2F%2Favatar-management--avatars.us-west-2.prod.public.atl-paas.net%2Finitials%2FWE-5.png",
                                        "48x48": "https://secure.gravatar.com/avatar/8acd7ecda9b8e9c5e20c1d791b5d8671?d=https%3A%2F%2Favatar-management--avatars.us-west-2.prod.public.atl-paas.net%2Finitials%2FWE-5.png"
                                    },
                                    "displayName": "Wu, Eric",
                                    "emailAddress": "eric.wu@commscope.com",
                                    "self": "https://ruckus.atlassian.net/rest/api/2/user?accountId=712020%3Ad33662dd-7b1d-4cbb-8905-e7c9a5cc49f6",
                                    "timeZone": "America/Los_Angeles"
                                },
                                "body": "Hi Praveen,\n \nThe DBOM requirement mandates a P2 priority.\n \nSince this ticket was created with P3,\n \nthere may be a conflict with the DBOM process. Could you please review whether the priority should be escalated or if the customer can wait for RBOM instead?\n \nNote: Many fixes are pending for the next RBOM due to a backlog of DBOMs currently in the queue.\n \nPlease advise.\n \nThanks!",
                                "created": "2025-02-27T09:21:32.327-0800",
                                "id": "1043120",
                                "jsdPublic": True,
                                "self": "https://ruckus.atlassian.net/rest/api/2/issue/317008/comment/1043120",
                                "updateAuthor": {
                                    "accountId": "557058:8b59251f-4f6a-4a26-bd58-ebff9abe7972",
                                    "accountType": "atlassian",
                                    "active": True,
                                    "avatarUrls": {
                                        "16x16": "https://avatar-management--avatars.us-west-2.prod.public.atl-paas.net/557058:8b59251f-4f6a-4a26-bd58-ebff9abe7972/a3b20eb3-6eeb-4bf6-a5c7-7747cdbea555/16",
                                        "24x24": "https://avatar-management--avatars.us-west-2.prod.public.atl-paas.net/557058:8b59251f-4f6a-4a26-bd58-ebff9abe7972/a3b20eb3-6eeb-4bf6-a5c7-7747cdbea555/24",
                                        "32x32": "https://avatar-management--avatars.us-west-2.prod.public.atl-paas.net/557058:8b59251f-4f6a-4a26-bd58-ebff9abe7972/a3b20eb3-6eeb-4bf6-a5c7-7747cdbea555/32",
                                        "48x48": "https://avatar-management--avatars.us-west-2.prod.public.atl-paas.net/557058:8b59251f-4f6a-4a26-bd58-ebff9abe7972/a3b20eb3-6eeb-4bf6-a5c7-7747cdbea555/48"
                                    },
                                    "displayName": "Onteddu, Rajesh",
                                    "emailAddress": "rajesh.onteddu@commscope.com",
                                    "self": "https://ruckus.atlassian.net/rest/api/2/user?accountId=557058%3A8b59251f-4f6a-4a26-bd58-ebff9abe7972",
                                    "timeZone": "America/Los_Angeles"
                                },
                                "updated": "2025-03-01T01:21:26.391-0800"
                            },
                            {
                                "author": {
                                    "accountId": "712020:f85b2370-dba7-49c7-9733-7243dcd25af7",
                                    "accountType": "atlassian",
                                    "active": True,
                                    "avatarUrls": {
                                        "16x16": "https://secure.gravatar.com/avatar/67b44b9ab907929dae90a026d9fb178e?d=https%3A%2F%2Favatar-management--avatars.us-west-2.prod.public.atl-paas.net%2Finitials%2FJP-0.png",
                                        "24x24": "https://secure.gravatar.com/avatar/67b44b9ab907929dae90a026d9fb178e?d=https%3A%2F%2Favatar-management--avatars.us-west-2.prod.public.atl-paas.net%2Finitials%2FJP-0.png",
                                        "32x32": "https://secure.gravatar.com/avatar/67b44b9ab907929dae90a026d9fb178e?d=https%3A%2F%2Favatar-management--avatars.us-west-2.prod.public.atl-paas.net%2Finitials%2FJP-0.png",
                                        "48x48": "https://secure.gravatar.com/avatar/67b44b9ab907929dae90a026d9fb178e?d=https%3A%2F%2Favatar-management--avatars.us-west-2.prod.public.atl-paas.net%2Finitials%2FJP-0.png"
                                    },
                                    "displayName": "Jacob, Praveen",
                                    "emailAddress": "praveen.jacob@commscope.com",
                                    "self": "https://ruckus.atlassian.net/rest/api/2/user?accountId=712020%3Af85b2370-dba7-49c7-9733-7243dcd25af7",
                                    "timeZone": "America/Los_Angeles"
                                },
                                "body": "Hi [~EWU],\n \nI have increased the priority to P2/S2 to get this fixed through the DBOM at the earliest.\n \nThanks,\n \nPraveen. J",
                                "created": "2025-02-28T07:18:38.579-0800",
                                "id": "1043121",
                                "jsdPublic": True,
                                "self": "https://ruckus.atlassian.net/rest/api/2/issue/317008/comment/1043121",
                                "updateAuthor": {
                                    "accountId": "557058:8b59251f-4f6a-4a26-bd58-ebff9abe7972",
                                    "accountType": "atlassian",
                                    "active": True,
                                    "avatarUrls": {
                                        "16x16": "https://avatar-management--avatars.us-west-2.prod.public.atl-paas.net/557058:8b59251f-4f6a-4a26-bd58-ebff9abe7972/a3b20eb3-6eeb-4bf6-a5c7-7747cdbea555/16",
                                        "24x24": "https://avatar-management--avatars.us-west-2.prod.public.atl-paas.net/557058:8b59251f-4f6a-4a26-bd58-ebff9abe7972/a3b20eb3-6eeb-4bf6-a5c7-7747cdbea555/24",
                                        "32x32": "https://avatar-management--avatars.us-west-2.prod.public.atl-paas.net/557058:8b59251f-4f6a-4a26-bd58-ebff9abe7972/a3b20eb3-6eeb-4bf6-a5c7-7747cdbea555/32",
                                        "48x48": "https://avatar-management--avatars.us-west-2.prod.public.atl-paas.net/557058:8b59251f-4f6a-4a26-bd58-ebff9abe7972/a3b20eb3-6eeb-4bf6-a5c7-7747cdbea555/48"
                                    },
                                    "displayName": "Onteddu, Rajesh",
                                    "emailAddress": "rajesh.onteddu@commscope.com",
                                    "self": "https://ruckus.atlassian.net/rest/api/2/user?accountId=557058%3A8b59251f-4f6a-4a26-bd58-ebff9abe7972",
                                    "timeZone": "America/Los_Angeles"
                                },
                                "updated": "2025-03-01T01:21:26.703-0800"
                            },
                            {
                                "author": {
                                    "accountId": "712020:d33662dd-7b1d-4cbb-8905-e7c9a5cc49f6",
                                    "accountType": "atlassian",
                                    "active": True,
                                    "avatarUrls": {
                                        "16x16": "https://secure.gravatar.com/avatar/8acd7ecda9b8e9c5e20c1d791b5d8671?d=https%3A%2F%2Favatar-management--avatars.us-west-2.prod.public.atl-paas.net%2Finitials%2FWE-5.png",
                                        "24x24": "https://secure.gravatar.com/avatar/8acd7ecda9b8e9c5e20c1d791b5d8671?d=https%3A%2F%2Favatar-management--avatars.us-west-2.prod.public.atl-paas.net%2Finitials%2FWE-5.png",
                                        "32x32": "https://secure.gravatar.com/avatar/8acd7ecda9b8e9c5e20c1d791b5d8671?d=https%3A%2F%2Favatar-management--avatars.us-west-2.prod.public.atl-paas.net%2Finitials%2FWE-5.png",
                                        "48x48": "https://secure.gravatar.com/avatar/8acd7ecda9b8e9c5e20c1d791b5d8671?d=https%3A%2F%2Favatar-management--avatars.us-west-2.prod.public.atl-paas.net%2Finitials%2FWE-5.png"
                                    },
                                    "displayName": "Wu, Eric",
                                    "emailAddress": "eric.wu@commscope.com",
                                    "self": "https://ruckus.atlassian.net/rest/api/2/user?accountId=712020%3Ad33662dd-7b1d-4cbb-8905-e7c9a5cc49f6",
                                    "timeZone": "America/Los_Angeles"
                                },
                                "body": "[Root Cause]\n\nThe username reported by AP does not match the expected GuestPass username\n\nGUI filter fails to identify matching guests and guestDetails field remains empty.\n\n\n[Resolution]\nImproved the GUI filtering logic with MAC address matching, the issue should be gone.\n\n\n\n[Coming Fix]\n\n(3/6 update)\n\nacx-ui : 65793 is now on QA ENV\n\n!image-20250305-181255.png|width=1062,height=183,alt=\"image-20250305-181255.png\"!",
                                "created": "2025-03-03T10:52:52.454-0800",
                                "id": "2774428",
                                "jsdPublic": True,
                                "self": "https://ruckus.atlassian.net/rest/api/2/issue/317008/comment/2774428",
                                "updateAuthor": {
                                    "accountId": "712020:d33662dd-7b1d-4cbb-8905-e7c9a5cc49f6",
                                    "accountType": "atlassian",
                                    "active": True,
                                    "avatarUrls": {
                                        "16x16": "https://secure.gravatar.com/avatar/8acd7ecda9b8e9c5e20c1d791b5d8671?d=https%3A%2F%2Favatar-management--avatars.us-west-2.prod.public.atl-paas.net%2Finitials%2FWE-5.png",
                                        "24x24": "https://secure.gravatar.com/avatar/8acd7ecda9b8e9c5e20c1d791b5d8671?d=https%3A%2F%2Favatar-management--avatars.us-west-2.prod.public.atl-paas.net%2Finitials%2FWE-5.png",
                                        "32x32": "https://secure.gravatar.com/avatar/8acd7ecda9b8e9c5e20c1d791b5d8671?d=https%3A%2F%2Favatar-management--avatars.us-west-2.prod.public.atl-paas.net%2Finitials%2FWE-5.png",
                                        "48x48": "https://secure.gravatar.com/avatar/8acd7ecda9b8e9c5e20c1d791b5d8671?d=https%3A%2F%2Favatar-management--avatars.us-west-2.prod.public.atl-paas.net%2Finitials%2FWE-5.png"
                                    },
                                    "displayName": "Wu, Eric",
                                    "emailAddress": "eric.wu@commscope.com",
                                    "self": "https://ruckus.atlassian.net/rest/api/2/user?accountId=712020%3Ad33662dd-7b1d-4cbb-8905-e7c9a5cc49f6",
                                    "timeZone": "America/Los_Angeles"
                                },
                                "updated": "2025-03-06T12:51:06.542-0800"
                            },
                            {
                                "author": {
                                    "accountId": "712020:f85b2370-dba7-49c7-9733-7243dcd25af7",
                                    "accountType": "atlassian",
                                    "active": True,
                                    "avatarUrls": {
                                        "16x16": "https://secure.gravatar.com/avatar/67b44b9ab907929dae90a026d9fb178e?d=https%3A%2F%2Favatar-management--avatars.us-west-2.prod.public.atl-paas.net%2Finitials%2FJP-0.png",
                                        "24x24": "https://secure.gravatar.com/avatar/67b44b9ab907929dae90a026d9fb178e?d=https%3A%2F%2Favatar-management--avatars.us-west-2.prod.public.atl-paas.net%2Finitials%2FJP-0.png",
                                        "32x32": "https://secure.gravatar.com/avatar/67b44b9ab907929dae90a026d9fb178e?d=https%3A%2F%2Favatar-management--avatars.us-west-2.prod.public.atl-paas.net%2Finitials%2FJP-0.png",
                                        "48x48": "https://secure.gravatar.com/avatar/67b44b9ab907929dae90a026d9fb178e?d=https%3A%2F%2Favatar-management--avatars.us-west-2.prod.public.atl-paas.net%2Finitials%2FJP-0.png"
                                    },
                                    "displayName": "Jacob, Praveen",
                                    "emailAddress": "praveen.jacob@commscope.com",
                                    "self": "https://ruckus.atlassian.net/rest/api/2/user?accountId=712020%3Af85b2370-dba7-49c7-9733-7243dcd25af7",
                                    "timeZone": "America/Los_Angeles"
                                },
                                "body": "Hi [~accountid:712020:d33662dd-7b1d-4cbb-8905-e7c9a5cc49f6],\n\nHas this been rolled out to the prod servers yet? \n\nThanks,\n\nPraveen. J ",
                                "created": "2025-03-07T07:25:03.176-0800",
                                "id": "2778260",
                                "jsdPublic": True,
                                "self": "https://ruckus.atlassian.net/rest/api/2/issue/317008/comment/2778260",
                                "updateAuthor": {
                                    "accountId": "712020:f85b2370-dba7-49c7-9733-7243dcd25af7",
                                    "accountType": "atlassian",
                                    "active": True,
                                    "avatarUrls": {
                                        "16x16": "https://secure.gravatar.com/avatar/67b44b9ab907929dae90a026d9fb178e?d=https%3A%2F%2Favatar-management--avatars.us-west-2.prod.public.atl-paas.net%2Finitials%2FJP-0.png",
                                        "24x24": "https://secure.gravatar.com/avatar/67b44b9ab907929dae90a026d9fb178e?d=https%3A%2F%2Favatar-management--avatars.us-west-2.prod.public.atl-paas.net%2Finitials%2FJP-0.png",
                                        "32x32": "https://secure.gravatar.com/avatar/67b44b9ab907929dae90a026d9fb178e?d=https%3A%2F%2Favatar-management--avatars.us-west-2.prod.public.atl-paas.net%2Finitials%2FJP-0.png",
                                        "48x48": "https://secure.gravatar.com/avatar/67b44b9ab907929dae90a026d9fb178e?d=https%3A%2F%2Favatar-management--avatars.us-west-2.prod.public.atl-paas.net%2Finitials%2FJP-0.png"
                                    },
                                    "displayName": "Jacob, Praveen",
                                    "emailAddress": "praveen.jacob@commscope.com",
                                    "self": "https://ruckus.atlassian.net/rest/api/2/user?accountId=712020%3Af85b2370-dba7-49c7-9733-7243dcd25af7",
                                    "timeZone": "America/Los_Angeles"
                                },
                                "updated": "2025-03-07T07:25:03.176-0800"
                            },
                            {
                                "author": {
                                    "accountId": "712020:d33662dd-7b1d-4cbb-8905-e7c9a5cc49f6",
                                    "accountType": "atlassian",
                                    "active": True,
                                    "avatarUrls": {
                                        "16x16": "https://secure.gravatar.com/avatar/8acd7ecda9b8e9c5e20c1d791b5d8671?d=https%3A%2F%2Favatar-management--avatars.us-west-2.prod.public.atl-paas.net%2Finitials%2FWE-5.png",
                                        "24x24": "https://secure.gravatar.com/avatar/8acd7ecda9b8e9c5e20c1d791b5d8671?d=https%3A%2F%2Favatar-management--avatars.us-west-2.prod.public.atl-paas.net%2Finitials%2FWE-5.png",
                                        "32x32": "https://secure.gravatar.com/avatar/8acd7ecda9b8e9c5e20c1d791b5d8671?d=https%3A%2F%2Favatar-management--avatars.us-west-2.prod.public.atl-paas.net%2Finitials%2FWE-5.png",
                                        "48x48": "https://secure.gravatar.com/avatar/8acd7ecda9b8e9c5e20c1d791b5d8671?d=https%3A%2F%2Favatar-management--avatars.us-west-2.prod.public.atl-paas.net%2Finitials%2FWE-5.png"
                                    },
                                    "displayName": "Wu, Eric",
                                    "emailAddress": "eric.wu@commscope.com",
                                    "self": "https://ruckus.atlassian.net/rest/api/2/user?accountId=712020%3Ad33662dd-7b1d-4cbb-8905-e7c9a5cc49f6",
                                    "timeZone": "America/Los_Angeles"
                                },
                                "body": "Hi Praveen,\n\nThanks for the info.\n\nNot yet, due to the high volume of DBOM recently. \n\nIt is expected to be included in the next RBOM (e.g., acx-service-5245+ ).\n\nwill continue to provide updates on the fix progress below.\n\nThanks!\n\n\n\n[Coming Fix]\n\n(3/12 update)\n\nacx-ui : 65793 is now on QA ENV\n\n!image-20250310-171841.png|width=908,height=118,alt=\"image-20250310-171841.png\"!",
                                "created": "2025-03-07T09:53:08.650-0800",
                                "id": "2778302",
                                "jsdPublic": True,
                                "self": "https://ruckus.atlassian.net/rest/api/2/issue/317008/comment/2778302",
                                "updateAuthor": {
                                    "accountId": "712020:d33662dd-7b1d-4cbb-8905-e7c9a5cc49f6",
                                    "accountType": "atlassian",
                                    "active": True,
                                    "avatarUrls": {
                                        "16x16": "https://secure.gravatar.com/avatar/8acd7ecda9b8e9c5e20c1d791b5d8671?d=https%3A%2F%2Favatar-management--avatars.us-west-2.prod.public.atl-paas.net%2Finitials%2FWE-5.png",
                                        "24x24": "https://secure.gravatar.com/avatar/8acd7ecda9b8e9c5e20c1d791b5d8671?d=https%3A%2F%2Favatar-management--avatars.us-west-2.prod.public.atl-paas.net%2Finitials%2FWE-5.png",
                                        "32x32": "https://secure.gravatar.com/avatar/8acd7ecda9b8e9c5e20c1d791b5d8671?d=https%3A%2F%2Favatar-management--avatars.us-west-2.prod.public.atl-paas.net%2Finitials%2FWE-5.png",
                                        "48x48": "https://secure.gravatar.com/avatar/8acd7ecda9b8e9c5e20c1d791b5d8671?d=https%3A%2F%2Favatar-management--avatars.us-west-2.prod.public.atl-paas.net%2Finitials%2FWE-5.png"
                                    },
                                    "displayName": "Wu, Eric",
                                    "emailAddress": "eric.wu@commscope.com",
                                    "self": "https://ruckus.atlassian.net/rest/api/2/user?accountId=712020%3Ad33662dd-7b1d-4cbb-8905-e7c9a5cc49f6",
                                    "timeZone": "America/Los_Angeles"
                                },
                                "updated": "2025-03-11T10:01:25.790-0700"
                            },
                            {
                                "author": {
                                    "accountId": "712020:d33662dd-7b1d-4cbb-8905-e7c9a5cc49f6",
                                    "accountType": "atlassian",
                                    "active": True,
                                    "avatarUrls": {
                                        "16x16": "https://secure.gravatar.com/avatar/8acd7ecda9b8e9c5e20c1d791b5d8671?d=https%3A%2F%2Favatar-management--avatars.us-west-2.prod.public.atl-paas.net%2Finitials%2FWE-5.png",
                                        "24x24": "https://secure.gravatar.com/avatar/8acd7ecda9b8e9c5e20c1d791b5d8671?d=https%3A%2F%2Favatar-management--avatars.us-west-2.prod.public.atl-paas.net%2Finitials%2FWE-5.png",
                                        "32x32": "https://secure.gravatar.com/avatar/8acd7ecda9b8e9c5e20c1d791b5d8671?d=https%3A%2F%2Favatar-management--avatars.us-west-2.prod.public.atl-paas.net%2Finitials%2FWE-5.png",
                                        "48x48": "https://secure.gravatar.com/avatar/8acd7ecda9b8e9c5e20c1d791b5d8671?d=https%3A%2F%2Favatar-management--avatars.us-west-2.prod.public.atl-paas.net%2Finitials%2FWE-5.png"
                                    },
                                    "displayName": "Wu, Eric",
                                    "emailAddress": "eric.wu@commscope.com",
                                    "self": "https://ruckus.atlassian.net/rest/api/2/user?accountId=712020%3Ad33662dd-7b1d-4cbb-8905-e7c9a5cc49f6",
                                    "timeZone": "America/Los_Angeles"
                                },
                                "body": "Resolving this ticket as the acx-ui: 65793 in acx-service-5248 is now on STAGE and should be on PROD soon.",
                                "created": "2025-03-14T09:46:00.418-0700",
                                "id": "2781615",
                                "jsdPublic": True,
                                "self": "https://ruckus.atlassian.net/rest/api/2/issue/317008/comment/2781615",
                                "updateAuthor": {
                                    "accountId": "712020:d33662dd-7b1d-4cbb-8905-e7c9a5cc49f6",
                                    "accountType": "atlassian",
                                    "active": True,
                                    "avatarUrls": {
                                        "16x16": "https://secure.gravatar.com/avatar/8acd7ecda9b8e9c5e20c1d791b5d8671?d=https%3A%2F%2Favatar-management--avatars.us-west-2.prod.public.atl-paas.net%2Finitials%2FWE-5.png",
                                        "24x24": "https://secure.gravatar.com/avatar/8acd7ecda9b8e9c5e20c1d791b5d8671?d=https%3A%2F%2Favatar-management--avatars.us-west-2.prod.public.atl-paas.net%2Finitials%2FWE-5.png",
                                        "32x32": "https://secure.gravatar.com/avatar/8acd7ecda9b8e9c5e20c1d791b5d8671?d=https%3A%2F%2Favatar-management--avatars.us-west-2.prod.public.atl-paas.net%2Finitials%2FWE-5.png",
                                        "48x48": "https://secure.gravatar.com/avatar/8acd7ecda9b8e9c5e20c1d791b5d8671?d=https%3A%2F%2Favatar-management--avatars.us-west-2.prod.public.atl-paas.net%2Finitials%2FWE-5.png"
                                    },
                                    "displayName": "Wu, Eric",
                                    "emailAddress": "eric.wu@commscope.com",
                                    "self": "https://ruckus.atlassian.net/rest/api/2/user?accountId=712020%3Ad33662dd-7b1d-4cbb-8905-e7c9a5cc49f6",
                                    "timeZone": "America/Los_Angeles"
                                },
                                "updated": "2025-03-14T09:46:00.418-0700"
                            },
                            {
                                "author": {
                                    "accountId": "712020:f85b2370-dba7-49c7-9733-7243dcd25af7",
                                    "accountType": "atlassian",
                                    "active": True,
                                    "avatarUrls": {
                                        "16x16": "https://secure.gravatar.com/avatar/67b44b9ab907929dae90a026d9fb178e?d=https%3A%2F%2Favatar-management--avatars.us-west-2.prod.public.atl-paas.net%2Finitials%2FJP-0.png",
                                        "24x24": "https://secure.gravatar.com/avatar/67b44b9ab907929dae90a026d9fb178e?d=https%3A%2F%2Favatar-management--avatars.us-west-2.prod.public.atl-paas.net%2Finitials%2FJP-0.png",
                                        "32x32": "https://secure.gravatar.com/avatar/67b44b9ab907929dae90a026d9fb178e?d=https%3A%2F%2Favatar-management--avatars.us-west-2.prod.public.atl-paas.net%2Finitials%2FJP-0.png",
                                        "48x48": "https://secure.gravatar.com/avatar/67b44b9ab907929dae90a026d9fb178e?d=https%3A%2F%2Favatar-management--avatars.us-west-2.prod.public.atl-paas.net%2Finitials%2FJP-0.png"
                                    },
                                    "displayName": "Jacob, Praveen",
                                    "emailAddress": "praveen.jacob@commscope.com",
                                    "self": "https://ruckus.atlassian.net/rest/api/2/user?accountId=712020%3Af85b2370-dba7-49c7-9733-7243dcd25af7",
                                    "timeZone": "America/Los_Angeles"
                                },
                                "body": "Hi [~accountid:712020:d33662dd-7b1d-4cbb-8905-e7c9a5cc49f6],\n\nDo you have an ETA for this fix? \n\nThanks,\n\nPraveen. J ",
                                "created": "2025-03-17T07:06:55.851-0700",
                                "id": "2782410",
                                "jsdPublic": True,
                                "self": "https://ruckus.atlassian.net/rest/api/2/issue/317008/comment/2782410",
                                "updateAuthor": {
                                    "accountId": "712020:f85b2370-dba7-49c7-9733-7243dcd25af7",
                                    "accountType": "atlassian",
                                    "active": True,
                                    "avatarUrls": {
                                        "16x16": "https://secure.gravatar.com/avatar/67b44b9ab907929dae90a026d9fb178e?d=https%3A%2F%2Favatar-management--avatars.us-west-2.prod.public.atl-paas.net%2Finitials%2FJP-0.png",
                                        "24x24": "https://secure.gravatar.com/avatar/67b44b9ab907929dae90a026d9fb178e?d=https%3A%2F%2Favatar-management--avatars.us-west-2.prod.public.atl-paas.net%2Finitials%2FJP-0.png",
                                        "32x32": "https://secure.gravatar.com/avatar/67b44b9ab907929dae90a026d9fb178e?d=https%3A%2F%2Favatar-management--avatars.us-west-2.prod.public.atl-paas.net%2Finitials%2FJP-0.png",
                                        "48x48": "https://secure.gravatar.com/avatar/67b44b9ab907929dae90a026d9fb178e?d=https%3A%2F%2Favatar-management--avatars.us-west-2.prod.public.atl-paas.net%2Finitials%2FJP-0.png"
                                    },
                                    "displayName": "Jacob, Praveen",
                                    "emailAddress": "praveen.jacob@commscope.com",
                                    "self": "https://ruckus.atlassian.net/rest/api/2/user?accountId=712020%3Af85b2370-dba7-49c7-9733-7243dcd25af7",
                                    "timeZone": "America/Los_Angeles"
                                },
                                "updated": "2025-03-17T07:06:55.851-0700"
                            },
                            {
                                "author": {
                                    "accountId": "712020:f85b2370-dba7-49c7-9733-7243dcd25af7",
                                    "accountType": "atlassian",
                                    "active": True,
                                    "avatarUrls": {
                                        "16x16": "https://secure.gravatar.com/avatar/67b44b9ab907929dae90a026d9fb178e?d=https%3A%2F%2Favatar-management--avatars.us-west-2.prod.public.atl-paas.net%2Finitials%2FJP-0.png",
                                        "24x24": "https://secure.gravatar.com/avatar/67b44b9ab907929dae90a026d9fb178e?d=https%3A%2F%2Favatar-management--avatars.us-west-2.prod.public.atl-paas.net%2Finitials%2FJP-0.png",
                                        "32x32": "https://secure.gravatar.com/avatar/67b44b9ab907929dae90a026d9fb178e?d=https%3A%2F%2Favatar-management--avatars.us-west-2.prod.public.atl-paas.net%2Finitials%2FJP-0.png",
                                        "48x48": "https://secure.gravatar.com/avatar/67b44b9ab907929dae90a026d9fb178e?d=https%3A%2F%2Favatar-management--avatars.us-west-2.prod.public.atl-paas.net%2Finitials%2FJP-0.png"
                                    },
                                    "displayName": "Jacob, Praveen",
                                    "emailAddress": "praveen.jacob@commscope.com",
                                    "self": "https://ruckus.atlassian.net/rest/api/2/user?accountId=712020%3Af85b2370-dba7-49c7-9733-7243dcd25af7",
                                    "timeZone": "America/Los_Angeles"
                                },
                                "body": "Hi [~accountid:712020:d33662dd-7b1d-4cbb-8905-e7c9a5cc49f6], \n\nI still see the same issue in the R1 GUI. \n\n!image-20250325-154149.png|width=1706,height=891,alt=\"image-20250325-154149.png\"!\n\nThanks,\n\nPraveen. J",
                                "created": "2025-03-25T08:42:09.539-0700",
                                "id": "2787602",
                                "jsdPublic": True,
                                "self": "https://ruckus.atlassian.net/rest/api/2/issue/317008/comment/2787602",
                                "updateAuthor": {
                                    "accountId": "712020:f85b2370-dba7-49c7-9733-7243dcd25af7",
                                    "accountType": "atlassian",
                                    "active": True,
                                    "avatarUrls": {
                                        "16x16": "https://secure.gravatar.com/avatar/67b44b9ab907929dae90a026d9fb178e?d=https%3A%2F%2Favatar-management--avatars.us-west-2.prod.public.atl-paas.net%2Finitials%2FJP-0.png",
                                        "24x24": "https://secure.gravatar.com/avatar/67b44b9ab907929dae90a026d9fb178e?d=https%3A%2F%2Favatar-management--avatars.us-west-2.prod.public.atl-paas.net%2Finitials%2FJP-0.png",
                                        "32x32": "https://secure.gravatar.com/avatar/67b44b9ab907929dae90a026d9fb178e?d=https%3A%2F%2Favatar-management--avatars.us-west-2.prod.public.atl-paas.net%2Finitials%2FJP-0.png",
                                        "48x48": "https://secure.gravatar.com/avatar/67b44b9ab907929dae90a026d9fb178e?d=https%3A%2F%2Favatar-management--avatars.us-west-2.prod.public.atl-paas.net%2Finitials%2FJP-0.png"
                                    },
                                    "displayName": "Jacob, Praveen",
                                    "emailAddress": "praveen.jacob@commscope.com",
                                    "self": "https://ruckus.atlassian.net/rest/api/2/user?accountId=712020%3Af85b2370-dba7-49c7-9733-7243dcd25af7",
                                    "timeZone": "America/Los_Angeles"
                                },
                                "updated": "2025-03-25T08:42:09.539-0700"
                            },
                            {
                                "author": {
                                    "accountId": "712020:d33662dd-7b1d-4cbb-8905-e7c9a5cc49f6",
                                    "accountType": "atlassian",
                                    "active": True,
                                    "avatarUrls": {
                                        "16x16": "https://secure.gravatar.com/avatar/8acd7ecda9b8e9c5e20c1d791b5d8671?d=https%3A%2F%2Favatar-management--avatars.us-west-2.prod.public.atl-paas.net%2Finitials%2FWE-5.png",
                                        "24x24": "https://secure.gravatar.com/avatar/8acd7ecda9b8e9c5e20c1d791b5d8671?d=https%3A%2F%2Favatar-management--avatars.us-west-2.prod.public.atl-paas.net%2Finitials%2FWE-5.png",
                                        "32x32": "https://secure.gravatar.com/avatar/8acd7ecda9b8e9c5e20c1d791b5d8671?d=https%3A%2F%2Favatar-management--avatars.us-west-2.prod.public.atl-paas.net%2Finitials%2FWE-5.png",
                                        "48x48": "https://secure.gravatar.com/avatar/8acd7ecda9b8e9c5e20c1d791b5d8671?d=https%3A%2F%2Favatar-management--avatars.us-west-2.prod.public.atl-paas.net%2Finitials%2FWE-5.png"
                                    },
                                    "displayName": "Wu, Eric",
                                    "emailAddress": "eric.wu@commscope.com",
                                    "self": "https://ruckus.atlassian.net/rest/api/2/user?accountId=712020%3Ad33662dd-7b1d-4cbb-8905-e7c9a5cc49f6",
                                    "timeZone": "America/Los_Angeles"
                                },
                                "body": "The issue is still observed on EU, \n\nchecking if the acx-ui fix is included in latest build or not.\n\n!image-20250325-175041.png|width=1358,height=763,alt=\"image-20250325-175041.png\"!",
                                "created": "2025-03-25T10:53:28.602-0700",
                                "id": "2787652",
                                "jsdPublic": True,
                                "self": "https://ruckus.atlassian.net/rest/api/2/issue/317008/comment/2787652",
                                "updateAuthor": {
                                    "accountId": "712020:d33662dd-7b1d-4cbb-8905-e7c9a5cc49f6",
                                    "accountType": "atlassian",
                                    "active": True,
                                    "avatarUrls": {
                                        "16x16": "https://secure.gravatar.com/avatar/8acd7ecda9b8e9c5e20c1d791b5d8671?d=https%3A%2F%2Favatar-management--avatars.us-west-2.prod.public.atl-paas.net%2Finitials%2FWE-5.png",
                                        "24x24": "https://secure.gravatar.com/avatar/8acd7ecda9b8e9c5e20c1d791b5d8671?d=https%3A%2F%2Favatar-management--avatars.us-west-2.prod.public.atl-paas.net%2Finitials%2FWE-5.png",
                                        "32x32": "https://secure.gravatar.com/avatar/8acd7ecda9b8e9c5e20c1d791b5d8671?d=https%3A%2F%2Favatar-management--avatars.us-west-2.prod.public.atl-paas.net%2Finitials%2FWE-5.png",
                                        "48x48": "https://secure.gravatar.com/avatar/8acd7ecda9b8e9c5e20c1d791b5d8671?d=https%3A%2F%2Favatar-management--avatars.us-west-2.prod.public.atl-paas.net%2Finitials%2FWE-5.png"
                                    },
                                    "displayName": "Wu, Eric",
                                    "emailAddress": "eric.wu@commscope.com",
                                    "self": "https://ruckus.atlassian.net/rest/api/2/user?accountId=712020%3Ad33662dd-7b1d-4cbb-8905-e7c9a5cc49f6",
                                    "timeZone": "America/Los_Angeles"
                                },
                                "updated": "2025-03-25T10:53:28.602-0700"
                            },
                            {
                                "author": {
                                    "accountId": "712020:d33662dd-7b1d-4cbb-8905-e7c9a5cc49f6",
                                    "accountType": "atlassian",
                                    "active": True,
                                    "avatarUrls": {
                                        "16x16": "https://secure.gravatar.com/avatar/8acd7ecda9b8e9c5e20c1d791b5d8671?d=https%3A%2F%2Favatar-management--avatars.us-west-2.prod.public.atl-paas.net%2Finitials%2FWE-5.png",
                                        "24x24": "https://secure.gravatar.com/avatar/8acd7ecda9b8e9c5e20c1d791b5d8671?d=https%3A%2F%2Favatar-management--avatars.us-west-2.prod.public.atl-paas.net%2Finitials%2FWE-5.png",
                                        "32x32": "https://secure.gravatar.com/avatar/8acd7ecda9b8e9c5e20c1d791b5d8671?d=https%3A%2F%2Favatar-management--avatars.us-west-2.prod.public.atl-paas.net%2Finitials%2FWE-5.png",
                                        "48x48": "https://secure.gravatar.com/avatar/8acd7ecda9b8e9c5e20c1d791b5d8671?d=https%3A%2F%2Favatar-management--avatars.us-west-2.prod.public.atl-paas.net%2Finitials%2FWE-5.png"
                                    },
                                    "displayName": "Wu, Eric",
                                    "emailAddress": "eric.wu@commscope.com",
                                    "self": "https://ruckus.atlassian.net/rest/api/2/user?accountId=712020%3Ad33662dd-7b1d-4cbb-8905-e7c9a5cc49f6",
                                    "timeZone": "America/Los_Angeles"
                                },
                                "body": "The previous change has already been deployed to PROD.\nchecking if other fixes are needed or not",
                                "created": "2025-03-27T10:13:49.731-0700",
                                "id": "2789059",
                                "jsdPublic": True,
                                "self": "https://ruckus.atlassian.net/rest/api/2/issue/317008/comment/2789059",
                                "updateAuthor": {
                                    "accountId": "712020:d33662dd-7b1d-4cbb-8905-e7c9a5cc49f6",
                                    "accountType": "atlassian",
                                    "active": True,
                                    "avatarUrls": {
                                        "16x16": "https://secure.gravatar.com/avatar/8acd7ecda9b8e9c5e20c1d791b5d8671?d=https%3A%2F%2Favatar-management--avatars.us-west-2.prod.public.atl-paas.net%2Finitials%2FWE-5.png",
                                        "24x24": "https://secure.gravatar.com/avatar/8acd7ecda9b8e9c5e20c1d791b5d8671?d=https%3A%2F%2Favatar-management--avatars.us-west-2.prod.public.atl-paas.net%2Finitials%2FWE-5.png",
                                        "32x32": "https://secure.gravatar.com/avatar/8acd7ecda9b8e9c5e20c1d791b5d8671?d=https%3A%2F%2Favatar-management--avatars.us-west-2.prod.public.atl-paas.net%2Finitials%2FWE-5.png",
                                        "48x48": "https://secure.gravatar.com/avatar/8acd7ecda9b8e9c5e20c1d791b5d8671?d=https%3A%2F%2Favatar-management--avatars.us-west-2.prod.public.atl-paas.net%2Finitials%2FWE-5.png"
                                    },
                                    "displayName": "Wu, Eric",
                                    "emailAddress": "eric.wu@commscope.com",
                                    "self": "https://ruckus.atlassian.net/rest/api/2/user?accountId=712020%3Ad33662dd-7b1d-4cbb-8905-e7c9a5cc49f6",
                                    "timeZone": "America/Los_Angeles"
                                },
                                "updated": "2025-03-27T10:13:49.731-0700"
                            },
                            {
                                "author": {
                                    "accountId": "712020:312e8ba4-7f21-4469-a639-1a67636dcfc8",
                                    "accountType": "atlassian",
                                    "active": True,
                                    "avatarUrls": {
                                        "16x16": "https://secure.gravatar.com/avatar/1ce2e868f1ef9aeed6740b4fc435a740?d=https%3A%2F%2Favatar-management--avatars.us-west-2.prod.public.atl-paas.net%2Finitials%2FYW-5.png",
                                        "24x24": "https://secure.gravatar.com/avatar/1ce2e868f1ef9aeed6740b4fc435a740?d=https%3A%2F%2Favatar-management--avatars.us-west-2.prod.public.atl-paas.net%2Finitials%2FYW-5.png",
                                        "32x32": "https://secure.gravatar.com/avatar/1ce2e868f1ef9aeed6740b4fc435a740?d=https%3A%2F%2Favatar-management--avatars.us-west-2.prod.public.atl-paas.net%2Finitials%2FYW-5.png",
                                        "48x48": "https://secure.gravatar.com/avatar/1ce2e868f1ef9aeed6740b4fc435a740?d=https%3A%2F%2Favatar-management--avatars.us-west-2.prod.public.atl-paas.net%2Finitials%2FYW-5.png"
                                    },
                                    "displayName": "Yang, William",
                                    "emailAddress": "william.yang@commscope.com",
                                    "self": "https://ruckus.atlassian.net/rest/api/2/user?accountId=712020%3A312e8ba4-7f21-4469-a639-1a67636dcfc8",
                                    "timeZone": "America/Los_Angeles"
                                },
                                "body": "Issue unable to be reproduced in my PROD-EU tenant.\n\n\n!image-20250328-022553.png|width=408,height=677,alt=\"image-20250328-022553.png\"!",
                                "created": "2025-03-27T19:27:00.577-0700",
                                "id": "2789229",
                                "jsdPublic": True,
                                "self": "https://ruckus.atlassian.net/rest/api/2/issue/317008/comment/2789229",
                                "updateAuthor": {
                                    "accountId": "712020:312e8ba4-7f21-4469-a639-1a67636dcfc8",
                                    "accountType": "atlassian",
                                    "active": True,
                                    "avatarUrls": {
                                        "16x16": "https://secure.gravatar.com/avatar/1ce2e868f1ef9aeed6740b4fc435a740?d=https%3A%2F%2Favatar-management--avatars.us-west-2.prod.public.atl-paas.net%2Finitials%2FYW-5.png",
                                        "24x24": "https://secure.gravatar.com/avatar/1ce2e868f1ef9aeed6740b4fc435a740?d=https%3A%2F%2Favatar-management--avatars.us-west-2.prod.public.atl-paas.net%2Finitials%2FYW-5.png",
                                        "32x32": "https://secure.gravatar.com/avatar/1ce2e868f1ef9aeed6740b4fc435a740?d=https%3A%2F%2Favatar-management--avatars.us-west-2.prod.public.atl-paas.net%2Finitials%2FYW-5.png",
                                        "48x48": "https://secure.gravatar.com/avatar/1ce2e868f1ef9aeed6740b4fc435a740?d=https%3A%2F%2Favatar-management--avatars.us-west-2.prod.public.atl-paas.net%2Finitials%2FYW-5.png"
                                    },
                                    "displayName": "Yang, William",
                                    "emailAddress": "william.yang@commscope.com",
                                    "self": "https://ruckus.atlassian.net/rest/api/2/user?accountId=712020%3A312e8ba4-7f21-4469-a639-1a67636dcfc8",
                                    "timeZone": "America/Los_Angeles"
                                },
                                "updated": "2025-03-27T19:27:00.577-0700"
                            },
                            {
                                "author": {
                                    "accountId": "712020:d33662dd-7b1d-4cbb-8905-e7c9a5cc49f6",
                                    "accountType": "atlassian",
                                    "active": True,
                                    "avatarUrls": {
                                        "16x16": "https://secure.gravatar.com/avatar/8acd7ecda9b8e9c5e20c1d791b5d8671?d=https%3A%2F%2Favatar-management--avatars.us-west-2.prod.public.atl-paas.net%2Finitials%2FWE-5.png",
                                        "24x24": "https://secure.gravatar.com/avatar/8acd7ecda9b8e9c5e20c1d791b5d8671?d=https%3A%2F%2Favatar-management--avatars.us-west-2.prod.public.atl-paas.net%2Finitials%2FWE-5.png",
                                        "32x32": "https://secure.gravatar.com/avatar/8acd7ecda9b8e9c5e20c1d791b5d8671?d=https%3A%2F%2Favatar-management--avatars.us-west-2.prod.public.atl-paas.net%2Finitials%2FWE-5.png",
                                        "48x48": "https://secure.gravatar.com/avatar/8acd7ecda9b8e9c5e20c1d791b5d8671?d=https%3A%2F%2Favatar-management--avatars.us-west-2.prod.public.atl-paas.net%2Finitials%2FWE-5.png"
                                    },
                                    "displayName": "Wu, Eric",
                                    "emailAddress": "eric.wu@commscope.com",
                                    "self": "https://ruckus.atlassian.net/rest/api/2/user?accountId=712020%3Ad33662dd-7b1d-4cbb-8905-e7c9a5cc49f6",
                                    "timeZone": "America/Los_Angeles"
                                },
                                "body": "[next action item]\n\n1 Unauthorized Guest Client:\n\n=> can have further enhancement to Keep the guest details field completely empty to avoid confusion\n\n\n\n2 Working Authorized Guest Client:\n\n=> Unable to reproduce the issue as shown in the screenshot above.\n\n\n\n3 Non-Working Authorized Guest Client:\n\nThe guest service was unable to find the login record of client b0:68:e6:60:9c:f1, resulting in the guest info not being displayed as expected.\n\nFurther investigation would be needed from both the AP and CP teams.\n\n!image-20250328-041538.png|width=1375,height=663,alt=\"image-20250328-041538.png\"!\n\n{{https://logs.int.cloud.ruckuswireless.com/s/alto-eu/goto/52ee6a6d390eca545a9b28a658676bc3}}\n\n!image-20250328-042807.png|width=1469,height=614,alt=\"image-20250328-042807.png\"!\n\n\n\ncustomer problematic client b0:68:e6:60:9c:f1\n\ncustomer R650 7.0.0.300.649  202339001014  \n[^SupportLog_202339001014_27032025-2123.log] \n\n{panel:bgColor=#eae6ff}\n(SupportLog_202339001014_27032025-2123.log)\n\n----- wlan34 -----\nb0:68:e6:60:9c:f1 {\n    Allow                   : Y\n    Device Info             : { Smartphone, Android, Android } [DHCP]\n    Hostname                : android-83d4097bc05e727a\n    Forwarding Policy       : 4(LBOAP)\n    VLAN ID                 : 994\n    IP Address              : 10.99.4.23 (H)\n    IPv6 Address            :  \n    DHCP Lease Time         : 41726\n    DHCP XID                : 0x534abffa\n    Packet Drop (Force DHCP): 0\n    DHCP ACK Packets        : 163\n    Life Time               : 300\n    FIREWALL ID             : N/A\n    CI Unicast Filter       : Enabled\n    CI Multicast Filter     : Disabled\n    Antispoof arpreq_count  : 0\n    Antispoof dhcpreq_count : 0\n    CUI                     :\n    DHCP Pool Name          :\n    NAT Pool Name           :\n    Session Duration        : 1362305\n    Station Type            : Wireless\n    Roam state              : New connection\n{color:#bf2600}    Auth Type               : Wispr{color}\n{color:#bf2600}    Auth Method             : Mac{color}\n    RL UPlink               : 0\n    RL Downlink             : 0\n    Mscs Status             : Disabled\n    Flags                   : 0x618\n}\n{panel}",
                                "created": "2025-03-27T21:33:46.321-0700",
                                "id": "2789298",
                                "jsdPublic": True,
                                "self": "https://ruckus.atlassian.net/rest/api/2/issue/317008/comment/2789298",
                                "updateAuthor": {
                                    "accountId": "712020:d33662dd-7b1d-4cbb-8905-e7c9a5cc49f6",
                                    "accountType": "atlassian",
                                    "active": True,
                                    "avatarUrls": {
                                        "16x16": "https://secure.gravatar.com/avatar/8acd7ecda9b8e9c5e20c1d791b5d8671?d=https%3A%2F%2Favatar-management--avatars.us-west-2.prod.public.atl-paas.net%2Finitials%2FWE-5.png",
                                        "24x24": "https://secure.gravatar.com/avatar/8acd7ecda9b8e9c5e20c1d791b5d8671?d=https%3A%2F%2Favatar-management--avatars.us-west-2.prod.public.atl-paas.net%2Finitials%2FWE-5.png",
                                        "32x32": "https://secure.gravatar.com/avatar/8acd7ecda9b8e9c5e20c1d791b5d8671?d=https%3A%2F%2Favatar-management--avatars.us-west-2.prod.public.atl-paas.net%2Finitials%2FWE-5.png",
                                        "48x48": "https://secure.gravatar.com/avatar/8acd7ecda9b8e9c5e20c1d791b5d8671?d=https%3A%2F%2Favatar-management--avatars.us-west-2.prod.public.atl-paas.net%2Finitials%2FWE-5.png"
                                    },
                                    "displayName": "Wu, Eric",
                                    "emailAddress": "eric.wu@commscope.com",
                                    "self": "https://ruckus.atlassian.net/rest/api/2/user?accountId=712020%3Ad33662dd-7b1d-4cbb-8905-e7c9a5cc49f6",
                                    "timeZone": "America/Los_Angeles"
                                },
                                "updated": "2025-03-27T21:33:46.321-0700"
                            },
                            {
                                "author": {
                                    "accountId": "712020:d33662dd-7b1d-4cbb-8905-e7c9a5cc49f6",
                                    "accountType": "atlassian",
                                    "active": True,
                                    "avatarUrls": {
                                        "16x16": "https://secure.gravatar.com/avatar/8acd7ecda9b8e9c5e20c1d791b5d8671?d=https%3A%2F%2Favatar-management--avatars.us-west-2.prod.public.atl-paas.net%2Finitials%2FWE-5.png",
                                        "24x24": "https://secure.gravatar.com/avatar/8acd7ecda9b8e9c5e20c1d791b5d8671?d=https%3A%2F%2Favatar-management--avatars.us-west-2.prod.public.atl-paas.net%2Finitials%2FWE-5.png",
                                        "32x32": "https://secure.gravatar.com/avatar/8acd7ecda9b8e9c5e20c1d791b5d8671?d=https%3A%2F%2Favatar-management--avatars.us-west-2.prod.public.atl-paas.net%2Finitials%2FWE-5.png",
                                        "48x48": "https://secure.gravatar.com/avatar/8acd7ecda9b8e9c5e20c1d791b5d8671?d=https%3A%2F%2Favatar-management--avatars.us-west-2.prod.public.atl-paas.net%2Finitials%2FWE-5.png"
                                    },
                                    "displayName": "Wu, Eric",
                                    "emailAddress": "eric.wu@commscope.com",
                                    "self": "https://ruckus.atlassian.net/rest/api/2/user?accountId=712020%3Ad33662dd-7b1d-4cbb-8905-e7c9a5cc49f6",
                                    "timeZone": "America/Los_Angeles"
                                },
                                "body": "Hi [~accountid:712020:f85b2370-dba7-49c7-9733-7243dcd25af7] \n\nCould you please assist with the following action items?\n\n\n\n# Given the EET AP could not reproduce the issue as previously mentioned, \ncould you please verify whether the issue can be observed from the Support lab AP or if it only exists on the customer side?\n\n# If the issue cannot be replicated in support lab, please check whether the customer allows at least two more lab APs (Support lab AP and EET AP) to join the problematic guest SSID.\n\n# Enable the Durga info level of the \"session-manager\" as shown in the screenshot:\na. Set the customer tenant ID to \"add root.DEBUG tenant (max 5)\".\nb. change log level to \"INFO\".\nc. Wait for 5 minutes and ensure that the \"INFO\" logs of the \"session-manager\" are populated on Kibana.\n\n!image-20250329-062044.png|width=1284,height=765,alt=\"image-20250329-062044.png\"!\n\n# Once the \"session-manager\" \"INFO\" logs are visible on Kibana:\na.  Join the Support lab AP and client to the problematic guest SSID\nb. Check whether the issue can be reproduced, particularly when the client auth status shows \"authorized\" while the guest created/expiration time remains the same.\n\n# EET AP will remain on hold from joining the customer SSID until EET has R1 customer account access permission again.\n\n# If the issue is reproduced from either the Support lab AP or the customer AP(new guest client joins),\nPlease share the Kibana link with the timestamp and the customer's GUI view.\n\n\nThanks!",
                                "created": "2025-03-28T23:23:22.173-0700",
                                "id": "2790027",
                                "jsdPublic": True,
                                "self": "https://ruckus.atlassian.net/rest/api/2/issue/317008/comment/2790027",
                                "updateAuthor": {
                                    "accountId": "712020:d33662dd-7b1d-4cbb-8905-e7c9a5cc49f6",
                                    "accountType": "atlassian",
                                    "active": True,
                                    "avatarUrls": {
                                        "16x16": "https://secure.gravatar.com/avatar/8acd7ecda9b8e9c5e20c1d791b5d8671?d=https%3A%2F%2Favatar-management--avatars.us-west-2.prod.public.atl-paas.net%2Finitials%2FWE-5.png",
                                        "24x24": "https://secure.gravatar.com/avatar/8acd7ecda9b8e9c5e20c1d791b5d8671?d=https%3A%2F%2Favatar-management--avatars.us-west-2.prod.public.atl-paas.net%2Finitials%2FWE-5.png",
                                        "32x32": "https://secure.gravatar.com/avatar/8acd7ecda9b8e9c5e20c1d791b5d8671?d=https%3A%2F%2Favatar-management--avatars.us-west-2.prod.public.atl-paas.net%2Finitials%2FWE-5.png",
                                        "48x48": "https://secure.gravatar.com/avatar/8acd7ecda9b8e9c5e20c1d791b5d8671?d=https%3A%2F%2Favatar-management--avatars.us-west-2.prod.public.atl-paas.net%2Finitials%2FWE-5.png"
                                    },
                                    "displayName": "Wu, Eric",
                                    "emailAddress": "eric.wu@commscope.com",
                                    "self": "https://ruckus.atlassian.net/rest/api/2/user?accountId=712020%3Ad33662dd-7b1d-4cbb-8905-e7c9a5cc49f6",
                                    "timeZone": "America/Los_Angeles"
                                },
                                "updated": "2025-03-28T23:23:22.173-0700"
                            },
                            {
                                "author": {
                                    "accountId": "712020:f85b2370-dba7-49c7-9733-7243dcd25af7",
                                    "accountType": "atlassian",
                                    "active": True,
                                    "avatarUrls": {
                                        "16x16": "https://secure.gravatar.com/avatar/67b44b9ab907929dae90a026d9fb178e?d=https%3A%2F%2Favatar-management--avatars.us-west-2.prod.public.atl-paas.net%2Finitials%2FJP-0.png",
                                        "24x24": "https://secure.gravatar.com/avatar/67b44b9ab907929dae90a026d9fb178e?d=https%3A%2F%2Favatar-management--avatars.us-west-2.prod.public.atl-paas.net%2Finitials%2FJP-0.png",
                                        "32x32": "https://secure.gravatar.com/avatar/67b44b9ab907929dae90a026d9fb178e?d=https%3A%2F%2Favatar-management--avatars.us-west-2.prod.public.atl-paas.net%2Finitials%2FJP-0.png",
                                        "48x48": "https://secure.gravatar.com/avatar/67b44b9ab907929dae90a026d9fb178e?d=https%3A%2F%2Favatar-management--avatars.us-west-2.prod.public.atl-paas.net%2Finitials%2FJP-0.png"
                                    },
                                    "displayName": "Jacob, Praveen",
                                    "emailAddress": "praveen.jacob@commscope.com",
                                    "self": "https://ruckus.atlassian.net/rest/api/2/user?accountId=712020%3Af85b2370-dba7-49c7-9733-7243dcd25af7",
                                    "timeZone": "America/Los_Angeles"
                                },
                                "body": "Hi [~accountid:712020:d33662dd-7b1d-4cbb-8905-e7c9a5cc49f6], \n\nLet me request the customer to allow us to add 2 APs.\n\nThanks,\n\nPraveen. J ",
                                "created": "2025-04-01T09:29:56.825-0700",
                                "id": "2791868",
                                "jsdPublic": True,
                                "self": "https://ruckus.atlassian.net/rest/api/2/issue/317008/comment/2791868",
                                "updateAuthor": {
                                    "accountId": "712020:f85b2370-dba7-49c7-9733-7243dcd25af7",
                                    "accountType": "atlassian",
                                    "active": True,
                                    "avatarUrls": {
                                        "16x16": "https://secure.gravatar.com/avatar/67b44b9ab907929dae90a026d9fb178e?d=https%3A%2F%2Favatar-management--avatars.us-west-2.prod.public.atl-paas.net%2Finitials%2FJP-0.png",
                                        "24x24": "https://secure.gravatar.com/avatar/67b44b9ab907929dae90a026d9fb178e?d=https%3A%2F%2Favatar-management--avatars.us-west-2.prod.public.atl-paas.net%2Finitials%2FJP-0.png",
                                        "32x32": "https://secure.gravatar.com/avatar/67b44b9ab907929dae90a026d9fb178e?d=https%3A%2F%2Favatar-management--avatars.us-west-2.prod.public.atl-paas.net%2Finitials%2FJP-0.png",
                                        "48x48": "https://secure.gravatar.com/avatar/67b44b9ab907929dae90a026d9fb178e?d=https%3A%2F%2Favatar-management--avatars.us-west-2.prod.public.atl-paas.net%2Finitials%2FJP-0.png"
                                    },
                                    "displayName": "Jacob, Praveen",
                                    "emailAddress": "praveen.jacob@commscope.com",
                                    "self": "https://ruckus.atlassian.net/rest/api/2/user?accountId=712020%3Af85b2370-dba7-49c7-9733-7243dcd25af7",
                                    "timeZone": "America/Los_Angeles"
                                },
                                "updated": "2025-04-01T09:29:56.825-0700"
                            },
                            {
                                "author": {
                                    "accountId": "712020:d33662dd-7b1d-4cbb-8905-e7c9a5cc49f6",
                                    "accountType": "atlassian",
                                    "active": True,
                                    "avatarUrls": {
                                        "16x16": "https://secure.gravatar.com/avatar/8acd7ecda9b8e9c5e20c1d791b5d8671?d=https%3A%2F%2Favatar-management--avatars.us-west-2.prod.public.atl-paas.net%2Finitials%2FWE-5.png",
                                        "24x24": "https://secure.gravatar.com/avatar/8acd7ecda9b8e9c5e20c1d791b5d8671?d=https%3A%2F%2Favatar-management--avatars.us-west-2.prod.public.atl-paas.net%2Finitials%2FWE-5.png",
                                        "32x32": "https://secure.gravatar.com/avatar/8acd7ecda9b8e9c5e20c1d791b5d8671?d=https%3A%2F%2Favatar-management--avatars.us-west-2.prod.public.atl-paas.net%2Finitials%2FWE-5.png",
                                        "48x48": "https://secure.gravatar.com/avatar/8acd7ecda9b8e9c5e20c1d791b5d8671?d=https%3A%2F%2Favatar-management--avatars.us-west-2.prod.public.atl-paas.net%2Finitials%2FWE-5.png"
                                    },
                                    "displayName": "Wu, Eric",
                                    "emailAddress": "eric.wu@commscope.com",
                                    "self": "https://ruckus.atlassian.net/rest/api/2/user?accountId=712020%3Ad33662dd-7b1d-4cbb-8905-e7c9a5cc49f6",
                                    "timeZone": "America/Los_Angeles"
                                },
                                "body": "Hi [~accountid:712020:f85b2370-dba7-49c7-9733-7243dcd25af7]  ,\n\nwould like to check the issue is reproducible through the Support lab AP using the customer tenant, \n\nor if it's only occurring on the customer's AP+client ?\n\nThanks!",
                                "created": "2025-04-03T09:30:20.582-0700",
                                "id": "2793251",
                                "jsdPublic": True,
                                "self": "https://ruckus.atlassian.net/rest/api/2/issue/317008/comment/2793251",
                                "updateAuthor": {
                                    "accountId": "712020:d33662dd-7b1d-4cbb-8905-e7c9a5cc49f6",
                                    "accountType": "atlassian",
                                    "active": True,
                                    "avatarUrls": {
                                        "16x16": "https://secure.gravatar.com/avatar/8acd7ecda9b8e9c5e20c1d791b5d8671?d=https%3A%2F%2Favatar-management--avatars.us-west-2.prod.public.atl-paas.net%2Finitials%2FWE-5.png",
                                        "24x24": "https://secure.gravatar.com/avatar/8acd7ecda9b8e9c5e20c1d791b5d8671?d=https%3A%2F%2Favatar-management--avatars.us-west-2.prod.public.atl-paas.net%2Finitials%2FWE-5.png",
                                        "32x32": "https://secure.gravatar.com/avatar/8acd7ecda9b8e9c5e20c1d791b5d8671?d=https%3A%2F%2Favatar-management--avatars.us-west-2.prod.public.atl-paas.net%2Finitials%2FWE-5.png",
                                        "48x48": "https://secure.gravatar.com/avatar/8acd7ecda9b8e9c5e20c1d791b5d8671?d=https%3A%2F%2Favatar-management--avatars.us-west-2.prod.public.atl-paas.net%2Finitials%2FWE-5.png"
                                    },
                                    "displayName": "Wu, Eric",
                                    "emailAddress": "eric.wu@commscope.com",
                                    "self": "https://ruckus.atlassian.net/rest/api/2/user?accountId=712020%3Ad33662dd-7b1d-4cbb-8905-e7c9a5cc49f6",
                                    "timeZone": "America/Los_Angeles"
                                },
                                "updated": "2025-04-03T09:30:20.582-0700"
                            },
                            {
                                "author": {
                                    "accountId": "712020:f85b2370-dba7-49c7-9733-7243dcd25af7",
                                    "accountType": "atlassian",
                                    "active": True,
                                    "avatarUrls": {
                                        "16x16": "https://secure.gravatar.com/avatar/67b44b9ab907929dae90a026d9fb178e?d=https%3A%2F%2Favatar-management--avatars.us-west-2.prod.public.atl-paas.net%2Finitials%2FJP-0.png",
                                        "24x24": "https://secure.gravatar.com/avatar/67b44b9ab907929dae90a026d9fb178e?d=https%3A%2F%2Favatar-management--avatars.us-west-2.prod.public.atl-paas.net%2Finitials%2FJP-0.png",
                                        "32x32": "https://secure.gravatar.com/avatar/67b44b9ab907929dae90a026d9fb178e?d=https%3A%2F%2Favatar-management--avatars.us-west-2.prod.public.atl-paas.net%2Finitials%2FJP-0.png",
                                        "48x48": "https://secure.gravatar.com/avatar/67b44b9ab907929dae90a026d9fb178e?d=https%3A%2F%2Favatar-management--avatars.us-west-2.prod.public.atl-paas.net%2Finitials%2FJP-0.png"
                                    },
                                    "displayName": "Jacob, Praveen",
                                    "emailAddress": "praveen.jacob@commscope.com",
                                    "self": "https://ruckus.atlassian.net/rest/api/2/user?accountId=712020%3Af85b2370-dba7-49c7-9733-7243dcd25af7",
                                    "timeZone": "America/Los_Angeles"
                                },
                                "body": "Hi [~accountid:712020:d33662dd-7b1d-4cbb-8905-e7c9a5cc49f6],\n\nCustomer has just provided his permission to add our APs to his tenant. \n\nI will add the AP and keep you posted on the test. \n\nThanks,\n\nPraveen. J ",
                                "created": "2025-04-04T10:00:36.361-0700",
                                "id": "2793693",
                                "jsdPublic": True,
                                "self": "https://ruckus.atlassian.net/rest/api/2/issue/317008/comment/2793693",
                                "updateAuthor": {
                                    "accountId": "712020:f85b2370-dba7-49c7-9733-7243dcd25af7",
                                    "accountType": "atlassian",
                                    "active": True,
                                    "avatarUrls": {
                                        "16x16": "https://secure.gravatar.com/avatar/67b44b9ab907929dae90a026d9fb178e?d=https%3A%2F%2Favatar-management--avatars.us-west-2.prod.public.atl-paas.net%2Finitials%2FJP-0.png",
                                        "24x24": "https://secure.gravatar.com/avatar/67b44b9ab907929dae90a026d9fb178e?d=https%3A%2F%2Favatar-management--avatars.us-west-2.prod.public.atl-paas.net%2Finitials%2FJP-0.png",
                                        "32x32": "https://secure.gravatar.com/avatar/67b44b9ab907929dae90a026d9fb178e?d=https%3A%2F%2Favatar-management--avatars.us-west-2.prod.public.atl-paas.net%2Finitials%2FJP-0.png",
                                        "48x48": "https://secure.gravatar.com/avatar/67b44b9ab907929dae90a026d9fb178e?d=https%3A%2F%2Favatar-management--avatars.us-west-2.prod.public.atl-paas.net%2Finitials%2FJP-0.png"
                                    },
                                    "displayName": "Jacob, Praveen",
                                    "emailAddress": "praveen.jacob@commscope.com",
                                    "self": "https://ruckus.atlassian.net/rest/api/2/user?accountId=712020%3Af85b2370-dba7-49c7-9733-7243dcd25af7",
                                    "timeZone": "America/Los_Angeles"
                                },
                                "updated": "2025-04-04T10:00:36.361-0700"
                            },
                            {
                                "author": {
                                    "accountId": "712020:f85b2370-dba7-49c7-9733-7243dcd25af7",
                                    "accountType": "atlassian",
                                    "active": True,
                                    "avatarUrls": {
                                        "16x16": "https://secure.gravatar.com/avatar/67b44b9ab907929dae90a026d9fb178e?d=https%3A%2F%2Favatar-management--avatars.us-west-2.prod.public.atl-paas.net%2Finitials%2FJP-0.png",
                                        "24x24": "https://secure.gravatar.com/avatar/67b44b9ab907929dae90a026d9fb178e?d=https%3A%2F%2Favatar-management--avatars.us-west-2.prod.public.atl-paas.net%2Finitials%2FJP-0.png",
                                        "32x32": "https://secure.gravatar.com/avatar/67b44b9ab907929dae90a026d9fb178e?d=https%3A%2F%2Favatar-management--avatars.us-west-2.prod.public.atl-paas.net%2Finitials%2FJP-0.png",
                                        "48x48": "https://secure.gravatar.com/avatar/67b44b9ab907929dae90a026d9fb178e?d=https%3A%2F%2Favatar-management--avatars.us-west-2.prod.public.atl-paas.net%2Finitials%2FJP-0.png"
                                    },
                                    "displayName": "Jacob, Praveen",
                                    "emailAddress": "praveen.jacob@commscope.com",
                                    "self": "https://ruckus.atlassian.net/rest/api/2/user?accountId=712020%3Af85b2370-dba7-49c7-9733-7243dcd25af7",
                                    "timeZone": "America/Los_Angeles"
                                },
                                "body": "Hi [~accountid:712020:d33662dd-7b1d-4cbb-8905-e7c9a5cc49f6], \n\nI noticed that the phenomenon of the same time being shown for Guest Created' and ‘Guest Expires’ is seen only when the concerned Guest device is in an ‘Unauthorized’ state. \n\nI have tested this with two difference wireless clients and their MAC addresses are:  *00:c0:ca:ac:2e:f6* & *00:c0:ca:ac:2e:f5*. This can be seen in the two screenshots below. \n\n!image-20250407-175339.png|width=624,height=329,alt=\"image-20250407-175339.png\"!\n\n!image-20250407-175358.png|width=624,height=327,alt=\"image-20250407-175358.png\"!\n\nHowever, when both clients are authorized, their details are as expected as it should be. Please see the working screenshots below. \n\n!image-20250407-175512.png|width=624,height=326,alt=\"image-20250407-175512.png\"!\n\n!image-20250407-175606.png|width=624,height=327,alt=\"image-20250407-175606.png\"!\n\nKibana logs with Session Manager debug are available here: \n\n[https://logs.int.cloud.ruckuswireless.com/s/alto-eu/goto/d9eda7a82b5b97fc8635f2e3b2045de1|https://logs.int.cloud.ruckuswireless.com/s/alto-eu/goto/d9eda7a82b5b97fc8635f2e3b2045de1]\n\n[https://logs.int.cloud.ruckuswireless.com/s/alto-eu/goto/fa5227fa47424f30df7b627b6efe7dfb|https://logs.int.cloud.ruckuswireless.com/s/alto-eu/goto/fa5227fa47424f30df7b627b6efe7dfb]\n\n[https://logs.int.cloud.ruckuswireless.com/s/alto-eu/goto/0b37b06e0688a4a1d6ba0b27a5f7d1a2|https://logs.int.cloud.ruckuswireless.com/s/alto-eu/goto/0b37b06e0688a4a1d6ba0b27a5f7d1a2]\n\nAP Support log files: Are also attached. \n\n+*Note:*+ I believe we only need to explain if it makes sense to show the same timestamp for ‘Guest Created’ and ‘Guest Expires’ for unauthorized clients. \n\nThanks,\n\nPraveen. J",
                                "created": "2025-04-07T10:58:59.032-0700",
                                "id": "2794557",
                                "jsdPublic": True,
                                "self": "https://ruckus.atlassian.net/rest/api/2/issue/317008/comment/2794557",
                                "updateAuthor": {
                                    "accountId": "712020:f85b2370-dba7-49c7-9733-7243dcd25af7",
                                    "accountType": "atlassian",
                                    "active": True,
                                    "avatarUrls": {
                                        "16x16": "https://secure.gravatar.com/avatar/67b44b9ab907929dae90a026d9fb178e?d=https%3A%2F%2Favatar-management--avatars.us-west-2.prod.public.atl-paas.net%2Finitials%2FJP-0.png",
                                        "24x24": "https://secure.gravatar.com/avatar/67b44b9ab907929dae90a026d9fb178e?d=https%3A%2F%2Favatar-management--avatars.us-west-2.prod.public.atl-paas.net%2Finitials%2FJP-0.png",
                                        "32x32": "https://secure.gravatar.com/avatar/67b44b9ab907929dae90a026d9fb178e?d=https%3A%2F%2Favatar-management--avatars.us-west-2.prod.public.atl-paas.net%2Finitials%2FJP-0.png",
                                        "48x48": "https://secure.gravatar.com/avatar/67b44b9ab907929dae90a026d9fb178e?d=https%3A%2F%2Favatar-management--avatars.us-west-2.prod.public.atl-paas.net%2Finitials%2FJP-0.png"
                                    },
                                    "displayName": "Jacob, Praveen",
                                    "emailAddress": "praveen.jacob@commscope.com",
                                    "self": "https://ruckus.atlassian.net/rest/api/2/user?accountId=712020%3Af85b2370-dba7-49c7-9733-7243dcd25af7",
                                    "timeZone": "America/Los_Angeles"
                                },
                                "updated": "2025-04-07T10:58:59.032-0700"
                            },
                            {
                                "author": {
                                    "accountId": "712020:d33662dd-7b1d-4cbb-8905-e7c9a5cc49f6",
                                    "accountType": "atlassian",
                                    "active": True,
                                    "avatarUrls": {
                                        "16x16": "https://secure.gravatar.com/avatar/8acd7ecda9b8e9c5e20c1d791b5d8671?d=https%3A%2F%2Favatar-management--avatars.us-west-2.prod.public.atl-paas.net%2Finitials%2FWE-5.png",
                                        "24x24": "https://secure.gravatar.com/avatar/8acd7ecda9b8e9c5e20c1d791b5d8671?d=https%3A%2F%2Favatar-management--avatars.us-west-2.prod.public.atl-paas.net%2Finitials%2FWE-5.png",
                                        "32x32": "https://secure.gravatar.com/avatar/8acd7ecda9b8e9c5e20c1d791b5d8671?d=https%3A%2F%2Favatar-management--avatars.us-west-2.prod.public.atl-paas.net%2Finitials%2FWE-5.png",
                                        "48x48": "https://secure.gravatar.com/avatar/8acd7ecda9b8e9c5e20c1d791b5d8671?d=https%3A%2F%2Favatar-management--avatars.us-west-2.prod.public.atl-paas.net%2Finitials%2FWE-5.png"
                                    },
                                    "displayName": "Wu, Eric",
                                    "emailAddress": "eric.wu@commscope.com",
                                    "self": "https://ruckus.atlassian.net/rest/api/2/user?accountId=712020%3Ad33662dd-7b1d-4cbb-8905-e7c9a5cc49f6",
                                    "timeZone": "America/Los_Angeles"
                                },
                                "body": "Hi [~accountid:712020:f85b2370-dba7-49c7-9733-7243dcd25af7] \n\nThanks for the info.\n\n\n\n(non-working case)\non this customer side, a few clients which might hit the corner case that  \n\n\"authorized\" state with \"the same Guest Created and Expires timestamps\"\n\n\n\n(working case)\n1.\nEET AP + clients under dogfooder tenant in the former comment\n\n2.\n\nSupport AP + clients (00:c0:ca:ac:2e:f6 & 00:c0:ca:ac:2e:f5) under the customer tenant \"ebb3238545f64af78a05504e2b470a35\"\n\nboth #1 and #2 were\n\"unauthorized\" state with \"the same Guest Created and Expires timestamps\"\n\"authorized\"     state with \"actual Guest Created and Expires timestamps\"\n\n\n\n[next action item]\nSince the issue could not be consistently reproduced across multiple device combinations,\n\nthe proposed next step would be a potential enhancement [https://ruckus.atlassian.net/browse/ACX-83183|https://ruckus.atlassian.net/browse/ACX-83183|smart-link] to improve clarity in GUI:\n\n\"unauthorized\" state which should display empty timestamps when actual values are not yet available.\n\nPlease note that \n\n1.\n\nThis is a non-blocking display enhancement, and would not be considered for urgent fix and would go with RBOM flow.\n\n2.\n\nPlease help to keep monitoring whether the non-working case can be reproduced within the next two days.\n\nIf reproducible, please ensure that:\n\n* EU Durga has enabled \"session-manager\" at INFO level for this customer tenant\n* The INFO log is observable in EU Kibana\n* AP debug log is collected\n\n\n\nIf not reproducible, \nwe would proceed to resolve [https://ruckus.atlassian.net/browse/ER-14520|https://ruckus.atlassian.net/browse/ER-14520|smart-link] in two days, \n\nas the display enhancement would be scheduled through the RBOM flow.\n\n\n\nThanks!",
                                "created": "2025-04-07T14:32:56.944-0700",
                                "id": "2794628",
                                "jsdPublic": True,
                                "self": "https://ruckus.atlassian.net/rest/api/2/issue/317008/comment/2794628",
                                "updateAuthor": {
                                    "accountId": "712020:d33662dd-7b1d-4cbb-8905-e7c9a5cc49f6",
                                    "accountType": "atlassian",
                                    "active": True,
                                    "avatarUrls": {
                                        "16x16": "https://secure.gravatar.com/avatar/8acd7ecda9b8e9c5e20c1d791b5d8671?d=https%3A%2F%2Favatar-management--avatars.us-west-2.prod.public.atl-paas.net%2Finitials%2FWE-5.png",
                                        "24x24": "https://secure.gravatar.com/avatar/8acd7ecda9b8e9c5e20c1d791b5d8671?d=https%3A%2F%2Favatar-management--avatars.us-west-2.prod.public.atl-paas.net%2Finitials%2FWE-5.png",
                                        "32x32": "https://secure.gravatar.com/avatar/8acd7ecda9b8e9c5e20c1d791b5d8671?d=https%3A%2F%2Favatar-management--avatars.us-west-2.prod.public.atl-paas.net%2Finitials%2FWE-5.png",
                                        "48x48": "https://secure.gravatar.com/avatar/8acd7ecda9b8e9c5e20c1d791b5d8671?d=https%3A%2F%2Favatar-management--avatars.us-west-2.prod.public.atl-paas.net%2Finitials%2FWE-5.png"
                                    },
                                    "displayName": "Wu, Eric",
                                    "emailAddress": "eric.wu@commscope.com",
                                    "self": "https://ruckus.atlassian.net/rest/api/2/user?accountId=712020%3Ad33662dd-7b1d-4cbb-8905-e7c9a5cc49f6",
                                    "timeZone": "America/Los_Angeles"
                                },
                                "updated": "2025-04-07T14:39:31.151-0700"
                            },
                            {
                                "author": {
                                    "accountId": "712020:f85b2370-dba7-49c7-9733-7243dcd25af7",
                                    "accountType": "atlassian",
                                    "active": True,
                                    "avatarUrls": {
                                        "16x16": "https://secure.gravatar.com/avatar/67b44b9ab907929dae90a026d9fb178e?d=https%3A%2F%2Favatar-management--avatars.us-west-2.prod.public.atl-paas.net%2Finitials%2FJP-0.png",
                                        "24x24": "https://secure.gravatar.com/avatar/67b44b9ab907929dae90a026d9fb178e?d=https%3A%2F%2Favatar-management--avatars.us-west-2.prod.public.atl-paas.net%2Finitials%2FJP-0.png",
                                        "32x32": "https://secure.gravatar.com/avatar/67b44b9ab907929dae90a026d9fb178e?d=https%3A%2F%2Favatar-management--avatars.us-west-2.prod.public.atl-paas.net%2Finitials%2FJP-0.png",
                                        "48x48": "https://secure.gravatar.com/avatar/67b44b9ab907929dae90a026d9fb178e?d=https%3A%2F%2Favatar-management--avatars.us-west-2.prod.public.atl-paas.net%2Finitials%2FJP-0.png"
                                    },
                                    "displayName": "Jacob, Praveen",
                                    "emailAddress": "praveen.jacob@commscope.com",
                                    "self": "https://ruckus.atlassian.net/rest/api/2/user?accountId=712020%3Af85b2370-dba7-49c7-9733-7243dcd25af7",
                                    "timeZone": "America/Los_Angeles"
                                },
                                "body": "Hi [~accountid:712020:d33662dd-7b1d-4cbb-8905-e7c9a5cc49f6],\n\nI have reviewed a bunch of clients and so far keeping with the latest findings only unauthorized users are seeing the same timestamps for both ‘Guest Created’ and ‘Guest Expires’. \n\nI will keep monitoring for the next couple of days. \n\nWhat would be the tentative for this RBOM?\n\nThanks,\n\nPraveen. J ",
                                "created": "2025-04-08T09:26:49.249-0700",
                                "id": "2795309",
                                "jsdPublic": True,
                                "self": "https://ruckus.atlassian.net/rest/api/2/issue/317008/comment/2795309",
                                "updateAuthor": {
                                    "accountId": "712020:f85b2370-dba7-49c7-9733-7243dcd25af7",
                                    "accountType": "atlassian",
                                    "active": True,
                                    "avatarUrls": {
                                        "16x16": "https://secure.gravatar.com/avatar/67b44b9ab907929dae90a026d9fb178e?d=https%3A%2F%2Favatar-management--avatars.us-west-2.prod.public.atl-paas.net%2Finitials%2FJP-0.png",
                                        "24x24": "https://secure.gravatar.com/avatar/67b44b9ab907929dae90a026d9fb178e?d=https%3A%2F%2Favatar-management--avatars.us-west-2.prod.public.atl-paas.net%2Finitials%2FJP-0.png",
                                        "32x32": "https://secure.gravatar.com/avatar/67b44b9ab907929dae90a026d9fb178e?d=https%3A%2F%2Favatar-management--avatars.us-west-2.prod.public.atl-paas.net%2Finitials%2FJP-0.png",
                                        "48x48": "https://secure.gravatar.com/avatar/67b44b9ab907929dae90a026d9fb178e?d=https%3A%2F%2Favatar-management--avatars.us-west-2.prod.public.atl-paas.net%2Finitials%2FJP-0.png"
                                    },
                                    "displayName": "Jacob, Praveen",
                                    "emailAddress": "praveen.jacob@commscope.com",
                                    "self": "https://ruckus.atlassian.net/rest/api/2/user?accountId=712020%3Af85b2370-dba7-49c7-9733-7243dcd25af7",
                                    "timeZone": "America/Los_Angeles"
                                },
                                "updated": "2025-04-08T09:26:49.249-0700"
                            },
                            {
                                "author": {
                                    "accountId": "712020:aae798e1-d04c-4d36-b994-9e311c230698",
                                    "accountType": "atlassian",
                                    "active": True,
                                    "avatarUrls": {
                                        "16x16": "https://secure.gravatar.com/avatar/a7480b50b7b3fa44e9adad9ac1775143?d=https%3A%2F%2Favatar-management--avatars.us-west-2.prod.public.atl-paas.net%2Finitials%2FLP-5.png",
                                        "24x24": "https://secure.gravatar.com/avatar/a7480b50b7b3fa44e9adad9ac1775143?d=https%3A%2F%2Favatar-management--avatars.us-west-2.prod.public.atl-paas.net%2Finitials%2FLP-5.png",
                                        "32x32": "https://secure.gravatar.com/avatar/a7480b50b7b3fa44e9adad9ac1775143?d=https%3A%2F%2Favatar-management--avatars.us-west-2.prod.public.atl-paas.net%2Finitials%2FLP-5.png",
                                        "48x48": "https://secure.gravatar.com/avatar/a7480b50b7b3fa44e9adad9ac1775143?d=https%3A%2F%2Favatar-management--avatars.us-west-2.prod.public.atl-paas.net%2Finitials%2FLP-5.png"
                                    },
                                    "displayName": "Lumos, Paul",
                                    "emailAddress": "paul.lumos@commscope.com",
                                    "self": "https://ruckus.atlassian.net/rest/api/2/user?accountId=712020%3Aaae798e1-d04c-4d36-b994-9e311c230698",
                                    "timeZone": "America/Los_Angeles"
                                },
                                "body": "Per [https://ruckus.atlassian.net/browse/ACX-79018|https://ruckus.atlassian.net/browse/ACX-79018|smart-link] ACX-UI 65793 is the fix.  Current acx-ui build is 68188.\nIs this issue resolved?",
                                "created": "2025-04-08T09:51:58.123-0700",
                                "id": "2795323",
                                "jsdPublic": True,
                                "self": "https://ruckus.atlassian.net/rest/api/2/issue/317008/comment/2795323",
                                "updateAuthor": {
                                    "accountId": "712020:aae798e1-d04c-4d36-b994-9e311c230698",
                                    "accountType": "atlassian",
                                    "active": True,
                                    "avatarUrls": {
                                        "16x16": "https://secure.gravatar.com/avatar/a7480b50b7b3fa44e9adad9ac1775143?d=https%3A%2F%2Favatar-management--avatars.us-west-2.prod.public.atl-paas.net%2Finitials%2FLP-5.png",
                                        "24x24": "https://secure.gravatar.com/avatar/a7480b50b7b3fa44e9adad9ac1775143?d=https%3A%2F%2Favatar-management--avatars.us-west-2.prod.public.atl-paas.net%2Finitials%2FLP-5.png",
                                        "32x32": "https://secure.gravatar.com/avatar/a7480b50b7b3fa44e9adad9ac1775143?d=https%3A%2F%2Favatar-management--avatars.us-west-2.prod.public.atl-paas.net%2Finitials%2FLP-5.png",
                                        "48x48": "https://secure.gravatar.com/avatar/a7480b50b7b3fa44e9adad9ac1775143?d=https%3A%2F%2Favatar-management--avatars.us-west-2.prod.public.atl-paas.net%2Finitials%2FLP-5.png"
                                    },
                                    "displayName": "Lumos, Paul",
                                    "emailAddress": "paul.lumos@commscope.com",
                                    "self": "https://ruckus.atlassian.net/rest/api/2/user?accountId=712020%3Aaae798e1-d04c-4d36-b994-9e311c230698",
                                    "timeZone": "America/Los_Angeles"
                                },
                                "updated": "2025-04-08T09:51:58.123-0700"
                            },
                            {
                                "author": {
                                    "accountId": "712020:d33662dd-7b1d-4cbb-8905-e7c9a5cc49f6",
                                    "accountType": "atlassian",
                                    "active": True,
                                    "avatarUrls": {
                                        "16x16": "https://secure.gravatar.com/avatar/8acd7ecda9b8e9c5e20c1d791b5d8671?d=https%3A%2F%2Favatar-management--avatars.us-west-2.prod.public.atl-paas.net%2Finitials%2FWE-5.png",
                                        "24x24": "https://secure.gravatar.com/avatar/8acd7ecda9b8e9c5e20c1d791b5d8671?d=https%3A%2F%2Favatar-management--avatars.us-west-2.prod.public.atl-paas.net%2Finitials%2FWE-5.png",
                                        "32x32": "https://secure.gravatar.com/avatar/8acd7ecda9b8e9c5e20c1d791b5d8671?d=https%3A%2F%2Favatar-management--avatars.us-west-2.prod.public.atl-paas.net%2Finitials%2FWE-5.png",
                                        "48x48": "https://secure.gravatar.com/avatar/8acd7ecda9b8e9c5e20c1d791b5d8671?d=https%3A%2F%2Favatar-management--avatars.us-west-2.prod.public.atl-paas.net%2Finitials%2FWE-5.png"
                                    },
                                    "displayName": "Wu, Eric",
                                    "emailAddress": "eric.wu@commscope.com",
                                    "self": "https://ruckus.atlassian.net/rest/api/2/user?accountId=712020%3Ad33662dd-7b1d-4cbb-8905-e7c9a5cc49f6",
                                    "timeZone": "America/Los_Angeles"
                                },
                                "body": "Hi Praveen, Paul,\n\nThanks for checking in.\n\n\n\n[Resolved Bug]\n\n[https://ruckus.atlassian.net/browse/ACX-79018|https://ruckus.atlassian.net/browse/ACX-79018|smart-link] \n\nhas helped address partial display issues by falling back to MAC address when the username does not match, allowing the client reported by AP to still be identified.\n\n\n\nHowever, there is still another display concern where clients in the \"unauthorized\" state show identical \"Guest Created\" and \"Expires\" timestamps, \n\nwhich requires the following GUI enhancement\n\n[GUI Enhancement]\n\n[https://ruckus.atlassian.net/browse/ACX-83183|https://ruckus.atlassian.net/browse/ACX-83183|smart-link]\n\n\n\nSince the last enhancement is primarily intended to improve GUI clarity \n\nby replacing potentially misleading \"Guest Created\" and \"Expires\" timestamps for unauthorized guests with empty values,\n\n\n\nit does not affect core functionality and is not considered a blocking issue for this *ER-14520*.\n\nThe RBOM ETA will depend on resource scheduling by the DEV team\n\nC.C. [~accountid:712020:51db05f0-216a-474e-b47e-e789b96b019d] \n\n\n\nThis *ER-14520* is expected to be resolved soon.\n\nThanks!",
                                "created": "2025-04-08T10:17:57.390-0700",
                                "id": "2795327",
                                "jsdPublic": True,
                                "self": "https://ruckus.atlassian.net/rest/api/2/issue/317008/comment/2795327",
                                "updateAuthor": {
                                    "accountId": "712020:d33662dd-7b1d-4cbb-8905-e7c9a5cc49f6",
                                    "accountType": "atlassian",
                                    "active": True,
                                    "avatarUrls": {
                                        "16x16": "https://secure.gravatar.com/avatar/8acd7ecda9b8e9c5e20c1d791b5d8671?d=https%3A%2F%2Favatar-management--avatars.us-west-2.prod.public.atl-paas.net%2Finitials%2FWE-5.png",
                                        "24x24": "https://secure.gravatar.com/avatar/8acd7ecda9b8e9c5e20c1d791b5d8671?d=https%3A%2F%2Favatar-management--avatars.us-west-2.prod.public.atl-paas.net%2Finitials%2FWE-5.png",
                                        "32x32": "https://secure.gravatar.com/avatar/8acd7ecda9b8e9c5e20c1d791b5d8671?d=https%3A%2F%2Favatar-management--avatars.us-west-2.prod.public.atl-paas.net%2Finitials%2FWE-5.png",
                                        "48x48": "https://secure.gravatar.com/avatar/8acd7ecda9b8e9c5e20c1d791b5d8671?d=https%3A%2F%2Favatar-management--avatars.us-west-2.prod.public.atl-paas.net%2Finitials%2FWE-5.png"
                                    },
                                    "displayName": "Wu, Eric",
                                    "emailAddress": "eric.wu@commscope.com",
                                    "self": "https://ruckus.atlassian.net/rest/api/2/user?accountId=712020%3Ad33662dd-7b1d-4cbb-8905-e7c9a5cc49f6",
                                    "timeZone": "America/Los_Angeles"
                                },
                                "updated": "2025-04-08T10:17:57.390-0700"
                            },
                            {
                                "author": {
                                    "accountId": "712020:d33662dd-7b1d-4cbb-8905-e7c9a5cc49f6",
                                    "accountType": "atlassian",
                                    "active": True,
                                    "avatarUrls": {
                                        "16x16": "https://secure.gravatar.com/avatar/8acd7ecda9b8e9c5e20c1d791b5d8671?d=https%3A%2F%2Favatar-management--avatars.us-west-2.prod.public.atl-paas.net%2Finitials%2FWE-5.png",
                                        "24x24": "https://secure.gravatar.com/avatar/8acd7ecda9b8e9c5e20c1d791b5d8671?d=https%3A%2F%2Favatar-management--avatars.us-west-2.prod.public.atl-paas.net%2Finitials%2FWE-5.png",
                                        "32x32": "https://secure.gravatar.com/avatar/8acd7ecda9b8e9c5e20c1d791b5d8671?d=https%3A%2F%2Favatar-management--avatars.us-west-2.prod.public.atl-paas.net%2Finitials%2FWE-5.png",
                                        "48x48": "https://secure.gravatar.com/avatar/8acd7ecda9b8e9c5e20c1d791b5d8671?d=https%3A%2F%2Favatar-management--avatars.us-west-2.prod.public.atl-paas.net%2Finitials%2FWE-5.png"
                                    },
                                    "displayName": "Wu, Eric",
                                    "emailAddress": "eric.wu@commscope.com",
                                    "self": "https://ruckus.atlassian.net/rest/api/2/user?accountId=712020%3Ad33662dd-7b1d-4cbb-8905-e7c9a5cc49f6",
                                    "timeZone": "America/Los_Angeles"
                                },
                                "body": "The latest GUI enhancement ACX-83183 is currently under code review and planned for completion by 04/15/25.\r\n\r\nETA for PROD to have RBOM of ACX-83183: Late April.\r\n\r\nSummary of the display change:\r\n\r\n[Before ACX-83183]\r\nWhen no available date in guest details,\r\nboth \"Guest Created\" and \"Expires\" timestamps default to the page access time.\r\n\r\n[After ACX-83183]\r\nWhen no available date in guest details, \r\nboth \"Guest Created\" and \"Expires\" timestamps will default to empty.",
                                "created": "2025-04-09T10:38:07.755-0700",
                                "id": "2796086",
                                "jsdPublic": True,
                                "self": "https://ruckus.atlassian.net/rest/api/2/issue/317008/comment/2796086",
                                "updateAuthor": {
                                    "accountId": "712020:d33662dd-7b1d-4cbb-8905-e7c9a5cc49f6",
                                    "accountType": "atlassian",
                                    "active": True,
                                    "avatarUrls": {
                                        "16x16": "https://secure.gravatar.com/avatar/8acd7ecda9b8e9c5e20c1d791b5d8671?d=https%3A%2F%2Favatar-management--avatars.us-west-2.prod.public.atl-paas.net%2Finitials%2FWE-5.png",
                                        "24x24": "https://secure.gravatar.com/avatar/8acd7ecda9b8e9c5e20c1d791b5d8671?d=https%3A%2F%2Favatar-management--avatars.us-west-2.prod.public.atl-paas.net%2Finitials%2FWE-5.png",
                                        "32x32": "https://secure.gravatar.com/avatar/8acd7ecda9b8e9c5e20c1d791b5d8671?d=https%3A%2F%2Favatar-management--avatars.us-west-2.prod.public.atl-paas.net%2Finitials%2FWE-5.png",
                                        "48x48": "https://secure.gravatar.com/avatar/8acd7ecda9b8e9c5e20c1d791b5d8671?d=https%3A%2F%2Favatar-management--avatars.us-west-2.prod.public.atl-paas.net%2Finitials%2FWE-5.png"
                                    },
                                    "displayName": "Wu, Eric",
                                    "emailAddress": "eric.wu@commscope.com",
                                    "self": "https://ruckus.atlassian.net/rest/api/2/user?accountId=712020%3Ad33662dd-7b1d-4cbb-8905-e7c9a5cc49f6",
                                    "timeZone": "America/Los_Angeles"
                                },
                                "updated": "2025-04-09T10:38:07.755-0700"
                            }
                        ],
                        "maxResults": 25,
                        "self": "https://ruckus.atlassian.net/rest/api/2/issue/317008/comment",
                        "startAt": 0,
                        "total": 25
                    },
                    "components": [
                        {
                            "id": "10875",
                            "name": "R1-UX/UI",
                            "self": "https://ruckus.atlassian.net/rest/api/2/component/10875"
                        }
                    ],
                    "created": "2025-02-25T05:32:09.716-0800",
                    "creator": {
                        "accountId": "712020:f85b2370-dba7-49c7-9733-7243dcd25af7",
                        "accountType": "atlassian",
                        "active": True,
                        "avatarUrls": {
                            "16x16": "https://secure.gravatar.com/avatar/67b44b9ab907929dae90a026d9fb178e?d=https%3A%2F%2Favatar-management--avatars.us-west-2.prod.public.atl-paas.net%2Finitials%2FJP-0.png",
                            "24x24": "https://secure.gravatar.com/avatar/67b44b9ab907929dae90a026d9fb178e?d=https%3A%2F%2Favatar-management--avatars.us-west-2.prod.public.atl-paas.net%2Finitials%2FJP-0.png",
                            "32x32": "https://secure.gravatar.com/avatar/67b44b9ab907929dae90a026d9fb178e?d=https%3A%2F%2Favatar-management--avatars.us-west-2.prod.public.atl-paas.net%2Finitials%2FJP-0.png",
                            "48x48": "https://secure.gravatar.com/avatar/67b44b9ab907929dae90a026d9fb178e?d=https%3A%2F%2Favatar-management--avatars.us-west-2.prod.public.atl-paas.net%2Finitials%2FJP-0.png"
                        },
                        "displayName": "Jacob, Praveen",
                        "emailAddress": "praveen.jacob@commscope.com",
                        "self": "https://ruckus.atlassian.net/rest/api/2/user?accountId=712020%3Af85b2370-dba7-49c7-9733-7243dcd25af7",
                        "timeZone": "America/Los_Angeles"
                    },
                    "customfield_10000": "{}",
                    "customfield_10001": None,
                    "customfield_10002": [],
                    "customfield_10003": None,
                    "customfield_10004": None,
                    "customfield_10005": None,
                    "customfield_10006": None,
                    "customfield_10007": None,
                    "customfield_10008": None,
                    "customfield_10009": None,
                    "customfield_10010": None,
                    "customfield_10014": None,
                    "customfield_10015": None,
                    "customfield_10016": None,
                    "customfield_10017": None,
                    "customfield_10018": {
                        "hasEpicLinkFieldDependency": False,
                        "nonEditableReason": {
                            "message": "To set an epic as the parent, use the epic link instead",
                            "reason": "EPIC_LINK_SHOULD_BE_USED"
                        },
                        "showField": False
                    },
                    "customfield_10019": "0|i1mjak:",
                    "customfield_10020": None,
                    "customfield_10021": None,
                    "customfield_10022": None,
                    "customfield_10023": None,
                    "customfield_10024": None,
                    "customfield_10025": None,
                    "customfield_10026": "2025-02-25T06:48:40.693-0800",
                    "customfield_10027": "1_*:*_3_*:*_25229564_*|*_10007_*:*_2_*:*_2283691294_*|*_3_*:*_2_*:*_465677047_*|*_4_*:*_1_*:*_7856518_*|*_5_*:*_1_*:*_946601501",
                    "customfield_10028": None,
                    "customfield_10029": None,
                    "customfield_10030": None,
                    "customfield_10031": None,
                    "customfield_10033": None,
                    "customfield_10034": None,
                    "customfield_10035": None,
                    "customfield_10036": None,
                    "customfield_10037": None,
                    "customfield_10038": None,
                    "customfield_10039": None,
                    "customfield_10072": {
                        "id": "11117",
                        "self": "https://ruckus.atlassian.net/rest/api/2/customFieldOption/11117",
                        "value": "Development"
                    },
                    "customfield_10073": {
                        "id": "11047",
                        "self": "https://ruckus.atlassian.net/rest/api/2/customFieldOption/11047",
                        "value": "S2 Major"
                    },
                    "customfield_10074": [
                        {
                            "archived": False,
                            "description": "",
                            "id": "10780",
                            "name": "Ruckus-One",
                            "released": False,
                            "self": "https://ruckus.atlassian.net/rest/api/2/version/10780"
                        }
                    ],
                    "customfield_10075": None,
                    "customfield_10076": [
                        {
                            "id": "10109",
                            "self": "https://ruckus.atlassian.net/rest/api/2/customFieldOption/10109",
                            "value": "Ruckus-One"
                        }
                    ],
                    "customfield_10077": None,
                    "customfield_10078": None,
                    "customfield_10079": {
                        "id": "10704",
                        "self": "https://ruckus.atlassian.net/rest/api/2/customFieldOption/10704",
                        "value": "P2"
                    },
                    "customfield_10080": None,
                    "customfield_10081": None,
                    "customfield_10082": None,
                    "customfield_10083": None,
                    "customfield_10084": None,
                    "customfield_10085": None,
                    "customfield_10086": None,
                    "customfield_10087": {
                        "id": "10940",
                        "self": "https://ruckus.atlassian.net/rest/api/2/customFieldOption/10940",
                        "value": "Yes"
                    },
                    "customfield_10088": None,
                    "customfield_10089": None,
                    "customfield_10090": "NA",
                    "customfield_10091": None,
                    "customfield_10092": None,
                    "customfield_10093": None,
                    "customfield_10094": None,
                    "customfield_10095": None,
                    "customfield_10096": None,
                    "customfield_10097": "Please update the information below before marking this issue as verified:\r\n1) Which functional behavior is changed?\r\n2) If new test cases required for this ER?\r\n3) Brief description for the test setup which is unique to this ER (for example, what tools is used, intra AP roaming setup etc)\r\n4) Summary for test procedure\r\n5) Does fix have some area of system performance impact?  ",
                    "customfield_10099": None,
                    "customfield_10100": {
                        "id": "10997",
                        "self": "https://ruckus.atlassian.net/rest/api/2/customFieldOption/10997",
                        "value": "No"
                    },
                    "customfield_10102": None,
                    "customfield_10103": None,
                    "customfield_10104": None,
                    "customfield_10105": None,
                    "customfield_10106": None,
                    "customfield_10107": None,
                    "customfield_10108": None,
                    "customfield_10109": None,
                    "customfield_10113": None,
                    "customfield_10114": None,
                    "customfield_10116": None,
                    "customfield_10118": {
                        "id": "11432",
                        "self": "https://ruckus.atlassian.net/rest/api/2/customFieldOption/11432",
                        "value": "Release Build"
                    },
                    "customfield_10119": None,
                    "customfield_10121": {
                        "id": "11356",
                        "self": "https://ruckus.atlassian.net/rest/api/2/customFieldOption/11356",
                        "value": "AP"
                    },
                    "customfield_10122": None,
                    "customfield_10124": {
                        "id": "11370",
                        "self": "https://ruckus.atlassian.net/rest/api/2/customFieldOption/11370",
                        "value": "NO"
                    },
                    "customfield_10125": None,
                    "customfield_10127": None,
                    "customfield_10129": None,
                    "customfield_10131": None,
                    "customfield_10132": None,
                    "customfield_10133": None,
                    "customfield_10134": "Required if WebUI is not supported",
                    "customfield_10135": None,
                    "customfield_10136": "Required if RESTConf is not supported",
                    "customfield_10137": None,
                    "customfield_10138": None,
                    "customfield_10139": None,
                    "customfield_10140": None,
                    "customfield_10142": {
                        "id": "11743",
                        "self": "https://ruckus.atlassian.net/rest/api/2/customFieldOption/11743",
                        "value": "No"
                    },
                    "customfield_10143": None,
                    "customfield_10144": None,
                    "customfield_10145": None,
                    "customfield_10146": None,
                    "customfield_10148": 0,
                    "customfield_10149": None,
                    "customfield_10150": {
                        "id": "11423",
                        "self": "https://ruckus.atlassian.net/rest/api/2/customFieldOption/11423",
                        "value": "NO"
                    },
                    "customfield_10151": None,
                    "customfield_10154": None,
                    "customfield_10155": 0,
                    "customfield_10156": None,
                    "customfield_10157": None,
                    "customfield_10158": {
                        "id": "11191",
                        "self": "https://ruckus.atlassian.net/rest/api/2/customFieldOption/11191",
                        "value": "False"
                    },
                    "customfield_10160": None,
                    "customfield_10161": {
                        "id": "11577",
                        "self": "https://ruckus.atlassian.net/rest/api/2/customFieldOption/11577",
                        "value": "N"
                    },
                    "customfield_10162": None,
                    "customfield_10163": None,
                    "customfield_10164": {
                        "id": "10451",
                        "self": "https://ruckus.atlassian.net/rest/api/2/customFieldOption/10451",
                        "value": "N"
                    },
                    "customfield_10165": [
                        {
                            "id": "11408",
                            "self": "https://ruckus.atlassian.net/rest/api/2/customFieldOption/11408",
                            "value": "SW-Design/Architecture Flaw"
                        }
                    ],
                    "customfield_10166": "2025-04-18",
                    "customfield_10167": {
                        "id": "11429",
                        "self": "https://ruckus.atlassian.net/rest/api/2/customFieldOption/11429",
                        "value": "No"
                    },
                    "customfield_10168": None,
                    "customfield_10169": {
                        "id": "11355",
                        "self": "https://ruckus.atlassian.net/rest/api/2/customFieldOption/11355",
                        "value": "Default"
                    },
                    "customfield_10170": {
                        "id": "11198",
                        "self": "https://ruckus.atlassian.net/rest/api/2/customFieldOption/11198",
                        "value": "Not Committed"
                    },
                    "customfield_10171": {
                        "id": "11938",
                        "self": "https://ruckus.atlassian.net/rest/api/2/customFieldOption/11938",
                        "value": "Y"
                    },
                    "customfield_10172": {
                        "id": "11364",
                        "self": "https://ruckus.atlassian.net/rest/api/2/customFieldOption/11364",
                        "value": "No"
                    },
                    "customfield_10173": None,
                    "customfield_10174": [
                        {
                            "id": "11436",
                            "self": "https://ruckus.atlassian.net/rest/api/2/customFieldOption/11436",
                            "value": "Process Improvement"
                        }
                    ],
                    "customfield_10175": {
                        "id": "11771",
                        "self": "https://ruckus.atlassian.net/rest/api/2/customFieldOption/11771",
                        "value": "No"
                    },
                    "customfield_10176": None,
                    "customfield_10177": {
                        "groupId": "537806bc-37f4-4026-b7d1-227a3e6f4712",
                        "name": "ol-vijaya.mynam-directreports",
                        "self": "https://ruckus.atlassian.net/rest/api/2/group?groupId=537806bc-37f4-4026-b7d1-227a3e6f4712"
                    },
                    "customfield_10178": {
                        "id": "11737",
                        "self": "https://ruckus.atlassian.net/rest/api/2/customFieldOption/11737",
                        "value": "No"
                    },
                    "customfield_10179": None,
                    "customfield_10180": None,
                    "customfield_10181": {
                        "id": "11417",
                        "self": "https://ruckus.atlassian.net/rest/api/2/customFieldOption/11417",
                        "value": "No"
                    },
                    "customfield_10182": None,
                    "customfield_10183": {
                        "id": "11154",
                        "self": "https://ruckus.atlassian.net/rest/api/2/customFieldOption/11154",
                        "value": "NonE"
                    },
                    "customfield_10184": {
                        "id": "11778",
                        "self": "https://ruckus.atlassian.net/rest/api/2/customFieldOption/11778",
                        "value": "No"
                    },
                    "customfield_10185": "acx-schema-935",
                    "customfield_10186": {
                        "id": "11209",
                        "self": "https://ruckus.atlassian.net/rest/api/2/customFieldOption/11209",
                        "value": "EMEA"
                    },
                    "customfield_10187": 0,
                    "customfield_10188": None,
                    "customfield_10189": {
                        "id": "11760",
                        "self": "https://ruckus.atlassian.net/rest/api/2/customFieldOption/11760",
                        "value": "No"
                    },
                    "customfield_10190": {
                        "id": "11768",
                        "self": "https://ruckus.atlassian.net/rest/api/2/customFieldOption/11768",
                        "value": "To Do"
                    },
                    "customfield_10192": {
                        "id": "11930",
                        "self": "https://ruckus.atlassian.net/rest/api/2/customFieldOption/11930",
                        "value": "No"
                    },
                    "customfield_10193": {
                        "id": "11940",
                        "self": "https://ruckus.atlassian.net/rest/api/2/customFieldOption/11940",
                        "value": "False"
                    },
                    "customfield_10194": None,
                    "customfield_10195": {
                        "id": "11937",
                        "self": "https://ruckus.atlassian.net/rest/api/2/customFieldOption/11937",
                        "value": "False"
                    },
                    "customfield_10197": None,
                    "customfield_10198": "What recent software versions have been used by the customer? What was the reason for the upgrade? Which versions work ok?\r\n\r\nWhen was the issue first noticed/discovered? (ie: after upgrade or downgrade? Which versions? What is the history of this issue?)",
                    "customfield_10200": {
                        "id": "11777",
                        "self": "https://ruckus.atlassian.net/rest/api/2/customFieldOption/11777",
                        "value": "False"
                    },
                    "customfield_10201": None,
                    "customfield_10202": None,
                    "customfield_10203": None,
                    "customfield_10204": {
                        "id": "11699",
                        "self": "https://ruckus.atlassian.net/rest/api/2/customFieldOption/11699",
                        "value": "N"
                    },
                    "customfield_10205": "[Root Cause]\r\nThe username reported by AP does not match the expected GuestPass username\r\nGUI filter fails to identify matching guests and guestDetails field remains empty.\r\n\r\n[Resolution]\r\nImproved the GUI filtering logic with MAC address matching, the issue should be gone. ",
                    "customfield_10206": None,
                    "customfield_10207": None,
                    "customfield_10208": None,
                    "customfield_10209": {
                        "accountId": "712020:312e8ba4-7f21-4469-a639-1a67636dcfc8",
                        "accountType": "atlassian",
                        "active": True,
                        "avatarUrls": {
                            "16x16": "https://secure.gravatar.com/avatar/1ce2e868f1ef9aeed6740b4fc435a740?d=https%3A%2F%2Favatar-management--avatars.us-west-2.prod.public.atl-paas.net%2Finitials%2FYW-5.png",
                            "24x24": "https://secure.gravatar.com/avatar/1ce2e868f1ef9aeed6740b4fc435a740?d=https%3A%2F%2Favatar-management--avatars.us-west-2.prod.public.atl-paas.net%2Finitials%2FYW-5.png",
                            "32x32": "https://secure.gravatar.com/avatar/1ce2e868f1ef9aeed6740b4fc435a740?d=https%3A%2F%2Favatar-management--avatars.us-west-2.prod.public.atl-paas.net%2Finitials%2FYW-5.png",
                            "48x48": "https://secure.gravatar.com/avatar/1ce2e868f1ef9aeed6740b4fc435a740?d=https%3A%2F%2Favatar-management--avatars.us-west-2.prod.public.atl-paas.net%2Finitials%2FYW-5.png"
                        },
                        "displayName": "Yang, William",
                        "emailAddress": "william.yang@commscope.com",
                        "self": "https://ruckus.atlassian.net/rest/api/2/user?accountId=712020%3A312e8ba4-7f21-4469-a639-1a67636dcfc8",
                        "timeZone": "America/Los_Angeles"
                    },
                    "customfield_10210": None,
                    "customfield_10211": {
                        "id": "10933",
                        "self": "https://ruckus.atlassian.net/rest/api/2/customFieldOption/10933",
                        "value": "N"
                    },
                    "customfield_10213": None,
                    "customfield_10214": None,
                    "customfield_10215": None,
                    "customfield_10216": None,
                    "customfield_10217": None,
                    "customfield_10218": None,
                    "customfield_10219": None,
                    "customfield_10220": None,
                    "customfield_10221": None,
                    "customfield_10222": None,
                    "customfield_10223": "acx-service-5082-D",
                    "customfield_10224": None,
                    "customfield_10225": None,
                    "customfield_10226": None,
                    "customfield_10227": None,
                    "customfield_10228": None,
                    "customfield_10229": None,
                    "customfield_10230": None,
                    "customfield_10231": None,
                    "customfield_10232": {
                        "accountId": "712020:f85b2370-dba7-49c7-9733-7243dcd25af7",
                        "accountType": "atlassian",
                        "active": True,
                        "avatarUrls": {
                            "16x16": "https://secure.gravatar.com/avatar/67b44b9ab907929dae90a026d9fb178e?d=https%3A%2F%2Favatar-management--avatars.us-west-2.prod.public.atl-paas.net%2Finitials%2FJP-0.png",
                            "24x24": "https://secure.gravatar.com/avatar/67b44b9ab907929dae90a026d9fb178e?d=https%3A%2F%2Favatar-management--avatars.us-west-2.prod.public.atl-paas.net%2Finitials%2FJP-0.png",
                            "32x32": "https://secure.gravatar.com/avatar/67b44b9ab907929dae90a026d9fb178e?d=https%3A%2F%2Favatar-management--avatars.us-west-2.prod.public.atl-paas.net%2Finitials%2FJP-0.png",
                            "48x48": "https://secure.gravatar.com/avatar/67b44b9ab907929dae90a026d9fb178e?d=https%3A%2F%2Favatar-management--avatars.us-west-2.prod.public.atl-paas.net%2Finitials%2FJP-0.png"
                        },
                        "displayName": "Jacob, Praveen",
                        "emailAddress": "praveen.jacob@commscope.com",
                        "self": "https://ruckus.atlassian.net/rest/api/2/user?accountId=712020%3Af85b2370-dba7-49c7-9733-7243dcd25af7",
                        "timeZone": "America/Los_Angeles"
                    },
                    "customfield_10233": "NA",
                    "customfield_10234": None,
                    "customfield_10235": None,
                    "customfield_10236": None,
                    "customfield_10237": 1,
                    "customfield_10238": None,
                    "customfield_10239": [
                        {
                            "id": "10302",
                            "self": "https://ruckus.atlassian.net/rest/api/2/customFieldOption/10302",
                            "value": "R650"
                        }
                    ],
                    "customfield_10241": None,
                    "customfield_10242": None,
                    "customfield_10243": None,
                    "customfield_10244": None,
                    "customfield_10246": "Please update the information below before resolving this issue:\r\n1) Fix description (Solution)* \r\nImproved the GUI filtering logic with MAC address matching, the issue should be gone.\r\n2) Brief description of the issue (root cause analysis)\r\nThe username reported by AP does not match the expected GuestPass username\r\nGUI filter fails to identify matching guests and guestDetails field remains empty. ",
                    "customfield_10248": None,
                    "customfield_10254": None,
                    "customfield_10255": None,
                    "customfield_10256": None,
                    "customfield_10257": None,
                    "customfield_10259": None,
                    "customfield_10260": None,
                    "customfield_10261": "Problem Statement: \r\n\r\nWhat is the configuration of the customers wireless and wired network topology? Include model numbers if possible. (AP's, ZD, Mesh, Switches, Clients, WAN, Servers, etc)\r\n\r\nIs this a new feature failure or existing feature? (new or existing)\r\n\r\nHow often does the issue occur? (always, every few minutes, hourly, daily, every few days, rarely, etc)\r\n\r\nDoes this issue impact the end-user service? Explain.\r\n\r\nAny recent wireless and wired network changes that may have caused the issue? (switches or routers or server changes)?\r\n\r\n If the issue is related to VoIP, is the voice choppy, delayed, noisy, or have gaps?\r\n\r\nDetails which may help troubleshoot this issue? Load conditions? Memory state?\r\n\r\nDetailed Troubleshooting/ Analysis:\r\n\r\nPlease attach/link all the customer debug info, system logs, support info, sniffer traces, and screenshots to this report while the issue is occurring.\r\n\r\nNote: For timely resolution by the Escalation Team please explain any details found in the logs completely and clearly.",
                    "customfield_10262": {
                        "id": "11427",
                        "self": "https://ruckus.atlassian.net/rest/api/2/customFieldOption/11427",
                        "value": "Default"
                    },
                    "customfield_10264": {
                        "groupId": "11f4a77e-fa6e-43d4-8aef-52ba19f9c3bf",
                        "name": "ol-michael.ren-directreports",
                        "self": "https://ruckus.atlassian.net/rest/api/2/group?groupId=11f4a77e-fa6e-43d4-8aef-52ba19f9c3bf"
                    },
                    "customfield_10265": "|Acceptance criteria met|y/n|\r\n|user stories are demonstrated to internal and external customers|y/n|\r\n|Story acceptance Tests written and passes|y/n|\r\n|Incremental Functional Design Specs updated based on each story|y/n|\r\n|Unit tested |y/n|\r\n|Static Analysis is at 100% pass rate on code development for the story|y/n|\r\n|Code Checked in and merged into the branch|y/n|\r\n|Code peer reviewed|y/n|\r\n|Code peer reviewed|y/n|\r\n|Test cases are 100% executed for the story with 95% pass rate|y/n|\r\n|No must-fix defects|y/n|\r\n|Story accepted by PLM/TPO|y/n|",
                    "customfield_10266": {
                        "id": "11224",
                        "self": "https://ruckus.atlassian.net/rest/api/2/customFieldOption/11224",
                        "value": "1 - One Line Story, before research"
                    },
                    "customfield_10267": {
                        "id": "11352",
                        "self": "https://ruckus.atlassian.net/rest/api/2/customFieldOption/11352",
                        "value": "Not Reviewed"
                    },
                    "customfield_10268": {
                        "id": "10698",
                        "self": "https://ruckus.atlassian.net/rest/api/2/customFieldOption/10698",
                        "value": "No"
                    },
                    "customfield_10269": None,
                    "customfield_10270": {
                        "id": "11928",
                        "self": "https://ruckus.atlassian.net/rest/api/2/customFieldOption/11928",
                        "value": "No"
                    },
                    "customfield_10271": {
                        "id": "10747",
                        "self": "https://ruckus.atlassian.net/rest/api/2/customFieldOption/10747",
                        "value": "No"
                    },
                    "customfield_10272": {
                        "id": "10748",
                        "self": "https://ruckus.atlassian.net/rest/api/2/customFieldOption/10748",
                        "value": "To Do"
                    },
                    "customfield_10273": {
                        "id": "11765",
                        "self": "https://ruckus.atlassian.net/rest/api/2/customFieldOption/11765",
                        "value": "To Do"
                    },
                    "customfield_10274": None,
                    "customfield_10275": None,
                    "customfield_10276": None,
                    "customfield_10277": None,
                    "customfield_10278": {
                        "id": "11682",
                        "self": "https://ruckus.atlassian.net/rest/api/2/customFieldOption/11682",
                        "value": "Education"
                    },
                    "customfield_10279": {
                        "id": "11712",
                        "self": "https://ruckus.atlassian.net/rest/api/2/customFieldOption/11712",
                        "value": "N"
                    },
                    "customfield_10280": {
                        "id": "11944",
                        "self": "https://ruckus.atlassian.net/rest/api/2/customFieldOption/11944",
                        "value": "ENT"
                    },
                    "customfield_10281": [
                        "James_Allen's_Girls'_School"
                    ],
                    "customfield_10282": None,
                    "customfield_10283": None,
                    "customfield_10284": None,
                    "customfield_10285": None,
                    "customfield_10286": None,
                    "customfield_10287": None,
                    "customfield_10288": None,
                    "customfield_10289": "acx-platform-303",
                    "customfield_10291": None,
                    "customfield_10292": "NA",
                    "customfield_10293": "Confirmed the fix acx-ui: 65793 in acx-service-5248 is now on STAGE",
                    "customfield_10294": None,
                    "customfield_10295": None,
                    "customfield_10296": None,
                    "customfield_10305": None,
                    "customfield_10309": "34.0",
                    "customfield_10310": None,
                    "customfield_10311": None,
                    "customfield_10312": None,
                    "customfield_10313": None,
                    "customfield_10314": None,
                    "customfield_10315": None,
                    "customfield_10316": None,
                    "customfield_10317": None,
                    "customfield_10318": None,
                    "customfield_10319": None,
                    "customfield_10320": None,
                    "customfield_10321": None,
                    "customfield_10322": None,
                    "customfield_10323": None,
                    "customfield_10324": None,
                    "customfield_10325": None,
                    "customfield_10326": None,
                    "customfield_10327": None,
                    "customfield_10328": None,
                    "customfield_10329": None,
                    "customfield_10330": None,
                    "customfield_10331": None,
                    "customfield_10333": None,
                    "customfield_10334": None,
                    "customfield_10335": None,
                    "customfield_10336": None,
                    "customfield_10337": None,
                    "customfield_10338": None,
                    "customfield_10339": None,
                    "customfield_10340": None,
                    "customfield_10341": None,
                    "customfield_10342": None,
                    "customfield_10343": None,
                    "customfield_10344": None,
                    "customfield_10345": None,
                    "customfield_10347": None,
                    "customfield_10348": None,
                    "customfield_10349": None,
                    "customfield_10350": None,
                    "customfield_10351": None,
                    "customfield_10352": None,
                    "customfield_10353": None,
                    "customfield_10355": None,
                    "customfield_10356": None,
                    "customfield_10357": None,
                    "customfield_10358": None,
                    "customfield_10359": None,
                    "customfield_10360": None,
                    "customfield_10361": None,
                    "customfield_10362": None,
                    "customfield_10363": None,
                    "customfield_10364": None,
                    "customfield_10365": None,
                    "customfield_10366": None,
                    "customfield_10369": None,
                    "customfield_10371": None,
                    "customfield_10372": None,
                    "customfield_10378": None,
                    "customfield_10379": None,
                    "customfield_10381": None,
                    "customfield_10382": None,
                    "customfield_10383": None,
                    "customfield_10384": None,
                    "customfield_10385": None,
                    "customfield_10386": None,
                    "customfield_10387": None,
                    "customfield_10388": None,
                    "customfield_10389": None,
                    "customfield_10390": None,
                    "customfield_10391": None,
                    "customfield_10392": None,
                    "customfield_10393": None,
                    "customfield_10394": None,
                    "customfield_10395": None,
                    "customfield_10396": None,
                    "customfield_10397": None,
                    "customfield_10398": None,
                    "customfield_10399": None,
                    "customfield_10400": None,
                    "customfield_10401": None,
                    "customfield_10402": None,
                    "customfield_10403": None,
                    "customfield_10404": None,
                    "customfield_10405": None,
                    "customfield_10406": None,
                    "customfield_10407": None,
                    "customfield_10408": None,
                    "customfield_10409": None,
                    "customfield_10410": None,
                    "customfield_10411": None,
                    "customfield_10412": None,
                    "customfield_10413": None,
                    "customfield_10414": None,
                    "customfield_10415": None,
                    "customfield_10416": None,
                    "customfield_10417": None,
                    "customfield_10418": None,
                    "customfield_10419": None,
                    "customfield_10422": None,
                    "customfield_10426": None,
                    "customfield_10434": None,
                    "customfield_10435": None,
                    "customfield_10443": None,
                    "customfield_10444": None,
                    "customfield_10446": None,
                    "customfield_10449": None,
                    "customfield_10450": None,
                    "customfield_10451": None,
                    "customfield_10453": None,
                    "customfield_10454": None,
                    "customfield_10456": None,
                    "customfield_10457": None,
                    "customfield_10458": None,
                    "customfield_10459": None,
                    "customfield_10460": None,
                    "customfield_10461": None,
                    "customfield_10462": None,
                    "customfield_10463": None,
                    "customfield_10465": None,
                    "customfield_10468": None,
                    "customfield_10469": None,
                    "customfield_10470": None,
                    "customfield_10471": None,
                    "customfield_10476": None,
                    "customfield_10480": None,
                    "customfield_10481": "[500PH00000YW07nYAD|https://ruckuswireless.my.salesforce.com/500PH00000YW07nYAD]",
                    "customfield_10482": "NA",
                    "customfield_10483": None,
                    "customfield_10484": None,
                    "customfield_10485": "01927279",
                    "customfield_10486": None,
                    "customfield_10487": {
                        "id": "13143",
                        "self": "https://ruckus.atlassian.net/rest/api/2/customFieldOption/13143",
                        "value": "No"
                    },
                    "customfield_10488": None,
                    "customfield_10489": None,
                    "customfield_10490": {
                        "id": "13124",
                        "self": "https://ruckus.atlassian.net/rest/api/2/customFieldOption/13124",
                        "value": "No"
                    },
                    "customfield_10491": None,
                    "customfield_10492": {
                        "accountId": "712020:f85b2370-dba7-49c7-9733-7243dcd25af7",
                        "accountType": "atlassian",
                        "active": True,
                        "avatarUrls": {
                            "16x16": "https://secure.gravatar.com/avatar/67b44b9ab907929dae90a026d9fb178e?d=https%3A%2F%2Favatar-management--avatars.us-west-2.prod.public.atl-paas.net%2Finitials%2FJP-0.png",
                            "24x24": "https://secure.gravatar.com/avatar/67b44b9ab907929dae90a026d9fb178e?d=https%3A%2F%2Favatar-management--avatars.us-west-2.prod.public.atl-paas.net%2Finitials%2FJP-0.png",
                            "32x32": "https://secure.gravatar.com/avatar/67b44b9ab907929dae90a026d9fb178e?d=https%3A%2F%2Favatar-management--avatars.us-west-2.prod.public.atl-paas.net%2Finitials%2FJP-0.png",
                            "48x48": "https://secure.gravatar.com/avatar/67b44b9ab907929dae90a026d9fb178e?d=https%3A%2F%2Favatar-management--avatars.us-west-2.prod.public.atl-paas.net%2Finitials%2FJP-0.png"
                        },
                        "displayName": "Jacob, Praveen",
                        "emailAddress": "praveen.jacob@commscope.com",
                        "self": "https://ruckus.atlassian.net/rest/api/2/user?accountId=712020%3Af85b2370-dba7-49c7-9733-7243dcd25af7",
                        "timeZone": "America/Los_Angeles"
                    },
                    "customfield_10493": "acx-ui: 65793 in acx-service-5248",
                    "customfield_10494": {
                        "id": "13125",
                        "self": "https://ruckus.atlassian.net/rest/api/2/customFieldOption/13125",
                        "value": "Yes"
                    },
                    "customfield_10495": "01927279",
                    "customfield_10496": None,
                    "customfield_10498": None,
                    "customfield_10499": None,
                    "customfield_10500": None,
                    "customfield_10503": None,
                    "customfield_10504": None,
                    "customfield_10505": None,
                    "customfield_10506": None,
                    "customfield_10507": None,
                    "customfield_10509": None,
                    "customfield_10510": None,
                    "customfield_10516": None,
                    "customfield_10521": None,
                    "customfield_10523": None,
                    "customfield_10526": None,
                    "customfield_10529": None,
                    "customfield_10531": None,
                    "customfield_10532": None,
                    "customfield_10534": None,
                    "customfield_10537": None,
                    "customfield_10538": None,
                    "customfield_10540": None,
                    "customfield_10541": None,
                    "customfield_10543": None,
                    "customfield_10544": None,
                    "customfield_10545": None,
                    "customfield_10546": None,
                    "customfield_10547": None,
                    "customfield_10548": None,
                    "customfield_10549": None,
                    "customfield_10550": None,
                    "customfield_10551": None,
                    "customfield_10557": None,
                    "customfield_10562": None,
                    "customfield_10565": None,
                    "customfield_10566": None,
                    "customfield_10567": None,
                    "customfield_10568": None,
                    "customfield_10569": None,
                    "customfield_10570": None,
                    "customfield_10571": None,
                    "customfield_10574": None,
                    "customfield_10580": None,
                    "customfield_10582": None,
                    "customfield_10583": None,
                    "customfield_10584": None,
                    "customfield_10587": None,
                    "customfield_10589": None,
                    "customfield_10590": None,
                    "customfield_10594": None,
                    "customfield_10660": None,
                    "customfield_10661": None,
                    "customfield_10662": None,
                    "customfield_10664": None,
                    "customfield_10670": None,
                    "customfield_10678": None,
                    "customfield_10679": None,
                    "customfield_10681": None,
                    "customfield_10682": None,
                    "customfield_10683": None,
                    "customfield_10684": None,
                    "customfield_10685": None,
                    "customfield_10686": None,
                    "customfield_10687": None,
                    "customfield_10688": None,
                    "customfield_10689": None,
                    "customfield_10690": None,
                    "customfield_10734": None,
                    "customfield_10740": None,
                    "customfield_10748": None,
                    "customfield_10753": None,
                    "customfield_10758": None,
                    "customfield_10788": None,
                    "customfield_10801": None,
                    "customfield_10812": None,
                    "customfield_10816": None,
                    "customfield_10820": None,
                    "customfield_10824": None,
                    "customfield_10827": None,
                    "customfield_10828": None,
                    "customfield_10829": None,
                    "customfield_10831": None,
                    "customfield_10832": None,
                    "customfield_10833": None,
                    "customfield_10835": None,
                    "customfield_10836": None,
                    "customfield_10839": None,
                    "customfield_10840": None,
                    "customfield_10841": None,
                    "customfield_10843": None,
                    "customfield_10844": None,
                    "customfield_10845": None,
                    "customfield_10847": None,
                    "customfield_10848": None,
                    "customfield_10855": None,
                    "customfield_10859": None,
                    "customfield_10861": None,
                    "customfield_10863": None,
                    "customfield_10868": None,
                    "customfield_10871": None,
                    "customfield_10872": None,
                    "customfield_10880": [],
                    "customfield_10919": None,
                    "customfield_10920": None,
                    "customfield_10921": None,
                    "customfield_10922": None,
                    "customfield_10923": None,
                    "customfield_10924": "True",
                    "customfield_10925": None,
                    "customfield_10926": None,
                    "customfield_10927": None,
                    "customfield_10928": None,
                    "customfield_10929": None,
                    "customfield_10930": None,
                    "customfield_10931": None,
                    "customfield_10932": None,
                    "customfield_10933": None,
                    "customfield_10935": None,
                    "customfield_10936": None,
                    "customfield_10937": None,
                    "customfield_10939": None,
                    "customfield_10940": None,
                    "customfield_10941": None,
                    "customfield_10942": None,
                    "customfield_10943": None,
                    "customfield_10978": None,
                    "customfield_11012": None,
                    "customfield_11013": None,
                    "description": "+*Issue:*+ Guest details are missing for some random guest users on the wireless clients page.\n \n+*Summary:*+\n> The customer suspects that some unknown users can connect to JAGS-Guests SSID without going through captive portal authentication.\n> The JAGS-Guests SSID is configured with the portal type “Guest Pass.” So, users must sign in with a guest pass credential to connect to the SSID.\n> Some unknown users are found to be in Authorized state without any guest pass information.\n \n+*Observations:*+\n> For example client MAC address “E2:B8:C8:54:6C:B8” is seen in the authorized state on the wireless clients list page.\n \n!https://ruckus.atlassian.net/rest/api/3/attachment/content/745675|height=230,width=553!\n \n> Guest details are empty for this client. Particularly the guest name which is a mandatory field when a guest pass is generated.\nh1.  !https://ruckus.atlassian.net/rest/api/3/attachment/content/786980|height=266,width=553!\n\n> Also, the Guest Created and Guest Expires time are same.\n \n> Moreover, Guest Created and Guest Expires time shown is the time when we click on the client. So if we click again on the client at 15:20 then it shows Guest Created and Guest Expires time as 15:20 as shown below:\n \n!https://ruckus.atlassian.net/rest/api/3/attachment/content/786981|height=273,width=553!\n \n> This client device \"aa:41:bf:da:4b:6c\" is also a current example.\n!https://ruckus.atlassian.net/rest/api/3/attachment/content/786982|height=308,width=553!\n+*>*+ AP logs how the client authorization event:\nFeb 13 09:53:45 James-Allen's-Girls'-School_15c22d54b671445cb3ecf8dc528b97ca_202339001035_AP-JGS-GF-L13 daemon.info hostapd: @@206,clientAuthorization,\"apMac\"=\"c8:a6:08:12:2c:60\",\"clientMac\"=\"e2:b8:c8:54:6c:b8\",\"ssid\"=\"JAGS-Guests\",\"bssid\"=\"c8:a6:08:92:2c:61\",\"userId\"=\"\",\"wlanId\"=\"44\",\"iface\"=\"wlan33\",\"tenantUUID\"=\"839f87c6-d116-497e-afce-aa8157abd30c\",\"apName\"=\"AP-JGS-GF-L13\",\"apGps\"=\"51.454821,-0.085475\",\"networkId\"=\"59dc792a872e4f40a4836f2e1d0120ae\",\"networkName\"=\"JAGS-Guests\",\"clientIP\"=\"10.99.4.229\",\"userName\"=\"e2b8c8546cb8\",\"vlanId\"=\"994\",\"radio\"=\"a/n/ac/ax\",\"encryption\"=\"None\",\"band\"=\"5g\"\nFeb 13 09:53:45 James-Allen's-Girls'-School_15c22d54b671445cb3ecf8dc528b97ca_202339001035_AP-JGS-GF-L13 daemon.info hostapd: wlan33: STA e2:b8:c8:54:6c:b8 IEEE 802.11: wlan33: IEEE 802.11: station authorized: ssid:JAGS-Guests, is_wispr:2, wispr_start_time:1739440425, session_timeout:86400, idle_timeout:0, expiration:0, acct_interim_interval:0, grace_period:3600, uuid:, common_state:1 filter_id:0\n\\------------output omitted---------------\n+*Kibana logs:*+\nReceived RSyslog event message RequestId: a4d5fbb10ac54754bf8a02199376e07e Topic: acx.event.syslog-message Raw payload: Feb 13 09:54:20 James-Allen's-Girls'-School_15c22d54b671445cb3ecf8dc528b97ca_202339001035_AP-JGS-GF-L13 daemon.info hostapd: @@206,clientAuthorization,\"apMac\"=\"c8:a6:08:12:2c:60\",\"clientMac\"=\"e2:b8:c8:54:6c:b8\",\"ssid\"=\"JAGS-Guests\",\"bssid\"=\"c8:a6:08:92:2c:61\",\"userId\"=\"\",\"wlanId\"=\"44\",\"iface\"=\"wlan33\",\"tenantUUID\"=\"839f87c6-d116-497e-afce-aa8157abd30c\",\"apName\"=\"AP-JGS-GF-L13\",\"apGps\"=\"51.454821,-0.085475\",\"networkId\"=\"59dc792a872e4f40a4836f2e1d0120ae\",\"networkName\"=\"JAGS-Guests\",\"clientIP\"=\"10.99.4.229\",\"userName\"=\"e2b8c8546cb8\",\"vlanId\"=\"994\",\"radio\"=\"a/n/ac/ax\",\"encryption\"=\"None\",\"band\"=\"5g\",\"fwVersion\"=\"7.0.0.300.6497\",\"model\"=\"R650\",\"zoneUUID\"=\"15c22d54b671445cb3ecf8dc528b97ca\",\"zoneName\"=\"15c22d54b671445cb3ecf8dc528b97ca\",\"timeZone\"=\"GMT+0BST,M3.5.0/01:00,M10.4.0/01:00\",\"apLocation\"=\"\",\"apGps\"=\"51.454821,-0.085475\",\"apIpAddress\"=\"10.0.12.65\",\"apIpv6Address\"=\"\",\"apGroupUUID\"=\"3dff52291b4a4db6a5394f904ea71e12\",\"domainId\"=\"ebb3238545f64af78a05504e2b470a35\",\"serialNumber\"=\"202339001035\",\"domainName\"=\"James Allen's Girls' School\",\"wlanGroupUUID\"=\"3dff52291b4a4db6a5394f904ea71e12_RADIO24\",\"apDescription\"=\"AP-JGS-GF-L13\",\"serialNumber\"=\"202339001035\",\"tenantId\"=\"ebb3238545f64af78a05504e2b470a35\",\"tenantName\"=\"James Allen's Girls' School\",\"venueId\"=\"15c22d54b671445cb3ecf8dc528b97ca\",\"venueName\"=\"James Allen's Girls' School\",\"apGroupId\"=\"3dff52291b4a4db6a5394f904ea71e12\",\"apGroupName\"=\"Science Maths Block\",\"apId\"=\"C8:A6:08:12:2C:60\",\"apName\"=\"AP-JGS-GF-L13\",\"poePort\"=\"1\"\n\\----------------------------------------------------\n> Such users are unknown and the issue is not easily reproducible.\n \n+*Tenant Info:*+\n \nTenant Name: James Allen's Girls' School\nTenant Email: lsterling@webuy.com\nIDM Tenant ID: 0015000000kaVOpAAM\nAlto Tenant ID: ebb3238545f64af78a05504e2b470a35\nResource Profile: ruckus-one\nAccount Type: REC\n \n+*Logs attached:*+\n \n> HAR log file\n \n> AP Support log file",
                    "duedate": None,
                    "environment": None,
                    "fixVersions": [
                        {
                            "archived": False,
                            "description": "",
                            "id": "10780",
                            "name": "Ruckus-One",
                            "released": False,
                            "self": "https://ruckus.atlassian.net/rest/api/2/version/10780"
                        }
                    ],
                    "issuelinks": [
                        {
                            "id": "174017",
                            "outwardIssue": {
                                "fields": {
                                    "issuetype": {
                                        "avatarId": 10303,
                                        "description": "A problem which impairs or prevents the functions of the product. (Migrated on 28 Feb 2025 23:55 UTC)",
                                        "hierarchyLevel": 0,
                                        "iconUrl": "https://ruckus.atlassian.net/rest/api/2/universal_avatar/view/type/issuetype/avatar/10303?size=medium",
                                        "id": "10006",
                                        "name": "Bug",
                                        "self": "https://ruckus.atlassian.net/rest/api/2/issuetype/10006",
                                        "subtask": False
                                    },
                                    "priority": {
                                        "iconUrl": "https://ruckus.atlassian.net/images/icons/priorities/critical.svg",
                                        "id": "10001",
                                        "name": "P2",
                                        "self": "https://ruckus.atlassian.net/rest/api/2/priority/10001"
                                    },
                                    "status": {
                                        "description": "",
                                        "iconUrl": "https://ruckus.atlassian.net/images/icons/statuses/resolved.png",
                                        "id": "5",
                                        "name": "Resolved",
                                        "self": "https://ruckus.atlassian.net/rest/api/2/status/5",
                                        "statusCategory": {
                                            "colorName": "green",
                                            "id": 3,
                                            "key": "done",
                                            "name": "Done",
                                            "self": "https://ruckus.atlassian.net/rest/api/2/statuscategory/3"
                                        }
                                    },
                                    "summary": "[ER-14520] Wireless Guest user information is not displayed correctly"
                                },
                                "id": "284906",
                                "key": "ACX-79018",
                                "self": "https://ruckus.atlassian.net/rest/api/2/issue/284906"
                            },
                            "self": "https://ruckus.atlassian.net/rest/api/2/issueLink/174017",
                            "type": {
                                "id": "10013",
                                "inward": "is child of",
                                "name": "Parent-Child",
                                "outward": "is parent of",
                                "self": "https://ruckus.atlassian.net/rest/api/2/issueLinkType/10013"
                            }
                        },
                        {
                            "id": "461932",
                            "outwardIssue": {
                                "fields": {
                                    "issuetype": {
                                        "avatarId": 10310,
                                        "description": "An improvement or enhancement to an existing feature or task. (Migrated on 28 Feb 2025 23:55 UTC)",
                                        "hierarchyLevel": 0,
                                        "iconUrl": "https://ruckus.atlassian.net/rest/api/2/universal_avatar/view/type/issuetype/avatar/10310?size=medium",
                                        "id": "10028",
                                        "name": "Improvement",
                                        "self": "https://ruckus.atlassian.net/rest/api/2/issuetype/10028",
                                        "subtask": False
                                    },
                                    "priority": {
                                        "iconUrl": "https://ruckus.atlassian.net/images/icons/priorities/major.svg",
                                        "id": "10002",
                                        "name": "P3",
                                        "self": "https://ruckus.atlassian.net/rest/api/2/priority/10002"
                                    },
                                    "status": {
                                        "description": "",
                                        "iconUrl": "https://ruckus.atlassian.net/images/icons/statuses/resolved.png",
                                        "id": "5",
                                        "name": "Resolved",
                                        "self": "https://ruckus.atlassian.net/rest/api/2/status/5",
                                        "statusCategory": {
                                            "colorName": "green",
                                            "id": 3,
                                            "key": "done",
                                            "name": "Done",
                                            "self": "https://ruckus.atlassian.net/rest/api/2/statuscategory/3"
                                        }
                                    },
                                    "summary": "[ER-14520] Wireless Guest user information should be empty if unauthorized"
                                },
                                "id": "968621",
                                "key": "ACX-83183",
                                "self": "https://ruckus.atlassian.net/rest/api/2/issue/968621"
                            },
                            "self": "https://ruckus.atlassian.net/rest/api/2/issueLink/461932",
                            "type": {
                                "id": "10013",
                                "inward": "is child of",
                                "name": "Parent-Child",
                                "outward": "is parent of",
                                "self": "https://ruckus.atlassian.net/rest/api/2/issueLinkType/10013"
                            }
                        }
                    ],
                    "issuerestriction": {
                        "issuerestrictions": {},
                        "shouldDisplay": False
                    },
                    "issuetype": {
                        "avatarId": 10300,
                        "description": "Escalation to Eng (Migrated on 28 Feb 2025 23:55 UTC)",
                        "hierarchyLevel": 0,
                        "iconUrl": "https://ruckus.atlassian.net/rest/api/2/universal_avatar/view/type/issuetype/avatar/10300?size=medium",
                        "id": "10013",
                        "name": "Support Case",
                        "self": "https://ruckus.atlassian.net/rest/api/2/issuetype/10013",
                        "subtask": False
                    },
                    "labels": [
                        "emea"
                    ],
                    "lastViewed": "2025-05-21T19:58:37.950-0700",
                    "progress": {
                        "progress": 0,
                        "total": 0
                    },
                    "project": {
                        "avatarUrls": {
                            "16x16": "https://ruckus.atlassian.net/rest/api/2/universal_avatar/view/type/project/avatar/10422?size=xsmall",
                            "24x24": "https://ruckus.atlassian.net/rest/api/2/universal_avatar/view/type/project/avatar/10422?size=small",
                            "32x32": "https://ruckus.atlassian.net/rest/api/2/universal_avatar/view/type/project/avatar/10422?size=medium",
                            "48x48": "https://ruckus.atlassian.net/rest/api/2/universal_avatar/view/type/project/avatar/10422"
                        },
                        "id": "10010",
                        "key": "ER",
                        "name": "Escalation",
                        "projectCategory": {
                            "description": "Projects for all software",
                            "id": "10000",
                            "name": "SOFTWARE ENGINEERING",
                            "self": "https://ruckus.atlassian.net/rest/api/2/projectCategory/10000"
                        },
                        "projectTypeKey": "software",
                        "self": "https://ruckus.atlassian.net/rest/api/2/project/10010",
                        "simplified": False
                    },
                    "reporter": {
                        "accountId": "712020:f85b2370-dba7-49c7-9733-7243dcd25af7",
                        "accountType": "atlassian",
                        "active": True,
                        "avatarUrls": {
                            "16x16": "https://secure.gravatar.com/avatar/67b44b9ab907929dae90a026d9fb178e?d=https%3A%2F%2Favatar-management--avatars.us-west-2.prod.public.atl-paas.net%2Finitials%2FJP-0.png",
                            "24x24": "https://secure.gravatar.com/avatar/67b44b9ab907929dae90a026d9fb178e?d=https%3A%2F%2Favatar-management--avatars.us-west-2.prod.public.atl-paas.net%2Finitials%2FJP-0.png",
                            "32x32": "https://secure.gravatar.com/avatar/67b44b9ab907929dae90a026d9fb178e?d=https%3A%2F%2Favatar-management--avatars.us-west-2.prod.public.atl-paas.net%2Finitials%2FJP-0.png",
                            "48x48": "https://secure.gravatar.com/avatar/67b44b9ab907929dae90a026d9fb178e?d=https%3A%2F%2Favatar-management--avatars.us-west-2.prod.public.atl-paas.net%2Finitials%2FJP-0.png"
                        },
                        "displayName": "Jacob, Praveen",
                        "emailAddress": "praveen.jacob@commscope.com",
                        "self": "https://ruckus.atlassian.net/rest/api/2/user?accountId=712020%3Af85b2370-dba7-49c7-9733-7243dcd25af7",
                        "timeZone": "America/Los_Angeles"
                    },
                    "resolution": {
                        "description": "Work has been completed on this issue.",
                        "id": "10000",
                        "name": "Done",
                        "self": "https://ruckus.atlassian.net/rest/api/2/resolution/10000"
                    },
                    "resolutiondate": "2025-04-09T10:38:07.682-0700",
                    "security": None,
                    "status": {
                        "description": "",
                        "iconUrl": "https://ruckus.atlassian.net/images/icons/statuses/resolved.png",
                        "id": "5",
                        "name": "Resolved",
                        "self": "https://ruckus.atlassian.net/rest/api/2/status/5",
                        "statusCategory": {
                            "colorName": "green",
                            "id": 3,
                            "key": "done",
                            "name": "Done",
                            "self": "https://ruckus.atlassian.net/rest/api/2/statuscategory/3"
                        }
                    },
                    "statusCategory": {
                        "colorName": "green",
                        "id": 3,
                        "key": "done",
                        "name": "Done",
                        "self": "https://ruckus.atlassian.net/rest/api/2/statuscategory/3"
                    },
                    "statuscategorychangedate": "2025-04-09T10:38:07.813-0700",
                    "subtasks": [],
                    "summary": "James Allen's Girls' School | R1_EU | Wireless Guest user information is not displayed correctly",
                    "timeestimate": None,
                    "timeoriginalestimate": None,
                    "timespent": None,
                    "timetracking": {},
                    "updated": "2025-05-01T08:33:25.275-0700",
                    "versions": [
                        {
                            "archived": False,
                            "description": "",
                            "id": "10780",
                            "name": "Ruckus-One",
                            "released": False,
                            "self": "https://ruckus.atlassian.net/rest/api/2/version/10780"
                        }
                    ],
                    "votes": {
                        "hasVoted": False,
                        "self": "https://ruckus.atlassian.net/rest/api/2/issue/ER-14520/votes",
                        "votes": 0
                    },
                    "watches": {
                        "isWatching": False,
                        "self": "https://ruckus.atlassian.net/rest/api/2/issue/ER-14520/watchers",
                        "watchCount": 40
                    },
                    "worklog": {
                        "maxResults": 20,
                        "startAt": 0,
                        "total": 0,
                        "worklogs": []
                    },
                    "workratio": -1
                },
                "id": "317008",
                "key": "ER-14520",
                "self": "https://ruckus.atlassian.net/rest/api/2/issue/317008"
            }
        }
    ]

    result = main(sample_jira_response)
    print(result["result"])
