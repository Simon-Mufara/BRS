"""
BuildRight Solutions (Pty) Ltd — Document Automation Agent
===========================================================
Automatically generate professional PDFs:
  • Quotations (tabular & clean styles)
  • Payment Requests (deposit / final balance)
  • Invoices
  • Delivery Notes
  • Scope of Works
"""

from .quotation import QuotationGenerator
from .payment_request import PaymentRequestGenerator
from .invoice import InvoiceGenerator
from .delivery_note import DeliveryNoteGenerator
from .scope_of_works import ScopeOfWorksGenerator
from .cli import main
from .mailer import send_document_email

__all__ = [
    "QuotationGenerator",
    "PaymentRequestGenerator",
    "InvoiceGenerator",
    "DeliveryNoteGenerator",
    "ScopeOfWorksGenerator",
    "main",
    "send_document_email"
]

# Convenience functions for quick usage
def generate_quotation(data, output_path=None):
    """Generate a quotation PDF.

    Args:
        data: Dictionary containing quotation data
        output_path: Optional path to save PDF (defaults to auto-generated name)

    Returns:
        Path to generated PDF file
    """
    gen = QuotationGenerator()
    gen.build(data)
    if output_path is None:
        # Generate default filename
        from brs_agent.utils import sf
        import re
        safe_project_title = re.sub(r'[^\w\-_]', '_', data.get('project_title', 'QUOTATION'))
        safe_client_name = re.sub(r'[^\w\-_]', '_', data.get('client_name', 'CLIENT'))
        output_path = f"{safe_client_name}_{safe_project_title}_QUOTATION.pdf"
    return gen.save(output_path)

def generate_payment_request(data, output_path=None):
    """Generate a payment request PDF.

    Args:
        data: Dictionary containing payment request data
        output_path: Optional path to save PDF (defaults to auto-generated name)

    Returns:
        Path to generated PDF file
    """
    gen = PaymentRequestGenerator()
    gen.build(data)
    if output_path is None:
        # Generate default filename
        from brs_agent.utils import sf
        import re
        safe_client_name = re.sub(r'[^\w\-_]', '_', data.get('client_name', 'CLIENT'))
        output_path = f"{safe_client_name}_PAYMENT_REQUEST.pdf"
    return gen.save(output_path)

def generate_invoice(data, output_path=None):
    """Generate an invoice PDF.

    Args:
        data: Dictionary containing invoice data
        output_path: Optional path to save PDF (defaults to auto-generated name)

    Returns:
        Path to generated PDF file
    """
    gen = InvoiceGenerator()
    gen.build(data)
    if output_path is None:
        # Generate default filename
        import re
        safe_client_name = re.sub(r'[^\w\-_]', '_', data.get('client_name', 'CLIENT'))
        output_path = f"{safe_client_name}_INVOICE.pdf"
    return gen.save(output_path)

def generate_delivery_note(data, output_path=None):
    """Generate a delivery note PDF.

    Args:
        data: Dictionary containing delivery note data
        output_path: Optional path to save PDF (defaults to auto-generated name)

    Returns:
        Path to generated PDF file
    """
    gen = DeliveryNoteGenerator()
    gen.build(data)
    if output_path is None:
        # Generate default filename
        import re
        safe_client_name = re.sub(r'[^\w\-_]', '_', data.get('client_name', 'CLIENT'))
        output_path = f"{safe_client_name}_DELIVERY_NOTE.pdf"
    return gen.save(output_path)

def generate_scope_of_works(data, output_path=None):
    """Generate a scope of works PDF.

    Args:
        data: Dictionary containing scope of works data
        output_path: Optional path to save PDF (defaults to auto-generated name)

    Returns:
        Path to generated PDF file
    """
    gen = ScopeOfWorksGenerator()
    gen.build(data)
    if output_path is None:
        # Generate default filename
        import re
        safe_client_name = re.sub(r'[^\w\-_]', '_', data.get('client_name', 'CLIENT'))
        output_path = f"{safe_client_name}_SCOPE_OF_WORKS.pdf"
    return gen.save(output_path)
