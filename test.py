import perplexity

cookies = {
    'pplx.visitor-id': 'a708621e-c83b-4453-8763-f0d7f075986a',
    'pplx.session-id': '69312f60-388b-4c15-94da-d9ce9ca1a292',
    '__cflb': '02DiuDyvFMmK5p9jVbVnMNSKYZhUL9aGmKaa5e4DZaVd6',
    'cf_clearance': 'I0cjtmC5xF.702gN0DBjUeJl_FNJI6h37FBkI8_IDlI-1749821658-1.2.1.1-BTClaKezyACtLYwRJ8.1RAXwWbz7o2arWCoghHLHX.U.Zrzg6Fc9hi6JVv7Q3TRvQG9YvzkNJr6exiaP6ybjpEnDYk5SU67KaADWsFHyTpdRzJmhz28AGIIQmxiLmfpqM7c2GikaU4j.Xh87ged..K1k7CDZaMVmeP49gUxVcJO4dPgJG08h5dZvUexArdld5cIzTaxl5CNqbcu7wM.zuAmd8iKlkq6023OqE9ApAMpyObIwY8YgSRH3_vkjyc7OP.titWFbOpkstGGw.kBAHf4u9I.bcS3h1B7U3B80rquk82hl7A6sK9cXQaSYqsAi7SgpvnJdWSeLozFMXc9F4YXf49fgBiZcVaHis2TuccE_rHTIFmguPG603uJ6P7iI',
    'next-auth.csrf-token': '016caa3f88438bee1fd806d0c0108763eb3cb81871dc4d77120581c1d7bd7cb3%7C7e1ea93d7b2f2f1be609b9e3d71623557d0aca785065a6be987238956a6eeab0',
    'sidebarHiddenHubs': '[]',
    'voice-mode-activation-tooltip': '1',
    '_gcl_au': '1.1.1607421484.1749821661',
    'next-auth.callback-url': 'https%3A%2F%2Fwww.perplexity.ai%2Fapi%2Fauth%2Fsignin-callback%3Fredirect%3Dhttps%253A%252F%252Fwww.perplexity.ai%252F%253Flogin-source%253DfloatingSignup',
    'pplx.metadata': '{%22qc%22:0%2C%22qcu%22:280%2C%22qcm%22:79%2C%22qcc%22:274%2C%22qcr%22:0%2C%22qcdr%22:0%2C%22qcs%22:0%2C%22qcd%22:0%2C%22hli%22:true%2C%22hcga%22:false%2C%22hcds%22:false%2C%22hso%22:false%2C%22hfo%22:false}',
    'AWSALB': 'Ny2UV2ifO+O7KoyNiAEvUTfMPm2jGgTuyT4jFgCr0dnEctI9cWYmWwArqdkuU89MHWjoCbvkSrPTWa85bf0/dt4vtDL3MQ9Ej6GrgNTe1WPXV3ZFIQzTP5D3pBPd',
    'AWSALBCORS': 'Ny2UV2ifO+O7KoyNiAEvUTfMPm2jGgTuyT4jFgCr0dnEctI9cWYmWwArqdkuU89MHWjoCbvkSrPTWa85bf0/dt4vtDL3MQ9Ej6GrgNTe1WPXV3ZFIQzTP5D3pBPd',
    '__Secure-next-auth.session-token': 'eyJhbGciOiJkaXIiLCJlbmMiOiJBMjU2R0NNIn0..On1BQ0DqJs6b2jhz.6YfeepB0p6mEATHaagXE0qlR_yc5rKTnBsU2hIeK7Wty9wa91StuKjK5cES-dhUjiACBHl1-vk8wJz0CfqrVzI2b7mT9MnZYCNGwZTizNw8CIDqJkdIwDK8zvHjqxD3VildNdKnfoRxjmASZurAOi9xarUFWFTWw-eirGAADWZzYMTkK4tJYmRIGRMZJ2e5Yk_Rz2fng9ZW5N90Kb-cdCltpOC7oE_-fhSgmiHlCm37OTwS0QjeJtyOidCwyOBNu24wtpQ.97Kq8E6MO3uh0ClLc72plw',
    '_rdt_uuid': '1749821752527.90917331-65cc-4955-ad75-9c3bd3793e50',
    '__podscribe_perplexityai_referrer': 'https://accounts.google.co.jp/',
    '__podscribe_perplexityai_landing_url': 'https://www.perplexity.ai/?login-source=floatingSignup&login-new=false',
    '__cf_bm': 'HE3GzvB5nyL9mBSrpC9sbxjDuWupqqDgRTFS6gCqEKM-1749821760-1.0.1.1-wngYpOQvZgBQI8AlyslKfiEt50_upcMZOLN5DmhJU3AMvFDF5wRhzIuZfYTz4xqTdQdJRJ6MNnZR3Xi.t_Drb3M0OIycQxOR0N8GljzMaI8',
    '_fbp': 'fb.1.1749821759753.831608165429360035',
    '_dd_s': 'aid=cb614a2c-b942-4cb5-97f3-4d4453a1fb63&rum=0&expire=1749822667984&logs=0',
}

perplexity_cli = perplexity.Client(cookies)

# mode = ['auto', 'pro', 'reasoning', 'deep research']
# model = model for mode, which can only be used in own accounts, that is {
#     'auto': [None],
#     'pro': [None, 'sonar', 'gpt-4.5', 'gpt-4o', 'claude 3.7 sonnet', 'gemini 2.0 flash', 'grok-2'],
#     'reasoning': [None, 'r1', 'o3-mini', 'claude 3.7 sonnet'],
#     'deep research': [None]
# }
# sources = ['web', 'scholar', 'social']
# files = a dictionary which has keys as filenames and values as file data
# stream = returns a generator when enabled and just final response when disabled
# language = ISO 639 code of language you want to use
# follow_up = last query info for follow-up queries, you can directly pass response from a query, look at second example below
# incognito = Enables incognito mode, for people who are using their own account
resp = perplexity_cli.search('你背后是使用的什么模型？', mode='reasoning', model='claude 3.7 sonnet', sources=['web'], files={}, stream=False, follow_up=None, incognito=False)
print(resp)
