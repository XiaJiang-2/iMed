input_question = '[\n' +
    '  {"tag": "treatment_year",\n' +
    '  "nextques": "race",\n' +
    '   "patterns": ["5 year", "10 year", "15 year"],\n' +
    '   "responses": ["I can predict the recurrence probability of breast cancer, please tell me which year you want to predict",\n' +
    '                 "Could you tell me hwo long you have had breast cancer"]\n' +
    '  },\n' +

    '  {"tag": "race",\n' +
    '  "nextques": "menopause_status",\n' +
    '  "patterns": ["Asian", "American Indian","Hispanic or Latino","White" ],\n' +
    '  "responses": ["What is your race?"]' +
    '  },\n' +

    '  {"tag": "menopause_status",\n' +
    '  "nextques": "none",\n' +
    '  "patterns": ["0", "1","2"],\n' +
    '  "responses": ["What is your menopause_status?"]' +
    '  }\n' +

    ']';

