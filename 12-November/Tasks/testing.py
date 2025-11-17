# # import json
# from reminder_service import llm, task_extract_template,set_task_reminders
# #
# # sample_analysis = """
# # ### ✅ 3. Action Items and Responsibilities
# # - Task: Finalize UI/UX design, Person: Soham, Deadline: Nov 14
# # - Task: Backend-Frontend integration, Person: Rohit, Deadline: Nov 22
# # - Task: Marketing content & teaser video, Person: Revksky, Deadline: Nov 25
# # """
# #
# # # Invoke LLM
# # result = llm.invoke(task_extract_template.format(analysis_text=sample_analysis))
# # tasks_json = result.content
# #
# # # Remove Markdown code block if present
# # if tasks_json.startswith("```"):
# #     tasks_json = "\n".join(tasks_json.strip().split("\n")[1:-1])  # remove first and last line
# #
# # print("Cleaned JSON:\n", tasks_json)
# #
# # # Parse JSON
# # try:
# #     tasks = json.loads(tasks_json)
# # except Exception as e:
# #     print("Failed to parse LLM JSON:", e)
# #     tasks = []
# #
# # # Test email lookup
# # from reminder_service import get_email_by_name
# #
# # for t in tasks:
# #     email = get_email_by_name(t["person"])
# #     if email:
# #         print(f"Would create event for {email} | Task: {t['task']} | Deadline: {t['deadline']}")
# #     else:
# #         print(f"⚠️ No email found for {t['person']}")
#
#
# sample_analysis = """
# - Task: Finalize UI/UX design, Person: Soham, Deadline: Nov 14
# - Task: Backend-Frontend integration, Person: Rohit, Deadline: Nov 22
# - Task: Marketing content & teaser video, Person: Revksky, Deadline: Nov 25
# """
#
# # Call your function
# set_task_reminders(sample_analysis)


from reminder_service import set_task_reminders

sample_analysis = """
### ✅ 3. Action Items and Responsibilities
- Task: Finalize UI/UX design, Person: Soham, Deadline: Nov 14
- Task: Backend-Frontend integration, Person: Rohit, Deadline: Nov 22
- Task: Marketing content & teaser video, Person: Revksky, Deadline: Nov 25
"""

set_task_reminders(sample_analysis)
