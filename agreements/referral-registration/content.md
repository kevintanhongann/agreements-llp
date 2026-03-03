---
title: Referral Registration
version: 0.1.0
referrer_name: "[REFERRER_NAME]"
referrer_registration_no: "[REFERRER_REGISTRATION_NO]"
referrer_address: "[REFERRER_ADDRESS]"
recipient_name: "[RECIPIENT_NAME]"
recipient_registration_no: "[RECIPIENT_REGISTRATION_NO]"
recipient_address: "[RECIPIENT_ADDRESS]"
effective_date: DD MMMM YYYY
end_client: "[END_CLIENT]"
opportunity_name: "[OPPORTUNITY_NAME]"
commission_rate: 5%
validity_period: 12 months
introducer_agreement_date: 
specific_modifications_and_overrides: |
    1. None
---

**PARTIES INFORMATION**

|   |   |
| - | --- |
| **Referrer** | **${REFERRER_NAME} (Registration No. ${REFERRER_REGISTRATION_NO})** at ${REFERRER_ADDRESS} |
| **Recipient** | **${RECIPIENT_NAME} (Registration No. ${RECIPIENT_REGISTRATION_NO})** at ${RECIPIENT_ADDRESS} |
| **Effective Date** | ${EFFECTIVE_DATE} |

<br/>

**INCORPORATED TERMS**

This Referral Registration is issued pursuant to, and is governed by, the following documents (collectively, the "Agreement"). If the documents conflict, the following order of precedence applies:

1. This Referral Registration including the Specific Modifications And Overrides
{% if INTRODUCER_AGREEMENT_DATE %}
2. Business Development Introducer Agreement entered between Referrer and Recipient on ${INTRODUCER_AGREEMENT_DATE}{% endif %}

3. Business Development Service Terms at ${AGREEMENTS_URL}

By executing this Referral Registration, the Parties acknowledges that they have read, understood, and agree to be bound by the Agreement in its entirety. This Referral Registration and the Agreement shall be governed by the laws of Malaysia.

<br/>

**OPPORTUNITY DETAILS**

|   |   |
| - | - |
| **End Client (Prospective Client)** | ${END_CLIENT} |
| **Opportunity Name** | ${OPPORTUNITY_NAME} |
| **Commission Rate** | ${COMMISSION_RATE} |
| **Validity Period (The "Tail")** | ${VALIDITY_PERIOD} |

<br/>

**SPECIFIC MODIFICATIONS AND OVERRIDES**

${SPECIFIC_MODIFICATIONS_AND_OVERRIDES}

\newpage

**IN WITNESS WHEREOF,** the parties have executed this Referral Registration by their duly authorized representatives on the Effective Date.

| **For and on behalf of Referrer**    | **For and on behalf of Recipient** |
| - | - |
| Signature: | Signature: |
| | |
| | |
| Name: | Name: |
| Position: | Position: |
| Date: | Date: |
