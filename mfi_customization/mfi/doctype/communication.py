import frappe

def after_insert_file(doc, method):
    """
    Handles file attachment logic when a file is attached to a Communication.
    """
    if doc.attached_to_doctype == "Communication":
        # Fetch linked Issues for the Communication
        linked_issues = frappe.get_all('Issue', {'communication': doc.attached_to_name}, ['name'])

        if not linked_issues:  # No linked Issues found
            cmm_doc = frappe.get_doc("Communication", doc.attached_to_name)
            domain_rule = email_rules_true_for_domain(cmm_doc.sender)
            email_rule = email_rules_true_for_emails_table(cmm_doc.sender)

            # Check domain or email-based rules and if the communication is received
            if (domain_rule.get('is_true') or email_rule.get('is_true')) and cmm_doc.sent_or_received == 'Received':
                if not cmm_doc.subject.startswith("Re:"):
                    # Create a new Issue
                    issue = frappe.new_doc("Issue")
                    issue.subject = cmm_doc.subject
                    issue.description = cmm_doc.content
                    issue.raised_by = cmm_doc.sender
                    issue.communication = doc.attached_to_name
                    issue.customer = domain_rule.get('customer') if domain_rule.get('is_true') else email_rule.get('customer')
                    issue.flags.ignore_mandatory = True
                    issue.company = domain_rule.get('company') if domain_rule.get('is_true') else email_rule.get('company')
                    issue.save()

                    # Attach the file to the new Issue
                    attach_file_to_issue(doc, issue.name)
        else:
            # Attach the file to all linked Issues
            for issue in linked_issues:
                attach_file_to_issue(doc, issue['name'])


def attach_file_to_issue(file_doc, issue_name):
    """
    Attaches a file to a specific Issue.
    """
    frappe.get_doc({
        "doctype": "File",
        "file_name": file_doc.file_name,
        "file_size": file_doc.file_size,
        "folder": file_doc.folder,
        "is_private": file_doc.is_private,
        "file_url": file_doc.file_url,
        "attached_to_doctype": "Issue",
        "attached_to_name": issue_name,
    }).insert(ignore_permissions=True)


def email_rules_true_for_domain(sender):
    """
    Checks if the sender matches any domain-based email rules for Issues.
    """
    response = {'is_true': False, 'customer': '', 'company': ''}

    # Fetch all domain-based email rules
    email_rules = frappe.get_all('Email Rules for Issue', {'group_by': 'Domain'}, ['domain_name', 'customer'])

    # Check if sender's domain matches any rule
    sender_domain = sender.split('@')[1] if '@' in sender else ''
    for rule in email_rules:
        if rule['domain_name'].lower() == sender_domain.lower():
            customer = frappe.get_doc('Customer', rule['customer'])
            response.update({
                'is_true': True,
                'customer': rule['customer'],
                'company': customer.accounts[0].company if customer.accounts else ''
            })
            return response

    return response


def email_rules_true_for_emails_table(sender):
    """
    Checks if the sender matches any email-specific rules for Issues.
    """
    response = {'is_true': False, 'customer': '', 'company': ''}

    # Fetch all email-based rules
    email_rules = frappe.get_all('Email Rules for Issue', {'group_by': 'Emails'}, ['name', 'customer'])

    for rule in email_rules:
        # Fetch email list for the current rule
        rule_doc = frappe.get_doc('Email Rules for Issue', rule['name'])
        emails = [email_row.email for email_row in rule_doc.email_list_for_issue]

        if sender in emails:
            customer = frappe.get_doc('Customer', rule['customer'])
            response.update({
                'is_true': True,
                'customer': rule['customer'],
                'company': customer.accounts[0].company if customer.accounts else ''
            })
            return response

    return response


def after_insert(doc, method):
    """
    Handles logic to create an Issue after inserting a Communication.
    """
    # Fetch any existing issue linked to this communication
    existing_issue = frappe.db.get_value('Issue', {'communication': doc.name}, "name")

    if not existing_issue:
        # Get email-based rules
        domain_rule = email_rules_true_for_domain(doc.sender)
        email_rule = email_rules_true_for_emails_table(doc.sender)

        # Check if either rule applies and if the email was received
        if doc.sent_or_received == 'Received' and (domain_rule.get('is_true') or email_rule.get('is_true')):
            if not doc.subject.startswith("Re:"):
                # Determine customer & company from matching rule
                matching_rule = domain_rule if domain_rule.get('is_true') else email_rule

                # Create and insert Issue
                frappe.get_doc({
                    "doctype": "Issue",
                    "subject": doc.subject,
                    "description": doc.content,
                    "raised_by": doc.sender,
                    "communication": doc.name,
                    "customer": matching_rule.get('customer'),
                    "company": matching_rule.get('company'),
                    "flags": {"ignore_mandatory": True}
                }).insert()

