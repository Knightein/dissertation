import base64
import json
import time

import vertexai
from flask import request
from flask_login import current_user
from vertexai.generative_models import GenerativeModel, Part, FinishReason
import vertexai.preview.generative_models as generative_models

from app import db
from models import Grade, encrypt, User


def generate(challenge, code):
    vertexai.init(project="axial-glow-420413", location="europe-west2")
    model = GenerativeModel("gemini-1.0-pro-vision-001")
    responses = model.generate_content(
        [fine_tuned_text(challenge, code)],
        generation_config=generation_config,
        safety_settings=safety_settings,
        stream=False,
    )
    print(responses.text)
    # Clean the text response removing ` and json
    clean_text = responses.text.strip()
    clean_text = clean_text.replace("```", "")
    clean_text = clean_text.replace("json", "")

    # Try parsing the response as JSON
    try:
        data = json.loads(clean_text)
        assignment_correct = data["assignment_correct"]
        feedback = data["feedback"]
        next_steps = data["next_steps"]

        # Create a new grade (DB)
        postkey = User.query.filter_by(id=current_user.id).first().postkey
        student_id = current_user.id

        new_grade = Grade(
            assignment_id=request.form.get("assignment_id"),
            student_id=student_id,
            grade="U",  # U for unmarked
            correct=assignment_correct,
            feedback=feedback,
            next_steps=next_steps,
            # Encrypt the code submission for security
            code_submission=encrypt(code, postkey)
        )

        db.session.add(new_grade)
        db.session.commit()
        print("Successfully uploaded LLM response to database.")

        # Print the parsed data for DEBUGGING
        print("---")
        print(f"Correct: {assignment_correct}")
        print(f"Feedback: {feedback}")
        print(f"Next Steps: {next_steps}")
        print("---")

    # Handle JSON parsing errors
    except json.JSONDecodeError:
        print(f"Error: Could not parse response as JSON: {clean_text}")


def text(challenge, code):
    return """Taking the challenge \"%s\"

    How well does this code solve the challenge? 
    Replace true in assignment_correct with a boolean value. 
    True if the code solves the challenge, false otherwise.

    ```
    %s
    ```

    Respond in this JSON format:
    {
        \"assignment_correct\": true,
        \"feedback\": \"\",
        \"next_steps\": \"\"
    }""" % (challenge, code)


def fine_tuned_text(challenge, code):
    return """Taking the challenge \"%s\"

    How well does this code solve the challenge?
    Please provide detailed feedback including any errors or issues in the code,
    and how can the code be improved to solve the challenge.
    
    Make sure you explain in detail the next steps to improve the code.
    
    Replace true in assignment_correct with a boolean value. 
    True if the code solves the challenge, false otherwise.

    ```
    %s
    ```

    Respond in this JSON format:
    {
        \"assignment_correct\": true,
        \"feedback\": \"\",
        \"next_steps\": \"\"
    }""" % (challenge, code)


generation_config = {
    "max_output_tokens": 2048,
    "temperature": 0.4,
    "top_p": 0.4,
}

safety_settings = {
    generative_models.HarmCategory.HARM_CATEGORY_HATE_SPEECH: generative_models.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
    generative_models.HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: generative_models.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
    generative_models.HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: generative_models.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
    generative_models.HarmCategory.HARM_CATEGORY_HARASSMENT: generative_models.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
}
