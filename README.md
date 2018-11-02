# santastic
secret santa organizer, emailer

Provides a gift-giving circle working with potential group-specific limitations. For instance, for organizations where you want to force the members of one household to get names from a different household.

Example (included in sample.json):
- House 1, members Alice and Bob.
- House 2, members Carl and Donna

In this example, we want to prevent Alice from getting Bob (and vice versa), and prevent Carl from getting Donna (and vice versa).
Potential outcomes are:

- alice->carl->bob->donna->alice
- alice->donna->bob->carl->alice

We would denote this in an organization's config .json using "family" groups.

You can run Santastic by using the following command:
```
python3 santastic.py -c sample.json
```

## TODO
- Add support to send emails to candidates
- Add GUI
- Add support to retrieve a specific member's targets
- Add support for multiple unique pickings
