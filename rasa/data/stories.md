## question-first-lesson
* first-lesson
  - action_first-lesson

## question-next-lesson-subject
* next-lesson
  - action_next-lesson

## question-next-lesson-subject-and-room
* next-lesson
  - action_next-lesson
* lesson-room
  - action_get-lesson-room

## question-next-lesson-time
* next-lesson-time
  - action_next-lesson-time

## question-next-lesson-time-and-room
* next-lesson-time
  - action_next-lesson-time
* lesson-room
  - action_get-lesson-room

## question-lesson-room-subject provided
* lesson-room{"subject": "Maths"}
  - action_get-lesson-room

## question-lesson-room-subject set
* lesson-room
  - action_subject-set
  - slot{"subject-set": true}
  - slot{"subject": "Maths"}
  - action_get-lesson-room

## question-lesson-room-subject-not set
* lesson-room
  - action_subject-set
  - slot{"subject-set": false}
  - utter_ask-subject
* inform{"subject": "Maths"}
  - slot{"subject": "Maths"}
  - action_get-lesson-room

## question-lesson-time-start-subject provided
* lesson-time-start{"subject": "Maths"}
  - action_get_lesson_time_start

## question-lesson-time-start-subject set
* lesson-time-start
  - action_subject-set
  - slot{"subject-set": true}
  - action_get_lesson_time_start

## question-lesson-time-start-subject-not set
* lesson-time-start
  - action_subject-set
  - slot{"subject-set": false}
  - utter_ask-subject
* inform{"subject": "Maths"}
  - slot{"subject": "Maths"}
  - action_get_lesson_time_start

## question-lesson-time-end-subject provided
* lesson-time-end{"subject": "Maths"}
  - action_get_lesson_time_end

## question-lesson-time-end-subject set
* lesson-time-end
  - action_subject-set
  - slot{"subject-set": true}
  - action_get_lesson_time_end

## question-lesson-time-end-subject-not set
* lesson-time-end
  - action_subject-set
  - slot{"subject-set": false}
  - utter_ask-subject
* inform{"subject": "Maths"}
  - action_get_lesson_time_end

## question-school-ends
* school-ends
  - action_school-ends

## question-news
* news
  - action_get-news

## question-article-details
* article-details
  - utter_show-news-details



