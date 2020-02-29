class OnboardingTutorial:
    """Constructs the onboarding message and stores the state of which tasks were completed."""

    WELCOME_BLOCK = {
        "type": "section",
        "text": {
            "type": "mrkdwn",
            "text": (
                "Jumpman, Jumpman, I don't need no introduction. :basketball: \n\n"
                "*Here are a few things Shot Clock could help with:*"
            ),
        },
    }
    DIVIDER_BLOCK = {"type": "divider"}

    def __init__(self, channel):
        self.channel = channel
        self.username = "Shot Clock"
        # self.icon_emoji = ":basketball:"
        self.timestamp = ""
        self.reaction_task_completed = False
        self.pin_task_completed = False

    def get_message_payload(self):
        return {
            "ts": self.timestamp,
            "channel": self.channel,
            "username": self.username,
            # "icon_emoji": self.icon_emoji,
            "blocks": [
                self.WELCOME_BLOCK,
                self.DIVIDER_BLOCK,
                *self._greetings_block(),
                self.DIVIDER_BLOCK,
                *self._get_schedule_block(),
            ],
        }

    def _greetings_block(self):
        # task_checkmark = self._get_checkmark(self.reaction_task_completed)
        text = (
            f" *Our whole universe was in a hot, dense state...* :handshake:\n"
            "That all started with the big bang! Hey!\n"
            "It all starts with a simple \"hey_\" (or _hello_, _hi_, or even \"SUP\" "
            "- if you are feeling extra cool today. :sunglasses:) "
            "Say your greetings with a hashtag e.g. `#hello` - Shot Clock will do the same."
        )
        return self._get_task_block(text) #, information)

    def _get_schedule_block(self):
        # task_checkmark = self._get_checkmark(self.pin_task_completed)
        text = (
            f"*Hey Google, ...* :speaker:\n"
            "\", is the Rockets playing tonight?\"\n"
            "Ask Shot Clock the same question `is [YOUR TEAM NAME] playing` "
            "- it'll tell you when to grab a beer and turn on the TV."
        )
        return self._get_task_block(text) # , information)

    @staticmethod
    def _get_checkmark(task_completed: bool) -> str:
        if task_completed:
            return ":white_check_mark:"
        return ":white_large_square:"

    @staticmethod
    def _get_task_block(text):
        return [
            {"type": "section", "text": {"type": "mrkdwn", "text": text}},
           # {"type": "context", "elements": [{"type": "mrkdwn", "text": information}]},
        ]