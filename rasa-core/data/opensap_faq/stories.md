## welcome
* conversation_greet
  - utter_conversation_greet
  - utter_conversation_offer_help

## goodbye
* conversation_goodbye
  - utter_conversation_goodbye

## thanks
* conversation_thank_you
  - utter_conversation_youre_welcome

## notification settings
* account_settings_notifications
  - utter_account_notification_settings

## change email
* account_change_email
  - utter_ask_new_email
* account_provide_email{"email": "peter@sap.com"}
  - slot{"email": "peter@sap.com"}
  - utter_ask_new_email_confirmed
> cp_account_check_email

## change email 2
* account_change_email_to{"email": "frank.gustav-held@company.lt"}
  - slot{"email": "frank.gustav-held@company.lt"}
  - utter_ask_new_email_confirmed
> cp_account_check_email

## confirm email
> cp_account_check_email
* conversation_confirm
  - utter_account_changed_email

## cancel email change
> cp_account_check_email
* conversation_cancel
  - utter_conversation_canceled

## account deletion
* account_deletion
  - utter_account_deletion

## registration problems
* account_activation
  - utter_account_registration_problem

## sap id
* account_sap_id
  - utter_account_sap_id