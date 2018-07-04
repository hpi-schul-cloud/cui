from rasa_core.actions.forms import FormAction, EntityFormField, BooleanFormField
from rasa_core.events import SlotSet

class ActionEmailForm(FormAction):

    RANDOMIZE = False

    @staticmethod
    def required_fields():
        return [
            EntityFormField("email", "new_email"),
            BooleanFormField("new_email_confirmed", "conversation_confirm", "conversation_cancel")
        ]

    def name(self):
        return 'action_email_form'
    
    def submit(self, dispatcher, tracker, domain):
        email = tracker.get_slot("new_email")
        confirmed = tracker.get_slot("new_email_confirmed")

        tracker.update(SlotSet("new_email"))
        tracker.update(SlotSet("new_email_confirmed"))