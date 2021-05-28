input_question = '[\n' +
    '  {"tag": "treatment_year",\n' +
    '  "nextques": "DCIS_level",\n' +
    '   "patterns": {"5 year":"5","10 year":"10","15 year":"15"},\n' +
    '   "responses": ["I can predict the recurrence probability of breast cancer, please tell me which year you want to predict",\n' +
    '                 "I would love to help you, Can you tell me your treatment time" ,\n' +
    '                 "Could you tell me hwo long you have had breast cancer"]\n' +
    '  },\n' +

    '  {"tag": "DCIS_level",\n' +
    '  "nextques": "size",\n' +
    '  "patterns": {"DCIS_level0":"0","DCIS_level1":"1","DCIS_level2":"2","DCIS_level3":"3", "DCIS_level4":"4","DCIS_level5":"5","DCIS_level6":"6", "DCIS_level7":"7","DCIS_leve8":"8"},\n' +
    '  "responses": ["What is your DCIS_level?","Could you tell me your DCIS_level"]' +
    '  },\n' +

     '  {"tag": "size",\n' +
    '  "nextques": "grade",\n' +
    '  "patterns": {"size0":"0","size1":"1","size2":"2"},\n' +
    '  "responses": ["What is your tumor size?","Could you tell me your tumor size"]' +
    '  },\n' +

    // '  {"tag": "race",\n' +
    // '  "nextques": "menopause_status",\n' +
    // '  "patterns": ["Asian", "American Indian","Hispanic or Latino","White" ],\n' +
    // '  "responses": ["What is your race?"]' +
    // '  },\n' +

    // '  {"tag": "menopause_status",\n' +
    // '  "nextques": "none",\n' +
    // '  "patterns": ["0", "1","2"],\n' +
    // '  "responses": ["What is your menopause_status?"]' +
    // '  }\n' +
    '  {"tag": "grade",\n' +
    '  "nextques": "PR_percent",\n' +
    '  "patterns": {"grade0":"0","grade1":"1","grade2":"2"},\n' +
    '  "responses": ["What is your tumor grade?","Could you tell me your grade"]' +
    '  },\n' +

    '  {"tag": "PR_percent",\n' +
    '  "nextques": "invasive_tumor_Location",\n' +
    '  "patterns": {"PR_percent0":"0", "PR_percent1":"1","PR_percent2":"2"},\n' +
    '  "responses": ["What is your PR_percent?","Could you tell me your PR_PERCENT?"]' +
    '  },\n' +



    '  {"tag": "invasive_tumor_Location",\n' +
    '  "nextques": "none",\n' +
    '  "patterns": {"invasive_tumor_Location0":"0", "invasive_tumor_Location1":"1","invasive_tumor_Location2":"2"},\n' +
    '  "responses": ["What is your invasive_tumor_Location?","Could you tell me your invasive_tumor_Location?"]' +
    '  }\n' +


    ']';

