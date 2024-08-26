from typing_extensions import override
from openai import AssistantEventHandler, OpenAI
import os
from dotenv import load_dotenv
import json
import pickle
import pandas as pd 

load_dotenv()
API_KEY = os.getenv("GPT_API")

try:
    client = OpenAI(
        api_key=API_KEY)
except:
    print("Client did not initialize, exiting")
    pass
def pd_length_print(pd_array):
    return sum(pd_array.map(lambda x : len(x)))
 
json_file = client.files.create(
  file=open("templates.json", "rb"),
  purpose="assistants"
)

sorted_data : pd.DataFrame = pd.read_pickle("../../ISIDM/sorted_references.pkl")
print(sorted_data)

assistant = client.beta.assistants.create(
    name="Reference to Json Bib Converter",
    instructions="You are an expert schollar that is capable of formatting direct references into json formated bib references.",
    model="gpt-4o",
    tools=[{"type": "file_search"}],
)

# Create a vector store caled "Financial Statements"
vector_store = client.beta.vector_stores.create(name="Json bib references")
 
# Ready the files for upload to OpenAI
file_paths = ["templates.json", ]
file_streams = [open(path, "rb") for path in file_paths]
 
# Use the upload and poll SDK helper to upload the files, add them to the vector store,
# and poll the status of the file batch for completion.
file_batch = client.beta.vector_stores.file_batches.upload_and_poll(
  vector_store_id=vector_store.id, files=file_streams
)
 
# You can print the status and the file counts of the batch to see the result of this operation.
print(file_batch.status)
print(file_batch.file_counts)

assistant = client.beta.assistants.update(
  assistant_id=assistant.id,
  tool_resources={"file_search": {"vector_store_ids": [vector_store.id]}},
)


# thread = client.beta.threads.create(
#   messages=[
#     {
#       "role": "user",
#       "content": "What are the different types of references listed in this document?",
#       # Attach the new file to the message.
#       "attachments": [
#         { "file_id": json_file.id, "tools": [{"type": "file_search"}] }
#       ],
#     }
#   ]
# )
 
# The thread now has a vector store with that file in its tool resources.
# print(thread.tool_resources.file_search)

# with client.beta.threads.runs.stream(
#     thread_id=thread.id,
#     assistant_id=assistant.id,
#     instructions="Please address the user as User. The user has a premium account.",
#     event_handler=EventHandler(),
# ) as stream:
#     stream.until_done()

thread = client.beta.threads.create(
  messages=[
    {
      "role": "user",
      "content": [
        {
          "type": "text",
          "text": "Based on the reference templates listed in the attached file, can you format the entire list of references into bib text references"
        },
        {
          "type": "text",
          "text": json_conv
        },
      ],
        "attachments": [
        { "file_id": json_file.id, "tools": [{"type": "file_search"}] }
      ],
    }
  ]
)