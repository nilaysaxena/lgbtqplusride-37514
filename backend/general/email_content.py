MESSAGE_CONTENT = {
    "INVITE_CUSTOMER": {
        'subject': 'Application Invitation from {business_name}',
        'template': 'email_templates/invite_customer.html'
    },
    "BUSINESS_APPROVAL": {
        'subject': '{business_name} profile has been {flag}',
        'template': 'email_templates/business_approval.html'
    },
    "ISSUE_IN_FUNDING": {
        'subject': 'Urgent: Issue in funding of Loans',
        'template': 'email_templates/issue_in_funding.html'
    },
    "WARN_CUSTOMER": {
        'subject': '{subject_text}',
        'template': 'email_templates/warn_customer.html'
    },
    "ADD_USER": {
        'subject': 'You are added in VTP Financial',
        'template': 'email_templates/add_user.html'
    },
}
