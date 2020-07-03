from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.utils.translation import ugettext as _
from django.views.decorators.vary import vary_on_headers
from wagtail.admin import messages
from wagtail.admin.forms.search import SearchForm
from wagtail.admin.utils import PermissionPolicyChecker, popular_tags_for_model
from wagtail.core.models import Collection
from wagtail.search.backends import get_search_backends

from wagtailvideos import ffmpeg
from wagtailvideos.forms import VideoTranscodeAdminForm, VideoChannelForm
from wagtailvideos.models import Channels as Channel
from wagtailvideos.permissions import permission_policy

permission_checker = PermissionPolicyChecker(permission_policy)


@permission_checker.require_any('add', 'change', 'delete')
@vary_on_headers('X-Requested-With')
def index(request):
    # Get Videos (filtered by user permission)
    channels = Channel.objects.all()

    # Search
    query_string = None
    if 'q' in request.GET:
        form = SearchForm(request.GET, placeholder=_("Search Channel"))
        if form.is_valid():
            query_string = form.cleaned_data['q']

            channels = channels.search(query_string)
    else:
        form = SearchForm(placeholder=_("Search Channel"))


    paginator = Paginator(channels, per_page=25)
    page = paginator.get_page(request.GET.get('p'))

    # Create response
    if request.is_ajax():
        response = render(request, 'wagtailvideos/channels/results.html', {
            'channels': page,
            'query_string': query_string,
            'is_searching': bool(query_string),
        })
        return response
    else:
        response = render(request, 'wagtailvideos/channels/index.html', {
            'channels': page,
            'query_string': query_string,
            'is_searching': bool(query_string),

            'search_form': form,
            'popular_tags': popular_tags_for_model(Channel),
        })
        return response


@permission_checker.require('change')
def edit(request, channel_id):
    channel = get_object_or_404(Channel, id=channel_id)

    if request.POST:
        form = VideoChannelForm(request.POST, instance=channel)
        if form.is_valid():
            channel = form.save()

            # Reindex the image to make sure all tags are indexed
            for backend in get_search_backends():
                backend.add(channel)

            messages.success(request, _("Channel '{0}' updated.").format(channel.title), buttons=[
                messages.button(reverse('wagtailvideos:channel_edit', args=(channel.id,)), _('Edit again'))
            ])
            return redirect('wagtailvideos:channels_index')
        else:
            messages.error(request, _("The channel could not be saved due to errors."))
    else:
        form = VideoChannelForm(instance=channel)

    return render(request, "wagtailvideos/channels/edit.html", {
        'channel': channel,
        'form': form,
        'user_can_delete': permission_policy.user_has_permission_for_instance(request.user, 'delete', Channel)
    })



@permission_checker.require('delete')
def delete(request, channel_id):
    channel = get_object_or_404(Channel, id=channel_id)

    if request.POST:
        try:
            channel.delete()
            messages.success(request, _("Channel '{0}' deleted.").format(channel.title))
            return redirect('wagtailvideos:channels_index')
        except Exception as ex:
            messages.error(request, _("{0}").format(str(ex)))

    return render(request, "wagtailvideos/channels/confirm_delete.html", {
        'channel': channel,
    })


@permission_checker.require('add')
def add(request):
    if request.POST:
        form = VideoChannelForm(request.POST)
        if form.is_valid():
            channel = form.save()
            # Success! Send back an edit form
            for backend in get_search_backends():
                backend.add(channel)

            messages.success(request, _("Channel '{0}' added.").format(channel.title), buttons=[
                messages.button(reverse('wagtailvideos:channel_edit', args=(channel.id,)), _('Edit'))
            ])
            return redirect('wagtailvideos:channels_index')
        else:
            messages.error(request, _("The channel could not be created due to errors."))
    else:
        form = VideoChannelForm()

    return render(request, "wagtailvideos/channels/add.html", {
        'form': form,
    })
