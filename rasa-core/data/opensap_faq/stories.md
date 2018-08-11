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

## conversation meow
* conversation_meow
  - utter_conversation_meow

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
* account_change_email{"email": "frank.gustav-held@company.lt"}
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

## certificate informations
* certificate
  - utter_certificate_info

## difference between channels
* channel_difference
  - utter_channel_difference

## course browsing
* course_browsing
  - utter_course_browsing

## deadline extension
* course_deadline_extension
  - utter_course_deadline_extension

## effort
* course_effort
  - utter_course_effort

## course enrollment after it started
* course_enrollment_after_start
  - utter_course_enrollment_after_start

## self paced mode
* course_self_paced
  - utter_course_self_paced

## course starting time
* course_starting_time
  - utter_course_starting_time

## course structure
* course_structure
  - utter_course_structure

## peer assessment
* course_peer_assessment
  - utter_course_peer_assessment

## unenrollemnt
* course_unenrollment
  - utter_course_unenrollment

## forum contribution
* forum_contribution
  - utter_forum_contribution

## beta functions
* platform_beta
  - utter_platform_beta

## etherpad
* platform_etherpad
  - utter_platform_etherpad

## mobile compability
* platform_mobile
  - utter_platform_mobile

## pricing
* platform_pricing
  - utter_platform_pricing

## target group
* platform_target_group
  - utter_platform_target_group

## technical prerequisites
* platform_technical_prerequisites
  - utter_platform_technical_prerequisites

## how to start
* platform_how_to_start
  - utter_platform_how_to_start