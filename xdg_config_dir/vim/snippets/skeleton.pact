        (pact
         .given('State')
         .upon_receiving('Description') 
         .with_request('GET', '/api/thing')
         .will_respond_with(200, body=expected))
        with pact:
