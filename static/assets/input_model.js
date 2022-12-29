input_question_model = '[\n' +
    '  {"tag": "Instruction",\n' +
    ' "instruction": "treatment_year instruction",\n' +
    '  "nextques": "DCIS_level",\n' +
    '   "patterns": {"Choice 1":"1","Choice 2":"2"},\n' +
    '   "responses": ["I can either predict breast cancer metastasis for your patient based on our deep learning models trained using one existing dataset,or I can train a model for you if you can provide your own dataset, so how do you want to proceed?Please enter 1 for the first choice, or 2 for the second choice"]'+
    '  },\n' +


    '  {"tag": "grade",\n' +
    '  "instruction": "grade instruction",\n' +
    '  "nextques": "PR_percent",\n' +
    '  "patterns": {"grade0":"0","grade1":"1","grade2":"2"},\n' +
    '  "responses": ["What is your tumor grade?","Could you tell me your grade"]' +
    '  },\n' +

    '  {"tag": "PR_percent",\n' +
    '  "instruction": "PR_percent instruction",\n' +
    '  "nextques": "invasive_tumor_Location",\n' +
    '  "patterns": {"PR_percent0":"0", "PR_percent1":"1","PR_percent2":"2"},\n' +
    '  "responses": ["What is your PR_percent?","Could you tell me your PR_PERCENT?"]' +
    '  },\n' +



    '  {"tag": "invasive_tumor_Location",\n' +
    '  "instruction": "invasive_tumor_Location instruction",\n' +
    '  "nextques": "none",\n' +
    '  "patterns": {"invasive_tumor_Location0":"0", "invasive_tumor_Location1":"1","invasive_tumor_Location2":"2"},\n' +
    '  "responses": ["What is your invasive_tumor_Location?","Could you tell me your invasive_tumor_Location?"]' +
    '  }\n' +


    ']';

