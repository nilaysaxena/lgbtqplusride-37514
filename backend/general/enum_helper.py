from django.utils.decorators import classproperty
from django.utils.translation import ugettext_lazy as _

from enum import Enum, unique


class BaseEnum(Enum):
    @classmethod
    def choices(cls):
        choices = list()
        for item in cls:
            choices.append((item.value, _(item.descriptive_name)))
        return tuple(choices)

    # string the name
    def __str__(self):
        return self.name

    # int the value
    def __int__(self):
        return self.value

    @classproperty
    def valid_values(cls):
        choices = list()
        for item in cls:
            choices.append(item.value)
        return tuple(choices)

    @property
    def descriptive_name(self):
        return self.name.replace('_', ' ').title()

    @classproperty
    def choices_dict(cls):
        choices = {}
        for item in cls:
            choices[item.value] = _(item.descriptive_name)
        return choices


@unique
class UserType(BaseEnum):
    SUPER_ADMIN = 'SA'
    ADMIN = "A"
    CUSTOMER = 'C'
    BUSINESS = "B"
    LENDER = 'L'


@unique
class ApplicationStatus(BaseEnum):
    PENDING = "PENDING"
    APPROVED = "APPROVED"
    DENIED = "DENIED"
    CUSTOMER_OTP_VERIFIED = 'CUSTOMER_OTP_VERIFIED'
    PRODUCT_DETAILS_FILLED = 'PRODUCT_DETAILS_FILLED'
    FINANCE_FEE_CHARGED = 'FINANCE_FEE_CHARGED'
    FUNDED = "FUNDED"
    VOID_APPLICATION = 'VOID_APPLICATION'
    EXPIRED = 'EXPIRED'

    @classmethod
    def get_possible_application_status(cls, status):
        possible_new_status = {
            cls.PENDING.value: (cls.APPROVED.value, cls.DENIED.value),
            cls.APPROVED.value: (cls.CUSTOMER_OTP_VERIFIED.value, cls.EXPIRED.value, cls.VOID_APPLICATION.value),
            cls.CUSTOMER_OTP_VERIFIED.value: (cls.PRODUCT_DETAILS_FILLED.value,),
            cls.PRODUCT_DETAILS_FILLED.value: (cls.FINANCE_FEE_CHARGED.value,),
            cls.FINANCE_FEE_CHARGED.value: (cls.FUNDED.value, cls.VOID_APPLICATION.value),
            cls.VOID_APPLICATION.value: (),
            cls.DENIED.value: (),
            cls.FUNDED.value: (),
            cls.EXPIRED.value: (),
        }
        return possible_new_status.get(status, ())

    @classmethod
    def get_cancel_application_status(cls):
        return (
            ApplicationStatus.FUNDED.value, ApplicationStatus.DENIED.value, ApplicationStatus.VOID_APPLICATION.value,
            ApplicationStatus.EXPIRED.value)


@unique
class LoanStatus(BaseEnum):
    UNDERWRITING = "UNDERWRITING"
    SEND_TO_SIGN = 'SEND_TO_SIGN'
    CUSTOMER_SIGNED = 'CUSTOMER_SIGNED'
    DEALER_SIGNED = 'DEALER_SIGNED'
    FUNDED = "FUNDED"
    OFFER_DECLINED = "OFFER_DECLINED"
    LOAN_CANCELLED = "LOAN_CANCELLED"
    VOID_LOAN = 'VOID_LOAN'
    CLOSED = 'CLOSED'

    @classmethod
    def get_possible_loan_status(cls, status):
        possible_new_status = {
            cls.UNDERWRITING.value: (cls.SEND_TO_SIGN.value, cls.LOAN_CANCELLED.value),
            cls.SEND_TO_SIGN.value: (
                cls.CUSTOMER_SIGNED.value, cls.OFFER_DECLINED.value,
                cls.LOAN_CANCELLED.value),
            cls.CUSTOMER_SIGNED.value: (cls.DEALER_SIGNED.value, cls.LOAN_CANCELLED.value, cls.VOID_LOAN.value),
            cls.DEALER_SIGNED.value: (cls.FUNDED.value, cls.LOAN_CANCELLED.value, cls.VOID_LOAN.value),
            cls.FUNDED.value: (cls.LOAN_CANCELLED.value, cls.VOID_LOAN.value, cls.CLOSED.value),
            cls.OFFER_DECLINED.value: (),
            cls.LOAN_CANCELLED.value: (),
            cls.VOID_LOAN.value: (),
            cls.CLOSED.value: (),
        }
        return possible_new_status.get(status, ())

    @classmethod
    def get_cancel_loan_status(cls):
        return (LoanStatus.OFFER_DECLINED.value, LoanStatus.LOAN_CANCELLED.value, LoanStatus.VOID_LOAN.value,
                LoanStatus.CLOSED.value)


@unique
class ApplicationSource(BaseEnum):
    ONLINE = "O"
    INSTORE = 'I'


@unique
class ApplicationGender(BaseEnum):
    MALE = "M"
    FEMALE = 'F'
    TRANSGENDER = 'T'
    NON_BINARY = 'NB'
    PREFER_NOT_TO_SAY = 'NOT'


@unique
class PhoneType(BaseEnum):
    HOME = "HOM"
    WORK = "WRK"
    MOBILE = "MBL"
    FAX = "FAX"


@unique
class BusinessApplicationStatus(BaseEnum):
    PENDING = "PEN"
    APPROVED = "APR"
    DENIED = "DEN"

    @classmethod
    def get_possible_business_status(cls, status):
        possible_new_status = {
            cls.PENDING.value: (cls.APPROVED.value, cls.DENIED.value),
            cls.APPROVED.value: (),
            cls.DENIED.value: (),
        }
        return possible_new_status.get(status, ())


@unique
class Frequency(BaseEnum):
    MONTHLY = 'M'
    WEEKLY = "W"
    BI_WEEKLY = 'BW'


@unique
class AccountType(BaseEnum):
    SAVING = 'S'
    CHECKING = "C"


@unique
class SignatureStatus(BaseEnum):
    PENDING = "PENDING"
    COMPLETED = 'COMPLETED'
    DISPUTED = 'DISPUTED'


@unique
class SignatureRecipientType(BaseEnum):
    CUSTOMER = 'C'
    DEALER = 'D'


@unique
class TransactionType(BaseEnum):
    DEBIT = 'DEBIT'
    CREDIT = 'CREDIT'


@unique
class TransactionSubType(BaseEnum):
    FINANCE_FEE = 'FINANCE_FEE'
    REFUND_FINANCE_FEE = 'REFUND_FINANCE_FEE'
    OUTSTANDING = 'OUTSTANDING'
    ADDITIONAL = 'ADDITIONAL'
    REGULAR = 'REGULAR'
    APPLY_LATE_FEES = 'APPLY_LATE_FEES'
    APPLY_NSF_FEES = 'APPLY_NSF_FEES'
    WAIVED_LATE_FEES = 'WAIVED_LATE_FEES'
    DEALER_PAYOUTS = 'DEALER_PAYOUTS'
    MANUALLY_ADDED = 'MANUALLY_ADDED'
    MANUALLY_DEDUCTED = 'MANUALLY_DEDUCTED'
    LOAN_SANCTIONED = 'LOAN_SANCTIONED'


@unique
class TransactionStatus(BaseEnum):
    PENDING = 'PENDING'
    SETTLED = 'SETTLED'
    ERROR = 'ERROR'
