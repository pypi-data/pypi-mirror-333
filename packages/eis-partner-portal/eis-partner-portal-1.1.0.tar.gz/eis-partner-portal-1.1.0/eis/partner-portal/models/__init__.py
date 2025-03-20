# flake8: noqa

# import all models into this package
# if you have many models here with many references from one model to another this may
# raise a RecursionError
# to avoid this, import only the models that you directly need like:
# from from eis.partner-portal.model.pet import Pet
# or import this package, but before doing it, use:
# import sys
# sys.setrecursionlimit(n)

from eis.partner-portal.model.account_class import AccountClass
from eis.partner-portal.model.account_policy_class import AccountPolicyClass
from eis.partner-portal.model.create_payment_method_request_dto import CreatePaymentMethodRequestDto
from eis.partner-portal.model.create_policy_request_dto import CreatePolicyRequestDto
from eis.partner-portal.model.insured_object_type_class import InsuredObjectTypeClass
from eis.partner-portal.model.invoice_class import InvoiceClass
from eis.partner-portal.model.invoice_item_class import InvoiceItemClass
from eis.partner-portal.model.invoice_status_class import InvoiceStatusClass
from eis.partner-portal.model.lead_bank_account_class import LeadBankAccountClass
from eis.partner-portal.model.lead_class import LeadClass
from eis.partner-portal.model.list_accounts_response_class import ListAccountsResponseClass
from eis.partner-portal.model.list_leads_response_class import ListLeadsResponseClass
from eis.partner-portal.model.list_partners_response_class import ListPartnersResponseClass
from eis.partner-portal.model.list_policies_response_class import ListPoliciesResponseClass
from eis.partner-portal.model.omit_type_class import OmitTypeClass
from eis.partner-portal.model.partner_class import PartnerClass
from eis.partner-portal.model.partner_link_class import PartnerLinkClass
from eis.partner-portal.model.partner_role_class import PartnerRoleClass
from eis.partner-portal.model.policy_class import PolicyClass
from eis.partner-portal.model.policy_object_class import PolicyObjectClass
from eis.partner-portal.model.policy_premium_class import PolicyPremiumClass
from eis.partner-portal.model.policy_premium_item_class import PolicyPremiumItemClass
from eis.partner-portal.model.policy_version_class import PolicyVersionClass
from eis.partner-portal.model.premium_formula_class import PremiumFormulaClass
from eis.partner-portal.model.premium_override_dto import PremiumOverrideDto
from eis.partner-portal.model.premium_override_request_dto import PremiumOverrideRequestDto
from eis.partner-portal.model.product_class import ProductClass
from eis.partner-portal.model.product_version_class import ProductVersionClass
from eis.partner-portal.model.sepa_dto import SepaDto
from eis.partner-portal.model.tag_class import TagClass
from eis.partner-portal.model.timeslice_class import TimesliceClass
from eis.partner-portal.model.uploaded_document_dto import UploadedDocumentDto
