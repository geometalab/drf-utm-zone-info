from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.utils.translation import gettext as _

from osmaxx.excerptexport.models import extraction_order, ExtractionOrderState
from osmaxx.excerptexport.services.shortcuts import get_authenticated_api_client
from osmaxx.utilities.shortcuts import Emissary


def tracker(request, order_id):
    order = get_object_or_404(extraction_order.ExtractionOrder, pk=order_id)
    order.progress_url = request.GET['status']
    order.save()
    client = get_authenticated_api_client()
    client.update_order_status(order)

    emissary = Emissary(recipient=order.orderer)

    substitutions = dict(
        order_id=order.id,
        excerpt_name=order.excerpt_name,
        order_state=ExtractionOrderState.label(order.state),
    )

    if order.are_downloads_ready:
        message = _(
            'The extraction of the order #{order_id} "{excerpt_name}" has been finished.'
        ).format(**substitutions)

        finished_email_subject = _('Extraction Order #{order_id} "{excerpt_name}" finished').format(**substitutions)
        finished_email_body = _(
            'The extraction order #{order_id} "{excerpt_name}" has been finished and is ready for retrieval.'
        ).format(**substitutions)

        emissary.success(message)
        emissary.inform_mail(subject=finished_email_subject, mail_body=finished_email_body)
    elif order.state == ExtractionOrderState.FAILED:
        message = _(
            'The extraction order #{order_id} "{excerpt_name}" has failed. Please try again later.'
        ).format(**substitutions)

        finished_email_subject = _('Extraction Order #{order_id} "{excerpt_name}" failed').format(**substitutions)
        finished_email_body = _(
            'The extraction order #{order_id} "{excerpt_name}" could not be completed, please try again later.'
        ).format(**substitutions)

        emissary.error(message)
        emissary.inform_mail(subject=finished_email_subject, mail_body=finished_email_body)
    else:
        message = _('Extraction order #{order_id} "{excerpt_name}" is now {order_state}.').format(**substitutions)
        emissary.info(message)
    response = HttpResponse('')
    response.status_code = 200
    return response
