input_question =
    '  {' +
    '"START":[{"tag": "Instruction",\n' +
    ' "instruction": "We can either predict the probability of recurrence or help you train a model online.",\n' +
    '  "nextques": "Predict or Train a Model",\n' +
    '   "patterns": {"Predict":"1","Train a Model":"2"},\n' +
    '   "responses": ["I can either predict breast cancer metastasis for your patient based on our deep learning models trained using one existing dataset,or I can train a model for you if you can provide your own dataset, so how do you want to proceed?Please enter 1 for the first choice, or 2 for the second choice"]\n'+
    '  }],\n' +

    '"Predict": [' +
    '{"tag": "treatment_year",\n' +
    ' "instruction": "Please choose the treatment year",\n' +
    '  "nextques": "DCIS_level",\n' +
    '   "patterns": {"5 year":"5","10 year":"10","15 year":"15"},\n' +
    '   "responses": ["I can predict the recurrence probability of breast cancer, please tell me which year you want to predict",\n' +
    '                 "I would love to help you, Can you tell me your treatment time" ,\n' +
    '                 "Could you tell me how long you have had breast cancer?"]\n' +
    '  },\n' +
    '  {"tag": "DCIS_level",\n' +
    ' "instruction": "Choose the type of ductal carcinoma in situ. Ductal carcinoma in situ (DCIS) is the presence of abnormal cells inside a milk duct in the breast. DCIS is considered the earliest form of breast cancer. DCIS is noninvasive, meaning it has not spread out of the milk duct to invade other parts of the breast. ",\n' +
    '  "nextques": "size",\n' +
    '  "patterns": {"solid":"0","apocrine":"4","cribriform":"3","dcis":"5", "comedo":"2","papillary":"6","micropapillary":"8","micropapillalry":"7","not present":"1"},\n' +
    '  "responses": ["What is your DCIS_level?","Could you tell me your DCIS_level"]' +
    '  },\n' +



     '  {"tag": "size",\n' +
   ' "instruction": "Size of tumor is measured in mm.",\n' +
    '  "nextques": "grade",\n' +
    '  "patterns": {"0-32":"0","32-70":"1","greater than 70":"2"},\n' +
    '  "responses": ["What is your tumor size?","Could you tell me your tumor size"]' +
    '  },\n' +

    // '  {"tag": "race",\n' +
    //' "instruction": "treatment_year instruction",\n' +
    // '  "nextques": "menopause_status",\n' +
    // '  "patterns": ["Asian", "American Indian","Hispanic or Latino","White" ],\n' +
    // '  "responses": ["What is your race?"]' +
    // '  },\n' +

    // '  {"tag": "menopause_status",\n' +
    //' "instruction": "treatment_year instruction",\n' +
    // '  "nextques": "none",\n' +
    // '  "patterns": ["0", "1","2"],\n' +
    // '  "responses": ["What is your menopause_status?"]' +
    // '  }\n' +
    '  {"tag": "grade",\n' +
    '  "instruction": "Grade of disease: grade 1 – looks most like normal breast cells and is usually slow-growing; grade 2 – looks less like normal cells and is growing faster; grade 3 – looks different to normal breast cells and is usually fast-growing",\n' +
    '  "nextques": "PR_percent",\n' +
    '  "patterns": {"grade1":"0","grade2":"1","grade3":"2"},\n' +
    '  "responses": ["What is your tumor grade?","Could you tell me your grade"]' +
    '  },\n' +

    '  {"tag": "PR_percent",\n' +
    '  "instruction": "Receptors are proteins that attach to certain substances. Progesterone receptor (PR) tests look for receptors that attach to the hormones estrogen and progesterone in a sample of breast cancer tissue. PR Percent means percent of cell stain positive for PR receptors",\n' +
    '  "nextques": "invasive_tumor_Location",\n' +
    '  "patterns": {"0-20":"2", "20-90":"1","90-100":"0"},\n' +
    '  "responses": ["What is your PR_percent?","Could you tell me your PR_PERCENT?"]' +
    '  },\n' +

    '  {"tag": "invasive_tumor_Location",\n' +
    '  "instruction": "Where invasive tumor is located. Ductal means an overgrowth of the cells that line the small tubes (ducts) inside the breast, while lobular is an overgrowth of cell lining the milk glands (lobules).",\n' +
    '  "nextques": "none",\n' +
    '  "patterns": {"mixed duct and lobular":"1", "duct":"0","lobular":"2","none":"3"},\n' +
    '  "responses": ["What is your invasive_tumor_Location?","Could you tell me your invasive_tumor_Location?"]' +
    '  }],\n' +

      '"Train a Model":[{"tag": "choice2",\n' +
    ' "instruction": "Browse data",\n' +
    '  "nextques": "View your dataset",\n' +
    '   "patterns": {"Example Dataset":"1","Browse Local":"2"},\n' +
    '   "responses": ["Please review the demo dataset first and upload your local dataset, only .txt and .csv format are permitted"]'+
    '  },' +
    '{"tag": "View your dataset",\n' +
    ' "instruction": "View your dataset",\n' +
    '  "nextques": "",\n' +
    '   "patterns": {"View your dataset":"1"},\n' +
    '   "responses": ["Please check the chuhan dataset you uploaded and it will give your some basic stats"]'+
    '  }]\n'+
    '}'