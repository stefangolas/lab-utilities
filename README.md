# Lab Utilities
Lab Utilities provides general-purpose code that can help with an automated lab

## Installation
`git clone https://github.com/stefangolas/lab_utilities.git` </br>
`cd lab_utilities` </br>
`pip install -e .` </br>

Use `set-lab-email` to configure the built-in email service

## Resources

Documentation for the different resources provided by this library

### ConfigLoader

The `ConfigLoader` class creates equipment interfaces defined in config.json.

```python
configuration = ConfigLoader(os.path.join(local_dir, 'config.json'))
pump_int = configuration.load_class('pump', simulating = simulating)
```

We can apply arguments such as `simulating` at run-time to create the interface. 

### email_error
`email_error` provides a very simple function that uses a gmail service to send emails from Python.

To use this function you must create a gmail account with an App Password according to this guide.

Then, apply the account information to these environment variables: `lab_utilities_email` and `lab_utilities_email_password`.

```python
email_error(recipients=email_addresses, subject = 'Robot Error', error='Exception Raised')
```

