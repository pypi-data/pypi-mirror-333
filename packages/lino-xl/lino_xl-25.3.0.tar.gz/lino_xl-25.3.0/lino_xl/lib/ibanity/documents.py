# -*- coding: UTF-8 -*-
# Copyright 2025 Rumma & Ko Ltd
# License: GNU Affero General Public License v3 (see file COPYING for details)
# Developer docs: https://dev.lino-framework.org/plugins/peppol.html

# from datetime import datetime
import base64
from dateutil.parser import isoparse
from dateutil import parser as dateparser
from bs4 import BeautifulSoup
from django.utils import timezone
from django.conf import settings
from django.db import models
from lino.api import dd, rt, _
from lino.core import constants
from lino.modlib.linod.models import SystemTasks
from lino.modlib.linod.choicelists import background_task
from lino_xl.lib.accounting.choicelists import VoucherStates, VoucherTypes
from lino_xl.lib.accounting.roles import LedgerStaff
from lino_xl.lib.vat.ui import InvoicesByJournal

try:
    from lino_book import DEMO_DATA
except ImportError:
    DEMO_DATA = None

ibanity = dd.plugins.ibanity
use_sandbox = dd.plugins.ibanity.use_sandbox


def check_supplier(docinfo):
    return docinfo['relationships']['supplier']['data']['id'] == ibanity.supplier_id


def check_doctype(ar, obj, data):
    dt = 'peppolInvoice' if obj.voucher.is_reversal() else 'peppolCreditNote'
    if data['type'] != dt:
        ar.warning("Ibanity response says %s instead of %s in %s",
                   data['type'], dt, data)


def parse_timestamp(s):
    dt = isoparse(s)
    return dt if settings.USE_TZ else timezone.make_naive(dt)


class OutboundStates(dd.ChoiceList):
    verbose_name = _("State")
    verbose_name_plural = _("Outbound document states")
    required_roles = dd.login_required(LedgerStaff)


add = OutboundStates.add_item
add('10', _("Created"), 'created')
add('20', _("Sending"), 'sending')
add('30', _("Sent"), 'sent')
add('40', _("Invalid"), 'invalid')
add('50', _("Send-Error"), 'send_error')


class OutboundErrors(dd.ChoiceList):
    verbose_name = _("State")
    verbose_name_plural = _("Outbound document errors")
    required_roles = dd.login_required(LedgerStaff)


add = OutboundErrors.add_item
add('010', _("Malicious"), 'malicious')
add('020', _("Invalid format"), 'format')
add('030', _("Invalid XML"), 'xsd')
add('040', _("Invalid Schematron"), 'schematron')
add('050', _("Invalid identifiers"), 'identifiers')
add('060', _("Invalid size"), 'size')
add('070', _("Invalid type"), 'invalid_type')
add('080', _("Customer not registered"), 'customer_not_registered')
add('090', _("Type not supported"), 'unsupported')
add('100', _("Access Point issue"), 'access_point')
add('110', _("Unspecified error"), 'unspecified')


class InboundDocument(dd.Model):
    class Meta:
        app_label = 'ibanity'
        verbose_name = _("Inbound document")
        verbose_name_plural = _("Inbound documents")

    allow_cascaded_delete = ['voucher']

    document_id = models.CharField(
        _("DocumentId"), max_length=50, blank=True, editable=False, unique=True)
    transmission_id = models.CharField(
        _("Transmission ID"), max_length=50, blank=True, editable=False)
    created_at = models.DateTimeField(
        _("Created at"), editable=False, null=True)
    voucher = dd.ForeignKey(ibanity.inbound_model, null=True, blank=True)


class Inbox(dd.Table):
    label = _("Inbox")
    model = 'ibanity.InboundDocument'
    filter = models.Q(voucher__isnull=True)
    order_by = ['created_at']
    column_names = "created_at document_id transmission_id *"


class Archive(dd.Table):
    label = _("Archive")
    model = 'ibanity.InboundDocument'
    filter = models.Q(voucher__isnull=False)
    column_names = "voucher voucher__partner voucher__vat_regime voucher__state voucher__entry_date voucher__total_incl *"


dd.inject_field(
    'accounting.Journal', 'is_outbound', models.BooleanField(
        _("Peppol outbound"), default=False))
dd.inject_field(
    'contacts.Partner', 'is_outbound', models.BooleanField(
        _("Peppol outbound"), default=False))
dd.inject_field(
    'contacts.Partner', 'peppol_id', models.CharField(
        _("Peppol ID"), max_length=50, blank=True))


class OutboundInfo(dd.Model):

    class Meta:
        app_label = 'ibanity'
        # verbose_name = _("Outbound document")
        # verbose_name_plural = _("Outbound documents")

    allow_cascaded_delete = 'voucher'
    voucher = dd.OneToOneField(ibanity.outbound_model, primary_key=True)
    document_id = models.CharField(
        _("DocumentId"), max_length=50, blank=True, editable=False)
    created_at = models.DateTimeField(
        _("Created at"), editable=False, null=True)
    outbound_state = OutboundStates.field(editable=False, null=True)
    outbound_error = OutboundErrors.field(editable=False, null=True)
    transmission_id = models.CharField(
        _("Transmission ID"), max_length=50, blank=True, editable=False)

    @dd.displayfield(_("Voucher"))
    def voucher_info(self, ar):
        v = self.voucher
        return f"{v.partner} {v.due_date} {v.total_incl}"


class Outbox(dd.Table):
    label = _("Outbox")
    model = OutboundInfo
    filter = models.Q(created_at__isnull=True)
    column_names = "voucher voucher__partner voucher__vat_regime voucher__entry_date voucher__total_base voucher__total_vat *"


class Sent(dd.Table):
    label = _("Sent")
    model = OutboundInfo
    filter = models.Q(created_at__isnull=False)
    column_names = "voucher voucher__partner created_at outbound_state transmission_id *"


class ReceivedInvoiceDetail(dd.DetailLayout):
    main = "general more"

    general = dd.Panel("""
    general1 general2 general3
    vat.ItemsByInvoice
    """, label=_("General"))

    general1 = """
    number partner
    entry_date
    """

    general2 = """
    source_document
    due_date
    """

    general3 = """
    workflow_buttons
    total_incl
    """

    more = dd.Panel("""
    more1 more2
    vat.MovementsByVoucher
    """, label=_("More"))

    more1 = """
    accounting_period your_ref:20 vat_regime:20
    match journal user
    payment_term
    narration id
    total_base
    total_vat
    """

    more2 = """
    uploads.UploadsByController:60
    """


class ReceivedInvoicesByJournal(InvoicesByJournal):
    detail_layout = ReceivedInvoiceDetail()


VoucherTypes.add_item_lazy(ReceivedInvoicesByJournal)


def collect_outbound(ar):
    # ar.debug("20250215 sync_ibanity %s", ibanity.outbound_model)
    ar.info("Collect outbound invoices into outbox")
    if ibanity.outbound_model is None:
        ar.debug("No outbox on this site.")
        return

    qs = rt.models.accounting.Journal.objects.filter(is_outbound=True)
    if (count := qs.count()) == 0:
        ar.debug("No outbound journals configured")
        return
    ar.debug("Scan %d outbound journal(s): %s ",
             count, [jnl.ref for jnl in qs])

    qs = ibanity.outbound_model.objects.filter(journal__is_outbound=True)
    qs = qs.filter(partner__is_outbound=True)
    qs = qs.filter(state=VoucherStates.registered)
    qs = qs.filter(outboundinfo__isnull=True)
    if (count := qs.count()) == 0:
        ar.debug("No new new invoices for outbox")
        return
    ar.debug("Collect %d new invoices into outbox", count)
    for obj in qs.order_by('id'):
        obj.do_print.run_from_ui(ar)
        OutboundInfo.objects.create(voucher=obj)


def send_outbound(ses, ar):
    ar.info("Send outbound documents")
    if not ibanity.supplier_id:
        ar.debug("This site is not an Ibanity supplier")
    qs = OutboundInfo.objects.filter(created_at__isnull=True)
    if (count := qs.count()) == 0:
        ar.debug("Outbox is empty")
    for obj in qs.order_by('voucher_id'):
        voucher = obj.voucher
        objects_to_save = [obj, voucher]
        ar.debug("Gonna send %s", voucher)
        xmlfile = voucher.make_xml_file(ar)
        ar.debug("Made %s", xmlfile.path)
        res = ses.create_outbound_document(ibanity.supplier_id, xmlfile.path)
        ar.debug("Ibanity response %s", res['data'])
        data = res['data']
        obj.document_id = data['id']
        obj.outbound_state = OutboundStates.get_by_name(
            data['attributes']['status'])
        obj.created_at = parse_timestamp(data['attributes']['createdAt'])
        check_doctype(ar, obj, data)
        voucher.state = VoucherStates.sent
        for obj in objects_to_save:
            obj.full_clean()
        for obj in objects_to_save:
            obj.save()


def followup_outbound(ses, ar):
    ar.info("Check outbound documents")
    if not ibanity.supplier_id:
        ar.debug("This site is not an Ibanity supplier")
    qs = OutboundInfo.objects.filter(created_at__isnull=False)
    qs = qs.exclude(outbound_state__in={OutboundStates.sent})
    if (count := qs.count()) == 0:
        ar.debug("Sent folder is empty")
    for obj in qs.order_by('created_at'):
        res = ses.get_outbound_document(ibanity.supplier_id, obj.document_id)
        data = res['data']
        obj.transmission_id = data['attributes']['transmissionId']
        if not check_supplier(data):
            ar.warning("Oops wrong supplier in %s", data)
        new_state = OutboundStates.get_by_name(data['attributes']['status'])
        if obj.outbound_state != new_state:
            ar.debug("%s (%s) state %s becomes %s",
                     obj.voucher, obj.transmission_id, obj.outbound_state.name,
                     new_state.name)
            obj.outbound_state = new_state
        check_doctype(ar, obj, data)
        obj.full_clean()
        obj.save()


def check_inbox(ses, ar):
    ar.info("Check our inbox")
    if not ibanity.supplier_id:
        ar.debug("This site is not an Ibanity supplier")
    res = ses.list_inbound_documents(ibanity.supplier_id)
    for docinfo in res['data']:
        # [{'attributes': {'createdAt': '...',
        #                  'transmissionId': 'c038dbdc1-26ed-41bf-9ebf-37g3c4ceaa58'},
        #   'id': '431cb851-5bb2-4526-8149-5655d648292f',
        #   'relationships': {'supplier': {'data': {'id': 'de142988-373c-4829-8181-92bdaf8ef26d',
        #                                           'type': 'supplier'}}},
        #   'type': 'peppolInboundDocument'}]
        document_id = docinfo['id']
        if not check_supplier(docinfo):
            if not use_sandbox:
                ar.debug("Ignore doc for other supplier")
                continue
        qs = InboundDocument.objects.filter(document_id=document_id)
        if qs.count() == 0:
            ar.debug("We got a new document %s", document_id)
            InboundDocument.objects.create(
                document_id=document_id,
                transmission_id=docinfo['attributes']['transmissionId'],
                created_at=parse_timestamp(docinfo['attributes']['createdAt']))
        else:
            ar.debug("Document %s is still there", document_id)


def download_inbound(ses, ar):
    if not ibanity.supplier_id:
        ar.debug("This site is not an Ibanity supplier")
        return
    if not ibanity.inbound_journal:
        ar.debug("This site has no inbound journal")
        return
    jnl = rt.models.accounting.Journal.get_by_ref(ibanity.inbound_journal)
    ibanity.inbox_dir.mkdir(exist_ok=True)
    qs = InboundDocument.objects.filter(voucher__isnull=True)
    count = qs.count()
    if count == 0:
        ar.info("No inbound documents to download.")
        return
    ar.info("Download %s inbound documents", count)
    for obj in qs:
        ar.debug("Download %s", obj.document_id)
        xmlfile = ibanity.inbox_dir / f"{obj.document_id}.xml"
        if xmlfile.exists():
            ar.debug("Reuse previously downloaded %s", xmlfile)
            res = xmlfile.read_text()
        else:
            if use_sandbox:
                pth = DEMO_DATA / f"peppol/{obj.document_id}.xml"
                if not pth.exists():
                    ar.warning("Oops, %s does not exist", pth)
                    continue
                res = pth.read_text()
            else:
                res = ses.get_inbound_document_xml(obj.document_id)
                ar.debug("Import %d bytes into %s", len(res), xmlfile)
            xmlfile.write_text(res)

        voucher = create_from_ubl(ar, jnl, res)
        if voucher is None:
            ar.info("Failed to create document from %s", obj.document_id)
        else:
            ar.info("Created %s from %s", voucher, obj.document_id)
            obj.voucher = voucher
            obj.full_clean()
            obj.save()


def create_from_ubl(ar, jnl, xml):
    soup = BeautifulSoup(xml, "xml")
    if (main := soup.find("Invoice")):
        ar.debug("It's an invoice")
    elif (main := soup.find("CreditNote")):
        ar.debug("It's a credit note")
    else:
        ar.warning(f"Invalid XML content {list(soup.children)}")
        return

    assert main.find("cbc:DocumentCurrencyCode").text == "EUR"
    kw = dict()
    kw.update(entry_date=dateparser.parse(main.find("cbc:IssueDate").text))
    kw.update(due_date=dateparser.parse(main.find("cbc:DueDate").text))

    if (ref := main.find("cbc:BuyerReference")) is not None:
        kw.update(your_ref=ref.text)

    if (tot := main.find("cac:LegalMonetaryTotal")) is None:
        ar.warning("No total amount")
        return
    kw.update(total_incl=tot.find("cbc:PayableAmount").text)

    # print(main.find("cbc:IssueDate").prettify())
    # print(main.find("cbc:DueDate").prettify())
    Partner = rt.models.contacts.Partner
    p = main.find("cac:AccountingSupplierParty")
    p = p.find("cac:Party")
    endpoint = p.find("cbc:EndpointID")
    peppol_id = f"{endpoint['schemeID']}:{endpoint.text}"
    name = p.find("cac:PartyName").find("cbc:Name").string
    partner = None
    qs = Partner.objects.filter(peppol_id=peppol_id)
    if qs.count() == 1:
        partner = qs.first()
        if partner.name != name:
            ar.warning("Partner %s name %r != %r",
                       peppol_id, partner.name, name)
    elif qs.count() == 0:
        ar.debug("Unknown Peppol ID %s", peppol_id)
        qs = Partner.objects.filter(name=name)
        if qs.count() == 0:
            ar.info("Create partner %s with Peppol ID %s)",
                    name, peppol_id)
            partner = rt.models.contacts.Company(
                name=name, peppol_id=peppol_id)
            partner.full_clean()
            partner.save()
        elif qs.count() > 1:
            ar.debug("Multiple partners with name %s", name)
        else:
            ar.debug(
                "Assign %s to partner %s because name matches", peppol_id, name)
            partner = qs.first()
            partner.peppol_id = peppol_id
            partner.full_clean()
            partner.save()
    else:
        ar.debug("Multiple partners with Peppol ID %s", peppol_id)
    if partner is None:
        return
    ar.debug("Supplier %s is %s", peppol_id, partner)
    kw.update(partner=partner)
    # p = main.find("cac:AccountingCustomerParty")
    # p = p.find("cac:Party")
    # p = p.find("cbc:EndpointID")
    # print("I am the customer", p)
    # print(main.find("cac:AccountingCustomerParty").prettify())
    # print(str(kw))
    obj = jnl.create_voucher(**kw)
    obj.full_clean()
    obj.save()
    for line in main.find_all("cac:InvoiceLine"):
        # qty = line.find("cbc:InvoicedQuantity").text
        # account_text = line.find("cbc:AccountingCost").text
        # tax_cat = line.find("cac:ClassifiedTaxCategory").ID.text
        desc = line.find("cac:Item").find("cbc:Name").text
        total_base = line.find("cbc:PriceAmount").text
        ar.debug("Lino ignores information in %s %s", desc, total_base)
    obj.after_ui_save(ar, None)
    for adoc in main.find_all("cac:AdditionalDocumentReference"):
        if e := adoc.find("cbc:ID"):
            ar.debug("Lino ignores information in %s", e)
        if desc := adoc.find("cbc:DocumentDescription"):
            desc = desc.string
        if att := adoc.find("cac:Attachment"):
            if e := att.find("cac:ExternalReference"):
                ar.debug("Lino ignores information in %s", e)
            if bo := att.find("cbc:EmbeddedDocumentBinaryObject"):
                ar.debug("Store embedded file (%s) %s",
                         desc, bo['filename'])
                imgdata = base64.b64decode(bo.string)
                obj.store_attached_file(
                   ar, imgdata, bo['mimeCode'], bo['filename'], desc)
    return obj


# @dd.background_task(every_unit="daily", every=1)
@background_task(every_unit="never")
def sync_ibanity(ar):
    collect_outbound(ar)
    ses = ibanity.get_ibanity_session()
    send_outbound(ses, ar)
    followup_outbound(ses, ar)
    check_inbox(ses, ar)
    download_inbound(ses, ar)


class SyncIbanity(SystemTasks):
    label = _("Sync Ibanity")
    help_text = _("Synchronize with Peppol network.")
    required_roles = dd.login_required(LedgerStaff)
    default_record_id = "row"
    default_display_modes = {None: constants.DISPLAY_MODE_DETAIL}
    hide_navigator = True

    @classmethod
    def get_row_by_pk(cls, ar, pk):
        p = rt.models.linod.Procedures.find(func=sync_ibanity)
        return rt.models.linod.SystemTask.objects.get(procedure=p)
