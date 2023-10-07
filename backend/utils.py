from django.contrib.auth.models import User
from django.urls import reverse
import os, json


def load_navbar_items():
    json_file_path = os.path.join(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
        "frontend/templates/core/partials/base/navbar/items.json",
    )

    with open(json_file_path) as json_file:
        navbar_items = json.load(json_file)

    return navbar_items


class Toast:
    def __init__(
        self,
        title,
        message,
        level="info",
        time=5000,
        autohide=True,
        delay=None,
        icon=None,
        progress=False,
        request=None,
    ):
        self.title = title
        self.message = message
        self.level = level
        self.time = time
        self.autohide = autohide
        self.delay = delay
        self.icon = icon
        self.progress = progress
        self.request = request

        if self.request is not None:
            self.add_to_request(self.request)

    def add_to_request(self, request):
        toasts = request.session.get("toasts", [])
        toasts.append(
            {
                "title": self.title,
                "message": self.message,
                "level": self.level,
                "time": self.time,
                "autohide": self.autohide,
                "delay": self.delay,
                "icon": self.icon,
                "progress": self.progress,
            }
        )
        request.session["toasts"] = toasts

    @staticmethod
    def get_from_request(request):
        toasts = request.session.get("toasts", [])
        request.session["toasts"] = []
        return toasts


class Toasts:
    def refresh(self):
        return {
            "title": "Page is outdated",
            "level": "warning",
            "text": "Your page is out of date. Please <a href='#' onclick='location.reload();return false;'>Click here to refresh</a>.",
            "position": "top-center",
        }


TOASTS = Toasts()


class Modals:
    @staticmethod
    def example(
        id="create_customer",
        success_message="Customer created with the name of ${$('#nameInput').val()}",
        toasts=[TOASTS.refresh()],
    ):
        return {}

    @staticmethod
    def change_profile_picture():
        return {
            "id": "modal_change_profile_picture",
            "title": "Change Profile Picture",
            "action": {
                "text": "Save",
                "method": "post",
                "extra": f"enctype=multipart/form-data #",  # hx-post={reverse_lazy('api v1 receipts new')} hx-target=#items hx-refresh=true",
                "fields": [
                    {
                        "type": "file",
                        "name": "profile_image",
                        "required": False,
                        "extra": "accept=image/png,image/jpeg",
                    }
                ],
            },
        }

    @staticmethod
    def create_team():
        return {
            "id": "modal_create_team",
            "title": "Create Team",
            "action": {
                "text": "Save",
                "method": "post",
                "href": reverse("user settings teams create"),
                # "extra": f"enctype=multipart/form-data",  # hx-post={reverse_lazy('api v1 receipts new')} hx-target=#items hx-refresh=true",
                "fields": [
                    {
                        "text": "Name your team",
                        "type": "text",
                        "placeholder": "The best team ever",
                        "name": "name",
                        "label" "required": True,
                    }
                ],
            },
        }

    @staticmethod
    def invite_user_to_team():
        return {
            "id": "modal_invite_user_to_team",
            "title": "Invite User",
            "action": {
                "text": "Send",
                "method": "post",
                "href": reverse("user settings teams invite"),
                # "extra": f"enctype=multipart/form-data",  # hx-post={reverse_lazy('api v1 receipts new')} hx-target=#items hx-refresh=true",
                "fields": [
                    {
                        "type": "text",
                        "name": "user_email",
                        "required": True,
                        "label": "Users Email",
                        "placeholder": "bob@example.com",
                    }
                ],
            },
        }

    @staticmethod
    def invited_to_team_accept(invitation):
        return {
            "id": "invited_to_team_accept",
            "title": f"Are you sure you would like to join <strong>{invitation.team.name}</strong> team?",
            "action": {
                "text": "Accept",
                "method": "post",
                "href": reverse(
                    "user settings teams join accept", kwargs={"code": invitation.code}
                ),
                "fields": [],
            },
        }

    @staticmethod
    def invited_to_team_decline(invitation):
        return {
            "id": "invited_to_team_decline",
            "title": f"Are you sure you would like to <u>decline</u> <strong>{invitation.team.name}</strong> teams invitation?",
            "action": {
                "text": "Decline",
                "color": "error",
                "method": "post",
                "href": reverse(
                    "user settings teams join decline", kwargs={"code": invitation.code}
                ),
                "fields": [
                    {
                        "type": "text",
                        "name": "confirmation_text",
                        "required": True,
                        "label": f'Please type "i confirm i want to decline {invitation.team.name}" ',
                        "placeholder": "please type the message above to confirm",
                    }
                ],
            },
        }

    @staticmethod
    def team_kick_user(user: User):
        return {
            "id": f"team_kick_user_{user.id}",
            "title": f'<p class="text-sm">Are you sure you would like to <u>kick</u> <strong>{user.username}</strong> from your team?</p>',
            "action": {
                "text": "Decline",
                "color": "error",
                "method": "post",
                "href": reverse(
                    "user settings teams kick", kwargs={"user_id": user.id}
                ),
                "fields": [
                    {
                        "type": "text",
                        "name": "confirmation_text",
                        "required": True,
                        "label": f'Please type "i confirm i want to kick {user.username}"',
                        "placeholder": "please type the message above to confirm",
                    }
                ],
            },
        }
